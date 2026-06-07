"""Registry-driven public source fetch entrypoint checks."""

from __future__ import annotations

import argparse
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_snapshot import ROOT, source_files, source_raw_dir


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


def fetch_script_path(script_path: str) -> Path:
    return ROOT / script_path


def expected_raw_artifact_path(source_id: str) -> Path:
    plans = {plan.source_id: plan for plan in load_public_source_retrieval_plans()}
    plan = plans[source_id]
    return ROOT / plan.expected_raw_dir / plan.expected_raw_artifact


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
    target_url = plan.download_url or plan.landing_page_url
    output_path = ROOT / plan.expected_raw_dir / plan.expected_raw_artifact
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(target_url, headers={"User-Agent": "gtpcnz-public-source-fetch/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        output_path.write_bytes(response.read())
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