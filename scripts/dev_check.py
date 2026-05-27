from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    [sys.executable, "scripts/check_repo_health.py"],
    [sys.executable, "scripts/check_concern_boundaries.py"],
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "-m", "py_compile", "streamlit_app.py", "models/primarycare_model/app.py"],
]


def main() -> int:
    for command in COMMANDS:
        print(f"+ {' '.join(command)}")
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
