"""Registry-driven public source transform entrypoints."""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

from models.primarycare_model.contracts.public_sources import PublicSourceRetrievalPlan
from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_snapshot import (
    ROOT,
    processed_artifact_sha256,
    sha256_file,
    source_files,
)

TRANSFORMABLE_STATUSES = {"downloaded_pending_transform", "processed_ready"}


@dataclass(frozen=True)
class TransformReadinessResult:
    source_id: str
    transform_script: str
    status: str
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class TransformOutput:
    source_id: str
    artifact: Path
    rows_written: int
    status: str


XLSX_NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


class _TableAndLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self.links: list[tuple[str, str]] = []
        self._table_stack: list[list[list[str]]] = []
        self._row: list[str] | None = None
        self._cell_parts: list[str] | None = None
        self._link_href: str | None = None
        self._link_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name: value or "" for name, value in attrs}
        if tag == "table":
            self._table_stack.append([])
        elif tag == "tr" and self._table_stack:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell_parts = []
        elif tag == "a":
            self._link_href = attrs_dict.get("href")
            self._link_parts = []

    def handle_data(self, data: str) -> None:
        if self._cell_parts is not None:
            self._cell_parts.append(data)
        if self._link_parts is not None:
            self._link_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._cell_parts is not None and self._row is not None:
            self._row.append(_clean_text(" ".join(self._cell_parts)))
            self._cell_parts = None
        elif tag == "tr" and self._row is not None and self._table_stack:
            if any(cell for cell in self._row):
                self._table_stack[-1].append(self._row)
            self._row = None
        elif tag == "table" and self._table_stack:
            table = self._table_stack.pop()
            if table:
                self.tables.append(table)
        elif tag == "a" and self._link_parts is not None:
            text = _clean_text(" ".join(self._link_parts))
            if self._link_href and text:
                self.links.append((text, self._link_href))
            self._link_href = None
            self._link_parts = None


def transform_script_path(script_path: str) -> Path:
    return ROOT / script_path


def _sha256(path: Path) -> str:
    return sha256_file(path)


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    path.with_suffix(path.suffix + ".hash").write_text(processed_artifact_sha256(path) + "\n", encoding="utf-8")


def _write_metadata(path: Path, *, source_id: str, raw_artifact: Path, rows_written: int, note: str) -> None:
    metadata = "\n".join(
        (
            f"source_id: {source_id}",
            f"processed_artifact: {_relative(path)}",
            f"raw_artifact: {_relative(raw_artifact)}",
            f"raw_artifact_sha256: {_sha256(raw_artifact)}",
            f"rows_written: {rows_written}",
            "claim_level: public_benchmark",
            "calibration_status: calibration_readiness_only",
            "not_valid_for: patient-level, private administrative, confidential, stakeholder, or causal forecast use",
            f"transform_note: {note}",
            "",
        )
    )
    metadata_path = path.parent / "_metadata.yaml"
    metadata_path.write_text(metadata, encoding="utf-8")
    metadata_path.with_suffix(metadata_path.suffix + ".hash").write_text(
        processed_artifact_sha256(metadata_path) + "\n", encoding="utf-8"
    )


def _parse_html(path: Path) -> _TableAndLinkParser:
    parser = _TableAndLinkParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def _select_raw_artifact(plan: PublicSourceRetrievalPlan) -> Path:
    raw_dir = ROOT / plan.expected_raw_dir
    expected = raw_dir / plan.expected_raw_artifact
    if expected.exists():
        return expected
    files = tuple(path for path in source_files(raw_dir) if not path.name.endswith(".fetch.json"))
    if not files:
        raise FileNotFoundError(f"{plan.source_id}: no raw public source files under {plan.expected_raw_dir}")
    return files[0]


def _transform_statsnz_population(
    plan: PublicSourceRetrievalPlan, raw_artifact: Path, output_path: Path
) -> TransformOutput:
    text = html.unescape(raw_artifact.read_text(encoding="utf-8", errors="replace"))
    indicator = re.search(
        r'"Name":"Estimated population of NZ"[^{}]{0,1200}"Value":"([0-9,]+)"[^{}]{0,300}"Period":"(\d{1,2} [A-Za-z]+ (\d{4}))"',
        text,
        flags=re.IGNORECASE,
    )
    if not indicator:
        indicator = re.search(
            r"The (?:provisional )?estimated resident population of (?:Aotearoa )?New Zealand (?:at|was) "
            r"(\d{1,2} [A-Za-z]+ (\d{4})) was ([0-9,]+)",
            text,
            flags=re.IGNORECASE,
        )
        if indicator:
            _date_text, year, count = indicator.groups()
            rows = [{"jurisdiction": "NZ", "year": int(year), "population_count": int(count.replace(",", ""))}]
        else:
            rows = []
    else:
        count, _date_text, year = indicator.groups()
        rows = [{"jurisdiction": "NZ", "year": int(year), "population_count": int(count.replace(",", ""))}]
    if not rows:
        raise ValueError("src_statsnz_population: could not parse a national aggregate population estimate")
    _write_csv(output_path, rows, ["jurisdiction", "year", "population_count"])
    _write_metadata(
        output_path,
        source_id=plan.source_id,
        raw_artifact=raw_artifact,
        rows_written=len(rows),
        note="Deterministic parse of the public Stats NZ national aggregate population estimate.",
    )
    return TransformOutput(plan.source_id, output_path, len(rows), "processed_public_aggregate")


def _transform_html_tables(plan: PublicSourceRetrievalPlan, raw_artifact: Path, output_path: Path) -> TransformOutput:
    parser = _parse_html(raw_artifact)
    rows: list[dict[str, object]] = []
    raw_hash = _sha256(raw_artifact)
    for table_index, table in enumerate(parser.tables, start=1):
        headers = tuple(table[0]) if table else ()
        for row_index, row in enumerate(table[1:] if headers else table, start=1):
            for column_index, value in enumerate(row, start=1):
                if value:
                    rows.append(
                        {
                            "source_id": plan.source_id,
                            "raw_artifact_sha256": raw_hash,
                            "table_index": table_index,
                            "row_index": row_index,
                            "column_index": column_index,
                            "column_label": headers[column_index - 1] if column_index <= len(headers) else "",
                            "cell_value": value,
                        }
                    )
    if not rows:
        rows.append(
            {
                "source_id": plan.source_id,
                "raw_artifact_sha256": raw_hash,
                "table_index": 0,
                "row_index": 0,
                "column_index": 0,
                "column_label": "no_table_found",
                "cell_value": "No tabular aggregate values were parsed from the public HTML snapshot.",
            }
        )
    _write_csv(
        output_path,
        rows,
        ["source_id", "raw_artifact_sha256", "table_index", "row_index", "column_index", "column_label", "cell_value"],
    )
    _write_metadata(
        output_path,
        source_id=plan.source_id,
        raw_artifact=raw_artifact,
        rows_written=len(rows),
        note="Public HTML table cell extraction only; not calibrated model input.",
    )
    return TransformOutput(plan.source_id, output_path, len(rows), "processed_reference_extract")


def _transform_link_inventory(plan: PublicSourceRetrievalPlan, raw_artifact: Path, output_path: Path) -> TransformOutput:
    parser = _parse_html(raw_artifact)
    raw_hash = _sha256(raw_artifact)
    rows = [
        {
            "source_id": plan.source_id,
            "raw_artifact_sha256": raw_hash,
            "link_text": text,
            "href": href,
            "transform_note": "public landing-page link inventory; not enrolment counts",
        }
        for text, href in parser.links
        if any(term in f"{text} {href}".lower() for term in ("enrol", "primary", "pho", "data"))
    ]
    if not rows:
        rows.append(
            {
                "source_id": plan.source_id,
                "raw_artifact_sha256": raw_hash,
                "link_text": "no_relevant_links_found",
                "href": "",
                "transform_note": "No aggregate enrolment table was present in the captured public landing page.",
            }
        )
    _write_csv(output_path, rows, ["source_id", "raw_artifact_sha256", "link_text", "href", "transform_note"])
    _write_metadata(
        output_path,
        source_id=plan.source_id,
        raw_artifact=raw_artifact,
        rows_written=len(rows),
        note="Public landing-page link inventory only; no enrolment counts fabricated.",
    )
    return TransformOutput(plan.source_id, output_path, len(rows), "processed_reference_extract")


def _transform_artifact_manifest(
    plan: PublicSourceRetrievalPlan, raw_artifact: Path, output_path: Path
) -> TransformOutput:
    rows = [
        {
            "source_id": plan.source_id,
            "artifact_name": raw_artifact.name,
            "artifact_sha256": _sha256(raw_artifact),
            "artifact_size_bytes": raw_artifact.stat().st_size,
            "transform_note": "raw public PDF manifest only; table extraction not implemented in this bounded transform",
        }
    ]
    _write_csv(output_path, rows, ["source_id", "artifact_name", "artifact_sha256", "artifact_size_bytes", "transform_note"])
    _write_metadata(
        output_path,
        source_id=plan.source_id,
        raw_artifact=raw_artifact,
        rows_written=len(rows),
        note="Public PDF artifact manifest only; not calibrated model input.",
    )
    return TransformOutput(plan.source_id, output_path, len(rows), "processed_reference_manifest")


def _xlsx_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(text.text or "" for text in item.findall(".//main:t", XLSX_NS))
        for item in root.findall("main:si", XLSX_NS)
    ]


def _cell_column(cell_ref: str) -> str:
    return re.sub(r"\d+", "", cell_ref)


def _column_index(column: str) -> int:
    index = 0
    for char in column:
        index = index * 26 + ord(char.upper()) - ord("A") + 1
    return index


def _cell_value(cell: ElementTree.Element, shared_strings: list[str]) -> str:
    value = cell.find("main:v", XLSX_NS)
    if value is None or value.text is None:
        return ""
    raw = value.text
    if cell.attrib.get("t") == "s":
        return shared_strings[int(raw)]
    return raw


def _worksheet_rows(
    archive: zipfile.ZipFile,
    *,
    sheet_index: int,
    shared_strings: list[str],
) -> list[dict[int, str]]:
    worksheet = ElementTree.fromstring(archive.read(f"xl/worksheets/sheet{sheet_index}.xml"))
    parsed_rows: list[dict[int, str]] = []
    for sheet_row in worksheet.findall("main:sheetData/main:row", XLSX_NS):
        row: dict[int, str] = {}
        for cell in sheet_row.findall("main:c", XLSX_NS):
            cell_ref = cell.attrib.get("r", "")
            if not cell_ref:
                continue
            row[_column_index(_cell_column(cell_ref))] = _cell_value(cell, shared_strings)
        parsed_rows.append(row)
    return parsed_rows


def _xlsx_sheet_metadata(raw_artifact: Path) -> list[dict[str, object]]:
    with zipfile.ZipFile(raw_artifact) as archive:
        workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        sheet_names = [
            str(sheet.attrib["name"])
            for sheet in workbook.findall("main:sheets/main:sheet", XLSX_NS)
        ]
        rows: list[dict[str, object]] = []
        for index, sheet_name in enumerate(sheet_names, start=1):
            worksheet_path = f"xl/worksheets/sheet{index}.xml"
            worksheet = ElementTree.fromstring(archive.read(worksheet_path))
            dimension = worksheet.find("main:dimension", XLSX_NS)
            sheet_rows = worksheet.findall("main:sheetData/main:row", XLSX_NS)
            max_columns = 0
            for sheet_row in sheet_rows:
                max_columns = max(max_columns, len(sheet_row.findall("main:c", XLSX_NS)))
            rows.append(
                {
                    "source_id": "src_hnz_pho_access_timeseries",
                    "raw_artifact_sha256": _sha256(raw_artifact),
                    "workbook_artifact": raw_artifact.name,
                    "sheet_name": sheet_name,
                    "dimension": dimension.attrib.get("ref", "") if dimension is not None else "",
                    "row_count": len(sheet_rows),
                    "max_observed_columns": max_columns,
                    "validation_use": _validation_use_for_sheet(sheet_name),
                    "claim_boundary": "public validation-source evidence only; not a passed holdout validation result",
                }
            )
    return rows


def _safe_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _pho_group_columns(sheet_name: str) -> tuple[tuple[str, int, int, int], ...]:
    if sheet_name == "Ethnicity":
        return (
            ("Total", 2, 3, 4),
            ("Māori", 5, 6, 7),
            ("Pacific", 8, 9, 10),
            ("Asian", 11, 12, 13),
            ("Other", 14, 15, 16),
        )
    if sheet_name == "Gender":
        return (("Total", 2, 3, 4), ("Female", 5, 6, 7), ("Male", 8, 9, 10))
    if sheet_name == "Age":
        return (
            ("Total", 2, 3, 4),
            ("0 - 4 Year Olds", 5, 6, 7),
            ("5 - 14 Year Olds", 8, 9, 10),
            ("15 - 24 Year Olds", 11, 12, 13),
            ("25 - 44 Year Olds", 14, 15, 16),
            ("45 - 64 Year Olds", 17, 18, 19),
            ("65+ Year Olds", 20, 21, 22),
        )
    if sheet_name == "Deprivation":
        return (
            ("Total", 2, 3, 4),
            ("NZ Dep 1 - 2", 5, 6, 7),
            ("NZ Dep 3 - 4", 8, 9, 10),
            ("NZ Dep 5 - 6", 11, 12, 13),
            ("NZ Dep 7 - 8", 14, 15, 16),
            ("NZ Dep 9 - 10 (Highly Deprived)", 17, 18, 19),
        )
    return ()


def _extract_pho_access_numeric_rows(raw_artifact: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    raw_hash = _sha256(raw_artifact)
    sheet_names = ("Ethnicity", "Gender", "Age", "Deprivation")
    with zipfile.ZipFile(raw_artifact) as archive:
        shared_strings = _xlsx_shared_strings(archive)
        for sheet_index, sheet_name in enumerate(sheet_names, start=1):
            worksheet_rows = _worksheet_rows(archive, sheet_index=sheet_index, shared_strings=shared_strings)
            for worksheet_row in worksheet_rows[5:]:
                district = worksheet_row.get(1, "").strip()
                if not district:
                    continue
                for group_name, enrolled_col, population_col, rate_col in _pho_group_columns(sheet_name):
                    enrolled = _safe_float(worksheet_row.get(enrolled_col, ""))
                    population = _safe_float(worksheet_row.get(population_col, ""))
                    reported_rate = _safe_float(worksheet_row.get(rate_col, ""))
                    if enrolled is None or population is None or reported_rate is None or population <= 0:
                        continue
                    calculated_rate = enrolled / population
                    rows.append(
                        {
                            "source_id": "src_hnz_pho_access_timeseries",
                            "raw_artifact_sha256": raw_hash,
                            "workbook_artifact": raw_artifact.name,
                            "period": "2025-Q4",
                            "sheet_name": sheet_name,
                            "district": district,
                            "stratifier": sheet_name.lower(),
                            "group": group_name,
                            "enrolled_count": round(enrolled, 6),
                            "population_count": round(population, 6),
                            "reported_coverage_rate": round(reported_rate, 12),
                            "calculated_coverage_rate": round(calculated_rate, 12),
                            "absolute_rate_difference": round(abs(calculated_rate - reported_rate), 12),
                            "validation_use": _validation_use_for_sheet(sheet_name),
                            "claim_boundary": "public numeric validation extract only; not a passed model validation result",
                        }
                    )
    return rows


def _validation_use_for_sheet(sheet_name: str) -> str:
    lower = sheet_name.lower()
    if "ethnicity" in lower or "deprivation" in lower:
        return "subgroup_gradient_validation_candidate"
    if "age" in lower or "gender" in lower:
        return "subgroup_descriptive_validation_candidate"
    return "public_validation_candidate"


def _transform_hnz_pho_access_timeseries(
    plan: PublicSourceRetrievalPlan, raw_artifact: Path, output_path: Path
) -> TransformOutput:
    metadata_rows = _xlsx_sheet_metadata(raw_artifact)
    metadata_path = output_path.parent / "pho_access_workbook_metadata.csv"
    _write_csv(
        metadata_path,
        metadata_rows,
        [
            "source_id",
            "raw_artifact_sha256",
            "workbook_artifact",
            "sheet_name",
            "dimension",
            "row_count",
            "max_observed_columns",
            "validation_use",
            "claim_boundary",
        ],
    )
    rows = _extract_pho_access_numeric_rows(raw_artifact)
    _write_csv(
        output_path,
        rows,
        [
            "source_id",
            "raw_artifact_sha256",
            "workbook_artifact",
            "period",
            "sheet_name",
            "district",
            "stratifier",
            "group",
            "enrolled_count",
            "population_count",
            "reported_coverage_rate",
            "calculated_coverage_rate",
            "absolute_rate_difference",
            "validation_use",
            "claim_boundary",
        ],
    )
    _write_metadata(
        output_path,
        source_id=plan.source_id,
        raw_artifact=raw_artifact,
        rows_written=len(rows),
        note="Public Health NZ PHO access workbook numeric extract for validation evidence only; no model claim upgrade.",
    )
    return TransformOutput(plan.source_id, output_path, len(rows), "processed_validation_numeric_extract")


def _transform_nz_health_survey(
    plan: PublicSourceRetrievalPlan, raw_artifact: Path, output_path: Path
) -> TransformOutput:
    text = _clean_text(re.sub(r"<[^>]+>", " ", raw_artifact.read_text(encoding="utf-8", errors="replace")))
    match = re.search(
        r"One in six adults \((?P<percent>\d+(?:\.\d+)?)%\) reported not visiting a GP due to cost",
        text,
    )
    if match is None:
        raise ValueError("src_nz_health_survey: could not parse the public GP cost-barrier aggregate")
    rows = [
        {
            "indicator_id": "gp_cost_barrier_adults",
            "year": 2024,
            "value": f"{float(match.group('percent')) / 100.0:.3f}",
        }
    ]
    _write_csv(output_path, rows, ["indicator_id", "year", "value"])
    _write_metadata(
        output_path,
        source_id=plan.source_id,
        raw_artifact=raw_artifact,
        rows_written=len(rows),
        note="Deterministic parse of the published 2023/24 NZ Health Survey GP cost-barrier aggregate.",
    )
    return TransformOutput(plan.source_id, output_path, len(rows), "processed_public_aggregate")


def transform_public_source(source_id: str) -> TransformOutput:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans.get(source_id)
    if plan is None:
        raise ValueError(f"{source_id}: no retrieval plan")
    if plan.retrieval_status not in TRANSFORMABLE_STATUSES:
        raise ValueError(f"{source_id}: retrieval status {plan.retrieval_status} is not transformable")

    raw_artifact = _select_raw_artifact(plan)
    output_path = ROOT / plan.expected_processed_artifact
    if source_id == "src_statsnz_population":
        return _transform_statsnz_population(plan, raw_artifact, output_path)
    if source_id == "src_hnz_capitation_schedule":
        return _transform_html_tables(plan, raw_artifact, output_path)
    if source_id == "src_hnz_enrolment":
        return _transform_link_inventory(plan, raw_artifact, output_path)
    if source_id == "src_hnz_pho_access_timeseries":
        return _transform_hnz_pho_access_timeseries(plan, raw_artifact, output_path)
    if source_id == "src_nz_health_survey":
        return _transform_nz_health_survey(plan, raw_artifact, output_path)
    if source_id in {"src_mcnz_workforce", "src_pho_services_agreement"}:
        return _transform_artifact_manifest(plan, raw_artifact, output_path)
    raise ValueError(f"{source_id}: no bounded public transform is implemented")


def verify_public_source_transform_scripts() -> tuple[str, ...]:
    """Return issues for missing or misaligned transform entrypoints."""

    issues: list[str] = []
    seen: set[str] = set()
    for plan in load_public_source_retrieval_plans():
        if plan.transform_script in seen:
            issues.append(f"{plan.source_id}: duplicate transform_script {plan.transform_script}")
        seen.add(plan.transform_script)
        path = transform_script_path(plan.transform_script)
        if not path.exists():
            issues.append(f"{plan.source_id}: missing transform script {plan.transform_script}")
            continue
        text = path.read_text(encoding="utf-8")
        expected = f'run_transform_cli("{plan.source_id}"'
        if expected not in text:
            issues.append(f"{plan.source_id}: transform script is not pinned to {plan.source_id}")
    return tuple(issues)


def check_source_transform_readiness(source_id: str, *, require_raw: bool = False) -> TransformReadinessResult:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans.get(source_id)
    if plan is None:
        return TransformReadinessResult(
            source_id=source_id,
            transform_script="",
            status="unknown_source",
            issues=(f"{source_id}: no retrieval plan",),
        )

    issues: list[str] = []
    script_issues = tuple(issue for issue in verify_public_source_transform_scripts() if issue.startswith(f"{source_id}:"))
    issues.extend(script_issues)

    raw_dir = ROOT / plan.expected_raw_dir
    raw_files = source_files(raw_dir)
    if require_raw and not raw_files:
        issues.append(f"{source_id}: no raw public source files under {plan.expected_raw_dir}")
    if require_raw and plan.retrieval_status not in TRANSFORMABLE_STATUSES:
        issues.append(f"{source_id}: retrieval status {plan.retrieval_status} is not transformable")

    if issues:
        status = "blocked"
    elif (ROOT / plan.expected_processed_artifact).exists():
        status = "processed_ready"
    elif plan.retrieval_status not in TRANSFORMABLE_STATUSES:
        status = "reference_pinned_pending_download"
    elif raw_files:
        status = "raw_available_pending_source_specific_parser"
    else:
        status = "reference_pinned_pending_download"
    return TransformReadinessResult(
        source_id=source_id,
        transform_script=plan.transform_script,
        status=status,
        issues=tuple(issues),
    )


def run_transform_cli(source_id: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Run or check public transform readiness for {source_id}.")
    parser.add_argument("--check-only", action="store_true", help="Check transform readiness without writing outputs.")
    parser.add_argument("--require-raw", action="store_true", help="Fail until the expected raw public files exist.")
    args = parser.parse_args(argv)

    result = check_source_transform_readiness(source_id, require_raw=args.require_raw)
    if result.issues:
        print("\n".join(result.issues))
        return 1
    if not args.check_only:
        try:
            output = transform_public_source(source_id)
        except (FileNotFoundError, ValueError) as exc:
            print(str(exc))
            return 1
        print(f"{source_id} transform wrote {_relative(output.artifact)} rows={output.rows_written} status={output.status}")
        return 0
    print(f"{source_id} transform readiness: {result.status}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate public source transform script registry coverage.")
    parser.add_argument("--require-raw", action="store_true", help="Also require raw files for every transform source.")
    args = parser.parse_args(argv)

    issues = list(verify_public_source_transform_scripts())
    if args.require_raw:
        for plan in load_public_source_retrieval_plans():
            issues.extend(check_source_transform_readiness(plan.source_id, require_raw=True).issues)
    if issues:
        print("\n".join(dict.fromkeys(issues)))
        return 1
    print("public source transform script contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
