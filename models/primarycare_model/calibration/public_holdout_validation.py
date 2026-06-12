"""Public aggregate holdout comparison helpers.

These comparisons are deliberately benchmark-only. They compare public PHO
access workbook rows with transparent public aggregate baselines and do not
promote the model to empirically calibrated status.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from models.primarycare_model.data.public_source_snapshot import ROOT

HoldoutComparisonStatus = Literal["passed", "comparison_failed"]

PHO_ACCESS_NUMERIC = (
    ROOT
    / "data"
    / "public_processed"
    / "src_hnz_pho_access_timeseries"
    / "pho_access_numeric_extract.csv"
)


@dataclass(frozen=True)
class PublicHoldoutObservation:
    district: str
    stratifier: str
    group: str
    observed_coverage_rate: float
    predicted_coverage_rate: float
    absolute_error: float
    tolerance_gap: float

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class PublicHoldoutComparison:
    gate_id: str
    validation_family: str
    predictor_id: str
    stratifier: str
    group: str
    observations: int
    mean_absolute_error: float
    max_absolute_error: float
    max_error_tolerance: float
    tolerance_gap: float
    failing_groups: tuple[str, ...]
    failing_observations: tuple[PublicHoldoutObservation, ...]
    status: HoldoutComparisonStatus
    claim_status: str
    interpretation_note: str
    next_data_model_requirement: str

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def load_pho_access_numeric_rows(path: Path = PHO_ACCESS_NUMERIC) -> tuple[dict[str, str], ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(csv.DictReader(handle))


def _coverage_rate(row: dict[str, str]) -> float:
    return float(row["reported_coverage_rate"])


def _weighted_rate(rows: tuple[dict[str, str], ...]) -> float:
    enrolled = sum(float(row["enrolled_count"]) for row in rows)
    population = sum(float(row["population_count"]) for row in rows)
    if population <= 0:
        raise ValueError("public holdout population denominator must be positive")
    return enrolled / population


def _next_data_model_requirement(gate_id: str, validation_family: str) -> str:
    if gate_id == "CAL-G-003":
        return (
            "Add independent regional or rurality-grain public holdout targets and model predictions "
            "that explain district variation beyond the weighted public baseline."
        )
    if gate_id == "CAL-G-004":
        return (
            "Add subgroup-gradient model predictions at the same ethnicity/deprivation grain as the "
            "public extract and reduce each failed group within tolerance."
        )
    return f"Add public holdout data and model predictions for {validation_family} at matching grain."


def _failure_label(observation: PublicHoldoutObservation) -> str:
    return f"{observation.stratifier}/{observation.group}/{observation.district}"


def _comparison_for_rows(
    *,
    gate_id: str,
    validation_family: str,
    stratifier: str,
    group: str,
    rows: tuple[dict[str, str], ...],
    max_error_tolerance: float,
) -> PublicHoldoutComparison:
    predicted = _weighted_rate(rows)
    observations = [
        PublicHoldoutObservation(
            district=row["district"],
            stratifier=stratifier,
            group=group,
            observed_coverage_rate=round(_coverage_rate(row), 12),
            predicted_coverage_rate=round(predicted, 12),
            absolute_error=round(abs(_coverage_rate(row) - predicted), 12),
            tolerance_gap=round(max(0.0, abs(_coverage_rate(row) - predicted) - max_error_tolerance), 12),
        )
        for row in rows
    ]
    max_error = max(observation.absolute_error for observation in observations)
    mean_error = sum(observation.absolute_error for observation in observations) / len(observations)
    failed_observations = tuple(
        sorted(
            (observation for observation in observations if observation.absolute_error > max_error_tolerance),
            key=lambda observation: (-observation.absolute_error, observation.district),
        )
    )
    status: HoldoutComparisonStatus = "passed" if max_error <= max_error_tolerance else "comparison_failed"
    return PublicHoldoutComparison(
        gate_id=gate_id,
        validation_family=validation_family,
        predictor_id="weighted_public_baseline_rate",
        stratifier=stratifier,
        group=group,
        observations=len(observations),
        mean_absolute_error=round(mean_error, 12),
        max_absolute_error=round(max_error, 12),
        max_error_tolerance=max_error_tolerance,
        tolerance_gap=round(max(0.0, max_error - max_error_tolerance), 12),
        failing_groups=tuple(_failure_label(observation) for observation in failed_observations),
        failing_observations=failed_observations,
        status=status,
        claim_status="calibration_readiness_only",
        interpretation_note=(
            "Transparent weighted public baseline comparison only; not a causal, fiscal, "
            "or individual-care prediction validation."
        ),
        next_data_model_requirement=(
            _next_data_model_requirement(gate_id, validation_family)
            if failed_observations
            else "No row-level tolerance gap; gate remains readiness-only until all sibling comparisons pass."
        ),
    )


def _training_prediction_for_holdout_row(
    holdout_row: dict[str, str],
    training_rows: tuple[dict[str, str], ...],
    fallback_rate: float,
) -> float:
    district = holdout_row.get("district")
    matching_rows = tuple(row for row in training_rows if row.get("district") == district)
    if not matching_rows:
        return fallback_rate
    return _weighted_rate(matching_rows)


def _period_persistence_comparison_for_rows(
    *,
    gate_id: str,
    validation_family: str,
    predictor_id: str,
    stratifier: str,
    group: str,
    rows: tuple[dict[str, str], ...],
    max_error_tolerance: float,
    passed_requirement: str,
    interpretation_note: str,
) -> PublicHoldoutComparison:
    periods = tuple(sorted({row["period"] for row in rows if row.get("period")}))
    if len(periods) < 2:
        return _comparison_for_rows(
            gate_id=gate_id,
            validation_family=validation_family,
            stratifier=stratifier,
            group=group,
            rows=rows,
            max_error_tolerance=max_error_tolerance,
        )

    holdout_period = periods[-1]
    training_periods = periods[:-1]
    training_rows = tuple(row for row in rows if row["period"] in training_periods)
    holdout_rows = tuple(row for row in rows if row["period"] == holdout_period)
    fallback_rate = _weighted_rate(training_rows)
    observations = []
    for row in holdout_rows:
        predicted = _training_prediction_for_holdout_row(row, training_rows, fallback_rate)
        absolute_error = abs(_coverage_rate(row) - predicted)
        observations.append(
            PublicHoldoutObservation(
                district=row["district"],
                stratifier=stratifier,
                group=group,
                observed_coverage_rate=round(_coverage_rate(row), 12),
                predicted_coverage_rate=round(predicted, 12),
                absolute_error=round(absolute_error, 12),
                tolerance_gap=round(max(0.0, absolute_error - max_error_tolerance), 12),
            )
        )
    max_error = max(observation.absolute_error for observation in observations)
    mean_error = sum(observation.absolute_error for observation in observations) / len(observations)
    failed_observations = tuple(
        sorted(
            (observation for observation in observations if observation.absolute_error > max_error_tolerance),
            key=lambda observation: (-observation.absolute_error, observation.district),
        )
    )
    status: HoldoutComparisonStatus = "passed" if max_error <= max_error_tolerance else "comparison_failed"
    return PublicHoldoutComparison(
        gate_id=gate_id,
        validation_family=validation_family,
        predictor_id=predictor_id,
        stratifier=stratifier,
        group=group,
        observations=len(observations),
        mean_absolute_error=round(mean_error, 12),
        max_absolute_error=round(max_error, 12),
        max_error_tolerance=max_error_tolerance,
        tolerance_gap=round(max(0.0, max_error - max_error_tolerance), 12),
        failing_groups=tuple(_failure_label(observation) for observation in failed_observations),
        failing_observations=failed_observations,
        status=status,
        claim_status="calibration_readiness_only",
        interpretation_note=interpretation_note,
        next_data_model_requirement=(
            _next_data_model_requirement(gate_id, validation_family)
            if failed_observations
            else passed_requirement
        ),
    )


def build_public_holdout_comparisons() -> tuple[PublicHoldoutComparison, ...]:
    rows = load_pho_access_numeric_rows()
    comparisons: list[PublicHoldoutComparison] = []

    geographic_rows = tuple(row for row in rows if row["stratifier"] == "ethnicity" and row["group"] == "Total")
    if geographic_rows:
        comparisons.append(
            _period_persistence_comparison_for_rows(
                gate_id="CAL-G-003",
                validation_family="geographic_holdout_validation",
                predictor_id="district_public_training_period_rate",
                stratifier="district",
                group="total_coverage",
                rows=geographic_rows,
                max_error_tolerance=0.05,
                passed_requirement=(
                    "No district-level tolerance gap; gate remains readiness-only until all sibling comparisons pass."
                ),
                interpretation_note=(
                    "Public aggregate geographic holdout comparison using district-level training-period "
                    "persistence with national fallback only when a district is absent; not a causal, fiscal, "
                    "or individual-care prediction validation."
                ),
            )
        )

    subgroup_rows = tuple(
        row
        for row in rows
        if row["stratifier"] in {"ethnicity", "deprivation"} and row["group"] != "Total"
    )
    for stratifier, group in sorted({(row["stratifier"], row["group"]) for row in subgroup_rows}):
        group_rows = tuple(row for row in subgroup_rows if row["stratifier"] == stratifier and row["group"] == group)
        comparisons.append(
            _period_persistence_comparison_for_rows(
                gate_id="CAL-G-004",
                validation_family="subgroup_gradient_validation",
                predictor_id="district_subgroup_public_training_period_rate",
                stratifier=stratifier,
                group=group,
                rows=group_rows,
                max_error_tolerance=0.05,
                passed_requirement=(
                    "No district-subgroup tolerance gap; gate remains readiness-only until all sibling comparisons pass."
                ),
                interpretation_note=(
                    "Public aggregate subgroup-gradient holdout comparison using district-subgroup "
                    "training-period persistence with subgroup national fallback only when a district subgroup "
                    "is absent; not a causal, fiscal, or individual-care prediction validation."
                ),
            )
        )
    return tuple(comparisons)


def holdout_gate_status(gate_id: str) -> str:
    comparisons = tuple(row for row in build_public_holdout_comparisons() if row.gate_id == gate_id)
    if not comparisons:
        return "public_validation_numeric_ready"
    if all(row.status == "passed" for row in comparisons):
        return "passed"
    return "public_holdout_comparison_failed"


def _ascii_safe(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", errors="ignore").decode("ascii")


def holdout_gate_blockers(gate_id: str) -> tuple[str, ...]:
    blockers = []
    for comparison in build_public_holdout_comparisons():
        if comparison.gate_id != gate_id or comparison.status == "passed":
            continue
        failed_groups = ", ".join(_ascii_safe(group) for group in comparison.failing_groups[:5])
        if len(comparison.failing_groups) > 5:
            failed_groups = f"{failed_groups}, +{len(comparison.failing_groups) - 5} more"
        blockers.append(
            f"{comparison.gate_id}: {comparison.validation_family} "
            f"{_ascii_safe(comparison.stratifier)}/{_ascii_safe(comparison.group)} "
            f"max_abs_error={comparison.max_absolute_error} exceeds tolerance={comparison.max_error_tolerance}; "
            f"tolerance_gap={comparison.tolerance_gap}; failing_groups={failed_groups}; "
            f"next_data_model_requirement={comparison.next_data_model_requirement}"
        )
    return tuple(blockers)


def public_holdout_comparisons_as_json() -> str:
    payload = {
        "claim_boundary": "benchmark comparison only; public_benchmark/calibration_readiness_only until holdout gates pass",
        "rows": [row.to_json_dict() for row in build_public_holdout_comparisons()],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run public aggregate holdout benchmark comparisons.")
    parser.add_argument("--json", action="store_true", help="Print comparison rows as JSON.")
    parser.add_argument("--require-pass", action="store_true", help="Fail unless all public holdout comparisons pass.")
    args = parser.parse_args(argv)

    comparisons = build_public_holdout_comparisons()
    if args.json:
        print(public_holdout_comparisons_as_json())
    else:
        for comparison in comparisons:
            print(
                f"{comparison.gate_id}: {_ascii_safe(comparison.stratifier)}/{_ascii_safe(comparison.group)}; "
                f"status={comparison.status}; max_abs_error={comparison.max_absolute_error}; "
                f"tolerance={comparison.max_error_tolerance}; tolerance_gap={comparison.tolerance_gap}; "
                f"failing_groups={len(comparison.failing_groups)}; "
                f"next={comparison.next_data_model_requirement}; claim={comparison.claim_status}"
            )

    if args.require_pass and any(comparison.status != "passed" for comparison in comparisons):
        print("\n".join(holdout_gate_blockers("CAL-G-003") + holdout_gate_blockers("CAL-G-004")), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
