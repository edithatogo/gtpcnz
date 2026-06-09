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
    assert next(row for row in comparisons if row.gate_id == "CAL-G-003").status == "passed"
    assert {row.claim_status for row in comparisons} == {"calibration_readiness_only"}


def test_public_holdout_gate_statuses_report_cal_g_003_passed_and_cal_g_004_failed() -> None:
    assert holdout_gate_status("CAL-G-003") == "passed"
    assert holdout_gate_status("CAL-G-004") == "public_holdout_comparison_failed"
    assert holdout_gate_blockers("CAL-G-003") == ()
    assert holdout_gate_blockers("CAL-G-004")
    assert "failing_groups=" in holdout_gate_blockers("CAL-G-004")[0]
    assert "next_data_model_requirement=" in holdout_gate_blockers("CAL-G-004")[0]


def test_public_holdout_comparison_json_has_claim_boundary() -> None:
    payload = json.loads(public_holdout_comparisons_as_json())

    assert "calibration_readiness_only" in payload["claim_boundary"]
    assert payload["rows"]
    failed_rows = [row for row in payload["rows"] if row["status"] == "comparison_failed"]
    assert failed_rows
    assert all(row["tolerance_gap"] > 0 for row in failed_rows)
    assert all(row["failing_groups"] for row in failed_rows)
    assert all(row["failing_observations"] for row in failed_rows)
    assert all(row["next_data_model_requirement"] for row in failed_rows)


def test_public_holdout_cli_readiness_mode_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_holdout_validation.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAL-G-003: district/total_coverage; status=passed" in result.stdout
    assert "comparison_failed" in result.stdout
    assert "tolerance_gap=" in result.stdout
    assert "failing_groups=" in result.stdout
    assert "next=" in result.stdout


def test_public_holdout_cli_require_pass_fails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_holdout_validation.py", "--require-pass"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "max_abs_error" in result.stderr
    assert "tolerance_gap=" in result.stderr
    assert "failing_groups=" in result.stderr
    assert "next_data_model_requirement=" in result.stderr
    assert "CAL-G-003" not in result.stderr
