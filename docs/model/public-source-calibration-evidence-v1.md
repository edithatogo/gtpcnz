# Public Source Calibration Evidence v1

## Status

GTPCNZ now has verified public source acquisition evidence for the public aggregate calibration scaffold. This does not upgrade the model to a fully empirically calibrated policy model.

| Layer | Status |
|---|---|
| Public source files | 7 of 7 raw public artefacts present |
| Source checksums | 7 of 7 source registry checksums are verified SHA-256 values |
| Licence/access gate | Passed; sources remain public references with public access |
| Processed artefacts | 7 of 7 expected processed artefacts present |
| Processed schema gate | Passed in `--require-processed` mode |
| Calibration target readiness | Passed for 3 public aggregate targets |
| Baseline public aggregate reproduction | Passed |
| Posterior predictive checks | Passed |
| Temporal holdout validation | Public source registered; one public period available; temporal holdout comparison not yet possible |
| Geographic/rural holdout validation | Public benchmark comparison run; tolerance not passed |
| Subgroup gradient validation | Public benchmark comparisons run; tolerance not passed |
| Public policy-shock plausibility | Public policy references registered; no numeric pre/post shock comparison has passed |
| Calibration status | `calibration_readiness_only` |
| Claim level | `public_benchmark` |

## Verified Source Evidence

The public source registry records seven public/published aggregate source families:

- `src_hnz_capitation_schedule`: Health NZ capitation rates public reference page.
- `src_pho_services_agreement`: Health NZ PHO Services Agreement public PDF.
- `src_hnz_enrolment`: Health NZ primary-care public data/statistics page.
- `src_hnz_pho_access_timeseries`: Health NZ quarterly PHO access workbook with public district, ethnicity, gender, age, and deprivation aggregate rows.
- `src_mcnz_workforce`: Medical Council workforce survey public report.
- `src_nz_health_survey`: Ministry of Health New Zealand Health Survey annual update public page.
- `src_statsnz_population`: Stats NZ population indicator public page.

These source families were checked against current public landing pages during implementation. Reproducibility is enforced by the local registry checksums and raw/processed artefact gates, not by live web availability at runtime.

## Gates Run

```powershell
uv run --frozen --all-groups python scripts/check_public_source_snapshot.py --verify-files --verify-checksums --verify-licences --verify-processed
uv run --frozen --all-groups python scripts/check_public_source_fetch_scripts.py --require-raw
uv run --frozen --all-groups python scripts/check_public_source_transform_scripts.py --require-raw
uv run --frozen --all-groups python scripts/check_public_source_readiness_matrix.py --strict
uv run --frozen --all-groups python scripts/check_transformed_schemas.py --require-processed
uv run --frozen --all-groups python scripts/check_calibration_target_readiness.py
uv run --frozen --all-groups python scripts/check_calibration_validation_gates.py
uv run --frozen --all-groups python scripts/check_posterior_predictive_checks.py
uv run --frozen --all-groups python scripts/run_public_aggregate_calibration.py --check-only
```

## Calibration Interpretation

The current calibration evidence supports source-ready public aggregate benchmark checks only. The calibration runner retains:

```yaml
calibration_status: calibration_readiness_only
claim_level: public_benchmark
```

This is deliberate. CAL-G-002 and CAL-G-005 now have public readiness evidence, but they do not pass validation: CAL-G-002 has only one public period and CAL-G-005 has no numeric pre/post shock comparison. CAL-G-003 and CAL-G-004 run transparent weighted public benchmark comparisons, but those comparisons exceed tolerance and remain failed.

## Not Valid For

The public model remains not valid for:

- precise fiscal savings
- ED reductions
- hospital-demand reductions
- workforce effects
- implementation impacts
- causal effects

These exclusions remain in force unless separate public-data gates for those specific claims pass.
