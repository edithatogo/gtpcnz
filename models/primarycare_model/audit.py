"""Audit helpers for claim-source ledgers.

These helpers keep the non-code audit artefacts lightly testable. They do not
replace substantive research review.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

VALID_EVIDENCE_LEVELS = {"1", "2", "3", "4", "5"}


@dataclass(frozen=True)
class AuditClaim:
    """A research or policy claim in the audit ledger."""

    claim_id: str
    short_name: str
    evidence_level: str
    source_ids: tuple[str, ...]
    linked_games: tuple[str, ...]
    test_or_next_step: str

    @property
    def is_empirical_fact(self) -> bool:
        """Return whether the claim is coded as publicly documented fact."""

        return self.evidence_level == "1"

    @property
    def requires_validation(self) -> bool:
        """Return whether the claim requires further empirical or policy validation."""

        return self.evidence_level in {"3", "4", "5"}


def _split_ids(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.replace(",", ";").split(";") if part.strip())


def load_claims(path: str | Path) -> tuple[AuditClaim, ...]:
    """Load the claim-source ledger from CSV."""

    claims: list[AuditClaim] = []
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            claims.append(
                AuditClaim(
                    claim_id=row["Claim_ID"],
                    short_name=row["Short_Name"],
                    evidence_level=row["Evidence_Level"],
                    source_ids=_split_ids(row["Source_IDs"]),
                    linked_games=_split_ids(row["Linked_Games"]),
                    test_or_next_step=row["Test_or_Next_Step"],
                )
            )
    return tuple(claims)


def validate_claims(claims: tuple[AuditClaim, ...]) -> list[str]:
    """Return validation errors for a set of claims."""

    errors: list[str] = []
    seen: set[str] = set()
    for claim in claims:
        if claim.claim_id in seen:
            errors.append(f"duplicate claim_id: {claim.claim_id}")
        seen.add(claim.claim_id)
        if claim.evidence_level not in VALID_EVIDENCE_LEVELS:
            errors.append(f"invalid evidence level for {claim.claim_id}: {claim.evidence_level}")
        if not claim.source_ids:
            errors.append(f"missing source ids for {claim.claim_id}")
        if not claim.linked_games:
            errors.append(f"missing linked games for {claim.claim_id}")
        if not claim.test_or_next_step:
            errors.append(f"missing test/next step for {claim.claim_id}")
    return errors
