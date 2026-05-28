from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    command: list[str]
    required: bool = True


CHECKS = [
    Check([sys.executable, "-m", "ruff", "check", "."]),
    Check([sys.executable, "-m", "basedpyright", "--pythonpath", sys.executable]),
    Check([sys.executable, "-m", "mypy", "models/primarycare_model/contracts", "models/primarycare_model/validation/pandera_schemas.py"]),
    Check([sys.executable, "scripts/check_repo_health.py"]),
    Check([sys.executable, "scripts/check_concern_boundaries.py"]),
    Check([sys.executable, "scripts/check_no_patient_data.py"]),
    Check([sys.executable, "-m", "pytest", "-q", "--cov=models.primarycare_model", "--cov-report=term-missing", "--cov-fail-under=90"]),
    Check([sys.executable, "-m", "pip_audit", "-r", "requirements.txt"]),
    Check([sys.executable, "-m", "py_compile", "streamlit_app.py", "models/primarycare_model/app.py"]),
    Check([sys.executable, "-m", "ty", "check", "models/primarycare_model"], required=False),
]


def main() -> int:
    for check in CHECKS:
        print(f"+ {' '.join(check.command)}")
        completed = subprocess.run(check.command, cwd=ROOT)
        if completed.returncode != 0 and check.required:
            return completed.returncode
        if completed.returncode != 0:
            print("  non-blocking canary failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
