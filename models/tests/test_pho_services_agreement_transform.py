from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from models.primarycare_model.calibration.public_policy_shock_plausibility import (
    build_public_policy_shock_evidence,
    policy_shock_gate_status,
)
from models.primarycare_model.data.public_source_transforms import (
    transform_public_source,
)

ROOT = Path(__file__).resolve().parents[2]
RAW_ARTIFACT = (
    ROOT
    / "data"
    / "public_raw"
    / "src_pho_services_agreement"
    / "master-pho-services-agreement.pdf"
)
PROCESSED_ARTIFACT = (
    ROOT
    / "data"
    / "public_processed"
    / "src_pho_services_agreement"
    / "pho_services_schedule.csv"
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_checked_in_pho_services_artifact_is_not_pdf() -> None:
    data = RAW_ARTIFACT.read_bytes()

    assert data.startswith(b"<!doctype html>")
    assert not data.startswith(b"%PDF")


def test_pho_services_transform_records_deterministic_blocker() -> None:
    first = transform_public_source("src_pho_services_agreement")
    first_hash = PROCESSED_ARTIFACT.with_suffix(".csv.hash").read_text(encoding="utf-8")
    second = transform_public_source("src_pho_services_agreement")
    second_hash = PROCESSED_ARTIFACT.with_suffix(".csv.hash").read_text(encoding="utf-8")
    rows = _read_csv(PROCESSED_ARTIFACT)

    assert first.rows_written == second.rows_written == 1
    assert first_hash == second_hash
    assert rows[0]["extraction_status"] == "extraction_blocked"
    assert rows[0]["artifact_media_type"] == "text/html"
    assert "expected PDF" in rows[0]["blocker_reason"]
    assert "no causal" in rows[0]["claim_boundary"]


def test_pho_services_transform_cli_writes_blocker_artifact() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/transform_pho_agreement.py"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "status=processed_reference_blocker" in result.stdout


def test_pho_services_reference_row_does_not_affect_policy_shock_gate() -> None:
    rows = build_public_policy_shock_evidence()
    pho_rows = [row for row in rows if row.source_id == "src_pho_services_agreement"]

    assert policy_shock_gate_status() == "passed"
    assert {row.gate_role for row in pho_rows} == {"reference_only"}
    assert {row.comparison_status for row in pho_rows} == {"readiness_only"}
    assert {row.numeric_comparison_readiness.status for row in pho_rows} == {"artifact_not_registered"}
