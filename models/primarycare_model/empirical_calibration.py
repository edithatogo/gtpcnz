"""Empirical calibration pipeline for linked NZ data.

The pipeline is conservative: if linked inputs are unavailable or insufficient,
it stays on the public-data benchmark claim boundary. When data and checks pass,
it upgrades to an empirically supported boundary for the validated dimensions.
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from models.primarycare_model.calibration_v150 import (
    DEFAULT_BASELINE,
    CalibrationParameters,
    calibrate_grid,
    simulate_months,
)

DEFAULT_LINKED_DATA_DIR = Path("data") / "linked-nz"

MONTHLY_DATA_FILES = (
    "linked-nz-monthly-observations.csv",
    "linked_nz_monthly_observations.csv",
    "empirical_monthly_observations.csv",
)

GEOGRAPHIC_DATA_FILES = (
    "linked-nz-geographic-observations.csv",
    "linked_nz_geographic_observations.csv",
)

EQUITY_DATA_FILES = (
    "linked-nz-equity-observations.csv",
    "linked_nz_equity_observations.csv",
)

SHOCK_DATA_FILES = (
    "linked-nz-known-shocks.csv",
    "linked_nz_known_shocks.csv",
)

KNOWN_INPUT_COLUMNS = {
    "month": ("month", "period", "time", "Date"),
    "primary_contacts": ("primary_contacts", "contacts", "appointments", "visits"),
    "unmet_need_index": ("unmet_need", "unmet_need_index"),
    "ed_presentations": ("ed_presentations", "ed_visits", "ed_events"),
    "ambulance_conveyances": ("ambulance_conveyances", "ambulance_events"),
    "public_cost": ("public_cost", "public_costs", "cost"),
}

TARGET_METRICS = (
    "primary_contacts",
    "unmet_need_index",
    "ed_presentations",
    "ambulance_conveyances",
    "public_cost",
)


def _resolve_data_dir(candidate_dir: str | Path | None = None) -> Path:
    env_dir = os.getenv("GTPCNZ_LINKED_DATA_DIR")
    if candidate_dir is not None:
        return Path(candidate_dir)
    if env_dir:
        return Path(env_dir)
    return DEFAULT_LINKED_DATA_DIR


def _find_first_existing(directory: Path, candidates: tuple[str, ...]) -> Path | None:
    for candidate in candidates:
        path = directory / candidate
        if path.exists():
            return path
    return None


def _normalise_columns(df: pd.DataFrame, aliases: tuple[str, ...]) -> str | None:
    lowered = {str(c).lower(): str(c) for c in df.columns if isinstance(c, str)}
    for alias in aliases:
        if alias.lower() in lowered:
            return lowered[alias.lower()]
    return None


def _coerce_month_column(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    month_col = _normalise_columns(working, KNOWN_INPUT_COLUMNS["month"])
    if month_col is None:
        raise ValueError("missing month column")

    parsed = pd.to_datetime(working[month_col], errors="coerce")
    if parsed.notna().any():
        working["month"] = parsed.dt.to_period("M").astype("int64")
    else:
        working["month"] = pd.to_numeric(working[month_col], errors="coerce")

    working = working.dropna(subset=["month"]).copy()
    working["month"] = working["month"].round().astype(int)
    return working


def _coerce_numeric_series(values: pd.Series, key: str) -> pd.Series:
    coerced = pd.to_numeric(values, errors="coerce")
    if coerced.isna().all():
        raise ValueError(f"missing usable numeric values for {key}")
    return coerced.fillna(float(coerced.mean()))


def _coerce_required_frame(
    path: Path,
    required: list[str],
    keep: tuple[str, ...] = (),
) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.empty:
        return df
    working = _coerce_month_column(df)
    if working.empty:
        raise ValueError(f"{path} has no usable month values")

    out = pd.DataFrame({"month": working["month"]})
    for key in required:
        col = _normalise_columns(working, KNOWN_INPUT_COLUMNS[key])
        if col is None:
            raise ValueError(f"{path} missing required column for {key}")
        out[key] = _coerce_numeric_series(working[col], key)
    for key in keep:
        if key not in working.columns:
            raise ValueError(f"{path} missing required column for {key}")
        out[key] = working[key]

    out = out.sort_values("month").reset_index(drop=True)
    out["month"] = out["month"].astype(int) - int(out["month"].min()) + 1
    return out.dropna().reset_index(drop=True)


def _safe_score(pred: pd.DataFrame, observed: pd.DataFrame, keys: tuple[str, ...]) -> float:
    if pred.empty or observed.empty:
        return float("inf")
    errors = []
    for key in keys:
        pred_v = pred[key].to_numpy(dtype=float)
        obs_v = observed[key].to_numpy(dtype=float)
        if len(pred_v) != len(obs_v) or len(obs_v) == 0:
            return float("inf")
        scale = max(float(np.mean(np.abs(obs_v))), 1.0)
        errors.append(float(np.sqrt(np.mean((pred_v - obs_v) ** 2)) / scale))
    return float(np.mean(errors))


def _simulate_baseline(metrics_len: int, params: CalibrationParameters) -> pd.DataFrame:
    return simulate_months(params, DEFAULT_BASELINE, months=metrics_len)


def _fit_parameters(observed: pd.DataFrame) -> CalibrationParameters:
    return calibrate_grid(
        observed,
        starting=CalibrationParameters(
            marginal_supply_response=0.30,
            unmet_need_to_ed_rate=0.25,
            copayment_elasticity=0.20,
            ambulance_deflection_rate=0.20,
            acc_stabilisation_effect=0.12,
            scope_supply_multiplier=0.20,
        ),
    )


def _calc_profile_bounds(
    observed: pd.DataFrame,
    fit: CalibrationParameters,
    baseline_score: float,
    tol: float = 0.20,
) -> dict[str, tuple[float, float]]:
    bounds: dict[str, tuple[float, float]] = {}
    base = asdict(fit)
    for key, current in base.items():
        if key in {"base_primary_contacts", "base_ed_presentations", "base_public_cost"}:
            continue
        lo = current
        hi = current
        for direction in (-1.0, 1.0):
            trial = current
            step = 0.03 if direction > 0 else -0.03
            while 0.01 <= trial + step <= 0.95:
                trial += step
                candidate = dict(base)
                candidate[key] = trial
                params = CalibrationParameters(**candidate)
                score = _safe_score(
                    _simulate_baseline(len(observed), params),
                    observed,
                    TARGET_METRICS,
                )
                if score <= baseline_score * (1 + tol):
                    if direction > 0:
                        hi = max(hi, trial)
                    else:
                        lo = min(lo, trial)
                else:
                    break
        bounds[key] = (round(float(max(0.01, lo - 0.01)), 3), round(float(min(0.95, hi + 0.01)), 3))
    return bounds


def _load_grouped_shocks(path: Path | None) -> pd.DataFrame:
    if path is None or not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def _validate_shocks(
    observations: pd.DataFrame,
    params: CalibrationParameters,
    shock_df: pd.DataFrame,
) -> dict[str, Any]:
    if shock_df.empty:
        return {"status": False, "passed": False, "message": "no known-shock table available"}

    required = ("shock_month", "shock_type")
    for field in required:
        if field not in shock_df.columns:
            return {"status": False, "passed": False, "message": f"shock file missing {field}"}

    baseline = _simulate_baseline(len(observations), params)
    checks = []
    for _, row in shock_df.iterrows():
        month = int(row.get("shock_month", 0))
        if month <= 0 or month >= len(observations):
            continue

        delta = float(row.get("shock_delta", 0.10))
        shock_type = str(row.get("shock_type", "")).lower()
        metric = str(row.get("target_metric", "primary_contacts")).lower()
        expected = int(row.get("expected_direction", 0))

        shock_inputs = DEFAULT_BASELINE
        if "copayment" in shock_type:
            shock_inputs = DEFAULT_BASELINE.__class__(
                **{**asdict(DEFAULT_BASELINE), "copayment_level": max(0.01, min(0.95, DEFAULT_BASELINE.copayment_level + delta))}
            )
        elif "scope" in shock_type:
            shock_inputs = DEFAULT_BASELINE.__class__(
                **{**asdict(DEFAULT_BASELINE), "scope_flexibility": max(0.01, min(0.95, DEFAULT_BASELINE.scope_flexibility + delta))}
            )
        elif "acc" in shock_type:
            shock_inputs = DEFAULT_BASELINE.__class__(
                **{**asdict(DEFAULT_BASELINE), "acc_activity_strength": max(0.01, min(0.95, DEFAULT_BASELINE.acc_activity_strength + delta))}
            )
        elif "ambulance" in shock_type:
            shock_inputs = DEFAULT_BASELINE.__class__(
                **{**asdict(DEFAULT_BASELINE), "ambulance_alternative_strength": max(0.01, min(0.95, DEFAULT_BASELINE.ambulance_alternative_strength + delta))}
            )

        shocked = simulate_months(params, shock_inputs, months=len(observations))
        if metric not in shocked.columns or metric not in baseline.columns:
            continue

        before = float(observations[metric].iloc[:month].mean())
        after = float(observations[metric].iloc[month:].mean())
        pred_before = float(shocked[metric].iloc[:month].mean())
        pred_after = float(shocked[metric].iloc[month:].mean())
        obs_delta = np.sign(after - before)
        pred_delta = np.sign(pred_after - pred_before)
        if expected:
            expected_sign = np.sign(expected or 1)
            checks.append(int(obs_delta) == int(expected_sign * pred_delta))
        else:
            checks.append(int(obs_delta) == int(pred_delta))

    if not checks:
        return {"status": False, "passed": False, "message": "shock table present but no compatible rows"}
    return {
        "status": True,
        "passed": all(checks),
        "message": f"shock checks: {sum(checks)}/{len(checks)} passed",
    }


def _validate_equity(observations: pd.DataFrame, params: CalibrationParameters, equity_df: pd.DataFrame) -> dict[str, Any]:
    if equity_df.empty:
        return {"status": False, "passed": False, "message": "equity file missing"}
    group_col = "equity_group" if "equity_group" in equity_df.columns else ("group" if "group" in equity_df.columns else None)
    if group_col is None:
        return {"status": False, "passed": False, "message": "equity file missing group column"}

    observed = equity_df.groupby(group_col)["primary_contacts"].mean().sort_index()
    if observed.empty or observed.size < 2:
        return {"status": False, "passed": False, "message": "equity file has insufficient groups"}

    proxy = None
    for candidate in ("unmet_need_index", "ed_presentations", "ambulance_conveyances", "public_cost"):
        if candidate in equity_df.columns:
            proxy = candidate
            break
    if proxy is None:
        return {"status": False, "passed": False, "message": "equity file missing equity proxy metric"}

    predicted = equity_df.groupby(group_col)[proxy].mean().sort_index()
    if predicted.size != observed.size:
        return {
            "status": False,
            "passed": False,
            "message": "equity file missing comparable groups between contacts and proxy",
        }

    corr = observed.corr(predicted)
    if pd.isna(corr):
        return {"status": False, "passed": False, "message": "equity check failed (insufficient variation in predicted signal)"}

    return {
        "status": True,
        "passed": float(abs(corr)) >= 0.2,
        "message": f"equity monotonicity check via {proxy} correlation={corr:.2f}",
    }


def _validate_geographic(
    observations: pd.DataFrame,
    params: CalibrationParameters,
    geographic_df: pd.DataFrame,
) -> dict[str, Any]:
    if geographic_df.empty:
        return {"status": False, "passed": False, "message": "geographic file missing"}

    locality_col = "locality" if "locality" in geographic_df.columns else ("region" if "region" in geographic_df.columns else None)
    if locality_col is None:
        return {"status": False, "passed": False, "message": "geographic file missing locality column"}

    by_locality = geographic_df.groupby(locality_col)["primary_contacts"].mean()
    if by_locality.empty:
        return {"status": False, "passed": False, "message": "geographic file has no grouped observations"}

    share = by_locality / max(by_locality.sum(), 1.0)
    pred = _simulate_baseline(len(observations), params)
    expected_total = pred["primary_contacts"].mean()
    predicted = share * expected_total
    mae = float(np.mean(np.abs(predicted - by_locality))) / max(float(by_locality.mean()), 1.0)
    return {
        "status": True,
        "passed": mae <= 0.6,
        "metric": mae,
        "message": f"geographic MAE share={mae:.3f}",
    }


def _validate_temporal_holdout(observations: pd.DataFrame) -> dict[str, Any]:
    n = len(observations)
    if n < 24:
        return {"status": False, "passed": False, "message": "insufficient months for temporal split"}

    split = n * 3 // 4
    train = observations.iloc[:split].copy()
    test = observations.iloc[split:].copy()
    if train.empty or test.empty:
        return {"status": False, "passed": False, "message": "insufficient rows for temporal split"}

    train_fit = _fit_parameters(train)
    pred = _simulate_baseline(len(test), train_fit)
    score = _safe_score(pred, test, TARGET_METRICS)
    return {"status": True, "passed": score <= 0.45, "metric": float(score), "message": f"temporal holdout score={score:.3f}"}


@dataclass(frozen=True)
class CalibrationValidationResult:
    name: str
    status: str
    message: str
    metric: float | None = None


@dataclass(frozen=True)
class LinkedCalibrationSummary:
    available: bool
    supported_where_valid: bool
    in_sample_score: float | None
    holdout_score: float | None
    parameter_estimates: dict[str, float]
    parameter_bounds: dict[str, tuple[float, float]]
    validation: tuple[CalibrationValidationResult, ...]
    source_monthly: str | None = None
    source_geographic: str | None = None
    source_equity: str | None = None
    source_shock: str | None = None


def load_linked_inputs(
    linked_dir: str | Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    base_dir = _resolve_data_dir(linked_dir)
    if not base_dir.exists():
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    monthly_path = _find_first_existing(base_dir, MONTHLY_DATA_FILES)
    geographic_path = _find_first_existing(base_dir, GEOGRAPHIC_DATA_FILES)
    equity_path = _find_first_existing(base_dir, EQUITY_DATA_FILES)
    shock_path = _find_first_existing(base_dir, SHOCK_DATA_FILES)

    monthly = _coerce_required_frame(monthly_path, list(TARGET_METRICS)) if monthly_path else pd.DataFrame()
    geographic = _coerce_required_frame(
        geographic_path,
        ["primary_contacts"],
        keep=("locality", "unmet_need_index", "ed_presentations", "ambulance_conveyances", "public_cost"),
    ) if geographic_path else pd.DataFrame()
    equity = _coerce_required_frame(
        equity_path,
        ["primary_contacts"],
        keep=("equity_group", "unmet_need_index", "ed_presentations", "ambulance_conveyances", "public_cost"),
    ) if equity_path else pd.DataFrame()
    shock = _load_grouped_shocks(shock_path)
    return monthly, geographic, equity, shock


def build_claim_boundary_text(summary: LinkedCalibrationSummary | None = None) -> str:
    if summary is None or not summary.available:
        return (
            "This is a public-data anchored benchmark and educational explainer. "
            "It is not linked-data calibrated and not a patient-level forecast. "
            "It should not be used to claim precise fiscal savings, hospital-demand reductions, "
            "workforce effects, or implementation impacts."
        )
    if not summary.supported_where_valid:
        return (
            "This is a public-data anchored benchmark with calibration inputs. "
            "Calibration checks are incomplete, so claims are only empirically supported where valid; "
            "it is not a patient-level forecast."
        )
    return (
        "This is an empirically supported benchmark where valid. "
        "Published aggregate calibration checks have cleared the documented public validation gates where available. "
        "It is still an indexed benchmark and is not a patient-level forecast."
    )


def run_empirical_calibration_pipeline(
    linked_dir: str | Path | None = None,
    tolerance_temporal_score: float = 0.45,
) -> LinkedCalibrationSummary:
    monthly_df, geographic_df, equity_df, shock_df = load_linked_inputs(linked_dir)
    if monthly_df.empty or len(monthly_df) < 12:
        return LinkedCalibrationSummary(
            available=False,
            supported_where_valid=False,
            in_sample_score=None,
            holdout_score=None,
            parameter_estimates={},
            parameter_bounds={},
            validation=(
                CalibrationValidationResult(
                    name="data",
                    status="missing",
                    message="linked monthly observations unavailable or too short",
                ),
            ),
        )

    fitted = _fit_parameters(monthly_df)
    in_sample = _safe_score(_simulate_baseline(len(monthly_df), fitted), monthly_df, TARGET_METRICS)
    bounds = _calc_profile_bounds(monthly_df, fitted, in_sample)

    temporal = _validate_temporal_holdout(monthly_df)
    geographic = _validate_geographic(monthly_df, fitted, geographic_df)
    equity = _validate_equity(monthly_df, fitted, equity_df)
    shock = _validate_shocks(monthly_df, fitted, shock_df)

    validation = (
        CalibrationValidationResult(
            name="baseline_fit",
            status="passed" if in_sample <= 0.45 else "failed",
            message=f"in-sample normalized RMSE={in_sample:.3f}",
            metric=in_sample,
        ),
        CalibrationValidationResult(
            name="temporal_holdout",
            status="passed" if temporal.get("passed") else "skipped" if not temporal.get("status") else "failed",
            message=temporal["message"],
            metric=temporal.get("metric"),
        ),
        CalibrationValidationResult(
            name="geographic",
            status="passed" if geographic.get("passed") else "skipped" if not geographic.get("status") else "failed",
            message=geographic["message"],
            metric=geographic.get("metric"),
        ),
        CalibrationValidationResult(
            name="equity",
            status="passed" if equity.get("passed") else "skipped" if not equity.get("status") else "failed",
            message=equity["message"],
            metric=equity.get("metric"),
        ),
        CalibrationValidationResult(
            name="known_shock",
            status="passed" if shock.get("passed") else "skipped" if not shock.get("status") else "failed",
            message=shock["message"],
            metric=shock.get("metric"),
        ),
    )

    required_passes = {"baseline_fit", "temporal_holdout", "geographic", "equity", "known_shock"}
    passed_all = all(item.name not in required_passes or item.status == "passed" for item in validation)

    return LinkedCalibrationSummary(
        available=True,
        supported_where_valid=passed_all and in_sample <= tolerance_temporal_score,
        in_sample_score=float(in_sample),
        holdout_score=temporal.get("metric") if temporal.get("metric") is not None else None,
        parameter_estimates={k: float(v) for k, v in asdict(fitted).items() if k not in {"base_primary_contacts", "base_ed_presentations", "base_public_cost"}},
        parameter_bounds=bounds,
        validation=validation,
        source_monthly="linked-nz-monthly-observations.csv" if not monthly_df.empty else None,
        source_geographic="linked-nz-geographic-observations.csv" if not geographic_df.empty else None,
        source_equity="linked-nz-equity-observations.csv" if not equity_df.empty else None,
        source_shock="linked-nz-known-shocks.csv" if not shock_df.empty else None,
    )


def calibration_ready_rows(summary: LinkedCalibrationSummary) -> tuple[tuple[str, str, str, str], ...]:
    return (
        (
            "Primary care appointments",
            "NPCD booking and encounter fields",
            "Ready" if summary.supported_where_valid else ("In progress" if summary.available else "Needed"),
            "Access and waiting-time calibration",
        ),
        (
            "Capitation and payment rules",
            "Rate tables, pass-through and programme funding",
            "Ready for calibration" if summary.available else "Needed",
            "Practice revenue and marginal-supply calibration",
        ),
        (
            "Co-payments",
            "Practice fee schedules and patient out-of-pocket costs",
            "Ready for calibration" if summary.available else "Needed",
            "Demand/equity response",
        ),
        (
            "Ambulance pathways",
            "Conveyance, hear-and-treat, treat-and-refer, handover delay",
            "Ready for calibration" if summary.available else "Needed",
            "Hospital-deflection calibration",
        ),
        (
            "ACC treatment payments",
            "Cost of Treatment Regulations, contracts, claims",
            "Ready for calibration" if summary.available else "Needed",
            "Cross-funder and supply-stabilisation effects",
        ),
        (
            "ED and inpatient data",
            "ED presentations, admissions, diagnosis and disposition",
            "Ready for calibration" if summary.available and summary.supported_where_valid else "In progress" if summary.available else "Needed",
            "Downstream hospital-pressure validation",
        ),
        (
            "Workforce and scope",
            "Provider type, FTE, location, prescribing/scope rules",
            "Ready for calibration" if summary.available else "Needed",
            "Scope-enabled supply calibration",
        ),
        (
            "Stakeholder validation",
            "Game scoring and decision weights",
            "Needs face-validity review",
            "Decision support and face validity",
        ),
    )
