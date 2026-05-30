# Uncertainty analysis and calibration-readiness report v0.7.0

## Status

This is an **uncertainty stress test of the demonstrative game models**, not an empirical calibration. It tests whether the v0.6.0 modelling artefacts are interrogable, which assumptions drive the results, and where empirical data are most urgently needed.

The analysis perturbs every scenario lever around its v0.6.0 demonstrative value, using clipped normal draws on a 0-1 scale. For each draw, the 14 mapped New Zealand policy games are run under five scenarios. This release uses 1,000 draws per scenario, generating 70,000 game-level outcome rows.

## Scenarios tested

- **S0 Status quo tight control**: dominant capitation/contracting, PHO intermediation, weak marginal contact benefit and high hospital salience.
- **S1 Capitation reweighting only**: better distribution within capitation but no material demand-driven benefit stream.
- **S2 Primary Care Benefits Schedule**: contact-type benefits, direct/optional claiming and broader provider eligibility with moderate safeguards.
- **S3 Full upstream access architecture**: benefits schedule plus strong KPIs, observability, ambulance alternatives, equity protections and governance.
- **S4 Loose benefits, weak controls**: broad demand-driven benefits with weak governance, weak equity protections, weak data and high gaming risk.

## Scenario summary

| scenario_id   | scenario_name                     |   access_score_mean |   hospital_pressure_mean |   gaming_risk_mean |   system_welfare_mean |   system_welfare_p05 |   system_welfare_p95 |
|:--------------|:----------------------------------|--------------------:|-------------------------:|-------------------:|----------------------:|---------------------:|---------------------:|
| S0            | Status quo tight control          |               32.52 |                    77.83 |              21.6  |                 41.05 |                30.64 |                51.61 |
| S1            | Capitation reweighting only       |               38.25 |                    72.04 |              20.41 |                 46.33 |                35.81 |                56.28 |
| S2            | Primary Care Benefits Schedule    |               63.21 |                    52.24 |              20.39 |                 60.16 |                52.22 |                69.59 |
| S3            | Full upstream access architecture |               74.85 |                    39.39 |              16.12 |                 70.17 |                62.63 |                77.34 |
| S4            | Loose benefits, weak controls     |               65.65 |                    53.77 |              35.23 |                 53.76 |                44.34 |                66.63 |

## Pairwise comparison with S0

These are **demonstrative uncertainty proportions**, not real-world probabilities.

| scenario_id   | scenario_name                     |   p_welfare_gt_s0 |   p_hospital_pressure_lt_s0 |   p_access_gt_s0 |   p_gaming_risk_lt_s0 | comparison_status                                         |
|:--------------|:----------------------------------|------------------:|----------------------------:|-----------------:|----------------------:|:----------------------------------------------------------|
| S1            | Capitation reweighting only       |                 1 |                       0.998 |            0.989 |                 0.832 | demonstrative uncertainty only; not empirical probability |
| S2            | Primary Care Benefits Schedule    |                 1 |                       1     |            1     |                 0.792 | demonstrative uncertainty only; not empirical probability |
| S3            | Full upstream access architecture |                 1 |                       1     |            1     |                 0.999 | demonstrative uncertainty only; not empirical probability |
| S4            | Loose benefits, weak controls     |                 1 |                       1     |            1     |                 0     | demonstrative uncertainty only; not empirical probability |

## Top welfare sensitivity drivers across games

| parameter                     |   abs_correlation |
|:------------------------------|------------------:|
| local_inperson_loading        |             0.893 |
| direct_claiming               |             0.89  |
| narrative_coherence           |             0.885 |
| marginal_contact_benefit      |             0.877 |
| data_observability            |             0.875 |
| primary_kpi_salience          |             0.874 |
| pho_transaction_cost          |             0.856 |
| ambulance_alternative_funding |             0.856 |
| ambulance_kpi_salience        |             0.856 |
| stakeholder_alignment         |             0.853 |

## Interpretation

The stress test preserves the main v0.6.0 result: capitation reweighting improves the model only modestly; a Primary Care Benefits Schedule improves access and hospital-pressure logic; and the full upstream architecture performs best because it adds data, KPIs, co-payment protections, scope governance, ambulance alternatives and local in-person support.

The weak-control scenario is important. It shows that demand-driven benefits can improve access while increasing gaming risk and weakening equity. This supports the central policy phrase:

> **Demand-driven within rules; not demand-driven without rules.**

## What the sensitivity results imply

The top drivers are not yet empirical findings. They are a prioritisation device. They identify where real-world estimation matters first:

1. **local_inperson_loading**: rural and local in-person capacity support;
2. **direct_claiming**: whether eligible providers can claim directly through a national platform;
3. **narrative_coherence**: political economy and stakeholder framing;
4. **marginal_contact_benefit**: strength of contact-type payment;
5. **data_observability**: linked visibility of primary care, ambulance, ED and hospital pathways;
6. **primary_kpi_salience**: whether upstream access is elevated to hospital-equivalent accountability;
7. **pho_transaction_cost**: intermediation friction and market-entry barriers;
8. **ambulance_alternative_funding**: funding for non-conveyance and alternative care pathways;
9. **ambulance_kpi_salience**: visibility of ambulance outcomes as access infrastructure;
10. **stakeholder_alignment**: coalition feasibility.

## Minimum empirical validation needed

The next stage should estimate, or at least bound, the parameters above using:

- current and proposed capitation formulas and rate tables;
- National Enrolment Service and National Primary Care Dataset data;
- practice fee/co-payment data;
- PHO financial-flow and pass-through information;
- ACC claims and payment mix by provider/practice type;
- ambulance response, disposition and ED interface data;
- ED, ambulatory-sensitive and potentially preventable hospitalisation data;
- workforce data by profession, scope and geography;
- stakeholder validation with providers, PHOs, Māori/Pacific providers, ACC, Health NZ, Treasury and ambulance organisations.

## Calibration standard

The model should not be presented as predictive until it passes:

1. parameter provenance review;
2. face-validity review with sector experts;
3. calibration to observed access, utilisation and hospital-pressure data;
4. external validation against data not used for calibration;
5. equity validation by ethnicity, deprivation, rurality, age and multimorbidity;
6. sensitivity/falsification testing;
7. transparent reporting using STRESS for simulation and ODD for agent-based components.

## Bottom line

The v0.7.0 result is not “the model proves the policy”. It is:

> **The demonstrative game map is now testable. The uncertainty layer shows which assumptions matter most and defines the empirical work needed before making predictive or fiscal claims.**
