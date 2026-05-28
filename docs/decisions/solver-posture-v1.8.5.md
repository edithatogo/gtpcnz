# Solver Posture Decision v1.8.5

**Date:** 2026-05-28  
**Track:** 048 — Equilibrium Solver Exploration  
**Status:** Decided — do NOT add analytical solver lane at this stage

---

## 1. Current Adapter Audit

### File audited
`models/primarycare_model/engines/nash_opt_adapter.py`

### Method used
**Iterated best-response dynamics** with discrete candidate search and learning-rate smoothing.

| Component | Detail |
|---|---|
| Search strategy | Each player evaluates 11 equally spaced candidates in ±20 range around current strategy |
| Learning rate | 0.1 default (clamped 0.01–0.50) |
| Convergence criterion | Both players' strategy change < 0.01 |
| Max iterations | 100 hard cap |
| Payoffs | Two static payoff functions (`_funder_payoff`, `_provider_payoff`) with linear and quadratic terms |
| Determinism | Fixed seed; `np.random.default_rng(seed)` called but not used in current payoff functions |
| `calculation_status` | `"live_deterministic"` — benchmark lane, not educational |

### Purpose classification

**Primarily analytical/benchmark, with pedagogical method.**

The adapter sits in the **engines layer** (not the UI layer) and produces `calculation_status = "live_deterministic"` outputs that feed the benchmark dashboard. However, the method itself — iterated best response with a small discrete candidate set — is deliberately **readable and pedagogical**. It is not a rigorous equilibrium solver:

- It does not compute mixed-strategy equilibria.
- It does not guarantee convergence to a Nash equilibrium; it stops when step size falls below tolerance.
- It uses a small, fixed candidate grid (11 points per dimension), not continuous optimisation.
- There is no sensitivity analysis, uniqueness check, or equilibrium refinement.

The adapter is therefore **analytical in purpose but pedagogical in method**. This hybrid posture creates a risk: consumers could mistake the output for a rigorous equilibrium computation when it is really an illustrative best-response walk.

### What the adapter does NOT do

- No mixed-strategy support
- No support-enumeration search
- No LCP / Lemke-Howson computation
- No JAX/XLA acceleration
- No Anderson acceleration or fixed-point iteration
- No extragradient or mirror-descent dynamics
- No convergence proof or uniqueness guarantee

---

## 2. Solver Comparison Matrix

Seven solver families were evaluated against the repo's mission as a **public-data anchored educational benchmark**.

| Solver | What it does | Analytical rigour | Readability | Dep. cost | Fit for GTPCNZ |
|---|---|---|---|---|---|
| **Iterated best response** (current) | Sequential best-response search with discrete grid and learning rate | Low — approximate, no convergence guarantee | High — ~50 lines of pure Python | None (numpy only) | **In use** — adequate for educational explainer |
| **Anderson acceleration** | Fixed-point acceleration for smooth best-response maps | Medium — faster convergence, same limits | Medium — requires vector residual formulation | None (numpy/scipy) | Low — overkill for 2-player 1D strategy space |
| **Support enumeration** | Exhaustive search over pure-strategy supports for small normal-form games | High — finds exact mixed equilibria in small games | Medium — standard textbook algorithm | None (pure Python) | Low — strategy space is continuous (audit/effort ∈ [0,100]), not discrete |
| **Lemke-Howson / LCP** | Exact mixed-equilibrium computation for 2-player bimatrix games | High — exact for linear payoffs | Low — complex pivoting algorithm | None (pure Python) | Low — continuous strategy space; repo does not use bimatrix form |
| **JAX / XLA batched optimisation** | GPU/TPU-accelerated gradient search over many scenarios | Medium — batch search, same limits as SGD | Low — JAX compilation pipeline, jaxtyping | High — JAX + CUDA runtime | **Rejected** — would make the repo depend on JAX ecosystem for a single small adapter |
| **JAXopt / implicit differentiation** | Gradient-based equilibrium with differentiable solver layers | High — analytical gradients through fixed points | Low — requires implicit function theorem | Very high — JAX + JAXopt | **Rejected** — analytical differentiation is unjustified for a pedagogical 2-player game |
| **Extragradient / mirror descent** | Dynamical systems view; approximate equilibrium via iterative dynamics | Medium — proven convergence for monotone games | Medium — extra gradient step doubles compute | None (numpy) | Low — adds complexity without benefit for the simple payoff structure |

### Key observations

1. **The strategy space is continuous**, not discrete bimatrix. Support enumeration and Lemke-Howson solve discrete games and are not a natural fit.
2. **The payoff functions are simple static formulas** with linear and quadratic terms. They do not have the non-convex, non-smooth structure that would justify advanced solvers.
3. **The repo's purpose is educational explanation**, not equilibrium computation research. A reader should be able to trace each line of the solver.
4. **JAX/XLA would add a heavy dependency** (JAX, jaxtyping, CUDA toolchain for GPU, or a large CPU-only JAX install) for a single small adapter. The existing `jax_mc_adapter.py` already uses JAX for Monte Carlo, but that is a distinct use case (vectorised random draws) that justifies the dependency. The Nash adapter would not benefit proportionally.

---

## 3. Decision

### Decision statement

> **Keep the current iterated best-response heuristic. Do NOT add an analytical solver lane at this stage. Harden the existing adapter with clearer scope documentation and convergence tests.**

### Rationale

1. **Mission fit**: The repo is a public-data anchored educational benchmark and explainer. It does not claim to produce research-grade equilibrium estimates. The current adapter is adequate for demonstrating incentive logic.

2. **Proportionality**: The game is simple — two players, one continuous strategy each, deterministic payoff functions. Adding JAXopt, Lemke-Howson, or Anderson acceleration would be disproportionate to the problem's complexity.

3. **Dependency cost**: Every new solver lane adds maintenance burden, CI time, and documentation surface. JAX/XLA in particular would require a significant dependency for minimal benefit.

4. **Claim-boundary protection**: An analytical solver lane with exact equilibrium guarantees could create pressure to claim empirical validity (e.g., "the equilibrium audit level is X%"). Keeping the pedagogical method insulates the repo from that risk.

5. **Readability**: The current adapter is ~80 lines of pure Python with no external algorithm imports. An analytical lane would require opaque numerical methods that the target audience (policy readers, health economists) cannot inspect.

### What this decision does NOT prevent

- Adding a **standalone pedagogical game module** with support enumeration for small discrete games (e.g., 2×2 payoff matrices in the educational lab) — this would live in `runtime_lab.py` or the UI layer, not in `engines/`.
- Accepting **external contributions** of an analytical solver package, provided it is clearly separated from the public dashboard and documented as opt-in research tooling.
- **Hardening tests** on the current adapter, which is explicitly approved by this decision.

---

## 4. Trigger Conditions (What Would Change the Decision)

The analytical lane should be reconsidered if any of the following conditions are met:

| Condition | Trigger | Expected action |
|---|---|---|
| **Research-mode toggle** | The dashboard adds a clearly separated research/advanced mode that labels all analytical outputs as "research-grade — not validated for public use" | Add solver package under `models/solvers/` with its own test suite and dependency group |
| **External solver contribution** | An external contributor submits a well-tested solver package (e.g., Nashpy-based support enumeration or a JAXopt equilibrium layer) that does not affect the public dashboard | Accept as opt-in; require benchmarks against the educational lane; add CI gate for claim-boundary metadata |
| **Empirical calibration requirement** | The repo's scope expands to include linked-data calibrated game-theory estimates (e.g., calibrated provider response functions) | Add analytical lane with documented calibration, sensitivity analysis, and explicit "empirical estimate" claim-boundary labelling |
| **Performance bottleneck** | The current adapter becomes a measurable performance bottleneck in CI or dashboard load time (>5s per run) | Profile and replace with Anderson acceleration or vectorised JAX search only if measurable; document the change in a solver upgrade decision record |

---

## 5. Harden Plan (Approved Actions)

| Action | File(s) | Detail |
|---|---|---|
| **Add educational scope docstring** | `nash_opt_adapter.py` | Clarify that the method is iterated best-response, not a full equilibrium solver; document limitations |
| **Add inline comments** | `nash_opt_adapter.py` | Document the discrete search grid, learning rate rationale, and convergence criterion |
| **Add convergence edge-case test** | `test_engine_adapters.py` | Test that the adapter converges for extreme input values (0, 100) |
| **Add deterministic-repeat test** | `test_engine_adapters.py` | Verify that repeated runs with same seed produce identical output |
| **Document solver posture** | `docs/decisions/solver-posture-v1.8.5.md` | This document |

---

## 6. Verification

```powershell
python -m pytest -q models/tests/test_engine_adapters.py
rg -n "NashOptimisationAdapter|best-response|Lemke|support enumeration|JAX|XLA|jaxopt|extragradient|mirror descent|Anderson" models docs conductor
```

---

*This decision is recorded in `conductor/tracks/048-equilibrium-solver-exploration_20260528/` and `docs/decisions/solver-posture-v1.8.5.md`.*
