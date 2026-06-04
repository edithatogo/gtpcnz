"""Contracts for review-only public evidence candidates."""

from __future__ import annotations

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract


class EvidenceCandidate(StrictContract):
    candidate_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    relevance: float = Field(ge=0.0, le=1.0)
    quality: str = Field(min_length=1)
    transferability: float = Field(ge=0.0, le=1.0)
    contradiction_signal: str = Field(min_length=1)
    affected_parameters: tuple[str, ...]
    review_required: bool = True
    may_update_model: bool = False
