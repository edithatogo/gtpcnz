# Parameterisation data contract v1.7.0

This document defines what is now required to convert the v1.7.0 full parameterisation scaffold into a real-data calibrated model.

## Status

The model now has explicit parameters, bounds and scenario values. The values are still priors/placeholders. Real data must replace them before predictive claims can be made.

## Data domains required

1. **Primary care appointments and encounters** — waiting times, mode, urgency, provider type, contact type and outcome.
2. **Capitation and PHO payment flows** — current and proposed capitation rates, top-ups, pass-through and non-capitated PHO streams.
3. **Co-payments and fees** — practice fee schedules, concessions, CSC/VLCA status, patient payments and fee caps.
4. **ACC claims and payments** — Cost of Treatment Regulation payments, contract payments and provider/practice payment flows.
5. **Ambulance events** — acuity, response, disposition, conveyance, alternative pathways, handover delay and funding source.
6. **Emergency department and hospital data** — ED presentations, triage, diagnosis, disposition, admissions, length of stay and cost weights.
7. **Workforce and scope data** — provider type, FTE, scope, prescribing authority, sessions and vacancies.
8. **Practice market data** — open/closed books, entry/exit, ownership, new market entrants and rural/local supply.
9. **Equity and consumer data** — ethnicity, deprivation, rurality, multimorbidity, unmet need, trust and patient-reported access.
10. **Budget and policy-flow data** — appropriations, transfers, initiatives, baseline pressure and service-class spending.

The detailed contract is in `data-input-contract-v1.7.0.csv`.

## Minimum viable empirical update

The first empirical update does not need every table. A minimum viable calibration would use:

- appointment/encounter data;
- co-payment/fee sample;
- ED and admission linkage;
- ambulance conveyance data;
- practice/provider workforce and open-book data;
- capitation/payment-rate tables;
- ACC treatment-payment aggregates.

## Interpretation rule

Until these data are available, the v1.7.0 model should be described as:

> a fully specified parameterisation scaffold, not an empirically calibrated predictive model.
