"""Shared public aggregate calibration target loading and prediction helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.calibration_targets import CalibrationTarget
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
