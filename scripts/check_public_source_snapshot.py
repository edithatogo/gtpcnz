from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.data.public_source_snapshot import build_snapshot


def main() -> int:
    snapshot = build_snapshot()
    issues = []
    for source in snapshot.sources:
        if source.public_access_status not in {"public", "published", "open"}:
            issues.append(f"{source.source_id} is not public")
        if not source.licence_status:
            issues.append(f"{source.source_id} lacks licence status")
    if issues:
        print("\n".join(issues))
        return 1
    print("public source snapshot contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
