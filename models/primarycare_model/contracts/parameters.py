"""Strict parameter contracts used by registries and runtime adapters."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SensitivityClass = Literal["public", "public_aggregate", "template", "sensitive", "confidential"]
EvidenceTier = Literal["assumption", "public_data", "stakeholder", "linked_data", "calibrated"]
ParameterValueType = Literal["integer", "number", "boolean", "categorical"]


class StrictContract(BaseModel):
    """Base class for immutable, no-extra-fields Pydantic contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class ParameterDefinition(StrictContract):
    """Authoritative definition for a tunable model parameter."""

    parameter_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value_type: ParameterValueType
    unit: str = Field(min_length=1)
    default_value: int | float | bool | str
    lower_bound: float | None = None
    upper_bound: float | None = None
    category_values: tuple[str, ...] = ()
    description: str = Field(min_length=1)
    source: str = Field(min_length=1)
    sensitivity_class: SensitivityClass = "public_aggregate"
    evidence_tier: EvidenceTier = "assumption"
    tags: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _validate_default(self) -> ParameterDefinition:
        if self.lower_bound is not None and self.upper_bound is not None and self.lower_bound > self.upper_bound:
            raise ValueError("lower_bound cannot exceed upper_bound")
        if self.value_type == "integer" and type(self.default_value) is not int:
            raise ValueError("integer parameters require an integer default")
        if self.value_type == "number" and (
            not isinstance(self.default_value, (int, float)) or isinstance(self.default_value, bool)
        ):
            raise ValueError("number parameters require a numeric default")
        if self.value_type == "boolean" and not isinstance(self.default_value, bool):
            raise ValueError("boolean parameters require a boolean default")
        if self.value_type == "categorical":
            if not isinstance(self.default_value, str):
                raise ValueError("categorical parameters require a string default")
            if not self.category_values or self.default_value not in self.category_values:
                raise ValueError("categorical default must be in category_values")
        if isinstance(self.default_value, (int, float)) and not isinstance(self.default_value, bool):
            value = float(self.default_value)
            if self.lower_bound is not None and value < self.lower_bound:
                raise ValueError("default_value is below lower_bound")
            if self.upper_bound is not None and value > self.upper_bound:
                raise ValueError("default_value is above upper_bound")
        return self


class ParameterValue(StrictContract):
    """A concrete validated value for a registered parameter."""

    parameter_id: str = Field(min_length=1)
    value: int | float | bool | str
    source: str = Field(min_length=1)

    def validate_against(self, definition: ParameterDefinition) -> ParameterValue:
        if self.parameter_id != definition.parameter_id:
            raise ValueError("parameter_id does not match definition")
        if definition.value_type == "integer" and type(self.value) is not int:
            raise ValueError(f"{self.parameter_id} requires an integer value")
        if definition.value_type == "number" and (
            not isinstance(self.value, (int, float)) or isinstance(self.value, bool)
        ):
            raise ValueError(f"{self.parameter_id} requires a numeric value")
        if definition.value_type == "boolean" and not isinstance(self.value, bool):
            raise ValueError(f"{self.parameter_id} requires a boolean value")
        if definition.value_type == "categorical" and self.value not in definition.category_values:
            raise ValueError(f"{self.parameter_id} must be one of {definition.category_values}")
        if isinstance(self.value, (int, float)) and not isinstance(self.value, bool):
            numeric = float(self.value)
            if definition.lower_bound is not None and numeric < definition.lower_bound:
                raise ValueError(f"{self.parameter_id} is below lower_bound")
            if definition.upper_bound is not None and numeric > definition.upper_bound:
                raise ValueError(f"{self.parameter_id} is above upper_bound")
        return self


class ParameterVector(StrictContract):
    """A named bundle of parameter values validated against a registry."""

    vector_id: str = Field(min_length=1)
    values: tuple[ParameterValue, ...]
    claim_boundary: str = Field(min_length=1)

    def as_dict(self) -> dict[str, Any]:
        return {item.parameter_id: item.value for item in self.values}
