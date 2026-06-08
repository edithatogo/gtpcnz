"""Public-source readiness matrix across retrieval, fetch, transform, and processed outputs."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from models.primarycare_model.data.public_source_fetch import check_source_fetch_readiness
from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_snapshot import (
    ROOT,
    load_public_sources,
    sha256_many,
    source_files,
    source_processed_dir,
    source_raw_dir,
)
from models.primarycare_model.data.public_source_transforms import check_source_transform_readiness


@dataclass(frozen=True)
class PublicSourceReadinessRow:
    source_id: str
    retrieval_status: str
    fetch_status: str
    transform_status: str
    raw_artifact_status: str
    checksum_status: str
    processed_artifact_status: str
    calibration_claim_status: str
    source_ready: bool
    issues: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def _processed_artifact_path(expected_processed_artifact: str) -> Path:
    return ROOT / expected_processed_artifact


def _raw_artifact_status(source_id: str, expected_raw_artifact: str) -> tuple[str, tuple[str, ...]]:
    raw_dir = source_raw_dir(source_id)
    raw_files = source_files(raw_dir)
    expected_path = raw_dir / expected_raw_artifact
    issues: list[str] = []
    if expected_path.exists():
        return "expected_raw_artifact_present", ()
    if raw_files:
        issues.append(f"{source_id}: raw files exist but expected artifact {expected_path.relative_to(ROOT).as_posix()} is missing")
        return "raw_files_present_expected_artifact_missing", tuple(issues)
    return "pending_download", (f"{source_id}: no raw public source files under {raw_dir.relative_to(ROOT).as_posix()}",)


def _checksum_status(source_id: str, registry_checksum: str) -> tuple[str, tuple[str, ...]]:
    raw_files = source_files(source_raw_dir(source_id))
    if registry_checksum == "pending-download":
        return "pending_download", (f"{source_id}: checksum is pending-download",)
    if not raw_files:
        return "blocked_no_raw_files", (f"{source_id}: cannot verify checksum because no raw files exist",)
    actual = sha256_many(raw_files)
    if actual != registry_checksum:
        return "mismatch", (f"{source_id}: raw file checksum does not match registry checksum",)
    return "verified", ()


def _processed_artifact_status(source_id: str, expected_processed_artifact: str) -> tuple[str, tuple[str, ...]]:
    processed_dir = source_processed_dir(source_id)
    processed_files = source_files(processed_dir)
    expected_path = _processed_artifact_path(expected_processed_artifact)
    issues: list[str] = []
    if expected_path.exists():
        return "expected_processed_artifact_present", ()
    if processed_files:
        issues.append(
            f"{source_id}: processed files exist but expected artifact "
            f"{expected_path.relative_to(ROOT).as_posix()} is missing"
        )
        return "processed_files_present_expected_artifact_missing", tuple(issues)
    return "pending_transform", (f"{source_id}: no processed public source files under {processed_dir.relative_to(ROOT).as_posix()}",)


def build_public_source_readiness_matrix(*, strict: bool = False) -> tuple[PublicSourceReadinessRow, ...]:
    """Return one readiness row per public source without mutating claim status."""

    sources = {source.source_id: source for source in load_public_sources()}
    rows: list[PublicSourceReadinessRow] = []
    for plan in load_public_source_retrieval_plans():
        source = sources[plan.source_id]
        fetch = check_source_fetch_readiness(plan.source_id, require_raw=strict)
        transform = check_source_transform_readiness(plan.source_id, require_raw=strict)
        raw_status, raw_issues = _raw_artifact_status(plan.source_id, plan.expected_raw_artifact)
        checksum_status, checksum_issues = _checksum_status(plan.source_id, source.checksum)
        processed_status, processed_issues = _processed_artifact_status(plan.source_id, plan.expected_processed_artifact)

        readiness_issues: list[str] = []
        if strict:
            readiness_issues.extend(fetch.issues)
            readiness_issues.extend(transform.issues)
            readiness_issues.extend(raw_issues)
            readiness_issues.extend(checksum_issues)
            readiness_issues.extend(processed_issues)

        source_ready = (
            plan.retrieval_status == "processed_ready"
            and raw_status == "expected_raw_artifact_present"
            and checksum_status == "verified"
            and processed_status == "expected_processed_artifact_present"
        )
        calibration_claim_status = "public_aggregate_source_ready" if source_ready else "calibration_readiness_only"
        rows.append(
            PublicSourceReadinessRow(
                source_id=plan.source_id,
                retrieval_status=plan.retrieval_status,
                fetch_status=fetch.status,
                transform_status=transform.status,
                raw_artifact_status=raw_status,
                checksum_status=checksum_status,
                processed_artifact_status=processed_status,
                calibration_claim_status=calibration_claim_status,
                source_ready=source_ready,
                issues=tuple(dict.fromkeys(readiness_issues)),
            )
        )
    return tuple(rows)


def strict_readiness_issues() -> tuple[str, ...]:
    issues: list[str] = []
    for row in build_public_source_readiness_matrix(strict=True):
        if not row.source_ready:
            issues.append(f"{row.source_id}: source_ready=false; calibration remains calibration_readiness_only")
        issues.extend(row.issues)
    return tuple(dict.fromkeys(issues))


def readiness_matrix_as_json(*, strict: bool = False) -> str:
    rows = build_public_source_readiness_matrix(strict=strict)
    payload = {
        "claim_boundary": "public benchmark only until raw, checksum, transform, processed, and calibration gates pass",
        "rows": [row.to_json_dict() for row in rows],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report public-source readiness across retrieval, fetch, transform, and processed outputs.")
    parser.add_argument("--strict", action="store_true", help="Fail until every source has raw, checksum, and processed artifacts.")
    parser.add_argument("--json", action="store_true", help="Print the readiness matrix as JSON.")
    args = parser.parse_args(argv)

    if args.json:
        print(readiness_matrix_as_json(strict=args.strict))
    else:
        for row in build_public_source_readiness_matrix(strict=args.strict):
            print(
                f"{row.source_id}: retrieval={row.retrieval_status}; fetch={row.fetch_status}; "
                f"transform={row.transform_status}; raw={row.raw_artifact_status}; "
                f"checksum={row.checksum_status}; processed={row.processed_artifact_status}; "
                f"claim={row.calibration_claim_status}"
            )

    if args.strict:
        issues = strict_readiness_issues()
        if issues:
            print("\n".join(issues), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
