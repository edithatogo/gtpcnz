"""Human-reviewed public evidence monitoring."""

from __future__ import annotations

from models.primarycare_model.contracts.evidence_candidates import EvidenceCandidate
from models.primarycare_model.data.public_source_snapshot import load_public_sources


def detect_public_evidence_candidates() -> tuple[EvidenceCandidate, ...]:
    candidates = []
    for source in load_public_sources():
        if source.checksum == "pending-download":
            candidates.append(EvidenceCandidate(
                candidate_id=f"candidate-{source.source_id}",
                source=source.source_id,
                relevance=0.75,
                quality="public-source-metadata-needs-download-checksum",
                transferability=0.7,
                contradiction_signal="none_detected",
                affected_parameters=(),
            ))
    return tuple(candidates)
