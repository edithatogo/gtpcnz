from __future__ import annotations

import subprocess
import sys

from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_transforms import (
    check_source_transform_readiness,
    transform_public_source,
    verify_public_source_transform_scripts,
)


def test_public_source_transform_scripts_exist_for_every_plan() -> None:
    assert verify_public_source_transform_scripts() == ()


def test_public_source_transform_check_is_readiness_compatible() -> None:
    for plan in load_public_source_retrieval_plans():
        result = check_source_transform_readiness(plan.source_id)
        assert result.ok
        assert result.status in {
            "reference_pinned_pending_download",
            "raw_available_pending_source_specific_parser",
            "processed_ready",
        }


def test_public_source_transform_strict_mode_is_registry_driven() -> None:
    results = [check_source_transform_readiness(plan.source_id, require_raw=True) for plan in load_public_source_retrieval_plans()]
    assert all(result.status in {"blocked", "processed_ready", "raw_available_pending_source_specific_parser"} for result in results)


def test_public_source_transform_script_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_transform_scripts.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "public source transform script contract passed" in result.stdout


def test_source_specific_transform_entrypoint_is_checkable() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/transform_statsnz_population.py", "--check-only"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "src_statsnz_population transform readiness" in result.stdout


def test_nzhs_transform_writes_public_cost_barrier_aggregate() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/transform_nz_health_survey.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "cost_barrier_gp.csv" in result.stdout


def test_statsnz_transform_writes_schema_valid_public_aggregate() -> None:
    output = transform_public_source("src_statsnz_population")
    assert output.artifact.name == "population_estimates.csv"
    assert output.rows_written >= 1
    assert output.artifact.exists()
    assert output.artifact.with_suffix(output.artifact.suffix + ".hash").exists()
    assert (output.artifact.parent / "_metadata.yaml").exists()
