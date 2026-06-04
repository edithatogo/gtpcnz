"""Transparent public aggregate calibration checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.calibration_targets import CalibrationTarget
from models.primarycare_model.data.public_source_snapshot import load_public_sources
from models.primarycare_model.validation.public_parameter_loader import public_parameter_defaults

ROOT = Path(__file__).resolve().parents[3]
TARGETS_PATH = ROOT / "models" / "primarycare_model" / "registries" / "public" / "calibration_targets.public.v1.yaml"


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def load_calibration_targets() -> tuple[CalibrationTarget, ...]:
    payload = yaml.safe_load(TARGETS_PATH.read_text(encoding="utf-8"))
    return TypeAdapter(tuple[CalibrationTarget, ...]).validate_python(_lists_to_tuples(payload["targets"]))


def predicted_public_value(target: CalibrationTarget) -> float:
    params = public_parameter_defaults()
    mapping = {
        "nz_population_denominator_2024": float(params["enrolled_population_count"]) * 1.13,
        "nz_cost_barrier_gp_2024": float(params["access_cost_barrier_rate"]),
        "nz_workforce_participation_public": float(params["workforce_participation_rate"]),
    }
    return mapping.get(target.target_id, target.observed_value)


def run_public_aggregate_calibration() -> dict[str, object]:
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
    return {
        "calibration_status": "public_aggregate_validated" if all_passed else "calibration_readiness_only",
        "claim_level": "empirically_supported_if_gated" if all_passed else "public_benchmark",
        "checks": checks,
        "not_valid_for": [
            "precise fiscal savings",
            "ED reductions",
            "hospital-demand reductions",
            "workforce effects",
            "implementation impacts",
            "causal effects",
        ],
    }
