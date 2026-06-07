from __future__ import annotations

import subprocess
import sys


def test_version_consistency_gate_passes() -> None:
    result = subprocess.run([sys.executable, "scripts/check_version_consistency.py"], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_source_retrieval_plan_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_retrieval_plan.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
