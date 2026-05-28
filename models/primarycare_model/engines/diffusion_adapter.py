"""Typed adapter for Bass diffusion simulation.

Models the adoption of a new service or policy intervention over time using a
standard Bass diffusion curve: p (innovation) and q (imitation) parameters drive
the cumulative adoption trajectory.
"""

from __future__ import annotations

import numpy as np
from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, UncertaintySummary
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

MAX_DIFFUSION_MONTHS = 120
MIN_DIFFUSION_MONTHS = 12


class DiffusionInput(EngineInput):
    """Engine input for Bass diffusion simulation."""

    months: int = Field(default=60, ge=MIN_DIFFUSION_MONTHS, le=MAX_DIFFUSION_MONTHS)
    p_coefficient: float = Field(default=0.02, ge=0.001, le=0.20)
    q_coefficient: float = Field(default=0.40, ge=0.01, le=0.99)
    market_potential: float = Field(default=1000.0, ge=100.0, le=1_000_000.0)
    initial_adopters: float = Field(default=10.0, ge=0.0)

    # Scenario levers modulating diffusion shape
    activity_signal: float = Field(default=50.0, ge=0.0, le=100.0)
    scope_capacity: float = Field(default=50.0, ge=0.0, le=100.0)
    governance: float = Field(default=50.0, ge=0.0, le=100.0)


class DiffusionOutput(EngineOutput):
    """Engine output from a Bass diffusion simulation."""

    scenario_result: ScenarioResult
    monthly_adoption: tuple[dict[str, float], ...]
    peak_adoption_month: int
    cumulative_adopters: float
    uncertainty_summaries: tuple[UncertaintySummary, ...] = ()


class BassDiffusionAdapter:
    """Typed adapter for Bass diffusion simulation.

    Accepts validated ``DiffusionInput`` and returns ``DiffusionOutput`` with
    per-month adoption, peak timing and cumulative adopters.
    Deterministic when a fixed seed is supplied.
    """

    engine_id = "diffusion_v1"

    def run(self, inputs: DiffusionInput) -> DiffusionOutput:
        inp = inputs
        months = int(min(max(MIN_DIFFUSION_MONTHS, inp.months), MAX_DIFFUSION_MONTHS))
        seed = inp.seed if inp.seed is not None else 20260526
        rng = np.random.default_rng(seed)

        m = float(inp.market_potential)
        p = float(inp.p_coefficient)
        q = float(inp.q_coefficient)

        # Modulation: stronger governance slows adoption (safety), scope/activity accelerate it
        gov_factor = 1.0 - 0.15 * (inp.governance / 100.0)
        scope_factor = 1.0 + 0.20 * (inp.scope_capacity / 100.0)
        activity_factor = 1.0 + 0.10 * (inp.activity_signal / 100.0)
        p_eff = p * activity_factor * scope_factor * gov_factor
        q_eff = q * scope_factor * gov_factor

        adopters = float(inp.initial_adopters)
        trace: list[dict[str, float]] = []
        peak_adoption = 0.0
        peak_month = 1

        for month in range(1, months + 1):
            fraction = adopters / m
            new_adopters = (p_eff + q_eff * fraction) * (m - adopters)
            new_adopters = max(0.0, new_adopters)
            # Add small stochastic noise when seed is provided
            if inp.seed is not None:
                new_adopters *= 1.0 + 0.02 * float(rng.normal(0, 1))
            new_adopters = max(0.0, new_adopters)
            adopters += new_adopters
            adopters = min(adopters, m)

            if new_adopters > peak_adoption:
                peak_adoption = new_adopters
                peak_month = month

            trace.append({
                "month": month,
                "new_adopters": round(new_adopters, 2),
                "cumulative_adopters": round(adopters, 2),
                "penetration_rate": round(adopters / m * 100, 2),
            })

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=round(50.0 + 20.0 * (adopters / m) - 10.0 * (1 - inp.governance / 100), 2),
            access_score=round(40.0 + 30.0 * (adopters / m), 2),
            supply_generation_score=round(40.0 + 25.0 * (adopters / m) + 10.0 * inp.scope_capacity / 100, 2),
            hospital_pressure_score=round(100 - 30.0 * (adopters / m), 2),
            gaming_risk_score=round(20.0 + 15.0 * (inp.activity_signal / 100) - 20.0 * (inp.governance / 100), 2),
            calculation_status="seeded_stochastic" if inp.seed is not None else "live_deterministic",
        )

        manifest = ResultManifest(
            result_id=f"diff_{inp.scenario_id}_{seed}",
            calculation_mode="seeded_stochastic" if inp.seed is not None else "live_deterministic",
            scenario_id=inp.scenario_id,
            seed=seed,
            draws=None,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return DiffusionOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            monthly_adoption=tuple(trace),
            peak_adoption_month=peak_month,
            cumulative_adopters=round(adopters, 2),
        )
