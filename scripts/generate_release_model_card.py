from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_card() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    return f"""# GTPCNZ public model card v{version}

Claim level: public-data anchored benchmark.
Calibration status: calibration readiness unless public aggregate gates pass.
Not valid for: precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.
Inputs: public or published aggregate sources only.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    card = build_card()
    if args.check_only:
        print(card)
        return 0
    target = ROOT / "docs" / "release" / "model-card-v1.8.1.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(card, encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
