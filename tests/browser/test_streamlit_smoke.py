from __future__ import annotations

from models.primarycare_model.ui.cockpit import build_policy_cockpit_payload


def test_streamlit_cockpit_contract_smoke() -> None:
    payload = build_policy_cockpit_payload()
    assert "cockpit" in payload["sections"]
