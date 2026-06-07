from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.calibration_target_readiness import (
    build_calibration_target_readiness_matrix,
    readiness_matrix_as_json,
    strict_calibration_target_issues,
)
from models.primarycare_model.calibration.public_aggregate_calibration import load_calibration_targets


def test_calibration_target_readiness_has_one_row_per_target() -> None:
    rows = build_calibration_target_readiness_matrix()
    targets = load_calibration_targets()
    assert {row.target_id for row in rows} == {target.target_id for target in targets}
    assert all(row.calibration_claim_status == "calibration_readiness_only" for row in rows)


def test_calibration_target_readiness_default_mode_is_non_promotional() -> None:
    rows = build_calibration_target_readiness_matrix()
    assert rows
    assert all(not row.source_ready for row in rows)
    assert all(not row.calibration_gate_ready for row in rows)
    assert all(row.blockers == () for row in rows)
    assert all("precise fiscal savings" in row.not_valid_for for row in rows)


def test_calibration_target_readiness_strict_mode_reports_source_blockers() -> None:
    issues = strict_calibration_target_issues()
    assert any("calibration target remains calibration_readiness_only" in issue for issue in issues)
    assert any("is not source_ready" in issue for issue in issues)
    assert any("checksum is pending-download" in issue for issue in issues)


def test_calibration_target_readiness_json_has_claim_boundary() -> None:
    payload = json.loads(readiness_matrix_as_json())
    assert "public benchmark only" in payload["claim_boundary"]
    assert len(payload["rows"]) == len(load_calibration_targets())


def test_calibration_target_readiness_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_target_readiness.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "calibration_readiness_only" in result.stdout


def test_calibration_target_readiness_cli_strict_mode_fails_until_targets_ready() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_target_readiness.py", "--strict"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert "calibration target remains calibration_readiness_only" in result.stderr