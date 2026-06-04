from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_conductor_parallel_track_gate_passes() -> None:
    result = subprocess.run([sys.executable, "scripts/check_conductor_parallel_tracks.py"], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_release_track_waits_for_visual_and_dependency_tracks() -> None:
    matrix = json.loads(Path("conductor/parallel-execution-matrix.json").read_text(encoding="utf-8"))
    release = matrix["tracks"]["059-release-engineering-and-model-cards"]
    assert "056-streamlit-policy-cockpit-and-visual-grammar" in release["depends_on"]
    assert "061-visual-regression-accessibility-and-browser-tests" in release["depends_on"]
    assert "062-dependency-locking-and-reproducible-runtime" in release["depends_on"]
