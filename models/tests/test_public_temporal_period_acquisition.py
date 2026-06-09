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
    assert "2025-Q4" in {period.period for period in plan.acquired_public_periods}
    if plan.missing_public_period_requirements:
        assert plan.missing_public_period_requirements[0].status == "missing_public_file"
    else:
        assert len({period.period for period in plan.acquired_public_periods}) >= plan.minimum_distinct_periods
    assert "calibration_readiness_only" in plan.claim_boundary


def test_temporal_period_readiness_tracks_processed_periods_without_claim_upgrade() -> None:
    readiness = build_temporal_period_readiness()

    assert len(readiness) == 1
    row = readiness[0]
    assert row.gate_id == "CAL-G-002"
    assert row.claim_status == "calibration_readiness_only"
    assert "2025-Q4" in row.periods_available
    if len(row.periods_available) >= 2:
        assert row.status == "ready_for_temporal_holdout"
        assert row.missing_public_periods == ()
        assert row.blockers == ()
    else:
        assert row.status == "acquisition_plan_ready_missing_public_periods"
        assert row.missing_public_periods == ("any_public_period_before_latest_available",)
        assert row.blockers


def test_temporal_period_acquisition_default_check_is_readiness_compatible() -> None:
    assert temporal_period_acquisition_issues() == ()
    readiness = build_temporal_period_readiness()[0]
    strict_issues = temporal_period_acquisition_issues(require_ready=True)
    if len(readiness.periods_available) >= 2:
        assert strict_issues == ()
    else:
        assert strict_issues


def test_temporal_period_acquisition_json_reports_period_state() -> None:
    payload = json.loads(public_temporal_period_readiness_as_json())

    assert "no invented data" in payload["claim_boundary"]
    row = payload["rows"][0]
    assert row["gate_id"] == "CAL-G-002"
    assert "2025-Q4" in row["periods_available"]
    if len(row["periods_available"]) >= 2:
        assert row["missing_public_period_requirements"] == []
    else:
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
    assert "CAL-G-002" in default.stdout
    readiness = build_temporal_period_readiness()[0]
    if len(readiness.periods_available) >= 2:
        assert "ready_for_temporal_holdout" in default.stdout
        assert strict.returncode == 0
    else:
        assert "acquisition_plan_ready_missing_public_periods" in default.stdout
        assert strict.returncode == 1
        assert "missing public temporal period requirement" in strict.stderr
