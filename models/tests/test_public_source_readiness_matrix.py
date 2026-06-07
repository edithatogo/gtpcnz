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
    assert all(row.calibration_claim_status == "calibration_readiness_only" for row in rows)


def test_public_source_readiness_matrix_default_mode_is_non_promotional() -> None:
    rows = build_public_source_readiness_matrix()
    assert rows
    assert all(not row.source_ready for row in rows)
    assert all(row.issues == () for row in rows)
    assert {row.checksum_status for row in rows} == {"pending_download"}


def test_public_source_readiness_matrix_strict_mode_reports_blockers() -> None:
    issues = strict_readiness_issues()
    assert any("source_ready=false" in issue for issue in issues)
    assert any("checksum is pending-download" in issue for issue in issues)
    assert any("no raw public source files" in issue for issue in issues)
    assert any("no processed public source files" in issue for issue in issues)


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
    assert "calibration_readiness_only" in result.stdout


def test_public_source_readiness_matrix_cli_strict_mode_fails_until_artifacts_exist() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_readiness_matrix.py", "--strict"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert "calibration remains calibration_readiness_only" in result.stderr