"""Public parameter ontology for the public-only model path."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from models.primarycare_model.contracts.parameters import ParameterDefinition, StrictContract

DistributionType = Literal["fixed", "normal", "triangular", "beta", "uniform"]
EvidenceQuality = Literal["low", "medium", "high"]
SensitivityPriority = Literal["low", "medium", "high"]
CalibrationRole = Literal["baseline", "denominator", "scaling", "calibration_target", "validation_target", "scenario_modifier"]
ClaimBoundary = Literal["public_benchmark", "calibration_readiness", "empirically_supported_if_gated"]


class DistributionSpec(StrictContract):
    distribution_type: DistributionType
    distribution_parameters: dict[str, float] = Field(default_factory=dict)


class PublicParameterDefinition(ParameterDefinition):
    source_id: str = Field(min_length=1)
    distribution_type: DistributionType
    distribution_parameters: dict[str, float]
    bounds: dict[str, float]
    evidence_quality: EvidenceQuality
    transferability_score: float = Field(ge=0.0, le=1.0)
    sensitivity_priority: SensitivityPriority
    calibration_role: CalibrationRole
    update_cadence: str = Field(min_length=1)
    claim_boundary: str = Field(min_length=1)
    formula_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _public_only(self) -> "PublicParameterDefinition":
        if self.sensitivity_class not in {"public", "public_aggregate"}:
            raise ValueError("public parameter cannot be sensitive or confidential")
        if self.evidence_tier not in {"public_data", "assumption"}:
            raise ValueError("public parameter evidence tier must be public_data or assumption")
        if "lower" not in self.bounds or "upper" not in self.bounds:
            raise ValueError("public parameter bounds require lower and upper")
        return self
