"""Demonstrative models for each mapped New Zealand policy game.

These are deliberately stylised, non-calibrated models. They are designed to
make the logic of each game executable and inspectable before empirical data,
stakeholder validation, OIA material, and formal calibration are available.

All inputs are normalised to 0..1 unless otherwise stated. Outputs are
normalised to 0..100, where higher is better except for hospital_pressure and
gaming_risk, where lower is better.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Dict, Iterable, List, Mapping
import math


def clip(value: float, low: float = 0.0, high: float = 100.0) -> float:
    """Clip a value to a range."""

    return max(low, min(high, value))


def sigmoid(value: float) -> float:
    """Return logistic transform."""

    return 1.0 / (1.0 + math.exp(-value))


@dataclass(frozen=True)
class Scenario:
    """Normalised scenario inputs for demonstrative game models."""

    scenario_id: str
    name: str
    description: str
    marginal_contact_benefit: float
    capitation_weighting: float
    scope_flexibility: float
    pho_transaction_cost: float
    primary_kpi_salience: float
    ambulance_kpi_salience: float
    hospital_political_penalty: float
    data_observability: float
    copayment_level: float
    copayment_protections: float
    equity_program_strength: float
    telehealth_scale: float
    telehealth_integration: float
    local_inperson_loading: float
    ambulance_alternative_funding: float
    acc_activity_funding: float
    acc_constraint: float
    budget_tightness: float
    safety_governance: float
    gaming_controls: float
    direct_claiming: float
    stakeholder_alignment: float
    narrative_coherence: float


@dataclass(frozen=True)
class GameOutcome:
    """Output for one game under one scenario."""

    game_id: str
    game_name: str
    scenario_id: str
    scenario_name: str
    access_score: float
    provider_viability: float
    equity_score: float
    fiscal_control: float
    hospital_pressure: float
    gaming_risk: float
    system_welfare: float
    equilibrium_label: str
    mechanism_summary: str

    def as_row(self) -> dict[str, object]:
        """Return a CSV-friendly row."""

        row = asdict(self)
        for key, value in list(row.items()):
            if isinstance(value, float):
                row[key] = round(value, 2)
        return row


SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        scenario_id="S0",
        name="Status quo tight control",
        description="Dominant capitation/contracting, PHO intermediation, limited marginal contact benefit, high hospital salience.",
        marginal_contact_benefit=0.05,
        capitation_weighting=0.30,
        scope_flexibility=0.25,
        pho_transaction_cost=0.65,
        primary_kpi_salience=0.15,
        ambulance_kpi_salience=0.20,
        hospital_political_penalty=0.90,
        data_observability=0.25,
        copayment_level=0.65,
        copayment_protections=0.35,
        equity_program_strength=0.55,
        telehealth_scale=0.55,
        telehealth_integration=0.35,
        local_inperson_loading=0.20,
        ambulance_alternative_funding=0.25,
        acc_activity_funding=0.65,
        acc_constraint=0.10,
        budget_tightness=0.85,
        safety_governance=0.70,
        gaming_controls=0.55,
        direct_claiming=0.00,
        stakeholder_alignment=0.30,
        narrative_coherence=0.20,
    ),
    Scenario(
        scenario_id="S1",
        name="Capitation reweighting only",
        description="Better allocation inside capitation, modest access target and data improvement, no material demand-driven benefit stream.",
        marginal_contact_benefit=0.12,
        capitation_weighting=0.75,
        scope_flexibility=0.30,
        pho_transaction_cost=0.60,
        primary_kpi_salience=0.35,
        ambulance_kpi_salience=0.25,
        hospital_political_penalty=0.85,
        data_observability=0.45,
        copayment_level=0.55,
        copayment_protections=0.45,
        equity_program_strength=0.70,
        telehealth_scale=0.60,
        telehealth_integration=0.40,
        local_inperson_loading=0.30,
        ambulance_alternative_funding=0.30,
        acc_activity_funding=0.65,
        acc_constraint=0.10,
        budget_tightness=0.78,
        safety_governance=0.75,
        gaming_controls=0.60,
        direct_claiming=0.05,
        stakeholder_alignment=0.40,
        narrative_coherence=0.35,
    ),
    Scenario(
        scenario_id="S2",
        name="Primary Care Benefits Schedule",
        description="Contact-type benefits added to capitation, direct/optional claiming, broader provider eligibility, moderate safeguards.",
        marginal_contact_benefit=0.70,
        capitation_weighting=0.75,
        scope_flexibility=0.60,
        pho_transaction_cost=0.25,
        primary_kpi_salience=0.55,
        ambulance_kpi_salience=0.45,
        hospital_political_penalty=0.75,
        data_observability=0.60,
        copayment_level=0.45,
        copayment_protections=0.60,
        equity_program_strength=0.70,
        telehealth_scale=0.65,
        telehealth_integration=0.55,
        local_inperson_loading=0.55,
        ambulance_alternative_funding=0.50,
        acc_activity_funding=0.65,
        acc_constraint=0.10,
        budget_tightness=0.60,
        safety_governance=0.75,
        gaming_controls=0.70,
        direct_claiming=0.80,
        stakeholder_alignment=0.55,
        narrative_coherence=0.60,
    ),
    Scenario(
        scenario_id="S3",
        name="Full upstream access architecture",
        description="Benefits schedule plus strong KPIs, data observability, ambulance alternatives, equity protections and governance.",
        marginal_contact_benefit=0.80,
        capitation_weighting=0.80,
        scope_flexibility=0.80,
        pho_transaction_cost=0.20,
        primary_kpi_salience=0.85,
        ambulance_kpi_salience=0.80,
        hospital_political_penalty=0.65,
        data_observability=0.85,
        copayment_level=0.35,
        copayment_protections=0.80,
        equity_program_strength=0.85,
        telehealth_scale=0.70,
        telehealth_integration=0.80,
        local_inperson_loading=0.80,
        ambulance_alternative_funding=0.75,
        acc_activity_funding=0.70,
        acc_constraint=0.00,
        budget_tightness=0.55,
        safety_governance=0.90,
        gaming_controls=0.85,
        direct_claiming=0.85,
        stakeholder_alignment=0.75,
        narrative_coherence=0.85,
    ),
    Scenario(
        scenario_id="S4",
        name="Loose benefits, weak controls",
        description="Demand-driven benefits with broad eligibility but weak governance, weak equity protections, weak data and high gaming risk.",
        marginal_contact_benefit=0.90,
        capitation_weighting=0.60,
        scope_flexibility=0.90,
        pho_transaction_cost=0.10,
        primary_kpi_salience=0.70,
        ambulance_kpi_salience=0.70,
        hospital_political_penalty=0.70,
        data_observability=0.45,
        copayment_level=0.65,
        copayment_protections=0.30,
        equity_program_strength=0.40,
        telehealth_scale=0.90,
        telehealth_integration=0.30,
        local_inperson_loading=0.20,
        ambulance_alternative_funding=0.60,
        acc_activity_funding=0.65,
        acc_constraint=0.00,
        budget_tightness=0.80,
        safety_governance=0.40,
        gaming_controls=0.25,
        direct_claiming=0.95,
        stakeholder_alignment=0.25,
        narrative_coherence=0.30,
    ),
)


def _welfare(access: float, viability: float, equity: float, fiscal: float, hospital_pressure: float, gaming: float) -> float:
    """Stylised system welfare with hospital pressure and gaming as penalties."""

    return clip(0.28 * access + 0.18 * viability + 0.22 * equity + 0.18 * fiscal + 0.14 * (100 - hospital_pressure) - 0.18 * gaming)


def _outcome(
    game_id: str,
    game_name: str,
    scenario: Scenario,
    access: float,
    viability: float,
    equity: float,
    fiscal: float,
    hospital_pressure: float,
    gaming: float,
    label: str,
    mechanism: str,
) -> GameOutcome:
    """Build a clipped GameOutcome."""

    access = clip(access)
    viability = clip(viability)
    equity = clip(equity)
    fiscal = clip(fiscal)
    hospital_pressure = clip(hospital_pressure)
    gaming = clip(gaming)
    return GameOutcome(
        game_id=game_id,
        game_name=game_name,
        scenario_id=scenario.scenario_id,
        scenario_name=scenario.name,
        access_score=access,
        provider_viability=viability,
        equity_score=equity,
        fiscal_control=fiscal,
        hospital_pressure=hospital_pressure,
        gaming_risk=gaming,
        system_welfare=_welfare(access, viability, equity, fiscal, hospital_pressure, gaming),
        equilibrium_label=label,
        mechanism_summary=mechanism,
    )


def model_g1_hospital_salience(s: Scenario) -> GameOutcome:
    upstream_salience = 0.45 * s.primary_kpi_salience + 0.25 * s.ambulance_kpi_salience + 0.30 * s.data_observability
    rescue_bias = s.hospital_political_penalty * (1 - 0.65 * upstream_salience)
    access = 22 + 30 * s.marginal_contact_benefit + 18 * s.primary_kpi_salience + 10 * s.ambulance_kpi_salience
    viability = 35 + 30 * s.marginal_contact_benefit - 15 * s.budget_tightness + 10 * upstream_salience
    equity = 35 + 25 * s.equity_program_strength + 20 * s.copayment_protections + 10 * upstream_salience
    fiscal = 82 - 30 * s.marginal_contact_benefit - 10 * (1 - s.gaming_controls) + 12 * s.data_observability
    hospital = 35 + 45 * rescue_bias + 15 * (1 - upstream_salience) - 25 * s.marginal_contact_benefit
    gaming = 12 + 25 * s.marginal_contact_benefit * (1 - s.gaming_controls) + 10 * (1 - s.data_observability)
    label = "hospital-rescue equilibrium" if rescue_bias > 0.55 else "upstream-salience equilibrium"
    return _outcome("G1", "Hospital-salience budget game", s, access, viability, equity, fiscal, hospital, gaming, label, "Hospital rescue bias falls only when upstream access becomes visible, funded and politically salient.")


def model_g2_hnz_allocation(s: Scenario) -> GameOutcome:
    upstream_attention = clip(100 * (0.18 + 0.28 * s.primary_kpi_salience + 0.20 * s.ambulance_kpi_salience + 0.22 * s.data_observability - 0.18 * s.hospital_political_penalty), 0, 100) / 100
    access = 20 + 50 * upstream_attention + 18 * s.marginal_contact_benefit
    viability = 30 + 35 * s.marginal_contact_benefit + 15 * s.direct_claiming - 20 * s.budget_tightness
    equity = 32 + 30 * s.equity_program_strength + 18 * upstream_attention
    fiscal = 75 - 20 * s.marginal_contact_benefit + 12 * s.data_observability + 10 * s.gaming_controls
    hospital = 80 - 38 * upstream_attention - 18 * s.marginal_contact_benefit - 10 * s.ambulance_alternative_funding
    gaming = 20 + 12 * (1 - s.data_observability) + 18 * s.primary_kpi_salience * (1 - s.gaming_controls)
    label = "hospital-operations dominance" if upstream_attention < 0.45 else "balanced internal accountability"
    return _outcome("G2", "Health NZ internal allocation game", s, access, viability, equity, fiscal, hospital, gaming, label, "Management attention shifts upstream when primary and ambulance outcomes have hospital-equivalent salience.")


def model_g3_capitation_supply(s: Scenario) -> GameOutcome:
    effective_margin = s.marginal_contact_benefit + 0.35 * s.copayment_level + 0.18 * s.capitation_weighting - 0.62 - 0.15 * s.pho_transaction_cost - 0.10 * s.budget_tightness
    supply_elasticity = sigmoid(6 * effective_margin)
    access = 18 + 74 * supply_elasticity
    viability = 25 + 70 * supply_elasticity - 8 * s.budget_tightness
    equity = 35 + 25 * s.capitation_weighting + 20 * s.copayment_protections + 15 * s.equity_program_strength - 18 * s.copayment_level * (1 - s.copayment_protections)
    fiscal = 85 - 25 * s.marginal_contact_benefit - 10 * supply_elasticity + 12 * s.gaming_controls
    hospital = 86 - 55 * supply_elasticity - 8 * s.ambulance_alternative_funding
    gaming = 10 + 25 * s.marginal_contact_benefit * (1 - s.gaming_controls)
    label = "marginal-rationing equilibrium" if supply_elasticity < 0.45 else "marginal-expansion equilibrium"
    return _outcome("G3", "Capitation marginal-supply game", s, access, viability, equity, fiscal, hospital, gaming, label, "Additional contacts expand only when combined public benefit and co-payment exceed marginal cost, admin cost and risk.")


def model_g4_consumer_pathway(s: Scenario) -> GameOutcome:
    effective_price = s.copayment_level * (1 - 0.75 * s.copayment_protections)
    availability = 0.35 * s.marginal_contact_benefit + 0.20 * s.scope_flexibility + 0.15 * s.telehealth_integration + 0.15 * s.local_inperson_loading + 0.15 * s.ambulance_alternative_funding
    early_access_share = sigmoid(3.2 * availability - 2.6 * effective_price - 0.6)
    access = 15 + 78 * early_access_share
    viability = 35 + 25 * availability + 18 * s.marginal_contact_benefit
    equity = 75 - 55 * effective_price + 15 * s.equity_program_strength
    fiscal = 65 - 15 * s.marginal_contact_benefit + 20 * effective_price + 10 * s.gaming_controls
    hospital = 88 - 52 * early_access_share + 12 * effective_price
    gaming = 12 + 12 * (1 - s.gaming_controls) + 10 * s.telehealth_scale * (1 - s.telehealth_integration)
    label = "delay/ED-substitution equilibrium" if early_access_share < 0.50 else "early-access equilibrium"
    return _outcome("G4", "Consumer access pathway game", s, access, viability, equity, fiscal, hospital, gaming, label, "Patients move to lower-cost access when price, wait, travel and trust costs are lower than delay or ED substitution.")


def model_g5_pho_intermediation(s: Scenario) -> GameOutcome:
    entry_barrier = 0.65 * s.pho_transaction_cost + 0.35 * (1 - s.direct_claiming)
    function_value = 0.60 * s.equity_program_strength + 0.25 * s.data_observability + 0.15 * s.stakeholder_alignment
    access = 35 + 28 * s.direct_claiming + 20 * s.marginal_contact_benefit - 35 * entry_barrier
    viability = 40 + 28 * s.direct_claiming + 15 * s.marginal_contact_benefit - 25 * entry_barrier
    equity = 30 + 55 * function_value - 18 * s.direct_claiming * max(0, 0.65 - s.equity_program_strength)
    fiscal = 70 + 12 * s.data_observability + 8 * s.gaming_controls - 12 * s.direct_claiming
    hospital = 75 - 30 * s.direct_claiming - 12 * function_value - 10 * s.marginal_contact_benefit + 22 * entry_barrier
    gaming = 18 + 20 * s.direct_claiming * (1 - s.gaming_controls) + 12 * (1 - s.data_observability)
    label = "intermediated-gatekeeping equilibrium" if entry_barrier > 0.45 else "optional/direct-claiming equilibrium"
    return _outcome("G5", "PHO intermediation game", s, access, viability, equity, fiscal, hospital, gaming, label, "Direct claiming improves entry only if PHO/locality equity and population-health functions are explicitly preserved.")


def model_g6_acc_cross_funder(s: Scenario) -> GameOutcome:
    viability_signal = 0.35 * s.marginal_contact_benefit + 0.30 * s.acc_activity_funding - 0.30 * s.acc_constraint + 0.15 * s.direct_claiming + 0.10 * s.capitation_weighting
    spillover_risk = 0.65 * s.acc_constraint + 0.25 * (1 - s.data_observability) + 0.10 * (1 - s.stakeholder_alignment)
    access = 25 + 55 * viability_signal - 15 * spillover_risk
    viability = 30 + 65 * viability_signal - 20 * spillover_risk
    equity = 40 + 20 * s.equity_program_strength + 15 * s.copayment_protections + 10 * s.data_observability
    fiscal = 70 + 15 * s.data_observability - 12 * s.marginal_contact_benefit - 15 * s.acc_activity_funding * (1 - s.acc_constraint)
    hospital = 78 - 38 * viability_signal + 25 * spillover_risk - 8 * s.ambulance_alternative_funding
    gaming = 14 + 10 * (1 - s.data_observability) + 12 * (1 - s.gaming_controls)
    label = "siloed-cost-shifting equilibrium" if spillover_risk > 0.30 else "whole-of-Crown flow equilibrium"
    return _outcome("G6", "ACC/Health NZ cross-funder game", s, access, viability, equity, fiscal, hospital, gaming, label, "ACC activity funding can stabilise lower-cost capacity; constraining it in isolation risks spillover to Health NZ and patients.")


def model_g7_ambulance_conveyance(s: Scenario) -> GameOutcome:
    alternative_resolution = s.ambulance_alternative_funding * (0.45 * s.safety_governance + 0.30 * s.ambulance_kpi_salience + 0.25 * s.data_observability)
    conveyance_default = 1 - alternative_resolution
    access = 28 + 48 * alternative_resolution + 14 * s.primary_kpi_salience
    viability = 35 + 30 * alternative_resolution + 12 * s.acc_activity_funding
    equity = 42 + 18 * alternative_resolution + 20 * s.equity_program_strength + 10 * s.local_inperson_loading
    fiscal = 68 + 10 * alternative_resolution + 10 * s.data_observability - 12 * s.ambulance_alternative_funding
    hospital = 85 - 55 * alternative_resolution + 10 * conveyance_default
    gaming = 10 + 35 * s.ambulance_alternative_funding * max(0, 0.75 - s.safety_governance) + 10 * (1 - s.data_observability)
    label = "ED-conveyance default" if alternative_resolution < 0.45 else "safe alternative-disposition equilibrium"
    return _outcome("G7", "Ambulance conveyance game", s, access, viability, equity, fiscal, hospital, gaming, label, "Alternative disposition is stable only when payment, clinical governance, data and follow-up reduce organisational risk.")


def model_g8_scope_supply(s: Scenario) -> GameOutcome:
    safe_scope = s.scope_flexibility * s.safety_governance
    bottleneck = 1 - safe_scope
    access = 22 + 42 * safe_scope + 24 * s.marginal_contact_benefit + 8 * s.direct_claiming
    viability = 32 + 35 * safe_scope + 22 * s.marginal_contact_benefit
    equity = 40 + 24 * safe_scope + 20 * s.equity_program_strength + 10 * s.copayment_protections
    fiscal = 70 - 15 * s.marginal_contact_benefit + 12 * s.gaming_controls + 8 * s.data_observability
    hospital = 82 - 42 * safe_scope - 18 * s.marginal_contact_benefit + 15 * bottleneck
    gaming = 8 + 50 * max(0, s.scope_flexibility - s.safety_governance) + 18 * (1 - s.gaming_controls)
    label = "professional-bottleneck equilibrium" if safe_scope < 0.45 else "scope-enabled supply equilibrium"
    return _outcome("G8", "Scope-of-practice supply game", s, access, viability, equity, fiscal, hospital, gaming, label, "Funding eligibility should follow safe scope and governance, not professional category alone.")


def model_g9_telehealth_local_supply(s: Scenario) -> GameOutcome:
    simple_access = 0.45 * s.telehealth_scale + 0.25 * s.marginal_contact_benefit + 0.20 * s.data_observability + 0.10 * s.scope_flexibility
    local_viability = 0.45 * s.local_inperson_loading + 0.25 * s.telehealth_integration + 0.20 * s.marginal_contact_benefit - 0.30 * s.telehealth_scale * (1 - s.telehealth_integration)
    fragmentation = s.telehealth_scale * (1 - s.telehealth_integration) * (1 - 0.5 * s.data_observability)
    access = 25 + 45 * simple_access + 25 * max(0, local_viability)
    viability = 30 + 55 * max(0, local_viability)
    equity = 42 + 20 * s.telehealth_integration + 20 * s.local_inperson_loading + 15 * s.equity_program_strength - 18 * fragmentation
    fiscal = 70 + 8 * s.telehealth_scale - 10 * s.local_inperson_loading + 10 * s.gaming_controls
    hospital = 80 - 24 * simple_access - 28 * max(0, local_viability) + 20 * fragmentation
    gaming = 12 + 35 * fragmentation + 12 * (1 - s.gaming_controls)
    label = "telehealth-substitution/fragmentation" if fragmentation > 0.30 or local_viability < 0.25 else "integrated hybrid-access equilibrium"
    return _outcome("G9", "Telehealth/local-supply game", s, access, viability, equity, fiscal, hospital, gaming, label, "Telehealth improves simple access but must be integrated and paired with local in-person capacity.")


def model_g10_copayment(s: Scenario) -> GameOutcome:
    effective_burden = s.copayment_level * (1 - 0.80 * s.copayment_protections)
    demand_discipline = min(1.0, s.copayment_level + 0.3 * s.gaming_controls)
    access = 72 - 52 * effective_burden + 22 * s.marginal_contact_benefit
    viability = 36 + 22 * s.copayment_level + 24 * s.marginal_contact_benefit
    equity = 82 - 70 * effective_burden + 20 * s.equity_program_strength
    fiscal = 48 + 35 * demand_discipline - 18 * s.marginal_contact_benefit
    hospital = 45 + 48 * effective_burden - 18 * s.marginal_contact_benefit
    gaming = 10 + 28 * s.marginal_contact_benefit * (1 - s.gaming_controls) + 12 * max(0, 0.45 - s.copayment_level)
    label = "price-rationing equity failure" if effective_burden > 0.35 else "calibrated co-payment equilibrium"
    return _outcome("G10", "Co-payment calibration game", s, access, viability, equity, fiscal, hospital, gaming, label, "Co-payment can moderate discretionary demand but becomes a delayed-care mechanism without protections.")


def model_g11_kpi_salience(s: Scenario) -> GameOutcome:
    kpi_strength = 0.55 * s.primary_kpi_salience + 0.35 * s.ambulance_kpi_salience + 0.10 * s.data_observability
    target_gaming = kpi_strength * (1 - s.gaming_controls) * (1 - 0.4 * s.data_observability)
    access = 24 + 44 * kpi_strength + 22 * s.marginal_contact_benefit
    viability = 34 + 22 * kpi_strength + 26 * s.marginal_contact_benefit
    equity = 42 + 22 * kpi_strength + 24 * s.equity_program_strength + 10 * s.copayment_protections
    fiscal = 68 + 12 * s.data_observability + 10 * s.gaming_controls - 12 * s.marginal_contact_benefit
    hospital = 84 - 42 * kpi_strength - 18 * s.marginal_contact_benefit + 15 * target_gaming
    gaming = 8 + 70 * target_gaming
    label = "hospital-target dominance" if kpi_strength < 0.45 else "upstream target salience with balancing measures"
    return _outcome("G11", "KPI salience game", s, access, viability, equity, fiscal, hospital, gaming, label, "Top-tier KPIs shift behaviour only if paired with funding levers, data and balancing measures.")


def model_g12_equity_trust(s: Scenario) -> GameOutcome:
    trust_function = 0.45 * s.equity_program_strength + 0.25 * s.stakeholder_alignment + 0.20 * s.copayment_protections + 0.10 * s.local_inperson_loading
    direct_risk = s.direct_claiming * max(0, 0.65 - trust_function)
    access = 28 + 34 * s.marginal_contact_benefit + 28 * trust_function - 15 * direct_risk
    viability = 34 + 20 * s.marginal_contact_benefit + 20 * s.scope_flexibility + 15 * trust_function
    equity = 25 + 70 * trust_function - 28 * direct_risk
    fiscal = 68 + 10 * s.data_observability + 8 * s.gaming_controls - 10 * s.marginal_contact_benefit
    hospital = 78 - 28 * trust_function - 24 * s.marginal_contact_benefit + 18 * direct_risk
    gaming = 12 + 25 * direct_risk + 12 * (1 - s.data_observability)
    label = "transactional-access without trust" if direct_risk > 0.20 else "benefits plus equity-function equilibrium"
    return _outcome("G12", "Equity and trust game", s, access, viability, equity, fiscal, hospital, gaming, label, "Demand-driven benefits need retained kaupapa Maori, Pacific, rural and locality functions to avoid transactional equity failure.")


def model_g13_political_economy(s: Scenario) -> GameOutcome:
    coalition_score = 0.40 * s.narrative_coherence + 0.30 * s.stakeholder_alignment + 0.15 * s.data_observability + 0.15 * s.equity_program_strength
    contestability = s.marginal_contact_benefit * (1 - s.narrative_coherence) + s.direct_claiming * (1 - s.stakeholder_alignment)
    access = 28 + 35 * coalition_score + 22 * s.marginal_contact_benefit
    viability = 35 + 25 * coalition_score + 22 * s.marginal_contact_benefit
    equity = 40 + 25 * coalition_score + 20 * s.equity_program_strength + 10 * s.copayment_protections
    fiscal = 65 + 12 * s.data_observability + 12 * s.gaming_controls - 10 * contestability
    hospital = 78 - 30 * coalition_score - 16 * s.marginal_contact_benefit + 18 * contestability
    gaming = 16 + 45 * contestability * (1 - s.gaming_controls)
    label = "institutional-defence equilibrium" if coalition_score < 0.50 else "access-architecture coalition"
    return _outcome("G13", "Political economy game", s, access, viability, equity, fiscal, hospital, gaming, label, "Reform becomes feasible when framed as patient access and hospital avoidance rather than sector income or anti-PHO politics.")


def model_g14_data_observability(s: Scenario) -> GameOutcome:
    observability = s.data_observability
    budget_shift = observability * (0.45 * s.primary_kpi_salience + 0.30 * s.ambulance_kpi_salience + 0.25 * s.narrative_coherence)
    hidden_need = 1 - observability
    access = 24 + 38 * budget_shift + 20 * s.marginal_contact_benefit + 12 * s.direct_claiming
    viability = 34 + 28 * budget_shift + 24 * s.marginal_contact_benefit
    equity = 38 + 26 * observability + 24 * s.equity_program_strength + 10 * s.copayment_protections
    fiscal = 58 + 25 * observability + 12 * s.gaming_controls - 10 * s.marginal_contact_benefit
    hospital = 82 - 34 * budget_shift - 20 * observability - 12 * s.marginal_contact_benefit + 18 * hidden_need
    gaming = 10 + 30 * (1 - observability) + 20 * (1 - s.gaming_controls)
    label = "hidden-unmet-need equilibrium" if observability < 0.55 else "observable upstream-flow equilibrium"
    return _outcome("G14", "Data observability game", s, access, viability, equity, fiscal, hospital, gaming, label, "Upstream access failure becomes fundable only when data links it to ambulance, ED and avoidable admission outcomes.")


GAME_MODELS: Mapping[str, Callable[[Scenario], GameOutcome]] = {
    "G1": model_g1_hospital_salience,
    "G2": model_g2_hnz_allocation,
    "G3": model_g3_capitation_supply,
    "G4": model_g4_consumer_pathway,
    "G5": model_g5_pho_intermediation,
    "G6": model_g6_acc_cross_funder,
    "G7": model_g7_ambulance_conveyance,
    "G8": model_g8_scope_supply,
    "G9": model_g9_telehealth_local_supply,
    "G10": model_g10_copayment,
    "G11": model_g11_kpi_salience,
    "G12": model_g12_equity_trust,
    "G13": model_g13_political_economy,
    "G14": model_g14_data_observability,
}


def run_all(scenarios: Iterable[Scenario] = SCENARIOS) -> tuple[GameOutcome, ...]:
    """Run all demonstrative game models across all scenarios."""

    outcomes: list[GameOutcome] = []
    for scenario in scenarios:
        for model in GAME_MODELS.values():
            outcomes.append(model(scenario))
    return tuple(outcomes)


def summarise_by_scenario(outcomes: Iterable[GameOutcome]) -> dict[str, dict[str, float]]:
    """Return mean scores by scenario."""

    rows = list(outcomes)
    summary: dict[str, dict[str, float]] = {}
    for scenario_id in sorted({row.scenario_id for row in rows}):
        subset = [row for row in rows if row.scenario_id == scenario_id]
        summary[scenario_id] = {
            "mean_access_score": sum(row.access_score for row in subset) / len(subset),
            "mean_provider_viability": sum(row.provider_viability for row in subset) / len(subset),
            "mean_equity_score": sum(row.equity_score for row in subset) / len(subset),
            "mean_fiscal_control": sum(row.fiscal_control for row in subset) / len(subset),
            "mean_hospital_pressure": sum(row.hospital_pressure for row in subset) / len(subset),
            "mean_gaming_risk": sum(row.gaming_risk for row in subset) / len(subset),
            "mean_system_welfare": sum(row.system_welfare for row in subset) / len(subset),
        }
    return summary


def scenarios_as_rows() -> list[dict[str, object]]:
    """Return scenario inputs as rows."""

    rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        row = asdict(scenario)
        rows.append(row)
    return rows
