from __future__ import annotations

from pathlib import Path

import yaml

from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
)
from models.primarycare_model.calibration.public_aggregate_calibration import (
    run_public_aggregate_calibration,
)
from models.primarycare_model.contracts.public_sources import PublicSource
from models.primarycare_model.data.public_source_readiness_matrix import (
    build_public_source_readiness_matrix,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DOC = ROOT / "docs" / "model" / "public-source-calibration-evidence-v1.md"
CLOSEOUT_DOC = ROOT / "docs" / "model" / "public-source-readiness-closeout-v1.md"
SOURCES = ROOT / "models" / "primarycare_model" / "registries" / "public" / "sources.public.v1.yaml"


def test_public_sources_have_verified_non_placeholder_checksums() -> None:
    payload = yaml.safe_load(SOURCES.read_text(encoding="utf-8"))
    for item in payload["sources"]:
        item["retrieval_date"] = str(item["retrieval_date"])
    sources = [PublicSource.model_validate(item) for item in payload["sources"]]

    assert len(sources) >= 6
    for source in sources:
        assert source.public_access_status == "public"
        assert source.checksum != "pending-download"
        assert len(source.checksum) == 64


def test_public_source_readiness_matrix_is_source_ready_but_not_claim_expanding() -> None:
    rows = build_public_source_readiness_matrix(strict=True)

    assert len(rows) >= 6
    assert all(row.source_ready for row in rows)
    assert {row.calibration_claim_status for row in rows} == {"public_aggregate_source_ready"}


def test_calibration_evidence_keeps_readiness_only_claim_boundary() -> None:
    payload = run_public_aggregate_calibration()

    assert payload["calibration_status"] == "calibration_readiness_only"
    assert payload["claim_level"] == "public_benchmark"
    assert all(check["source_ready"] for check in payload["checks"])
    assert all(check["passed"] for check in payload["checks"])
    assert "precise fiscal savings" in payload["not_valid_for"]


def test_validation_gates_explain_why_calibration_is_not_upgraded() -> None:
    rows = build_calibration_validation_gate_matrix(strict=False)
    statuses = {row.gate_id: row.status for row in rows}

    assert statuses["CAL-G-001"] == "passed"
    assert statuses["CAL-G-006"] == "passed"
    assert statuses["CAL-G-007"] == "passed"
    assert statuses["CAL-G-002"] == "public_data_unavailable"
    assert statuses["CAL-G-003"] == "public_validation_numeric_ready"
    assert statuses["CAL-G-004"] == "public_validation_numeric_ready"
    assert statuses["CAL-G-005"] == "public_data_unavailable"


def test_public_source_evidence_docs_do_not_contain_stale_pending_download_claims() -> None:
    for path in [SOURCE_DOC, CLOSEOUT_DOC]:
        text = path.read_text(encoding="utf-8")
        assert "0/6 files downloaded" not in text
        assert "checksum: pending-download" not in text
        assert "all 6 registered public sources" not in text.lower()
        assert "calibration_readiness_only" in text
