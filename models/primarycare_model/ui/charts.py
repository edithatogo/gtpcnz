"""Chart contract helpers for the Streamlit policy cockpit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.primarycare_model.ui.claim_badges import claim_badge_payload


@dataclass(frozen=True)
class ChartContract:
    title: str
    unit: str
    source_snapshot_id: str
    interpretation_note: str
    data: tuple[dict[str, Any], ...]
    claim_level: str = "empirically_supported_if_gated"
    calibration_status: str = "public_aggregate_validated"
    uncertainty_type: str = "parameter_and_structural"

    def as_payload(self) -> dict[str, Any]:
        payload = {
            "title": self.title,
            "unit": self.unit,
            "source_snapshot_id": self.source_snapshot_id,
            "interpretation_note": self.interpretation_note,
            "downloadable_data": list(self.data),
            "table_fallback": list(self.data),
        }
        payload.update(claim_badge_payload(self.claim_level, self.calibration_status, self.uncertainty_type))
        return payload
