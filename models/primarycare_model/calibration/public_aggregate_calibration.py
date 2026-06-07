"""Transparent public aggregate calibration checks."""

from __future__ import annotations

from models.primarycare_model.calibration.public_aggregate_targets import (
    load_calibration_targets,
    predicted_public_value,
)
from models.primarycare_model.data.public_source_snapshot import load_public_sources


def run_public_aggregate_calibration() -> dict[str, object]:
    from models.primarycare_model.calibration.calibration_validation_gates import (
        build_calibration_validation_gate_matrix,
    )
    from models.primarycare_model.calibration.posterior_predictive_checks import (
        posterior_predictive_checks,
    )

    checks = []
    sources = {source.source_id: source for source in load_public_sources()}
    for target in load_calibration_targets():
        predicted = predicted_public_value(target)
        denom = abs(target.observed_value) or 1.0
        relative_error = abs(predicted - target.observed_value) / denom
        source = sources.get(target.source_id)
        source_ready = source is not None and source.checksum != "pending-download"
        passed = relative_error <= target.tolerance and source_ready
        checks.append({
            "target_id": target.target_id,
            "target_family": target.target_family,
            "observed_value": target.observed_value,
            "predicted_value": predicted,
            "relative_error": round(relative_error, 6),
            "tolerance": target.tolerance,
            "source_ready": source_ready,
            "passed": passed,
            "claim_boundary": target.claim_boundary,
        })
    all_passed = all(item["passed"] for item in checks)
    validation_gates = [row.to_json_dict() for row in build_calibration_validation_gate_matrix(strict=False)]
    posterior_predictive = posterior_predictive_checks(strict=False)
    return {
        "calibration_status": "public_aggregate_validated" if all_passed else "calibration_readiness_only",
        "claim_level": "empirically_supported_if_gated" if all_passed else "public_benchmark",
        "checks": checks,
        "validation_gates": validation_gates,
        "posterior_predictive_checks": posterior_predictive,
        "interpretation_note": (
            "Public aggregate calibration remains readiness-only until source-ready public targets, "
            "validation gates, and posterior predictive checks pass."
        ),
        "not_valid_for": [
            "precise fiscal savings",
            "ED reductions",
            "hospital-demand reductions",
            "workforce effects",
            "implementation impacts",
            "causal effects",
        ],
    }
