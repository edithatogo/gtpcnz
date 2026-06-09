"""Public temporal holdout validation helpers for CAL-G-002.

The lane is deliberately contract-first. It registers public time-series
evidence and only reports a passed temporal holdout when at least one public
training period and a distinct public holdout period can be compared.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import yaml

from models.primarycare_model.data.public_source_snapshot import ROOT

TEMPORAL_HOLDOUT_TARGETS = (
    ROOT
    / "models"
    / "primarycare_model"
    / "registries"
    / "public"
    / "temporal_holdout_targets.public.v1.yaml"
)

TemporalHoldoutStatus = Literal[
    "passed",
    "temporal_comparison_failed",
    "public_validation_source_registered",
    "public_data_unavailable",
]


@dataclass(frozen=True)
class PublicTemporalHoldoutTarget:
    target_id: str
    gate_id: str
    validation_family: str
    label: str
    source_id: str
    processed_artifact: str
    period_column: str
    geography_column: str
    observed_value_column: str
    numerator_column: str
    denominator_column: str
    stratifier: str
    group: str
    minimum_training_periods: int
    holdout_period_strategy: str
    max_error_tolerance: float
    public_access_status: str
    claim_boundary: str


@dataclass(frozen=True)
class PublicTemporalHoldoutComparison:
    gate_id: str
    target_id: str
    validation_family: str
    source_id: str
    training_periods: tuple[str, ...]
    holdout_period: str | None
    periods_available: tuple[str, ...]
    observations: int
    mean_absolute_error: float | None
    max_absolute_error: float | None
    max_error_tolerance: float
    status: TemporalHoldoutStatus
    claim_status: str
    interpretation_note: str

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["training_periods"] = list(self.training_periods)
        payload["periods_available"] = list(self.periods_available)
        return payload


def load_temporal_holdout_targets(path: Path = TEMPORAL_HOLDOUT_TARGETS) -> tuple[PublicTemporalHoldoutTarget, ...]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    targets = []
    for item in payload["targets"]:
        targets.append(
            PublicTemporalHoldoutTarget(
                target_id=str(item["target_id"]),
                gate_id=str(item["gate_id"]),
                validation_family=str(item["validation_family"]),
                label=str(item["label"]),
                source_id=str(item["source_id"]),
                processed_artifact=str(item["processed_artifact"]),
                period_column=str(item["period_column"]),
                geography_column=str(item["geography_column"]),
                observed_value_column=str(item["observed_value_column"]),
                numerator_column=str(item["numerator_column"]),
                denominator_column=str(item["denominator_column"]),
                stratifier=str(item["stratifier"]),
                group=str(item["group"]),
                minimum_training_periods=int(item["minimum_training_periods"]),
                holdout_period_strategy=str(item["holdout_period_strategy"]),
                max_error_tolerance=float(item["max_error_tolerance"]),
                public_access_status=str(item["public_access_status"]),
                claim_boundary=str(item["claim_boundary"]),
            )
        )
    return tuple(targets)


def load_temporal_holdout_rows(target: PublicTemporalHoldoutTarget) -> tuple[dict[str, str], ...]:
    path = ROOT / target.processed_artifact
    if not path.exists():
        return ()
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(csv.DictReader(handle))


def _weighted_rate(rows: tuple[dict[str, str], ...], target: PublicTemporalHoldoutTarget) -> float:
    numerator = sum(float(row[target.numerator_column]) for row in rows)
    denominator = sum(float(row[target.denominator_column]) for row in rows)
    if denominator <= 0:
        raise ValueError(f"{target.target_id}: temporal holdout denominator must be positive")
    return numerator / denominator


def _comparison_for_target(
    target: PublicTemporalHoldoutTarget,
    rows: tuple[dict[str, str], ...] | None = None,
) -> PublicTemporalHoldoutComparison:
    candidate_rows = tuple(rows if rows is not None else load_temporal_holdout_rows(target))
    filtered_rows = tuple(
        row
        for row in candidate_rows
        if row.get("source_id") == target.source_id
        and row.get("stratifier") == target.stratifier
        and row.get("group") == target.group
    )
    periods = tuple(sorted({row[target.period_column] for row in filtered_rows if row.get(target.period_column)}))
    required_periods = target.minimum_training_periods + 1
    if not filtered_rows:
        status: TemporalHoldoutStatus = "public_data_unavailable"
        return PublicTemporalHoldoutComparison(
            gate_id=target.gate_id,
            target_id=target.target_id,
            validation_family=target.validation_family,
            source_id=target.source_id,
            training_periods=(),
            holdout_period=None,
            periods_available=(),
            observations=0,
            mean_absolute_error=None,
            max_absolute_error=None,
            max_error_tolerance=target.max_error_tolerance,
            status=status,
            claim_status="calibration_readiness_only",
            interpretation_note="No public numeric rows are available for this temporal validation target.",
        )
    if len(periods) < required_periods:
        status = "public_validation_source_registered"
        return PublicTemporalHoldoutComparison(
            gate_id=target.gate_id,
            target_id=target.target_id,
            validation_family=target.validation_family,
            source_id=target.source_id,
            training_periods=(),
            holdout_period=None,
            periods_available=periods,
            observations=0,
            mean_absolute_error=None,
            max_absolute_error=None,
            max_error_tolerance=target.max_error_tolerance,
            status=status,
            claim_status="calibration_readiness_only",
            interpretation_note=(
                f"Public source is registered, but {len(periods)} public period(s) are available; "
                f"{required_periods} are required for a temporal train/holdout comparison."
            ),
        )

    holdout_period = periods[-1]
    training_periods = periods[: -1]
    training_rows = tuple(row for row in filtered_rows if row[target.period_column] in training_periods)
    holdout_rows = tuple(row for row in filtered_rows if row[target.period_column] == holdout_period)
    predicted = _weighted_rate(training_rows, target)
    errors = [abs(float(row[target.observed_value_column]) - predicted) for row in holdout_rows]
    max_error = max(errors) if errors else 0.0
    mean_error = sum(errors) / len(errors) if errors else 0.0
    status = "passed" if max_error <= target.max_error_tolerance else "temporal_comparison_failed"
    return PublicTemporalHoldoutComparison(
        gate_id=target.gate_id,
        target_id=target.target_id,
        validation_family=target.validation_family,
        source_id=target.source_id,
        training_periods=training_periods,
        holdout_period=holdout_period,
        periods_available=periods,
        observations=len(holdout_rows),
        mean_absolute_error=round(mean_error, 12),
        max_absolute_error=round(max_error, 12),
        max_error_tolerance=target.max_error_tolerance,
        status=status,
        claim_status="calibration_readiness_only",
        interpretation_note=(
            "Public aggregate temporal holdout comparison only; not a causal, fiscal, "
            "individual-care, implementation, or hospital-demand validation."
        ),
    )


def build_public_temporal_holdout_comparisons(
    rows: tuple[dict[str, str], ...] | None = None,
) -> tuple[PublicTemporalHoldoutComparison, ...]:
    return tuple(_comparison_for_target(target, rows=rows) for target in load_temporal_holdout_targets())


def temporal_holdout_gate_status(gate_id: str) -> str:
    comparisons = tuple(row for row in build_public_temporal_holdout_comparisons() if row.gate_id == gate_id)
    if not comparisons:
        return "public_data_unavailable"
    if all(row.status == "passed" for row in comparisons):
        return "passed"
    if any(row.status == "temporal_comparison_failed" for row in comparisons):
        return "public_holdout_comparison_failed"
    if any(row.status == "public_validation_source_registered" for row in comparisons):
        return "public_validation_source_registered"
    return "public_data_unavailable"


def temporal_holdout_gate_blockers(gate_id: str) -> tuple[str, ...]:
    blockers = []
    for comparison in build_public_temporal_holdout_comparisons():
        if comparison.gate_id != gate_id or comparison.status == "passed":
            continue
        if comparison.status == "temporal_comparison_failed":
            blockers.append(
                f"{comparison.gate_id}: {comparison.target_id} max_abs_error="
                f"{comparison.max_absolute_error} exceeds tolerance={comparison.max_error_tolerance}"
            )
        elif comparison.status == "public_validation_source_registered":
            blockers.append(
                f"{comparison.gate_id}: {comparison.target_id} has "
                f"{len(comparison.periods_available)} public period(s); at least 2 are required"
            )
        else:
            blockers.append(f"{comparison.gate_id}: {comparison.target_id} has no public numeric rows")
    return tuple(blockers)


def public_temporal_holdout_comparisons_as_json() -> str:
    payload = {
        "claim_boundary": "public temporal benchmark only; calibration_readiness_only unless temporal holdout comparisons pass",
        "rows": [row.to_json_dict() for row in build_public_temporal_holdout_comparisons()],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run public temporal holdout validation checks.")
    parser.add_argument("--json", action="store_true", help="Print temporal holdout rows as JSON.")
    parser.add_argument("--require-pass", action="store_true", help="Fail unless all public temporal holdouts pass.")
    args = parser.parse_args(argv)

    comparisons = build_public_temporal_holdout_comparisons()
    if args.json:
        print(public_temporal_holdout_comparisons_as_json())
    else:
        for comparison in comparisons:
            print(
                f"{comparison.gate_id}: target={comparison.target_id}; status={comparison.status}; "
                f"periods={len(comparison.periods_available)}; holdout={comparison.holdout_period}; "
                f"claim={comparison.claim_status}"
            )

    if args.require_pass and any(comparison.status != "passed" for comparison in comparisons):
        print("\n".join(temporal_holdout_gate_blockers("CAL-G-002")), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
