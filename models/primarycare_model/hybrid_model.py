"""Final hybrid demonstrative model for the NZ primary care funding architecture project.

The hybrid model integrates the 14 mapped policy games into a single, auditable
scenario-level synthesis. It is deliberately non-calibrated. It should be read as
an executable policy logic model: it formalises mechanisms, interaction effects,
and priority empirical tests before real data calibration.

Outputs are on 0-100 scales unless otherwise stated. Higher is better for
access, viability, equity, governance, hospital deflection and hybrid viability.
Higher is worse for hospital pressure, implementation risk and fiscal/gaming
risk.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Mapping

import pandas as pd

from .demonstrative_games import GAME_MODELS, SCENARIOS, Scenario, clip
from .uncertainty import PARAMETER_FIELDS, run_monte_carlo, summarise_uncertainty


GAME_WEIGHTS: dict[str, float] = {
    "G1": 1.10,  # hospital-salience budget game
    "G2": 1.00,  # Health NZ internal allocation game
    "G3": 1.20,  # capitation marginal-supply game
    "G4": 1.00,  # consumer access pathway game
    "G5": 0.95,  # PHO intermediation game
    "G6": 0.95,  # ACC/Health NZ cross-funder game
    "G7": 0.90,  # ambulance conveyance game
    "G8": 1.05,  # scope-of-practice supply game
    "G9": 0.80,  # telehealth/local-supply game
    "G10": 1.00,  # co-payment calibration game
    "G11": 1.05,  # KPI salience game
    "G12": 1.10,  # equity and trust game
    "G13": 0.85,  # political economy game
    "G14": 0.90,  # data observability game
}


@dataclass(frozen=True)
class HybridOutcome:
    """Scenario-level hybrid synthesis output."""

    scenario_id: str
    scenario_name: str
    funding_architecture: str
    weighted_access: float
    weighted_provider_viability: float
    weighted_equity: float
    weighted_fiscal_control: float
    weighted_hospital_pressure: float
    weighted_gaming_risk: float
    weighted_welfare: float
    supply_generation_index: float
    equity_legitimacy_index: float
    governance_resilience_index: float
    hospital_deflection_index: float
    implementation_readiness_index: float
    fiscal_gaming_risk_index: float
    interaction_penalty: float
    hybrid_viability_score: float
    model_interpretation: str

    def as_row(self) -> dict[str, object]:
        row = asdict(self)
        for key, value in list(row.items()):
            if isinstance(value, float):
                row[key] = round(value, 2)
        return row


def _weighted_mean(values: Mapping[str, float], weights: Mapping[str, float] = GAME_WEIGHTS) -> float:
    total_weight = 0.0
    total = 0.0
    for game_id, value in values.items():
        weight = float(weights.get(game_id, 1.0))
        total += weight * float(value)
        total_weight += weight
    return total / total_weight


def _game_outcomes_for_scenario(scenario: Scenario) -> dict[str, object]:
    return {game_id: model(scenario) for game_id, model in GAME_MODELS.items()}


def _scenario_weighted_metrics(scenario: Scenario) -> dict[str, float]:
    outcomes = _game_outcomes_for_scenario(scenario)
    metrics = [
        "access_score",
        "provider_viability",
        "equity_score",
        "fiscal_control",
        "hospital_pressure",
        "gaming_risk",
        "system_welfare",
    ]
    result: dict[str, float] = {}
    for metric in metrics:
        values = {game_id: float(getattr(outcome, metric)) for game_id, outcome in outcomes.items()}
        result[metric] = _weighted_mean(values)
    return result


def classify_architecture(scenario: Scenario) -> str:
    """Classify scenario as a plain-language architecture."""

    if scenario.scenario_id == "S0":
        return "constrained capitation/contracting equilibrium"
    if scenario.scenario_id == "S1":
        return "improved capitation allocation without supply architecture reform"
    if scenario.scenario_id == "S2":
        return "rules-based primary care benefits schedule layered onto capitation"
    if scenario.scenario_id == "S3":
        return "full hybrid upstream access architecture"
    if scenario.scenario_id == "S4":
        return "demand-driven benefits with insufficient controls"
    return "unspecified architecture"


def interaction_penalty(scenario: Scenario, metrics: Mapping[str, float]) -> float:
    """Return a penalty for known interaction failure modes.

    The penalty is deliberately transparent and simple. It captures the policy
    argument that a benefit schedule alone is insufficient unless supply,
    governance, equity and observability levers move together.
    """

    # Supply remains suppressed when benefits/direct claiming/scope are weak and transaction/budget pressure high.
    supply_constraint = (
        0.35 * (1 - scenario.marginal_contact_benefit)
        + 0.25 * (1 - scenario.direct_claiming)
        + 0.20 * scenario.pho_transaction_cost
        + 0.20 * scenario.budget_tightness
    )

    # Demand-driven benefits can create risk if safety, coding, data and governance do not keep pace.
    benefit_intensity = 0.55 * scenario.marginal_contact_benefit + 0.45 * scenario.scope_flexibility
    control_strength = (
        0.30 * scenario.safety_governance
        + 0.30 * scenario.gaming_controls
        + 0.25 * scenario.data_observability
        + 0.15 * scenario.stakeholder_alignment
    )
    governance_gap = max(0.0, benefit_intensity - control_strength)

    # Co-payment can be a demand signal or an equity failure, depending on protections and equity infrastructure.
    equity_gap = max(
        0.0,
        scenario.copayment_level
        - 0.45 * scenario.copayment_protections
        - 0.35 * scenario.equity_program_strength
        - 0.20 * scenario.capitation_weighting,
    )

    # Telehealth substitution risk appears when telehealth scale is not integrated with local in-person support.
    telehealth_gap = max(
        0.0,
        scenario.telehealth_scale
        - 0.55 * scenario.telehealth_integration
        - 0.45 * scenario.local_inperson_loading,
    )

    # Hospital rescue persists when hospital pressure is visible but upstream KPIs/data are not.
    salience_gap = max(
        0.0,
        scenario.hospital_political_penalty
        - 0.50 * scenario.primary_kpi_salience
        - 0.25 * scenario.ambulance_kpi_salience
        - 0.25 * scenario.data_observability,
    )

    penalty = (
        8.0 * supply_constraint
        + 10.0 * governance_gap
        + 8.0 * equity_gap
        + 5.0 * telehealth_gap
        + 7.0 * salience_gap
        + 0.08 * float(metrics["gaming_risk"])
    )
    return clip(penalty, 0, 35)


def hybrid_outcome(scenario: Scenario) -> HybridOutcome:
    """Compute the hybrid synthesis outcome for a single scenario."""

    metrics = _scenario_weighted_metrics(scenario)
    supply_generation = clip(
        0.25 * metrics["access_score"]
        + 0.20 * metrics["provider_viability"]
        + 18 * scenario.marginal_contact_benefit
        + 10 * scenario.scope_flexibility
        + 8 * scenario.direct_claiming
        + 7 * (1 - scenario.pho_transaction_cost)
        + 6 * scenario.local_inperson_loading
        - 8 * scenario.budget_tightness
    )
    equity_legitimacy = clip(
        0.35 * metrics["equity_score"]
        + 16 * scenario.equity_program_strength
        + 12 * scenario.copayment_protections
        + 8 * scenario.capitation_weighting
        + 6 * (1 - scenario.copayment_level)
        + 4 * scenario.data_observability
    )
    governance_resilience = clip(
        0.25 * metrics["fiscal_control"]
        + 0.20 * (100 - metrics["gaming_risk"])
        + 13 * scenario.safety_governance
        + 12 * scenario.gaming_controls
        + 9 * scenario.data_observability
        + 5 * scenario.stakeholder_alignment
        + 4 * scenario.narrative_coherence
    )
    hospital_deflection = clip(
        0.35 * (100 - metrics["hospital_pressure"])
        + 0.20 * metrics["access_score"]
        + 15 * scenario.ambulance_alternative_funding
        + 8 * scenario.primary_kpi_salience
        + 7 * scenario.ambulance_kpi_salience
        + 5 * scenario.data_observability
    )
    implementation_readiness = clip(
        0.25 * governance_resilience
        + 0.20 * equity_legitimacy
        + 0.20 * scenario.stakeholder_alignment * 100
        + 0.15 * scenario.narrative_coherence * 100
        + 0.10 * scenario.data_observability * 100
        + 0.10 * scenario.safety_governance * 100
    )
    fiscal_gaming_risk = clip(
        0.45 * metrics["gaming_risk"]
        + 15 * scenario.marginal_contact_benefit * (1 - scenario.gaming_controls)
        + 12 * scenario.scope_flexibility * (1 - scenario.safety_governance)
        + 9 * scenario.direct_claiming * (1 - scenario.data_observability)
        + 8 * max(0.0, scenario.copayment_level - scenario.copayment_protections)
        + 6 * scenario.telehealth_scale * (1 - scenario.telehealth_integration)
    )
    penalty = interaction_penalty(scenario, metrics)
    viability = clip(
        0.25 * supply_generation
        + 0.22 * hospital_deflection
        + 0.22 * governance_resilience
        + 0.18 * equity_legitimacy
        + 0.13 * implementation_readiness
        - penalty
    )

    if scenario.scenario_id == "S3":
        interpretation = "Best-performing demonstrative architecture: demand-driven where eligible, but governed by scope, safety, data, KPIs and equity protections."
    elif scenario.scenario_id == "S2":
        interpretation = "Materially improves supply and hospital-pressure logic, but still needs stronger ambulance, equity, data and governance architecture."
    elif scenario.scenario_id == "S4":
        interpretation = "Shows why benefits cannot be loose: access rises, but fiscal/gaming/equity risks weaken viability."
    elif scenario.scenario_id == "S1":
        interpretation = "Improves allocation inside capitation but leaves the marginal supply and hospital-rescue games largely intact."
    else:
        interpretation = "Status quo equilibrium: upstream sectors are tightly managed while hospital pressure remains visible and fundable."

    return HybridOutcome(
        scenario_id=scenario.scenario_id,
        scenario_name=scenario.name,
        funding_architecture=classify_architecture(scenario),
        weighted_access=metrics["access_score"],
        weighted_provider_viability=metrics["provider_viability"],
        weighted_equity=metrics["equity_score"],
        weighted_fiscal_control=metrics["fiscal_control"],
        weighted_hospital_pressure=metrics["hospital_pressure"],
        weighted_gaming_risk=metrics["gaming_risk"],
        weighted_welfare=metrics["system_welfare"],
        supply_generation_index=supply_generation,
        equity_legitimacy_index=equity_legitimacy,
        governance_resilience_index=governance_resilience,
        hospital_deflection_index=hospital_deflection,
        implementation_readiness_index=implementation_readiness,
        fiscal_gaming_risk_index=fiscal_gaming_risk,
        interaction_penalty=penalty,
        hybrid_viability_score=viability,
        model_interpretation=interpretation,
    )


def run_hybrid_model(scenarios: Iterable[Scenario] = SCENARIOS) -> pd.DataFrame:
    """Run the hybrid model for all scenarios."""

    return pd.DataFrame([hybrid_outcome(scenario).as_row() for scenario in scenarios])


def hybrid_uncertainty(
    n_per_scenario: int = 1000,
    sd: float = 0.08,
    seed: int = 20260508,
) -> pd.DataFrame:
    """Monte Carlo wrapper for hybrid model outputs.

    This reuses perturbed scenarios from the uncertainty layer and computes
    hybrid scores for each draw. It does not calibrate outputs to observed data.
    """

    # Re-run a perturbation layer, then aggregate game-level draws by draw/scenario.
    draws = run_monte_carlo(n_per_scenario=n_per_scenario, sd=sd, seed=seed)

    # The game-level draw table includes the perturbed parameters repeated for each game.
    param_cols = list(PARAMETER_FIELDS)
    base_cols = ["scenario_id", "scenario_name", "draw"] + param_cols
    scenarios_by_draw = draws[base_cols].drop_duplicates().reset_index(drop=True)

    # Avoid importing dataclasses dynamically: construct Scenario rows directly.
    rows: list[dict[str, object]] = []
    for _, row in scenarios_by_draw.iterrows():
        scenario = Scenario(
            scenario_id=str(row["scenario_id"]),
            name=str(row["scenario_name"]),
            description="uncertainty draw",
            **{field: float(row[field]) for field in PARAMETER_FIELDS},
        )
        outcome = hybrid_outcome(scenario).as_row()
        outcome["draw"] = int(row["draw"])
        rows.append(outcome)
    return pd.DataFrame(rows)


def summarise_hybrid_uncertainty(draws: pd.DataFrame) -> pd.DataFrame:
    """Summarise hybrid uncertainty draws by scenario."""

    metrics = [
        "supply_generation_index",
        "equity_legitimacy_index",
        "governance_resilience_index",
        "hospital_deflection_index",
        "implementation_readiness_index",
        "fiscal_gaming_risk_index",
        "interaction_penalty",
        "hybrid_viability_score",
    ]
    grouped = draws.groupby(["scenario_id", "scenario_name"])[metrics]
    summary = grouped.agg(["mean", "std", lambda s: s.quantile(0.05), lambda s: s.quantile(0.95)])
    summary.columns = [f"{metric}_{stat if isinstance(stat, str) else 'p'}" for metric, stat in summary.columns]
    # Rename lambda-generated fields cleanly.
    summary = summary.rename(columns={col: col.replace("_<lambda_0>", "_p05").replace("_<lambda_1>", "_p95") for col in summary.columns})
    return summary.reset_index()


if __name__ == "__main__":
    print(run_hybrid_model().to_string(index=False))
