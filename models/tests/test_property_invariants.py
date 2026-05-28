from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from models.primarycare_model.runtime_lab import (
    SCENARIOS,
    calculate_indices,
    clamp,
    diminishing_return,
    format_formula_markdown,
    get_calculation_details,
    get_runtime_scenario,
    run_stochastic_replay,
    run_stochastic_uncertainty,
    strategic_response,
    validate_slider_value,
)
from models.primarycare_model.scenario_service import (
    build_calibration_readiness_table,
    load_first_existing,
    summarise_reference_results,
)

FINITE_FLOATS = st.floats(
    min_value=-10_000,
    max_value=10_000,
    allow_nan=False,
    allow_infinity=False,
    width=32,
)


@given(value=FINITE_FLOATS, lower=st.floats(min_value=-1000, max_value=0, allow_nan=False), upper=st.floats(min_value=1, max_value=1000, allow_nan=False))
def test_clamp_respects_bounds(value: float, lower: float, upper: float) -> None:
    bounded = clamp(value, lower, upper)
    assert lower <= bounded <= upper


@given(value=st.floats(min_value=-5, max_value=5, allow_nan=False, allow_infinity=False))
def test_diminishing_return_is_bounded(value: float) -> None:
    result = diminishing_return(value)
    assert 0.0 <= result <= 1.0


@given(value=st.floats(min_value=-5, max_value=5, allow_nan=False, allow_infinity=False))
def test_strategic_response_is_bounded(value: float) -> None:
    result = strategic_response(value)
    assert 0.0 <= result <= 1.0


@given(scenario_index=st.integers(min_value=0, max_value=max(0, len(SCENARIOS) - 1)))
def test_calculated_indices_stay_on_0_to_100_scale(scenario_index: int) -> None:
    scores = calculate_indices(SCENARIOS[scenario_index])
    assert scores
    for value in scores.values():
        assert 0.0 <= value <= 100.0


@settings(deadline=None, max_examples=10)
@given(
    scenario_index=st.integers(min_value=0, max_value=max(0, len(SCENARIOS) - 1)),
    seed=st.integers(min_value=1, max_value=999_999),
)
def test_stochastic_uncertainty_is_seed_reproducible(scenario_index: int, seed: int) -> None:
    scenario_id = SCENARIOS[scenario_index].scenario_id
    first_draws, first_summary = run_stochastic_uncertainty(scenario_id, draws=20, seed=seed)
    second_draws, second_summary = run_stochastic_uncertainty(scenario_id, draws=20, seed=seed)
    assert first_draws.equals(second_draws)
    assert first_summary.equals(second_summary)


def test_runtime_helper_branches_are_bounded_and_renderable() -> None:
    assert get_runtime_scenario("F4").scenario_id == "F4"
    try:
        get_runtime_scenario("missing")
    except ValueError as exc:
        assert "valid IDs" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("missing scenario should raise")

    low_badge, low_message = validate_slider_value(-1, "test", 0, 100)
    high_badge, high_message = validate_slider_value(101, "test", 0, 100)
    ok_badge, ok_message = validate_slider_value(50, "test", 0, 100)
    assert low_badge and "below lower bound" in low_message
    assert high_badge and "above upper bound" in high_message
    assert ok_badge and "within" in ok_message

    details = get_calculation_details("F4", "Full hybrid")
    rendered = format_formula_markdown(details)
    assert "Hybrid viability" in rendered
    assert "Formula sketch" in rendered


def test_stochastic_replay_returns_comparable_frames() -> None:
    replay = run_stochastic_replay("F4", draws=20, fixed_seed=1, random_seed=2)
    assert {"fixed", "random", "summary"} == set(replay)
    assert len(replay["fixed"]) == 20
    assert len(replay["random"]) == 20
    assert "fixed_mean" in replay["summary"].columns
    assert "random_mean" in replay["summary"].columns


def test_scenario_service_helper_branches() -> None:
    assert load_first_existing(["missing-one.csv", "missing-two.csv"]).empty

    readiness = build_calibration_readiness_table()
    assert {"domain", "input", "status", "why_it_matters"}.issubset(readiness.columns)
    assert "Primary care appointments" in set(readiness["domain"])

    empty_summary = summarise_reference_results(readiness.iloc[0:0])
    assert empty_summary.empty

    reference = summarise_reference_results(
        readiness.assign(
            rank_by_hybrid_viability=range(1, len(readiness) + 1),
            scenario_id=[f"F{i}" for i in range(len(readiness))],
            scenario_name=readiness["domain"],
            scenario_role="test",
            hybrid_viability_score=50,
            supply_generation_score=50,
            hospital_pressure_score=50,
            gaming_risk_score=50,
        )
    )
    assert list(reference["rank_by_hybrid_viability"]) == sorted(reference["rank_by_hybrid_viability"])
