from dataclasses import replace

import numpy as np

from models.primarycare_model.runtime_lab import (
    MAX_ABM_POPULATION,
    MAX_MONTE_CARLO_DRAWS,
    SCENARIO_BY_ID,
    calculate_indices,
    calculation_trace,
    model_gap_map,
    run_agent_lens,
    run_reference_calculation,
    run_stochastic_uncertainty,
    run_stock_flow_trace,
)


def test_live_reference_calculation_has_expected_scenarios_and_bounds():
    result = run_reference_calculation(months=60)

    assert set(result["scenario_id"]) == {f"F{i}" for i in range(10)}
    assert result["rank_by_hybrid_viability"].min() == 1

    score_columns = [
        "hybrid_viability_score",
        "access_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    for column in score_columns:
        assert result[column].between(0, 100).all()


def test_calculation_trace_exposes_formula_sketches():
    trace = calculation_trace("F4")

    assert {"calculation", "formula_sketch", "index_value"}.issubset(trace.columns)
    assert "Hybrid viability" in set(trace["calculation"])
    assert trace["index_value"].between(0, 100).all()
    assert "threshold" in " ".join(trace["formula_sketch"]).lower()


def test_runtime_supply_response_is_nonlinear_in_activity_signal():
    base = SCENARIO_BY_ID["F4"]
    values = [
        calculate_indices(replace(base, activity_signal=activity))["supply_generation_score"]
        for activity in range(10, 91, 10)
    ]

    second_diff = np.diff(values, n=2)
    assert np.max(np.abs(second_diff)) > 0.5


def test_stochastic_uncertainty_is_seeded_and_capped():
    first, first_summary = run_stochastic_uncertainty("F4", draws=MAX_MONTE_CARLO_DRAWS + 100, seed=123)
    second, second_summary = run_stochastic_uncertainty("F4", draws=MAX_MONTE_CARLO_DRAWS + 100, seed=123)

    assert len(first) == MAX_MONTE_CARLO_DRAWS
    assert first.equals(second)
    assert first_summary.equals(second_summary)
    assert first["hybrid_viability_score"].between(0, 100).all()


def test_stock_flow_trace_has_monthly_pressure_outputs():
    trace = run_stock_flow_trace("F4", months=36)

    assert len(trace) == 36
    assert {"month", "unmet_need", "primary_capacity", "hospital_pressure", "fiscal_pressure"}.issubset(trace.columns)
    assert (trace["month"] == range(1, 37)).all()


def test_agent_lens_is_seeded_and_population_capped():
    agents, summary = run_agent_lens("F4", population_size=MAX_ABM_POPULATION + 50, months=12, seed=55)
    agents_again, summary_again = run_agent_lens("F4", population_size=MAX_ABM_POPULATION + 50, months=12, seed=55)

    assert len(agents) == MAX_ABM_POPULATION
    assert agents.equals(agents_again)
    assert summary.equals(summary_again)
    assert agents["access_probability"].between(0, 1).all()


def test_model_gap_map_covers_current_comprehensive_sota_and_bleeding_edge():
    gap_map = model_gap_map()

    assert {"Current", "Comprehensive", "SOTA", "Bleeding edge"}.issubset(set(gap_map["tier"]))
    assert "calculation audit overlay" in " ".join(gap_map["asset_or_gap"].str.lower())
