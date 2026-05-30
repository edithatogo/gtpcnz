# Final hybrid model specification v0.8.0

## Purpose

The hybrid model synthesises 14 mapped New Zealand policy games into a scenario-level architecture model. It is a demonstrative, non-calibrated model.

## Inputs

The model uses the scenario levers defined in `demonstrative_games.py`: marginal contact benefit, capitation weighting, scope flexibility, PHO transaction cost, primary and ambulance KPI salience, hospital political penalty, data observability, co-payment level/protections, equity programme strength, telehealth scale/integration, local in-person loading, ambulance alternative funding, ACC funding/constraint, budget tightness, safety governance, gaming controls, direct claiming, stakeholder alignment and narrative coherence.

## Component games

The model calls the 14 game models in `demonstrative_games.py` and computes weighted base metrics.

## Hybrid indices

- supply_generation_index
- equity_legitimacy_index
- governance_resilience_index
- hospital_deflection_index
- implementation_readiness_index
- fiscal_gaming_risk_index
- interaction_penalty
- hybrid_viability_score

## Interpretation

S3 is expected to perform best if the architecture has strong benefits, governance, data, KPIs, equity protections and ambulance alternatives. S4 is expected to have higher fiscal/gaming/equity risk because benefits are loose and controls are weak.

## Calibration status

Not calibrated. The model should not be used for fiscal estimates or predictive claims.
