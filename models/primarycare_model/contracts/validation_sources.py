"""Contracts for independent public validation-source candidates."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from models.primarycare_model.contracts.parameters import StrictContract
from models.primarycare_model.contracts.public_sources import LicenceStatus, PublicAccessStatus

CandidateStatus = Literal[
    "registered_retrieval_plan",
    "candidate_pending_locator",
    "rejected_for_independence",
    "rejected_for_access",
    "rejected_for_grain",
]

IndependenceAssessment = Literal[
    "independent_of_current_calibration_targets",
    "not_independent_of_current_calibration_targets",
    "independence_pending_review",
]

RuntimeUse = Literal["not_loaded_public_runtime", "eligible_after_release_gate"]


class PublicValidationSourceCandidate(StrictContract):
    candidate_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    url_or_reference: str = Field(min_length=1)
    public_access_status: PublicAccessStatus
    licence_status: LicenceStatus
    candidate_status: CandidateStatus
    retrieval_path: str = Field(min_length=1)
    expected_grain: str = Field(min_length=1)
    claim_family: str = Field(min_length=1)
    cal_gates: tuple[str, ...]
    independence_assessment: IndependenceAssessment
    current_runtime_use: RuntimeUse = "not_loaded_public_runtime"
    expected_raw_dir: str | None = None
    expected_raw_artifact: str | None = None
    fetch_script: str | None = None
    transform_script: str | None = None
    expected_processed_artifact: str | None = None
    rejection_reason: str | None = None
    not_valid_for: tuple[str, ...]
    claim_boundary: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_candidate_status(self) -> PublicValidationSourceCandidate:
        if not self.cal_gates:
            raise ValueError("cal_gates must not be empty")
        if self.candidate_status == "registered_retrieval_plan":
            required = {
                "expected_raw_dir": self.expected_raw_dir,
                "expected_raw_artifact": self.expected_raw_artifact,
                "fetch_script": self.fetch_script,
                "transform_script": self.transform_script,
                "expected_processed_artifact": self.expected_processed_artifact,
            }
            missing = [name for name, value in required.items() if not value]
            if missing:
                raise ValueError(f"registered retrieval candidates require {', '.join(missing)}")
            if self.rejection_reason is not None:
                raise ValueError("registered retrieval candidates must not have rejection_reason")
        if self.candidate_status.startswith("rejected_") and not self.rejection_reason:
            raise ValueError("rejected candidates require rejection_reason")
        return self
