from __future__ import annotations

from models.primarycare_model.calibration.public_aggregate_calibration import run_public_aggregate_calibration


def test_public_aggregate_calibration_runs_and_bounds_claims() -> None:
    result = run_public_aggregate_calibration()
    assert result["calibration_status"] in {"public_aggregate_validated", "calibration_readiness_only"}
    assert "precise fiscal savings" in result["not_valid_for"]
    assert result["checks"]
