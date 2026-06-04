from __future__ import annotations

from models.primarycare_model.ui.accessibility import validate_chart_payload
from models.primarycare_model.ui.cockpit import REQUIRED_SECTIONS, REQUIRED_VISUALS, build_policy_cockpit_payload


def test_policy_cockpit_payload_has_sections_and_chart_contracts() -> None:
    payload = build_policy_cockpit_payload()
    assert set(REQUIRED_SECTIONS).issubset(set(payload["sections"]))
    assert {chart["title"] for chart in payload["charts"]} == set(REQUIRED_VISUALS)
    for chart in payload["charts"]:
        assert validate_chart_payload(chart) == []
        assert chart["table_fallback"]
        assert chart["downloadable_data"]
