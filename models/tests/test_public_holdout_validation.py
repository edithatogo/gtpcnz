from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.public_holdout_validation import (
    build_public_holdout_comparisons,
    holdout_gate_blockers,
    holdout_gate_status,
    public_holdout_comparisons_as_json,
)


def test_public_holdout_comparisons_run_without_promoting_claims() -> None:
    comparisons = build_public_holdout_comparisons()

    assert comparisons
    assert {row.gate_id for row in comparisons} == {"CAL-G-003", "CAL-G-004"}
    assert any(row.status == "comparison_failed" for row in comparisons)
    assert {row.claim_status for row in comparisons} == {"calibration_readiness_only"}


def test_public_holdout_gate_statuses_report_failed_comparisons() -> None:
    assert holdout_gate_status("CAL-G-003") == "public_holdout_comparison_failed"
    assert holdout_gate_status("CAL-G-004") == "public_holdout_comparison_failed"
    assert holdout_gate_blockers("CAL-G-003")
    assert holdout_gate_blockers("CAL-G-004")


def test_public_holdout_comparison_json_has_claim_boundary() -> None:
    payload = json.loads(public_holdout_comparisons_as_json())

    assert "calibration_readiness_only" in payload["claim_boundary"]
    assert payload["rows"]


def test_public_holdout_cli_readiness_mode_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_holdout_validation.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "comparison_failed" in result.stdout


def test_public_holdout_cli_require_pass_fails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_holdout_validation.py", "--require-pass"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "max_abs_error" in result.stderr
