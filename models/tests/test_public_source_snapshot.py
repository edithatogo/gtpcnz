from __future__ import annotations

from pathlib import Path

from models.primarycare_model.data.public_source_snapshot import (
    build_snapshot,
    sha256_many,
    verify_public_source_readiness,
)

ROOT = Path(__file__).resolve().parents[2]


def test_public_source_snapshot_is_valid() -> None:
    snapshot = build_snapshot()
    assert snapshot.sources
    assert len(snapshot.source_registry_sha256) == 64
    assert all(source.public_access_status == "public" for source in snapshot.sources)


def test_default_public_source_readiness_allows_pending_downloads() -> None:
    assert verify_public_source_readiness() == ()


def test_strict_public_source_readiness_passes_with_downloaded_processed_artifacts() -> None:
    assert verify_public_source_readiness(verify_files=True, verify_checksums=True, verify_processed=True) == ()


def test_public_source_multi_file_checksum_is_deterministic() -> None:
    first = ROOT / "data" / "public_raw" / "README.md"
    second = ROOT / "data" / "public_processed" / "README.md"

    assert sha256_many((first, second)) == sha256_many((first, second))
    assert sha256_many((first, second)) != sha256_many((second, first))
