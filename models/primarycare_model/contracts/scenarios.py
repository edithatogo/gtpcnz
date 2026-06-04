"""Scenario and UI-control contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from models.primarycare_model.contracts.parameters import StrictContract

ScenarioKind = Literal["reference", "educational", "stochastic_demo"]


class RuntimeScenarioDefinition(StrictContract):
    """Runtime scenario inputs consumed by the public calculation lab."""

    scenario_id: str = Field(min_length=1)
    scenario_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    scenario_kind: ScenarioKind = "reference"
    activity_signal: float = Field(ge=0, le=100)
    capitation: float = Field(ge=0, le=100)
    place_accountability: float = Field(ge=0, le=100)
    scope_capacity: float = Field(ge=0, le=100)
    urgent_ambulance: float = Field(ge=0, le=100)
    data_visibility: float = Field(ge=0, le=100)
    governance: float = Field(ge=0, le=100)
    equity_protection: float = Field(ge=0, le=100)
    copayment_burden: float = Field(ge=0, le=100)
    budget_tightness: float = Field(ge=0, le=100)
    hospital_salience: float = Field(ge=0, le=100)
    complexity: float = Field(ge=0, le=100)
    source: str = Field(min_length=1)
    claim_boundary: str = Field(min_length=1)


class EducationalLeverDefinition(StrictContract):
    """Registry-backed definition for an educational Streamlit lever."""

    field_name: str = Field(min_length=1)
    public_label: str = Field(min_length=1)
    health_economics_meaning: str = Field(min_length=1)
    high_value_meaning: str = Field(min_length=1)
    educational_output_effect: str = Field(min_length=1)
    slider_help: str = Field(min_length=1)
    default_value: int = Field(ge=0, le=100)
    lower_bound: int = Field(default=0, ge=0, le=100)
    upper_bound: int = Field(default=100, ge=0, le=100)
    step: int = Field(default=1, ge=1, le=100)
    source: str = Field(min_length=1)
    claim_boundary: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_bounds(self) -> EducationalLeverDefinition:
        if self.lower_bound > self.upper_bound:
            raise ValueError("lower_bound cannot exceed upper_bound")
        if not self.lower_bound <= self.default_value <= self.upper_bound:
            raise ValueError("default_value must sit within slider bounds")
        return self


ToyLeverDefinition = EducationalLeverDefinition


class ScenarioOverride(StrictContract):
    """A named override against known parameter or scenario fields."""

    target_id: str = Field(min_length=1)
    field_name: str = Field(min_length=1)
    value: int | float | bool | str
    reason: str = Field(min_length=1)
