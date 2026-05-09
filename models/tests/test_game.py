from primarycare_model.game import (
    FunderStrategy,
    PolicyParameters,
    ProviderStrategy,
    best_provider_response,
    calculate_payoff,
    evaluate_outcome,
    provider_best_response_table,
    repeated_hospital_pressure,
)


def test_best_provider_response_under_tight_control_is_rationing():
    assert best_provider_response(FunderStrategy.TIGHT_UPSTREAM_CONTROL) == ProviderStrategy.RATION_SUPPLY


def test_contact_benefits_expand_supply_has_lower_hospital_pressure_than_tight_rationing():
    tight = evaluate_outcome(FunderStrategy.TIGHT_UPSTREAM_CONTROL, ProviderStrategy.RATION_SUPPLY)
    benefits = evaluate_outcome(FunderStrategy.CONTACT_BENEFITS, ProviderStrategy.EXPAND_SUPPLY)
    assert benefits.hospital_pressure < tight.hospital_pressure


def test_best_response_table_includes_reweighting():
    table = provider_best_response_table()
    assert FunderStrategy.REWEIGHT_CAPITATION_ONLY in table
    assert table[FunderStrategy.CONTACT_BENEFITS] == ProviderStrategy.EXPAND_SUPPLY


def test_repeated_pressure_declines_under_contact_benefits_expansion():
    path = [(FunderStrategy.CONTACT_BENEFITS, ProviderStrategy.EXPAND_SUPPLY)] * 5
    pressures = repeated_hospital_pressure(path, initial_pressure=8.0, persistence=0.5)
    assert pressures[-1] < pressures[0]


def test_calculate_payoff_penalises_hospital_pressure():
    base = PolicyParameters(
        upstream_public_cost=2,
        hospital_cost=4,
        hospital_pressure=2,
        hospital_political_penalty=1,
        copayment_burden=1,
        copayment_penalty=1,
        equity_gap=1,
        equity_penalty=1,
        safety_failure=0,
        safety_penalty=2,
        avoidance_benefit=5,
        provider_revenue=6,
        provider_marginal_cost=3,
        provider_admin_cost=1,
        provider_burnout_cost=1,
        consumer_health_benefit=6,
        consumer_waiting_cost=1,
        consumer_travel_cost=1,
        consumer_fragmentation_cost=1,
    )
    high_pressure = PolicyParameters(**{**base.__dict__, "hospital_pressure": 8})
    assert calculate_payoff(high_pressure).funder < calculate_payoff(base).funder
