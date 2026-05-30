# Queue Safety Invariant Notes

## Overview
Prototype invariant checks for the patient/provider queue scheduling system.
This is not yet a formal proof or TLA+ model.

## State Model
- Providers: each has remaining capacity and serves at most one patient at a time
- Patients: wait in per-provider FIFO queues until assigned
- Transitions: enqueue(patient, provider), assign(provider), complete(provider)

## Safety Invariants
### INV1 - No Negative Capacity
For every provider p, capacity(p) >= 0 at all times.

### INV2 - Patient Conservation
Patients in system never exceed total patients entered.

### INV3 - No Duplicate Waiting Assignments
A patient cannot appear in multiple waiting queues.

### INV4 - No Simultaneous Waiting And Service
A patient cannot be both in-service and waiting.

## Liveness Targets
These are planned verification targets, not currently proven properties.

### Capacity-Blocked Backlog Detection
If patients wait and all providers have no immediately assignable capacity,
the prototype flags a capacity-blocked backlog state for later scheduling logic
or bounded-service-completion tests.

### Starvation Freedom
Future property tests should verify that every enqueued patient is eventually
assigned under finite service-completion assumptions.

## Python Implementation
- File: models/tests/test_queue_safety.py
- Class: QueueState (dataclass) with check_invariants() method
- Functions: enqueue_patient(), assign_to_provider(), complete_service()
- Detection: detect_capacity_blocked_backlog()

## TLA+ (Planned)
A TLA+ specification may be added at docs/formal/queue-safety.tla for TLC model
checking once the production scheduler semantics are stable.
