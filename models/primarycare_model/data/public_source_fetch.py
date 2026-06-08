"""Registry-driven public source fetch entrypoint checks."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from http.client import HTTPResponse
from pathlib import Path
from typing import BinaryIO
from urllib.parse import urlparse

from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_snapshot import ROOT, source_files, source_raw_dir

MAX_PUBLIC_SOURCE_BYTES = 75 * 1024 * 1024
PUBLIC_URL_SCHEMES = {"http", "https"}


@dataclass(frozen=True)
class FetchReadinessResult:
    source_id: str
    fetch_script: str
    target_url: str
    expected_raw_path: Path
    status: str
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


class PublicSourceFetchError(RuntimeError):
    """Raised when a public source cannot be fetched without weakening boundaries."""


def fetch_script_path(script_path: str) -> Path:
    return ROOT / script_path


def expected_raw_artifact_path(source_id: str) -> Path:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans[source_id]
    return ROOT / plan.expected_raw_dir / plan.expected_raw_artifact


def expected_fetch_metadata_path(source_id: str) -> Path:
    return expected_raw_artifact_path(source_id).with_suffix(expected_raw_artifact_path(source_id).suffix + ".fetch.json")


def verify_public_source_fetch_scripts() -> tuple[str, ...]:
    """Return issues for missing or misaligned fetch entrypoints."""

    issues: list[str] = []
    seen: set[str] = set()
    for plan in load_public_source_retrieval_plans():
        if plan.fetch_script in seen:
            issues.append(f"{plan.source_id}: duplicate fetch_script {plan.fetch_script}")
        seen.add(plan.fetch_script)
        path = fetch_script_path(plan.fetch_script)
        if not path.exists():
            issues.append(f"{plan.source_id}: missing fetch script {plan.fetch_script}")
            continue
        text = path.read_text(encoding="utf-8")
        expected = f'run_fetch_cli("{plan.source_id}"'
        if expected not in text:
            issues.append(f"{plan.source_id}: fetch script is not pinned to {plan.source_id}")
    return tuple(issues)


def _validate_public_download_target(source_id: str) -> None:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans[source_id]
    target_url = plan.download_url or plan.landing_page_url
    parsed = urlparse(target_url)
    if parsed.scheme not in PUBLIC_URL_SCHEMES or not parsed.netloc:
        raise PublicSourceFetchError(f"{source_id}: fetch target must be an absolute public HTTP(S) URL")
    if plan.public_access_status not in {"public", "published", "open"}:
        raise PublicSourceFetchError(f"{source_id}: public_access_status does not permit public fetch")
    if plan.licence_basis not in {"open", "public_reference", "open_or_public_reference"}:
        raise PublicSourceFetchError(f"{source_id}: licence_basis does not permit public fetch")
    if plan.expected_raw_artifact.endswith(".csv") and not target_url.lower().endswith(".csv"):
        raise PublicSourceFetchError(
            f"{source_id}: expected CSV artifact requires a source-specific public export URL; "
            "the pinned URL is an interactive/reference page"
        )


def _read_bounded_response(response: HTTPResponse | BinaryIO, *, limit_bytes: int = MAX_PUBLIC_SOURCE_BYTES) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > limit_bytes:
            raise PublicSourceFetchError(f"download exceeded {limit_bytes} byte safety limit")
        chunks.append(chunk)
    data = b"".join(chunks)
    if not data:
        raise PublicSourceFetchError("download returned an empty response")
    return data


def check_source_fetch_readiness(source_id: str, *, require_raw: bool = False) -> FetchReadinessResult:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans.get(source_id)
    if plan is None:
        return FetchReadinessResult(
            source_id=source_id,
            fetch_script="",
            target_url="",
            expected_raw_path=ROOT / "data" / "public_raw" / source_id,
            status="unknown_source",
            issues=(f"{source_id}: no retrieval plan",),
        )

    issues: list[str] = []
    script_issues = tuple(issue for issue in verify_public_source_fetch_scripts() if issue.startswith(f"{source_id}:"))
    issues.extend(script_issues)

    target_url = plan.download_url or plan.landing_page_url
    expected_path = ROOT / plan.expected_raw_dir / plan.expected_raw_artifact
    raw_files = source_files(source_raw_dir(source_id))
    if require_raw and not raw_files:
        issues.append(f"{source_id}: no raw public source files under {plan.expected_raw_dir}")
    if require_raw and not expected_path.exists():
        issues.append(f"{source_id}: expected raw artifact missing at {expected_path.relative_to(ROOT).as_posix()}")
    try:
        _validate_public_download_target(source_id)
    except PublicSourceFetchError as exc:
        issues.append(str(exc))

    if issues:
        status = "blocked"
    elif raw_files:
        status = "raw_available_pending_checksum_verification"
    else:
        status = "reference_pinned_pending_download"
    return FetchReadinessResult(
        source_id=source_id,
        fetch_script=plan.fetch_script,
        target_url=target_url,
        expected_raw_path=expected_path,
        status=status,
        issues=tuple(issues),
    )


def download_public_source(source_id: str) -> Path:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans[source_id]
    _validate_public_download_target(source_id)
    target_url = plan.download_url or plan.landing_page_url
    output_path = ROOT / plan.expected_raw_dir / plan.expected_raw_artifact
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(target_url, headers={"User-Agent": "gtpcnz-public-source-fetch/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = _read_bounded_response(response)
    output_path.write_bytes(data)
    metadata = {
        "source_id": source_id,
        "target_url": target_url,
        "landing_page_url": plan.landing_page_url,
        "download_url": plan.download_url,
        "expected_raw_artifact": plan.expected_raw_artifact,
        "retrieved_at": datetime.now(UTC).isoformat(),
        "retrieval_method": plan.retrieval_method,
        "public_access_status": plan.public_access_status,
        "licence_basis": plan.licence_basis,
        "claim_boundary": plan.claim_boundary,
        "not_valid_for": "private administrative, confidential, patient-level, stakeholder, or calibration-claim use",
    }
    expected_fetch_metadata_path(source_id).write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def run_fetch_cli(source_id: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Fetch or check public source readiness for {source_id}.")
    parser.add_argument("--check-only", action="store_true", help="Check fetch readiness without network access or writes.")
    parser.add_argument("--require-raw", action="store_true", help="Fail until the expected raw public file exists.")
    parser.add_argument("--download", action="store_true", help="Download the registry-pinned public URL into data/public_raw.")
    args = parser.parse_args(argv)

    if args.download:
        output_path = download_public_source(source_id)
        print(f"{source_id} downloaded to {output_path.relative_to(ROOT).as_posix()}")
        return 0

    result = check_source_fetch_readiness(source_id, require_raw=args.require_raw)
    if result.issues:
        print("\n".join(result.issues))
        return 1
    print(f"{source_id} fetch readiness: {result.status}; target={result.target_url}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate public source fetch script registry coverage.")
    parser.add_argument("--require-raw", action="store_true", help="Also require raw files for every public source.")
    args = parser.parse_args(argv)

    issues = list(verify_public_source_fetch_scripts())
    if args.require_raw:
        for plan in load_public_source_retrieval_plans():
            issues.extend(check_source_fetch_readiness(plan.source_id, require_raw=True).issues)
    if issues:
        print("\n".join(dict.fromkeys(issues)))
        return 1
    print("public source fetch script contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
