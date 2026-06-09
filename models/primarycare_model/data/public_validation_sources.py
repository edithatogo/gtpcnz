"""Load and verify independent public validation-source candidates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.validation_sources import PublicValidationSourceCandidate
from models.primarycare_model.data.public_source_snapshot import PUBLIC_REGISTRY

VALIDATION_CANDIDATE_PATH = PUBLIC_REGISTRY / "validation_source_candidates.public.v1.yaml"
FORBIDDEN_BOUNDARY_TERMS = (
    "private administrative data",
    "patient-level",
    "confidential oia",
    "stakeholder analysis",
    "unpublished expert elicitation",
)
EXCLUDED_CLAIMS = {
    "precise fiscal savings",
    "ed reductions",
    "hospital-demand reductions",
    "workforce effects",
    "implementation impacts",
    "causal effects",
}


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def load_public_validation_source_candidates() -> tuple[PublicValidationSourceCandidate, ...]:
    payload = yaml.safe_load(VALIDATION_CANDIDATE_PATH.read_text(encoding="utf-8"))
    return TypeAdapter(tuple[PublicValidationSourceCandidate, ...]).validate_python(
        _lists_to_tuples(payload["validation_source_candidates"])
    )


def _is_repo_relative(path: str) -> bool:
    candidate = Path(path)
    return not candidate.is_absolute() and ".." not in candidate.parts


def verify_public_validation_source_candidates() -> tuple[str, ...]:
    issues: list[str] = []
    candidates = load_public_validation_source_candidates()

    candidate_ids = [candidate.candidate_id for candidate in candidates]
    duplicate_candidate_ids = sorted({candidate_id for candidate_id in candidate_ids if candidate_ids.count(candidate_id) > 1})
    issues.extend(f"{candidate_id}: duplicate candidate_id" for candidate_id in duplicate_candidate_ids)

    registered = [candidate for candidate in candidates if candidate.candidate_status == "registered_retrieval_plan"]
    rejected = [candidate for candidate in candidates if candidate.candidate_status.startswith("rejected_")]
    if not registered and not rejected:
        issues.append("at least one validation source must be registered or explicitly rejected")

    for candidate in candidates:
        if candidate.public_access_status not in {"public", "published", "open"}:
            issues.append(f"{candidate.candidate_id}: public_access_status is not public/published/open")
        if candidate.licence_status not in {"open", "public_reference", "open_or_public_reference"}:
            issues.append(f"{candidate.candidate_id}: licence_status is not public/open")
        if candidate.current_runtime_use != "not_loaded_public_runtime":
            issues.append(f"{candidate.candidate_id}: candidates must not be loaded by the public runtime")
        if any(term in candidate.claim_boundary.lower() for term in FORBIDDEN_BOUNDARY_TERMS):
            issues.append(f"{candidate.candidate_id}: claim_boundary contains a forbidden input type")
        missing_exclusions = sorted(EXCLUDED_CLAIMS - {item.lower() for item in candidate.not_valid_for})
        if missing_exclusions:
            issues.append(f"{candidate.candidate_id}: not_valid_for is missing {', '.join(missing_exclusions)}")
        if candidate.candidate_status == "registered_retrieval_plan":
            assert candidate.expected_raw_dir is not None
            assert candidate.expected_raw_artifact is not None
            assert candidate.fetch_script is not None
            assert candidate.transform_script is not None
            assert candidate.expected_processed_artifact is not None
            expected_raw_dir = f"data/public_raw/{candidate.source_id}"
            expected_processed_prefix = f"data/public_processed/{candidate.source_id}/"
            if candidate.expected_raw_dir != expected_raw_dir:
                issues.append(f"{candidate.candidate_id}: expected_raw_dir must be {expected_raw_dir}")
            if not candidate.expected_processed_artifact.startswith(expected_processed_prefix):
                issues.append(
                    f"{candidate.candidate_id}: expected_processed_artifact must be under {expected_processed_prefix}"
                )
            for field_name in ("expected_raw_dir", "fetch_script", "transform_script", "expected_processed_artifact"):
                value = getattr(candidate, field_name)
                if value is not None and not _is_repo_relative(value):
                    issues.append(f"{candidate.candidate_id}: {field_name} must be repository-relative")
            if not candidate.fetch_script.startswith("scripts/fetch_"):
                issues.append(f"{candidate.candidate_id}: fetch_script must be an explicit fetch script")
            if not candidate.transform_script.startswith("scripts/transform_"):
                issues.append(f"{candidate.candidate_id}: transform_script must be an explicit transform script")
            if candidate.independence_assessment != "independent_of_current_calibration_targets":
                issues.append(f"{candidate.candidate_id}: registered retrieval candidate must be independently assessed")
    return tuple(issues)
