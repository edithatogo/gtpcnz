"""Public aggregate calibration validation gate matrix."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from typing import Literal, cast

from models.primarycare_model.calibration.calibration_target_readiness import (
    build_calibration_target_readiness_matrix,
)
from models.primarycare_model.calibration.public_holdout_validation import (
    holdout_gate_blockers,
    holdout_gate_status,
)
from models.primarycare_model.calibration.public_policy_shock_plausibility import (
    policy_shock_gate_blockers,
    policy_shock_gate_status,
)
from models.primarycare_model.calibration.public_temporal_holdout_validation import (
    temporal_holdout_gate_blockers,
    temporal_holdout_gate_status,
)
from models.primarycare_model.data.public_source_snapshot import ROOT

ValidationGateStatus = Literal[
    "passed",
    "calibration_readiness_only",
    "public_data_unavailable",
    "public_validation_source_registered",
    "public_validation_numeric_ready",
    "public_holdout_comparison_failed",
]


@dataclass(frozen=True)
class CalibrationValidationGateRow:
    gate_id: str
    gate_family: str
    label: str
    public_data_requirement: str
    status: ValidationGateStatus
    claim_status: str
    blockers: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


def _target_blockers() -> tuple[str, ...]:
    blockers: list[str] = []
    for row in build_calibration_target_readiness_matrix(strict=True):
        if not row.calibration_gate_ready:
            blockers.append(f"{row.target_id}: calibration target is not ready")
        blockers.extend(row.blockers)
    return tuple(dict.fromkeys(blockers))


def _pho_access_numeric_rows() -> tuple[dict[str, str], ...]:
    path = ROOT / "data" / "public_processed" / "src_hnz_pho_access_timeseries" / "pho_access_numeric_extract.csv"
    if not path.exists():
        return ()
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(csv.DictReader(handle))


def _has_pho_access_numeric_validation_extract(*validation_uses: str) -> bool:
    uses = set(validation_uses)
    return any(
        row.get("validation_use") in uses
        and row.get("absolute_rate_difference") not in {None, ""}
        and float(row["absolute_rate_difference"]) <= 1e-9
        for row in _pho_access_numeric_rows()
    )


def _strict_holdout_blockers(gate_id: str, status: ValidationGateStatus, optional_holdout_blocker: str) -> tuple[str, ...]:
    if status == "public_holdout_comparison_failed":
        return holdout_gate_blockers(gate_id)
    if status == "public_data_unavailable":
        return (f"{gate_id}: {optional_holdout_blocker}",)
    return ()


def build_calibration_validation_gate_matrix(*, strict: bool = False) -> tuple[CalibrationValidationGateRow, ...]:
    """Return validation gates without upgrading empirical calibration claims."""

    target_blockers = _target_blockers()
    baseline_status: ValidationGateStatus = "passed" if not target_blockers else "calibration_readiness_only"
    ppc_status: ValidationGateStatus = baseline_status
    optional_holdout_blocker = "public aggregate holdout dataset not yet registered as source_ready"
    temporal_status = cast(ValidationGateStatus, temporal_holdout_gate_status("CAL-G-002"))
    subgroup_status: ValidationGateStatus = (
        holdout_gate_status("CAL-G-004")
        if _has_pho_access_numeric_validation_extract("subgroup_gradient_validation_candidate")
        else "public_data_unavailable"
    )
    geographic_status: ValidationGateStatus = (
        holdout_gate_status("CAL-G-003")
        if _has_pho_access_numeric_validation_extract(
            "subgroup_gradient_validation_candidate",
            "subgroup_descriptive_validation_candidate",
        )
        else "public_data_unavailable"
    )
    claim_downgrade_status = "calibration_readiness_only"

    rows = [
        CalibrationValidationGateRow(
            gate_id="CAL-G-001",
            gate_family="baseline_public_aggregate_reproduction",
            label="Baseline public aggregate reproduction",
            public_data_requirement="All calibration targets source-ready and within tolerance.",
            status=baseline_status,
            claim_status="public_aggregate_validated" if baseline_status == "passed" else "calibration_readiness_only",
            blockers=target_blockers if strict else (),
        ),
        CalibrationValidationGateRow(
            gate_id="CAL-G-002",
            gate_family="temporal_holdout_validation",
            label="Temporal holdout validation where public time series permit",
            public_data_requirement="Public time-series extracts with held-out periods and verified checksums.",
            status=temporal_status,
            claim_status="calibration_readiness_only",
            blockers=temporal_holdout_gate_blockers("CAL-G-002") if strict else (),
        ),
        CalibrationValidationGateRow(
            gate_id="CAL-G-003",
            gate_family="geographic_holdout_validation",
            label="Geographic/rural holdout validation where public regional data permit",
            public_data_requirement="Public regional or rurality aggregate extracts with held-out areas.",
            status=geographic_status,
            claim_status="calibration_readiness_only",
            blockers=_strict_holdout_blockers("CAL-G-003", geographic_status, optional_holdout_blocker) if strict else (),
        ),
        CalibrationValidationGateRow(
            gate_id="CAL-G-004",
            gate_family="subgroup_gradient_validation",
            label="Subgroup gradient validation where public subgroup data permit",
            public_data_requirement="Public ethnicity, deprivation, age, sex, or rurality aggregate gradients.",
            status=subgroup_status,
            claim_status="calibration_readiness_only",
            blockers=_strict_holdout_blockers("CAL-G-004", subgroup_status, optional_holdout_blocker) if strict else (),
        ),
        CalibrationValidationGateRow(
            gate_id="CAL-G-005",
            gate_family="public_policy_shock_plausibility",
            label="Known public policy shock plausibility where published shock data permit",
            public_data_requirement=(
                "Published aggregate pre/post policy-shock data or bounded public policy-condition "
                "comparison data and documented shock definition."
            ),
            status=policy_shock_gate_status(),
            claim_status="calibration_readiness_only",
            blockers=policy_shock_gate_blockers() if strict else (),
        ),
        CalibrationValidationGateRow(
            gate_id="CAL-G-006",
            gate_family="posterior_predictive_checks",
            label="Posterior predictive checks",
            public_data_requirement="Source-ready public targets and reproducible predictive draws.",
            status=ppc_status,
            claim_status="public_aggregate_validated" if ppc_status == "passed" else "calibration_readiness_only",
            blockers=target_blockers if strict else (),
        ),
        CalibrationValidationGateRow(
            gate_id="CAL-G-007",
            gate_family="claim_level_downgrade",
            label="Claim-level downgrade if validation gates fail",
            public_data_requirement="Any failed or unavailable gate must keep outputs at public_benchmark.",
            status="passed",
            claim_status=claim_downgrade_status,
            blockers=(),
        ),
    ]
    return tuple(rows)


def strict_validation_gate_issues() -> tuple[str, ...]:
    return validation_gate_issues(require_all_validation_data=False)


def validation_gate_issues(*, require_all_validation_data: bool) -> tuple[str, ...]:
    issues: list[str] = []
    for row in build_calibration_validation_gate_matrix(strict=True):
        if row.status in {
            "public_data_unavailable",
            "public_validation_source_registered",
            "public_validation_numeric_ready",
            "public_holdout_comparison_failed",
        } and not require_all_validation_data:
            continue
        if row.status != "passed" and row.gate_id != "CAL-G-007":
            issues.append(f"{row.gate_id}: {row.label} is not passed; claim remains calibration_readiness_only")
        issues.extend(row.blockers)
    return tuple(dict.fromkeys(issues))


def validation_gate_matrix_as_json(*, strict: bool = False) -> str:
    payload = {
        "claim_boundary": "public benchmark only until all public aggregate validation gates pass",
        "rows": [row.to_json_dict() for row in build_calibration_validation_gate_matrix(strict=strict)],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report public aggregate calibration validation gates.")
    parser.add_argument("--strict", action="store_true", help="Fail until required calibration validation gates pass.")
    parser.add_argument(
        "--require-all-validation-data",
        action="store_true",
        help="Also fail documented public_data_unavailable holdout gates; use for empirical claim-upgrade releases.",
    )
    parser.add_argument("--json", action="store_true", help="Print the validation gate matrix as JSON.")
    args = parser.parse_args(argv)

    if args.json:
        print(validation_gate_matrix_as_json(strict=args.strict))
    else:
        for row in build_calibration_validation_gate_matrix(strict=args.strict):
            print(
                f"{row.gate_id}: family={row.gate_family}; status={row.status}; "
                f"claim={row.claim_status}"
            )

    if args.strict:
        issues = validation_gate_issues(require_all_validation_data=args.require_all_validation_data)
        if issues:
            print("\n".join(issues), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
