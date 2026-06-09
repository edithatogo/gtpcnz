# Public Validation Numeric Comparisons

## Goal

Convert the registered Health NZ PHO access workbook into numeric public aggregate validation rows for geographic and subgroup validation readiness.

## Scope

- Parse public workbook values into a long, hashed numeric extract.
- Recalculate reported coverage rates from public enrolled and population counts.
- Use the numeric extract to move CAL-G-003 and CAL-G-004 from source-registered to numeric-ready.
- Keep claim status at `calibration_readiness_only` until model-vs-holdout comparisons pass.
