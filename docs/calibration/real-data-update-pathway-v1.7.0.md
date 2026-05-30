# Real-data update pathway v1.7.0

## Aim

Replace the v1.7.0 prior values with observed parameter estimates while preserving the current model structure.

## Step 1 — Data acquisition

Submit or progress requests for:

- current and proposed capitation formula/rate tables;
- PHO pass-through and non-capitated funding information;
- NPCD appointment and encounter extracts;
- ACC treatment payment and contract data;
- ambulance event/disposition data;
- ED and hospital linkage;
- workforce and open/closed book data;
- fee schedules and patient co-payment information.

## Step 2 — Descriptive baseline

Before calibration, create descriptive baseline tables by region/locality/rurality/deprivation/ethnicity:

- access within 7 days;
- same-day/urgent access;
- primary contact volume by provider type;
- co-payment burden;
- ED presentations and admissions;
- ambulance conveyance and non-conveyance;
- practice open/closed books;
- public and patient cost.

## Step 3 — Estimate transition functions

Estimate these first:

1. marginal supply response to activity-sensitive payment;
2. price response to co-payments;
3. unmet need to ED/hospital conversion;
4. ambulance alternative-disposition effect;
5. ACC activity funding stabilisation effect;
6. scope-enabled provider supply and safety;
7. place accountability/cherry-picking protection.

## Step 4 — Validate

Validation should include:

- temporal validation;
- geographic validation;
- equity validation;
- policy-shock validation;
- stakeholder face-validity review;
- sensitivity analysis.

## Step 5 — Update MCDA

Only after the empirical parameter update should the model outputs be used as quantitative inputs to the MCDA layer.

## Stop rule

Do not call the model predictive unless it reproduces baseline patterns and predicts held-out data within pre-specified tolerances.
