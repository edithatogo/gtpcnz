from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.ui.accessibility import validate_chart_payload
from models.primarycare_model.ui.cockpit import build_policy_cockpit_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.parse_args()
    payload = build_policy_cockpit_payload()
    issues = []
    for chart in payload["charts"]:
        issues.extend(validate_chart_payload(chart))
    if issues:
        print("\n".join(issues))
        return 1
    print("accessibility/chart fallback contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
