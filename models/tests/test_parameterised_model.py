from primarycare_model.parameterised_model import (
    PARAMETERISED_SCENARIOS,
    parameter_input_frame,
    scenario_input_frame,
    run_parameterised_game_models,
    run_parameterised_hybrid_model,
    hybrid_informed_mcda,
)
from primarycare_model.uncertainty import PARAMETER_FIELDS


def test_parameter_input_register_covers_all_scenario_fields():
    params = set(parameter_input_frame()["parameter"])
    assert set(PARAMETER_FIELDS) == params


def test_parameterised_scenarios_are_bounded():
    df = scenario_input_frame()
    assert len(df) >= 9
    for field in PARAMETER_FIELDS:
        assert df[field].between(0, 1).all(), field


def test_parameterised_game_results_cover_all_games_and_scenarios():
    df = run_parameterised_game_models()
    assert df["scenario_id"].nunique() == len(PARAMETERISED_SCENARIOS)
    assert df["game_id"].nunique() == 14
    assert len(df) == len(PARAMETERISED_SCENARIOS) * 14


def test_full_upstream_scenario_scores_higher_than_current_baseline():
    df = run_parameterised_hybrid_model().set_index("scenario_id")
    assert df.loc["P3", "hybrid_viability_score"] > df.loc["P0", "hybrid_viability_score"]
    assert df.loc["P3", "weighted_hospital_pressure"] < df.loc["P0", "weighted_hospital_pressure"]


def test_hybrid_informed_mcda_ranks_full_architecture_first():
    df = hybrid_informed_mcda()
    first = df.sort_values("rank").iloc[0]
    assert first["scenario_id"] == "P3"
