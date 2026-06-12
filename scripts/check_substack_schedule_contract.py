"""Validate Substack launch schedules against public-post contracts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEDULES = [ROOT / "launch-schedule-v1.7.2.json"]
CURRENT_POST_DIR = "docs/substack-ready/posts-v1.8.1-applied/"
CURRENT_MODEL_TERMS = ("public_aggregate_validated", "empirically_supported_if_gated")


def schedule_paths() -> list[Path]:
    if len(sys.argv) > 1:
        return [Path(arg) if Path(arg).is_absolute() else ROOT / arg for arg in sys.argv[1:]]
    return DEFAULT_SCHEDULES


def local_post_path(post_path: str) -> Path:
    prefix = "rareinsights/primary-care-funding-architecture-v1.7.2/"
    relative = post_path.removeprefix(prefix)
    return ROOT / relative


def validate_schedule(path: Path) -> list[str]:
    failures: list[str] = []
    rows = json.loads(path.read_text(encoding="utf-8"))
    for row in rows:
        post_number = str(row.get("postNumber", "")).zfill(2)
        if post_number == "00":
            continue
        label = f"{path.name} sequence {row.get('sequence')} post {post_number}"
        post_path = str(row.get("postPath", ""))
        subtitle = str(row.get("subtitle", ""))
        title = str(row.get("title", ""))
        if "appendices-" in post_path:
            failures.append(f"{label}: public schedule points to appendix path: {post_path}")
        if "technical appendix" in f"{title} {subtitle}".lower():
            failures.append(f"{label}: public title/subtitle contains 'technical appendix'")
        if CURRENT_POST_DIR not in post_path:
            failures.append(f"{label}: postPath does not use current applied v1.8.1 post directory")
            continue
        markdown_path = local_post_path(post_path)
        if not markdown_path.exists():
            failures.append(f"{label}: postPath target is missing: {markdown_path.relative_to(ROOT)}")
            continue
        markdown = markdown_path.read_text(encoding="utf-8")
        for term in CURRENT_MODEL_TERMS:
            if term not in markdown:
                failures.append(f"{label}: missing current model contract term {term}")
    return failures


def main() -> int:
    failures: list[str] = []
    for path in schedule_paths():
        if not path.exists():
            failures.append(f"Schedule not found: {path}")
            continue
        failures.extend(validate_schedule(path))
    if failures:
        print("Substack schedule contract failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Substack schedule contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
