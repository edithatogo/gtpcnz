"""Readiness checks for public temporal-period acquisition plans."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from models.primarycare_model.data.public_source_snapshot import PUBLIC_REGISTRY, ROOT

TEMPORAL_PERIOD_ACQUISITION_PLAN = PUBLIC_REGISTRY / "temporal_period_acquisition.public.v1.yaml"


@dataclass(frozen=True)
class MissingPublicPeriodRequirement:
    requirement_id: str
    role: str
    period_selector: str
    latest_available_period: str
    expected_raw_artifact_pattern: str
    status: str
    acquisition_method: str


@dataclass(frozen=True)
class AcquiredPublicPeriod:
    period: str
    role: str
    raw_artifact: str
    status: str


@dataclass(frozen=True)
class TemporalPeriodAcquisitionPlan:
    plan_id: str
    gate_id: str
    source_id: str
    target_id: str
    landing_page_url: str
    raw_dir: str
    processed_artifact: str
    period_column: str
    workbook_artifact_column: str
    minimum_distinct_periods: int
    required_holdout_strategy: str
    acquired_public_periods: tuple[AcquiredPublicPeriod, ...]
    missing_public_period_requirements: tuple[MissingPublicPeriodRequirement, ...]
    readiness_status: str
    claim_boundary: str


@dataclass(frozen=True)
class TemporalPeriodReadiness:
    plan_id: str
    gate_id: str
    source_id: str
    target_id: str
    status: str
    claim_status: str
    periods_available: tuple[str, ...]
    missing_public_periods: tuple[str, ...]
    missing_public_period_requirements: tuple[MissingPublicPeriodRequirement, ...]
    blockers: tuple[str, ...]
    claim_boundary: str

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["periods_available"] = list(self.periods_available)
        payload["missing_public_periods"] = list(self.missing_public_periods)
        payload["missing_public_period_requirements"] = [
            asdict(requirement) for requirement in self.missing_public_period_requirements
        ]
        payload["blockers"] = list(self.blockers)
        return payload


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def _require_repo_relative(path: str, *, field_name: str, plan_id: str) -> None:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"{plan_id}: {field_name} must be a repository-relative path")


def load_temporal_period_acquisition_plans(
    path: Path = TEMPORAL_PERIOD_ACQUISITION_PLAN,
) -> tuple[TemporalPeriodAcquisitionPlan, ...]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    plans = []
    for item in _lists_to_tuples(payload["temporal_period_acquisition_plans"]):
        acquired = tuple(AcquiredPublicPeriod(**period) for period in item["acquired_public_periods"])
        missing = tuple(
            MissingPublicPeriodRequirement(**requirement)
            for requirement in item["missing_public_period_requirements"]
        )
        plan = TemporalPeriodAcquisitionPlan(
            plan_id=str(item["plan_id"]),
            gate_id=str(item["gate_id"]),
            source_id=str(item["source_id"]),
            target_id=str(item["target_id"]),
            landing_page_url=str(item["landing_page_url"]),
            raw_dir=str(item["raw_dir"]),
            processed_artifact=str(item["processed_artifact"]),
            period_column=str(item["period_column"]),
            workbook_artifact_column=str(item["workbook_artifact_column"]),
            minimum_distinct_periods=int(item["minimum_distinct_periods"]),
            required_holdout_strategy=str(item["required_holdout_strategy"]),
            acquired_public_periods=acquired,
            missing_public_period_requirements=missing,
            readiness_status=str(item["readiness_status"]),
            claim_boundary=str(item["claim_boundary"]),
        )
        _require_repo_relative(plan.raw_dir, field_name="raw_dir", plan_id=plan.plan_id)
        _require_repo_relative(plan.processed_artifact, field_name="processed_artifact", plan_id=plan.plan_id)
        plans.append(plan)
    return tuple(plans)


def _processed_periods(plan: TemporalPeriodAcquisitionPlan) -> tuple[str, ...]:
    path = ROOT / plan.processed_artifact
    if not path.exists():
        return ()
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(sorted({row[plan.period_column] for row in csv.DictReader(handle) if row.get(plan.period_column)}))


def build_temporal_period_readiness() -> tuple[TemporalPeriodReadiness, ...]:
    rows: list[TemporalPeriodReadiness] = []
    for plan in load_temporal_period_acquisition_plans():
        periods = _processed_periods(plan)
        missing_count = max(plan.minimum_distinct_periods - len(periods), 0)
        missing_public_periods = tuple(
            requirement.period_selector for requirement in plan.missing_public_period_requirements[:missing_count]
        )
        blockers = tuple(
            f"{plan.gate_id}: {plan.target_id} missing public temporal period requirement "
            f"{requirement.requirement_id} ({requirement.period_selector})"
            for requirement in plan.missing_public_period_requirements[:missing_count]
        )
        status = "ready_for_temporal_holdout" if not blockers else plan.readiness_status
        rows.append(
            TemporalPeriodReadiness(
                plan_id=plan.plan_id,
                gate_id=plan.gate_id,
                source_id=plan.source_id,
                target_id=plan.target_id,
                status=status,
                claim_status="calibration_readiness_only",
                periods_available=periods,
                missing_public_periods=missing_public_periods,
                missing_public_period_requirements=plan.missing_public_period_requirements[:missing_count],
                blockers=blockers,
                claim_boundary=plan.claim_boundary,
            )
        )
    return tuple(rows)


def public_temporal_period_readiness_as_json() -> str:
    payload = {
        "claim_boundary": "temporal period acquisition/readiness only; no invented data and no CAL-G-002 claim upgrade",
        "rows": [row.to_json_dict() for row in build_temporal_period_readiness()],
    }
    return json.dumps(payload, indent=2)


def temporal_period_acquisition_issues(*, require_ready: bool = False) -> tuple[str, ...]:
    issues: list[str] = []
    for row in build_temporal_period_readiness():
        if row.gate_id != "CAL-G-002":
            issues.append(f"{row.plan_id}: temporal acquisition plan must remain scoped to CAL-G-002")
        if row.claim_status != "calibration_readiness_only":
            issues.append(f"{row.plan_id}: claim_status must remain calibration_readiness_only")
        if require_ready:
            issues.extend(row.blockers)
    return tuple(issues)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check public temporal-period acquisition readiness.")
    parser.add_argument("--json", action="store_true", help="Print the temporal-period acquisition matrix as JSON.")
    parser.add_argument("--require-ready", action="store_true", help="Fail until all required public periods are present.")
    args = parser.parse_args(argv)

    rows = build_temporal_period_readiness()
    if args.json:
        print(public_temporal_period_readiness_as_json())
    else:
        for row in rows:
            print(
                f"{row.gate_id}: plan={row.plan_id}; status={row.status}; "
                f"periods={len(row.periods_available)}; missing={len(row.missing_public_periods)}; "
                f"claim={row.claim_status}"
            )

    issues = temporal_period_acquisition_issues(require_ready=args.require_ready)
    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
