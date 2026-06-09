# Public Temporal Holdout Validation

CAL-G-002 is now represented as a public-only temporal validation lane. The
registered source is the Health NZ PHO access workbook numeric extract:

- registry: `models/primarycare_model/registries/public/temporal_holdout_targets.public.v1.yaml`
- processed evidence: `data/public_processed/src_hnz_pho_access_timeseries/pho_access_numeric_extract.csv`
- gate: `CAL-G-002`
- claim status: `calibration_readiness_only`

The current public extract contains one published period, `2025-Q4`. That is
valid public validation-source evidence, but it is not enough for a temporal
train/holdout comparison. The lane therefore reports
`public_validation_source_registered` until at least two public periods are
available and the latest-period holdout comparison passes the registered
tolerance.

Passing CAL-G-002 requires all of the following:

1. The source remains public/published and checksum-backed.
2. The processed extract contains at least one public training period and a
   distinct public holdout period.
3. The latest-period public holdout comparison stays within the registered
   maximum absolute error tolerance.

This lane is not valid for individual-care inference, private administrative
calibration, causal claims, fiscal savings, hospital-demand reductions,
workforce effects, or implementation-impact claims.
