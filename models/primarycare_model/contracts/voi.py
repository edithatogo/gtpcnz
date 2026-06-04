"""Contracts for transparent value-of-information outputs."""

from __future__ import annotations

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract


class VoiResult(StrictContract):
    analysis_id: str = Field(min_length=1)
    seed: int
    evpi: float
    evppi: dict[str, float]
    evsi: dict[str, float]
    enbs: dict[str, float]
    decision_error_probability: float = Field(ge=0.0, le=1.0)
    evidence_priority_ranking: tuple[str, ...]
    label: str = "decision-uncertainty analysis, not a forecast"
