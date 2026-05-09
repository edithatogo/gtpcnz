"""v1.3.1 uncapped FFS entitlement model.

Source-informed demonstrative model. Not empirically calibrated.
"""
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class Scenario:
    code: str
    name: str
    marginal_supply: float
    population_accountability: float
    equity_protection: float
    fiscal_governance: float
    hospital_deflection: float
    gaming_risk: float

SCENARIOS: List[Scenario] = [
    Scenario('UC0','Legacy baseline / capped upstream supply',28,40,38,54,25,22),
    Scenario('UC1','Current reform pathway',46,55,54,60,44,25),
    Scenario('UC2','Current reform + place accountability',50,70,66,66,49,23),
    Scenario('UC3','Uncapped medical FFS without place accountability',74,38,40,45,58,43),
    Scenario('UC4','Uncapped medical FFS + capitation + place accountability',78,73,70,68,66,29),
    Scenario('UC5','Uncapped weak-control model',82,28,30,25,55,62),
    Scenario('UC6','ACC-style medical-only stream',66,48,50,62,56,32),
    Scenario('UC7','Capitation reweighting only',38,54,55,62,38,20),
    Scenario('UC8','Full hybrid upstream architecture',84,78,76,76,76,24),
]

def hybrid_score(s: Scenario) -> float:
    return round(0.24*s.marginal_supply + 0.18*s.population_accountability + 0.18*s.equity_protection + 0.17*s.fiscal_governance + 0.18*s.hospital_deflection + 0.05*(100-s.gaming_risk), 2)

def hospital_pressure(s: Scenario) -> float:
    return round(max(0, 100 - (0.42*s.hospital_deflection + 0.26*s.marginal_supply + 0.16*s.population_accountability + 0.16*s.equity_protection)), 2)

def results() -> List[Dict[str, object]]:
    return [{
        'scenario': s.code,
        'name': s.name,
        'marginal_supply': s.marginal_supply,
        'population_accountability': s.population_accountability,
        'equity_protection': s.equity_protection,
        'fiscal_governance': s.fiscal_governance,
        'hospital_deflection': s.hospital_deflection,
        'gaming_risk': s.gaming_risk,
        'hybrid_score': hybrid_score(s),
        'estimated_hospital_pressure': hospital_pressure(s),
    } for s in SCENARIOS]
