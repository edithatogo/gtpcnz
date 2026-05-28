"""Typed adapter for Nash equilibrium-based strategic optimisation.

SCOPE AND LIMITATIONS
---------------------
This adapter implements **iterated best-response dynamics**, a pedagogical
method that approximates Nash equilibrium by having each player alternately
optimise their payoff given the other's current strategy.  It is NOT a full
equilibrium solver toolkit.

Specifically, this adapter does NOT implement:
- Mixed-strategy equilibrium computation
- Support enumeration or Lemke-Howson / LCP methods
- Anderson acceleration or fixed-point iteration
- JAX/XLA-accelerated batch optimisation
- Extragradient or mirror-descent dynamics
- Convergence proofs or equilibrium uniqueness guarantees

The method uses a small discrete candidate grid (11 points per dimension)
and a learning-rate smoother.  This is deliberately **readable and pedagogical**
— suitable for demonstrating incentive direction in a public-data anchored
educational benchmark, not for producing research-grade equilibrium estimates.

See `docs/decisions/solver-posture-v1.8.5.md` for the full solver posture
decision.

Models two players (funder and provider) choosing policy or effort levels
respectively.  The Nash equilibrium is found by iterated best-response: each
player adjusts their strategy to optimise their payoff given the other's
current strategy, repeating until convergence.
"""

from __future__ import annotations

import numpy as np
from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, UncertaintySummary
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

MAX_NASH_ITERATIONS = 100
DEFAULT_NASH_ITERATIONS = 50
CONVERGENCE_TOLERANCE = 0.01


class NashInput(EngineInput):
    """Engine input for Nash equilibrium optimisation."""

    max_iterations: int = Field(default=DEFAULT_NASH_ITERATIONS, ge=10, le=MAX_NASH_ITERATIONS)
    learning_rate: float = Field(default=0.1, ge=0.01, le=0.5)

    # Funder strategy bounds
    funder_audit: float = Field(default=50.0, ge=0.0, le=100.0, description="Funder audit/oversight level")
    funder_place_accountability: float = Field(default=50.0, ge=0.0, le=100.0)

    # Provider strategy bounds
    provider_effort: float = Field(default=50.0, ge=0.0, le=100.0, description="Provider compliance/effort level")
    provider_scope_utilisation: float = Field(default=50.0, ge=0.0, le=100.0)

    # Scenario context
    budget_tightness: float = Field(default=50.0, ge=0.0, le=100.0)
    complexity: float = Field(default=50.0, ge=0.0, le=100.0)
    activity_signal: float = Field(default=50.0, ge=0.0, le=100.0)


class NashOutput(EngineOutput):
    """Engine output from Nash equilibrium optimisation."""

    scenario_result: ScenarioResult
    equilibrium_funder_audit: float
    equilibrium_provider_effort: float
    iterations_to_converge: int
    payoff_trajectory: tuple[dict[str, float], ...]
    uncertainty_summaries: tuple[UncertaintySummary, ...] = ()


class NashOptimisationAdapter:
    """Typed adapter for Nash equilibrium-based strategic optimisation.

    Uses iterated best-response dynamics to find approximate Nash equilibrium
    strategies for funder and provider.  Deterministic for a fixed seed.
    """

    engine_id = "nash_opt_v1"

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return float(max(lower, min(upper, value)))

    @staticmethod
    def _funder_payoff(audit: float, effort: float, budget: float, complexity: float, activity: float, place: float) -> float:
        compliance_benefit = 30.0 * (effort / 100.0)
        gaming_penalty = -20.0 * (activity / 100.0) * (1.0 - audit / 100.0)
        audit_cost = -15.0 * (audit / 100.0)
        budget_pressure = -10.0 * (budget / 100.0) * (1.0 - effort / 100.0)
        return compliance_benefit + gaming_penalty + audit_cost + budget_pressure

    @staticmethod
    def _provider_payoff(effort: float, audit: float, scope: float, complexity: float, place: float) -> float:
        funding_benefit = 25.0 * (scope / 100.0)
        oversight_burden = -20.0 * (audit / 100.0) * (effort / 100.0)
        effort_cost = -15.0 * (effort / 100.0) ** 2
        place_benefit = 10.0 * (place / 100.0)
        complexity_penalty = -10.0 * (complexity / 100.0) * (effort / 100.0)
        return funding_benefit + oversight_burden + effort_cost + place_benefit + complexity_penalty

    def run(self, inputs: NashInput) -> NashOutput:
        # ── Initialisation ──────────────────────────────────────────────
        # Seed is accepted for API consistency but not used by the current
        # payoff functions, which are purely deterministic.  Called here to
        # reserve the seed contract for future stochastic extensions.
        inp = inputs
        seed = inp.seed if inp.seed is not None else 20260526
        np.random.default_rng(seed)

        audit = float(inp.funder_audit)
        effort = float(inp.provider_effort)
        # Learning rate controls how far the strategy moves toward the
        # current best-response target each iteration (0.01 = slow,
        # 0.5 = fast).  This smoothing prevents oscillation between
        # discrete candidate points.
        lr = float(inp.learning_rate)
        max_iter = int(min(max(10, inp.max_iterations), MAX_NASH_ITERATIONS))

        trajectory: list[dict[str, float]] = []
        converged = False
        final_iter = 0

        # ── Iterated best-response loop ─────────────────────────────────
        # Each iteration:
        #   1. Evaluate 11 equally spaced candidate strategies in a ±20
        #      window around each player's current strategy.
        #   2. Pick the candidate with the highest payoff (discrete
        #      argmax over a coarse grid — NOT continuous optimisation).
        #   3. Move partway toward that target (learning-rate smoothing).
        #   4. Check convergence: stop when both strategies change by
        #      less than CONVERGENCE_TOLERANCE (0.01 units).
        for iteration in range(1, max_iter + 1):
            # ── Funder best response ──
            # Funders choose an audit level to maximise their payoff
            # given the current provider effort.
            audit_candidates = np.linspace(max(0, audit - 20), min(100, audit + 20), 11)
            funder_payoffs = [self._funder_payoff(
                a, effort, inp.budget_tightness, inp.complexity, inp.activity_signal, inp.funder_place_accountability
            ) for a in audit_candidates]
            best_audit_idx = int(np.argmax(funder_payoffs))
            target_audit = float(audit_candidates[best_audit_idx])

            # ── Provider best response ──
            # Providers choose an effort level to maximise their payoff
            # given the current funder audit.
            effort_candidates = np.linspace(max(0, effort - 20), min(100, effort + 20), 11)
            provider_payoffs = [self._provider_payoff(
                e, audit, inp.provider_scope_utilisation, inp.complexity, inp.funder_place_accountability
            ) for e in effort_candidates]
            best_effort_idx = int(np.argmax(provider_payoffs))
            target_effort = float(effort_candidates[best_effort_idx])

            # ── Learning-rate step ──
            # Smooth movement toward the best-response target to avoid
            # discrete jumps between candidate grid points.
            new_audit = self._clamp(audit + lr * (target_audit - audit))
            new_effort = self._clamp(effort + lr * (target_effort - effort))

            trajectory.append({
                "iteration": iteration,
                "funder_audit": round(new_audit, 2),
                "provider_effort": round(new_effort, 2),
                "funder_payoff": round(float(funder_payoffs[best_audit_idx]), 2),
                "provider_payoff": round(float(provider_payoffs[best_effort_idx]), 2),
            })

            # ── Convergence check ──
            # Both strategies must change by less than 0.01 for the
            # loop to terminate early.  This does NOT guarantee that
            # the strategies form a Nash equilibrium — only that the
            # step size has fallen below the reporting threshold.
            if abs(new_audit - audit) < CONVERGENCE_TOLERANCE and abs(new_effort - effort) < CONVERGENCE_TOLERANCE:
                converged = True
                final_iter = iteration
                break

            audit, effort = new_audit, new_effort
            final_iter = iteration

        hybrid = self._clamp(30.0 + 0.30 * audit + 0.25 * effort + 0.15 * inp.funder_place_accountability - 0.10 * inp.complexity)
        access = self._clamp(30.0 + 0.20 * effort + 0.20 * inp.funder_place_accountability + 0.15 * inp.activity_signal - 0.15 * inp.budget_tightness)
        supply = self._clamp(25.0 + 0.25 * inp.activity_signal + 0.20 * inp.provider_scope_utilisation + 0.15 * effort)
        hosp_pressure = self._clamp(100 - 0.25 * access - 0.15 * audit)
        gaming = self._clamp(40.0 + 0.30 * inp.activity_signal - 0.35 * audit - 0.15 * effort)

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=round(hybrid, 2),
            access_score=round(access, 2),
            supply_generation_score=round(supply, 2),
            hospital_pressure_score=round(hosp_pressure, 2),
            gaming_risk_score=round(gaming, 2),
            calculation_status="live_deterministic",
        )

        manifest = ResultManifest(
            result_id=f"nash_{inp.scenario_id}_{seed}",
            calculation_mode="live_deterministic",
            scenario_id=inp.scenario_id,
            seed=seed,
            draws=None,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return NashOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            equilibrium_funder_audit=round(audit, 2),
            equilibrium_provider_effort=round(effort, 2),
            iterations_to_converge=final_iter if converged else max_iter,
            payoff_trajectory=tuple(trajectory),
        )
