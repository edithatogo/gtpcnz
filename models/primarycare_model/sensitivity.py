"""Variance-based sensitivity helpers for primary care funding models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pyarrow as pa


@dataclass(frozen=True)
class ParameterRange:
    name: str
    lower: float
    upper: float
    baseline: float


PARAMETER_RANGES: tuple[ParameterRange, ...] = (
    ParameterRange("capitation_rate", 40.0, 160.0, 80.0),
    ParameterRange("ffs_gp_visit", 20.0, 90.0, 45.0),
    ParameterRange("ffs_nurse_visit", 10.0, 50.0, 25.0),
    ParameterRange("demand_elasticity", 0.0, 0.2, 0.05),
    ParameterRange("supply_elasticity", 0.0, 0.15, 0.03),
    ParameterRange("equity_weight", 0.0, 1.0, 0.5),
    ParameterRange("wait_penalty", 0.0, 5.0, 2.0),
)


def sobol_sequence(n_points: int, n_dims: int, seed: int = 42, skip: int = 0) -> np.ndarray:
    """Generate a deterministic low-discrepancy-like sample matrix.

    This is a lightweight fallback sampler, not a full Saltelli generator. It
    gives stable bounded samples for dashboard and smoke-test use until SALib or
    the JAX lane is available.
    """
    n_total = max(1, int(n_points) + int(skip))
    rng = np.random.default_rng(seed)
    base = np.arange(n_total, dtype=float)[:, None] / n_total
    noise = rng.uniform(0.0, 0.5 / n_total, size=(n_total, n_dims))
    return np.clip((base + noise)[skip:], 0.0, 1.0)


def param_ranges_to_table() -> pa.Table:
    """Return the sensitivity parameter register as an Arrow table."""
    schema = pa.schema(
        [
            pa.field("name", pa.utf8()),
            pa.field("lower", pa.float64()),
            pa.field("upper", pa.float64()),
            pa.field("baseline", pa.float64()),
        ]
    )
    arrays = [
        pa.array([item.name for item in PARAMETER_RANGES], type=pa.utf8()),
        pa.array([item.lower for item in PARAMETER_RANGES], type=pa.float64()),
        pa.array([item.upper for item in PARAMETER_RANGES], type=pa.float64()),
        pa.array([item.baseline for item in PARAMETER_RANGES], type=pa.float64()),
    ]
    return pa.Table.from_arrays(arrays, schema=schema)


def scale_samples_to_params(samples: np.ndarray, baseline: np.ndarray | None = None) -> np.ndarray:
    """Scale unit samples around baseline values using configured ranges."""
    values = np.asarray(samples, dtype=float)
    ranges = PARAMETER_RANGES[: values.shape[-1]]
    lower = np.asarray([item.lower for item in ranges], dtype=float)
    upper = np.asarray([item.upper for item in ranges], dtype=float)
    if baseline is not None:
        centre = np.asarray(baseline, dtype=float)
        width = upper - lower
        return np.clip(centre + (values - 0.5) * width, lower, upper)
    return lower + values * (upper - lower)


def _default_objective(params: np.ndarray) -> np.ndarray:
    """Simple deterministic policy score for sensitivity smoke runs."""
    capitation, ffs_gp, ffs_nurse, demand_elast, supply_elast, equity_weight, wait_penalty = params.T
    supply_signal = 0.25 * capitation + 0.55 * ffs_gp + 0.35 * ffs_nurse
    access_score = supply_signal * (1.0 + supply_elast) - wait_penalty * 8.0
    demand_pressure = 500.0 * demand_elast
    equity_adjustment = 20.0 * equity_weight
    return access_score - demand_pressure + equity_adjustment


def compute_sobol_indices(
    eval_fn=None,
    n_params: int = 7,
    n_eval: int = 256,
    seed: int = 42,
) -> dict[str, object]:
    """Compute stable first-order and total-effect sensitivity proxies."""
    n_params = max(1, min(int(n_params), len(PARAMETER_RANGES)))
    n_eval = max(16, int(n_eval))
    rng = np.random.default_rng(seed)
    samples = rng.uniform(size=(n_eval, n_params))
    params = scale_samples_to_params(samples)
    objective = eval_fn or _default_objective
    y = np.asarray(objective(params), dtype=float)
    total_var = float(np.var(y)) + 1e-12

    first_order: list[float] = []
    total_effect: list[float] = []
    for idx in range(n_params):
        corr = np.corrcoef(params[:, idx], y)[0, 1]
        if not np.isfinite(corr):
            corr = 0.0
        first_order.append(float(np.clip(corr * corr, 0.0, 1.0)))

        permuted = params.copy()
        permuted[:, idx] = permuted[rng.permutation(n_eval), idx]
        y_permuted = np.asarray(objective(permuted), dtype=float)
        total_effect.append(float(np.clip(np.mean((y - y_permuted) ** 2) / (2.0 * total_var), 0.0, 1.0)))

    return {
        "param_names": [item.name for item in PARAMETER_RANGES[:n_params]],
        "S1": np.asarray(first_order),
        "ST": np.asarray(total_effect),
        "n_params": n_params,
        "n_eval": n_eval,
    }


__all__ = [
    "ParameterRange",
    "PARAMETER_RANGES",
    "compute_sobol_indices",
    "param_ranges_to_table",
    "sobol_sequence",
    "scale_samples_to_params",
]
