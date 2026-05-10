# Full parameterised model build report v1.7.0

## Status

This release continues the fully parameterised model build. It does **not** claim to be a real-data calibrated predictive model. It now provides a complete parameterisation scaffold: every major modelling mechanism has an explicit parameter, bounds, source status, real-data requirement and estimation strategy.

## What changed

- Expanded the parameter register from the earlier compact source-informed layer to **70 explicit parameters** across demand, supply, funding, governance, ambulance, hospital, equity, risk and implementation domains.
- Added a **data-input contract** with **12 required input tables** for future empirical calibration.
- Added **10 policy scenarios**, including current reform, uncapped scheduled medical fee-for-service, controlled full hybrid architecture, weak-control uncapping, ACC constraint shock, urgent/ambulance-only, scope-only and place-only scenarios.
- Added a 60-month dynamic simulation linking supply generation, access, unmet need, ambulance conveyance, emergency department events, admissions, hospital pressure and public cost.
- Added one-at-a-time sensitivity analysis and a calibration-target matrix.

## Scenario results

|   rank_by_hybrid_viability | scenario_id   | scenario_name                               |   hybrid_viability_score |   access_score |   supply_generation_score |   hospital_pressure_score |   fiscal_risk_score |   gaming_risk_score |   mean_last12_primary_contacts_per_1000 |   mean_last12_ed_events_per_100k |   mean_last12_public_cost_index |
|---------------------------:|:--------------|:--------------------------------------------|-------------------------:|---------------:|--------------------------:|--------------------------:|--------------------:|--------------------:|----------------------------------------:|---------------------------------:|--------------------------------:|
|                          1 | F4            | Full hybrid upstream architecture           |                    77.26 |          52.75 |                     55.66 |                     61.61 |               37.94 |               27.3  |                                   42.7  |                            58    |                            2.46 |
|                          2 | F3            | Uncapped medical FFS + place accountability |                    62.51 |          38.62 |                     40.1  |                     74.36 |               44.45 |               30.76 |                                   29.03 |                            66.07 |                            2.72 |
|                          3 | F2            | Uncapped scheduled medical FFS              |                    56.4  |          36.44 |                     40.38 |                     75.86 |               49.23 |               39.1  |                                   27.08 |                            71.9  |                            2.91 |
|                          4 | F9            | Place-based commissioning only              |                    54.26 |          22.11 |                     14.33 |                     79.07 |               27.09 |               30.35 |                                   11.89 |                            77.9  |                            3.09 |
|                          5 | F8            | Scope-enabled supply only                   |                    52.96 |          25.94 |                     21.29 |                     78.25 |               30.18 |               36.22 |                                   15.82 |                            79.53 |                            3.14 |
|                          6 | F7            | Ambulance and urgent alternatives only      |                    52.74 |          26.87 |                     14.33 |                     72.31 |               26.57 |               35.75 |                                   14.92 |                            74.96 |                            2.95 |
|                          7 | F0            | Current reform pathway                      |                    52.24 |          23.56 |                     15.43 |                     78.07 |               27.85 |               34.04 |                                   13.04 |                            79.71 |                            3.15 |
|                          8 | F1            | Capitation reweighting only                 |                    50.37 |          22    |                     14.11 |                     79.91 |               27.47 |               35.45 |                                   11.77 |                            81.77 |                            3.22 |
|                          9 | F6            | ACC activity constraint shock               |                    50.11 |          21.86 |                     13.87 |                     80.21 |               26.67 |               35.35 |                                   11.23 |                            82.26 |                            3.23 |
|                         10 | F5            | Uncapped weak-control model                 |                    46.11 |          33.47 |                     37.25 |                     77.18 |               65.29 |               70.64 |                                   24.06 |                            75.19 |                            3.03 |

## Interpretation

The full hybrid upstream architecture continues to rank highest in this parameterised scaffold. The model distinguishes this from an uncontrolled uncapped model. The weak-control scenario improves the marginal activity signal but scores poorly on gaming, fiscal leakage and place/equity safeguards.

The result should be read as a structured modelling hypothesis, not as a forecast. The model is ready to accept real data, but the values remain priors/placeholders until linked data and stakeholder validation are available.

## Top sensitivity drivers

| parameter                           | domain            |   abs_viability_change |
|:------------------------------------|:------------------|-----------------------:|
| copayment_protection_strength       | equity/price      |               0.540534 |
| data_observability_primary          | data              |               0.432265 |
| safety_governance                   | governance        |               0.431665 |
| item_rules_strength                 | fiscal/governance |               0.353188 |
| cherry_picking_risk                 | risk              |               0.335232 |
| stakeholder_alignment               | political economy |               0.32     |
| equity_program_strength             | equity            |               0.316256 |
| local_inperson_constraint           | rural/supply      |               0.314286 |
| fiscal_leakage_risk                 | risk              |               0.287232 |
| rural_loading_response              | rural/supply      |               0.269388 |
| gaming_controls                     | governance        |               0.267141 |
| implementation_complexity           | implementation    |               0.2528   |
| place_based_accountability_strength | commissioning     |               0.246701 |
| patient_copayment_level             | funding/price     |               0.24426  |
| market_entry_response               | supply dynamics   |               0.22449  |

## Output tables

- `full-parameter-register-v1.7.0.csv`
- `data-input-contract-v1.7.0.csv`
- `scenario-parameter-matrix-v1.7.0.csv`
- `full-parameterised-monthly-results-v1.7.0.csv`
- `full-parameterised-summary-results-v1.7.0.csv`
- `full-parameterised-sensitivity-v1.7.0.csv`
- `calibration-target-matrix-v1.7.0.csv`

## Figures

- `outputs/figures/full-parameterised-scenario-viability-pressure-v1.7.0.png`
- `outputs/figures/full-parameterised-hospital-pressure-trajectories-v1.7.0.png`
- `outputs/figures/full-parameterised-access-vs-fiscal-risk-v1.7.0.png`
- `outputs/figures/full-parameterised-top-sensitivity-drivers-v1.7.0.png`
- `outputs/figures/full-parameterised-parameter-domain-coverage-v1.7.0.png`

## What this enables next

1. Replace placeholder priors with actual values from capitation, PHO, ACC, ambulance, NPCD, ED, hospital and workforce data.
2. Fit the transition parameters for marginal supply, price response, unmet-need conversion, ambulance deflection and ACC stabilisation.
3. Use temporal and geographic validation before making any predictive claims.
4. Feed the updated scenario outputs into the existing MCDA layer.

## Caveat

This is a fully specified parameterisation framework, not a completed empirical calibration. It makes the model auditable and data-ready, but does not yet estimate real-world effect sizes.
