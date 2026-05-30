"""Game-theoretic scaffolding for primary care funding architecture.

The model is intentionally simple. It makes the policy logic testable before
calibration with empirical data.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Tuple


class FunderStrategy(str, Enum):
    """Funder strategies in the simplified upstream/hospital game."""

    TIGHT_UPSTREAM_CONTROL = "tight_upstream_control"
    REWEIGHT_CAPITATION_ONLY = "reweight_capitation_only"
    CONTACT_BENEFITS = "contact_benefits"


class ProviderStrategy(str, Enum):
    """Provider strategies in response to funding architecture."""

    RATION_SUPPLY = "ration_supply"
    MAINTAIN_SUPPLY = "maintain_supply"
    EXPAND_SUPPLY = "expand_supply"


@dataclass(frozen=True)
class Payoff:
    """Simple payoff tuple for funder, provider and consumers."""

    funder: float
    provider: float
    consumer: float
    hospital_pressure: float


DEFAULT_PAYOFFS: Dict[Tuple[FunderStrategy, ProviderStrategy], Payoff] = {
    (FunderStrategy.TIGHT_UPSTREAM_CONTROL, ProviderStrategy.RATION_SUPPLY): Payoff(-6.0, -3.0, -6.0, 8.0),
    (FunderStrategy.TIGHT_UPSTREAM_CONTROL, ProviderStrategy.MAINTAIN_SUPPLY): Payoff(-7.0, -5.0, -4.0, 7.0),
    (FunderStrategy.TIGHT_UPSTREAM_CONTROL, ProviderStrategy.EXPAND_SUPPLY): Payoff(-4.0, -8.0, 1.0, 4.0),
    (FunderStrategy.REWEIGHT_CAPITATION_ONLY, ProviderStrategy.RATION_SUPPLY): Payoff(-5.0, -2.0, -5.0, 7.0),
    (FunderStrategy.REWEIGHT_CAPITATION_ONLY, ProviderStrategy.MAINTAIN_SUPPLY): Payoff(-5.0, -1.0, -3.0, 6.0),
    (FunderStrategy.REWEIGHT_CAPITATION_ONLY, ProviderStrategy.EXPAND_SUPPLY): Payoff(-3.0, -4.0, 1.5, 4.0),
    (FunderStrategy.CONTACT_BENEFITS, ProviderStrategy.RATION_SUPPLY): Payoff(-5.0, 0.0, -2.0, 6.0),
    (FunderStrategy.CONTACT_BENEFITS, ProviderStrategy.MAINTAIN_SUPPLY): Payoff(-2.0, 1.0, 2.0, 4.0),
    (FunderStrategy.CONTACT_BENEFITS, ProviderStrategy.EXPAND_SUPPLY): Payoff(2.0, 3.0, 4.0, 2.0),
}


@dataclass(frozen=True)
class PolicyParameters:
    """Parameters for a transparent payoff calculator."""

    upstream_public_cost: float
    hospital_cost: float
    hospital_pressure: float
    hospital_political_penalty: float
    copayment_burden: float
    copayment_penalty: float
    equity_gap: float
    equity_penalty: float
    safety_failure: float
    safety_penalty: float
    avoidance_benefit: float
    provider_revenue: float
    provider_marginal_cost: float
    provider_admin_cost: float
    provider_burnout_cost: float
    consumer_health_benefit: float
    consumer_waiting_cost: float
    consumer_travel_cost: float
    consumer_fragmentation_cost: float


def calculate_payoff(params: PolicyParameters) -> Payoff:
    """Calculate a simplified payoff tuple from scenario parameters."""

    funder = (
        -params.upstream_public_cost
        -params.hospital_cost
        -params.hospital_political_penalty * params.hospital_pressure
        -params.copayment_penalty * params.copayment_burden
        -params.equity_penalty * params.equity_gap
        -params.safety_penalty * params.safety_failure
        + params.avoidance_benefit
    )
    provider = (
        params.provider_revenue
        - params.provider_marginal_cost
        - params.provider_admin_cost
        - params.provider_burnout_cost
    )
    consumer = (
        params.consumer_health_benefit
        - params.copayment_burden
        - params.consumer_waiting_cost
        - params.consumer_travel_cost
        - params.consumer_fragmentation_cost
        - params.safety_failure
    )
    return Payoff(funder=funder, provider=provider, consumer=consumer, hospital_pressure=params.hospital_pressure)


def evaluate_outcome(
    funder_strategy: FunderStrategy,
    provider_strategy: ProviderStrategy,
    payoffs: Dict[Tuple[FunderStrategy, ProviderStrategy], Payoff] = DEFAULT_PAYOFFS,
) -> Payoff:
    """Return payoff for a strategy pair."""

    return payoffs[(funder_strategy, provider_strategy)]


def best_provider_response(
    funder_strategy: FunderStrategy,
    payoffs: Dict[Tuple[FunderStrategy, ProviderStrategy], Payoff] = DEFAULT_PAYOFFS,
) -> ProviderStrategy:
    """Return the provider strategy with highest provider payoff."""

    candidates = {strategy: payoffs[(funder_strategy, strategy)].provider for strategy in ProviderStrategy}
    return max(candidates, key=candidates.get)


def provider_best_response_table(
    payoffs: Dict[Tuple[FunderStrategy, ProviderStrategy], Payoff] = DEFAULT_PAYOFFS,
) -> Dict[FunderStrategy, ProviderStrategy]:
    """Return provider best responses to each funder strategy."""

    return {strategy: best_provider_response(strategy, payoffs) for strategy in FunderStrategy}


def repeated_hospital_pressure(
    strategy_path: Iterable[Tuple[FunderStrategy, ProviderStrategy]],
    initial_pressure: float = 5.0,
    persistence: float = 0.75,
    payoffs: Dict[Tuple[FunderStrategy, ProviderStrategy], Payoff] = DEFAULT_PAYOFFS,
) -> List[float]:
    """Simulate repeated-game hospital-pressure trajectory."""

    pressures: List[float] = []
    pressure = initial_pressure
    for funder_strategy, provider_strategy in strategy_path:
        target = evaluate_outcome(funder_strategy, provider_strategy, payoffs).hospital_pressure
        pressure = persistence * pressure + (1 - persistence) * target
        pressures.append(pressure)
    return pressures
