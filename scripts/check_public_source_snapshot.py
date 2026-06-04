from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.data.public_source_snapshot import (  # noqa: E402
    build_snapshot,
    verify_public_source_readiness,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate public-source snapshot readiness.")
    parser.add_argument("--verify-files", action="store_true", help="Require raw public source files for every source.")
    parser.add_argument("--verify-checksums", action="store_true", help="Require non-pending raw file checksums to match.")
    parser.add_argument("--verify-licences", action="store_true", help="Require licences to be in the allowed public set.")
    parser.add_argument("--verify-processed", action="store_true", help="Require processed files and companion hashes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    snapshot = build_snapshot()
    issues = []
    for source in snapshot.sources:
        if source.public_access_status not in {"public", "published", "open"}:
            issues.append(f"{source.source_id} is not public")
        if not source.licence_status:
            issues.append(f"{source.source_id} lacks licence status")
    issues.extend(
        verify_public_source_readiness(
            verify_files=args.verify_files,
            verify_checksums=args.verify_checksums,
            verify_licences=args.verify_licences,
            verify_processed=args.verify_processed,
        )
    )
    if issues:
        print("\n".join(issues))
        return 1
    print("public source snapshot contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
