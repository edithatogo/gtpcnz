"""Readiness-only public policy-shock plausibility evidence for CAL-G-005."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any, Literal, cast

import yaml

from models.primarycare_model.data.public_source_readiness_matrix import build_public_source_readiness_matrix
from models.primarycare_model.data.public_source_snapshot import PUBLIC_REGISTRY

REGISTRY_PATH = PUBLIC_REGISTRY / "policy_shock_plausibility.public.v1.yaml"

PolicyShockComparisonStatus = Literal["readiness_only", "numeric_ready", "passed", "comparison_failed"]
PolicyShockGateStatus = Literal[
    "passed",
    "public_data_unavailable",
    "public_validation_source_registered",
    "public_validation_numeric_ready",
    "public_holdout_comparison_failed",
]


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


def build_public_policy_shock_evidence() -> tuple[PublicPolicyShockEvidence, ...]:
    """Return registered public policy-shock evidence without promoting claims."""

    readiness = {row.source_id: row for row in build_public_source_readiness_matrix(strict=False)}
    evidence: list[PublicPolicyShockEvidence] = []
    for row in _registry_rows():
        source_id = str(row["source_id"])
        source_ready = bool(readiness.get(source_id) and readiness[source_id].source_ready)
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
                comparison_artifact=_optional_str(row["comparison_artifact"]),
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
    if any(row.comparison_status == "comparison_failed" for row in rows):
        return "public_holdout_comparison_failed"
    if rows and all(row.comparison_status == "passed" and row.source_ready for row in rows):
        return "passed"
    if any(row.comparison_status == "numeric_ready" for row in rows):
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
            if row.comparison_status == "comparison_failed"
        )
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
