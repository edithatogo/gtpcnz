"""Typed adapter for Monte Carlo simulation.

Runs seeded stochastic draws over perturbed scenario inputs and returns
per-draw results plus uncertainty summaries for key metrics.
"""

from __future__ import annotations

import numpy as np
from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, UncertaintySummary
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

MAX_DRAWS = 500
MIN_DRAWS = 10
DEFAULT_DRAWS = 100


class MCInput(EngineInput):
    """Engine input for Monte Carlo simulation."""

    draws: int = Field(default=DEFAULT_DRAWS, ge=MIN_DRAWS, le=MAX_DRAWS)
    perturbation_sd: float = Field(default=0.08, ge=0.01, le=0.20)

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


class MCOutput(EngineOutput):
    """Engine output from a Monte Carlo simulation."""

    scenario_result: ScenarioResult
    draw_data: tuple[dict[str, float | int | str], ...]
    uncertainty_summaries: tuple[UncertaintySummary, ...]

class MonteCarloAdapter:
    """Typed adapter for Monte Carlo simulation.

    Accepts validated ``MCInput`` and returns ``MCOutput`` with per-draw results
    and percentile summaries.  Deterministic when a fixed seed is supplied.
    """

    engine_id = "jax_mc_v1"

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return float(max(lower, min(upper, value)))

    @staticmethod
    def _as_fraction(value: float) -> float:
        return float(max(0.0, min(100.0, value))) / 100.0

    def _calculate_indices(self, inp: MCInput) -> dict[str, float]:
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
        compl = self._as_fraction(inp.complexity)
        hosp_sal = self._as_fraction(inp.hospital_salience)

        supply = self._clamp(100 * (0.34 * activity + 0.18 * capitation + 0.24 * scope + 0.12 * urgent + 0.12 * place - 0.12 * budget))
        access = self._clamp(100 * (0.42 * supply / 100 + 0.18 * urgent + 0.15 * equity + 0.12 * place + 0.10 * data - 0.16 * copay))
        equity_leg = self._clamp(100 * (0.34 * equity + 0.24 * place + 0.16 * capitation + 0.14 * data - 0.16 * copay))
        gov_res = self._clamp(100 * (0.44 * governance + 0.20 * data + 0.18 * place + 0.10 * equity + 0.08 * capitation))
        hosp_def = self._clamp(100 * (0.32 * access / 100 + 0.22 * urgent + 0.16 * supply / 100 + 0.16 * data + 0.14 * place - 0.10 * compl))
        gaming = self._clamp(100 * (0.35 * activity + 0.18 * scope + 0.18 * compl - 0.30 * governance - 0.18 * data - 0.16 * place))
        fiscal = self._clamp(100 * (0.22 * activity + 0.18 * gaming / 100 + 0.16 * compl + 0.14 * (1 - budget) - 0.18 * governance - 0.14 * hosp_def / 100))
        hosp_pressure = self._clamp(100 * (0.34 * hosp_sal + 0.26 * (1 - hosp_def / 100) + 0.16 * compl + 0.14 * budget - 0.18 * access / 100 - 0.12 * urgent))
        hybrid = self._clamp(0.24 * supply + 0.18 * access + 0.18 * equity_leg + 0.16 * gov_res + 0.14 * hosp_def + 0.06 * (100 - fiscal) + 0.04 * (100 - gaming))

        return {
            "hybrid_viability_score": round(hybrid, 2),
            "access_score": round(access, 2),
            "supply_generation_score": round(supply, 2),
            "equity_legitimacy_score": round(equity_leg, 2),
            "governance_resilience_score": round(gov_res, 2),
            "hospital_deflection_score": round(hosp_def, 2),
            "fiscal_risk_score": round(fiscal, 2),
            "gaming_risk_score": round(gaming, 2),
            "hospital_pressure_score": round(hosp_pressure, 2),
        }

    def run(self, inputs: MCInput) -> MCOutput:
        inp = inputs
        draws = int(min(max(MIN_DRAWS, inp.draws), MAX_DRAWS))
        sd = float(min(max(inp.perturbation_sd, 0.01), 0.20))
        seed = inp.seed if inp.seed is not None else 20260526
        rng = np.random.default_rng(seed)

        # Reference (unperturbed) calculation
        ref = self._calculate_indices(inp)

        # Stochastic draws
        keys = ["hybrid_viability_score", "access_score", "hospital_pressure_score", "gaming_risk_score", "fiscal_risk_score"]
        draw_metrics: dict[str, list[float]] = {k: [] for k in keys}
        draw_rows: list[dict[str, float | int | str]] = []

        for draw in range(draws):
            perturbed = MCInput(
                scenario_id=inp.scenario_id,
                draws=inp.draws,
                perturbation_sd=inp.perturbation_sd,
                seed=seed,
                claim_boundary=inp.claim_boundary,
                activity_signal=self._clamp(float(rng.normal(inp.activity_signal, sd * 100.0))),
                capitation=self._clamp(float(rng.normal(inp.capitation, sd * 100.0))),
                place_accountability=self._clamp(float(rng.normal(inp.place_accountability, sd * 100.0))),
                scope_capacity=self._clamp(float(rng.normal(inp.scope_capacity, sd * 100.0))),
                urgent_ambulance=self._clamp(float(rng.normal(inp.urgent_ambulance, sd * 100.0))),
                data_visibility=self._clamp(float(rng.normal(inp.data_visibility, sd * 100.0))),
                governance=self._clamp(float(rng.normal(inp.governance, sd * 100.0))),
                equity_protection=self._clamp(float(rng.normal(inp.equity_protection, sd * 100.0))),
                copayment_burden=self._clamp(float(rng.normal(inp.copayment_burden, sd * 100.0))),
                budget_tightness=self._clamp(float(rng.normal(inp.budget_tightness, sd * 100.0))),
                hospital_salience=self._clamp(float(rng.normal(inp.hospital_salience, sd * 100.0))),
                complexity=self._clamp(float(rng.normal(inp.complexity, sd * 100.0))),
            )
            idx = self._calculate_indices(perturbed)
            row: dict[str, float | int | str] = {"draw": draw + 1, "scenario_id": inp.scenario_id}
            row.update(idx)
            draw_rows.append(row)
            for k in keys:
                draw_metrics[k].append(float(idx[k]))

        summaries: list[UncertaintySummary] = []
        for metric in keys:
            values = np.array(draw_metrics[metric])
            summaries.append(
                UncertaintySummary(
                    metric=metric,
                    mean=round(float(values.mean()), 2),
                    std=round(float(values.std()), 2),
                    p05=round(float(np.percentile(values, 5)), 2),
                    p50=round(float(np.percentile(values, 50)), 2),
                    p95=round(float(np.percentile(values, 95)), 2),
                    draws=draws,
                )
            )

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=ref["hybrid_viability_score"],
            access_score=ref["access_score"],
            supply_generation_score=ref["supply_generation_score"],
            hospital_pressure_score=ref["hospital_pressure_score"],
            gaming_risk_score=ref["gaming_risk_score"],
            calculation_status="seeded_stochastic",
        )

        manifest = ResultManifest(
            result_id=f"mc_{inp.scenario_id}_{seed}",
            calculation_mode="seeded_stochastic",
            scenario_id=inp.scenario_id,
            seed=seed,
            draws=draws,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return MCOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            draw_data=tuple(draw_rows),
            uncertainty_summaries=tuple(summaries),
        )

