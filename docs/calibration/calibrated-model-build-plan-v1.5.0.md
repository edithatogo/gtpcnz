# Calibrated model build plan v1.5.0

This release starts the calibrated-model pathway without claiming calibration has been achieved. The current code provides a working starter pipeline: schema, synthetic observations, a simple dynamic model, least-squares fitting, parameter recovery plots and scenario comparison.

## What has started

1. Minimal dynamic equations for primary contacts, unmet need, emergency department presentations, ambulance conveyance and public cost.
2. A calibration objective comparing model outputs with observed monthly data.
3. A deterministic grid/coordinate search routine that can be replaced by Bayesian calibration or simulated method of moments.
4. Synthetic-data tests to show the pipeline runs before confidential linked NZ data are available.

## What is still needed before claiming empirical calibration

- National Primary Care Dataset appointment and encounter data.
- National Enrolment Service population and practice data.
- Capitation/payment formula and rate tables.
- Accident Compensation Corporation claim/payment data.
- Ambulance event, disposition and handover data.
- Emergency department and inpatient data linked to patient and locality.
- Workforce, provider-scope and practice capacity data.
- Co-payment and patient fee data.
- Māori, Pacific, rural and deprivation-stratified validation.
