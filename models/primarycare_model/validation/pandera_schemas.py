"""Data-frame validation with optional Pandera support.

Pandera is intentionally optional for the Streamlit deployment path. When it is
installed, the public result frame is validated through a Pandera schema; when it
is not installed, the same column and bounds checks run locally.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

try:  # pragma: no cover - exercised only in environments with pandera.
    import pandera.pandas as pa
    from pandera.typing import Series
except ImportError:  # pragma: no cover - local fallback is the normal lean path.
    pa = None  # type: ignore[assignment]
    Series = Any  # type: ignore[assignment, misc]


REFERENCE_RESULT_COLUMNS = {
    "scenario_id",
    "scenario_name",
    "description",
    "hybrid_viability_score",
    "access_score",
    "supply_generation_score",
    "equity_legitimacy_score",
    "governance_resilience_score",
    "hospital_deflection_score",
    "fiscal_risk_score",
    "gaming_risk_score",
    "hospital_pressure_score",
    "mean_last12_public_cost_index",
    "rank_by_hybrid_viability",
}

SCORE_COLUMNS = [
    "hybrid_viability_score",
    "access_score",
    "supply_generation_score",
    "equity_legitimacy_score",
    "governance_resilience_score",
    "hospital_deflection_score",
    "fiscal_risk_score",
    "gaming_risk_score",
    "hospital_pressure_score",
]


if pa is not None:  # pragma: no cover

    class ReferenceResultSchema(pa.DataFrameModel):
        class Config:
            coerce = True

        scenario_id: Series[str]
        scenario_name: Series[str]
        description: Series[str]
        hybrid_viability_score: Series[float] = pa.Field(ge=0, le=100)
        access_score: Series[float] = pa.Field(ge=0, le=100)
        supply_generation_score: Series[float] = pa.Field(ge=0, le=100)
        equity_legitimacy_score: Series[float] = pa.Field(ge=0, le=100)
        governance_resilience_score: Series[float] = pa.Field(ge=0, le=100)
        hospital_deflection_score: Series[float] = pa.Field(ge=0, le=100)
        fiscal_risk_score: Series[float] = pa.Field(ge=0, le=100)
        gaming_risk_score: Series[float] = pa.Field(ge=0, le=100)
        hospital_pressure_score: Series[float] = pa.Field(ge=0, le=100)
        mean_last12_public_cost_index: Series[float]
        rank_by_hybrid_viability: Series[int]


def validate_reference_results_frame(df: pd.DataFrame, expected_scenario_ids: set[str] | None = None) -> list[str]:
    """Return validation issues for a public reference result frame."""

    issues: list[str] = []
    missing = REFERENCE_RESULT_COLUMNS.difference(df.columns)
    if missing:
        issues.append(f"missing columns: {sorted(missing)}")
        return issues

    if pa is not None:  # pragma: no cover
        try:
            ReferenceResultSchema.validate(df, lazy=True)
        except pa.errors.SchemaErrors as exc:
            issues.append(f"pandera validation failed: {exc.failure_cases.to_dict(orient='records')}")

    for column in SCORE_COLUMNS:
        numeric = pd.to_numeric(df[column], errors="coerce")
        if numeric.isna().any():
            issues.append(f"{column} contains non-numeric or null values")
        elif not numeric.between(0, 100).all():
            issues.append(f"{column} contains values outside 0-100")

    if expected_scenario_ids is not None:
        found = set(df["scenario_id"].astype(str))
        missing_scenarios = expected_scenario_ids.difference(found)
        if missing_scenarios:
            issues.append(f"missing expected scenarios: {sorted(missing_scenarios)}")
    return issues
