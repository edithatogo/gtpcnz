# Parameterised model run report v1.0.0

**Project:** Primary care funding architecture in Aotearoa New Zealand and Australia  
**Status:** source-informed demonstrative parameterisation; not an empirically calibrated predictive model  
**Date:** 2026-05-08

## 1. What changed in this version

This version identifies the model parameters, links them to public-source inputs where available, updates the scenario inputs, reruns the game models, hybrid model, uncertainty layer and hybrid-informed MCDA, and generates plots/tables for review.

The core modelling status remains deliberately cautious: this is a source-informed demonstrative run. It improves the audit trail from v0.9.0, but it does not replace formal calibration using administrative datasets, OIA material, provider-level payment flows, ambulance disposition data, ED/hospital linkage, workforce data and stakeholder validation.

## 2. Public inputs used

The main empirical anchors used in the parameterisation are:

- NZ capitation funding was introduced in 2002, remains the core way general practice is funded, and the proposed reweighting considers age, sex, multimorbidity, rurality and socio-economic deprivation.
- A new primary care access target is proposed to take effect from 1 July 2026: more than 80% of people can access an appointment with a general practice provider within one week.
- The National Primary Care Dataset begins with general practice appointment and encounter data, including when appointments were booked, when people were seen and the outcome of appointments.
- The 2024/25 NZ Health Survey reports that 25.5% of adults experienced appointment wait time as a barrier to GP care, 14.9% did not visit a GP because of cost, and 17.1% visited an ED in the prior 12 months.
- The closed-books survey reported that only 28% of respondent general practices were freely enrolling new people in 2022, and 79% had closed or limited enrolments at some point since 2019.
- Health NZ commissions ambulance services on behalf of Health NZ and ACC, and ambulance providers report response time KPIs, demand, quality and call-type information.
- ACC pays providers through regulations, contracts or purchase orders and contributes to consultation/procedure costs for GPs, nurses and nurse practitioners in relevant injury-related care.

## 3. Parameter register

A full parameter-input register is included in the workbook and CSV artefacts. Key parameters include marginal contact benefit, capitation weighting, scope flexibility, PHO transaction cost, primary and ambulance KPI salience, data observability, co-payment level/protection, equity programme strength, ambulance alternative funding, ACC activity funding, budget tightness, safety governance, gaming controls and direct claiming.

The normalised values are not claimed to be natural units. They are documented priors for model exploration. Each parameter has a source, transformation rule, confidence rating and next data requirement.

## 4. Updated scenarios

The run now compares nine scenarios:

| scenario_id   | name                                             | description                                                                                                                                              |
|:--------------|:-------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| P0            | Current source-informed baseline                 | Current/public input baseline: capitation-centred, PHO-mediated, partial ACC/activity funding, imminent primary care target and developing NPCD.         |
| P1            | Capitation reweighting plus access target        | Reweight capitation and implement the access target/NPCD, but do not introduce a demand-driven contact benefit stream.                                   |
| P2            | National Primary Care Benefits Schedule          | Defined primary/urgent/ambulance contact benefits, direct claiming, broader provider eligibility and moderate controls layered onto capitation.          |
| P3            | Full upstream access architecture                | Benefits schedule plus top-tier primary/ambulance KPIs, strong data, rural/in-person loading, equity protections, governance and ambulance alternatives. |
| P4            | Benefits without adequate controls               | Demand-driven benefits with broad eligibility but weak controls, weak equity protection and weak integration.                                            |
| P5            | ACC activity constraint shock                    | Narrow cost-containment move that constrains ACC activity funding without compensating primary care supply architecture.                                 |
| P6            | Ambulance alternatives only                      | Strengthen ambulance alternative disposition pathways and KPIs while leaving most primary care funding architecture unchanged.                           |
| P7            | Scope-enabled provider supply only               | Broaden provider eligibility and clinical governance without a full demand-driven benefit stream or full accountability reset.                           |
| P8            | Direct claims and PHO intermediation reform only | Reduce PHO payment-gateway friction and add direct claims, but do not materially increase eligible contact benefits.                                     |

## 5. Hybrid model results

| scenario_id   | scenario_name                                    |   hybrid_viability_score |   supply_generation_index |   hospital_deflection_index |   weighted_hospital_pressure |   fiscal_gaming_risk_index |   interaction_penalty |
|:--------------|:-------------------------------------------------|-------------------------:|--------------------------:|----------------------------:|-----------------------------:|---------------------------:|----------------------:|
| P0            | Current source-informed baseline                 |                    24.97 |                     20.4  |                       31.2  |                        72.04 |                      14.27 |                 14.06 |
| P1            | Capitation reweighting plus access target        |                    32.05 |                     22.1  |                       35.8  |                        68.64 |                      12.9  |                 11.81 |
| P2            | National Primary Care Benefits Schedule          |                    54    |                     60.04 |                       52.62 |                        48.24 |                      16.6  |                  5.88 |
| P3            | Full upstream access architecture                |                    67.36 |                     70    |                       66.62 |                        37.22 |                      10.84 |                  3.09 |
| P4            | Benefits without adequate controls               |                    34.61 |                     64.32 |                       52.6  |                        51.5  |                      41.82 |                 15.15 |
| P5            | ACC activity constraint shock                    |                    23.71 |                     18.84 |                       29.1  |                        73.96 |                      14.13 |                 14.16 |
| P6            | Ambulance alternatives only                      |                    33.03 |                     21.86 |                       44.22 |                        66.2  |                      12.46 |                 12.79 |
| P7            | Scope-enabled provider supply only               |                    38.34 |                     40.8  |                       39.93 |                        60.58 |                      16.45 |                 10.83 |
| P8            | Direct claims and PHO intermediation reform only |                    34.56 |                     34.45 |                       35.51 |                        66.53 |                      16.34 |                 11.21 |

The result is consistent with the previous architecture hypothesis. Capitation reweighting plus an access target improves the source-informed baseline, but remains weaker than a benefits schedule or full upstream access architecture on supply generation and hospital deflection. The full upstream architecture performs best. A loose benefits model improves access but is penalised by gaming, fiscal and governance risk.

## 6. Hybrid-informed MCDA

|   rank | scenario_id   | scenario_name                                    |   weighted_score_before_penalty |   risk_penalty |   risk_adjusted_mcda_score |
|-------:|:--------------|:-------------------------------------------------|--------------------------------:|---------------:|---------------------------:|
|      1 | P3            | Full upstream access architecture                |                           77.34 |           2.04 |                      75.3  |
|      2 | P2            | National Primary Care Benefits Schedule          |                           66.79 |           3.24 |                      63.54 |
|      3 | P8            | Direct claims and PHO intermediation reform only |                           55.96 |           3.74 |                      52.22 |
|      4 | P7            | Scope-enabled provider supply only               |                           55.76 |           3.71 |                      52.05 |
|      5 | P6            | Ambulance alternatives only                      |                           54.06 |           3.27 |                      50.78 |
|      6 | P1            | Capitation reweighting plus access target        |                           52.11 |           3.25 |                      48.86 |
|      7 | P4            | Benefits without adequate controls               |                           53.96 |           8.21 |                      45.75 |
|      8 | P0            | Current source-informed baseline                 |                           47.75 |           3.69 |                      44.06 |
|      9 | P5            | ACC activity constraint shock                    |                           46.96 |           3.68 |                      43.28 |

The MCDA is derived from the hybrid outputs and scenario parameters. It is not a separate empirical proof; it is a decision-support translation of the model. The highest-ranked option remains the full upstream access architecture, followed by the National Primary Care Benefits Schedule.

## 7. Uncertainty summary

| scenario_id   | scenario_name                                    |   hybrid_viability_score_mean |   hybrid_viability_score_p05 |   hybrid_viability_score_p95 |   weighted_hospital_pressure_mean |   weighted_hospital_pressure_p05 |   weighted_hospital_pressure_p95 |
|:--------------|:-------------------------------------------------|------------------------------:|-----------------------------:|-----------------------------:|----------------------------------:|---------------------------------:|---------------------------------:|
| P0            | Current source-informed baseline                 |                         24.96 |                        21.92 |                        27.91 |                             72.03 |                            69.86 |                            74.17 |
| P1            | Capitation reweighting plus access target        |                         32.17 |                        29.24 |                        34.9  |                             68.48 |                            66.05 |                            70.82 |
| P2            | National Primary Care Benefits Schedule          |                         53.75 |                        51.02 |                        56.47 |                             48.31 |                            45.67 |                            50.74 |
| P3            | Full upstream access architecture                |                         67.26 |                        64.86 |                        69.57 |                             37.29 |                            34.84 |                            39.74 |
| P4            | Benefits without adequate controls               |                         34.57 |                        31.27 |                        37.87 |                             51.61 |                            49.19 |                            54.08 |
| P5            | ACC activity constraint shock                    |                         23.74 |                        20.7  |                        26.91 |                             73.86 |                            71.56 |                            75.99 |
| P6            | Ambulance alternatives only                      |                         33.17 |                        30.34 |                        36.21 |                             66.03 |                            63.67 |                            68.27 |
| P7            | Scope-enabled provider supply only               |                         38.26 |                        35.16 |                        41.57 |                             60.51 |                            57.55 |                            63.3  |
| P8            | Direct claims and PHO intermediation reform only |                         34.5  |                        31.18 |                        37.58 |                             66.5  |                            63.88 |                            69.19 |

The uncertainty layer perturbs all scenario levers around the source-informed values. It is still demonstrative, but it shows that the full upstream architecture remains the strongest scenario under the assumed parameter ranges.

## 8. Key sensitivity drivers

The pooled sensitivity run indicates the strongest drivers of hybrid viability are:

| parameter                |   correlation |   abs_correlation |
|:-------------------------|--------------:|------------------:|
| local_inperson_loading   |         0.887 |             0.887 |
| narrative_coherence      |         0.88  |             0.88  |
| data_observability       |         0.824 |             0.824 |
| stakeholder_alignment    |         0.824 |             0.824 |
| budget_tightness         |        -0.813 |             0.813 |
| telehealth_integration   |         0.781 |             0.781 |
| primary_kpi_salience     |         0.772 |             0.772 |
| copayment_protections    |         0.772 |             0.772 |
| copayment_level          |        -0.725 |             0.725 |
| marginal_contact_benefit |         0.724 |             0.724 |
| capitation_weighting     |         0.667 |             0.667 |
| direct_claiming          |         0.661 |             0.661 |

These should be prioritised for data collection and stakeholder validation.

## 9. Interpretation

The parameterised model supports the same cautious conclusion as the earlier demonstrative model:

> Demand-driven within rules; not demand-driven without rules.

The modelling implication is that New Zealand's policy question should not be framed as capitation versus fee-for-service. It is whether the system can define eligible contact types, allow accredited providers to generate activity within scope, calibrate co-payments with equity protections, preserve locality/equity functions, fund ambulance alternatives, and lift primary care/ambulance KPIs to hospital-equivalent salience.

## 10. Limitations

This run is not empirically calibrated. Key values remain source-informed priors or explicit modelling judgements. The results should be used to guide further empirical work, not as final estimates of fiscal impact, hospital deflection or workforce response.

## 11. Priority next data inputs

1. Full current capitation formula, rate tables and implementation workbook.
2. Provider-level payment flows: capitation, co-payments, ACC, programme funding and PHO pass-through.
3. Appointment availability, booked-to-seen interval and closed-books data from NPCD.
4. Ambulance disposition data, non-conveyance outcomes, offload delay and alternative pathway funding.
5. ED and ambulatory-sensitive hospitalisation linkage to primary care access indicators.
6. Workforce counts, provider scope utilisation and productivity by provider type.
7. Practice fee schedules and patient-level co-payment exposure.
8. Stakeholder MCDA scoring by PHOs, practices, kaupapa Māori/Pacific providers, rural providers, ambulance, Health NZ, ACC, Treasury and consumers.

## 12. Source notes

Full source details are included in `parameter-input-register-v1.0.0.csv`. This report keeps URLs in the register to preserve reproducibility.
