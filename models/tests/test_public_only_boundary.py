from __future__ import annotations

import subprocess
import sys


def test_public_only_boundary_gate_passes() -> None:
    result = subprocess.run([sys.executable, "scripts/check_public_only_boundary.py"], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
