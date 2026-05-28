"""Typed adapter for system dynamics (stock-flow) simulation.

Produces month-by-month traces of need, capacity, utilisation and pressure
metrics for a given scenario over a multi-year horizon.
"""

from __future__ import annotations

import numpy as np
from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, UncertaintySummary
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

MAX_MONTHS = 60
MIN_MONTHS = 6


class SDInput(EngineInput):
    """Engine input for system dynamics simulation."""

    months: int = Field(default=36, ge=MIN_MONTHS, le=MAX_MONTHS)

    # Scenario lever values (0-100) for stock-flow dynamics
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


class SDOutput(EngineOutput):
    """Engine output from a system dynamics simulation."""

    scenario_result: ScenarioResult
    monthly_trace: tuple[dict[str, float | int | str], ...]
    uncertainty_summaries: tuple[UncertaintySummary, ...] = ()


class SystemDynamicsAdapter:
    """Typed adapter for system dynamics (stock-flow) simulation.

    Accepts validated ``SDInput`` and returns ``SDOutput`` with monthly traces
    of need, capacity, utilisation and hospital/fiscal pressure.
    Deterministic when a fixed seed is supplied.
    """

    engine_id = "sd_v1"

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return float(max(lower, min(upper, value)))

    def run(self, inputs: SDInput) -> SDOutput:
        inp = inputs
        months = int(min(max(MIN_MONTHS, inp.months), MAX_MONTHS))
        seed = inp.seed if inp.seed is not None else 20260526
        np.random.default_rng(seed)  # kept for future perturbation use

        def f(x: float) -> float:
            return float(max(0.0, min(100.0, x))) / 100.0

        activity = f(inp.activity_signal)
        capitation = f(inp.capitation)
        place = f(inp.place_accountability)
        scope = f(inp.scope_capacity)
        urgent = f(inp.urgent_ambulance)
        data = f(inp.data_visibility)
        governance = f(inp.governance)
        equity = f(inp.equity_protection)
        copay = f(inp.copayment_burden)
        budget = f(inp.budget_tightness)

        supply = self._clamp(
            100 * (0.34 * activity + 0.18 * capitation + 0.24 * scope + 0.12 * urgent + 0.12 * place - 0.12 * budget)
        )
        access = self._clamp(
            100 * (0.42 * supply / 100 + 0.18 * urgent + 0.15 * equity + 0.12 * place + 0.10 * data - 0.16 * copay)
        )
        hospital_pressure_idx = self._clamp(
            100
            * (
                0.34 * f(inp.hospital_salience)
                + 0.26 * (1 - access / 100)
                + 0.16 * f(inp.complexity)
                + 0.14 * budget
                - 0.18 * access / 100
                - 0.12 * urgent
            )
        )
        gaming_risk = self._clamp(
            100 * (0.35 * activity + 0.18 * scope + 0.18 * f(inp.complexity) - 0.30 * governance - 0.18 * data - 0.16 * place)
        )
        fiscal_risk = self._clamp(
            100 * (0.22 * activity + 0.18 * gaming_risk / 100 + 0.16 * f(inp.complexity) + 0.14 * (1 - budget) - 0.18 * governance)
        )

        # --- stock-flow dynamics ---
        capacity = 35.0 + 0.45 * supply
        unmet = 70.0 + 0.35 * inp.budget_tightness - 0.55 * access
        trace: list[dict[str, float | int | str]] = []

        for month in range(1, months + 1):
            seasonal = 1.0 + 0.05 * np.sin(2 * np.pi * month / 12.0)
            need = 55.0 * seasonal + 0.18 * unmet + 0.15 * inp.complexity
            capacity = max(1.0, capacity + 0.06 * supply + 0.04 * inp.place_accountability - 0.05 * inp.budget_tightness)
            served = min(need + 0.20 * unmet, capacity * (0.72 + access / 250.0))
            ambulance_resolved = min(need * (0.08 + inp.urgent_ambulance / 400.0), 12.0 + capacity / 10.0)
            unmet = max(0.0, 0.70 * unmet + need - served - ambulance_resolved)
            hospital_pressure = self._clamp(35.0 + 0.42 * unmet + 0.28 * inp.hospital_salience - 0.32 * hospital_pressure_idx)
            fiscal_pressure = self._clamp(20.0 + 0.28 * fiscal_risk + 0.12 * unmet + 0.08 * served)

            trace.append(
                {
                    "month": month,
                    "scenario_id": inp.scenario_id,
                    "need_generated": round(float(need), 2),
                    "primary_contacts": round(float(served), 2),
                    "ambulance_resolved": round(float(ambulance_resolved), 2),
                    "unmet_need": round(float(unmet), 2),
                    "primary_capacity": round(float(capacity), 2),
                    "hospital_pressure": round(float(hospital_pressure), 2),
                    "fiscal_pressure": round(float(fiscal_pressure), 2),
                }
            )

        equity_legitimacy = self._clamp(100 * (0.34 * equity + 0.24 * place + 0.16 * capitation + 0.14 * data - 0.16 * copay))
        governance_resilience = self._clamp(100 * (0.44 * governance + 0.20 * data + 0.18 * place + 0.10 * equity + 0.08 * capitation))
        hospital_deflection = self._clamp(100 * (0.32 * access / 100 + 0.22 * urgent + 0.16 * supply / 100 + 0.16 * data + 0.14 * place - 0.10 * f(inp.complexity)))
        hybrid = self._clamp(
            0.24 * supply
            + 0.18 * access
            + 0.18 * equity_legitimacy
            + 0.16 * governance_resilience
            + 0.14 * hospital_deflection
            + 0.06 * (100 - fiscal_risk)
            + 0.04 * (100 - gaming_risk)
        )

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=round(hybrid, 2),
            access_score=round(access, 2),
            supply_generation_score=round(supply, 2),
            hospital_pressure_score=round(hospital_pressure_idx, 2),
            gaming_risk_score=round(gaming_risk, 2),
            calculation_status="live_deterministic" if inp.seed is not None else "seeded_stochastic",
        )

        manifest = ResultManifest(
            result_id=f"sd_{inp.scenario_id}_{seed}",
            calculation_mode="seeded_stochastic",
            scenario_id=inp.scenario_id,
            seed=seed,
            draws=None,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return SDOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            monthly_trace=tuple(trace),
        )
