from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.generate_release_manifest import build_manifest
from scripts.generate_release_model_card import build_card

ROOT = Path(__file__).resolve().parents[2]


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


def test_calibration_target_readiness_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_target_readiness.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_temporal_period_acquisition_gate_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_temporal_period_acquisition.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_calibration_validation_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_calibration_validation_gates.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_policy_shock_plausibility_gate_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_policy_shock_plausibility.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_posterior_predictive_check_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_posterior_predictive_checks.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_release_model_card_reflects_public_aggregate_validation_without_precision_claims() -> None:
    card = build_card()

    assert "Claim level: empirically_supported_if_gated" in card
    assert "Calibration status: public_aggregate_validated" in card
    assert "CAL-G-005: passed" in card
    assert "Not valid for:" in card
    assert "precise fiscal savings" in card
    assert "causal effects" in card


def test_release_manifest_records_claim_metadata() -> None:
    manifest = build_manifest()

    assert manifest["claim_level"] == "empirically_supported_if_gated"
    assert manifest["calibration_status"] == "public_aggregate_validated"
    assert "precise fiscal savings" in manifest["not_valid_for"]
    assert "causal effects" in manifest["not_valid_for"]


def test_release_site_sources_expose_aggregate_validation_boundary() -> None:
    index = (ROOT / "index.qmd").read_text(encoding="utf-8")
    report = (ROOT / "reports" / "primary_care_architecture.qmd").read_text(
        encoding="utf-8"
    )
    site_map = (
        ROOT / "docs" / "public-site" / "site-map-and-release-manifest-v1.8.4.md"
    ).read_text(encoding="utf-8")
    quarto = (ROOT / "_quarto.yml").read_text(encoding="utf-8")

    assert "docs/release/model-card-v1.8.1.md" in quarto
    assert "docs/release/track-071-release-regeneration-v1.md" in quarto
    assert "public_aggregate_validated" in index
    assert "empirically_supported_if_gated" in report
    assert "precise fiscal savings" in report
    assert "causal effects" in site_map
