from __future__ import annotations

import csv
import zipfile
from pathlib import Path

from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
    validation_gate_issues,
)
from models.primarycare_model.contracts.public_sources import PublicSourceRetrievalPlan
from models.primarycare_model.data import public_source_transforms
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
PHO_ACCESS_NUMERIC = (
    ROOT
    / "data"
    / "public_processed"
    / "src_hnz_pho_access_timeseries"
    / "pho_access_numeric_extract.csv"
)


def _sheet_xml(sheet_index: int, shared_string_count: int, *, enrolled: float, population: float) -> str:
    district_shared_index = shared_string_count - 1
    rows = [
        '<row r="1"><c r="A1" t="s"><v>0</v></c></row>',
        '<row r="2"><c r="A2" t="s"><v>0</v></c></row>',
        '<row r="3"><c r="A3" t="s"><v>0</v></c></row>',
        '<row r="4"><c r="A4" t="s"><v>0</v></c></row>',
        '<row r="5"><c r="A5" t="s"><v>0</v></c></row>',
        (
            f'<row r="6"><c r="A6" t="s"><v>{district_shared_index}</v></c>'
            f'<c r="B6"><v>{enrolled}</v></c><c r="C6"><v>{population}</v></c>'
            f'<c r="D6"><v>{enrolled / population}</v></c></row>'
        ),
    ]
    max_column = ("P", "M", "V", "U")[sheet_index - 1]
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="A1:{max_column}6"/><sheetData>{"".join(rows)}</sheetData></worksheet>'
    )


def _write_pho_access_fixture(path: Path, *, enrolled: float, population: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet_names = ("Ethnicity", "Gender", "Age", "Deprivation")
    shared_strings = ("placeholder", "Fixture District")
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<sheets>"
            + "".join(f'<sheet name="{name}" sheetId="{index}"/>' for index, name in enumerate(sheet_names, start=1))
            + "</sheets></workbook>",
        )
        archive.writestr(
            "xl/sharedStrings.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            + "".join(f"<si><t>{value}</t></si>" for value in shared_strings)
            + "</sst>",
        )
        for index, _sheet_name in enumerate(sheet_names, start=1):
            archive.writestr(
                f"xl/worksheets/sheet{index}.xml",
                _sheet_xml(index, len(shared_strings), enrolled=enrolled + index, population=population + index),
            )


def test_pho_access_workbook_metadata_covers_public_subgroup_tabs() -> None:
    with PHO_ACCESS_METADATA.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))

    sheet_names = {row["sheet_name"] for row in rows}
    assert {"Ethnicity", "Deprivation"}.issubset(sheet_names)
    assert all(int(row["row_count"]) > 0 for row in rows)
    assert all(row["claim_boundary"].startswith("public validation-source evidence only") for row in rows)


def test_pho_access_numeric_extract_covers_district_and_subgroup_rows() -> None:
    with PHO_ACCESS_NUMERIC.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))

    periods = {row["period"] for row in rows}
    assert len(rows) == 441 * len(periods)
    assert len(periods) >= 1
    assert {"ethnicity", "deprivation"}.issubset({row["stratifier"] for row in rows})
    assert {"Auckland", "Southern"}.issubset({row["district"] for row in rows})
    assert all(float(row["absolute_rate_difference"]) <= 1e-9 for row in rows)
    assert all(row["claim_boundary"].startswith("public numeric validation extract only") for row in rows)


def test_pho_access_transform_accepts_multiple_public_workbook_periods(monkeypatch) -> None:
    temp_root = Path("fixture-root")
    raw_dir = temp_root / "data" / "public_raw" / "src_hnz_pho_access_timeseries"
    processed = temp_root / "data" / "public_processed" / "src_hnz_pho_access_timeseries" / "pho_access_numeric_extract.csv"
    current = raw_dir / "access-to-primary-care-stats-2025-q4.xlsx"
    additional = raw_dir / "access-to-primary-care-stats-2025-q3.xlsx"
    written: dict[str, list[dict[str, object]]] = {}
    metadata_calls: list[tuple[Path, str]] = []
    extract_calls: list[tuple[Path, str]] = []

    def fake_metadata(workbook: Path, *, period: str | None = None) -> list[dict[str, object]]:
        metadata_calls.append((workbook, period or ""))
        return [{"workbook_artifact": workbook.name, "period": period}]

    def fake_extract(workbook: Path, *, period: str | None = None) -> list[dict[str, object]]:
        extract_calls.append((workbook, period or ""))
        return [{"workbook_artifact": workbook.name, "period": period, "absolute_rate_difference": 0.0}]

    def fake_write_csv(path: Path, rows: list[dict[str, object]], _fieldnames: list[str]) -> None:
        written[path.name] = rows

    plan = PublicSourceRetrievalPlan(
        source_id="src_hnz_pho_access_timeseries",
        landing_page_url="https://example.test/pho-access",
        download_url=None,
        expected_raw_dir="data/public_raw/src_hnz_pho_access_timeseries",
        expected_raw_artifact=current.name,
        retrieval_method="fixture",
        fetch_script="scripts/fetch_hnz_pho_access_timeseries.py",
        retrieval_status="processed_ready",
        licence_basis="public_reference",
        public_access_status="public",
        transform_script="scripts/transform_hnz_pho_access_timeseries.py",
        expected_processed_artifact="data/public_processed/src_hnz_pho_access_timeseries/pho_access_numeric_extract.csv",
        claim_boundary="fixture",
    )

    monkeypatch.setattr(public_source_transforms, "ROOT", temp_root)
    monkeypatch.setattr(public_source_transforms, "source_files", lambda _raw_dir: (current, additional))
    monkeypatch.setattr(public_source_transforms, "_xlsx_sheet_metadata", fake_metadata)
    monkeypatch.setattr(public_source_transforms, "_extract_pho_access_numeric_rows", fake_extract)
    monkeypatch.setattr(public_source_transforms, "_write_csv", fake_write_csv)
    monkeypatch.setattr(public_source_transforms, "_write_metadata", lambda *args, **kwargs: None)

    output = public_source_transforms._transform_hnz_pho_access_timeseries(plan, current, processed)

    assert output.rows_written == 2
    assert [period for _workbook, period in metadata_calls] == ["2025-Q3", "2025-Q4"]
    assert [period for _workbook, period in extract_calls] == ["2025-Q3", "2025-Q4"]
    assert {row["period"] for row in written["pho_access_numeric_extract.csv"]} == {"2025-Q3", "2025-Q4"}
    assert {row["period"] for row in written["pho_access_workbook_metadata.csv"]} == {"2025-Q3", "2025-Q4"}


def test_pho_access_source_is_ready_without_upgrading_validation_claims() -> None:
    readiness = {row.source_id: row for row in build_public_source_readiness_matrix(strict=True)}
    assert readiness["src_hnz_pho_access_timeseries"].source_ready

    gate_statuses = {row.gate_id: row.status for row in build_calibration_validation_gate_matrix(strict=True)}
    assert gate_statuses["CAL-G-003"] == "passed"
    assert gate_statuses["CAL-G-004"] == "passed"

    issues = validation_gate_issues(require_all_validation_data=True)
    assert not any(issue.startswith("CAL-G-003") for issue in issues)
    assert not any(issue.startswith("CAL-G-004") for issue in issues)
