from __future__ import annotations

import subprocess
import sys

from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans
from models.primarycare_model.data.public_source_transforms import (
    check_source_transform_readiness,
    verify_public_source_transform_scripts,
)


def test_public_source_transform_scripts_exist_for_every_plan() -> None:
    assert verify_public_source_transform_scripts() == ()


def test_public_source_transform_check_is_readiness_compatible() -> None:
    for plan in load_public_source_retrieval_plans():
        result = check_source_transform_readiness(plan.source_id)
        assert result.ok
        assert result.status in {"reference_pinned_pending_download", "raw_available_pending_source_specific_parser"}


def test_public_source_transform_strict_mode_reports_missing_raw_files() -> None:
    results = [check_source_transform_readiness(plan.source_id, require_raw=True) for plan in load_public_source_retrieval_plans()]
    assert any(any("no raw public source files" in issue for issue in result.issues) for result in results)


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