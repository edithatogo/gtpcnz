# Equilibrium Solver Exploration

## Problem

The repo already has a Nash-style strategic adapter based on iterated best response. That is enough for an educational explainer, but it is not the same thing as a modern equilibrium solver stack. The current question is whether the project should stay with a readable heuristic or add a separate analytical lane with stronger numerical methods.

## Goal

Make the solver posture explicit and testable:

- keep the public dashboard solver readable and bounded;
- identify which equilibrium methods are actually worth adding;
- separate pedagogical best-response logic from analytical solver logic;
- define whether any advanced solver should be XLA/JAX-backed, pure-Python, or both;
- require tests and performance gates before promoting any new solver to the repo.

## Current State

| Concern | Current locations | Gap |
|---|---|---|
| Nash-style strategic adapter | `models/primarycare_model/engines/nash_opt_adapter.py` | Uses iterated best response; useful, but not a full solver toolkit. |
| Game-theory UI | `models/primarycare_model/app.py` | Shows payoff and best-response surfaces, but does not expose a solver selection layer. |
| Solver docs | `docs/launch/claim-boundaries-v1.7.2.md`, `docs/design/concern-extraction-architecture-v1.8.3.md` | Documents engine lanes, but not an explicit solver decision matrix. |
| Tests | `models/tests/test_engine_adapters.py` | Verifies current adapter behaviour, not solver class comparison. |

## Candidate Solver Lanes

| Lane | What it is good for | Fit |
|---|---|---|
| Iterated best response | Simple educational Nash approximation, easy to read | Already in repo |
| Fixed-point / Anderson acceleration | Faster convergence for smooth best-response maps | Strong candidate |
| JAX / XLA batched optimisation | GPU/TPU-friendly search over many scenarios | Strong candidate if the repo wants performance |
| JAXopt / implicit differentiation | Gradient-based equilibrium and sensitivity analysis | Strong candidate if the solver becomes analytical |
| Support enumeration | Exact pure/mixed equilibrium search for small games | Good for small pedagogical games |
| Lemke-Howson / LCP-style methods | Exact or near-exact mixed-equilibrium computation in 2-player settings | Good for small and medium games |
| Replicator / extragradient / mirror descent | Dynamical viewpoint and approximate equilibrium search | Good if the game module becomes more research-like |

## Decision Rule

- If the game module remains an explainer, keep iterated best response and add stronger tests only.
- If the repo wants an analytical lane, add a separate solver package and keep the public dashboard on the heuristic path.
- If the repo wants both, the analytical lane must be opt-in, documented, and benchmarked against the educational lane.

## Acceptance Criteria

- the repo has a written decision on whether Nash stays heuristic or becomes analytical;
- the chosen solver lane has clear numerical-method documentation;
- any new solver has convergence or correctness tests;
- public dashboard wording remains educational and non-forecasting;
- the solver lane is separated from the explainer lane in code and docs.

## Non-Goals

- Do not change the public calibration boundary.
- Do not claim empirical equilibrium estimates from public-data-only surfaces.
- Do not replace the existing dashboard with a black-box optimiser.

## Verification

```powershell
rg -n "NashOptimisationAdapter|best-response|Lemke|support enumeration|JAX|XLA|jaxopt|extragradient|mirror descent|Anderson" models docs conductor
python -m pytest -q models/tests/test_engine_adapters.py
```
