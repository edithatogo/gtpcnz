"""Load and strictly validate versioned model registries.

Supports educational levers, runtime scenarios, model parameters and input
datasets. All loaders cache results (LRU) and validate payloads against
their Pydantic v2 contracts at load time.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.inputs import InputDataset, ProvenanceEntry
from models.primarycare_model.contracts.oia import OIAComponentEntry
from models.primarycare_model.contracts.parameters import ParameterDefinition
from models.primarycare_model.contracts.scenarios import EducationalLeverDefinition, RuntimeScenarioDefinition

REGISTRY_ROOT = Path(__file__).resolve().parents[1] / "registries"


def _check_unique(items: Iterable[Any], attr: str, label: str) -> None:
    """Check that all items have a unique value for the named attribute."""
    values = [getattr(item, attr) for item in items]
    if len(values) != len(set(values)):
        raise ValueError(f"Duplicate {attr} in {label} registry")


def _lists_to_tuples(obj: Any) -> Any:
    """Recursively convert all YAML lists to tuples for strict Pydantic validation."""
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    return _lists_to_tuples(raw)


def _registry_path(name: str) -> Path:
    path = REGISTRY_ROOT / name
    if not path.exists():
        raise FileNotFoundError(f"Missing registry: {path}")
    return path


@lru_cache(maxsize=1)
def load_educational_levers_registry() -> tuple[EducationalLeverDefinition, ...]:
    payload = _read_yaml(_registry_path("educational_levers.v1.yaml"))
    levers = TypeAdapter(tuple[EducationalLeverDefinition, ...]).validate_python(payload["levers"])
    _check_unique(levers, "field_name", "educational lever")
    return levers


load_toy_levers_registry = load_educational_levers_registry


@lru_cache(maxsize=1)
def load_runtime_scenarios_registry() -> tuple[RuntimeScenarioDefinition, ...]:
    payload = _read_yaml(_registry_path("scenarios.v1.yaml"))
    scenarios = TypeAdapter(tuple[RuntimeScenarioDefinition, ...]).validate_python(payload["scenarios"])
    _check_unique(scenarios, "scenario_id", "runtime scenario")
    return scenarios


def educational_lever_defaults() -> dict[str, int]:
    return {lever.field_name: lever.default_value for lever in load_educational_levers_registry()}


toy_lever_defaults = educational_lever_defaults


def export_registry_json_schemas() -> dict[str, dict[str, Any]]:
    """Export JSON schemas for all **existing** registry contracts.

    .. versionadded:: 0.2.0
        Use :func:`export_all_registry_json_schemas` instead for a complete
        export that includes parameters and inputs schemas.

    Returns
    -------
    dict[str, dict[str, Any]]
        Schemas keyed by short registry name.
    """
    return {
        "educational_lever": EducationalLeverDefinition.model_json_schema(),
        "toy_lever": EducationalLeverDefinition.model_json_schema(),
        "runtime_scenario": RuntimeScenarioDefinition.model_json_schema(),
    }


# ── Model parameters ──────────────────────────────────────────────────


@lru_cache(maxsize=1)
def load_parameters_registry() -> tuple[ParameterDefinition, ...]:
    """Load and validate the parameters.v1.yaml registry.

    Returns
    -------
    tuple[ParameterDefinition, ...]
        Immutable, validated tuple of parameter definitions.

    Raises
    ------
    FileNotFoundError
        If the registry file is missing.
    pydantic.ValidationError
        If any definition fails contract validation.
    ValueError
        If duplicate ``parameter_id`` values are detected.
    """
    payload = _read_yaml(_registry_path("parameters.v1.yaml"))
    params = TypeAdapter(tuple[ParameterDefinition, ...]).validate_python(payload["parameters"])
    _check_unique(params, "parameter_id", "parameter")
    return params


def parameter_defaults() -> dict[str, int | float | bool | str]:
    """Return a flat dictionary of parameter_id -> default_value."""
    return {param.parameter_id: param.default_value for param in load_parameters_registry()}


# ── Input datasets ────────────────────────────────────────────────────


@lru_cache(maxsize=1)
def load_inputs_registry() -> tuple[InputDataset, ...]:
    """Load and validate the inputs.v1.yaml registry.

    Returns
    -------
    tuple[InputDataset, ...]
        Immutable, validated tuple of input dataset definitions.

    Raises
    ------
    FileNotFoundError
        If the registry file is missing.
    pydantic.ValidationError
        If any dataset fails contract validation.
    ValueError
        If duplicate ``dataset_id`` values are detected.
    """
    payload = _read_yaml(_registry_path("inputs.v1.yaml"))
    datasets = TypeAdapter(tuple[InputDataset, ...]).validate_python(payload["datasets"])
    _check_unique(datasets, "dataset_id", "input dataset")
    return datasets


def input_dataset_defaults() -> dict[str, dict[str, Any]]:
    """Return a dictionary of dataset_id -> {field_name: required} summary."""
    return {
        ds.dataset_id: {field.field_name: field.required for field in ds.fields}
        for ds in load_inputs_registry()
    }


# ── Provenance registry ────────────────────────────────────────────────


@lru_cache(maxsize=1)
def load_provenance_registry() -> tuple[ProvenanceEntry, ...]:
    """Load and validate the provenance.v1.yaml registry.

    Returns
    -------
    tuple[ProvenanceEntry, ...]
        Immutable, validated tuple of provenance entries.

    Raises
    ------
    FileNotFoundError
        If the registry file is missing.
    pydantic.ValidationError
        If any entry fails contract validation.
    ValueError
        If duplicate ``source_id`` values are detected.
    """
    payload = _read_yaml(_registry_path("provenance.v1.yaml"))
    entries = TypeAdapter(tuple[ProvenanceEntry, ...]).validate_python(payload["provenance"])
    _check_unique(entries, "source_id", "provenance")
    return entries


def build_provenance_summary() -> dict[str, Any]:
    """Build a dashboard-ready summary of the provenance registry.

    Groups provenance entries by status and returns a dictionary with
    summary counts, a flat list of entries (sorted by ``source_id``),
    and a mapping of status to entry lists.

    Returns
    -------
    dict
        A dictionary with the following keys:

        - **total_entries** (*int*) — total number of provenance entries.
        - **status_counts** (*dict[str, int]*) — count of entries per status.
        - **entries** (*list[dict]*) — all entries as plain dicts sorted
          by ``source_id``; each dict contains ``source_id``, ``label``,
          ``source_url_or_reference``, ``retrieval_date``,
          ``transform_description``, ``status`` and ``claim_boundary``.
        - **by_status** (*dict[str, list[dict]]*) — entries grouped by
          their ``status`` value.
    """
    entries = load_provenance_registry()

    status_counts: dict[str, int] = {}
    by_status: dict[str, list[dict[str, str]]] = {}
    flat: list[dict[str, str]] = []

    for entry in sorted(entries, key=lambda e: e.source_id):
        d = {
            "source_id": entry.source_id,
            "label": entry.label,
            "source_url_or_reference": entry.source_url_or_reference,
            "retrieval_date": entry.retrieval_date,
            "transform_description": entry.transform_description,
            "status": entry.status,
            "claim_boundary": entry.claim_boundary,
        }
        flat.append(d)
        status_counts[entry.status] = status_counts.get(entry.status, 0) + 1
        by_status.setdefault(entry.status, []).append(d)

    return {
        "total_entries": len(entries),
        "status_counts": status_counts,
        "entries": flat,
        "by_status": by_status,
    }


# ── Full JSON Schema export ───────────────────────────────────────────


@lru_cache(maxsize=1)
def load_oia_component_map_registry() -> tuple[Any, ...]:
    payload = _read_yaml(_registry_path("oia_component_map.v1.yaml"))
    entries = TypeAdapter(tuple[OIAComponentEntry, ...]).validate_python(payload["entries"])
    _check_unique(entries, "oia_id", "OIA component map")
    return entries


def build_oia_component_dataframe() -> list[dict[str, str]]:
    entries = load_oia_component_map_registry()
    result = []
    for e in sorted(entries, key=lambda x: x.oia_id):
        result.append({"oia_id": e.oia_id, "topic": e.topic, "component_type": e.component_type, "component_path": e.component_path, "chart_or_table": e.chart_or_table, "impact_description": e.impact_description})
    return result


def export_all_registry_json_schemas() -> dict[str, dict[str, Any]]:
    """Export JSON schemas for **all** registry contracts.

    Includes educational levers, runtime scenarios, model parameters and
    input datasets — the full surface area for external tooling, OpenAPI
    specs or documentation generators.

    Returns
    -------
    dict[str, dict[str, Any]]
        Schemas keyed by short registry name.
    """
    return {
        "educational_lever": EducationalLeverDefinition.model_json_schema(),
        "toy_lever": EducationalLeverDefinition.model_json_schema(),
        "runtime_scenario": RuntimeScenarioDefinition.model_json_schema(),
        "parameter": ParameterDefinition.model_json_schema(),
        "input_dataset": InputDataset.model_json_schema(),
    }
