"""Claim grammar helpers for cockpit charts."""

from __future__ import annotations

PUBLIC_NOT_VALID_FOR = (
    "precise fiscal savings",
    "ED reductions",
    "hospital-demand reductions",
    "workforce effects",
    "implementation impacts",
    "causal effects",
)


def claim_badge_payload(claim_level: str = "public_benchmark", calibration_status: str = "calibration_readiness_only", uncertainty_type: str = "parameter_and_structural") -> dict[str, str]:
    return {
        "claim_level": claim_level,
        "calibration_status": calibration_status,
        "uncertainty_type": uncertainty_type,
        "not_valid_for_warning": "; ".join(PUBLIC_NOT_VALID_FOR),
    }
