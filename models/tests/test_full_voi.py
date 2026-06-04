from __future__ import annotations

from models.primarycare_model.voi.full_voi import run_full_voi


def test_full_voi_is_seeded_and_complete() -> None:
    first = run_full_voi(seed=42)
    second = run_full_voi(seed=42)
    assert first == second
    assert first.evpi >= 0
    assert first.evppi
    assert first.evsi
    assert first.enbs
    assert 0 <= first.decision_error_probability <= 1
    assert first.label == "decision-uncertainty analysis, not a forecast"
