"""Load the public-only parameter registry."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.public_parameters import PublicParameterDefinition

REGISTRY_ROOT = Path(__file__).resolve().parents[1] / "registries" / "public"


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return _lists_to_tuples(yaml.safe_load(handle))


@lru_cache(maxsize=1)
def load_public_parameters() -> tuple[PublicParameterDefinition, ...]:
    payload = _read_yaml(REGISTRY_ROOT / "parameters.public.v1.yaml")
    parameters = TypeAdapter(tuple[PublicParameterDefinition, ...]).validate_python(payload["parameters"])
    ids = [item.parameter_id for item in parameters]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate public parameter_id")
    return parameters


def public_parameter_defaults() -> dict[str, int | float | bool | str]:
    return {item.parameter_id: item.default_value for item in load_public_parameters()}
