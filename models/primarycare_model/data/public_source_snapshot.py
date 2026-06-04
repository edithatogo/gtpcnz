"""Build and validate reproducible public-source snapshots."""

from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from models.primarycare_model.contracts.public_sources import PublicSource, PublicSourceSnapshot

ROOT = Path(__file__).resolve().parents[3]
PUBLIC_REGISTRY = ROOT / "models" / "primarycare_model" / "registries" / "public"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


def load_public_sources() -> tuple[PublicSource, ...]:
    payload = yaml.safe_load((PUBLIC_REGISTRY / "sources.public.v1.yaml").read_text(encoding="utf-8"))
    return TypeAdapter(tuple[PublicSource, ...]).validate_python(_lists_to_tuples(payload["sources"]))


def build_snapshot(snapshot_id: str = "public-snapshot-v1") -> PublicSourceSnapshot:
    return PublicSourceSnapshot(
        snapshot_id=snapshot_id,
        created_at=datetime.now(UTC).isoformat(),
        sources=load_public_sources(),
        source_registry_sha256=sha256_file(PUBLIC_REGISTRY / "sources.public.v1.yaml"),
        parameter_registry_sha256=sha256_file(PUBLIC_REGISTRY / "parameters.public.v1.yaml"),
        claim_boundary="Public/published aggregate source snapshot only; no private, confidential, or patient-level inputs.",
    )
