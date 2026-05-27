"""Load and strictly validate versioned model registries."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.scenarios import EducationalLeverDefinition, RuntimeScenarioDefinition

REGISTRY_ROOT = Path(__file__).resolve().parents[1] / "registries"


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _registry_path(name: str) -> Path:
    path = REGISTRY_ROOT / name
    if not path.exists():
        raise FileNotFoundError(f"Missing registry: {path}")
    return path


@lru_cache(maxsize=1)
def load_educational_levers_registry() -> tuple[EducationalLeverDefinition, ...]:
    payload = _read_yaml(_registry_path("educational_levers.v1.yaml"))
    levers = TypeAdapter(tuple[EducationalLeverDefinition, ...]).validate_python(payload["levers"])
    field_names = [lever.field_name for lever in levers]
    if len(field_names) != len(set(field_names)):
        raise ValueError("Duplicate educational lever field_name in registry")
    return levers


load_toy_levers_registry = load_educational_levers_registry


@lru_cache(maxsize=1)
def load_runtime_scenarios_registry() -> tuple[RuntimeScenarioDefinition, ...]:
    payload = _read_yaml(_registry_path("scenarios.v1.yaml"))
    scenarios = TypeAdapter(tuple[RuntimeScenarioDefinition, ...]).validate_python(payload["scenarios"])
    scenario_ids = [scenario.scenario_id for scenario in scenarios]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("Duplicate scenario_id in registry")
    return scenarios


def educational_lever_defaults() -> dict[str, int]:
    return {lever.field_name: lever.default_value for lever in load_educational_levers_registry()}


toy_lever_defaults = educational_lever_defaults


def export_registry_json_schemas() -> dict[str, dict[str, Any]]:
    return {
        "educational_lever": EducationalLeverDefinition.model_json_schema(),
        "toy_lever": EducationalLeverDefinition.model_json_schema(),
        "runtime_scenario": RuntimeScenarioDefinition.model_json_schema(),
    }
