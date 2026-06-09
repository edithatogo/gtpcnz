from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.public_policy_shock_plausibility import (
    build_public_policy_shock_evidence,
    policy_shock_gate_blockers,
    policy_shock_gate_status,
    public_policy_shock_evidence_as_json,
)


def test_public_policy_shock_evidence_is_registered_without_promoting_claims() -> None:
    rows = build_public_policy_shock_evidence()

    assert {row.gate_id for row in rows} == {"CAL-G-005"}
    assert {row.comparison_status for row in rows} == {"readiness_only"}
    assert {row.claim_status for row in rows} == {"calibration_readiness_only"}
    assert all(row.public_access_status == "public" for row in rows)
    assert all("no causal" in row.claim_boundary for row in rows)


def test_public_policy_shock_gate_remains_source_registered_readiness_only() -> None:
    assert policy_shock_gate_status() == "public_validation_source_registered"
    assert policy_shock_gate_blockers() == (
        "CAL-G-005: public policy-shock evidence is registered, but no public pre/post "
        "shock comparison has passed; claim remains calibration_readiness_only",
    )


def test_public_policy_shock_json_has_claim_boundary() -> None:
    payload = json.loads(public_policy_shock_evidence_as_json())

    assert payload["gate_status"] == "public_validation_source_registered"
    assert "no causal" in payload["claim_boundary"]
    assert payload["rows"]


def test_public_policy_shock_cli_readiness_mode_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_policy_shock_plausibility.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAL-G-005" in result.stdout
    assert "calibration_readiness_only" in result.stdout


def test_public_policy_shock_cli_require_pass_fails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_policy_shock_plausibility.py", "--require-pass"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "claim remains calibration_readiness_only" in result.stderr
