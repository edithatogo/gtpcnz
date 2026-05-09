"""System dynamics stub for unmet need and hospital pressure."""

from dataclasses import dataclass


@dataclass
class SystemState:
    unmet_need: float
    primary_capacity: float
    hospital_pressure: float


def step(state: SystemState, need_generated: float, primary_contacts: float, ambulance_resolved: float, alpha: float = 0.2) -> SystemState:
    """Advance a simple unmet-need/hospital-pressure state by one period."""
    new_unmet = max(0.0, state.unmet_need + need_generated - primary_contacts - ambulance_resolved)
    new_hospital_pressure = max(0.0, state.hospital_pressure + alpha * new_unmet)
    return SystemState(unmet_need=new_unmet, primary_capacity=state.primary_capacity, hospital_pressure=new_hospital_pressure)
