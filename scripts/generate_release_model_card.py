from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.calibration.public_aggregate_calibration import (  # noqa: E402
    run_public_aggregate_calibration,
)


def build_card() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    calibration = run_public_aggregate_calibration()
    validation_gates = "\n".join(
        f"- {row['gate_id']}: {row['status']} ({row['gate_family']})"
        for row in calibration["validation_gates"]
    )
    not_valid_for = ", ".join(str(item) for item in calibration["not_valid_for"])
    return f"""# GTPCNZ public model card v{version}

Claim level: {calibration["claim_level"]}.
Calibration status: {calibration["calibration_status"]}.
Interpretation: {calibration["interpretation_note"]}
Not valid for: {not_valid_for}.
Inputs: public or published aggregate sources only.

## Validation gates

{validation_gates}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    card = build_card()
    if args.check_only:
        print(card)
        return 0
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    target = ROOT / "docs" / "release" / f"model-card-v{version}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(card, encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
