from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.data.public_source_retrieval import verify_public_source_retrieval_plan  # noqa: E402


def main() -> int:
    issues = verify_public_source_retrieval_plan()
    if issues:
        print("\n".join(issues))
        return 1
    print("public source retrieval plan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
