from __future__ import annotations

import csv
from pathlib import Path

from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
    validation_gate_issues,
)
from models.primarycare_model.data.public_source_readiness_matrix import (
    build_public_source_readiness_matrix,
)

ROOT = Path(__file__).resolve().parents[2]
PHO_ACCESS_METADATA = (
    ROOT
    / "data"
    / "public_processed"
    / "src_hnz_pho_access_timeseries"
    / "pho_access_workbook_metadata.csv"
)


def test_pho_access_workbook_metadata_covers_public_subgroup_tabs() -> None:
    with PHO_ACCESS_METADATA.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))

    sheet_names = {row["sheet_name"] for row in rows}
    assert {"Ethnicity", "Deprivation"}.issubset(sheet_names)
    assert all(int(row["row_count"]) > 0 for row in rows)
    assert all(row["claim_boundary"].startswith("public validation-source evidence only") for row in rows)


def test_pho_access_source_is_ready_without_upgrading_validation_claims() -> None:
    readiness = {row.source_id: row for row in build_public_source_readiness_matrix(strict=True)}
    assert readiness["src_hnz_pho_access_timeseries"].source_ready

    gate_statuses = {row.gate_id: row.status for row in build_calibration_validation_gate_matrix(strict=True)}
    assert gate_statuses["CAL-G-003"] == "public_validation_source_registered"
    assert gate_statuses["CAL-G-004"] == "public_validation_source_registered"

    issues = validation_gate_issues(require_all_validation_data=True)
    assert any(issue.startswith("CAL-G-003") for issue in issues)
    assert any(issue.startswith("CAL-G-004") for issue in issues)
