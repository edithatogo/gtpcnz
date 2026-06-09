from __future__ import annotations

import json
import subprocess
import sys

from models.primarycare_model.data.public_temporal_period_acquisition import (
    build_temporal_period_readiness,
    load_temporal_period_acquisition_plans,
    public_temporal_period_readiness_as_json,
    temporal_period_acquisition_issues,
)


def test_temporal_period_acquisition_plan_is_cal_g_002_only() -> None:
    plans = load_temporal_period_acquisition_plans()

    assert len(plans) == 1
    plan = plans[0]
    assert plan.gate_id == "CAL-G-002"
    assert plan.source_id == "src_hnz_pho_access_timeseries"
    assert plan.minimum_distinct_periods == 2
    assert plan.acquired_public_periods[0].period == "2025-Q4"
    assert plan.missing_public_period_requirements[0].status == "missing_public_file"
    assert "calibration_readiness_only" in plan.claim_boundary


def test_temporal_period_readiness_reports_missing_public_period_without_claim_upgrade() -> None:
    readiness = build_temporal_period_readiness()

    assert len(readiness) == 1
    row = readiness[0]
    assert row.gate_id == "CAL-G-002"
    assert row.status == "acquisition_plan_ready_missing_public_periods"
    assert row.claim_status == "calibration_readiness_only"
    assert row.periods_available == ("2025-Q4",)
    assert row.missing_public_periods == ("any_public_period_before_latest_available",)
    assert row.blockers


def test_temporal_period_acquisition_default_check_is_readiness_compatible() -> None:
    assert temporal_period_acquisition_issues() == ()
    assert temporal_period_acquisition_issues(require_ready=True)


def test_temporal_period_acquisition_json_lists_missing_public_period_requirements() -> None:
    payload = json.loads(public_temporal_period_readiness_as_json())

    assert "no invented data" in payload["claim_boundary"]
    row = payload["rows"][0]
    assert row["gate_id"] == "CAL-G-002"
    assert row["missing_public_period_requirements"][0]["requirement_id"] == "cal_g_002_training_period_1"


def test_temporal_period_acquisition_cli_default_passes_and_strict_fails() -> None:
    default = subprocess.run(
        [sys.executable, "scripts/check_public_temporal_period_acquisition.py"],
        text=True,
        capture_output=True,
    )
    strict = subprocess.run(
        [sys.executable, "scripts/check_public_temporal_period_acquisition.py", "--require-ready"],
        text=True,
        capture_output=True,
    )

    assert default.returncode == 0, default.stdout + default.stderr
    assert "acquisition_plan_ready_missing_public_periods" in default.stdout
    assert strict.returncode == 1
    assert "missing public temporal period requirement" in strict.stderr
