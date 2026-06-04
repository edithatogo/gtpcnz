from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = ROOT / "models" / "primarycare_model" / "registries" / "public"
FORBIDDEN = {
        "sensitive", "confidential", "private_admin", "patient" + "_level", "linked_data",
    "stakeholder", "unpublished_expert_elicitation", "calibrated_from_private", "calibrated",
}


def walk_values(obj: Any) -> list[str]:
    if isinstance(obj, dict):
        values = []
        for item in obj.values():
            values.extend(walk_values(item))
        return values
    if isinstance(obj, list):
        values = []
        for item in obj:
            values.extend(walk_values(item))
        return values
    if isinstance(obj, str):
        return [obj]
    return []


def main() -> int:
    issues: list[str] = []
    for path in sorted(PUBLIC_ROOT.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        for value in walk_values(payload):
            if value in FORBIDDEN:
                issues.append(f"{path.relative_to(ROOT)} contains forbidden public value {value!r}")
    if issues:
        print("\n".join(issues))
        return 1
    print("public-only boundary passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
