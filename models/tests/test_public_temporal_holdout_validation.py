from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
)
from models.primarycare_model.calibration.public_temporal_holdout_validation import (
    build_public_temporal_holdout_comparisons,
    load_temporal_holdout_targets,
    public_temporal_holdout_comparisons_as_json,
    temporal_holdout_gate_blockers,
    temporal_holdout_gate_status,
)


def _synthetic_rows(*, holdout_rate: float) -> tuple[dict[str, str], ...]:
    return (
        {
            "source_id": "src_hnz_pho_access_timeseries",
            "period": "2025-Q3",
            "district": "Auckland",
            "stratifier": "ethnicity",
            "group": "Total",
            "enrolled_count": "90",
            "population_count": "100",
            "reported_coverage_rate": "0.9",
        },
        {
            "source_id": "src_hnz_pho_access_timeseries",
            "period": "2025-Q4",
            "district": "Auckland",
            "stratifier": "ethnicity",
            "group": "Total",
            "enrolled_count": str(holdout_rate * 100),
            "population_count": "100",
            "reported_coverage_rate": str(holdout_rate),
        },
    )


def test_temporal_holdout_registry_is_cal_g_002_public_only() -> None:
    targets = load_temporal_holdout_targets()

    assert len(targets) == 1
    assert targets[0].gate_id == "CAL-G-002"
    assert targets[0].source_id == "src_hnz_pho_access_timeseries"
    assert targets[0].public_access_status == "public"
    assert "Public aggregate temporal validation evidence only" in targets[0].claim_boundary


def test_current_public_temporal_holdout_is_registered_but_not_passed() -> None:
    comparisons = build_public_temporal_holdout_comparisons()

    assert len(comparisons) == 1
    comparison = comparisons[0]
    assert comparison.gate_id == "CAL-G-002"
    assert comparison.status == "public_validation_source_registered"
    assert comparison.periods_available == ("2025-Q4",)
    assert comparison.holdout_period is None
    assert comparison.claim_status == "calibration_readiness_only"


def test_temporal_holdout_gate_matrix_wires_cal_g_002_status() -> None:
    rows = {row.gate_id: row for row in build_calibration_validation_gate_matrix(strict=True)}

    assert rows["CAL-G-002"].status == "public_validation_source_registered"
    assert rows["CAL-G-002"].claim_status == "calibration_readiness_only"
    assert temporal_holdout_gate_status("CAL-G-002") == "public_validation_source_registered"
    assert temporal_holdout_gate_blockers("CAL-G-002")


def test_temporal_holdout_future_two_period_comparison_can_pass_or_fail() -> None:
    passed = build_public_temporal_holdout_comparisons(rows=_synthetic_rows(holdout_rate=0.91))[0]
    failed = build_public_temporal_holdout_comparisons(rows=_synthetic_rows(holdout_rate=0.75))[0]

    assert passed.status == "passed"
    assert passed.holdout_period == "2025-Q4"
    assert passed.training_periods == ("2025-Q3",)
    assert failed.status == "temporal_comparison_failed"
    assert failed.max_absolute_error == 0.15


def test_public_temporal_holdout_json_has_claim_boundary() -> None:
    payload = json.loads(public_temporal_holdout_comparisons_as_json())

    assert "calibration_readiness_only" in payload["claim_boundary"]
    assert payload["rows"][0]["gate_id"] == "CAL-G-002"


def test_public_temporal_holdout_cli_readiness_mode_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_temporal_holdout_validation.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAL-G-002" in result.stdout
    assert "public_validation_source_registered" in result.stdout


def test_public_temporal_holdout_cli_require_pass_fails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_temporal_holdout_validation.py", "--require-pass"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "at least 2 are required" in result.stderr
