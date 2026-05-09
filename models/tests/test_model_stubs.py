from primarycare_model.abm_stub import ProviderAgent
from primarycare_model.sd_stub import SystemState, step


def test_provider_can_deliver_contact_type_when_in_scope():
    provider = ProviderAgent(provider_type="pharmacist", capacity=10, benefit_eligible=True, scope=("medicines_review",))
    assert provider.can_deliver("medicines_review")
    assert not provider.can_deliver("fracture_reduction")


def test_system_dynamics_step_increases_hospital_pressure_when_unmet_need_grows():
    state = SystemState(unmet_need=5, primary_capacity=10, hospital_pressure=3)
    new_state = step(state, need_generated=10, primary_contacts=2, ambulance_resolved=1)
    assert new_state.unmet_need == 12
    assert new_state.hospital_pressure > state.hospital_pressure
