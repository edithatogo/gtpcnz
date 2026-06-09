"""CLI gate for independent public validation-source candidates."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models.primarycare_model.data.public_validation_sources import verify_public_validation_source_candidates  # noqa: E402, I001


def main() -> int:
    issues = verify_public_validation_source_candidates()
    if issues:
        for issue in issues:
            print(issue)
        return 1
    print("public validation source candidate contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
