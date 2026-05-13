from pathlib import Path

import pandas as pd

from models.primarycare_model.scenario_service import (
    EXPECTED_SCENARIO_IDS,
    ToySettings,
    load_scenario_results,
    score_toy_settings,
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
            try:
                source.unlink()
            except PermissionError:
                # Windows/OneDrive can briefly hold the file after pandas reads it.
                pass
    assert "scenario_role" in loaded.columns
    assert "claim_boundary" in loaded.columns
    assert loaded["claim_boundary"].str.contains("not a real-data calibrated forecast").all()


def test_score_toy_settings_returns_scores_in_range():
    scores = score_toy_settings(
        ToySettings(
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
        "toy_supply_score",
        "toy_governance_score",
        "toy_equity_score",
        "toy_hospital_pressure_score",
        "toy_gaming_risk_score",
        "toy_viability_score",
    }
    assert all(0 <= value <= 100 for value in scores.values())
