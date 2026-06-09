from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.public_policy_shock_plausibility import (
    REQUIRED_NUMERIC_COMPARISON_COLUMNS,
    NumericComparisonContract,
    _numeric_comparison_readiness,
    build_public_policy_shock_evidence,
    main,
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
    blockers = policy_shock_gate_blockers()
    assert blockers
    assert all("No public numeric pre/post comparison artifact is registered" in blocker for blocker in blockers)


def test_public_policy_shock_numeric_comparison_contract_is_not_satisfied() -> None:
    rows = build_public_policy_shock_evidence()

    assert {row.numeric_comparison_readiness.status for row in rows} == {"artifact_not_registered"}
    assert all(row.numeric_comparison_contract.required_columns for row in rows)
    assert all("CAL-G-005 can pass only" in row.numeric_comparison_contract.pass_rule for row in rows)


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
    assert "No public numeric pre/post comparison artifact is registered" in result.stderr


def test_public_policy_shock_main_fails_only_when_pass_is_required() -> None:
    assert main(["--json"]) == 0
    assert main(["--require-pass"]) == 1


def test_numeric_comparison_artifact_requires_contract_columns() -> None:
    readiness = _numeric_comparison_readiness(
        shock_id="shock-a",
        comparison_artifact="tests/fixtures/policy_shock_bad_comparison.csv",
        contract=NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test readiness",
            pass_rule="test pass",
        ),
    )

    assert readiness.status == "artifact_invalid"
    assert readiness.rows_checked == 0
    assert any("Missing required numeric comparison columns" in issue for issue in readiness.issues)


def test_numeric_comparison_artifact_can_be_numeric_ready() -> None:
    readiness = _numeric_comparison_readiness(
        shock_id="shock-a",
        comparison_artifact="tests/fixtures/policy_shock_numeric_ready_comparison.csv",
        contract=NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test readiness",
            pass_rule="test pass",
        ),
    )

    assert readiness.status == "numeric_pre_post_ready"
    assert readiness.rows_checked == 1
    assert readiness.issues == ()
