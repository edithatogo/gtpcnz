"""NZ-specific game-theoretic scaffold for primary care funding architecture."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FundingArchitecture(str, Enum):
    """High-level NZ policy architecture choices."""

    STATUS_QUO_TIGHT_CONTROL = "status_quo_tight_control"
    REWEIGHTED_CAPITATION = "reweighted_capitation"
    PRIMARY_CARE_BENEFITS_SCHEDULE = "primary_care_benefits_schedule"


class ProviderResponse(str, Enum):
    """Stylised provider best responses."""

    RATION = "ration"
    MAINTAIN = "maintain"
    EXPAND_MULTIDISCIPLINARY = "expand_multidisciplinary"


@dataclass(frozen=True)
class ContactBenefit:
    """Contact-type benefit parameters."""

    public_benefit: float
    copayment: float
    marginal_cost: float
    admin_cost: float
    risk_cost: float
    scope_eligible: bool = True
    professional_value: float = 0.0

    @property
    def net_margin(self) -> float:
        """Return net margin from delivering the contact."""

        if not self.scope_eligible:
            return float("-inf")
        return (
            self.public_benefit
            + self.copayment
            + self.professional_value
            - self.marginal_cost
            - self.admin_cost
            - self.risk_cost
        )

    def is_supply_incentivised(self) -> bool:
        """Return whether the contact is financially and legally viable."""

        return self.net_margin > 0


@dataclass(frozen=True)
class AccessState:
    """State variables for lower-cost access and hospital pressure."""

    demand: float
    primary_capacity: float
    ambulance_resolved: float
    ambulance_conveyance: float
    hospital_pressure: float


def unmet_need(demand: float, primary_capacity: float, ambulance_resolved: float) -> float:
    """Compute unmet/delayed lower-cost need."""

    return max(0.0, demand - primary_capacity - ambulance_resolved)


def hospital_pressure_next(
    state: AccessState,
    persistence: float = 0.75,
    unmet_to_hospital: float = 0.3,
    conveyance_to_hospital: float = 0.2,
    avoidance: float = 0.0,
) -> float:
    """Return next-period hospital pressure."""

    u = unmet_need(state.demand, state.primary_capacity, state.ambulance_resolved)
    return max(
        0.0,
        persistence * state.hospital_pressure
        + unmet_to_hospital * u
        + conveyance_to_hospital * state.ambulance_conveyance
        - avoidance,
    )


def likely_provider_response(architecture: FundingArchitecture, marginal_contact: ContactBenefit) -> ProviderResponse:
    """Return a stylised provider response to architecture and marginal margin."""

    if architecture == FundingArchitecture.PRIMARY_CARE_BENEFITS_SCHEDULE:
        if marginal_contact.is_supply_incentivised():
            return ProviderResponse.EXPAND_MULTIDISCIPLINARY
        return ProviderResponse.MAINTAIN

    if architecture == FundingArchitecture.REWEIGHTED_CAPITATION:
        if marginal_contact.net_margin > 0:
            return ProviderResponse.MAINTAIN
        return ProviderResponse.RATION

    if marginal_contact.net_margin >= 2:
        return ProviderResponse.MAINTAIN
    return ProviderResponse.RATION


@dataclass(frozen=True)
class GameScore:
    """Qualitative welfare score for architecture comparison."""

    patient_access: float
    provider_viability: float
    hospital_avoidance: float
    fiscal_control: float
    equity: float
    gaming_risk: float

    @property
    def total(self) -> float:
        """Return a simple equally weighted score with gaming risk as penalty."""

        return (
            self.patient_access
            + self.provider_viability
            + self.hospital_avoidance
            + self.fiscal_control
            + self.equity
            - self.gaming_risk
        )


def score_architecture(architecture: FundingArchitecture) -> GameScore:
    """Return stylised qualitative scores for the mapped policy architectures."""

    if architecture == FundingArchitecture.STATUS_QUO_TIGHT_CONTROL:
        return GameScore(1.0, 1.5, 0.5, 4.0, 1.5, 0.5)
    if architecture == FundingArchitecture.REWEIGHTED_CAPITATION:
        return GameScore(2.0, 2.0, 1.5, 3.5, 3.0, 0.75)
    if architecture == FundingArchitecture.PRIMARY_CARE_BENEFITS_SCHEDULE:
        return GameScore(4.0, 3.5, 4.0, 2.5, 3.5, 1.5)
    raise ValueError(f"Unknown architecture: {architecture}")
