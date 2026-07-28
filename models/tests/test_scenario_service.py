from contextlib import suppress
from pathlib import Path

import numpy as np
import pandas as pd

from models.primarycare_model.scenario_service import (
    EXPECTED_SCENARIO_IDS,
    EducationalSettings,
    load_scenario_results,
    score_educational_settings,
    validate_scenario_results,
)


def minimal_results_frame():
    rows = []
    for idx, scenario_id in enumerate(sorted(EXPECTED_SCENARIO_IDS), start=1):
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": f"Scenario {scenario_id}",
                "description": "Test scenario",
                "hybrid_viability_score": 50 + idx,
                "access_score": 40,
                "supply_generation_score": 40,
                "equity_legitimacy_score": 40,
                "governance_resilience_score": 40,
                "hospital_deflection_score": 40,
                "fiscal_risk_score": 30,
                "gaming_risk_score": 30,
                "hospital_pressure_score": 70,
                "mean_last12_public_cost_index": 1.0,
                "rank_by_hybrid_viability": idx,
            }
        )
    return pd.DataFrame(rows)


def test_validate_scenario_results_accepts_expected_schema():
    df = minimal_results_frame()
    assert validate_scenario_results(df) == []


def test_load_scenario_results_adds_claim_boundary():
    df = minimal_results_frame()
    source = Path("codex-tmp") / "scenario-service-test-results.csv"
    source.parent.mkdir(exist_ok=True)
    try:
        df.to_csv(source, index=False)
        loaded = load_scenario_results(source)
    finally:
        if source.exists():
            with suppress(PermissionError):
                source.unlink()
    assert "scenario_role" in loaded.columns
    assert "claim_boundary" in loaded.columns
    assert loaded["claim_boundary"].str.contains("not linked-data calibrated", regex=False).all()
    assert loaded["claim_boundary"].str.contains("not a patient-level forecast", regex=False).all()


def test_score_educational_settings_returns_scores_in_range():
    scores = score_educational_settings(
        EducationalSettings(
            scheduled_benefit_level=60,
            capitation_support=70,
            place_accountability=70,
            audit_strength=80,
            equity_protection=80,
            scope_flexibility=60,
            local_in_person_support=60,
        )
    )
    assert set(scores) == {
        "educational_supply_score",
        "educational_governance_score",
        "educational_equity_score",
        "educational_hospital_pressure_score",
        "educational_gaming_risk_score",
        "educational_viability_score",
    }
    assert all(0 <= value <= 100 for value in scores.values())


def test_educational_supply_response_is_not_linear_in_scheduled_benefit():
    values = [
        score_educational_settings(
            EducationalSettings(
                scheduled_benefit_level=benefit,
                capitation_support=70,
                place_accountability=70,
                audit_strength=80,
                equity_protection=80,
                scope_flexibility=60,
                local_in_person_support=60,
            )
        )["educational_supply_score"]
        for benefit in range(10, 91, 10)
    ]
    second_diff = np.diff(values, n=2)

    assert np.max(np.abs(second_diff)) > 0.5

def test_load_scenario_results_missing_file():
    df = load_scenario_results("non_existent_file.csv")
    assert df.empty
    from models.primarycare_model.scenario_service import REQUIRED_SCENARIO_COLUMNS
    assert list(df.columns) == sorted(REQUIRED_SCENARIO_COLUMNS)

def test_load_scenario_results_validation_error():
    df = pd.DataFrame({"scenario_id": ["F1"]})
    source = Path("codex-tmp") / "scenario-service-test-results-bad.csv"
    source.parent.mkdir(exist_ok=True)
    try:
        df.to_csv(source, index=False)
        import pytest
        with pytest.raises(ValueError, match="Scenario results failed validation"):
            load_scenario_results(source)
    finally:
        if source.exists():
            with suppress(PermissionError):
                source.unlink()

def test_validate_scenario_results_with_nulls():
    df = minimal_results_frame()
    df.loc[0, "hybrid_viability_score"] = None
    issues = validate_scenario_results(df)
    assert len(issues) > 0
    assert "hybrid_viability_score contains null values" in issues

def test_score_legacy_settings():
    from models.primarycare_model.scenario_service import _score_legacy_settings
    settings = EducationalSettings(
        scheduled_benefit_level=60,
        capitation_support=70,
        place_accountability=70,
        audit_strength=80,
        equity_protection=80,
        scope_flexibility=60,
        local_in_person_support=60,
    )
    scores = _score_legacy_settings(settings)
    assert "toy_supply_score" in scores
    assert "educational_supply_score" not in scores

def test_load_first_existing():
    from models.primarycare_model.scenario_service import load_first_existing
    df = load_first_existing(["non_existent_1.csv", "non_existent_2.csv"])
    assert df.empty

    source = Path("codex-tmp") / "scenario-service-test-existing.csv"
    source.parent.mkdir(exist_ok=True)
    pd.DataFrame({"a": [1]}).to_csv(source, index=False)
    try:
        df = load_first_existing(["non_existent_1.csv", source])
        assert not df.empty
        assert "a" in df.columns
    finally:
        if source.exists():
            with suppress(PermissionError):
                source.unlink()

def test_build_calibration_readiness_table():
    from models.primarycare_model.scenario_service import build_calibration_readiness_table
    df = build_calibration_readiness_table()
    assert not df.empty
    assert list(df.columns) == ["domain", "input", "status", "why_it_matters"]
    assert len(df) == 8

def test_summarise_reference_results():
    from models.primarycare_model.scenario_service import summarise_reference_results
    df = pd.DataFrame()
    assert summarise_reference_results(df).empty

    df = minimal_results_frame()
    df["scenario_role"] = "Test Role"
    summary = summarise_reference_results(df)
    assert not summary.empty
    expected_cols = [
        "rank_by_hybrid_viability",
        "scenario_id",
        "scenario_name",
        "scenario_role",
        "hybrid_viability_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    assert list(summary.columns) == expected_cols
    assert list(summary["rank_by_hybrid_viability"]) == sorted(summary["rank_by_hybrid_viability"])

def test_normalized_slider_value_zero_span(monkeypatch):
    from models.primarycare_model.scenario_service import _normalized_slider_value, EducationalLeverDefinition, EDUCATIONAL_LEVER_DEFINITION_MAP

    mock_def = EducationalLeverDefinition(
        field_name="mock_lever",
        public_label="Mock",
        health_economics_meaning="Mock",
        high_value_meaning="Mock",
        educational_output_effect="Mock",
        slider_help="Mock",
        lower_bound=50,
        upper_bound=50,
    )

    EDUCATIONAL_LEVER_DEFINITION_MAP["mock_lever"] = mock_def

    class MockSettings:
        mock_lever = 50

    try:
        val = _normalized_slider_value(MockSettings(), "mock_lever")
        assert val == 0.0
    finally:
        del EDUCATIONAL_LEVER_DEFINITION_MAP["mock_lever"]
