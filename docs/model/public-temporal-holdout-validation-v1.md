# Public Temporal Holdout Validation

CAL-G-002 is now represented as a public-only temporal validation lane. The
registered source is the Health NZ PHO access workbook numeric extract:

- registry: `models/primarycare_model/registries/public/temporal_holdout_targets.public.v1.yaml`
- processed evidence: `data/public_processed/src_hnz_pho_access_timeseries/pho_access_numeric_extract.csv`
- gate: `CAL-G-002`
- claim status: `calibration_readiness_only`

The current public extract contains two published periods, `2025-Q3` and
`2025-Q4`. The lane uses Q3 as the public training period and Q4 as the latest
public holdout period.

The registered benchmark is district-level public persistence: each Q4
district total-coverage observation is compared with the same district's Q3
public aggregate rate. If a holdout district is absent from the training
period, the comparator falls back to the national Q3 weighted rate. This uses
only public aggregate workbook rows and avoids inventing regional data.

## Public Period Acquisition Readiness

CAL-G-002 now also has a machine-readable temporal-period acquisition plan:

- plan: `models/primarycare_model/registries/public/temporal_period_acquisition.public.v1.yaml`
- checker: `python scripts/check_public_temporal_period_acquisition.py`
- strict checker: `python scripts/check_public_temporal_period_acquisition.py --require-ready`

The acquisition plan records both local public periods already processed:
`2025-Q3` and `2025-Q4`. Default and strict acquisition-readiness modes pass.
Neither mode upgrades the model beyond its registered claim boundary.

Passing CAL-G-002 requires all of the following:

1. The source remains public/published and checksum-backed.
2. The processed extract contains at least one public training period and a
   distinct public holdout period.
3. The latest-period public holdout comparison stays within the registered
   maximum absolute error tolerance.

This lane is not valid for individual-care inference, private administrative
calibration, causal claims, fiscal savings, hospital-demand reductions,
workforce effects, or implementation-impact claims.
