from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from models.primarycare_model.calibration.public_policy_shock_plausibility import (
    REQUIRED_NUMERIC_COMPARISON_COLUMNS,
    NumericComparisonContract,
    _numeric_comparison_contract,
    _numeric_comparison_readiness,
    OBSERVED_DELTA_TOLERANCE,
    _numeric_value,
    _required_text,
    _direction_from_delta,
    NumericComparisonReadiness,
    build_public_policy_shock_evidence,
    main,
    policy_shock_gate_blockers,
    policy_shock_gate_status,
    public_policy_shock_evidence_as_json,
)

ROOT = Path(__file__).resolve().parents[2]


def test_public_policy_shock_evidence_is_registered_without_promoting_claims() -> None:
    rows = build_public_policy_shock_evidence()

    assert {row.gate_id for row in rows} == {"CAL-G-005"}
    assert {row.gate_role for row in rows} == {"numeric_comparison", "reference_only"}
    assert any(row.comparison_status == "passed" for row in rows)
    assert {row.claim_status for row in rows} == {"calibration_readiness_only"}
    assert all(row.public_access_status == "public" for row in rows)
    assert all("no causal" in row.claim_boundary for row in rows)


def test_public_policy_shock_gate_passes_numeric_comparison_lane() -> None:
    assert policy_shock_gate_status() == "passed"
    assert policy_shock_gate_blockers() == ()


def test_public_policy_shock_numeric_comparison_contract_is_satisfied_for_gate_rows() -> None:
    rows = build_public_policy_shock_evidence()
    gate_rows = [row for row in rows if row.gate_role == "numeric_comparison"]

    assert gate_rows
    assert {row.numeric_comparison_readiness.status for row in gate_rows} == {"comparison_passed"}
    assert all(row.numeric_comparison_contract.required_columns for row in gate_rows)
    assert all("CAL-G-005 can pass only" in row.numeric_comparison_contract.pass_rule for row in gate_rows)


def test_public_policy_shock_reference_rows_do_not_block_gate() -> None:
    rows = build_public_policy_shock_evidence()
    reference_rows = [row for row in rows if row.gate_role == "reference_only"]

    assert reference_rows
    assert {row.comparison_status for row in reference_rows} == {"readiness_only"}
    assert {row.numeric_comparison_readiness.status for row in reference_rows} == {"artifact_not_registered"}


def test_public_policy_shock_json_has_claim_boundary() -> None:
    payload = json.loads(public_policy_shock_evidence_as_json())

    assert payload["gate_status"] == "passed"
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

    assert result.returncode == 0, result.stdout + result.stderr
    assert "status=passed" in result.stdout


def test_public_policy_shock_main_fails_only_when_pass_is_required() -> None:
    assert main(["--json"]) == 0
    assert main(["--require-pass"]) == 0


def test_public_policy_shock_artifact_matches_checked_in_capitation_extract() -> None:
    source_path = ROOT / "data" / "public_processed" / "src_hnz_capitation_schedule" / "capitation_rates.csv"
    artifact_path = (
        ROOT
        / "data"
        / "public_processed"
        / "src_hnz_capitation_schedule"
        / "policy_shock_pre_post_comparison.csv"
    )
    source_rows = _read_csv(source_path)
    artifact_rows = _read_csv(artifact_path)

    def source_value(*, table_index: str, row_index: str, column_label: str) -> float:
        for row in source_rows:
            if (
                row["table_index"] == table_index
                and row["row_index"] == row_index
                and row["column_label"] == column_label
            ):
                return float(row["cell_value"].replace("$", ""))
        raise AssertionError(f"missing source value {table_index=} {row_index=} {column_label=}")

    for row in artifact_rows:
        assert float(row["pre_value"]) == source_value(
            table_index=row["source_table_index_pre"],
            row_index=row["source_row_index"],
            column_label=row["source_column_label"],
        )
        assert float(row["post_value"]) == source_value(
            table_index=row["source_table_index_post"],
            row_index=row["source_row_index"],
            column_label=row["source_column_label"],
        )
        assert "no causal" in row["claim_boundary"]


def _read_csv(path: Path) -> list[dict[str, str]]:
    import csv

    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def test_numeric_comparison_artifact_requires_delta_to_match_values() -> None:
    readiness = _numeric_comparison_readiness(
        shock_id="shock-a",
        comparison_artifact="tests/fixtures/policy_shock_mismatched_delta_comparison.csv",
        contract=NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test readiness",
            pass_rule="test pass",
        ),
    )

    assert readiness.status == "artifact_invalid"
    assert readiness.rows_checked == 1
    assert any("observed_delta must equal post_value - pre_value" in issue for issue in readiness.issues)


def test_numeric_comparison_artifact_requires_direction_to_match_delta() -> None:
    readiness = _numeric_comparison_readiness(
        shock_id="shock-a",
        comparison_artifact="tests/fixtures/policy_shock_mismatched_direction_comparison.csv",
        contract=NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test readiness",
            pass_rule="test pass",
        ),
    )

    assert readiness.status == "artifact_invalid"
    assert readiness.rows_checked == 1
    assert any("observed_direction must match observed_delta" in issue for issue in readiness.issues)


def test_passed_numeric_comparison_requires_direction_agreement() -> None:
    readiness = _numeric_comparison_readiness(
        shock_id="shock-a",
        comparison_artifact="tests/fixtures/policy_shock_passed_direction_disagreement_comparison.csv",
        contract=NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test readiness",
            pass_rule="test pass",
        ),
    )

    assert readiness.status == "artifact_invalid"
    assert readiness.rows_checked == 1
    assert any("comparison_result=passed requires observed_direction to match modelled_direction" in issue for issue in readiness.issues)

def test_numeric_comparison_readiness_to_json_dict() -> None:
    readiness = NumericComparisonReadiness(
        status="artifact_invalid",
        artifact_path="test",
        rows_checked=0,
        issues=("issue 1", "issue 2")
    )
    payload = readiness.to_json_dict()
    assert payload["status"] == "artifact_invalid"
    assert payload["issues"] == ["issue 1", "issue 2"]

def test_required_text() -> None:
    assert _required_text(None) is None
    assert _required_text("   ") is None
    assert _required_text(" test ") == "test"

def test_direction_from_delta() -> None:
    assert _direction_from_delta(OBSERVED_DELTA_TOLERANCE + 0.1) == "increase"
    assert _direction_from_delta(-(OBSERVED_DELTA_TOLERANCE + 0.1)) == "decrease"
    assert _direction_from_delta(0.0) == "no_change"

def test_numeric_comparison_contract_default() -> None:
    contract = _numeric_comparison_contract({})
    assert contract.required_columns == REQUIRED_NUMERIC_COMPARISON_COLUMNS
    assert "Public numeric pre/post comparison requires" in contract.readiness_rule

def test_numeric_comparison_readiness_missing_artifact() -> None:
    contract = NumericComparisonContract(
        required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
        readiness_rule="test",
        pass_rule="test"
    )
    readiness = _numeric_comparison_readiness(shock_id="shock_id", comparison_artifact="does_not_exist.csv", contract=contract)
    assert readiness.status == "artifact_missing"

def test_numeric_comparison_readiness_no_rows() -> None:
    import tempfile
    import csv
    with tempfile.NamedTemporaryFile(mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_NUMERIC_COMPARISON_COLUMNS)
        writer.writeheader()
        f.flush()

        contract = NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test",
            pass_rule="test"
        )
        readiness = _numeric_comparison_readiness(shock_id="shock_id", comparison_artifact=f.name, contract=contract)
        assert readiness.status == "artifact_invalid"
        assert any("No numeric comparison rows found" in issue for issue in readiness.issues)

def test_numeric_comparison_readiness_all_validation_issues() -> None:
    import tempfile
    import csv
    with tempfile.NamedTemporaryFile(mode="w", newline="") as f:
        fields = REQUIRED_NUMERIC_COMPARISON_COLUMNS + ("shock_id", "source_row_index", "source_column_label", "claim_boundary", "source_table_index_pre", "source_table_index_post", "metric_id", "pre_period", "post_period", "pre_value", "post_value", "observed_delta", "observed_direction", "modelled_direction", "comparison_result")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        # Write a row missing everything to trigger all issues
        writer.writerow({
            "shock_id": "shock_id",
            "metric_id": "  ",
            "pre_period": "",
            "post_period": "  ",
            "pre_value": "not_num",
            "post_value": "not_num",
            "observed_delta": "not_num",
            "observed_direction": "invalid",
            "modelled_direction": "invalid",
            "comparison_result": "invalid",
            "source_table_index_pre": "",
            "source_table_index_post": "",
            "source_row_index": "",
            "source_column_label": "",
            "claim_boundary": ""
        })
        f.flush()

        contract = NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule="test",
            pass_rule="test"
        )
        readiness = _numeric_comparison_readiness(shock_id="shock_id", comparison_artifact=f.name, contract=contract)
        assert readiness.status == "artifact_invalid"
        issues_str = " ".join(readiness.issues)
        assert "metric_id is required" in issues_str
        assert "pre_period is required" in issues_str
        assert "post_period is required" in issues_str
        assert "pre_value is not numeric" in issues_str
        assert "post_value is not numeric" in issues_str
        assert "observed_delta is not numeric" in issues_str
        assert "observed_direction must be one of" in issues_str
        assert "modelled_direction must be one of" in issues_str
        assert "comparison_result must be one of" in issues_str

def test_numeric_value_parsing_edge_cases() -> None:
    # Test valid numeric values
    assert _numeric_value("123.45") == 123.45
    assert _numeric_value("$1,234.56") == 1234.56

    # Test empty or None values
    assert _numeric_value(None) is None
    assert _numeric_value("") is None
    assert _numeric_value("   ") is None
    assert _numeric_value("$") is None
    assert _numeric_value(",") is None
    assert _numeric_value("$,") is None

    # Test invalid string that triggers ValueError
    assert _numeric_value("not-a-number") is None
    assert _numeric_value("12.34.56") is None
