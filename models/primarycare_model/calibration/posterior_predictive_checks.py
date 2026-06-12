"""Posterior predictive check readiness for public aggregate targets."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

from models.primarycare_model.calibration.calibration_target_readiness import (
    build_calibration_target_readiness_matrix,
)
from models.primarycare_model.calibration.calibration_validation_gates import (
    build_calibration_validation_gate_matrix,
    validation_gate_issues,
)


@dataclass(frozen=True)
class PosteriorPredictiveTargetRow:
    target_id: str
    source_id: str
    relative_error: float
    tolerance: float
    source_ready: bool
    posterior_predictive_status: str
    blockers: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
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


def _ppc_gate_status() -> str:
    gates = {row.gate_id: row for row in build_calibration_validation_gate_matrix(strict=False)}
    return gates["CAL-G-006"].status


def posterior_predictive_target_rows(*, strict: bool = False) -> tuple[PosteriorPredictiveTargetRow, ...]:
    rows: list[PosteriorPredictiveTargetRow] = []
    for target in build_calibration_target_readiness_matrix(strict=strict):
        blockers: tuple[str, ...] = target.blockers if strict else ()
        status = "passed" if target.calibration_gate_ready else "calibration_readiness_only"
        rows.append(
            PosteriorPredictiveTargetRow(
                target_id=target.target_id,
                source_id=target.source_id,
                relative_error=target.relative_error,
                tolerance=target.tolerance,
                source_ready=target.source_ready,
                posterior_predictive_status=status,
                blockers=blockers,
            )
        )
    return tuple(rows)


def posterior_predictive_checks(*, strict: bool = False) -> dict[str, object]:
    """Return PPC readiness without promoting empirical calibration claims."""

    target_rows = posterior_predictive_target_rows(strict=strict)
    failed_targets = tuple(row.target_id for row in target_rows if row.posterior_predictive_status != "passed")
    gate_status = _ppc_gate_status()
    ppc_status = "passed" if gate_status == "passed" and not failed_targets else "calibration_readiness_only"
    blockers = validation_gate_issues(require_all_validation_data=False) if strict else ()
    interpretation_note = (
        "Public aggregate posterior predictive checks passed for registered public targets; "
        "not-valid-for warnings still exclude precise fiscal, ED, hospital-demand, workforce, "
        "implementation-impact, and causal claims."
        if ppc_status == "passed"
        else (
            "Public aggregate posterior predictive checks remain readiness-only until source-ready "
            "public targets and reproducible predictive draws pass validation gates."
        )
    )
    return {
        "ppc_gate_id": "CAL-G-006",
        "ppc_status": ppc_status,
        "validation_gate_status": gate_status,
        "failed_targets": list(failed_targets),
        "target_rows": [row.to_json_dict() for row in target_rows],
        "not_valid_for": list(NOT_VALID_FOR),
        "blockers": list(blockers),
        "interpretation_note": interpretation_note,
    }


def strict_posterior_predictive_issues() -> tuple[str, ...]:
    payload = posterior_predictive_checks(strict=True)
    issues: list[str] = []
    if payload["ppc_status"] != "passed":
        issues.append("CAL-G-006: posterior predictive checks remain calibration_readiness_only")
    issues.extend(str(issue) for issue in payload["blockers"])
    return tuple(dict.fromkeys(issues))


def posterior_predictive_checks_as_json(*, strict: bool = False) -> str:
    return json.dumps(posterior_predictive_checks(strict=strict), indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report posterior predictive check readiness for public aggregate calibration.")
    parser.add_argument("--strict", action="store_true", help="Fail until posterior predictive checks are source-ready and passed.")
    parser.add_argument("--json", action="store_true", help="Print the PPC readiness payload as JSON.")
    args = parser.parse_args(argv)

    payload = posterior_predictive_checks(strict=args.strict)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"{payload['ppc_gate_id']}: status={payload['ppc_status']}; "
            f"validation_gate={payload['validation_gate_status']}; "
            f"failed_targets={len(payload['failed_targets'])}"
        )

    if args.strict:
        issues = strict_posterior_predictive_issues()
        if issues:
            print("\n".join(issues), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
