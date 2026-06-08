from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.data.public_source_readiness_matrix import (
    build_public_source_readiness_matrix,
    readiness_matrix_as_json,
    strict_readiness_issues,
)
from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans


def test_public_source_readiness_matrix_has_one_row_per_retrieval_plan() -> None:
    rows = build_public_source_readiness_matrix()
    plans = load_public_source_retrieval_plans()
    assert {row.source_id for row in rows} == {plan.source_id for plan in plans}
    assert all(row.calibration_claim_status == "public_aggregate_source_ready" for row in rows)


def test_public_source_readiness_matrix_default_mode_is_non_promotional() -> None:
    rows = build_public_source_readiness_matrix()
    assert rows
    assert all(row.source_ready for row in rows)
    assert all(row.issues == () for row in rows)
    assert {row.checksum_status for row in rows} == {"verified"}
    assert {row.processed_artifact_status for row in rows} == {"expected_processed_artifact_present"}


def test_public_source_readiness_matrix_strict_mode_reports_blockers() -> None:
    assert strict_readiness_issues() == ()


def test_public_source_readiness_matrix_json_has_claim_boundary() -> None:
    payload = json.loads(readiness_matrix_as_json())
    assert "public benchmark only" in payload["claim_boundary"]
    assert len(payload["rows"]) == len(load_public_source_retrieval_plans())


def test_public_source_readiness_matrix_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_readiness_matrix.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "public_aggregate_source_ready" in result.stdout


def test_public_source_readiness_matrix_cli_strict_mode_passes_after_processed_artifacts_exist() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_readiness_matrix.py", "--strict"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
