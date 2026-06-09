import pandas as pd

from models.primarycare_model import empirical_calibration
from models.primarycare_model.calibration_v150 import DEFAULT_BASELINE, CalibrationParameters, simulate_months
from models.primarycare_model.empirical_calibration import (
    LinkedCalibrationSummary,
    build_claim_boundary_text,
    load_linked_inputs,
    run_empirical_calibration_pipeline,
)


def _synthetic_linked_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    params = CalibrationParameters(
        marginal_supply_response=0.30,
        unmet_need_to_ed_rate=0.25,
        copayment_elasticity=0.20,
        ambulance_deflection_rate=0.20,
        acc_stabilisation_effect=0.12,
        scope_supply_multiplier=0.20,
    )
    monthly = simulate_months(params, DEFAULT_BASELINE, months=30)
    geographic = pd.DataFrame(
        {
            "month": [1, 1, 2, 2],
            "locality": ["A", "B", "A", "B"],
            "primary_contacts": [850.0, 790.0, 860.0, 800.0],
            "unmet_need_index": [0.12, 0.18, 0.11, 0.17],
            "ed_presentations": [190.0, 220.0, 188.0, 218.0],
            "ambulance_conveyances": [50.0, 62.0, 49.0, 61.0],
            "public_cost": [1_000_000.0, 1_060_000.0, 1_005_000.0, 1_058_000.0],
        }
    )
    equity = pd.DataFrame(
        {
            "month": [1, 1, 2, 2],
            "equity_group": ["least_deprived", "most_deprived", "least_deprived", "most_deprived"],
            "primary_contacts": [900.0, 760.0, 910.0, 750.0],
            "unmet_need_index": [0.10, 0.28, 0.11, 0.29],
            "ed_presentations": [175.0, 245.0, 176.0, 248.0],
            "ambulance_conveyances": [45.0, 70.0, 46.0, 71.0],
            "public_cost": [990_000.0, 1_120_000.0, 995_000.0, 1_130_000.0],
        }
    )
    shocks = pd.DataFrame(
        {
            "shock_month": [15],
            "shock_type": ["scope"],
            "target_metric": ["primary_contacts"],
            "shock_delta": [0.10],
            "expected_direction": [1],
        }
    )
    return monthly, geographic, equity, shocks


def _unsupported_summary(supported_where_valid: bool, available: bool = True) -> LinkedCalibrationSummary:
    return LinkedCalibrationSummary(
        available=available,
        supported_where_valid=supported_where_valid,
        in_sample_score=0.0 if available else None,
        holdout_score=0.0 if available else None,
        parameter_estimates={},
        parameter_bounds={},
        validation=(),
    )


def test_load_linked_inputs_returns_empty_for_missing_dir():
    monthly, geographic, equity, shocks = load_linked_inputs("does-not-exist")
    assert monthly.empty
    assert geographic.empty
    assert equity.empty
    assert shocks.empty


def test_empirical_calibration_pipeline_runs_on_synthetic_linked_data(monkeypatch):
    monkeypatch.setattr(empirical_calibration, "load_linked_inputs", lambda linked_dir=None: _synthetic_linked_inputs())
    summary = run_empirical_calibration_pipeline(linked_dir="synthetic-linked-fixture")

    assert summary.available is True
    assert isinstance(summary.in_sample_score, float)
    assert summary.in_sample_score != float("inf")
    assert summary.holdout_score is None or summary.holdout_score >= 0
    assert summary.source_monthly == "linked-nz-monthly-observations.csv"
    assert summary.source_geographic == "linked-nz-geographic-observations.csv"
    assert summary.source_equity == "linked-nz-equity-observations.csv"
    assert summary.source_shock == "linked-nz-known-shocks.csv"

    assert summary.parameter_estimates
    assert summary.parameter_bounds

    validation_names = {item.name for item in summary.validation}
    assert validation_names == {
        "baseline_fit",
        "temporal_holdout",
        "geographic",
        "equity",
        "known_shock",
    }
    assert {item.status for item in summary.validation} == {"passed"}

    assert "marginal_supply_response" in summary.parameter_estimates
    assert summary.parameter_estimates["marginal_supply_response"] > 0
    assert "base_public_cost" not in summary.parameter_estimates

    for value in summary.parameter_bounds.values():
        lo, hi = value
        assert lo <= hi
        assert isinstance(lo, float)
        assert isinstance(hi, float)


def test_build_claim_boundary_text_supports_boundary_states():
    missing = build_claim_boundary_text(None)
    unavailable = build_claim_boundary_text(_unsupported_summary(True, available=False))
    partial = build_claim_boundary_text(_unsupported_summary(available=True, supported_where_valid=False))
    supported = build_claim_boundary_text(_unsupported_summary(available=True, supported_where_valid=True))

    assert "not linked-data calibrated" in missing
    assert "not linked-data calibrated" in unavailable
    assert "only empirically supported where valid" in partial
    assert "empirically supported benchmark where valid" in supported
    assert "Published aggregate calibration checks" in supported
    assert "Linked-data calibration" not in supported
    assert "not a patient-level forecast" in supported
