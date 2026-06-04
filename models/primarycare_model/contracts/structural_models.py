"""Contracts for public structural uncertainty models."""

from __future__ import annotations

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract


class StructuralModel(StrictContract):
    structural_model_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    dag: str = Field(min_length=1)
    active_edges: tuple[str, ...]
    excluded_edges: tuple[str, ...]
    plausibility_weight: float = Field(ge=0.0, le=1.0)
    source_basis: tuple[str, ...]
    claim_boundary: str = Field(min_length=1)
