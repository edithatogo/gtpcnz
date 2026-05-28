"""Typed adapter for agent-based model simulation.

Simulates a capped population of heterogeneous agents over a finite time horizon
to explore access, barrier and contact-pattern dynamics under a given scenario.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, UncertaintySummary
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

MAX_ABM_POPULATION = 500
DEFAULT_ABM_POPULATION = 180
MAX_MONTHS = 24
MIN_MONTHS = 3


class ABMInput(EngineInput):
    """Engine input for agent-based model simulation."""

    population_size: int = Field(default=DEFAULT_ABM_POPULATION, ge=50, le=MAX_ABM_POPULATION)
    months: int = Field(default=12, ge=MIN_MONTHS, le=MAX_MONTHS)

    # Scenario lever values (0-100) for index calculation
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


class ABMOutput(EngineOutput):
    """Engine output from an agent-based model simulation."""

    scenario_result: ScenarioResult
    agent_data: tuple[dict[str, Any], ...]
    summary: tuple[dict[str, int | float | str], ...]
    uncertainty_summaries: tuple[UncertaintySummary, ...] = ()


class _IndexCalculator:
    """Stateless helper that mirrors runtime_lab calculate_indices logic."""

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return float(max(lower, min(upper, value)))

    @staticmethod
    def _as_fraction(value: float) -> float:
        return float(max(0.0, min(100.0, value))) / 100.0

    def calculate(self, inp: ABMInput) -> dict[str, float]:
        activity = self._as_fraction(inp.activity_signal)
        capitation = self._as_fraction(inp.capitation)
        place = self._as_fraction(inp.place_accountability)
        scope = self._as_fraction(inp.scope_capacity)
        urgent = self._as_fraction(inp.urgent_ambulance)
        data = self._as_fraction(inp.data_visibility)
        governance = self._as_fraction(inp.governance)
        equity = self._as_fraction(inp.equity_protection)
        copay = self._as_fraction(inp.copayment_burden)
        budget = self._as_fraction(inp.budget_tightness)

        supply = self._clamp(
            100 * (0.34 * activity + 0.18 * capitation + 0.24 * scope + 0.12 * urgent + 0.12 * place - 0.12 * budget)
        )
        access = self._clamp(
            100 * (0.42 * supply / 100 + 0.18 * urgent + 0.15 * equity + 0.12 * place + 0.10 * data - 0.16 * copay)
        )
        hospital_pressure = self._clamp(
            100
            * (
                0.34 * self._as_fraction(inp.hospital_salience)
                + 0.26 * (1 - access / 100)
                + 0.16 * self._as_fraction(inp.complexity)
                + 0.14 * budget
                - 0.18 * access / 100
                - 0.12 * urgent
            )
        )
        gaming_risk = self._clamp(
            100 * (0.35 * activity + 0.18 * scope + 0.18 * self._as_fraction(inp.complexity) - 0.30 * governance - 0.18 * data - 0.16 * place)
        )

        return {
            "access_score": round(access, 2),
            "supply_generation_score": round(supply, 2),
            "hospital_pressure_score": round(hospital_pressure, 2),
            "gaming_risk_score": round(gaming_risk, 2),
        }


class AgentBasedModelAdapter:
    """Typed adapter for agent-based model simulation.

    Accepts validated ``ABMInput`` and returns ``ABMOutput`` with per-agent
    contact data and aggregate summaries.  Deterministic when a fixed seed is
    supplied.
    """

    engine_id = "abm_v1"

    def run(self, inputs: ABMInput) -> ABMOutput:
        inp = inputs
        pop = int(min(max(50, inp.population_size), MAX_ABM_POPULATION))
        months = int(min(max(MIN_MONTHS, inp.months), MAX_MONTHS))
        seed = inp.seed if inp.seed is not None else 20260526
        rng = np.random.default_rng(seed)

        idx = _IndexCalculator().calculate(inp)

        high_need = rng.beta(2.2, 3.4, pop)
        rural = rng.random(pop) < (0.08 + inp.complexity / 260.0)
        barrier = np.clip(
            0.45 * high_need
            + 0.30 * rural.astype(float)
            + inp.copayment_burden / 180.0
            - inp.equity_protection / 240.0,
            0,
            1,
        )
        access_probability = np.clip(
            idx["access_score"] / 100.0 - 0.35 * barrier + inp.place_accountability / 350.0, 0.05, 0.95
        )
        contact_attempts = rng.random((months, pop)) < np.clip(0.22 + 0.30 * high_need, 0.05, 0.85)
        successful = rng.random((months, pop)) < access_probability
        served = contact_attempts & successful

        agent_data = tuple(
            {
                "patient_id": int(pid),
                "high_need_score": round(float(high_need[pid - 1]), 3),
                "rural": bool(rural[pid - 1]),
                "access_barrier": round(float(barrier[pid - 1]), 3),
                "access_probability": round(float(access_probability[pid - 1]), 3),
                "served_contacts": int(served[:, pid - 1].sum()),
                "unmet_attempts": int((contact_attempts[:, pid - 1] & ~successful[:, pid - 1]).sum()),
            }
            for pid in range(1, pop + 1)
        )

        served_total = sum(a["served_contacts"] for a in agent_data)
        unmet_total = sum(a["unmet_attempts"] for a in agent_data)
        mean_access_prob = float(np.mean(access_probability))
        high_barrier_share = float(np.mean(barrier >= 0.6))

        summary = (
            {"metric": "population_size", "value": pop},
            {"metric": "months", "value": months},
            {"metric": "mean_access_probability", "value": round(mean_access_prob, 3)},
            {"metric": "served_contacts", "value": served_total},
            {"metric": "unmet_attempts", "value": unmet_total},
            {"metric": "high_barrier_share", "value": round(high_barrier_share, 3)},
        )

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=idx.get("hybrid_viability_score", 50.0),
            access_score=idx["access_score"],
            supply_generation_score=idx["supply_generation_score"],
            hospital_pressure_score=idx["hospital_pressure_score"],
            gaming_risk_score=idx["gaming_risk_score"],
            calculation_status="live_deterministic" if inp.seed is not None else "seeded_stochastic",
        )

        manifest = ResultManifest(
            result_id=f"abm_{inp.scenario_id}_{seed}",
            calculation_mode="seeded_stochastic",
            scenario_id=inp.scenario_id,
            seed=seed,
            draws=None,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return ABMOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            agent_data=agent_data,
            summary=summary,
        )
