from __future__ import annotations

import shutil
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from models.primarycare_model.data.public_processed_schema import (
    processed_dataset_expectations,
    validate_processed_input_schemas,
)

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "models" / "primarycare_model" / "registries" / "public"
WORKSPACE_TMP = ROOT / "codex-tmp"


@contextmanager
def workspace_tmp_dir() -> Iterator[Path]:
    path = WORKSPACE_TMP / f"processed-schema-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_processed_dataset_expectations_are_registry_driven() -> None:
    expectations = processed_dataset_expectations(registry_root=REGISTRY)
    ids = {expectation.dataset.dataset_id for expectation in expectations}
    assert ids == {"population_denominators_public", "primary_care_access_public"}
    assert all(str(expectation.artifact).endswith(".csv") for expectation in expectations)


def test_processed_schema_default_allows_missing_readiness_artifacts() -> None:
    with workspace_tmp_dir() as processed_root:
        assert validate_processed_input_schemas(registry_root=REGISTRY, processed_root=processed_root) == ()


def test_processed_schema_strict_reports_missing_artifacts() -> None:
    with workspace_tmp_dir() as processed_root:
        issues = validate_processed_input_schemas(
            registry_root=REGISTRY,
            processed_root=processed_root,
            require_processed=True,
        )
    assert any("population_denominators_public: missing processed artifact" in issue for issue in issues)
    assert any("primary_care_access_public: missing processed artifact" in issue for issue in issues)


def test_processed_schema_accepts_valid_public_aggregate_csv() -> None:
    with workspace_tmp_dir() as processed_root:
        population_dir = processed_root / "src_statsnz_population"
        access_dir = processed_root / "src_nz_health_survey"
        population_dir.mkdir(parents=True)
        access_dir.mkdir(parents=True)
        (population_dir / "population_estimates.csv").write_text(
            "jurisdiction,year,population_count\nNZ,2024,5200000\n",
            encoding="utf-8",
        )
        (population_dir / "_metadata.yaml").write_text("source_id: src_statsnz_population\n", encoding="utf-8")
        (access_dir / "cost_barrier_gp.csv").write_text(
            "indicator_id,year,value\ngp_cost_barrier,2024,0.18\n",
            encoding="utf-8",
        )
        (access_dir / "_metadata.yaml").write_text("source_id: src_nz_health_survey\n", encoding="utf-8")

        assert validate_processed_input_schemas(registry_root=REGISTRY, processed_root=processed_root, require_processed=True) == ()


def test_processed_schema_rejects_person_level_columns() -> None:
    with workspace_tmp_dir() as processed_root:
        population_dir = processed_root / "src_statsnz_population"
        access_dir = processed_root / "src_nz_health_survey"
        population_dir.mkdir(parents=True)
        access_dir.mkdir(parents=True)
        (population_dir / "population_estimates.csv").write_text(
            "jurisdiction,year,population_count,patient_id\nNZ,2024,5200000,abc\n",
            encoding="utf-8",
        )
        (population_dir / "_metadata.yaml").write_text("source_id: src_statsnz_population\n", encoding="utf-8")
        (access_dir / "cost_barrier_gp.csv").write_text(
            "indicator_id,year,value\ngp_cost_barrier,2024,0.18\n",
            encoding="utf-8",
        )
        (access_dir / "_metadata.yaml").write_text("source_id: src_nz_health_survey\n", encoding="utf-8")

        issues = validate_processed_input_schemas(registry_root=REGISTRY, processed_root=processed_root, require_processed=True)
    assert any("forbidden person-level columns" in issue for issue in issues)
