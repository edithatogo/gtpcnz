"""Sync root source files to public/gtpcnz mirror."""
from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "public" / "gtpcnz"
COPY_MAP = [
    (ROOT / "streamlit_app.py", MIRROR / "streamlit_app.py"),
    (ROOT / "pyproject.toml", MIRROR / "pyproject.toml"),
    (ROOT / "uv.lock", MIRROR / "uv.lock"),
    (ROOT / "models" / "primarycare_model" / "app.py", MIRROR / "models" / "primarycare_model" / "app.py"),
    (ROOT / "models" / "primarycare_model" / "runtime_lab.py", MIRROR / "models" / "primarycare_model" / "runtime_lab.py"),
    (ROOT / "models" / "primarycare_model" / "scenario_service.py", MIRROR / "models" / "primarycare_model" / "scenario_service.py"),
    (ROOT / "models" / "primarycare_model" / "__init__.py", MIRROR / "models" / "primarycare_model" / "__init__.py"),
]
for sub in [
    "calibration",
    "contracts",
    "data",
    "evidence",
    "registries",
    "ui",
    "uncertainty",
    "validation",
    "voi",
]:
    src_dir = ROOT / "models" / "primarycare_model" / sub
    dst_dir = MIRROR / "models" / "primarycare_model" / sub
    if src_dir.exists():
        for pattern in ["**/*.py", "**/*.yaml"]:
            for f in src_dir.glob(pattern):
                COPY_MAP.append((f, dst_dir / f.relative_to(src_dir)))
def main() -> int:
    check_only = "--check" in sys.argv
    failures = 0
    for src, dst in COPY_MAP:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            print(f"MISSING SOURCE {src}")
            failures += 1
            continue
        if dst.exists() and filecmp.cmp(src, dst, shallow=False):
            rel = str(dst.relative_to(MIRROR))
            print(f"OK  {rel}")
        elif check_only:
            rel = str(dst.relative_to(MIRROR))
            print(f"DRIFT {rel}")
            failures += 1
        else:
            src_rel = str(src.relative_to(ROOT))
            dst_rel = str(dst.relative_to(MIRROR))
            shutil.copy2(src, dst)
            print(f"COPY {src_rel} -> {dst_rel}")
    if check_only:
        outcome = "FAILED" if failures else "PASSED"
        print("")
        print(f"Result: {outcome} ({failures} drift items)")
    else:
        print("")
        print(f"Sync complete. {failures} errors.")
    return 1 if failures else 0
if __name__ == "__main__":
    sys.exit(main())
