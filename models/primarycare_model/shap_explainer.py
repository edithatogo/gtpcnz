"""SHAP attribution helpers for primary care funding simulations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
import pyarrow as pa

try:
    import jax.numpy as jnp
except ModuleNotFoundError:  # pragma: no cover - lean runtime fallback
    jnp = None

try:
    import shap
except ImportError:  # pragma: no cover - optional analytical dependency
    shap = None

from .data_layer import shap_records_to_table, shap_summary_to_table


FEATURE_NAMES: list[str] = [
    "capitation_rate",
    "ffs_gp_fee",
    "ffs_nurse_fee",
    "demand_elasticity",
    "supply_elasticity",
    "equity_weight",
    "waiting_penalty",
]

FEATURE_SHORT_NAMES: dict[str, str] = {
    "capitation_rate": "Cap Rate",
    "ffs_gp_fee": "FFS GP",
    "ffs_nurse_fee": "FFS Nurse",
    "demand_elasticity": "Demand Elast.",
    "supply_elasticity": "Supply Elast.",
    "equity_weight": "Equity Wt.",
    "waiting_penalty": "Wait Penalty",
}

TARGET_METRICS: dict[str, int] = {
    "total_funding": 5,
    "total_visits": 2,
    "avg_wait_time_days": 6,
    "unmet_demand": 7,
    "total_providers": 1,
}


class JaxMCPredictor:
    """Sklearn-compatible predictor wrapping a JAX trajectory function."""

    def __init__(
        self,
        trajectory_fn: Callable[[jnp.ndarray, int, Any], jnp.ndarray],
        n_steps: int,
        target_metric: str = "total_funding",
        aggregate_fn: Optional[Callable[[np.ndarray], float]] = None,
    ) -> None:
        self._fn = trajectory_fn
        self._n_steps = n_steps
        self._target_idx = TARGET_METRICS.get(target_metric, 5)
        self._aggregate_fn = aggregate_fn or (lambda arr: float(np.mean(arr)))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target metric from a parameter matrix."""
        results: list[float] = []
        for row in X:
            array_module = jnp if jnp is not None else np
            params = array_module.asarray(row, dtype=np.float32)
            key = array_module.asarray([0, 0], dtype=np.uint32)
            trajectory = self._fn(params, self._n_steps, key)
            values = np.asarray(trajectory[:, self._target_idx])
            results.append(self._aggregate_fn(values))
        return np.asarray(results, dtype=np.float64)


@dataclass
class SHAPAttribution:
    """SHAP attribution result with Arrow serialisation helpers."""

    scenario_name: str
    feature_names: list[str]
    shap_values: np.ndarray
    base_values: np.ndarray
    data: np.ndarray
    explainer_type: str
    target_metric: str = "total_funding"
    batch_indices: Optional[np.ndarray] = None

    def _feature_matrix(self) -> np.ndarray:
        values = np.asarray(self.shap_values)
        if values.ndim == 3:
            values = values[0]
        return values

    def to_arrow_records(self) -> list[dict[str, Any]]:
        """Flatten SHAP values into one row per sample-feature pair."""
        records: list[dict[str, Any]] = []
        values = self._feature_matrix()
        base_value = (
            float(self.base_values)
            if np.ndim(self.base_values) == 0
            else float(np.mean(self.base_values))
        )

        for row_idx in range(values.shape[0]):
            batch_idx = int(self.batch_indices[row_idx]) if self.batch_indices is not None else row_idx
            for feature_idx, feature_name in enumerate(self.feature_names):
                records.append({
                    "scenario_name": self.scenario_name,
                    "month": 0,
                    "batch_idx": batch_idx,
                    "feature_name": feature_name,
                    "shap_value": float(values[row_idx, feature_idx]),
                    "feature_value": float(self.data[row_idx, feature_idx]) if self.data is not None else None,
                    "base_value": base_value,
                    "explainer_type": self.explainer_type,
                })
        return records

    def to_arrow_table(self) -> pa.Table:
        """Serialise full attributions to an Arrow table."""
        return shap_records_to_table(self.to_arrow_records())

    def compute_summary(self) -> list[dict[str, Any]]:
        """Aggregate SHAP values by feature and rank absolute importance."""
        values = self._feature_matrix()
        mean_abs = np.mean(np.abs(values), axis=0)
        std_values = np.std(values, axis=0)
        mean_features = (
            np.mean(self.data, axis=0)
            if self.data is not None
            else np.full(values.shape[1], np.nan)
        )

        records: list[dict[str, Any]] = []
        for rank, feature_idx in enumerate(np.argsort(-mean_abs), start=1):
            mean_feature = mean_features[feature_idx]
            records.append({
                "scenario_name": self.scenario_name,
                "feature_name": self.feature_names[feature_idx],
                "mean_abs_shap": float(mean_abs[feature_idx]),
                "std_shap": float(std_values[feature_idx]),
                "mean_feature_value": float(mean_feature) if not np.isnan(mean_feature) else None,
                "importance_rank": rank,
            })
        return records

    def to_summary_table(self) -> pa.Table:
        """Serialise feature importance summary to an Arrow table."""
        return shap_summary_to_table(self.compute_summary())


class TreeSHAPExplainer:
    """TreeSHAP wrapper for tree-based surrogate models."""

    def __init__(self, model: Any) -> None:
        self._model = model
        self._explainer: Optional[Any] = None

    def fit(self, background_data: Optional[np.ndarray] = None) -> None:
        """Initialise the TreeExplainer."""
        if shap is None:
            raise ImportError("Install shap to use TreeSHAPExplainer.")
        self._explainer = (
            shap.TreeExplainer(self._model, data=background_data)
            if background_data is not None
            else shap.TreeExplainer(self._model)
        )

    def explain(
        self,
        X: np.ndarray,
        scenario_name: str = "default",
        target_metric: str = "total_funding",
        batch_indices: Optional[np.ndarray] = None,
    ) -> SHAPAttribution:
        """Compute TreeSHAP values for input samples."""
        if self._explainer is None:
            raise RuntimeError("TreeSHAPExplainer is not fitted.")

        shap_values = self._explainer.shap_values(X)
        values = np.asarray(shap_values if not isinstance(shap_values, list) else shap_values)
        if values.ndim == 2:
            values = values[np.newaxis, ...]

        return SHAPAttribution(
            scenario_name=scenario_name,
            feature_names=FEATURE_NAMES[: X.shape[1]],
            shap_values=values,
            base_values=np.asarray(self._explainer.expected_value),
            data=X,
            explainer_type="TreeSHAP",
            target_metric=target_metric,
            batch_indices=batch_indices if batch_indices is not None else np.arange(X.shape[0]),
        )


class KernelSHAPExplainer:
    """KernelSHAP wrapper for model-agnostic JAX simulation attribution."""

    def __init__(self, predictor: JaxMCPredictor) -> None:
        self._predictor = predictor
        self._explainer: Optional[Any] = None

    def fit(self, background: np.ndarray) -> None:
        """Fit KernelExplainer on a background feature matrix."""
        if shap is None:
            raise ImportError("Install shap to use KernelSHAPExplainer.")
        self._explainer = shap.KernelExplainer(self._predictor.predict, background)

    def explain(
        self,
        X: np.ndarray,
        scenario_name: str = "default",
        target_metric: str = "total_funding",
        n_samples: int = 128,
        batch_indices: Optional[np.ndarray] = None,
        nsamples: int = 2000,
        **kwargs: Any,
    ) -> SHAPAttribution:
        """Compute KernelSHAP values for a bounded sample of rows."""
        if self._explainer is None:
            raise RuntimeError("KernelSHAPExplainer is not fitted.")

        n_explain = min(n_samples, X.shape[0])
        X_sub = X[:n_explain]
        shap_values = self._explainer.shap_values(X_sub, nsamples=nsamples, **kwargs)
        values = np.asarray(shap_values)
        if values.ndim == 2:
            values = values[np.newaxis, ...]

        return SHAPAttribution(
            scenario_name=scenario_name,
            feature_names=FEATURE_NAMES[: X.shape[1]],
            shap_values=values,
            base_values=np.asarray(self._explainer.expected_value),
            data=X_sub,
            explainer_type="KernelSHAP",
            target_metric=target_metric,
            batch_indices=(batch_indices[:n_explain] if batch_indices is not None else np.arange(n_explain)),
        )


__all__ = [
    "FEATURE_NAMES",
    "FEATURE_SHORT_NAMES",
    "TARGET_METRICS",
    "JaxMCPredictor",
    "SHAPAttribution",
    "TreeSHAPExplainer",
    "KernelSHAPExplainer",
]
