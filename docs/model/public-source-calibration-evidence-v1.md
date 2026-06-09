# Public Source Calibration Evidence v1

## Status

GTPCNZ now has verified public source acquisition evidence and passing public aggregate validation gates for the public aggregate calibration scaffold. This upgrades the aggregate calibration status while preserving explicit not-valid-for boundaries around precise causal, fiscal, hospital, workforce, and implementation claims.

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
| Temporal holdout validation | Q3/Q4 public periods available; registered district-level temporal holdout comparison passes |
| Geographic/rural holdout validation | Passed using district-level public training-period persistence against the Q4 holdout |
| Subgroup gradient validation | Passed using district-subgroup public training-period persistence at ethnicity/deprivation grain |
| Public policy-shock plausibility | Passed for the bounded capitation schedule directional policy-condition comparison; PHO Services Agreement remains reference-only |
| Calibration status | `public_aggregate_validated` |
| Claim level | `empirically_supported_if_gated` |

## Verified Source Evidence

The public source registry records seven public/published aggregate source families:

- `src_hnz_capitation_schedule`: Health NZ capitation rates public reference page. The processed capitation extract now also supplies the CAL-G-005 directional public policy-condition comparison artifact for selected access-practice versus non-access-practice published rates.
- `src_pho_services_agreement`: Health NZ PHO Services Agreement public reference. Track 072 re-fetched the registry-pinned public URL and found it currently returns HTML saved under the expected PDF filename; bounded table extraction is therefore recorded as `extraction_blocked` in `docs/model/pho-services-agreement-bounded-extraction-v1.md`.
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

The current calibration evidence supports a public aggregate validation claim only. The calibration runner now reports:

```yaml
calibration_status: public_aggregate_validated
claim_level: empirically_supported_if_gated
```

This is deliberately narrower than a forecast or impact claim. CAL-G-002 passes its registered public temporal holdout comparison, CAL-G-003 passes a district-level public geographic holdout using Q3 training-period persistence against the Q4 holdout, CAL-G-004 passes district-subgroup public subgroup-gradient holdouts at ethnicity/deprivation grain, and CAL-G-005 passes a bounded directional public policy-condition comparison derived from the checked-in Health NZ capitation schedule extract.

## Not Valid For

The public model remains not valid for:

- precise fiscal savings
- ED reductions
- hospital-demand reductions
- workforce effects
- implementation impacts
- causal effects

These exclusions remain in force unless separate public-data gates for those specific claims pass.
