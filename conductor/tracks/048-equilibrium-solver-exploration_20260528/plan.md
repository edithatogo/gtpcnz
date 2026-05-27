# Plan

- [ ] Audit the current Nash-style adapter and identify whether its purpose is educational, analytical, or both.
- [ ] Compare solver candidates: iterated best response, Anderson acceleration, support enumeration, Lemke-Howson, JAX/XLA optimisation, JAXopt/implicit differentiation, and extragradient methods.
- [ ] Decide whether any analytical solver belongs in the repo or whether the heuristic lane should remain the only supported one.
- [ ] If an analytical lane is approved, define the package boundary, inputs, outputs, and performance tests.
- [ ] If the analytical lane is not approved, document that decision and harden the current best-response adapter instead.
- [ ] Update public-facing docs only if the solver posture changes.
- [ ] Run targeted engine tests and record the solver decision in Conductor state.
