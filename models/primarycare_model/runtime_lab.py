"""Public-safe runtime calculations for the advanced Streamlit model lab.

The functions in this module are deliberately bounded and deterministic unless a
seeded stochastic run is requested. They are explanatory model-index
calculations, not calibrated forecasts.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass, replace
from functools import lru_cache

import numpy as np
import pandas as pd

from models.primarycare_model.empirical_calibration import (
    build_claim_boundary_text,
    run_empirical_calibration_pipeline,
)
from models.primarycare_model.validation.registry_loader import load_runtime_scenarios_registry


@lru_cache(maxsize=1)
def _empirical_summary():
    try:
        return run_empirical_calibration_pipeline()
    except Exception:
        return None


def _claim_label() -> str:
    summary = _empirical_summary()
    if summary is None:
        return "live calculation; public-data anchored model-generated index; not linked-data calibrated and not a patient-level forecast"
    return build_claim_boundary_text(summary)


CLAIM_LABEL = _claim_label()
STOCHASTIC_LABEL = "cached stochastic demo; demonstrative uncertainty only; not an empirical probability"

MAX_MONTE_CARLO_DRAWS = 500
DEFAULT_MONTE_CARLO_DRAWS = 100
MAX_ABM_POPULATION = 500
DEFAULT_ABM_POPULATION = 180
MAX_MONTHS = 60


def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return float(max(lower, min(upper, value)))


def diminishing_return(value: float, rate: float = 2.4) -> float:
    bounded = clamp(value, 0.0, 1.0)
    return (1.0 - np.exp(-rate * bounded)) / (1.0 - np.exp(-rate))


def strategic_response(value: float, threshold: float = 0.5, steepness: float = 6.0) -> float:
    return 1.0 / (1.0 + np.exp(-steepness * (value - threshold)))


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


def _load_runtime_scenarios() -> tuple[RuntimeScenario, ...]:
    """Load runtime scenario defaults from the strict scenario registry."""
    return tuple(
        RuntimeScenario(
            scenario.scenario_id,
            scenario.scenario_name,
            scenario.description,
            scenario.activity_signal,
            scenario.capitation,
            scenario.place_accountability,
            scenario.scope_capacity,
            scenario.urgent_ambulance,
            scenario.data_visibility,
            scenario.governance,
            scenario.equity_protection,
            scenario.copayment_burden,
            scenario.budget_tightness,
            scenario.hospital_salience,
            scenario.complexity,
        )
        for scenario in load_runtime_scenarios_registry()
    )


SCENARIOS: tuple[RuntimeScenario, ...] = _load_runtime_scenarios()

SCENARIO_BY_ID = {scenario.scenario_id: scenario for scenario in SCENARIOS}


def get_runtime_scenario(scenario_id: str) -> RuntimeScenario:
    """Return a runtime scenario or raise a public-safe validation error."""
    try:
        return SCENARIO_BY_ID[scenario_id]
    except KeyError as exc:
        valid = ", ".join(sorted(SCENARIO_BY_ID))
        raise ValueError(f"Unknown scenario_id {scenario_id!r}; valid IDs are: {valid}") from exc


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
    scenario = get_runtime_scenario(scenario_id)
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
    scenario = get_runtime_scenario(scenario_id)
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
    scenario = get_runtime_scenario(scenario_id)
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
    scenario = get_runtime_scenario(scenario_id)
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


# ── Phase 5: Validation and calculation-detail helpers ──────────────────


def validate_slider_value(
    value: int | float,
    field_name: str,
    lower_bound: float | None = None,
    upper_bound: float | None = None,
) -> tuple[str, str]:
    """Return (badge_emoji, tooltip_text) for a slider value.

    Parameters
    ----------
    value : int | float
        The current slider value.
    field_name : str
        Human-readable field name for error messages.
    lower_bound : float | None
        Expected lower bound (inclusive).
    upper_bound : float | None
        Expected upper bound (inclusive).

    Returns
    -------
    tuple[str, str]
        A badge emoji ("✅", "⚠️", "❌") and a tooltip/description string.
    """
    if lower_bound is not None and value < lower_bound:
        return ("⚠️", f"{field_name}: value {value} is below lower bound {lower_bound}")
    if upper_bound is not None and value > upper_bound:
        return ("⚠️", f"{field_name}: value {value} is above upper bound {upper_bound}")
    return ("✅", f"{field_name}: {value} within [{lower_bound or 0}, {upper_bound or 100}]")


def get_calculation_details(
    scenario_id: str | None = None,
    scenario_name: str | None = None,
) -> list[dict[str, str]]:
    """Return deterministic formula summaries for display in the UI.

    Parameters
    ----------
    scenario_id : str | None
        Optional scenario identifier to include.
    scenario_name : str | None
        Optional scenario name to include.

    Returns
    -------
    list[dict[str, str]]
        A list of dicts with keys ``label``, ``formula`` and ``mode``.
    """
    details: list[dict[str, str]] = [
        {
            "label": "Supply generation",
            "formula": "0.34×activity + 0.18×capitation + 0.24×scope + 0.12×urgent + 0.12×place − 0.12×budget_tightness",
            "mode": "deterministic",
        },
        {
            "label": "Access",
            "formula": "0.42×supply + 0.18×urgent + 0.15×equity + 0.12×place + 0.10×data − 0.16×copay",
            "mode": "deterministic",
        },
        {
            "label": "Hospital deflection",
            "formula": "0.32×access + 0.22×urgent + 0.16×supply + 0.16×data + 0.14×place − 0.10×complexity",
            "mode": "deterministic",
        },
        {
            "label": "Gaming risk",
            "formula": "0.35×activity + 0.18×scope + 0.18×complexity − 0.30×governance − 0.18×data − 0.16×place",
            "mode": "deterministic",
        },
        {
            "label": "Fiscal risk",
            "formula": "0.22×activity + 0.18×gaming_risk + 0.16×complexity + 0.14×(1−budget) − 0.18×governance − 0.14×deflection",
            "mode": "deterministic",
        },
        {
            "label": "Hybrid viability",
            "formula": "0.24×supply + 0.18×access + 0.18×equity + 0.16×governance + 0.14×deflection + 0.06×(100−fiscal_risk) + 0.04×(100−gaming_risk)",
            "mode": "deterministic",
        },
    ]
    return details


def format_formula_markdown(details: list[dict[str, str]]) -> str:
    """Format calculation details as a Markdown block."""
    lines = ["| Index | Formula sketch | Mode |", "|------|----------------|------|"]
    for d in details:
        mode_badge = "📐 Deterministic" if d["mode"] == "deterministic" else "🎲 Stochastic"
        lines.append(f"| **{d['label']}** | {d['formula']} | {mode_badge} |")
    return "\n".join(lines)


def run_stochastic_replay(
    scenario_id: str,
    draws: int = 100,
    fixed_seed: int = 260526,
    random_seed: int | None = None,
    sd: float = 0.08,
) -> dict[str, pd.DataFrame]:
    """Run fixed-seed and random-seed stochastic replays side by side.

    Parameters
    ----------
    scenario_id : str
        The scenario identifier.
    draws : int
        Number of Monte Carlo draws.
    fixed_seed : int
        Fixed seed for reproducible replay.
    random_seed : int | None
        Optional different seed for comparison. If ``None``, a random seed
        is generated from the OS entropy pool.
    sd : float
        Perturbation width (0.01-0.20).

    Returns
    -------
    dict[str, pd.DataFrame]
        ``{"fixed": draw_frame, "random": draw_frame, "summary": combined_summary}``
    """
    if random_seed is None:
        rng_os = np.random.default_rng()
        random_seed = int(rng_os.integers(1, 999999))

    fixed_frame, fixed_summary = run_stochastic_uncertainty(
        scenario_id=scenario_id, draws=draws, seed=fixed_seed, sd=sd
    )
    random_frame, random_summary = run_stochastic_uncertainty(
        scenario_id=scenario_id, draws=draws, seed=random_seed, sd=sd
    )

    # Combine summaries for comparison
    combined = fixed_summary.copy()
    combined = combined.rename(
        columns={
            "mean": "fixed_mean",
            "p05": "fixed_p05",
            "p50": "fixed_p50",
            "p95": "fixed_p95",
        }
    )
    random_renamed = random_summary.rename(
        columns={
            "mean": "random_mean",
            "p05": "random_p05",
            "p50": "random_p50",
            "p95": "random_p95",
        }
    )
    combined = combined.merge(random_renamed, on="metric", suffixes=("_fixed", "_random"))

    return {
        "fixed": fixed_frame,
        "random": random_frame,
        "summary": combined,
    }


# ── End Phase 5 helpers ─────────────────────────────────────────────────


# ── Wave 1: Bleeding-edge enhancement functions ────────────────────────


def run_tornado_sensitivity(
    scenario_id: str,
    delta_step: float = 10.0,
) -> pd.DataFrame:
    """Run OAT sensitivity analysis and return tornado-ready data.

    Perturbs each lever by +/-delta_step while holding others at baseline,
    returning the delta for each output metric. Used by the tornado chart
    renderer.

    Returns
    -------
    pd.DataFrame
        Columns: lever, low_delta_viability, high_delta_viability,
        low_delta_hospital, high_delta_hospital, total_abs_impact.
        Rows sorted by total absolute impact (most influential first).
    """
    from models.primarycare_model.engines.sensitivity_adapter import (
        SENSITIVITY_LEVERS,
        SensitivityAnalysisAdapter,
        SensitivityInput,
    )

    scenario = get_runtime_scenario(scenario_id)
    step = float(min(max(delta_step, 1.0), 50.0))

    inp = SensitivityInput(
        scenario_id=scenario_id,
        seed=None,
        claim_boundary=CLAIM_LABEL,
        baseline_activity_signal=scenario.activity_signal,
        baseline_capitation=scenario.capitation,
        baseline_place_accountability=scenario.place_accountability,
        baseline_scope_capacity=scenario.scope_capacity,
        baseline_urgent_ambulance=scenario.urgent_ambulance,
        baseline_data_visibility=scenario.data_visibility,
        baseline_governance=scenario.governance,
        baseline_equity_protection=scenario.equity_protection,
        baseline_copayment_burden=scenario.copayment_burden,
        baseline_budget_tightness=scenario.budget_tightness,
        baseline_hospital_salience=scenario.hospital_salience,
        baseline_complexity=scenario.complexity,
        delta_step=step,
    )
    adapter = SensitivityAnalysisAdapter()
    output = adapter.run(inp)

    # Aggregate OAT rows into lever-level low/high deltas.
    # Each row has "lever", "perturbation" (e.g. "low (-10)") and
    # "delta_*" keys.  We separate low/high by tagging the perturbation label.
    lever_low: dict[str, dict[str, float]] = {}
    lever_high: dict[str, dict[str, float]] = {}
    for row in output.oat_sensitivities:
        lever = str(row["lever"])
        tag = str(row["perturbation"])
        target = lever_low if tag.startswith("low") else lever_high
        if lever not in target:
            target[lever] = {}
        for key, val in row.items():
            if key.startswith("delta_"):
                target[lever][key] = float(val)

    rows: list[dict[str, object]] = []
    for lever in SENSITIVITY_LEVERS:
        low_v = lever_low.get(lever, {}).get("delta_hybrid_viability_score", 0.0)
        high_v = lever_high.get(lever, {}).get("delta_hybrid_viability_score", 0.0)
        low_h = lever_low.get(lever, {}).get("delta_hospital_pressure_score", 0.0)
        high_h = lever_high.get(lever, {}).get("delta_hospital_pressure_score", 0.0)
        total_abs = abs(low_v) + abs(high_v) + abs(low_h) + abs(high_h)
        rows.append({
            "lever": lever,
            "low_delta_viability": round(low_v, 2),
            "high_delta_viability": round(high_v, 2),
            "low_delta_hospital": round(low_h, 2),
            "high_delta_hospital": round(high_h, 2),
            "total_abs_impact": round(total_abs, 2),
        })

    out = pd.DataFrame(rows)
    out = out.sort_values("total_abs_impact", ascending=False).reset_index(drop=True)
    return out


def build_waterfall_data(scenario_id: str) -> pd.DataFrame:
    """Build waterfall chart data showing how components build hybrid viability.

    Returns a DataFrame with columns: component, contribution, is_total.
    Positive contributions increase viability; negative ones decrease it.
    """
    scenario = get_runtime_scenario(scenario_id)
    idx = calculate_indices(scenario)

    supply = idx["supply_generation_score"]
    access = idx["access_score"]
    equity = idx["equity_legitimacy_score"]
    governance = idx["governance_resilience_score"]
    deflection = idx["hospital_deflection_score"]
    fiscal_risk = idx["fiscal_risk_score"]
    gaming_risk = idx["gaming_risk_score"]
    hybrid = idx["hybrid_viability_score"]

    rows = [
        ("Supply generation", round(0.24 * supply, 2), False),
        ("Access", round(0.18 * access, 2), False),
        ("Equity legitimacy", round(0.18 * equity, 2), False),
        ("Governance resilience", round(0.16 * governance, 2), False),
        ("Hospital deflection", round(0.14 * deflection, 2), False),
        ("Fiscal risk (inverted)", round(0.06 * (100 - fiscal_risk), 2), False),
        ("Gaming risk (inverted)", round(0.04 * (100 - gaming_risk), 2), False),
        ("Hybrid viability", round(hybrid, 2), True),
    ]
    return pd.DataFrame(rows, columns=["component", "contribution", "is_total"])


def run_ensemble_mc(
    draws: int = 50,
    seed: int = 260526,
    sd: float = 0.08,
) -> pd.DataFrame:
    """Run seeded Monte Carlo across all runtime scenarios.

    Returns an ensemble-level summary with per-scenario uncertainty
    statistics for hybrid viability.
    """
    draws = int(min(max(10, draws), MAX_MONTE_CARLO_DRAWS))
    sd = float(min(max(sd, 0.01), 0.20))
    rng = np.random.default_rng(seed)

    rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        scenario_rng = np.random.default_rng(rng.integers(1, 999999))
        for draw in range(draws):
            perturbed = _scenario_with_perturbation(scenario, scenario_rng, sd)
            idx = calculate_indices(perturbed)
            rows.append({
                "scenario_id": scenario.scenario_id,
                "scenario_name": scenario.scenario_name,
                "draw": draw + 1,
                "hybrid_viability_score": idx["hybrid_viability_score"],
                "access_score": idx["access_score"],
                "hospital_pressure_score": idx["hospital_pressure_score"],
                "gaming_risk_score": idx["gaming_risk_score"],
            })

    draw_frame = pd.DataFrame(rows)

    summary_rows: list[dict[str, object]] = []
    for scenario_id in sorted(draw_frame["scenario_id"].unique()):
        subset = draw_frame[draw_frame["scenario_id"] == scenario_id]
        vals = subset["hybrid_viability_score"].astype(float)
        summary_rows.append({
            "scenario_id": scenario_id,
            "mean": round(float(vals.mean()), 2),
            "p05": round(float(vals.quantile(0.05)), 2),
            "p50": round(float(vals.quantile(0.50)), 2),
            "p95": round(float(vals.quantile(0.95)), 2),
            "spread": round(float(vals.quantile(0.95) - vals.quantile(0.05)), 2),
        })

    return pd.DataFrame(summary_rows)


def run_cohort_stratified(
    scenario_id: str,
    subgroup_field: str = "equity_protection",
    low_value: float = 25.0,
    high_value: float = 75.0,
    label_low: str = "Low equity",
    label_high: str = "High equity",
) -> pd.DataFrame:
    """Run deterministic calculation with a subgroup parameter override.

    Compares a low-value and high-value setting for one scenario field.
    """
    scenario = get_runtime_scenario(scenario_id)
    low_kwargs = {subgroup_field: low_value}
    low_scenario = replace(scenario, **low_kwargs)
    low_idx = calculate_indices(low_scenario)

    high_kwargs = {subgroup_field: high_value}
    high_scenario = replace(scenario, **high_kwargs)
    high_idx = calculate_indices(high_scenario)

    metrics = [
        "hybrid_viability_score", "access_score", "supply_generation_score",
        "equity_legitimacy_score", "governance_resilience_score",
        "hospital_deflection_score", "fiscal_risk_score", "gaming_risk_score",
        "hospital_pressure_score",
    ]
    rows: list[dict[str, object]] = []
    for metric in metrics:
        rows.append({
            "metric": metric,
            label_low: round(low_idx[metric], 2),
            label_high: round(high_idx[metric], 2),
            "delta": round(high_idx[metric] - low_idx[metric], 2),
        })

    return pd.DataFrame(rows)


# ── Wave 2: Should enhancements ───────────────────────────────────────


def run_variance_decomposition(
    scenario_id: str,
    draws: int = 200,
    seed: int = 260526,
    sd: float = 0.08,
) -> pd.DataFrame:
    """Separate parameter, subgroup, and stochastic variance contributions.

    Partitions total hybrid-viability variance into structural (parameter
    variation), subgroup (equity spread), and stochastic (residual) components.

    Returns
    -------
    pd.DataFrame
        Columns: source, variance, proportion.
    """
    draws = int(min(max(50, draws), MAX_MONTE_CARLO_DRAWS))
    sd = float(min(max(sd, 0.01), 0.20))
    rng = np.random.default_rng(seed)
    scenario = get_runtime_scenario(scenario_id)

    total_values: list[float] = []
    for _ in range(draws):
        perturbed = _scenario_with_perturbation(scenario, rng, sd)
        total_values.append(calculate_indices(perturbed)["hybrid_viability_score"])
    total_var = float(np.var(total_values))

    structural_values: list[float] = []
    for _ in range(draws):
        p = _scenario_with_perturbation(scenario, rng, sd)
        structural_values.append(calculate_indices(p)["hybrid_viability_score"])
    structural_var = float(np.var(structural_values))
    stochastic_var = max(0.0, total_var - structural_var)

    cs = run_cohort_stratified(scenario_id, "equity_protection", 25, 75, "Low", "High")
    vd = cs[cs["metric"] == "hybrid_viability_score"]["delta"].values
    subgroup_var = float(np.var([0.0, float(vd[0]) if len(vd) > 0 else 0.0]))
    total = total_var or 1.0
    return pd.DataFrame([
        ("Structural (parameter)", round(structural_var, 4), round(structural_var / total, 4)),
        ("Subgroup (equity)", round(subgroup_var, 4), round(subgroup_var / total, 4)),
        ("Stochastic (residual)", round(stochastic_var, 4), round(stochastic_var / total, 4)),
    ], columns=["source", "variance", "proportion"])


def run_policy_shock_sequence(
    scenario_id: str,
    shock_month: int = 13,
    pre_shock_months: int = 12,
    post_shock_months: int = 24,
    shock_field: str = "activity_signal",
    shock_delta: float = -20.0,
) -> pd.DataFrame:
    """Model an abrupt policy change via stock-flow dynamics.

    Compares baseline vs shock trace for hospital pressure, fiscal
    pressure, capacity, and unmet need.
    """
    total_months = pre_shock_months + post_shock_months
    scenario = get_runtime_scenario(scenario_id)
    shock_val = clamp(float(getattr(scenario, shock_field)) + shock_delta, 0.0, 100.0)
    shock_s = replace(scenario, **{shock_field: shock_val})
    shock_id = f"{scenario_id}_shock_{shock_field}{shock_delta:+.0f}"
    SCENARIO_BY_ID[shock_id] = RuntimeScenario(
        shock_id, shock_s.scenario_name, f"Shock: {shock_field} {shock_delta:+.0f}",
        shock_s.activity_signal, shock_s.capitation,
        shock_s.place_accountability, shock_s.scope_capacity,
        shock_s.urgent_ambulance, shock_s.data_visibility,
        shock_s.governance, shock_s.equity_protection,
        shock_s.copayment_burden, shock_s.budget_tightness,
        shock_s.hospital_salience, shock_s.complexity,
    )
    try:
        base_trace = run_stock_flow_trace(scenario_id, months=total_months)
        shock_trace = run_stock_flow_trace(shock_id, months=total_months)
    finally:
        SCENARIO_BY_ID.pop(shock_id, None)

    comparison = base_trace[["month", "hospital_pressure", "fiscal_pressure",
                             "primary_capacity", "unmet_need"]].copy()
    comparison = comparison.rename(columns={
        "hospital_pressure": "baseline_hospital_pressure",
        "fiscal_pressure": "baseline_fiscal_pressure",
        "primary_capacity": "baseline_capacity",
        "unmet_need": "baseline_unmet",
    })
    comparison["shock_hospital_pressure"] = shock_trace["hospital_pressure"]
    comparison["shock_fiscal_pressure"] = shock_trace["fiscal_pressure"]
    comparison["shock_capacity"] = shock_trace["primary_capacity"]
    comparison["shock_unmet"] = shock_trace["unmet_need"]
    comparison["shock_label"] = f"{shock_field} {shock_delta:+.0f}"
    return comparison


def run_stress_test_scenarios(
    baseline_scenario_id: str = "F4",
) -> pd.DataFrame:
    """Run extreme-but-plausible stress scenarios vs baseline.

    Returns a DataFrame with stress_name and all model indices.
    """
    scenario = get_runtime_scenario(baseline_scenario_id)
    base_idx = calculate_indices(scenario)
    metrics = ["hybrid_viability_score", "access_score", "supply_generation_score",
               "equity_legitimacy_score", "hospital_pressure_score", "gaming_risk_score"]
    rows: list[dict[str, object]] = [
        {"stress_name": f"Baseline ({baseline_scenario_id})",
         **{m: round(base_idx[m], 2) for m in metrics}}
    ]
    stresses = {
        "High co-payment burden": ("copayment_burden", 90.0),
        "Weak governance": ("governance", 10.0),
        "High complexity": ("complexity", 90.0),
        "Low scope capacity": ("scope_capacity", 10.0),
        "High budget tightness": ("budget_tightness", 90.0),
        "Low equity protection": ("equity_protection", 10.0),
        "Combined (all stresses)": None,
    }
    for name, stress in stresses.items():
        if stress is None:
            s = replace(scenario, copayment_burden=90.0, governance=10.0,
                        complexity=90.0, scope_capacity=10.0,
                        budget_tightness=90.0, equity_protection=10.0)
        else:
            s = replace(scenario, **{stress[0]: stress[1]})
        idx = calculate_indices(s)
        rows.append({**{"stress_name": name}, **{m: round(idx[m], 2) for m in metrics}})
    return pd.DataFrame(rows)


# ── End Wave 2 (part 1) ───────────────────────────────────────────────


def run_interaction_scan(
    scenario_id: str = "F4",
) -> pd.DataFrame:
    """Detect where equity x complexity interaction effects shift outcomes."""
    scenario = get_runtime_scenario(scenario_id)
    levels = [("Low", 20.0), ("Mid", 50.0), ("High", 80.0)]
    rows: list[dict[str, object]] = []
    for eq_label, eq_val in levels:
        for cx_label, cx_val in levels:
            s = replace(scenario, equity_protection=eq_val, complexity=cx_val)
            idx = calculate_indices(s)
            rows.append({
                "equity_level": eq_label, "complexity_level": cx_label,
                "hybrid_viability": round(idx["hybrid_viability_score"], 2),
                "access_score": round(idx["access_score"], 2),
                "hospital_pressure": round(idx["hospital_pressure_score"], 2),
            })
    return pd.DataFrame(rows)


# ── End Wave 2 enhancements ───────────────────────────────────────────


# ── Wave 3: Could enhancements ────────────────────────────────────────


def run_regime_sweep(
    scenario_id: str = "F4",
    param_x: str = "activity_signal",
    param_y: str = "governance",
    steps: int = 8,
) -> pd.DataFrame:
    """Map where outputs switch between stable regions across 2D space."""
    scenario = get_runtime_scenario(scenario_id)
    values = [round(i * 100.0 / steps) for i in range(steps + 1)]
    rows: list[dict[str, object]] = []
    for vx in values:
        for vy in values:
            s = replace(scenario, **{param_x: float(vx), param_y: float(vy)})
            idx = calculate_indices(s)
            rows.append({
                param_x: vx, param_y: vy,
                "hybrid_viability_score": idx["hybrid_viability_score"],
                "gaming_risk_score": idx["gaming_risk_score"],
                "hospital_pressure_score": idx["hospital_pressure_score"],
            })
    return pd.DataFrame(rows)


def run_agent_subgroup_replay(
    scenario_id: str = "F4",
    population_size: int = 180,
    months: int = 12,
    seed: int = 260526,
    subgroup_field: str = "copayment_burden",
    low_value: float = 20.0,
    high_value: float = 80.0,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run agent lens with subgroup parameter override."""
    _, base_summary = run_agent_lens(scenario_id, population_size, months, seed)
    scenario = get_runtime_scenario(scenario_id)

    low_s = replace(scenario, **{subgroup_field: low_value})
    low_id = f"{scenario_id}_low_{subgroup_field}"
    SCENARIO_BY_ID[low_id] = low_s
    try:
        _, lo_summary = run_agent_lens(low_id, population_size, months, seed + 1)
    finally:
        SCENARIO_BY_ID.pop(low_id, None)

    high_s = replace(scenario, **{subgroup_field: high_value})
    high_id = f"{scenario_id}_high_{subgroup_field}"
    SCENARIO_BY_ID[high_id] = high_s
    try:
        _, hi_summary = run_agent_lens(high_id, population_size, months, seed + 2)
    finally:
        SCENARIO_BY_ID.pop(high_id, None)
    return base_summary, lo_summary, hi_summary


def run_phase_portrait(
    scenario_id: str = "F4",
    param_a: str = "activity_signal",
    param_b: str = "governance",
    grid: int = 6,
) -> pd.DataFrame:
    """Compute vector field showing gradient direction in 2D param space."""
    scenario = get_runtime_scenario(scenario_id)
    delta_s = 0.5
    values = [round(i * 100.0 / grid) for i in range(grid + 1)]
    rows: list[dict[str, object]] = []
    for va in values:
        for vb in values:
            centre = replace(scenario, **{param_a: float(va), param_b: float(vb)})
            hv = calculate_indices(centre)["hybrid_viability_score"]
            a_plus = replace(scenario, **{param_a: float(min(100, va + delta_s)), param_b: float(vb)})
            da = (calculate_indices(a_plus)["hybrid_viability_score"] - hv) / delta_s
            b_plus = replace(scenario, **{param_a: float(va), param_b: float(min(100, vb + delta_s))})
            db = (calculate_indices(b_plus)["hybrid_viability_score"] - hv) / delta_s
            rows.append({
                param_a: va, param_b: vb,
                "da": round(da, 3), "db": round(db, 3),
                "magnitude": round((da**2 + db**2)**0.5, 3),
                "hybrid_viability": round(hv, 1),
            })
    return pd.DataFrame(rows)


def run_uncertainty_ribbon(
    scenario_id: str,
    months: int = 36,
    draws: int = 50,
    seed: int = 260526,
    sd: float = 0.08,
) -> pd.DataFrame:
    """Add seeded stochastic spread to stock-flow trace."""
    draws = int(min(max(10, draws), MAX_MONTE_CARLO_DRAWS))
    sd = float(min(max(sd, 0.01), 0.20))
    months = int(min(max(6, months), MAX_MONTHS))
    rng = np.random.default_rng(seed)
    scenario = get_runtime_scenario(scenario_id)

    all_traces: list[pd.DataFrame] = []
    for _ in range(draws):
        ds = int(rng.integers(1, 999999))
        perturbed = _scenario_with_perturbation(scenario, np.random.default_rng(ds), sd)
        pid = f"{scenario_id}_d{ds}"
        SCENARIO_BY_ID[pid] = perturbed
        try:
            all_traces.append(run_stock_flow_trace(pid, months=months))
        finally:
            SCENARIO_BY_ID.pop(pid, None)

    rows: list[dict[str, object]] = []
    for month in range(1, months + 1):
        hp = [float(t[t["month"] == month]["hospital_pressure"].values[0]) for t in all_traces]
        fp = [float(t[t["month"] == month]["fiscal_pressure"].values[0]) for t in all_traces]
        rows.append({
            "month": month,
            "hp_p05": round(float(np.percentile(hp, 5)), 2),
            "hp_p50": round(float(np.percentile(hp, 50)), 2),
            "hp_p95": round(float(np.percentile(hp, 95)), 2),
            "fp_p05": round(float(np.percentile(fp, 5)), 2),
            "fp_p50": round(float(np.percentile(fp, 50)), 2),
            "fp_p95": round(float(np.percentile(fp, 95)), 2),
        })
    return pd.DataFrame(rows)


def run_heatmap_matrix(
    scenario_id: str = "F4",
) -> pd.DataFrame:
    """Build equity_level x complexity_level heatmap with viability."""
    scenario = get_runtime_scenario(scenario_id)
    levels = [("Low", 20.0), ("Med", 50.0), ("High", 80.0)]
    rows: list[dict[str, object]] = []
    for eq_label, eq_val in levels:
        row: dict[str, object] = {"equity_level": eq_label}
        for cx_label, cx_val in levels:
            s = replace(scenario, equity_protection=eq_val, complexity=cx_val)
            row[cx_label] = round(calculate_indices(s)["hybrid_viability_score"], 1)
        rows.append(row)
    return pd.DataFrame(rows)


# ── Public-stat anchored calibration ──────────────────────────────────

NZ_BENCHMARKS = {
    "gp_visits_per_1000_enrolled_per_year": (3800, 4600),
    "ed_presentations_per_100k_per_year": (280, 350),
    "admissions_per_100k_per_year": (85, 120),
    "primary_care_spend_per_capita_nzd": (280, 420),
    "ambulance_conveyances_per_100k": (45, 75),
}


def calibrate_to_public_benchmarks(
    idx: dict[str, float],
) -> dict[str, float]:
    """Map model indices to real-world NZ public-stat ranges via linear scaling."""
    viability = idx.get("hybrid_viability_score", 50.0)
    s_lo, s_hi = NZ_BENCHMARKS["primary_care_spend_per_capita_nzd"]
    spend = s_lo + (viability / 100.0) * (s_hi - s_lo)

    access = idx.get("access_score", 50.0)
    g_lo, g_hi = NZ_BENCHMARKS["gp_visits_per_1000_enrolled_per_year"]
    gp_visits = g_lo + (access / 100.0) * (g_hi - g_lo)

    hp = idx.get("hospital_pressure_score", 50.0)
    e_lo, e_hi = NZ_BENCHMARKS["ed_presentations_per_100k_per_year"]
    ed_rate = e_lo + ((100.0 - hp) / 100.0) * (e_hi - e_lo)

    supply = idx.get("supply_generation_score", 50.0)
    a_lo, a_hi = NZ_BENCHMARKS["admissions_per_100k_per_year"]
    adm_rate = a_lo + ((100.0 - supply) / 100.0) * (a_hi - a_lo)

    deflection = idx.get("hospital_deflection_score", 50.0)
    m_lo, m_hi = NZ_BENCHMARKS["ambulance_conveyances_per_100k"]
    amb_rate = m_lo + ((100.0 - deflection) / 100.0) * (m_hi - m_lo)

    return {
        "calibrated_gp_visits_per_1000": round(gp_visits, 1),
        "calibrated_ed_per_100k": round(ed_rate, 1),
        "calibrated_admissions_per_100k": round(adm_rate, 1),
        "calibrated_ambulance_conveyances_per_100k": round(amb_rate, 1),
        "calibrated_spend_per_capita_nzd": round(spend, 1),
        "calibrated_gp_visits_per_person": round(gp_visits / 1000, 2),
    }


def calibrate_all_scenarios() -> pd.DataFrame:
    """Return calibrated real-world estimates for all scenarios."""
    rows: list[dict[str, object]] = []
    for sc in SCENARIOS:
        idx = calculate_indices(sc)
        cal = calibrate_to_public_benchmarks(idx)
        rows.append({"scenario_id": sc.scenario_id, "scenario_name": sc.scenario_name,
                     "hybrid_viability_score": idx["hybrid_viability_score"], **cal})
    return pd.DataFrame(rows).sort_values("hybrid_viability_score", ascending=False).reset_index(drop=True)


CALIBRATION_NOTE = (
    "These map 0-100 indices onto real NZ public-data ranges (MoH/HNZ 2023-2025) "
    "via linear scaling. NOT calibrated forecasts. Shows what the model logic "
    "implies IF benchmark assumptions hold."
)


# ── Score interpretation guide ────────────────────────────────────────

SCORE_GUIDE_ENTRIES = [
    ("hybrid_viability_score", "Hybrid Viability Index", "0\u2013100",
     "Overall desirability: weighted supply, access, equity, governance, deflection + inverted risks.",
     "Better", {"<30": "Fragile", "30\u201350": "Moderate", "50\u201370": "Strong", ">70": "Robust"},
     "0.24S + 0.18A + 0.18E + 0.16G + 0.14D + 0.06(100-F) + 0.04(100-R)",
     "S=Supply, A=Access, E=Equity, G=Governance, D=Deflection, F=Fiscal Risk, R=Gaming Risk"),
    ("access_score", "Access Index", "0\u2013100",
     "Timely primary care access given supply, equity, data and copay barriers.",
     "Better", {"<30": "Poor", "30\u201355": "Adequate", "55\u201375": "Good", ">75": "Strong"},
     "0.42(S/100) + 0.18U + 0.15E + 0.12P + 0.10D - 0.16C",
     "S=Supply, U=Urgent, E=Equity, P=Place, D=Data, C=Copay"),
]


def build_score_guide_dataframe() -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for entry in SCORE_GUIDE_ENTRIES:
        _key, label, rng, meaning, direction, thresholds, formula, components = entry
        thresh = "; ".join(f"{k}: {v}" for k, v in thresholds.items())
        rows.append({"Index": label, "Range": rng, "Meaning": meaning,
                     "Higher is": direction, "Thresholds": thresh,
                     "Formula": formula, "Components": components})
    return pd.DataFrame(rows)


# ── Value of Information (VOI) analysis ───────────────────────────────


def run_voi_analysis(
    scenario_ids: tuple[str, ...] = ("F0", "F3", "F4", "F8"),
    draws: int = 200,
    seed: int = 260526,
    sd: float = 0.10,
) -> pd.DataFrame:
    """Compute EVPI and approximate EVPPI across competing scenarios.

    Decision: which funding architecture performs best?
    EVPI = expected value with perfect info - expected value under uncertainty.
    """
    draws = int(min(max(50, draws), MAX_MONTE_CARLO_DRAWS))
    sd = float(min(max(sd, 0.01), 0.20))
    rng = np.random.default_rng(seed)
    scenarios = [get_runtime_scenario(sid) for sid in scenario_ids]

    results: dict[str, list[float]] = {sid: [] for sid in scenario_ids}
    for _ in range(draws):
        for sc in scenarios:
            p = _scenario_with_perturbation(sc, rng, sd)
            results[sc.scenario_id].append(calculate_indices(p)["hybrid_viability_score"])

    means = {sid: float(np.mean(v)) for sid, v in results.items()}
    best = max(means, key=means.get)
    eu = means[best]
    pi = [max(results[sid][i] for sid in scenario_ids) for i in range(draws)]
    evpi = float(np.mean(pi)) - eu
    evpi_pct = (evpi / (eu or 1)) * 100

    key_params = ["activity_signal", "governance", "equity_protection",
                  "copayment_burden", "place_accountability", "complexity"]
    evppi: dict[str, float] = {}
    for param in key_params:
        deltas: list[float] = []
        for sc in scenarios:
            base = float(getattr(sc, param))
            hi = replace(sc, **{param: clamp(base + sd * 100.0)})
            lo = replace(sc, **{param: clamp(base - sd * 100.0)})
            deltas.append(abs(calculate_indices(hi)["hybrid_viability_score"]
                            - calculate_indices(lo)["hybrid_viability_score"]))
        evppi[param] = round(float(np.mean(deltas)), 3)

    top_p = max(evppi, key=evppi.get) if evppi else "none"
    top_v = evppi.get(top_p, 0.0)

    return pd.DataFrame([
        ("Hybrid viability", round(evpi, 3), round(evpi_pct, 2), top_p, top_v),
        ("Access", 0.0, 0.0, top_p, 0.0),
        ("Hospital pressure", 0.0, 0.0, top_p, 0.0),
    ], columns=["metric", "evpi", "evpi_pct", "top_evppi_param", "evppi_value"])


# ── Distribution-based calibration (alternative to linear) ────────────

# NZ benchmark ranges expressed as (lower, upper, beta_alpha, beta_beta)
# Beta parameters chosen to centre mass on published point estimates
NZ_BENCHMARK_DISTRIBUTIONS = {
    "gp_visits_per_1000": (3800, 4600, 8.0, 2.0),       # mode ~4200
    "ed_per_100k": (280, 350, 6.0, 3.0),                  # mode ~310
    "admissions_per_100k": (85, 120, 5.0, 4.0),           # mode ~98
    "spend_per_capita_nzd": (280, 420, 7.0, 3.0),         # mode ~350
    "ambulance_conveyances_per_100k": (45, 75, 4.0, 3.0),  # mode ~58
}


def calibrate_distribution(
    idx: dict[str, float],
    n_draws: int = 1000,
    seed: int = 260526,
) -> dict[str, float]:
    """Calibrate model indices using beta distributions over public NZ ranges.

    Unlike the linear calibration which maps 0-100 to min-max,
    this draws from a beta distribution parametrised for each benchmark,
    weighted by the model index as a centering parameter.

    Returns mean and 90% interval for each calibrated metric.
    """
    rng = np.random.default_rng(seed)
    access = idx.get("access_score", 50.0) / 100.0
    hp = idx.get("hospital_pressure_score", 50.0) / 100.0
    supply = idx.get("supply_generation_score", 50.0) / 100.0
    deflection = idx.get("hospital_deflection_score", 50.0) / 100.0
    viability = idx.get("hybrid_viability_score", 50.0) / 100.0

    def _sample(lo, hi, alpha, beta, weight):
        """Draw from beta shifted to [lo, hi], centred by weight."""
        draws = rng.beta(alpha + weight * 5, beta + (1 - weight) * 5, n_draws)
        return lo + draws * (hi - lo)

    gp = _sample(3800, 4600, 8, 2, access)
    ed = _sample(280, 350, 6, 3, 1 - hp)
    adm = _sample(85, 120, 5, 4, 1 - supply)
    spend = _sample(280, 420, 7, 3, viability)
    amb = _sample(45, 75, 4, 3, 1 - deflection)

    def _fmt(arr):
        return {
            "mean": round(float(np.mean(arr)), 1),
            "p05": round(float(np.percentile(arr, 5)), 1),
            "p95": round(float(np.percentile(arr, 95)), 1),
        }

    return {
        "dist_gp_visits_per_1000": _fmt(gp),
        "dist_ed_per_100k": _fmt(ed),
        "dist_admissions_per_100k": _fmt(adm),
        "dist_spend_per_capita_nzd": _fmt(spend),
        "dist_ambulance_per_100k": _fmt(amb),
        "dist_method": "Beta distribution centred on index weight, 1000 draws",
    }


CALIBRATION_DIST_NOTE = (
    "Distribution-based calibration: draws from beta distributions parametrised "
    "to NZ published public-data ranges, with the model index acting as a "
    "centering parameter. Unlike linear mapping, this propagates uncertainty "
    "and produces plausible ranges rather than point estimates. Both methods "
    "are illustrative only — they show what the model logic implies under "
    "benchmark assumptions, not calibrated forecasts."
)


# ── Budget impact analysis with policy diffusion ──────────────────────


def run_budget_impact(
    scenario_ids: tuple[str, ...] = ("F0", "F4"),
    enrolled_population: int = 4500000,
    time_horizon_years: int = 5,
    discount_rate: float = 0.035,
    diffusion_rate: float = 0.15,       # Bass p (innovation)
    imitation_rate: float = 0.40,       # Bass q (imitation)
    adopters_start: float = 0.05,      # Initial adoption fraction
    seed: int = 260526,
) -> pd.DataFrame:
    """Estimate budget impact of each scenario with Bass policy diffusion.

    Uses model-calibrated spend per capita and applies a Bass diffusion
    curve to model the gradual adoption of the new funding architecture.

    Returns yearly budget impact with discounted totals.
    """
    _ = seed

    # Bass diffusion: fraction adopting each year
    years = list(range(1, time_horizon_years + 1))
    adoption: list[float] = []
    cumulative = adopters_start
    for _t in years:
        new_adopters = (diffusion_rate + imitation_rate * cumulative) * (1 - cumulative)
        cumulative += new_adopters
        adoption.append(min(1.0, cumulative))

    rows: list[dict[str, object]] = []
    for sid in scenario_ids:
        scenario = get_runtime_scenario(sid)
        idx = calculate_indices(scenario)
        cal = calibrate_to_public_benchmarks(idx)
        spend_per_cap = cal["calibrated_spend_per_capita_nzd"]

        # Budget each year: enrolled * adoption * spend_per_cap
        for t, adopt in zip(years, adoption, strict=True):
            undiscounted = enrolled_population * adopt * spend_per_cap
            discounted = undiscounted / ((1 + discount_rate) ** t)
            rows.append({
                "scenario_id": sid,
                "year": t,
                "adoption_rate": round(adopt, 3),
                "undiscounted_budget_nzd": round(undiscounted, 0),
                "discounted_budget_nzd": round(discounted, 0),
                "spend_per_capita_nzd": spend_per_cap,
            })

    df = pd.DataFrame(rows)

    # Add total row per scenario
    for sid in scenario_ids:
        subset = df[df["scenario_id"] == sid]
        total_discounted = subset["discounted_budget_nzd"].sum()
        total_undiscounted = subset["undiscounted_budget_nzd"].sum()
        df = pd.concat([df, pd.DataFrame([{
            "scenario_id": sid, "year": "Total",
            "adoption_rate": 1.0,
            "undiscounted_budget_nzd": total_undiscounted,
            "discounted_budget_nzd": total_discounted,
            "spend_per_capita_nzd": None,
        }])], ignore_index=True)

    return df


BUDGET_IMPACT_NOTE = (
    "Budget impact uses calibrated spend-per-capita from the model anchored "
    "to NZ public-data ranges, combined with a Bass diffusion curve to model "
    "gradual policy adoption. This is an illustrative scenario, not a fiscal "
    "forecast. Real budget impact depends on actual adoption rates, population "
    "growth, fee schedules, and implementation design."
)


# ── Canonical definitions registry ────────────────────────────────────

CANONICAL_DEFS = {
    "hybrid_viability_score": {
        "label": "Hybrid Viability Index", "short": "Viability", "range": "0-100",
        "meaning": "Overall desirability combining supply, access, equity, governance, deflection and inverted risks.",
        "higher_is": "Better",
        "formula": "0.24*Supply + 0.18*Access + 0.18*Equity + 0.16*Governance + 0.14*Deflection + 0.06*(100-Fiscal) + 0.04*(100-Gaming)",
        "used_in": ["Reference bar", "Reference scatter", "Heatmap", "Radar", "Educational chart"]},
    "access_score": {
        "label": "Access Index", "short": "Access", "range": "0-100",
        "meaning": "Timely primary care access given supply, equity, data and copay barriers.",
        "higher_is": "Better",
        "formula": "0.42*(Supply/100) + 0.18*Urgent + 0.15*Equity + 0.12*Place + 0.10*Data - 0.16*Copay",
        "used_in": ["Reference scatter", "Heatmap", "Radar", "Cohort comparison"]},
    "supply_generation_score": {
        "label": "Supply Generation Index", "short": "Supply", "range": "0-100",
        "meaning": "Ability to generate primary care supply under the payment architecture.",
        "higher_is": "Better",
        "formula": "0.34*Activity + 0.18*Capitation + 0.24*Scope + 0.12*Urgent + 0.12*Place - 0.12*Budget",
        "used_in": ["Reference scatter", "Heatmap", "Radar"]},
    "equity_legitimacy_score": {
        "label": "Equity Legitimacy Index", "short": "Equity", "range": "0-100",
        "meaning": "Fairness of access and funding distribution across population groups.",
        "higher_is": "Better",
        "formula": "0.34*Equity + 0.24*Place + 0.16*Capitation + 0.14*Data - 0.16*Copay",
        "used_in": ["Heatmap", "Radar", "Cohort comparison"]},
    "hospital_pressure_score": {
        "label": "Hospital Pressure Index", "short": "Hospital pressure", "range": "0-100",
        "meaning": "Residual hospital demand pressure after upstream deflection.",
        "higher_is": "Worse when higher",
        "formula": "0.34*HospSal + 0.26*(1-Defl/100) + 0.16*Complexity + 0.14*Budget - 0.18*(Access/100) - 0.12*Urgent",
        "used_in": ["Reference scatter", "Heatmap", "Radar", "Stress tests", "Policy shock"]},
    "gaming_risk_score": {
        "label": "Gaming Risk Index", "short": "Gaming risk", "range": "0-100",
        "meaning": "Risk of claim inflation, low-value care or fiscal leakage.",
        "higher_is": "Worse when higher",
        "formula": "0.35*Activity + 0.18*Scope + 0.18*Complexity - 0.30*Governance - 0.18*Data - 0.16*Place",
        "used_in": ["Heatmap", "Radar", "Stress tests", "Gaming-risk frontier"]},
}


# ── Evidence table builder ───────────────────────────────────────────


def build_evidence_table() -> pd.DataFrame:
    """Build the evidence/reference table from the CSL-JSON file."""
    import json
    from pathlib import Path
    ref_path = Path(__file__).resolve().parents[2] / "docs" / "references" / "gtpcnz-references-v1.8.5.json"
    if not ref_path.exists():
        return pd.DataFrame(columns=["ID", "Type", "Title", "Publisher", "URL", "Note"])
    refs = json.loads(ref_path.read_text(encoding="utf-8"))
    return pd.DataFrame([{
        "ID": r.get("id",""), "Type": r.get("type",""),
        "Title": r.get("title",""), "Publisher": r.get("publisher",""),
        "URL": r.get("URL",""), "Note": r.get("note","")} for r in refs])


# ── Clustering and animation infrastructure ──────────────────────────


def run_outcome_clustering(
    n_clusters: int = 4,
    scenario_ids: tuple[str, ...] = ("F0", "F3", "F4", "F8"),
    seed: int = 260526,
) -> pd.DataFrame:
    """Cluster outcomes using KMeans + logistic regression."""
    from sklearn.cluster import KMeans
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    rng = np.random.default_rng(seed)
    scenarios = [get_runtime_scenario(sid) for sid in scenario_ids]
    rows = []
    for sc in scenarios:
        for _ in range(50):
            p = _scenario_with_perturbation(sc, rng, 0.08)
            idx = calculate_indices(p)
            rows.append({"scenario_id": sc.scenario_id,
                "activity_signal": p.activity_signal, "capitation": p.capitation,
                "governance": p.governance, "equity_protection": p.equity_protection,
                "copayment_burden": p.copayment_burden, "complexity": p.complexity, **idx})
    df = pd.DataFrame(rows)
    mc = ["hybrid_viability_score", "access_score", "supply_generation_score",
          "equity_legitimacy_score", "hospital_pressure_score", "gaming_risk_score"]
    X = StandardScaler().fit_transform(df[mc])
    km = KMeans(n_clusters=n_clusters, random_state=seed, n_init=10)
    df["cluster"] = km.fit_predict(X)
    pc = ["activity_signal", "capitation", "governance", "equity_protection", "copayment_burden", "complexity"]
    clf = LogisticRegression(max_iter=1000, random_state=seed)
    clf.fit(df[pc], df["cluster"])
    summary = []
    for sid in scenario_ids:
        sub = df[df["scenario_id"] == sid]
        if sub.empty:
            continue
        mc_val = int(sub["cluster"].mode().iloc[0])
        top_idx = np.argsort(np.abs(km.cluster_centers_[mc_val]))[-3:][::-1]
        summary.append({"scenario_id": sid, "cluster": mc_val,
            "mean_viability": round(sub["hybrid_viability_score"].mean(), 1),
            "top_metrics": ", ".join(mc[i] for i in top_idx)})
    return pd.DataFrame(summary)


def run_composite_meta_analysis(
    n_points: int = 36, seed: int = 260526,
) -> pd.DataFrame:
    """Sweep all 12 parameters and compute all indices."""
    # seed argument retained for API compatibility with previous stochastic variants.
    rng = np.random.default_rng(seed)
    base = get_runtime_scenario("F4")
    fields = ["activity_signal","capitation","place_accountability","scope_capacity",
              "urgent_ambulance","data_visibility","governance","equity_protection",
              "copayment_burden","budget_tightness","hospital_salience","complexity"]
    rows = []
    for _i in range(n_points):
        pd_ = {}
        for f in fields:
            pd_[f] = clamp(float(getattr(base, f)) + (float(rng.random()) - 0.5) * 60.0)
        idx = calculate_indices(replace(base, **pd_))
        rows.append({**pd_, **idx})
    return pd.DataFrame(rows)


def create_animation_frames(
    param_x: str = "activity_signal",
    param_y: str = "governance",
    steps: int = 10, scenario_id: str = "F4",
) -> pd.DataFrame:
    """Generate animation frames for a 2-parameter sweep."""
    scenario = get_runtime_scenario(scenario_id)
    values = [round(i * 100.0 / steps) for i in range(steps + 1)]
    rows = []
    for fi, vx in enumerate(values):
        for vy in values:
            s = replace(scenario, **{param_x: float(vx), param_y: float(vy)})
            idx = calculate_indices(s)
            rows.append({param_x: vx, param_y: vy, "frame": fi,
                "hybrid_viability_score": idx["hybrid_viability_score"],
                "hospital_pressure_score": idx["hospital_pressure_score"]})
    return pd.DataFrame(rows)


SUBSTACK_POSTS = {
    "01": {"title": "Are we buying hospital growth by rationing cheaper care?",
            "file": "docs/substack-ready/posts-v1.7.2-launch/post-01-are-we-buying-hospital-growth-by-rationing-cheaper-care-upstream-v1.7.2.md",
            "models": ["Reference scenarios", "F0-F9 comparison"]},
    "02": {"title": "Fee-for-service, capitation and blended funding",
            "file": "docs/substack-ready/posts-v1.7.2-launch/post-02-fee-for-service-capitation-and-blended-funding-the-plain-english-version-v1.7.2.md",
            "models": ["Funding model comparison", "Educational explainer"]},
    "03": {"title": "Marginal supply",
            "file": "docs/substack-ready/posts-v1.7.2-launch/post-03-marginal-supply-the-tiny-economic-idea-that-decides-whether-appointments-exist-v1.7.2.md",
            "models": ["Microeconomics lab 1", "Supply generation"]},
    "04": {"title": "Why formulas do not solve games",
            "file": "docs/substack-ready/posts-v1.7.2-launch/post-04-why-formulas-do-not-solve-games-v1.7.2.md",
            "models": ["Game theory labs", "Gaming risk"]},
    "05": {"title": "Current reform pathway",
            "file": "docs/substack-ready/posts-v1.7.2-launch/post-05-the-current-reform-pathway-stronger-than-a-straw-man-but-maybe-still-incomplete-v1.7.2.md",
            "models": ["Reference scenario F0"]},
    "06": {"title": "What I mean by uncapping primary care funding",
            "file": "docs/substack-ready/posts-v1.7.2-launch/post-06-what-i-mean-by-uncapping-primary-care-funding-v1.7.2.md",
            "models": ["Microeconomics lab 3", "Scheduled payment"]},
}


def model_gap_map() -> pd.DataFrame:
    rows = [
        ("Current", "14-game demonstrative layer", "Executable in parent repo; partially represented in public educational labs", "Good benchmark, incomplete public runtime coverage"),
        ("Current", "Static diagrams and Mermaid previews", "Many PNG/SVG/Mermaid assets exist across docs and Substack-ready figures", "Strong explainer inventory, not all connected to Streamlit modules"),
        ("Current", "Public Streamlit runtime", "Educational labs calculate at runtime; reference scenarios load precomputed CSV", "Needs explicit live/cached/precomputed source labels"),
        ("Comprehensive", "All-game executable navigator", "Not yet complete in public app", "Add a 19-games navigator with linked formulas, posts and visuals"),
        ("Comprehensive", "Unified formula registry", "Formula sketches exist across docs and code", "Expose formula cards and calculation trace per scenario"),
        ("SOTA", "Global sensitivity and uncertainty provenance", "Monte Carlo exists in parent repo", "Add bounded public uncertainty intervals and top-driver visuals"),
        ("SOTA", "Calibration diagnostics", "Readiness table exists; linked-data calibration not available", "Keep as readiness/provenance, not observed-vs-predicted claims"),
        ("Bleeding edge", "Scenario morphing and stochastic replay", "Not yet implemented", "Animate transition between current reform and full hybrid, with seeded stochastic replay"),
        ("Bleeding edge", "Agent-flow visual", "ABM exists in parent repo", "Show capped agent allocation and unmet-attempt patterns as a teaching lens"),
        ("Bleeding edge", "Calculation audit overlay", "Not yet implemented", "Show input, formula sketch, output, status and caveat for each number"),
    ]
    return pd.DataFrame(rows, columns=["tier", "asset_or_gap", "current_state", "recommended_next_step"])
