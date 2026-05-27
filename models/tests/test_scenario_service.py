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
            try:
                source.unlink()
            except PermissionError:
                # Windows/OneDrive can briefly hold the file after pandas reads it.
                pass
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
