from __future__ import annotations

from models.primarycare_model.calibration.public_aggregate_calibration import run_public_aggregate_calibration


def test_public_aggregate_calibration_runs_and_bounds_claims() -> None:
    result = run_public_aggregate_calibration()
    assert result["calibration_status"] in {"public_aggregate_validated", "calibration_readiness_only"}
    assert "precise fiscal savings" in result["not_valid_for"]
    assert result["checks"]


def test_public_aggregate_calibration_embeds_validation_gate_summary() -> None:
    result = run_public_aggregate_calibration()
    gate_ids = {row["gate_id"] for row in result["validation_gates"]}

    assert {"CAL-G-001", "CAL-G-006", "CAL-G-007"}.issubset(gate_ids)
    assert any(row["claim_status"] == "calibration_readiness_only" for row in result["validation_gates"])
    assert result["claim_level"] == "empirically_supported_if_gated"


def test_public_aggregate_calibration_embeds_posterior_predictive_summary() -> None:
    result = run_public_aggregate_calibration()
    ppc = result["posterior_predictive_checks"]

    assert ppc["ppc_gate_id"] == "CAL-G-006"
    assert ppc["ppc_status"] == "passed"
    assert ppc["failed_targets"] == []
    assert "posterior predictive checks passed" in ppc["interpretation_note"]
    assert "not-valid-for warnings" in result["interpretation_note"]
