"""Scenario loading and dashboard scoring utilities for GTPCNZ.

This module deliberately separates reference scenario outputs from educational
slider scoring. Reference scenarios are model-generated outputs stored in CSVs.
Toy scores are for explanation only and must not be described as calibrated
forecasts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

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
    "This is a source-informed parameterised scaffold and educational explainer. "
    "It is not a real-data calibrated forecast and should not be used to claim "
    "precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts."
)


@dataclass(frozen=True)
class ToySettings:
    """Educational dashboard levers.

    These are not the 70-parameter model. They exist to help readers understand
    the direction of the policy logic.

    The field names are internal implementation names. Public-facing labels and
    definitions are stored in TOY_LEVER_DEFINITIONS below.
    """

    scheduled_benefit_level: int
    capitation_support: int
    place_accountability: int
    audit_strength: int
    equity_protection: int
    scope_flexibility: int
    local_in_person_support: int


@dataclass(frozen=True)
class ToyLeverDefinition:
    """Public definition for one educational toy lever."""

    field_name: str
    public_label: str
    health_economics_meaning: str
    high_value_meaning: str
    toy_output_effect: str
    slider_help: str


TOY_LEVER_DEFINITIONS: tuple[ToyLeverDefinition, ...] = (
    ToyLeverDefinition(
        "scheduled_benefit_level",
        "Payment for extra primary care activity",
        "How strong the marginal payment signal is for each eligible primary medical activity.",
        "A higher value means practices take less financial loss when they do extra clinically necessary work.",
        "Raises toy supply, but can raise gaming risk if not paired with audit and place accountability.",
        "Strength of the marginal payment signal for each eligible primary medical activity.",
    ),
    ToyLeverDefinition(
        "capitation_support",
        "Stable population-based base funding",
        "How strong the enrolled-population/capitation support is.",
        "A higher value means more stable baseline funding for continuity and population responsibility.",
        "Supports viability, governance and equity, but does not alone create strong marginal supply.",
        "Strength of enrolled-population/capitation support for continuity and population responsibility.",
    ),
    ToyLeverDefinition(
        "place_accountability",
        "Whole-population local accountability",
        "How strongly providers or commissioning bodies remain responsible for the whole local population.",
        "A higher value leaves less room to cherry-pick easy activity and ignore hard-to-reach groups.",
        "Improves governance and equity and reduces gaming risk.",
        "Strength of responsibility for the whole local population, including hard-to-reach groups.",
    ),
    ToyLeverDefinition(
        "audit_strength",
        "Claim rules and audit strength",
        "How clear and enforceable the item rules, documentation requirements and unusual-pattern checks are.",
        "A higher value means activity-sensitive payment is more controlled.",
        "Improves governance and reduces gaming risk.",
        "Strength of item definitions, documentation rules and unusual-pattern checks.",
    ),
    ToyLeverDefinition(
        "equity_protection",
        "Equity and co-payment protection",
        "How strongly the design prevents patient charges and access barriers from shifting cost to high-need groups.",
        "A higher value means better protection for people who would otherwise ration care by price.",
        "Improves toy equity and helps reduce hospital-pressure logic.",
        "Strength of protections against patient charges and access barriers for high-need groups.",
    ),
    ToyLeverDefinition(
        "scope_flexibility",
        "Flexible workforce scope",
        "How much appropriate care can be delivered by the right mix of GPs, nurses, nurse practitioners, pharmacists and other providers.",
        "A higher value means the toy logic is less bottlenecked by one workforce group.",
        "Raises toy supply, but needs audit and governance to avoid low-value activity.",
        "Ability for the right mix of providers to deliver eligible primary care activity.",
    ),
    ToyLeverDefinition(
        "local_in_person_support",
        "Local in-person care capacity",
        "How much local face-to-face capacity remains available for care that cannot be safely substituted by digital access.",
        "A higher value means rural, complex and hands-on care needs are less likely to be displaced.",
        "Improves toy supply, equity and hospital-pressure logic.",
        "Capacity for local face-to-face care that cannot be replaced by digital access.",
    ),
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
    issues: list[str] = []
    missing = REQUIRED_SCENARIO_COLUMNS.difference(df.columns)
    if missing:
        issues.append(f"missing columns: {sorted(missing)}")
    if "scenario_id" in df.columns:
        missing_scenarios = EXPECTED_SCENARIO_IDS.difference(set(df["scenario_id"].astype(str)))
        if missing_scenarios:
            issues.append(f"missing expected scenarios: {sorted(missing_scenarios)}")
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


def score_toy_settings(settings: ToySettings) -> dict[str, float]:
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

    supply = 100 * (0.33 * benefit + 0.18 * capitation + 0.22 * scope + 0.17 * local + 0.10 * place)
    governance = 100 * (0.42 * audit + 0.30 * place + 0.18 * equity + 0.10 * capitation)
    equity_score = 100 * (0.45 * equity + 0.25 * place + 0.15 * local + 0.15 * capitation)
    gaming_risk = 100 * max(0.0, 0.55 * benefit + 0.25 * scope - 0.45 * audit - 0.25 * place - 0.20 * equity)
    hospital_pressure = max(0.0, 100 - (0.48 * supply + 0.22 * governance + 0.18 * local * 100 + 0.12 * equity_score))
    viability = 0.34 * supply + 0.22 * governance + 0.18 * equity_score + 0.16 * (100 - hospital_pressure) + 0.10 * (100 - gaming_risk)

    return {
        "toy_supply_score": round(supply, 1),
        "toy_governance_score": round(governance, 1),
        "toy_equity_score": round(equity_score, 1),
        "toy_hospital_pressure_score": round(hospital_pressure, 1),
        "toy_gaming_risk_score": round(gaming_risk, 1),
        "toy_viability_score": round(viability, 1),
    }


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
