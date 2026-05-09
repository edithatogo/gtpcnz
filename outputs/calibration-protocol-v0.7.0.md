# Calibration protocol v0.7.0

## Purpose

This protocol defines how the v0.6.0 demonstrative game models and v0.7.0 uncertainty layer should be converted into calibrated empirical models.

The aim is not to prove a predetermined policy solution. The aim is to test whether New Zealand's current primary care, ambulance and hospital funding architecture creates a repeated-game equilibrium in which constrained upstream supply is translated into higher downstream hospital pressure.

## Calibration question

> Does a contact-type, demand-responsive primary care and ambulance benefits architecture produce better access, lower hospital pressure and acceptable fiscal/equity/safety outcomes compared with capitation reweighting alone?

## Core policy scenarios

1. **S0 Status quo tight control**: existing capitation/contracting/payment intermediation architecture.
2. **S1 Capitation reweighting only**: improved allocation within capitation without material marginal activity benefit.
3. **S2 Primary Care Benefits Schedule**: defined contact-type subsidies claimable by accredited providers within scope.
4. **S3 Full upstream access architecture**: S2 plus primary/ambulance KPIs, local in-person loading, equity protections, observability and governance.
5. **S4 Loose benefits, weak controls**: deliberately unsafe comparator to test fiscal, gaming and equity risks.

## Parameters requiring empirical calibration

The current parameter register is:

- `docs/modelling/parameter-prior-register-v0.7.0.csv`

Critical parameters to prioritise are:

1. `marginal_contact_benefit`
2. `data_observability`
3. `scope_flexibility`
4. `safety_governance`
5. `gaming_controls`
6. `copayment_level`
7. `copayment_protections`
8. `equity_program_strength`
9. `pho_transaction_cost`
10. `direct_claiming`
11. `local_inperson_loading`
12. `ambulance_alternative_funding`
13. `primary_kpi_salience`
14. `ambulance_kpi_salience`
15. `acc_activity_funding`

## Empirical data streams

| Data stream | Purpose | Likely variables |
|---|---|---|
| Capitation formula/rate tables | Estimate baseline funding and reweighting effects | age, sex, deprivation, rurality, multimorbidity, ethnicity, payment rates |
| National Enrolment Service | Define enrolled population and enrolment barriers | enrolment status, practice, NHI demographics, transfer patterns |
| National Primary Care Dataset | Calibrate access/contact volumes | appointment bookings, encounter dates, provider type, access target fields |
| Practice fee/co-payment data | Estimate demand signal and access barriers | published fees, CSC/VLCA/age concessions, unmet need due to cost |
| PHO financial and pass-through data | Estimate intermediation and transaction cost | administrative overhead, payment delays, programme funding, retained funds |
| ACC claims and payment data | Test ACC stabilisation hypothesis | claims, payments, provider/practice type, injury episode volumes |
| Ambulance data | Model prehospital access and alternatives | response, dispatch category, treat-and-refer, non-conveyance, ED handover |
| ED/hospital data | Calibrate downstream pressure | ED attendance, lower-urgency presentations, ASH/PPH admissions, cost |
| Workforce data | Calibrate supply elasticity | GP, NP, nurse, pharmacist, allied health, paramedic numbers and geography |
| Qualitative stakeholder data | Validate mechanisms | practice entry, closed books, scope bottlenecks, PHO value/friction |

## Model conversion stages

### Stage 1: Parameter provenance

For each model parameter:

1. define the policy meaning;
2. identify available data source(s);
3. assign an empirical unit;
4. estimate a prior range;
5. document whether it is data-derived, expert-elicited or still assumed.

### Stage 2: Outcome calibration

Calibrate against observed outputs:

- primary care appointment availability;
- contact volumes by provider type;
- practice enrolment/open-book status;
- patient co-payment burden;
- ambulance conveyance and alternative-disposition rates;
- ED presentations;
- ambulatory-sensitive/potentially preventable hospitalisations;
- provider viability and workforce retention proxies.

### Stage 3: Mechanism validation

For each game, confirm that the causal mechanism is plausible:

- **G1/G2**: hospital pressure crowds out upstream investment;
- **G3**: weak marginal payment constrains appointment supply;
- **G5**: PHO intermediation adds value and/or friction;
- **G6**: ACC activity funding contributes to primary care viability;
- **G7**: ambulance default conveyance changes when alternatives are funded;
- **G8**: scope-enabled claiming expands safe supply;
- **G10**: co-payment affects access and delayed care;
- **G11/G14**: observability and KPI salience alter budget behaviour.

### Stage 4: Calibration method

Use a staged approach:

1. deterministic calibration to match aggregate observed utilisation;
2. probabilistic calibration using priors for uncertain parameters;
3. approximate Bayesian computation or likelihood-free calibration if formal likelihood is impractical;
4. cross-validation by region, rurality and deprivation;
5. external validation using held-out data periods.

### Stage 5: Equity and Te Tiriti validation

The model must report all key outcomes by:

- Māori/non-Māori;
- Pacific/non-Pacific;
- deprivation quintile;
- rurality;
- age group;
- multimorbidity;
- disability where data permit.

The model should not treat equity functions as optional transaction costs. Kaupapa Māori, Pacific, locality, outreach and trust functions should be represented separately from payment intermediation.

### Stage 6: Falsification tests

The hypothesis should be weakened or rejected if:

- constrained upstream access does not correlate with hospital pressure after adjustment;
- marginal contact payments do not materially change supply in comparable settings;
- PHO intermediation does not measurably affect transaction cost, entry or pass-through;
- ACC activity payments do not affect primary care viability or marginal capacity;
- scope-enabled claiming worsens safety or equity beyond acceptable controls;
- co-payment settings produce unacceptable delayed care or inequity;
- the full upstream architecture fails to outperform capitation reweighting alone under plausible parameter ranges.

## Reporting standards

- Use STRESS for simulation reporting.
- Use ODD for agent-based model description.
- Use PRISMA-ScR for the evidence map.
- Use CHEERS 2022 if formal economic evaluation is undertaken.

## Minimum viable empirical model

A minimum viable calibrated model should include:

1. population strata by age, deprivation, ethnicity, rurality and multimorbidity;
2. provider supply by profession and geography;
3. capitation and contact-payment inputs;
4. co-payment settings;
5. patient pathway choice among primary care, telehealth, ambulance, ED and delayed care;
6. ambulance conveyance/non-conveyance pathway;
7. hospital-pressure outcomes;
8. equity outputs;
9. fiscal outputs;
10. uncertainty and sensitivity analysis.

## Decision rule for policy briefs

Policy claims should be tiered:

- **Can say now**: the current hypothesis is structured, traceable, executable and falsifiable.
- **Can say after calibration**: the model estimates relative impacts under specified assumptions.
- **Can say only after validation**: the policy option is likely to improve access or reduce hospital pressure in real-world implementation.
