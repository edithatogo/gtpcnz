# Calibration readiness

GTPCNZ is currently a source-informed parameterised scaffold. The next stage would require real data and validation.

## Data needed

| Domain | Data needed | Why it matters |
|---|---|---|
| Primary care appointments | Booking, encounter, provider type, mode and outcome | Access and waiting-time calibration |
| Capitation and payment rules | Rate tables, pass-through, programme funding | Revenue and marginal-supply calibration |
| Co-payments | Practice fee schedules and patient out-of-pocket costs | Demand and equity effects |
| Ambulance pathways | Conveyance, hear-and-treat, treat-and-refer, handover delay | Hospital deflection |
| Accident Compensation Corporation | Treatment claims, contracts, Cost of Treatment Regulations | Cross-funder supply effects |
| Emergency department and inpatient data | ED presentations, admissions, diagnosis and disposition | Downstream hospital pressure |
| Workforce and scope | Provider type, FTE, rurality, prescribing authority | Scope-enabled supply |
| Stakeholder validation | Game scoring and decision weights | Face validity and MCDA |

## Minimum validation tests

- Baseline reproduction.
- Temporal validation.
- Geographic validation.
- Equity validation.
- Known-policy-shock validation.
- Sensitivity and uncertainty analysis.

## Claim boundary

Until those tests are passed, public outputs should use phrases such as **source-informed scaffold**, **model-generated index**, and **not a calibrated forecast**.
