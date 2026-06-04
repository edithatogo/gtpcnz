from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.voi.full_voi import run_full_voi


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    result = run_full_voi()
    print(json.dumps(result.model_dump(), indent=2, sort_keys=True))
    return 0 if result.evpi >= 0 and result.label.endswith("not a forecast") else 1


if __name__ == "__main__":
    raise SystemExit(main())
