"""Calibration starter for the primary care funding architecture model.

This module is deliberately a *starter*, not a finished calibrated model. It provides:
- a minimal data schema for monthly observed outcomes;
- a simple dynamic simulation linking primary care supply, unmet need, ED demand and costs;
- a deterministic least-squares calibration routine that can be replaced by Bayesian calibration;
- a synthetic-data demo so the pipeline is executable before confidential linked NZ data are available.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable
import math
import random
import pandas as pd

@dataclass(frozen=True)
class CalibrationParameters:
    marginal_supply_response: float
    unmet_need_to_ed_rate: float
    copayment_elasticity: float
    ambulance_deflection_rate: float
    acc_stabilisation_effect: float
    scope_supply_multiplier: float
    base_primary_contacts: float = 1000.0
    base_ed_presentations: float = 220.0
    base_public_cost: float = 1_000_000.0

@dataclass(frozen=True)
class ScenarioInputs:
    scheduled_benefit_strength: float
    capitation_weighting_strength: float
    copayment_level: float
    ambulance_alternative_strength: float
    acc_activity_strength: float
    scope_flexibility: float
    governance_controls: float

@dataclass(frozen=True)
class MonthlyObservation:
    month: int
    primary_contacts: float
    unmet_need_index: float
    ed_presentations: float
    ambulance_conveyances: float
    public_cost: float

DEFAULT_BASELINE = ScenarioInputs(
    scheduled_benefit_strength=0.10,
    capitation_weighting_strength=0.35,
    copayment_level=0.45,
    ambulance_alternative_strength=0.25,
    acc_activity_strength=0.55,
    scope_flexibility=0.35,
    governance_controls=0.65,
)

FULL_HYBRID = ScenarioInputs(
    scheduled_benefit_strength=0.75,
    capitation_weighting_strength=0.80,
    copayment_level=0.35,
    ambulance_alternative_strength=0.75,
    acc_activity_strength=0.70,
    scope_flexibility=0.80,
    governance_controls=0.85,
)

TRUE_SYNTHETIC = CalibrationParameters(
    marginal_supply_response=0.42,
    unmet_need_to_ed_rate=0.33,
    copayment_elasticity=0.26,
    ambulance_deflection_rate=0.28,
    acc_stabilisation_effect=0.18,
    scope_supply_multiplier=0.31,
)

STARTING_PRIOR = CalibrationParameters(
    marginal_supply_response=0.30,
    unmet_need_to_ed_rate=0.25,
    copayment_elasticity=0.20,
    ambulance_deflection_rate=0.20,
    acc_stabilisation_effect=0.12,
    scope_supply_multiplier=0.20,
)

def simulate_months(params: CalibrationParameters, inputs: ScenarioInputs, months: int = 24) -> pd.DataFrame:
    """Run a minimal dynamic monthly simulation.

    The equations are stylised. They are placeholders for empirically estimated transition
    functions once linked data are available.
    """
    rows=[]
    unmet=55.0
    for m in range(1, months+1):
        seasonal = 1 + 0.05 * math.sin(2 * math.pi * m / 12)
        supply_gain = (
            params.marginal_supply_response * inputs.scheduled_benefit_strength
            + params.scope_supply_multiplier * inputs.scope_flexibility
            + params.acc_stabilisation_effect * inputs.acc_activity_strength
            + 0.12 * inputs.capitation_weighting_strength
        )
        price_suppression = params.copayment_elasticity * inputs.copayment_level
        primary_contacts = params.base_primary_contacts * seasonal * (1 + supply_gain - price_suppression)
        unmet = max(0.0, 0.82 * unmet + 72 * (1 - supply_gain) + 35 * price_suppression - 18 * inputs.governance_controls)
        ed_presentations = params.base_ed_presentations * seasonal + params.unmet_need_to_ed_rate * unmet * 2.5
        ambulance_conveyances = 80 * seasonal + 0.45 * unmet - 35 * params.ambulance_deflection_rate * inputs.ambulance_alternative_strength
        gaming_cost = 120000 * max(0.0, inputs.scheduled_benefit_strength - inputs.governance_controls)
        public_cost = params.base_public_cost + 90 * primary_contacts + 1550 * ed_presentations + 900 * ambulance_conveyances + gaming_cost
        rows.append(MonthlyObservation(m, primary_contacts, unmet, ed_presentations, ambulance_conveyances, public_cost))
    return pd.DataFrame([asdict(r) for r in rows])

def make_synthetic_observations(months: int = 24, seed: int = 150) -> pd.DataFrame:
    rng=random.Random(seed)
    df=simulate_months(TRUE_SYNTHETIC, DEFAULT_BASELINE, months)
    noisy=df.copy()
    for col, sd in [('primary_contacts',35),('unmet_need_index',4),('ed_presentations',8),('ambulance_conveyances',5),('public_cost',35000)]:
        noisy[col]=[max(0,v+rng.gauss(0,sd)) for v in noisy[col]]
    return noisy

def objective(params: CalibrationParameters, observed: pd.DataFrame, inputs: ScenarioInputs = DEFAULT_BASELINE) -> float:
    pred=simulate_months(params, inputs, len(observed))
    err=0.0
    for col, scale in [('primary_contacts',1000),('unmet_need_index',100),('ed_presentations',250),('ambulance_conveyances',150),('public_cost',1_500_000)]:
        diff=(pred[col].values-observed[col].values)/scale
        err += float((diff**2).mean())
    return err

def calibrate_grid(observed: pd.DataFrame, starting: CalibrationParameters = STARTING_PRIOR) -> CalibrationParameters:
    """Small deterministic coordinate-search calibration.

    This is not intended as the final method. It is robust enough for a starter pipeline and
    avoids additional dependencies. Replace with Bayesian calibration or simulated method of
    moments once real data are available.
    """
    values=asdict(starting)
    fixed={k: values.pop(k) for k in ['base_primary_contacts','base_ed_presentations','base_public_cost']}
    names=list(values)
    steps={name:0.12 for name in names}
    best=CalibrationParameters(**values, **fixed)
    best_score=objective(best, observed)
    for _ in range(8):
        improved=False
        for name in names:
            current=asdict(best)
            for direction in (-1,1):
                cand=current.copy()
                cand[name]=min(0.95,max(0.01,cand[name]+direction*steps[name]))
                cp=CalibrationParameters(**cand)
                score=objective(cp, observed)
                if score < best_score:
                    best, best_score, improved = cp, score, True
        if not improved:
            for name in names: steps[name]*=0.5
    return best

def run_calibration_demo(months: int = 24) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    observed=make_synthetic_observations(months)
    fitted=calibrate_grid(observed)
    pred=simulate_months(fitted, DEFAULT_BASELINE, months)
    params=[]
    true=asdict(TRUE_SYNTHETIC); fit=asdict(fitted); prior=asdict(STARTING_PRIOR)
    for name in ['marginal_supply_response','unmet_need_to_ed_rate','copayment_elasticity','ambulance_deflection_rate','acc_stabilisation_effect','scope_supply_multiplier']:
        params.append({'parameter':name,'starting_prior':prior[name],'synthetic_truth':true[name],'fitted_estimate':fit[name]})
    scen=[]
    for label,inp in [('baseline', DEFAULT_BASELINE), ('full_hybrid', FULL_HYBRID)]:
        out=simulate_months(fitted, inp, months)
        scen.append({'scenario':label,'mean_primary_contacts':out.primary_contacts.mean(),'mean_unmet_need':out.unmet_need_index.mean(),'mean_ed_presentations':out.ed_presentations.mean(),'mean_ambulance_conveyances':out.ambulance_conveyances.mean(),'mean_public_cost':out.public_cost.mean()})
    return observed, pred, pd.DataFrame(params), pd.DataFrame(scen)
