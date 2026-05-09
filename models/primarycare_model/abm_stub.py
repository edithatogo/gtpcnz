"""Agent-based model placeholder classes."""

from dataclasses import dataclass


@dataclass
class PatientAgent:
    deprivation: int
    rural: bool
    multimorbidity: int
    price_sensitivity: float


@dataclass
class ProviderAgent:
    provider_type: str
    capacity: int
    benefit_eligible: bool
    scope: tuple[str, ...]

    def can_deliver(self, contact_type: str) -> bool:
        """Return whether the provider can deliver a contact type within modelled scope."""
        return self.benefit_eligible and contact_type in self.scope
