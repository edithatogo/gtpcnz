# Parameter tiering v1.7.2

This document hardens the full 70-parameter scaffold by separating parameters into three analytic tiers. The purpose is to prevent the model being read as seventy equally important assumptions.

| Tier | Count | Use |
|---|---:|---|
| Tier 1 — core load-bearing | 21 | Headline sensitivity and early validation |
| Tier 2 — extended policy lever | 34 | Design and policy refinement |
| Tier 3 — exploratory/risk/implementation | 15 | Implementation, political economy and cautionary risk analysis |

## Tier 1 parameters
These are the parameters that should be prioritised for empirical testing, stakeholder validation and sensitivity reporting.
| ID | Name | Domain | Why it matters | Real data needed |
|---|---|---|---|---|
| D01 | base_need_per_1000 | demand | Underlying monthly primary-care-relevant need per 1,000 population before access constraints. | Monthly encounters, unmet need, population denominators |
| D08 | price_elasticity_general | demand/price | How strongly general patients reduce primary care use when co-payments increase. | Practice fees, CSC/VLCA status, utilisation changes |
| D09 | price_elasticity_high_need | demand/equity | How strongly high-need groups reduce or delay care when co-payments increase. | Fees and utilisation by ethnicity/deprivation/rurality/morbidity |
| D11 | unmet_need_persistence | demand dynamics | Persistence of unmet need from one month to the next. | Delayed care, repeat attempts, ED conversion |
| D12 | delay_complexity_growth | demand dynamics | Rate at which delayed care becomes more complex or costly. | Waiting time to ED/admission/acuity |
| S08 | scope_substitution_rate | supply/scope | Proportion of GP-bottlenecked contacts that can be safely shifted to other providers within scope. | Contact type, provider type, safety outcomes |
| S10 | market_entry_response | supply dynamics | Provider/practice entry or expansion response to clear activity-sensitive payment rules. | New practices, new PHOs, direct claim onboarding |
| S11 | local_inperson_constraint | rural/supply | Constraint on local in-person capacity, especially rural or under-served settings. | Rural session availability, travel time, closures |
| F03 | scheduled_medical_benefit_strength | funding/FFS | Strength of uncapped scheduled fee-for-service benefit for eligible primary medical contacts. | Item schedule, contact categories and public contribution |
| F05 | activity_signal_strength | funding/FFS | Marginal revenue signal attached to providing the next clinically necessary contact. | Marginal payment by contact type |
| F07 | copayment_protection_strength | equity/price | Strength of fee caps/subsidies/exemptions for children, high-need and low-income groups. | Eligibility, fees, utilisation by group |
| F08 | acc_activity_strength | ACC/funding | Extent to which ACC activity/contract payments sustain upstream provider capacity. | ACC claims/payments by provider/practice |
| F10 | pho_transaction_cost | PHO/admin | Administrative friction or pass-through opacity from PHO-mediated streams. | PHO financials, pass-through, onboarding delay |
| F12 | place_based_accountability_strength | commissioning | Population/geographic accountability that prevents cherry-picking under demand-led benefits. | Locality responsibility, outreach, hard-to-reach service targets |
| F14 | global_cap_constraint | fiscal | Strength of global cap/fixed envelope on eligible primary medical activity. | Funding envelope, claims cap rules, waiting/rationing outcomes |
| G02 | gaming_controls | governance | Audit, anomaly detection, coding rules and balancing measures. | Claims patterns, outliers, re-presentations |
| G04 | data_observability_primary | data | Visibility of appointment, encounter and outcome data. | NPCD completeness/timeliness |
| H02 | ed_conversion_rate | hospital | Rate at which unmet primary care need converts to ED presentation. | Unmet care/waiting time to ED |
| H05 | ambulance_deflection_rate | ambulance | Effectiveness of funded alternative disposition/hear-and-treat/treat-and-refer pathways. | Non-conveyance safety, re-presentation |
| R01 | cherry_picking_risk | risk | Risk that providers select easy/profitable contacts while hard-to-reach patients remain under-served. | Patient mix, complexity, outreach, non-attenders |
| R03 | fiscal_leakage_risk | risk | Risk that funding leaks to volume or margin without improving access/equity/outcomes. | Public spend, outcomes, claim patterns |

## Interpretation rule

Public outputs should not imply that every parameter is equally important. The headline argument should rest on Tier 1, with Tier 2 and Tier 3 used for scenario design, implementation risk and sensitivity testing.