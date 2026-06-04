"""Contracts for public aggregate calibration targets."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract

TargetFamily = Literal[
    "population_denominators", "primary_care_access", "unmet_need_cost_barriers",
    "workforce_supply", "hospital_ed_pressure", "avoidable_admissions",
    "equity_gradients", "rurality_gradients", "fiscal_aggregates"
]


class CalibrationTarget(StrictContract):
    target_id: str = Field(min_length=1)
    target_family: TargetFamily
    label: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    observed_value: float
    unit: str = Field(min_length=1)
    tolerance: float = Field(ge=0.0)
    public_access_status: str = Field(min_length=1)
    claim_boundary: str = Field(min_length=1)
