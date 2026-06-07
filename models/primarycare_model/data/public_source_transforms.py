"""Registry-driven public source transform entrypoint checks."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_snapshot import ROOT, source_files


@dataclass(frozen=True)
class TransformReadinessResult:
    source_id: str
    transform_script: str
    status: str
    issues: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


def transform_script_path(script_path: str) -> Path:
    return ROOT / script_path


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

    if issues:
        status = "blocked"
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
    parser = argparse.ArgumentParser(description=f"Check public transform readiness for {source_id}.")
    parser.add_argument("--check-only", action="store_true", help="Check transform readiness without writing outputs.")
    parser.add_argument("--require-raw", action="store_true", help="Fail until the expected raw public files exist.")
    args = parser.parse_args(argv)

    result = check_source_transform_readiness(source_id, require_raw=args.require_raw)
    if result.issues:
        print("\n".join(result.issues))
        return 1
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