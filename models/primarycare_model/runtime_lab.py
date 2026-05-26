"""Public-safe runtime calculations for the advanced Streamlit model lab.

The functions in this module are deliberately bounded and deterministic unless a
seeded stochastic run is requested. They are explanatory model-index
calculations, not calibrated forecasts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Iterable

import numpy as np
import pandas as pd


CLAIM_LABEL = "live calculation; demonstrative model-generated index; not linked-data calibrated and not a patient-level forecast"
STOCHASTIC_LABEL = "cached stochastic demo; demonstrative uncertainty only; not an empirical probability"

MAX_MONTE_CARLO_DRAWS = 500
DEFAULT_MONTE_CARLO_DRAWS = 100
MAX_ABM_POPULATION = 500
DEFAULT_ABM_POPULATION = 180
MAX_MONTHS = 60


def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return float(max(lower, min(upper, value)))


@dataclass(frozen=True)
class RuntimeScenario:
    scenario_id: str
    scenario_name: str
    description: str
    activity_signal: float
    capitation: float
    place_accountability: float
    scope_capacity: float
    urgent_ambulance: float
    data_visibility: float
    governance: float
    equity_protection: float
    copayment_burden: float
    budget_tightness: float
    hospital_salience: float
    complexity: float


SCENARIOS: tuple[RuntimeScenario, ...] = (
    RuntimeScenario("F0", "Current reform pathway", "Current reform without uncapped primary medical FFS.", 18, 70, 42, 36, 58, 48, 55, 46, 58, 76, 88, 45),
    RuntimeScenario("F1", "Capitation reweighting only", "Formula improves allocation but marginal activity remains weakly funded.", 20, 78, 42, 36, 55, 50, 53, 48, 55, 76, 86, 44),
    RuntimeScenario("F2", "Uncapped scheduled medical FFS", "Demand-led eligible activity, weaker place accountability.", 78, 70, 38, 48, 58, 60, 63, 55, 45, 60, 76, 62),
    RuntimeScenario("F3", "Uncapped medical FFS + place accountability", "Demand-led eligible activity plus explicit population responsibility.", 76, 78, 78, 52, 60, 70, 70, 70, 40, 58, 72, 64),
    RuntimeScenario("F4", "Full hybrid upstream architecture", "Capitation plus scheduled FFS, place accountability, urgent alternatives, scope, data and audit.", 78, 82, 82, 68, 74, 82, 82, 78, 35, 55, 65, 72),
    RuntimeScenario("F5", "Uncapped weak-control model", "Demand-led activity with weak controls, place accountability and equity protections.", 82, 60, 20, 70, 62, 45, 22, 30, 65, 80, 70, 76),
    RuntimeScenario("F6", "ACC activity constraint shock", "ACC activity payments constrained without compensating upstream supply.", 12, 70, 42, 32, 50, 48, 52, 44, 58, 86, 90, 48),
    RuntimeScenario("F7", "Ambulance and urgent alternatives only", "Urgent and ambulance alternatives strengthened while primary marginal payment remains weak.", 18, 70, 44, 38, 74, 68, 55, 46, 55, 70, 76, 52),
    RuntimeScenario("F8", "Scope-enabled supply only", "Broader providers can generate activity, but payment and place accountability remain incomplete.", 35, 70, 42, 68, 56, 55, 58, 46, 54, 68, 78, 58),
    RuntimeScenario("F9", "Place-based commissioning only", "Population accountability improves without materially uncapping marginal activity funding.", 18, 72, 78, 38, 55, 58, 55, 74, 50, 72, 78, 54),
)

SCENARIO_BY_ID = {scenario.scenario_id: scenario for scenario in SCENARIOS}


def _as_fraction(value: float) -> float:
    return clamp(value) / 100.0


def _scenario_with_perturbation(scenario: RuntimeScenario, rng: np.random.Generator, sd: float) -> RuntimeScenario:
    updates: dict[str, float] = {}
    for key, value in asdict(scenario).items():
        if isinstance(value, (int, float)):
            updates[key] = clamp(float(rng.normal(value, sd * 100.0)))
    return replace(scenario, **updates)


def calculate_indices(scenario: RuntimeScenario) -> dict[str, float]:
    """Calculate transparent public model indices from one runtime scenario."""

    activity = _as_fraction(scenario.activity_signal)
    capitation = _as_fraction(scenario.capitation)
    place = _as_fraction(scenario.place_accountability)
    scope = _as_fraction(scenario.scope_capacity)
    urgent = _as_fraction(scenario.urgent_ambulance)
    data = _as_fraction(scenario.data_visibility)
    governance = _as_fraction(scenario.governance)
    equity = _as_fraction(scenario.equity_protection)
    copay = _as_fraction(scenario.copayment_burden)
    budget = _as_fraction(scenario.budget_tightness)
    hospital_salience = _as_fraction(scenario.hospital_salience)
    complexity = _as_fraction(scenario.complexity)

    supply = clamp(100 * (0.34 * activity + 0.18 * capitation + 0.24 * scope + 0.12 * urgent + 0.12 * place - 0.12 * budget))
    access = clamp(100 * (0.42 * supply / 100 + 0.18 * urgent + 0.15 * equity + 0.12 * place + 0.10 * data - 0.16 * copay))
    equity_legitimacy = clamp(100 * (0.34 * equity + 0.24 * place + 0.16 * capitation + 0.14 * data - 0.16 * copay))
    governance_resilience = clamp(100 * (0.44 * governance + 0.20 * data + 0.18 * place + 0.10 * equity + 0.08 * capitation))
    hospital_deflection = clamp(100 * (0.32 * access / 100 + 0.22 * urgent + 0.16 * supply / 100 + 0.16 * data + 0.14 * place - 0.10 * complexity))
    gaming_risk = clamp(100 * (0.35 * activity + 0.18 * scope + 0.18 * complexity - 0.30 * governance - 0.18 * data - 0.16 * place))
    fiscal_risk = clamp(100 * (0.22 * activity + 0.18 * gaming_risk / 100 + 0.16 * complexity + 0.14 * (1 - budget) - 0.18 * governance - 0.14 * hospital_deflection / 100))
    hospital_pressure = clamp(100 * (0.34 * hospital_salience + 0.26 * (1 - hospital_deflection / 100) + 0.16 * complexity + 0.14 * budget - 0.18 * access / 100 - 0.12 * urgent))
    hybrid = clamp(
        0.24 * supply
        + 0.18 * access
        + 0.18 * equity_legitimacy
        + 0.16 * governance_resilience
        + 0.14 * hospital_deflection
        + 0.06 * (100 - fiscal_risk)
        + 0.04 * (100 - gaming_risk)
    )
    return {
        "hybrid_viability_score": round(hybrid, 2),
        "access_score": round(access, 2),
        "supply_generation_score": round(supply, 2),
        "equity_legitimacy_score": round(equity_legitimacy, 2),
        "governance_resilience_score": round(governance_resilience, 2),
        "hospital_deflection_score": round(hospital_deflection, 2),
        "fiscal_risk_score": round(fiscal_risk, 2),
        "gaming_risk_score": round(gaming_risk, 2),
        "hospital_pressure_score": round(hospital_pressure, 2),
    }


def run_reference_calculation(months: int = MAX_MONTHS, scenarios: Iterable[RuntimeScenario] = SCENARIOS) -> pd.DataFrame:
    months = int(min(max(12, months), MAX_MONTHS))
    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        idx = calculate_indices(scenario)
        last12_primary = 8.0 + 0.56 * idx["access_score"] + 0.10 * idx["supply_generation_score"]
        unmet = max(0.0, 110 - 1.30 * idx["access_score"] - 0.45 * idx["hospital_deflection_score"] + 0.18 * scenario.budget_tightness)
        ed_events = 48 + 0.36 * unmet + 0.18 * idx["hospital_pressure_score"]
        admissions = 9 + 0.18 * ed_events + 0.05 * scenario.complexity
        ambulance = 16 + 0.22 * unmet + 0.16 * scenario.hospital_salience - 0.18 * scenario.urgent_ambulance
        row = {
            "scenario_id": scenario.scenario_id,
            "scenario_name": scenario.scenario_name,
            "description": scenario.description,
            **idx,
            "mean_last12_primary_contacts_per_1000": round(last12_primary, 2),
            "mean_last12_unmet_need_index": round(unmet, 2),
            "mean_last12_ed_events_per_100k": round(ed_events, 2),
            "mean_last12_admissions_per_100k": round(admissions, 2),
            "mean_last12_ambulance_conveyances_per_100k": round(max(0.0, ambulance), 2),
            "mean_last12_hospital_pressure_index": round(idx["hospital_pressure_score"] / 100.0, 3),
            "mean_last12_public_cost_index": round(1.2 + 0.012 * idx["fiscal_risk_score"] + 0.009 * idx["hospital_pressure_score"] + months / 240.0, 2),
            "calculation_status": CLAIM_LABEL,
        }
        rows.append(row)
    out = pd.DataFrame(rows)
    out["rank_by_hybrid_viability"] = out["hybrid_viability_score"].rank(ascending=False, method="min").astype(int)
    return out.sort_values("rank_by_hybrid_viability").reset_index(drop=True)


def calculation_trace(scenario_id: str) -> pd.DataFrame:
    scenario = SCENARIO_BY_ID[scenario_id]
    idx = calculate_indices(scenario)
    rows = [
        ("Supply generation", "activity + capitation + scope + urgent alternatives + place - budget tightness", idx["supply_generation_score"]),
        ("Access", "supply + urgent alternatives + equity + place + data - co-payment burden", idx["access_score"]),
        ("Hospital deflection", "access + urgent alternatives + supply + data + place - complexity", idx["hospital_deflection_score"]),
        ("Gaming risk", "activity + scope + complexity - governance - data - place", idx["gaming_risk_score"]),
        ("Fiscal risk", "activity + gaming + complexity + uncapped exposure - governance - deflection", idx["fiscal_risk_score"]),
        ("Hybrid viability", "weighted supply, access, equity, governance, deflection and inverted risks", idx["hybrid_viability_score"]),
    ]
    return pd.DataFrame(rows, columns=["calculation", "formula_sketch", "index_value"])


def run_stochastic_uncertainty(
    scenario_id: str,
    draws: int = DEFAULT_MONTE_CARLO_DRAWS,
    seed: int = 20260526,
    sd: float = 0.08,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    draws = int(min(max(10, draws), MAX_MONTE_CARLO_DRAWS))
    sd = float(min(max(sd, 0.01), 0.20))
    rng = np.random.default_rng(seed)
    scenario = SCENARIO_BY_ID[scenario_id]
    rows: list[dict[str, object]] = []
    for draw in range(draws):
        perturbed = _scenario_with_perturbation(scenario, rng, sd)
        row = {
            "draw": draw + 1,
            "scenario_id": scenario_id,
            "scenario_name": scenario.scenario_name,
            **calculate_indices(perturbed),
            "calculation_status": STOCHASTIC_LABEL,
        }
        rows.append(row)
    draw_frame = pd.DataFrame(rows)
    summary_rows: list[dict[str, object]] = []
    for metric in [
        "hybrid_viability_score",
        "access_score",
        "hospital_pressure_score",
        "gaming_risk_score",
        "fiscal_risk_score",
    ]:
        values = draw_frame[metric].astype(float)
        summary_rows.append(
            {
                "metric": metric,
                "mean": round(values.mean(), 2),
                "p05": round(values.quantile(0.05), 2),
                "p50": round(values.quantile(0.50), 2),
                "p95": round(values.quantile(0.95), 2),
            }
        )
    return draw_frame, pd.DataFrame(summary_rows)


def run_stock_flow_trace(scenario_id: str, months: int = 36) -> pd.DataFrame:
    months = int(min(max(6, months), MAX_MONTHS))
    scenario = SCENARIO_BY_ID[scenario_id]
    idx = calculate_indices(scenario)
    capacity = 35 + 0.45 * idx["supply_generation_score"]
    unmet = 70 + 0.35 * scenario.budget_tightness - 0.55 * idx["access_score"]
    rows: list[dict[str, float | int | str]] = []
    for month in range(1, months + 1):
        seasonal = 1.0 + 0.05 * np.sin(2 * np.pi * month / 12.0)
        need = 55 * seasonal + 0.18 * unmet + 0.15 * scenario.complexity
        capacity = max(1.0, capacity + 0.06 * idx["supply_generation_score"] + 0.04 * scenario.place_accountability - 0.05 * scenario.budget_tightness)
        served = min(need + 0.20 * unmet, capacity * (0.72 + idx["access_score"] / 250.0))
        ambulance_resolved = min(need * (0.08 + scenario.urgent_ambulance / 400.0), 12 + capacity / 10.0)
        unmet = max(0.0, 0.70 * unmet + need - served - ambulance_resolved)
        hospital_pressure = clamp(35 + 0.42 * unmet + 0.28 * scenario.hospital_salience - 0.32 * idx["hospital_deflection_score"])
        fiscal_pressure = clamp(20 + 0.28 * idx["fiscal_risk_score"] + 0.12 * unmet + 0.08 * served)
        rows.append(
            {
                "month": month,
                "scenario_id": scenario_id,
                "need_generated": round(need, 2),
                "primary_contacts": round(served, 2),
                "ambulance_resolved": round(ambulance_resolved, 2),
                "unmet_need": round(unmet, 2),
                "primary_capacity": round(capacity, 2),
                "hospital_pressure": round(hospital_pressure, 2),
                "fiscal_pressure": round(fiscal_pressure, 2),
                "calculation_status": CLAIM_LABEL,
            }
        )
    return pd.DataFrame(rows)


def run_agent_lens(
    scenario_id: str,
    population_size: int = DEFAULT_ABM_POPULATION,
    months: int = 12,
    seed: int = 20260526,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    population_size = int(min(max(50, population_size), MAX_ABM_POPULATION))
    months = int(min(max(3, months), 24))
    scenario = SCENARIO_BY_ID[scenario_id]
    idx = calculate_indices(scenario)
    rng = np.random.default_rng(seed)
    high_need = rng.beta(2.2, 3.4, population_size)
    rural = rng.random(population_size) < (0.08 + scenario.complexity / 260.0)
    barrier = np.clip(0.45 * high_need + 0.30 * rural.astype(float) + scenario.copayment_burden / 180.0 - scenario.equity_protection / 240.0, 0, 1)
    access_probability = np.clip(idx["access_score"] / 100.0 - 0.35 * barrier + scenario.place_accountability / 350.0, 0.05, 0.95)
    contact_attempts = rng.random((months, population_size)) < np.clip(0.22 + 0.30 * high_need, 0.05, 0.85)
    successful = rng.random((months, population_size)) < access_probability
    served = contact_attempts & successful
    agent_frame = pd.DataFrame(
        {
            "patient_id": np.arange(1, population_size + 1),
            "high_need_score": high_need.round(3),
            "rural": rural,
            "access_barrier": barrier.round(3),
            "access_probability": access_probability.round(3),
            "served_contacts": served.sum(axis=0),
            "unmet_attempts": (contact_attempts & ~successful).sum(axis=0),
        }
    )
    summary = pd.DataFrame(
        [
            ("population_size", population_size),
            ("months", months),
            ("mean_access_probability", round(float(agent_frame["access_probability"].mean()), 3)),
            ("served_contacts", int(agent_frame["served_contacts"].sum())),
            ("unmet_attempts", int(agent_frame["unmet_attempts"].sum())),
            ("high_barrier_share", round(float((agent_frame["access_barrier"] >= 0.6).mean()), 3)),
        ],
        columns=["metric", "value"],
    )
    return agent_frame, summary


def model_gap_map() -> pd.DataFrame:
    rows = [
        ("Current", "14-game demonstrative layer", "Executable in parent repo; partially represented in public toy labs", "Good benchmark, incomplete public runtime coverage"),
        ("Current", "Static diagrams and Mermaid previews", "Many PNG/SVG/Mermaid assets exist across docs and Substack-ready figures", "Strong explainer inventory, not all connected to Streamlit modules"),
        ("Current", "Public Streamlit runtime", "Toy labs calculate at runtime; reference scenarios load precomputed CSV", "Needs explicit live/cached/precomputed source labels"),
        ("Comprehensive", "All-game executable navigator", "Not yet complete in public app", "Add a 19-games navigator with linked formulas, posts and visuals"),
        ("Comprehensive", "Unified formula registry", "Formula sketches exist across docs and code", "Expose formula cards and calculation trace per scenario"),
        ("SOTA", "Global sensitivity and uncertainty provenance", "Monte Carlo exists in parent repo", "Add bounded public uncertainty intervals and top-driver visuals"),
        ("SOTA", "Calibration diagnostics", "Readiness table exists; linked-data calibration not available", "Keep as readiness/provenance, not observed-vs-predicted claims"),
        ("Bleeding edge", "Scenario morphing and stochastic replay", "Not yet implemented", "Animate transition between current reform and full hybrid, with seeded stochastic replay"),
        ("Bleeding edge", "Agent-flow visual", "ABM exists in parent repo", "Show capped agent allocation and unmet-attempt patterns as a teaching lens"),
        ("Bleeding edge", "Calculation audit overlay", "Not yet implemented", "Show input, formula sketch, output, status and caveat for each number"),
    ]
    return pd.DataFrame(rows, columns=["tier", "asset_or_gap", "current_state", "recommended_next_step"])
