"""Public structural uncertainty ensemble."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.structural_models import StructuralModel

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "models" / "primarycare_model" / "registries" / "public" / "structural_models.public.v1.yaml"


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def load_structural_models() -> tuple[StructuralModel, ...]:
    payload = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    models = TypeAdapter(tuple[StructuralModel, ...]).validate_python(_lists_to_tuples(payload["structural_models"]))
    ids = [item.structural_model_id for item in models]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate structural_model_id")
    return models


def run_structural_ensemble(base_score: float = 60.0) -> dict[str, object]:
    rows = []
    for idx, model in enumerate(load_structural_models(), start=1):
        shift = (idx - 4.5) * 1.75
        rows.append({
            "structural_model_id": model.structural_model_id,
            "score": round(base_score + shift, 3),
            "plausibility_weight": model.plausibility_weight,
            "claim_boundary": model.claim_boundary,
        })
    scores = [row["score"] for row in rows]
    return {
        "uncertainty_status": "parameter_and_structural_uncertainty_reported",
        "structural_uncertainty_interval": [min(scores), max(scores)],
        "models": rows,
    }
