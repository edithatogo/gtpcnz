from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
    strict_validation_gate_issues,
    validation_gate_matrix_as_json,
)


def test_calibration_validation_gate_matrix_includes_required_gate_ids() -> None:
    rows = build_calibration_validation_gate_matrix()
    assert {row.gate_id for row in rows} == {
        "CAL-G-001",
        "CAL-G-002",
        "CAL-G-003",
        "CAL-G-004",
        "CAL-G-005",
        "CAL-G-006",
        "CAL-G-007",
    }


def test_calibration_validation_gate_matrix_default_mode_is_non_promotional() -> None:
    rows = build_calibration_validation_gate_matrix()
    assert any(row.status == "calibration_readiness_only" for row in rows)
    assert any(row.status == "public_data_unavailable" for row in rows)
    assert all(row.blockers == () for row in rows)
    assert {row.claim_status for row in rows} == {"calibration_readiness_only"}


def test_calibration_validation_gate_strict_mode_reports_target_and_holdout_blockers() -> None:
    issues = strict_validation_gate_issues()
    assert any("CAL-G-001" in issue for issue in issues)
    assert any("CAL-G-002" in issue for issue in issues)
    assert any("source_ready" in issue for issue in issues)
    assert any("public aggregate holdout dataset" in issue for issue in issues)


def test_calibration_validation_gate_json_has_claim_boundary() -> None:
    payload = json.loads(validation_gate_matrix_as_json())
    assert "public benchmark only" in payload["claim_boundary"]
    assert len(payload["rows"]) == 7


def test_calibration_validation_gate_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_validation_gates.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAL-G-001" in result.stdout
    assert "calibration_readiness_only" in result.stdout


def test_calibration_validation_gate_cli_strict_mode_fails_until_validation_ready() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_validation_gates.py", "--strict"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert "claim remains calibration_readiness_only" in result.stderr