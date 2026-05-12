from pathlib import Path

import pandas as pd

from models.primarycare_model.scenario_service import EXPECTED_SCENARIO_IDS, validate_scenario_results


def test_public_scenario_csv_contains_expected_scenarios():
    path = Path("outputs/full-parameterised-summary-results-v1.7.0.csv")
    assert path.exists(), "Expected public scenario-output CSV is missing"
    df = pd.read_csv(path)
    assert validate_scenario_results(df) == []
    assert EXPECTED_SCENARIO_IDS.issubset(set(df["scenario_id"].astype(str)))


def test_weak_control_scenario_has_high_gaming_risk_relative_to_full_hybrid():
    df = pd.read_csv("outputs/full-parameterised-summary-results-v1.7.0.csv")
    full = df.loc[df["scenario_id"] == "F4"].iloc[0]
    weak = df.loc[df["scenario_id"] == "F5"].iloc[0]
    assert weak["gaming_risk_score"] > full["gaming_risk_score"]
