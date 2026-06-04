from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.calibration.public_aggregate_calibration import run_public_aggregate_calibration


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    result = run_public_aggregate_calibration()
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.check_only and result["calibration_status"] not in {"public_aggregate_validated", "calibration_readiness_only"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
