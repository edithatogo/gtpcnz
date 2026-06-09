from __future__ import annotations

import subprocess
import sys

from models.primarycare_model.data.public_source_retrieval import (
    load_public_source_retrieval_plans,
    verify_public_source_retrieval_plan,
)
from models.primarycare_model.data.public_source_snapshot import load_public_sources


def test_public_source_retrieval_plan_covers_every_public_source() -> None:
    sources = {source.source_id for source in load_public_sources()}
    plans = {plan.source_id for plan in load_public_source_retrieval_plans()}

    assert plans == sources


def test_public_source_retrieval_plan_tracks_processed_public_sources() -> None:
    plans = load_public_source_retrieval_plans()
    statuses = {plan.source_id: plan.retrieval_status for plan in plans}

    assert statuses == {
        "src_hnz_capitation_schedule": "processed_ready",
        "src_pho_services_agreement": "processed_ready",
        "src_hnz_enrolment": "processed_ready",
        "src_hnz_pho_access_timeseries": "processed_ready",
        "src_mcnz_workforce": "processed_ready",
        "src_nz_health_survey": "processed_ready",
        "src_statsnz_population": "processed_ready",
    }
    assert all(plan.expected_raw_dir == f"data/public_raw/{plan.source_id}" for plan in plans)
    assert all(plan.fetch_script.startswith("scripts/fetch_") for plan in plans)
    assert all(plan.expected_processed_artifact.startswith(f"data/public_processed/{plan.source_id}/") for plan in plans)
    assert all("patient-level" not in plan.claim_boundary.lower() or "no patient-level" in plan.claim_boundary.lower() for plan in plans)


def test_public_source_retrieval_plan_verifier_passes() -> None:
    assert verify_public_source_retrieval_plan() == ()


def test_public_source_retrieval_plan_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_retrieval_plan.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "public source retrieval plan passed" in result.stdout
