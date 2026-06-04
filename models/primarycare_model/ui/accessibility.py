"""Accessibility contract checks for cockpit payloads."""

from __future__ import annotations

REQUIRED_CHART_FIELDS = {
    "title", "unit", "claim_level", "calibration_status", "uncertainty_type",
    "source_snapshot_id", "interpretation_note", "not_valid_for_warning",
    "downloadable_data", "table_fallback",
}


def validate_chart_payload(payload: dict[str, object]) -> list[str]:
    return sorted(field for field in REQUIRED_CHART_FIELDS if field not in payload)
