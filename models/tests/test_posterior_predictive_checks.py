from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.posterior_predictive_checks import (
    posterior_predictive_checks,
    posterior_predictive_checks_as_json,
    posterior_predictive_target_rows,
    strict_posterior_predictive_issues,
)


def test_posterior_predictive_checks_are_readiness_only_by_default() -> None:
    payload = posterior_predictive_checks()
    assert payload["ppc_gate_id"] == "CAL-G-006"
    assert payload["ppc_status"] == "calibration_readiness_only"
    assert payload["validation_gate_status"] == "calibration_readiness_only"
    assert payload["failed_targets"]
    assert "precise fiscal savings" in payload["not_valid_for"]


def test_posterior_predictive_target_rows_include_source_and_tolerance_status() -> None:
    rows = posterior_predictive_target_rows()
    assert rows
    assert all(row.posterior_predictive_status == "calibration_readiness_only" for row in rows)
    assert all(not row.source_ready for row in rows)
    assert all(row.tolerance >= 0 for row in rows)


def test_posterior_predictive_strict_mode_reports_validation_blockers() -> None:
    issues = strict_posterior_predictive_issues()
    assert any("CAL-G-006" in issue for issue in issues)
    assert any("source_ready" in issue for issue in issues)
    assert any("public aggregate holdout dataset" in issue for issue in issues)


def test_posterior_predictive_json_payload_is_machine_readable() -> None:
    payload = json.loads(posterior_predictive_checks_as_json())
    assert payload["ppc_gate_id"] == "CAL-G-006"
    assert isinstance(payload["target_rows"], list)


def test_posterior_predictive_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_posterior_predictive_checks.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAL-G-006" in result.stdout
    assert "calibration_readiness_only" in result.stdout


def test_posterior_predictive_cli_strict_mode_fails_until_ppc_ready() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_posterior_predictive_checks.py", "--strict"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert "posterior predictive checks remain calibration_readiness_only" in result.stderr