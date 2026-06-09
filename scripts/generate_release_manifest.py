from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.calibration.public_aggregate_calibration import (  # noqa: E402
    run_public_aggregate_calibration,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def build_manifest() -> dict[str, object]:
    calibration = run_public_aggregate_calibration()
    return {
        "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "claim_level": str(calibration["claim_level"]),
        "calibration_status": str(calibration["calibration_status"]),
        "not_valid_for": list(calibration["not_valid_for"]),
        "source_snapshot_hash": sha(ROOT / "models" / "primarycare_model" / "registries" / "public" / "sources.public.v1.yaml"),
        "parameter_hash": sha(ROOT / "models" / "primarycare_model" / "registries" / "public" / "parameters.public.v1.yaml"),
        "model_hash": sha(ROOT / "models" / "primarycare_model" / "ui" / "cockpit.py"),
        "output_hash": sha(ROOT / "data" / "snapshots" / "public-source-snapshot-v1.json"),
        "test_status": "not-run-by-manifest-generator",
        "visual_regression_status": "gate-present",
        "accessibility_status": "gate-present",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    manifest = build_manifest()
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if args.check_only:
        return 0 if all(value != "missing" for value in manifest.values()) else 1
    target = ROOT / "docs" / "release" / f"release-manifest-v{manifest['version']}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
