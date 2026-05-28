"""Low-cost validation checks suitable for public app execution.

These functions avoid pulling in heavy dependencies such as Pandera or
PyArrow. They are designed to be cheap enough to call on every user
interaction in the Streamlit deployment.

No Streamlit imports are allowed in this module.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

# ── Parameter value validation ────────────────────────────────────────


def check_parameter_value(value: Any, definition: object) -> list[str]:
    """Validate a single parameter value against its contract definition.

    Parameters
    ----------
    value : Any
        The user-supplied value to validate.
    definition : object
        A ``ParameterDefinition`` instance (duck-typed; any object with
        ``parameter_id``, ``value_type``, ``lower_bound``, ``upper_bound``,
        and ``category_values`` attributes is accepted).

    Returns
    -------
    list[str]
        A (possibly empty) list of human-readable issue descriptions.
    """
    issues: list[str] = []

    # Duck-type the definition attributes
    try:
        param_id: str = getattr(definition, "parameter_id", "?")
        value_type: str = getattr(definition, "value_type", "?")
        lower_bound: float | None = getattr(definition, "lower_bound", None)
        upper_bound: float | None = getattr(definition, "upper_bound", None)
        category_values: tuple[str, ...] = getattr(definition, "category_values", ())
    except Exception as exc:
        return [f"cannot read definition attributes: {exc}"]

    # Type checks
    if value_type == "integer":
        if type(value) is not int:
            issues.append(f"{param_id}: expected integer, got {type(value).__name__}")
    elif value_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            issues.append(f"{param_id}: expected number, got {type(value).__name__}")
    elif value_type == "boolean":
        if not isinstance(value, bool):
            issues.append(f"{param_id}: expected boolean, got {type(value).__name__}")
    elif value_type == "categorical":
        if not isinstance(value, str):
            issues.append(f"{param_id}: expected string (categorical), got {type(value).__name__}")
        elif category_values and value not in category_values:
            valid = ", ".join(sorted(category_values))
            issues.append(f"{param_id}: {value!r} not in allowed values: {valid}")
    else:
        issues.append(f"{param_id}: unknown value_type {value_type!r}")

    # Bounds checks for numeric values (skip booleans)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        numeric = float(value)
        if lower_bound is not None and numeric < lower_bound:
            issues.append(f"{param_id}: value {value} is below lower bound {lower_bound}")
        if upper_bound is not None and numeric > upper_bound:
            issues.append(f"{param_id}: value {value} is above upper bound {upper_bound}")

    return issues


# ── Scenario override validation ──────────────────────────────────────


def check_scenario_overrides(overrides: list[dict[str, Any]], known_ids: set[str]) -> list[str]:
    """Validate override targets exist in the known scenario ID set.

    Parameters
    ----------
    overrides : list[dict[str, Any]]
        A list of override dicts, each expected to have at least a
        ``"target_id"`` key.
    known_ids : set[str]
        The set of recognised scenario IDs (e.g. ``{"F0", "F1", ...}``).

    Returns
    -------
    list[str]
        A (possibly empty) list of issue descriptions.
    """
    issues: list[str] = []
    if not overrides:
        return issues

    for i, override in enumerate(overrides):
        if not isinstance(override, dict):
            issues.append(f"override[{i}]: expected dict, got {type(override).__name__}")
            continue

        target = override.get("target_id")
        if target is None:
            issues.append(f"override[{i}]: missing 'target_id'")
        elif target not in known_ids:
            valid = ", ".join(sorted(known_ids))
            issues.append(f"override[{i}]: target_id {target!r} not in known IDs: {valid}")

    return issues


# ── Lightweight result-frame bounds check ─────────────────────────────


_SCORE_BOUNDS = {
    "hybrid_viability_score": (0.0, 100.0),
    "access_score": (0.0, 100.0),
    "supply_generation_score": (0.0, 100.0),
    "equity_legitimacy_score": (0.0, 100.0),
    "governance_resilience_score": (0.0, 100.0),
    "hospital_deflection_score": (0.0, 100.0),
    "fiscal_risk_score": (0.0, 100.0),
    "gaming_risk_score": (0.0, 100.0),
    "hospital_pressure_score": (0.0, 100.0),
}

_REQUIRED_TEXT_COLUMNS = {
    "scenario_id",
    "scenario_name",
    "description",
}

def check_result_frame_bounds(df: pd.DataFrame) -> list[str]:
    """Lightweight bounds check on a reference result DataFrame.

    This function performs the same checks as the Pandera schema but
    without importing Pandera. It is intended for use in the public
    Streamlit app where minimising dependencies is important.

    Parameters
    ----------
    df : pd.DataFrame
        The reference result frame to check.

    Returns
    -------
    list[str]
        A (possibly empty) list of issue descriptions.
    """
    issues: list[str] = []

    # Check required text columns exist
    missing_text = _REQUIRED_TEXT_COLUMNS.difference(df.columns)
    if missing_text:
        issues.append(f"missing text columns: {sorted(missing_text)}")

    # Check score columns exist and validate bounds
    for column in _SCORE_BOUNDS:
        if column not in df.columns:
            issues.append(f"missing score column: {column}")
            continue

        numeric = pd.to_numeric(df[column], errors="coerce")
        if numeric.isna().any():
            nan_count = int(numeric.isna().sum())
            issues.append(f"{column}: {nan_count} non-numeric or null value(s)")
        else:
            lo, hi = _SCORE_BOUNDS[column]
            out_of_range = ~numeric.between(lo, hi, inclusive="both")
            if out_of_range.any():
                bad_indices = out_of_range[out_of_range].index.tolist()
                bad_values = df.loc[bad_indices, column].tolist()
                issues.append(
                    f"{column}: {len(bad_indices)} value(s) outside "
                    f"[{lo}, {hi}]: {bad_values[:5]}"
                )

    # Check that scenario_id is not empty
    if "scenario_id" in df.columns:
        empty = df["scenario_id"].isna() | (df["scenario_id"].astype(str).str.strip() == "")
        if empty.any():
            issues.append(f"{int(empty.sum())} row(s) with empty scenario_id")

    # Check rank column if present
    if "rank_by_hybrid_viability" in df.columns:
        rank_numeric = pd.to_numeric(df["rank_by_hybrid_viability"], errors="coerce")
        if rank_numeric.isna().any():
            issues.append("rank_by_hybrid_viability contains non-integer values")

    return issues


# ── Issue formatting ──────────────────────────────────────────────────


def format_validation_issues(issues: list[str]) -> str:
    """Format a list of validation issues as a human-readable block.

    The output is plain text suitable for display in Streamlit's
    ``st.warning`` or ``st.error``.

    Parameters
    ----------
    issues : list[str]
        Validation issues returned by any ``check_*`` function in this
        module, or by :func:`~.pandera_schemas.validate_reference_results_frame`.

    Returns
    -------
    str
        A bullet-pointed message, or an empty string when there are no
        issues.
    """
    if not issues:
        return ""

    lines = ["**Validation issues detected:**"]
    for issue in issues:
        lines.append(f"- {issue}")

    return "\n".join(lines)

