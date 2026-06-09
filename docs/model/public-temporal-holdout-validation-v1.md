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

## Public Period Acquisition Readiness

CAL-G-002 now also has a machine-readable temporal-period acquisition plan:

- plan: `models/primarycare_model/registries/public/temporal_period_acquisition.public.v1.yaml`
- checker: `python scripts/check_public_temporal_period_acquisition.py`
- strict checker: `python scripts/check_public_temporal_period_acquisition.py --require-ready`

The acquisition plan records the local public period already processed
(`2025-Q4`) and the missing public requirement for a temporal comparison: at
least one distinct public Health NZ access-to-primary-care workbook period
before the latest available period. The requirement is deliberately expressed
as `any_public_period_before_latest_available` because no earlier public
workbook is currently local in this repository. It is an acquisition target,
not substituted data.

Default checker mode is readiness-compatible and passes while reporting the
missing public period requirement. Strict mode fails until enough real public
periods are locally present and processed. Neither mode upgrades CAL-G-002
from `calibration_readiness_only`.

Passing CAL-G-002 requires all of the following:

1. The source remains public/published and checksum-backed.
2. The processed extract contains at least one public training period and a
   distinct public holdout period.
3. The latest-period public holdout comparison stays within the registered
   maximum absolute error tolerance.

This lane is not valid for individual-care inference, private administrative
calibration, causal claims, fiscal savings, hospital-demand reductions,
workforce effects, or implementation-impact claims.
