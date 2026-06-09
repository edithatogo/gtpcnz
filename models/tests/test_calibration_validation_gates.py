from __future__ import annotations

import json
import os
import subprocess
import sys

from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
    strict_validation_gate_issues,
    validation_gate_issues,
    validation_gate_matrix_as_json,
)

SUBPROCESS_ENV = {
    **os.environ,
    "OPENBLAS_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
}


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
    assert all(row.blockers == () for row in rows)
    assert any(row.claim_status == "public_aggregate_validated" for row in rows)
    assert any(row.claim_status == "calibration_readiness_only" for row in rows)
    assert next(row for row in rows if row.gate_id == "CAL-G-005").claim_status == "calibration_readiness_only"
    assert next(row for row in rows if row.gate_id == "CAL-G-007").claim_status == "calibration_readiness_only"


def test_calibration_validation_gate_strict_mode_allows_documented_unavailable_holdouts() -> None:
    assert strict_validation_gate_issues() == ()


def test_calibration_validation_gate_require_all_validation_data_blocks_source_registered_gates() -> None:
    issues = validation_gate_issues(require_all_validation_data=True)
    assert not any("CAL-G-002" in issue for issue in issues)
    assert not any("CAL-G-003" in issue for issue in issues)
    assert not any("CAL-G-004" in issue for issue in issues)
    assert not any("CAL-G-005" in issue for issue in issues)
    assert issues == ()


def test_calibration_validation_gate_json_has_claim_boundary() -> None:
    payload = json.loads(validation_gate_matrix_as_json())
    assert "public benchmark only" in payload["claim_boundary"]
    assert len(payload["rows"]) == 7


def test_calibration_validation_gate_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_validation_gates.py"],
        text=True,
        capture_output=True,
        env=SUBPROCESS_ENV,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAL-G-001" in result.stdout
    assert "calibration_readiness_only" in result.stdout


def test_calibration_validation_gate_cli_strict_mode_passes_readiness_validation() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_validation_gates.py", "--strict"],
        text=True,
        capture_output=True,
        env=SUBPROCESS_ENV,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_calibration_validation_gate_cli_empirical_upgrade_mode_passes_validation_gates() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_calibration_validation_gates.py",
            "--strict",
            "--require-all-validation-data",
        ],
        text=True,
        capture_output=True,
        env=SUBPROCESS_ENV,
    )
    assert result.returncode == 0, result.stdout + result.stderr
