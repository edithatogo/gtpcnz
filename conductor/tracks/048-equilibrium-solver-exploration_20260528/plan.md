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

## Provider policy follow-up — 22 November 2026

- [x] Record UOGTO/Paignia intake and clarify future provider choice while
  preserving the existing pedagogical solver decision; verify the documents.

Base: `4cae5a2f5ebeddd8e86de4263de55caf13c6ef1a`.
Allowed files: `AGENTS.md`, `CONTRIBUTING.md`,
`docs/decisions/solver-posture-v1.8.5.md` and this plan.
The [intake rule](../../../CONTRIBUTING.md#game-capability-intake) requires
separate dispositions using each provider's canonical vocabulary, including
explicit pending states; mapping evidence and executable support remain distinct.
Section 7 of the solver decision changes future provider routing only.

The earlier 20-test receipt retains its historical scope and is not a new test
run. No analytical lane, runtime migration or equilibrium qualification is
claimed. Local documentation checks and publication status are recorded below.

Local verification: the standard-library documentation check validated all seven
new local links/anchors, both canonical upstream pointers and both sets of
dispositions. Scoped `git diff --check` and staged `git diff --cached --check`
passed. No runtime tests were run for these documentation-only changes.
Remote publication, upstream-document availability and hosted checks remain
pending integration; this receipt covers the local policy files only.
