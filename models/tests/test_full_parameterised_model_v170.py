from primarycare_model.full_parameterised_model_v170 import (
    PARAMETER_SPECS,
    DATA_INPUT_SPECS,
    SCENARIOS,
    parameter_register,
    data_input_contract,
    scenario_matrix,
    scenario_parameters,
    compute_architecture_indices,
    run_all_scenarios,
    sensitivity_analysis,
    calibration_target_matrix,
)


def test_parameter_register_is_large_and_bounded():
    df = parameter_register()
    assert len(df) >= 60
    assert df["name"].is_unique
    assert (df["lower_bound"] < df["upper_bound"]).all()
    assert ((df["current_value"] >= df["lower_bound"]) & (df["current_value"] <= df["upper_bound"])).all()


def test_data_input_contract_has_core_sources():
    df = data_input_contract()
    assert len(df) >= 10
    uses = " ".join(df["model_use"].tolist()).lower()
    assert "access" in uses
    assert "ambulance" in uses
    assert "capitation" in uses


def test_scenario_matrix_covers_all_parameters():
    df = scenario_matrix()
    param_names = [p.name for p in PARAMETER_SPECS]
    assert len(df) == len(SCENARIOS)
    assert set(param_names).issubset(set(df.columns))
    for p in PARAMETER_SPECS:
        assert df[p.name].between(p.lower_bound, p.upper_bound).all(), p.name


def test_indices_are_bounded():
    params = scenario_parameters("F4")
    idx = compute_architecture_indices(params)
    assert idx["hybrid_viability"] > 0
    for value in idx.values():
        assert 0 <= value <= 1


def test_full_hybrid_beats_current_reform():
    _monthly, summary = run_all_scenarios(months=24)
    s = summary.set_index("scenario_id")
    assert s.loc["F4", "hybrid_viability_score"] > s.loc["F0", "hybrid_viability_score"]
    assert s.loc["F4", "hospital_pressure_score"] < s.loc["F0", "hospital_pressure_score"]


def test_weak_control_has_higher_gaming_than_controlled_uncapped():
    _monthly, summary = run_all_scenarios(months=24)
    s = summary.set_index("scenario_id")
    assert s.loc["F5", "gaming_risk_score"] > s.loc["F3", "gaming_risk_score"]


def test_sensitivity_and_calibration_targets_exist():
    sens = sensitivity_analysis("F4")
    targets = calibration_target_matrix()
    assert len(sens) >= 2 * len(PARAMETER_SPECS)
    assert targets["calibration_target"].nunique() >= 8
