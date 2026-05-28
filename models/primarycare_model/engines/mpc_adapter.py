"""Typed adapter for model-predictive control (MPC) simulation.

Solves a receding-horizon optimisation over scenario levers to minimise a
cost function that balances hybrid-viability maximisation against fiscal and
gaming-risk penalties.
"""

from __future__ import annotations

import numpy as np
from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

MAX_MPC_HORIZON = 60
MIN_MPC_HORIZON = 6
DEFAULT_MPC_HORIZON = 24


class MPCInput(EngineInput):
    """Engine input for model-predictive control simulation."""

    horizon: int = Field(default=DEFAULT_MPC_HORIZON, ge=MIN_MPC_HORIZON, le=MAX_MPC_HORIZON)
    n_control_steps: int = Field(default=5, ge=1, le=20)

    # Initial scenario lever values
    activity_signal: float = Field(default=50.0, ge=0.0, le=100.0)
    capitation: float = Field(default=50.0, ge=0.0, le=100.0)
    place_accountability: float = Field(default=50.0, ge=0.0, le=100.0)
    scope_capacity: float = Field(default=50.0, ge=0.0, le=100.0)
    urgent_ambulance: float = Field(default=50.0, ge=0.0, le=100.0)
    data_visibility: float = Field(default=50.0, ge=0.0, le=100.0)
    governance: float = Field(default=50.0, ge=0.0, le=100.0)
    equity_protection: float = Field(default=50.0, ge=0.0, le=100.0)
    copayment_burden: float = Field(default=50.0, ge=0.0, le=100.0)
    budget_tightness: float = Field(default=50.0, ge=0.0, le=100.0)
    hospital_salience: float = Field(default=50.0, ge=0.0, le=100.0)
    complexity: float = Field(default=50.0, ge=0.0, le=100.0)

    # Cost weights
    w_hybrid: float = Field(default=-1.0, ge=-10.0, le=0.0)
    w_fiscal: float = Field(default=0.5, ge=0.0, le=10.0)
    w_gaming: float = Field(default=0.3, ge=0.0, le=10.0)


class MPCOutput(EngineOutput):
    """Engine output from model-predictive control simulation."""

    scenario_result: ScenarioResult
    control_trajectory: tuple[dict[str, float | int], ...]
    optimised_levers: dict[str, float]
    total_cost: float

class ModelPredictiveControlAdapter:
    """Typed adapter for model-predictive control simulation.

    Uses a simple grid search over control steps to find lever adjustments that
    minimise the weighted cost.  Deterministic behaviour for a fixed seed.
    """

    engine_id = "mpc_v1"

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return float(max(lower, min(upper, value)))

    @staticmethod
    def _as_fraction(value: float) -> float:
        return float(max(0.0, min(100.0, value))) / 100.0

    def _calculate_indices(self,
        activity: float,
        capitation: float,
        place: float,
        scope: float,
        urgent: float,
        data: float,
        governance: float,
        equity: float,
        copay: float,
        budget: float,
        hosp_sal: float,
        compl: float,
    ) -> dict[str, float]:
        def f(v: float) -> float:
            return float(max(0.0, min(100.0, v))) / 100.0

        a, c, p, s, u, d, g, e, cp, b, _hs, cx = [f(v) for v in (activity, capitation, place, scope, urgent, data, governance, equity, copay, budget, hosp_sal, compl)]

        supply = self._clamp(100 * (0.34 * a + 0.18 * c + 0.24 * s + 0.12 * u + 0.12 * p - 0.12 * b))
        access = self._clamp(100 * (0.42 * supply / 100 + 0.18 * u + 0.15 * e + 0.12 * p + 0.10 * d - 0.16 * cp))
        gaming = self._clamp(100 * (0.35 * a + 0.18 * s + 0.18 * cx - 0.30 * g - 0.18 * d - 0.16 * p))
        fiscal = self._clamp(100 * (0.22 * a + 0.18 * gaming / 100 + 0.16 * cx + 0.14 * (1 - b) - 0.18 * g))
        hybrid = self._clamp(
            0.24 * supply + 0.18 * access
            + 0.18 * self._clamp(100 * (0.34 * e + 0.24 * p + 0.16 * c + 0.14 * d - 0.16 * cp))
            + 0.16 * self._clamp(100 * (0.44 * g + 0.20 * d + 0.18 * p + 0.10 * e + 0.08 * c))
            + 0.14 * self._clamp(100 * (0.32 * access / 100 + 0.22 * u + 0.16 * supply / 100 + 0.16 * d + 0.14 * p - 0.10 * cx))
            + 0.06 * (100 - fiscal) + 0.04 * (100 - gaming)
        )

        return {"hybrid": hybrid, "access": access, "supply": supply, "gaming": gaming, "fiscal": fiscal}

    def run(self, inputs: MPCInput) -> MPCOutput:
        inp = inputs
        seed = inp.seed if inp.seed is not None else 20260526
        np.random.default_rng(seed)

        base = [inp.activity_signal, inp.capitation, inp.place_accountability, inp.scope_capacity,
                inp.urgent_ambulance, inp.data_visibility, inp.governance, inp.equity_protection,
                inp.copayment_burden, inp.budget_tightness, inp.hospital_salience, inp.complexity]

        lever_names = ["activity_signal", "capitation", "place_accountability", "scope_capacity",
                       "urgent_ambulance", "data_visibility", "governance", "equity_protection",
                       "copayment_burden", "budget_tightness", "hospital_salience", "complexity"]

        # Optimise by grid search over control steps
        step_size = 5.0
        best_cost = float("inf")
        best_levers = list(base)

        for _ in range(inp.n_control_steps):
            candidate = list(best_levers)
            improved = False
            for i in range(len(candidate)):
                for delta in [-step_size, step_size]:
                    trial = list(candidate)
                    trial[i] = self._clamp(trial[i] + delta)
                    idx = self._calculate_indices(*trial)
                    cost = float(inp.w_hybrid * idx["hybrid"] + inp.w_fiscal * idx["fiscal"] + inp.w_gaming * idx["gaming"])
                    if cost < best_cost:
                        best_cost = cost
                        best_levers = list(trial)
                        improved = True
            if not improved:
                step_size *= 0.5
                if step_size < 0.5:
                    break

        # Build control trajectory over horizon
        horizon = int(min(max(MIN_MPC_HORIZON, inp.horizon), MAX_MPC_HORIZON))
        trajectory: list[dict[str, float | int]] = []
        current = list(base)

        for step in range(1, horizon + 1):
            blend = step / horizon
            blended = [self._clamp(current[i] + blend * (best_levers[i] - current[i])) for i in range(12)]
            idx = self._calculate_indices(*blended)
            trajectory.append({
                "step": step,
                "hybrid_viability": round(idx["hybrid"], 2),
                "access_score": round(idx["access"], 2),
                "fiscal_risk_score": round(idx["fiscal"], 2),
                "gaming_risk_score": round(idx["gaming"], 2),
            })
            current = blended

        final_idx = self._calculate_indices(*best_levers)

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=round(final_idx["hybrid"], 2),
            access_score=round(final_idx["access"], 2),
            supply_generation_score=round(final_idx["supply"], 2),
            hospital_pressure_score=round(100 - final_idx["access"] * 0.5, 2),
            gaming_risk_score=round(final_idx["gaming"], 2),
            calculation_status="live_deterministic",
        )

        manifest = ResultManifest(
            result_id=f"mpc_{inp.scenario_id}_{seed}",
            calculation_mode="live_deterministic",
            scenario_id=inp.scenario_id,
            seed=seed,
            draws=None,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return MPCOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            control_trajectory=tuple(trajectory),
            optimised_levers=dict(zip(lever_names, [round(v, 2) for v in best_levers], strict=False)),
            total_cost=round(best_cost, 4),
        )
