from primarycare_model.nz_game import (
    AccessState,
    ContactBenefit,
    FundingArchitecture,
    ProviderResponse,
    hospital_pressure_next,
    likely_provider_response,
    score_architecture,
    unmet_need,
)


def test_contact_benefit_incentivises_supply_when_margin_positive():
    contact = ContactBenefit(public_benefit=60, copayment=20, marginal_cost=50, admin_cost=5, risk_cost=5)
    assert contact.net_margin == 20
    assert contact.is_supply_incentivised()


def test_contact_not_claimable_when_scope_ineligible():
    contact = ContactBenefit(public_benefit=60, copayment=20, marginal_cost=30, admin_cost=5, risk_cost=5, scope_eligible=False)
    assert not contact.is_supply_incentivised()


def test_reweighted_capitation_still_rations_when_marginal_contact_negative():
    contact = ContactBenefit(public_benefit=0, copayment=20, marginal_cost=45, admin_cost=5, risk_cost=5)
    assert likely_provider_response(FundingArchitecture.REWEIGHTED_CAPITATION, contact) == ProviderResponse.RATION


def test_primary_care_benefits_schedule_expands_when_margin_positive():
    contact = ContactBenefit(public_benefit=55, copayment=15, marginal_cost=45, admin_cost=5, risk_cost=5)
    assert likely_provider_response(FundingArchitecture.PRIMARY_CARE_BENEFITS_SCHEDULE, contact) == ProviderResponse.EXPAND_MULTIDISCIPLINARY


def test_unmet_need_reappears_as_hospital_pressure():
    state = AccessState(demand=100, primary_capacity=60, ambulance_resolved=10, ambulance_conveyance=20, hospital_pressure=40)
    assert unmet_need(state.demand, state.primary_capacity, state.ambulance_resolved) == 30
    assert hospital_pressure_next(state, persistence=0.5, unmet_to_hospital=0.5, conveyance_to_hospital=0.1) > state.hospital_pressure * 0.5


def test_benefits_schedule_has_higher_access_score_than_status_quo():
    status_quo = score_architecture(FundingArchitecture.STATUS_QUO_TIGHT_CONTROL)
    schedule = score_architecture(FundingArchitecture.PRIMARY_CARE_BENEFITS_SCHEDULE)
    assert schedule.patient_access > status_quo.patient_access
    assert schedule.hospital_avoidance > status_quo.hospital_avoidance
