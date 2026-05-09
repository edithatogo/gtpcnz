from primarycare_model.demonstrative_games import GAME_MODELS, SCENARIOS, run_all, summarise_by_scenario


def test_demonstrative_models_cover_all_games_and_scenarios():
    outcomes = run_all()
    assert len(GAME_MODELS) == 14
    assert len(SCENARIOS) == 5
    assert len(outcomes) == 14 * 5
    assert sorted({o.game_id for o in outcomes}, key=lambda x: int(x[1:])) == [f"G{i}" for i in range(1, 15)]


def test_outputs_are_bounded():
    for outcome in run_all():
        for metric in [
            outcome.access_score,
            outcome.provider_viability,
            outcome.equity_score,
            outcome.fiscal_control,
            outcome.hospital_pressure,
            outcome.gaming_risk,
            outcome.system_welfare,
        ]:
            assert 0 <= metric <= 100


def test_full_access_architecture_improves_mean_access_and_pressure_vs_status_quo():
    summary = summarise_by_scenario(run_all())
    assert summary["S3"]["mean_access_score"] > summary["S0"]["mean_access_score"]
    assert summary["S3"]["mean_hospital_pressure"] < summary["S0"]["mean_hospital_pressure"]


def test_loose_benefits_have_higher_gaming_risk_than_governed_architecture():
    summary = summarise_by_scenario(run_all())
    assert summary["S4"]["mean_gaming_risk"] > summary["S3"]["mean_gaming_risk"]
