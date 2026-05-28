# Plan

- [x] Audit the current Nash-style adapter and identify whether its purpose is educational, analytical, or both.
- [x] Compare solver candidates: iterated best response, Anderson acceleration, support enumeration, Lemke-Howson, JAX/XLA optimisation, JAXopt/implicit differentiation, and extragradient methods.
- [x] Decide whether any analytical solver belongs in the repo or whether the heuristic lane should remain the only supported one.
- [x] If an analytical lane is approved, define the package boundary, inputs, outputs, and performance tests.
- [x] If the analytical lane is not approved, document that decision and harden the current best-response adapter instead.
- [x] Update public-facing docs only if the solver posture changes.
- [x] Run targeted engine tests and record the solver decision in Conductor state.

## Outcomes

| Item | Status | Evidence |
|---|---|---|
| Solver posture decision | Done | `docs/decisions/solver-posture-v1.8.5.md` — **Keep heuristic, do NOT add analytical lane** |
| Adapter audit | Done | Identified as "analytical in purpose, pedagogical in method" |
| Solver comparison matrix | Done | 7 methods compared; all advanced methods rejected for this repo |
| Adapter hardening | Done | Scope docstring, inline comments, solver posture cross-reference added |
| Claim-boundary wording | Unchanged | `calculation_status` and `calculation_mode` remain `"live_deterministic"` |
| Engine tests | Passed | 20/20 passed (including 2 Nash-specific tests) |
