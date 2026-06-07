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


def test_transformed_schema_gate_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_transformed_schemas.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_source_transform_script_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_transform_scripts.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_source_fetch_script_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_fetch_scripts.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_source_readiness_matrix_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_readiness_matrix.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
