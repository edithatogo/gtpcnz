from primarycare_model.calibration_v150 import make_synthetic_observations, calibrate_grid, objective, STARTING_PRIOR, DEFAULT_BASELINE, run_calibration_demo

def test_synthetic_observations_have_expected_columns():
    df = make_synthetic_observations(6)
    assert len(df) == 6
    assert {'primary_contacts','ed_presentations','public_cost'}.issubset(df.columns)

def test_calibration_improves_objective():
    obs = make_synthetic_observations(12)
    fitted = calibrate_grid(obs)
    assert objective(fitted, obs, DEFAULT_BASELINE) <= objective(STARTING_PRIOR, obs, DEFAULT_BASELINE)

def test_run_calibration_demo_outputs_tables():
    observed, pred, params, scen = run_calibration_demo(8)
    assert len(observed) == len(pred) == 8
    assert len(params) >= 6
    assert set(scen['scenario']) == {'baseline','full_hybrid'}
