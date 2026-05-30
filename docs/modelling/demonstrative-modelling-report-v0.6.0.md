# Demonstrative game modelling report v0.6.0
Status: demonstrative, non-calibrated, hypothesis-testing scaffold.
This report turns each of the 14 mapped New Zealand policy games into a small executable model. The outputs are not empirical estimates. They are structured demonstrations of how the hypothesised mechanisms behave under contrasting policy architectures.
## Scenarios
| Scenario | Description |
|---|---|
| S0 | Status quo tight control: dominant capitation/contracting, PHO intermediation, limited marginal benefit, high hospital salience. |
| S1 | Capitation reweighting only: better allocation inside capitation, modest access target/data improvement, no material demand-driven benefit stream. |
| S2 | Primary Care Benefits Schedule: contact-type benefits added to capitation, optional/direct claiming and moderate safeguards. |
| S3 | Full upstream access architecture: benefits schedule plus strong KPIs, data, ambulance alternatives, scope flexibility and equity protections. |
| S4 | Loose benefits, weak controls: high benefit activity with weak governance, weak equity protections and high gaming risk. |

## Mean scenario results
| Scenario | Access | Viability | Equity | Fiscal control | Hospital pressure | Gaming risk | Welfare |
|---|---:|---:|---:|---:|---:|---:|---:|
| S0 | 32.08 | 35.6 | 57.13 | 76.23 | 78.1 | 21.51 | 40.87 |
| S1 | 38.06 | 39.44 | 65.41 | 77.07 | 72.15 | 20.28 | 46.27 |
| S2 | 63.36 | 62.21 | 71.05 | 70.24 | 52.1 | 20.3 | 60.27 |
| S3 | 74.78 | 70.14 | 81.89 | 72.15 | 39.45 | 16.08 | 70.15 |
| S4 | 65.93 | 65.66 | 55.19 | 62.87 | 53.56 | 35.32 | 53.88 |

## Interpretation
Across the demonstrative parameterisation, S1 improves equity and information relative to S0 but does not fully reverse the marginal-supply problem. S2 and S3 improve access and reduce hospital pressure because eligible activity can expand. S4 is deliberately included as a caution: unrestricted demand-driven benefits without strong governance improve access but materially increase gaming, equity and safety risk.

## Per-game model cards

### G1: Hospital-salience budget game
Mechanism: Hospital rescue bias falls only when upstream access becomes visible, funded and politically salient.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | hospital-rescue equilibrium | 28.2 | 81.29 | 20.06 | 38.43 |
| S1 | hospital-rescue equilibrium | 34.4 | 71.1 | 18.7 | 44.47 |
| S2 | upstream-salience equilibrium | 57.4 | 46.3 | 21.25 | 56.31 |
| S3 | upstream-salience equilibrium | 69.3 | 30.76 | 16.5 | 66.51 |
| S4 | upstream-salience equilibrium | 68.6 | 36.83 | 34.38 | 54.11 |

### G2: Health NZ internal allocation game
Mechanism: Management attention shifts upstream when primary and ambulance outcomes have hospital-equivalent salience.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | hospital-operations dominance | 28.65 | 70.71 | 30.21 | 35.47 |
| S1 | hospital-operations dominance | 35.86 | 64.43 | 29.12 | 41.13 |
| S2 | hospital-operations dominance | 53.65 | 46.4 | 27.77 | 54.2 |
| S3 | balanced internal accountability | 66.8 | 33.48 | 24.1 | 63.64 |
| S4 | balanced internal accountability | 60.65 | 39.22 | 36.05 | 53.06 |

### G3: Capitation marginal-supply game
Mechanism: Additional contacts expand only when combined public benefit and co-payment exceed marginal cost, admin cost and risk.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | marginal-rationing equilibrium | 22.14 | 80.92 | 10.56 | 38.14 |
| S1 | marginal-rationing equilibrium | 26.49 | 77.29 | 11.2 | 44.17 |
| S2 | marginal-expansion equilibrium | 80.08 | 35.86 | 15.25 | 71.08 |
| S3 | marginal-expansion equilibrium | 84.41 | 30.64 | 13.0 | 76.09 |
| S4 | marginal-expansion equilibrium | 88.88 | 28.52 | 26.88 | 67.38 |

### G4: Consumer access pathway game
Mechanism: Patients move to lower-cost access when price, wait, travel and trust costs are lower than delay or ED substitution.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | delay/ED-substitution equilibrium | 32.42 | 82.14 | 20.97 | 41.9 |
| S1 | delay/ED-substitution equilibrium | 40.18 | 75.59 | 20.4 | 46.99 |
| S2 | early-access equilibrium | 66.99 | 56.31 | 18.53 | 60.61 |
| S3 | early-access equilibrium | 79.59 | 46.62 | 15.2 | 68.67 |
| S4 | early-access equilibrium | 57.93 | 65.42 | 27.3 | 51.59 |

### G5: PHO intermediation game
Mechanism: Direct claiming improves entry only if PHO/locality equity and population-health functions are explicitly preserved.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | intermediated-gatekeeping equilibrium | 8.96 | 86.25 | 27.0 | 29.26 |
| S1 | intermediated-gatekeeping equilibrium | 13.51 | 81.08 | 25.0 | 34.55 |
| S2 | optional/direct-claiming equilibrium | 63.26 | 41.29 | 27.6 | 60.71 |
| S3 | optional/direct-claiming equilibrium | 68.41 | 35.5 | 22.35 | 67.51 |
| S4 | optional/direct-claiming equilibrium | 76.71 | 34.63 | 38.85 | 59.94 |

### G6: ACC/Health NZ cross-funder game
Mechanism: ACC activity funding can stabilise lower-cost capacity; constraining it in isolation risks spillover to Health NZ and patients.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | siloed-cost-shifting equilibrium | 31.85 | 75.99 | 26.9 | 38.68 |
| S1 | whole-of-Crown flow equilibrium | 36.98 | 71.16 | 24.3 | 44.19 |
| S2 | whole-of-Crown flow equilibrium | 55.12 | 56.26 | 21.6 | 55.7 |
| S3 | whole-of-Crown flow equilibrium | 62.42 | 47.06 | 17.3 | 63.44 |
| S4 | whole-of-Crown flow equilibrium | 61.0 | 51.44 | 28.5 | 54.38 |

### G7: Ambulance conveyance game
Mechanism: Alternative disposition is stable only when payment, clinical governance, data and follow-up reduce organisational risk.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | ED-conveyance default | 35.35 | 87.89 | 17.94 | 41.54 |
| S1 | ED-conveyance default | 40.46 | 84.76 | 15.5 | 45.52 |
| S2 | ED-conveyance default | 50.64 | 74.77 | 14.0 | 52.14 |
| S3 | safe alternative-disposition equilibrium | 70.77 | 53.2 | 11.5 | 66.18 |
| S4 | ED-conveyance default | 52.27 | 75.4 | 22.85 | 48.23 |

### G8: Scope-of-practice supply game
Mechanism: Funding eligibility should follow safe scope and governance, not professional category alone.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | professional-bottleneck equilibrium | 30.55 | 86.12 | 16.1 | 41.59 |
| S1 | professional-bottleneck equilibrium | 34.73 | 82.02 | 15.2 | 45.44 |
| S2 | professional-bottleneck equilibrium | 64.1 | 58.75 | 13.4 | 61.34 |
| S3 | scope-enabled supply equilibrium | 78.24 | 41.56 | 10.7 | 73.23 |
| S4 | professional-bottleneck equilibrium | 66.32 | 60.28 | 46.5 | 51.83 |

### G9: Telehealth/local-supply game
Mechanism: Telehealth improves simple access but must be integrated and paired with local in-person capacity.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | telehealth-substitution/fragmentation | 42.08 | 75.97 | 28.35 | 42.5 |
| S1 | telehealth-substitution/fragmentation | 47.68 | 71.27 | 26.57 | 47.01 |
| S2 | integrated hybrid-access equilibrium | 65.07 | 56.31 | 22.77 | 59.35 |
| S3 | integrated hybrid-access equilibrium | 76.38 | 44.27 | 16.62 | 70.77 |
| S4 | telehealth-substitution/fragmentation | 65.35 | 65.96 | 38.09 | 47.96 |

### G10: Co-payment calibration game
Mechanism: Co-payment can moderate discretionary demand but becomes a delayed-care mechanism without protections.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | price-rationing equity failure | 48.76 | 66.56 | 10.63 | 52.56 |
| S1 | price-rationing equity failure | 56.34 | 59.74 | 11.34 | 57.09 |
| S2 | calibrated co-payment equilibrium | 75.23 | 43.63 | 15.88 | 65.43 |
| S3 | calibrated co-payment equilibrium | 83.05 | 36.65 | 14.56 | 70.52 |
| S4 | price-rationing equity failure | 66.11 | 52.51 | 28.9 | 55.38 |

### G11: KPI salience game
Mechanism: Top-tier KPIs shift behaviour only if paired with funding levers, data and balancing measures.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | hospital-target dominance | 32.91 | 76.72 | 13.03 | 44.62 |
| S1 | hospital-target dominance | 40.94 | 69.79 | 15.46 | 50.41 |
| S2 | upstream target salience with balancing measures | 62.28 | 51.34 | 16.3 | 62.83 |
| S3 | upstream target salience with balancing measures | 78.23 | 35.87 | 13.77 | 74.96 |
| S4 | upstream target salience with balancing measures | 73.5 | 45.68 | 37.06 | 61.52 |

### G12: Equity and trust game
Mechanism: Demand-driven benefits need retained kaupapa Maori, Pacific, rural and locality functions to avoid transactional equity failure.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | benefits plus equity-function equilibrium | 41.25 | 65.25 | 21.0 | 46.19 |
| S1 | benefits plus equity-function equilibrium | 46.97 | 60.24 | 18.74 | 51.82 |
| S2 | benefits plus equity-function equilibrium | 69.1 | 43.95 | 17.25 | 64.7 |
| S3 | benefits plus equity-function equilibrium | 77.88 | 36.12 | 13.8 | 73.86 |
| S4 | transactional-access without trust | 62.96 | 52.97 | 26.38 | 53.28 |

### G13: Political economy game
Mechanism: Reform becomes feasible when framed as patient access and hospital avoidance rather than sector income or anti-PHO politics.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | institutional-defence equilibrium | 39.25 | 69.22 | 16.81 | 47.02 |
| S1 | institutional-defence equilibrium | 45.78 | 65.05 | 17.94 | 52.22 |
| S2 | access-architecture coalition | 64.4 | 60.32 | 24.64 | 60.78 |
| S3 | access-architecture coalition | 74.3 | 46.59 | 18.24 | 71.74 |
| S4 | institutional-defence equilibrium | 59.09 | 78.09 | 61.31 | 43.68 |

### G14: Data observability game
Mechanism: Upstream access failure becomes fundable only when data links it to ambulance, ED and avoidable admission outcomes.

| Scenario | Equilibrium label | Access | Hospital pressure | Gaming risk | Welfare |
|---|---|---:|---:|---:|---:|
| S0 | hidden-unmet-need equilibrium | 26.69 | 88.39 | 41.5 | 34.31 |
| S1 | hidden-unmet-need equilibrium | 32.47 | 76.56 | 34.5 | 42.69 |
| S2 | observable upstream-flow equilibrium | 59.74 | 57.94 | 28.0 | 58.53 |
| S3 | observable upstream-flow equilibrium | 77.17 | 33.97 | 17.5 | 74.99 |
| S4 | hidden-unmet-need equilibrium | 63.66 | 62.92 | 41.5 | 52.01 |

## Sensitivity analysis
A one-at-a-time sensitivity table around S2 is available in `demonstrative-model-sensitivity-v0.6.0.csv`. It varies one key lever for each game by +/-0.20 on the normalised scale and records welfare and hospital-pressure changes.

## Limitations
These models use stylised normalised parameters and transparent formulae. They are intended to demonstrate mechanism plausibility and support stakeholder challenge. They should not be used as forecasts. Empirical calibration requires OIA material, administrative datasets, stakeholder validation and sensitivity analysis.
