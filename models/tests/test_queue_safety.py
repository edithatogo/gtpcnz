"""Queue safety invariants for a patient/provider scheduler prototype."""

from __future__ import annotations

from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class QueueState:
    provider_capacity: dict[str, int]
    waiting_queues: dict[str, list[str]]
    in_service: dict[str, str | None]
    total_patients: int

    @property
    def total_in_queue(self) -> int:
        return sum(len(queue) for queue in self.waiting_queues.values())

    @property
    def total_in_service(self) -> int:
        return sum(1 for patient in self.in_service.values() if patient is not None)

    @property
    def total_in_system(self) -> int:
        return self.total_in_queue + self.total_in_service

    def check_invariants(self) -> list[str]:
        violations: list[str] = []
        for provider_id, capacity in self.provider_capacity.items():
            if capacity < 0:
                violations.append(f"INV1: {provider_id} negative capacity {capacity}")

        if self.total_in_system > self.total_patients:
            violations.append(f"INV2: in-system {self.total_in_system} > total {self.total_patients}")

        waiting_patients: set[str] = set()
        for queue in self.waiting_queues.values():
            for patient_id in queue:
                if patient_id in waiting_patients:
                    violations.append(f"INV3: duplicate waiting patient {patient_id}")
                waiting_patients.add(patient_id)

        for patient_id in self.in_service.values():
            if patient_id is not None and patient_id in waiting_patients:
                violations.append(f"INV4: {patient_id} in service and waiting")

        return violations


def enqueue_patient(state: QueueState, patient_id: str, provider_id: str) -> QueueState:
    if provider_id not in state.provider_capacity:
        raise KeyError(f"Unknown provider: {provider_id}")

    waiting_queues = {pid: list(queue) for pid, queue in state.waiting_queues.items()}
    waiting_queues.setdefault(provider_id, []).append(patient_id)
    return QueueState(
        provider_capacity=dict(state.provider_capacity),
        waiting_queues=waiting_queues,
        in_service=dict(state.in_service),
        total_patients=state.total_patients + 1,
    )


def assign_to_provider(state: QueueState, provider_id: str) -> QueueState:
    if provider_id not in state.provider_capacity:
        raise KeyError(f"Unknown provider: {provider_id}")
    if state.provider_capacity[provider_id] <= 0:
        raise ValueError(f"Provider has no remaining capacity: {provider_id}")
    if state.in_service.get(provider_id) is not None:
        raise ValueError(f"Provider already has a patient in service: {provider_id}")
    if not state.waiting_queues.get(provider_id):
        raise ValueError(f"Provider queue is empty: {provider_id}")

    waiting_queues = {pid: list(queue) for pid, queue in state.waiting_queues.items()}
    patient_id = waiting_queues[provider_id].pop(0)
    provider_capacity = dict(state.provider_capacity)
    provider_capacity[provider_id] -= 1
    in_service = dict(state.in_service)
    in_service[provider_id] = patient_id
    return QueueState(
        provider_capacity=provider_capacity,
        waiting_queues=waiting_queues,
        in_service=in_service,
        total_patients=state.total_patients,
    )


def complete_service(state: QueueState, provider_id: str) -> QueueState:
    if provider_id not in state.in_service:
        raise KeyError(f"Unknown provider: {provider_id}")
    if state.in_service[provider_id] is None:
        raise ValueError(f"Provider has no patient in service: {provider_id}")

    in_service = dict(state.in_service)
    in_service[provider_id] = None
    return QueueState(
        provider_capacity=dict(state.provider_capacity),
        waiting_queues={pid: list(queue) for pid, queue in state.waiting_queues.items()},
        in_service=in_service,
        total_patients=state.total_patients - 1,
    )


def detect_capacity_blocked_backlog(state: QueueState) -> bool:
    """Flag a backlog when every provider has no immediately assignable capacity."""
    return state.total_in_queue > 0 and all(capacity <= 0 for capacity in state.provider_capacity.values())


def test_queue_safety_trace_preserves_invariants() -> None:
    state = QueueState(
        {"gp_1": 3, "nurse_1": 2},
        {"gp_1": [], "nurse_1": []},
        {"gp_1": None, "nurse_1": None},
        0,
    )
    trace = [state]
    trace.append(enqueue_patient(trace[-1], "P001", "gp_1"))
    trace.append(enqueue_patient(trace[-1], "P002", "gp_1"))
    trace.append(enqueue_patient(trace[-1], "P003", "nurse_1"))
    trace.append(assign_to_provider(trace[-1], "gp_1"))
    trace.append(assign_to_provider(trace[-1], "nurse_1"))

    for step, current in enumerate(trace):
        assert not current.check_invariants(), f"Step {step} violated"
        assert not detect_capacity_blocked_backlog(current), f"Step {step} capacity-blocked"


def test_duplicate_waiting_patient_violates_invariant() -> None:
    state = QueueState(
        provider_capacity={"gp_1": 2},
        waiting_queues={"gp_1": ["P001", "P001"]},
        in_service={"gp_1": None},
        total_patients=2,
    )

    assert any("duplicate waiting patient P001" in violation for violation in state.check_invariants())


def test_patient_cannot_be_waiting_and_in_service() -> None:
    state = QueueState(
        provider_capacity={"gp_1": 1},
        waiting_queues={"gp_1": ["P001"]},
        in_service={"gp_1": "P001"},
        total_patients=2,
    )

    assert any("in service and waiting" in violation for violation in state.check_invariants())


def test_capacity_blocked_backlog_detected_when_all_providers_unavailable() -> None:
    state = QueueState(
        provider_capacity={"gp_1": 0, "nurse_1": 0},
        waiting_queues={"gp_1": ["P003"], "nurse_1": []},
        in_service={"gp_1": "P001", "nurse_1": "P002"},
        total_patients=3,
    )

    assert detect_capacity_blocked_backlog(state)


@pytest.mark.parametrize(
    ("state", "provider_id", "error"),
    [
        (
            QueueState({"gp_1": 1}, {"gp_1": []}, {"gp_1": None}, 0),
            "missing",
            KeyError,
        ),
        (
            QueueState({"gp_1": 0}, {"gp_1": ["P001"]}, {"gp_1": None}, 1),
            "gp_1",
            ValueError,
        ),
        (
            QueueState({"gp_1": 1}, {"gp_1": []}, {"gp_1": None}, 0),
            "gp_1",
            ValueError,
        ),
        (
            QueueState({"gp_1": 1}, {"gp_1": ["P002"]}, {"gp_1": "P001"}, 2),
            "gp_1",
            ValueError,
        ),
    ],
)
def test_assign_to_provider_guards_invalid_states(
    state: QueueState,
    provider_id: str,
    error: type[Exception],
) -> None:
    with pytest.raises(error):
        assign_to_provider(state, provider_id)
