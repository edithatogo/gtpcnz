"""Typed adapter for one-at-a-time (OAT) sensitivity analysis.

Holds all but one scenario lever at baseline and perturbs the free lever across
its domain to measure the resulting change in each output metric.
"""

from __future__ import annotations

from pydantic import Field

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, UncertaintySummary
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult

SENSITIVITY_LEVERS = [
    "activity_signal",
    "capitation",
    "place_accountability",
    "scope_capacity",
    "urgent_ambulance",
    "data_visibility",
    "governance",
    "equity_protection",
    "copayment_burden",
    "budget_tightness",
    "hospital_salience",
    "complexity",
]


class SensitivityInput(EngineInput):
    """Engine input for one-at-a-time sensitivity analysis."""

    baseline_activity_signal: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_capitation: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_place_accountability: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_scope_capacity: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_urgent_ambulance: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_data_visibility: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_governance: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_equity_protection: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_copayment_burden: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_budget_tightness: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_hospital_salience: float = Field(default=50.0, ge=0.0, le=100.0)
    baseline_complexity: float = Field(default=50.0, ge=0.0, le=100.0)

    low_percentile: float = Field(default=25.0, ge=0.0, le=100.0)
    high_percentile: float = Field(default=75.0, ge=0.0, le=100.0)
    delta_step: float = Field(default=10.0, ge=1.0, le=50.0)


class SensitivityOutput(EngineOutput):
    """Engine output from sensitivity analysis."""

    scenario_result: ScenarioResult
    oat_sensitivities: tuple[dict[str, float | str], ...]
    uncertainty_summaries: tuple[UncertaintySummary, ...] = ()


class SensitivityAnalysisAdapter:
    """Typed adapter for one-at-a-time sensitivity analysis.

    For each lever, perturbs the value by +/- delta_step while holding all other
    levers at baseline, and records the change in each output metric.
    """

    engine_id = "sensitivity_v1"

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return float(max(lower, min(upper, value)))

    @staticmethod
    def _as_fraction(value: float) -> float:
        return float(max(0.0, min(100.0, value))) / 100.0

    @staticmethod
    def _calculate_indices(
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

        a, c, p, s, u, d, g, e, cp, b, hs, cx = [f(v) for v in (activity, capitation, place, scope, urgent, data, governance, equity, copay, budget, hosp_sal, compl)]

        supply = 100 * (0.34 * a + 0.18 * c + 0.24 * s + 0.12 * u + 0.12 * p - 0.12 * b)
        access = 100 * (0.42 * supply / 100 + 0.18 * u + 0.15 * e + 0.12 * p + 0.10 * d - 0.16 * cp)
        equity_leg = 100 * (0.34 * e + 0.24 * p + 0.16 * c + 0.14 * d - 0.16 * cp)
        gov_res = 100 * (0.44 * g + 0.20 * d + 0.18 * p + 0.10 * e + 0.08 * c)
        hosp_def = 100 * (0.32 * access / 100 + 0.22 * u + 0.16 * supply / 100 + 0.16 * d + 0.14 * p - 0.10 * cx)
        gaming = 100 * (0.35 * a + 0.18 * s + 0.18 * cx - 0.30 * g - 0.18 * d - 0.16 * p)
        fiscal = 100 * (0.22 * a + 0.18 * gaming / 100 + 0.16 * cx + 0.14 * (1 - b) - 0.18 * g - 0.14 * hosp_def / 100)
        hosp_pressure = 100 * (0.34 * hs + 0.26 * (1 - hosp_def / 100) + 0.16 * cx + 0.14 * b - 0.18 * access / 100 - 0.12 * u)
        hybrid = 0.24 * supply + 0.18 * access + 0.18 * equity_leg + 0.16 * gov_res + 0.14 * hosp_def + 0.06 * (100 - fiscal) + 0.04 * (100 - gaming)

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

    @staticmethod
    def _get_baseline(inp: SensitivityInput) -> list[float]:
        return [
            inp.baseline_activity_signal,
            inp.baseline_capitation,
            inp.baseline_place_accountability,
            inp.baseline_scope_capacity,
            inp.baseline_urgent_ambulance,
            inp.baseline_data_visibility,
            inp.baseline_governance,
            inp.baseline_equity_protection,
            inp.baseline_copayment_burden,
            inp.baseline_budget_tightness,
            inp.baseline_hospital_salience,
            inp.baseline_complexity,
        ]

    def run(self, inputs: SensitivityInput) -> SensitivityOutput:
        inp = inputs
        baseline = self._get_baseline(inp)
        ref = self._calculate_indices(*baseline)
        step = float(min(max(inp.delta_step, 1.0), 50.0))

        oat_rows: list[dict[str, float | str]] = []
        target_metrics = ["hybrid_viability_score", "access_score", "supply_generation_score", "hospital_pressure_score", "gaming_risk_score", "fiscal_risk_score"]

        for i, lever in enumerate(SENSITIVITY_LEVERS):
            for tag, direction in [("low", -step), ("high", +step)]:
                perturbed = list(baseline)
                perturbed[i] = self._clamp(perturbed[i] + direction)
                idx = self._calculate_indices(*perturbed)
                row: dict[str, float | str] = {"lever": lever, "perturbation": f"{tag} ({direction:+.0f})"}
                for metric in target_metrics:
                    row[f"delta_{metric}"] = round(float(idx[metric]) - float(ref[metric]), 2)
                oat_rows.append(row)

        scenario_result = ScenarioResult(
            scenario_id=inp.scenario_id,
            hybrid_viability_score=ref["hybrid_viability_score"],
            access_score=ref["access_score"],
            supply_generation_score=ref["supply_generation_score"],
            hospital_pressure_score=ref["hospital_pressure_score"],
            gaming_risk_score=ref["gaming_risk_score"],
            calculation_status="live_deterministic",
        )

        manifest = ResultManifest(
            result_id=f"sa_{inp.scenario_id}",
            calculation_mode="live_deterministic",
            scenario_id=inp.scenario_id,
            seed=None,
            draws=None,
            claim_boundary=inp.claim_boundary,
            validation_status="validated",
        )

        return SensitivityOutput(
            manifest=manifest,
            scenario_result=scenario_result,
            oat_sensitivities=tuple(oat_rows),
        )
