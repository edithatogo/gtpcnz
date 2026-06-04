from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.evidence.public_evidence_monitor import detect_public_evidence_candidates


def main() -> int:
    candidates = [item.model_dump() for item in detect_public_evidence_candidates()]
    print(json.dumps(candidates, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
