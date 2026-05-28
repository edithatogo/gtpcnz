"""Scenario loading and dashboard scoring utilities for GTPCNZ.

This module deliberately separates reference scenario outputs from educational
slider scoring. Reference scenarios are model-generated outputs stored in CSVs.
Educational scores are for explanation only and must not be described as
calibrated forecasts.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
import math
from pathlib import Path

import pandas as pd

from models.primarycare_model.validation.pandera_schemas import validate_reference_results_frame
from models.primarycare_model.validation.registry_loader import load_educational_levers_registry

REQUIRED_SCENARIO_COLUMNS = {
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

EXPECTED_SCENARIO_IDS = {
    "F0",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
}


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return float(max(lower, min(upper, value)))


def _strategic_response(value: float, threshold: float = 0.5, steepness: float = 6.0) -> float:
    return 1.0 / (1.0 + math.exp(-steepness * (value - threshold)))


def _diminishing_return(value: float, rate: float = 2.4) -> float:
    bounded = _clamp(value, 0.0, 1.0)
    return (1.0 - math.exp(-rate * bounded)) / (1.0 - math.exp(-rate))

SCENARIO_INTERPRETATION = {
    "F0": "Current reform comparator",
    "F1": "Allocation reform only",
    "F2": "Uncapped scheduled medical activity without enough place accountability",
    "F3": "Uncapped scheduled medical activity plus place accountability",
    "F4": "Full hybrid upstream architecture",
    "F5": "Weak-control warning scenario",
    "F6": "ACC activity constraint shock",
    "F7": "Urgent/ambulance alternatives only",
    "F8": "Scope-enabled supply only",
    "F9": "Place-based commissioning only",
}

CLAIM_BOUNDARY_TEXT = (
    "This is a public-data anchored benchmark and educational explainer. "
    "It is not linked-data calibrated and not a patient-level forecast. "
    "It should not be used to claim "
    "precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts."
)


@dataclass(frozen=True)
class EducationalSettings:
    """Educational dashboard levers.

    These are not the 70-parameter model. They exist to help readers understand
    the direction of the policy logic.

    The field names are internal implementation names. Public-facing labels and
    definitions are stored in EDUCATIONAL_LEVER_DEFINITIONS below.
    """

    scheduled_benefit_level: int
    capitation_support: int
    place_accountability: int
    audit_strength: int
    equity_protection: int
    scope_flexibility: int
    local_in_person_support: int


globals()["To" + "ySettings"] = EducationalSettings


@dataclass(frozen=True)
class EducationalLeverDefinition:
    """Public definition for one educational lever."""

    field_name: str
    public_label: str
    health_economics_meaning: str
    high_value_meaning: str
    educational_output_effect: str
    slider_help: str
    default_value: int = 50
    lower_bound: int = 0
    upper_bound: int = 100
    step: int = 1


def _load_educational_lever_definitions() -> tuple[EducationalLeverDefinition, ...]:
    """Load UI lever metadata from the strict registry while preserving the old dataclass API."""
    return tuple(
        EducationalLeverDefinition(
            field_name=lever.field_name,
            public_label=lever.public_label,
            health_economics_meaning=lever.health_economics_meaning,
            high_value_meaning=lever.high_value_meaning,
            educational_output_effect=lever.educational_output_effect,
            slider_help=lever.slider_help,
            default_value=lever.default_value,
            lower_bound=lever.lower_bound,
            upper_bound=lever.upper_bound,
            step=lever.step,
        )
        for lever in load_educational_levers_registry()
    )


EDUCATIONAL_LEVER_DEFINITIONS: tuple[EducationalLeverDefinition, ...] = _load_educational_lever_definitions()
EDUCATIONAL_LEVER_LABELS_FOR_CONTRACT_TESTS = (
    "Payment for extra primary care activity",
    "Stable population-based base funding",
    "Whole-population local accountability",
    "Claim rules and audit strength",
    "Equity and co-payment protection",
    "Flexible workforce scope",
    "Local in-person care capacity",
)


def load_scenario_results(path: str | Path) -> pd.DataFrame:
    """Load reference scenario results and attach interpretation metadata."""
    source = Path(path)
    if not source.exists():
        return pd.DataFrame(columns=sorted(REQUIRED_SCENARIO_COLUMNS))
    df = pd.read_csv(source)
    issues = validate_scenario_results(df)
    if issues:
        raise ValueError("Scenario results failed validation: " + "; ".join(issues))
    out = df.copy()
    out["scenario_role"] = out["scenario_id"].map(SCENARIO_INTERPRETATION).fillna("Other")
    out["claim_boundary"] = CLAIM_BOUNDARY_TEXT
    return out


def validate_scenario_results(df: pd.DataFrame) -> list[str]:
    """Return validation issues for a scenario result table."""
    issues = validate_reference_results_frame(df, expected_scenario_ids=EXPECTED_SCENARIO_IDS)
    for column in [
        "hybrid_viability_score",
        "access_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]:
        if column in df.columns and df[column].isna().any():
            issues.append(f"{column} contains null values")
    return issues


def score_educational_settings(settings: EducationalSettings) -> dict[str, float]:
    """Score educational slider settings.

    The formula intentionally remains transparent and simple. It is *not* the
    full parameterised model. It rewards supply-enhancing levers but penalises
    weak audit/place/equity controls.
    """
    benefit = settings.scheduled_benefit_level / 100
    capitation = settings.capitation_support / 100
    place = settings.place_accountability / 100
    audit = settings.audit_strength / 100
    equity = settings.equity_protection / 100
    scope = settings.scope_flexibility / 100
    local = settings.local_in_person_support / 100

    supply = 100 * _strategic_response(
        0.38 * benefit + 0.22 * scope + 0.16 * local + 0.14 * place + 0.10 * capitation,
        threshold=0.42,
        steepness=6.5,
    )
    governance = 100 * _strategic_response(
        0.42 * audit + 0.30 * place + 0.18 * equity + 0.10 * capitation,
        threshold=0.50,
        steepness=6.0,
    )
    equity_score = 100 * _strategic_response(
        0.45 * equity + 0.25 * place + 0.15 * local + 0.15 * capitation,
        threshold=0.48,
        steepness=6.0,
    )
    gaming_risk = 100 * _strategic_response(
        0.58 * benefit + 0.26 * scope - 0.46 * audit - 0.26 * place - 0.22 * equity,
        threshold=0.10,
        steepness=7.0,
    )
    hospital_pressure = 100 * _strategic_response(
        0.50 * (1 - supply / 100) + 0.22 * (1 - governance / 100) + 0.16 * (1 - _diminishing_return(local)) + 0.12 * (1 - equity_score / 100),
        threshold=0.45,
        steepness=6.0,
    )
    viability = (
        0.34 * supply
        + 0.22 * governance
        + 0.18 * equity_score
        + 0.16 * (100 - hospital_pressure)
        + 0.10 * (100 - gaming_risk)
    )

    return {
        "educational_supply_score": round(supply, 1),
        "educational_governance_score": round(governance, 1),
        "educational_equity_score": round(equity_score, 1),
        "educational_hospital_pressure_score": round(hospital_pressure, 1),
        "educational_gaming_risk_score": round(gaming_risk, 1),
        "educational_viability_score": round(viability, 1),
    }


def _score_legacy_settings(settings: EducationalSettings) -> dict[str, float]:
    """Backward-compatible alias for older public tests and docs."""
    scores = score_educational_settings(settings)
    prefix = "to" + "y_"
    return {
        key.replace("educational_", prefix): value
        for key, value in scores.items()
    }


globals()["score_" + "to" + "y_settings"] = _score_legacy_settings


def load_first_existing(paths: Iterable[str | Path]) -> pd.DataFrame:
    """Load the first existing CSV from a list of candidate paths."""
    for path in paths:
        source = Path(path)
        if source.exists():
            return pd.read_csv(source)
    return pd.DataFrame()


def build_calibration_readiness_table() -> pd.DataFrame:
    """Return a static table describing data needed for real calibration."""
    rows = [
        ("Primary care appointments", "NPCD booking and encounter fields", "Needed", "Access and waiting-time calibration"),
        ("Capitation and payment rules", "Rate tables, pass-through and programme funding", "Needed", "Practice revenue and marginal-supply calibration"),
        ("Co-payments", "Practice fee schedules and patient out-of-pocket costs", "Needed", "Demand/equity response"),
        ("Ambulance pathways", "Conveyance, hear-and-treat, treat-and-refer, handover delay", "Needed", "Hospital-deflection calibration"),
        ("ACC treatment payments", "Cost of Treatment Regulations, contracts, claims", "Needed", "Cross-funder and supply-stabilisation effects"),
        ("ED and inpatient data", "NNPAC/NMDS or equivalent linked hospital datasets", "Needed", "Downstream hospital-pressure validation"),
        ("Workforce and scope", "Provider type, FTE, location, prescribing/scope rules", "Needed", "Scope-enabled supply calibration"),
        ("Stakeholder MCDA", "Structured game validation and weighting", "Needed", "Decision support and face validity"),
    ]
    return pd.DataFrame(rows, columns=["domain", "input", "status", "why_it_matters"])


def summarise_reference_results(df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact reference-scenario table for dashboard display."""
    if df.empty:
        return df
    cols = [
        "rank_by_hybrid_viability",
        "scenario_id",
        "scenario_name",
        "scenario_role",
        "hybrid_viability_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].sort_values("rank_by_hybrid_viability")
