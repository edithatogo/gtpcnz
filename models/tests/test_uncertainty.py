from primarycare_model.uncertainty import (
    PARAMETER_FIELDS,
    parameter_prior_rows,
    run_monte_carlo,
    rank_sensitivity,
    scenario_pairwise_probabilities,
    summarise_uncertainty,
)


def test_parameter_prior_rows_cover_parameters():
    rows = parameter_prior_rows()
    assert len(rows) == len(PARAMETER_FIELDS)
    assert {row["parameter"] for row in rows} == set(PARAMETER_FIELDS)


def test_monte_carlo_shape_small():
    draws = run_monte_carlo(n_per_scenario=2, seed=1)
    # 5 scenarios * 2 draws * 14 games
    assert len(draws) == 5 * 2 * 14
    assert "system_welfare" in draws.columns
    assert "marginal_contact_benefit" in draws.columns


def test_uncertainty_summary_has_scenarios():
    draws = run_monte_carlo(n_per_scenario=2, seed=1)
    summary = summarise_uncertainty(draws)
    assert len(summary) == 5
    assert "system_welfare_mean" in summary.columns


def test_sensitivity_and_probabilities():
    draws = run_monte_carlo(n_per_scenario=5, seed=2)
    sensitivity = rank_sensitivity(draws, top_n=3)
    probabilities = scenario_pairwise_probabilities(draws)
    assert len(probabilities) == 4
    assert sensitivity["rank_within_game"].max() <= 3
