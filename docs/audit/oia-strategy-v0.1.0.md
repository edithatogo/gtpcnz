# OIA and Data Governance Strategy

## 1. Audience and Purpose
This strategy outlines the data acquisition and governance pathway required to transition the **Primary Care Funding Architecture Model** from a parameterised scaffold to an empirically informed simulation. The primary audience includes the project research team, legal advisors, and potential data custodians (Ministry of Health, Health NZ, ACC).

## 2. Evidence Gaps & OIA Targets

Based on the v1.7.2 parameter inventory, the following Tier 1 (load-bearing) gaps are prioritised for OIA requests:

### A. Capitation & Reweighting (Ministry of Health / Health NZ)
- **Gap:** Exact weights and "adjusters" used in the 2024/25 capitation formula reweighting.
- **OIA Target:** Technical specifications for the capitation formula, including age/sex/deprivation/morbidity weights and impact assessments on practice-level revenue.
- **Parameters Addressed:** F02 (Capitation weighting adequacy), F01 (Capitation base strength).

### B. National Primary Care Dataset (NPCD) Schema
- **Gap:** Data definitions and "observability" of real-time encounters.
- **OIA Target:** Current NPCD data dictionary, reporting compliance rates by PHO, and any internal evaluation of data completeness for "unmet need" identification.
- **Parameters Addressed:** G04 (Data observability primary), D01 (Base need per 1000).

### C. ACC Activity & Scope (ACC)
- **Gap:** Granular FFS payments by provider type and item.
- **OIA Target:** Last 24 months of payment data for injury-related primary care, stratified by item code and provider scope (GP vs. Nurse/NP).
- **Parameters Addressed:** F08 (ACC activity strength), S08 (Scope substitution rate).

### D. Ambulance Dispositions (St John / Wellington Free Ambulance)
- **Gap:** Rates of "Treat and Refer" vs. "Conveyance to ED."
- **OIA Target:** Regional data on alternative disposition success rates and re-presentation risk within 48 hours.
- **Parameters Addressed:** H04 (Ambulance conveyance default), H05 (Ambulance deflection rate).

## 3. Data Governance Dashboard

A formal log will be maintained in `docs/audit/oia-request-tracker.csv` to ensure traceability and compliance with the Official Information Act 1982.

---
_v0.1.0 - Drafted for Conductor Track 006_
