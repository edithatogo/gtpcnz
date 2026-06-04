from __future__ import annotations

from models.primarycare_model.evidence.public_evidence_monitor import detect_public_evidence_candidates


def test_public_evidence_monitor_is_review_only() -> None:
    candidates = detect_public_evidence_candidates()
    assert candidates
    assert all(candidate.review_required for candidate in candidates)
    assert all(not candidate.may_update_model for candidate in candidates)
