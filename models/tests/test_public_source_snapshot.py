from __future__ import annotations

from models.primarycare_model.data.public_source_snapshot import build_snapshot


def test_public_source_snapshot_is_valid() -> None:
    snapshot = build_snapshot()
    assert snapshot.sources
    assert len(snapshot.source_registry_sha256) == 64
    assert all(source.public_access_status == "public" for source in snapshot.sources)
