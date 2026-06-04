from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    app_version = (ROOT / "models" / "primarycare_model" / "version.py").read_text(encoding="utf-8")
    issues = []
    if f'version = "{version}"' not in pyproject:
        issues.append("pyproject.toml version mismatch")
    if re.search(r'__version__\s*=\s*"' + re.escape(version) + r'"', app_version) is None:
        issues.append("models/primarycare_model/version.py mismatch")
    if issues:
        print("\n".join(issues))
        return 1
    print(f"version consistency passed: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
