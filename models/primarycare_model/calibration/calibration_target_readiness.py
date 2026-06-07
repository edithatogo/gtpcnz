"""Calibration-target readiness joined to public-source readiness."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

from models.primarycare_model.calibration.public_aggregate_targets import (
    load_calibration_targets,
    predicted_public_value,
)
from models.primarycare_model.data.public_source_readiness_matrix import (
    PublicSourceReadinessRow,
    build_public_source_readiness_matrix,
)


@dataclass(frozen=True)
class CalibrationTargetReadinessRow:
    target_id: str
    target_family: str
    source_id: str
    observed_value: float
    predicted_value: float
    relative_error: float
    tolerance: float
    source_ready: bool
    calibration_gate_ready: bool
    calibration_claim_status: str
    not_valid_for: tuple[str, ...]
    blockers: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["not_valid_for"] = list(self.not_valid_for)
        payload["blockers"] = list(self.blockers)
        return payload


NOT_VALID_FOR = (
    "precise fiscal savings",
    "ED reductions",
    "hospital-demand reductions",
    "workforce effects",
    "implementation impacts",
    "causal effects",
)


def _relative_error(predicted: float, observed: float) -> float:
    denom = abs(observed) or 1.0
    return abs(predicted - observed) / denom


def _source_row_by_id(strict: bool) -> dict[str, PublicSourceReadinessRow]:
    return {row.source_id: row for row in build_public_source_readiness_matrix(strict=strict)}


def build_calibration_target_readiness_matrix(*, strict: bool = False) -> tuple[CalibrationTargetReadinessRow, ...]:
    """Return target-level readiness without promoting public calibration claims."""

    source_rows = _source_row_by_id(strict=strict)
    rows: list[CalibrationTargetReadinessRow] = []
    for target in load_calibration_targets():
        predicted = predicted_public_value(target)
        relative_error = round(_relative_error(predicted, target.observed_value), 6)
        source_row = source_rows.get(target.source_id)
        blockers: list[str] = []
        if source_row is None:
            blockers.append(f"{target.target_id}: source {target.source_id} has no public source readiness row")
            source_ready = False
        else:
            source_ready = source_row.source_ready
            if not source_row.source_ready:
                blockers.append(f"{target.target_id}: source {target.source_id} is not source_ready")
            blockers.extend(f"{target.target_id}: {issue}" for issue in source_row.issues)
        if relative_error > target.tolerance:
            blockers.append(
                f"{target.target_id}: relative_error {relative_error} exceeds tolerance {target.tolerance}"
            )

        calibration_gate_ready = source_ready and relative_error <= target.tolerance
        claim_status = "public_aggregate_target_ready" if calibration_gate_ready else "calibration_readiness_only"
        rows.append(
            CalibrationTargetReadinessRow(
                target_id=target.target_id,
                target_family=target.target_family,
                source_id=target.source_id,
                observed_value=target.observed_value,
                predicted_value=predicted,
                relative_error=relative_error,
                tolerance=target.tolerance,
                source_ready=source_ready,
                calibration_gate_ready=calibration_gate_ready,
                calibration_claim_status=claim_status,
                not_valid_for=NOT_VALID_FOR,
                blockers=tuple(dict.fromkeys(blockers if strict else ())),
            )
        )
    return tuple(rows)


def strict_calibration_target_issues() -> tuple[str, ...]:
    issues: list[str] = []
    for row in build_calibration_target_readiness_matrix(strict=True):
        if not row.calibration_gate_ready:
            issues.append(f"{row.target_id}: calibration target remains calibration_readiness_only")
        issues.extend(row.blockers)
    return tuple(dict.fromkeys(issues))


def readiness_matrix_as_json(*, strict: bool = False) -> str:
    rows = build_calibration_target_readiness_matrix(strict=strict)
    payload = {
        "claim_boundary": "public benchmark only until target source, tolerance, checksum, processed, and calibration gates pass",
        "rows": [row.to_json_dict() for row in rows],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report public aggregate calibration target readiness.")
    parser.add_argument("--strict", action="store_true", help="Fail until every calibration target is source-ready and within tolerance.")
    parser.add_argument("--json", action="store_true", help="Print the calibration target readiness matrix as JSON.")
    args = parser.parse_args(argv)

    if args.json:
        print(readiness_matrix_as_json(strict=args.strict))
    else:
        for row in build_calibration_target_readiness_matrix(strict=args.strict):
            print(
                f"{row.target_id}: source={row.source_id}; family={row.target_family}; "
                f"relative_error={row.relative_error}; tolerance={row.tolerance}; "
                f"source_ready={row.source_ready}; claim={row.calibration_claim_status}"
            )

    if args.strict:
        issues = strict_calibration_target_issues()
        if issues:
            print("\n".join(issues), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
