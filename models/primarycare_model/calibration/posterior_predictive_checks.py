"""Posterior predictive check scaffold for public aggregate targets."""

from __future__ import annotations

from models.primarycare_model.calibration.public_aggregate_calibration import run_public_aggregate_calibration


def posterior_predictive_checks() -> dict[str, object]:
    result = run_public_aggregate_calibration()
    checks = result["checks"]
    failed = [item["target_id"] for item in checks if not item["passed"]]
    return {
        "ppc_status": "passed" if not failed else "not_ready",
        "failed_targets": failed,
        "interpretation_note": "Public aggregate PPCs downgrade claims when any public target falls outside tolerance.",
    }
