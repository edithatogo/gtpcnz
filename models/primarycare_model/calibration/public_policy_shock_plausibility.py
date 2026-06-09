"""Readiness-only public policy-shock plausibility evidence for CAL-G-005."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, cast

import yaml

from models.primarycare_model.data.public_source_readiness_matrix import build_public_source_readiness_matrix
from models.primarycare_model.data.public_source_snapshot import PUBLIC_REGISTRY, ROOT

REGISTRY_PATH = PUBLIC_REGISTRY / "policy_shock_plausibility.public.v1.yaml"

PolicyShockComparisonStatus = Literal["readiness_only", "numeric_ready", "passed", "comparison_failed"]
PolicyShockComparisonReadinessStatus = Literal[
    "artifact_not_registered",
    "artifact_missing",
    "artifact_invalid",
    "numeric_pre_post_ready",
    "comparison_passed",
    "comparison_failed",
]
PolicyShockGateStatus = Literal[
    "passed",
    "public_data_unavailable",
    "public_validation_source_registered",
    "public_validation_numeric_ready",
    "public_holdout_comparison_failed",
]
REQUIRED_NUMERIC_COMPARISON_COLUMNS = (
    "shock_id",
    "metric_id",
    "pre_period",
    "post_period",
    "pre_value",
    "post_value",
    "observed_delta",
    "observed_direction",
    "modelled_direction",
    "comparison_result",
)
ALLOWED_COMPARISON_RESULTS = {"numeric_ready", "passed", "comparison_failed"}
ALLOWED_DIRECTIONS = {"increase", "decrease", "no_change"}
OBSERVED_DELTA_TOLERANCE = 1e-9


@dataclass(frozen=True)
class NumericComparisonContract:
    required_columns: tuple[str, ...]
    readiness_rule: str
    pass_rule: str


@dataclass(frozen=True)
class NumericComparisonReadiness:
    status: PolicyShockComparisonReadinessStatus
    artifact_path: str | None
    rows_checked: int
    issues: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


@dataclass(frozen=True)
class PublicPolicyShockEvidence:
    shock_id: str
    gate_id: str
    source_id: str
    label: str
    published_policy_reference: str
    public_access_status: str
    shock_definition_status: str
    comparison_status: PolicyShockComparisonStatus
    comparison_artifact: str | None
    numeric_comparison_contract: NumericComparisonContract
    numeric_comparison_readiness: NumericComparisonReadiness
    observed_direction: str | None
    modelled_direction: str | None
    tolerance_note: str
    claim_boundary: str
    source_ready: bool
    claim_status: str = "calibration_readiness_only"

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def _lists_to_tuples(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_lists_to_tuples(item) for item in obj)
    if isinstance(obj, dict):
        return {key: _lists_to_tuples(value) for key, value in obj.items()}
    return obj


def _registry_rows() -> tuple[dict[str, object], ...]:
    payload = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return _lists_to_tuples(payload["policy_shock_evidence"])


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)


def _comparison_artifact_path(comparison_artifact: str | None) -> Path | None:
    if comparison_artifact is None:
        return None
    path = Path(comparison_artifact)
    if not path.is_absolute():
        path = ROOT / path
    return path


def _numeric_value(value: str | None) -> float | None:
    if value is None:
        return None
    cleaned = value.strip().replace("$", "").replace(",", "")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _required_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _direction_from_delta(delta: float) -> str:
    if delta > OBSERVED_DELTA_TOLERANCE:
        return "increase"
    if delta < -OBSERVED_DELTA_TOLERANCE:
        return "decrease"
    return "no_change"


def _numeric_comparison_contract(row: dict[str, object]) -> NumericComparisonContract:
    raw_contract = row.get("numeric_comparison_contract")
    if not isinstance(raw_contract, dict):
        return NumericComparisonContract(
            required_columns=REQUIRED_NUMERIC_COMPARISON_COLUMNS,
            readiness_rule=(
                "Public numeric pre/post comparison requires a source-ready public artifact "
                "with numeric pre_value and post_value fields for this shock_id."
            ),
            pass_rule=(
                "CAL-G-005 can pass only when comparison_result is passed for a public "
                "pre/post metric and the source is source_ready."
            ),
        )
    required_columns = tuple(str(column) for column in raw_contract.get("required_columns", REQUIRED_NUMERIC_COMPARISON_COLUMNS))
    return NumericComparisonContract(
        required_columns=required_columns,
        readiness_rule=str(raw_contract["readiness_rule"]),
        pass_rule=str(raw_contract["pass_rule"]),
    )


def _numeric_comparison_readiness(
    *,
    shock_id: str,
    comparison_artifact: str | None,
    contract: NumericComparisonContract,
) -> NumericComparisonReadiness:
    path = _comparison_artifact_path(comparison_artifact)
    if path is None:
        return NumericComparisonReadiness(
            status="artifact_not_registered",
            artifact_path=None,
            rows_checked=0,
            issues=("No public numeric pre/post comparison artifact is registered.",),
        )
    artifact_label = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
    if not path.exists():
        return NumericComparisonReadiness(
            status="artifact_missing",
            artifact_path=artifact_label,
            rows_checked=0,
            issues=(f"Registered comparison artifact does not exist: {artifact_label}",),
        )

    issues: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing_columns = tuple(column for column in contract.required_columns if column not in fieldnames)
        if missing_columns:
            issues.append(f"Missing required numeric comparison columns: {', '.join(missing_columns)}")
            return NumericComparisonReadiness(
                status="artifact_invalid",
                artifact_path=artifact_label,
                rows_checked=0,
                issues=tuple(issues),
            )
        rows = tuple(row for row in reader if row.get("shock_id") == shock_id)

    if not rows:
        issues.append(f"No numeric comparison rows found for shock_id={shock_id}.")
    passed = False
    failed = False
    for index, row in enumerate(rows, start=1):
        metric_id = _required_text(row.get("metric_id"))
        pre_period = _required_text(row.get("pre_period"))
        post_period = _required_text(row.get("post_period"))
        pre_value = _numeric_value(row.get("pre_value"))
        post_value = _numeric_value(row.get("post_value"))
        observed_delta = _numeric_value(row.get("observed_delta"))
        observed_direction = (row.get("observed_direction") or "").strip()
        modelled_direction = (row.get("modelled_direction") or "").strip()
        result = (row.get("comparison_result") or "").strip()
        if metric_id is None:
            issues.append(f"Row {index}: metric_id is required.")
        if pre_period is None:
            issues.append(f"Row {index}: pre_period is required.")
        if post_period is None:
            issues.append(f"Row {index}: post_period is required.")
        if pre_value is None:
            issues.append(f"Row {index}: pre_value is not numeric.")
        if post_value is None:
            issues.append(f"Row {index}: post_value is not numeric.")
        if observed_delta is None:
            issues.append(f"Row {index}: observed_delta is not numeric.")
        if observed_direction not in ALLOWED_DIRECTIONS:
            issues.append(f"Row {index}: observed_direction must be one of {sorted(ALLOWED_DIRECTIONS)}.")
        if modelled_direction not in ALLOWED_DIRECTIONS:
            issues.append(f"Row {index}: modelled_direction must be one of {sorted(ALLOWED_DIRECTIONS)}.")
        if pre_value is not None and post_value is not None and observed_delta is not None:
            expected_delta = post_value - pre_value
            if abs(observed_delta - expected_delta) > OBSERVED_DELTA_TOLERANCE:
                issues.append(
                    f"Row {index}: observed_delta must equal post_value - pre_value "
                    f"({expected_delta:g})."
                )
            expected_direction = _direction_from_delta(observed_delta)
            if observed_direction in ALLOWED_DIRECTIONS and observed_direction != expected_direction:
                issues.append(
                    f"Row {index}: observed_direction must match observed_delta "
                    f"({expected_direction})."
                )
        if result not in ALLOWED_COMPARISON_RESULTS:
            issues.append(f"Row {index}: comparison_result must be one of {sorted(ALLOWED_COMPARISON_RESULTS)}.")
        if result == "passed" and observed_direction != modelled_direction:
            issues.append(f"Row {index}: comparison_result=passed requires observed_direction to match modelled_direction.")
        passed = passed or result == "passed"
        failed = failed or result == "comparison_failed"

    if issues:
        status: PolicyShockComparisonReadinessStatus = "artifact_invalid"
    elif failed:
        status = "comparison_failed"
    elif passed:
        status = "comparison_passed"
    else:
        status = "numeric_pre_post_ready"
    return NumericComparisonReadiness(
        status=status,
        artifact_path=artifact_label,
        rows_checked=len(rows),
        issues=tuple(dict.fromkeys(issues)),
    )


def build_public_policy_shock_evidence() -> tuple[PublicPolicyShockEvidence, ...]:
    """Return registered public policy-shock evidence without promoting claims."""

    readiness = {row.source_id: row for row in build_public_source_readiness_matrix(strict=False)}
    evidence: list[PublicPolicyShockEvidence] = []
    for row in _registry_rows():
        source_id = str(row["source_id"])
        source_ready = bool(readiness.get(source_id) and readiness[source_id].source_ready)
        comparison_artifact = _optional_str(row["comparison_artifact"])
        contract = _numeric_comparison_contract(row)
        evidence.append(
            PublicPolicyShockEvidence(
                shock_id=str(row["shock_id"]),
                gate_id=str(row["gate_id"]),
                source_id=source_id,
                label=str(row["label"]),
                published_policy_reference=str(row["published_policy_reference"]),
                public_access_status=str(row["public_access_status"]),
                shock_definition_status=str(row["shock_definition_status"]),
                comparison_status=cast(PolicyShockComparisonStatus, row["comparison_status"]),
                comparison_artifact=comparison_artifact,
                numeric_comparison_contract=contract,
                numeric_comparison_readiness=_numeric_comparison_readiness(
                    shock_id=str(row["shock_id"]),
                    comparison_artifact=comparison_artifact,
                    contract=contract,
                ),
                observed_direction=_optional_str(row["observed_direction"]),
                modelled_direction=_optional_str(row["modelled_direction"]),
                tolerance_note=str(row["tolerance_note"]),
                claim_boundary=str(row["claim_boundary"]),
                source_ready=source_ready,
            )
        )
    return tuple(evidence)


def policy_shock_gate_status() -> PolicyShockGateStatus:
    rows = build_public_policy_shock_evidence()
    if not rows:
        return "public_data_unavailable"
    if any(
        row.comparison_status == "comparison_failed" or row.numeric_comparison_readiness.status == "comparison_failed"
        for row in rows
    ):
        return "public_holdout_comparison_failed"
    if rows and all(
        row.comparison_status == "passed"
        and row.numeric_comparison_readiness.status == "comparison_passed"
        and row.source_ready
        for row in rows
    ):
        return "passed"
    if any(
        row.comparison_status == "numeric_ready"
        or row.numeric_comparison_readiness.status == "numeric_pre_post_ready"
        for row in rows
    ):
        return "public_validation_numeric_ready"
    return "public_validation_source_registered"


def policy_shock_gate_blockers() -> tuple[str, ...]:
    status = policy_shock_gate_status()
    if status == "passed":
        return ()
    if status == "public_holdout_comparison_failed":
        return tuple(
            f"CAL-G-005: {row.shock_id} comparison failed; claim remains calibration_readiness_only"
            for row in build_public_policy_shock_evidence()
            if row.comparison_status == "comparison_failed" or row.numeric_comparison_readiness.status == "comparison_failed"
        )
    artifact_issues = tuple(
        f"CAL-G-005: {row.shock_id}: {issue}"
        for row in build_public_policy_shock_evidence()
        for issue in row.numeric_comparison_readiness.issues
    )
    if artifact_issues:
        return artifact_issues
    return (
        "CAL-G-005: public policy-shock evidence is registered, but no public pre/post "
        "shock comparison has passed; claim remains calibration_readiness_only",
    )


def public_policy_shock_evidence_as_json() -> str:
    payload = {
        "claim_boundary": (
            "public policy-shock plausibility evidence only; no causal, effect-size, fiscal, "
            "hospital-demand, or implementation-impact claim"
        ),
        "gate_status": policy_shock_gate_status(),
        "rows": [row.to_json_dict() for row in build_public_policy_shock_evidence()],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report CAL-G-005 public policy-shock plausibility evidence.")
    parser.add_argument("--json", action="store_true", help="Print policy-shock evidence as JSON.")
    parser.add_argument("--require-pass", action="store_true", help="Fail unless public policy-shock comparisons pass.")
    args = parser.parse_args(argv)

    if args.json:
        print(public_policy_shock_evidence_as_json())
    else:
        for row in build_public_policy_shock_evidence():
            print(
                f"{row.gate_id}: {row.shock_id}; status={row.comparison_status}; "
                f"source_ready={row.source_ready}; claim={row.claim_status}"
            )

    if args.require_pass and policy_shock_gate_status() != "passed":
        print("\n".join(policy_shock_gate_blockers()), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
