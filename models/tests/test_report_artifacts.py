from __future__ import annotations

from pathlib import Path


def test_public_report_artifacts_exist() -> None:
    assert Path("reports/public_aggregate_model_report.qmd").exists()
    assert Path("docs/release/model-card-template.qmd").exists()
