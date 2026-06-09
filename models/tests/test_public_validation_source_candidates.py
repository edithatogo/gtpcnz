from __future__ import annotations

import subprocess
import sys

from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_snapshot import load_public_sources
from models.primarycare_model.data.public_validation_sources import (
    load_public_validation_source_candidates,
    verify_public_validation_source_candidates,
)


def test_validation_source_candidate_contract_passes() -> None:
    assert verify_public_validation_source_candidates() == ()


def test_validation_source_candidates_are_not_runtime_public_sources() -> None:
    runtime_sources = {source.source_id for source in load_public_sources()}
    runtime_plans = {plan.source_id for plan in load_public_source_retrieval_plans()}
    candidates = load_public_validation_source_candidates()

    assert {candidate.current_runtime_use for candidate in candidates} == {"not_loaded_public_runtime"}
    assert all(candidate.source_id not in runtime_sources for candidate in candidates)
    assert all(candidate.source_id not in runtime_plans for candidate in candidates)


def test_track_073_registers_and_rejects_validation_candidates() -> None:
    candidates = {candidate.candidate_id: candidate for candidate in load_public_validation_source_candidates()}

    registered = candidates["val_moh_planning_performance_historical"]
    assert registered.candidate_status == "registered_retrieval_plan"
    assert registered.independence_assessment == "independent_of_current_calibration_targets"
    assert registered.expected_raw_dir == f"data/public_raw/{registered.source_id}"
    assert registered.expected_processed_artifact is not None
    assert registered.expected_processed_artifact.startswith(f"data/public_processed/{registered.source_id}/")
    assert set(registered.cal_gates) == {"CAL-G-003", "CAL-G-004", "CAL-G-005"}

    rejected = candidates["val_nzhs_regional_release_independence_rejected"]
    assert rejected.candidate_status == "rejected_for_independence"
    assert rejected.rejection_reason is not None
    assert "already used as a calibration target source" in rejected.rejection_reason


def test_validation_source_candidate_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_validation_source_candidates.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "public validation source candidate contract passed" in result.stdout
