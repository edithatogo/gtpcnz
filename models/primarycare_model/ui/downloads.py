"""Download payload helpers."""

from __future__ import annotations

import json
from typing import Any


def scenario_report_card(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)
