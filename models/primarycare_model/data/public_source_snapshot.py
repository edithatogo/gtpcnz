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
PUBLIC_RAW = ROOT / "data" / "public_raw"
PUBLIC_PROCESSED = ROOT / "data" / "public_processed"
ALLOWED_LICENCE_STATUSES = {"open", "public_reference", "open_or_public_reference"}
TEXT_STABLE_PROCESSED_SUFFIXES = {".csv", ".json", ".txt", ".yaml", ".yml"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def processed_artifact_sha256(path: Path) -> str:
    """Hash processed text artifacts consistently across Windows and Linux checkouts."""

    data = path.read_bytes()
    if path.suffix.lower() in TEXT_STABLE_PROCESSED_SUFFIXES:
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


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


def source_raw_dir(source_id: str) -> Path:
    return PUBLIC_RAW / source_id


def source_processed_dir(source_id: str) -> Path:
    return PUBLIC_PROCESSED / source_id


def source_files(path: Path) -> tuple[Path, ...]:
    if not path.exists():
        return ()
    return tuple(
        sorted(
            item
            for item in path.rglob("*")
            if item.is_file() and item.name != ".gitkeep" and not item.name.endswith(".fetch.json")
        )
    )


def sha256_many(paths: tuple[Path, ...]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        try:
            path_key = path.relative_to(ROOT).as_posix()
        except ValueError:
            path_key = path.name
        digest.update(path_key.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def verify_public_source_readiness(
    *,
    verify_files: bool = False,
    verify_checksums: bool = False,
    verify_licences: bool = False,
    verify_processed: bool = False,
) -> tuple[str, ...]:
    """Return strict public-source readiness issues without mutating claim status."""

    issues: list[str] = []
    for source in load_public_sources():
        raw_files = source_files(source_raw_dir(source.source_id))
        processed_files = source_files(source_processed_dir(source.source_id))

        if source.public_access_status not in {"public", "published", "open"}:
            issues.append(f"{source.source_id}: public_access_status is not public/published/open")
        if not source.licence_status:
            issues.append(f"{source.source_id}: missing licence_status")

        if verify_licences and source.licence_status not in ALLOWED_LICENCE_STATUSES:
            issues.append(f"{source.source_id}: licence_status {source.licence_status!r} is not allowed")
        if verify_files and not raw_files:
            issues.append(f"{source.source_id}: no raw public source files under {source_raw_dir(source.source_id).relative_to(ROOT)}")
        if verify_checksums:
            if source.checksum == "pending-download":
                issues.append(f"{source.source_id}: checksum is pending-download")
            elif not raw_files:
                issues.append(f"{source.source_id}: cannot verify checksum because no raw files exist")
            elif sha256_many(raw_files) != source.checksum:
                issues.append(f"{source.source_id}: raw file checksum does not match registry checksum")
        if verify_processed:
            if not processed_files:
                issues.append(
                    f"{source.source_id}: no processed public source files under "
                    f"{source_processed_dir(source.source_id).relative_to(ROOT)}"
                )
                continue
            hash_files = tuple(path for path in processed_files if path.suffix == ".hash")
            data_files = tuple(path for path in processed_files if path.suffix != ".hash")
            if not data_files:
                issues.append(f"{source.source_id}: processed directory has no data files")
            for data_file in data_files:
                hash_file = data_file.with_suffix(data_file.suffix + ".hash")
                if not hash_file.exists():
                    issues.append(f"{source.source_id}: missing processed hash file for {data_file.relative_to(ROOT)}")
                    continue
                expected = hash_file.read_text(encoding="utf-8").strip()
                actual = processed_artifact_sha256(data_file)
                if expected != actual:
                    issues.append(f"{source.source_id}: processed hash mismatch for {data_file.relative_to(ROOT)}")
            orphan_hashes = tuple(path for path in hash_files if not path.with_suffix("").exists())
            for hash_file in orphan_hashes:
                issues.append(f"{source.source_id}: orphan processed hash file {hash_file.relative_to(ROOT)}")
    return tuple(issues)
