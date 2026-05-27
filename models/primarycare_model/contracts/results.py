"""Result contracts for public model outputs."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract

CalculationMode = Literal["precomputed", "live_deterministic", "seeded_stochastic", "educational"]


class ResultManifest(StrictContract):
    result_id: str = Field(min_length=1)
    calculation_mode: CalculationMode
    scenario_id: str = Field(min_length=1)
    seed: int | None = None
    draws: int | None = None
    claim_boundary: str = Field(min_length=1)
    validation_status: str = Field(min_length=1)


class ScenarioResult(StrictContract):
    scenario_id: str = Field(min_length=1)
    hybrid_viability_score: float = Field(ge=0, le=100)
    access_score: float = Field(ge=0, le=100)
    supply_generation_score: float = Field(ge=0, le=100)
    hospital_pressure_score: float = Field(ge=0, le=100)
    gaming_risk_score: float = Field(ge=0, le=100)
    calculation_status: str = Field(min_length=1)
