# Public Source Readiness Closeout v1

## Current Status

Public source acquisition has moved from placeholder readiness into verified public-source evidence.

| Property | Value |
|---|---|
| Public source raw artefacts | 7 of 7 present |
| Source checksums | 7 of 7 verified SHA-256 values in `sources.public.v1.yaml` |
| Processed artefacts | 7 of 7 expected processed outputs present |
| Strict source readiness matrix | Passed |
| Processed schema validation | Passed with `--require-processed` |
| Calibration target readiness | Passed for three public aggregate targets |
| Baseline public aggregate reproduction | Passed |
| Posterior predictive checks | Passed |
| Calibration state | `calibration_readiness_only` |
| Claim level | `public_benchmark` |

Detailed evidence is recorded in `docs/model/public-source-calibration-evidence-v1.md`.

## Verified Public Source Families

The public runtime source path now has raw and processed evidence for:

- Health NZ capitation rates public reference page.
- Health NZ PHO Services Agreement public PDF.
- Health NZ primary-care enrolment public data/statistics page.
- Health NZ PHO access quarterly public workbook.
- Medical Council workforce survey public report.
- Ministry of Health New Zealand Health Survey annual update public page.
- Stats NZ population indicator public page.

The source registry and snapshot manifest provide the reproducible checksum surface. Runtime calibration does not depend on live web requests.

## Gates That Now Pass

```powershell
uv run --frozen --all-groups python scripts/check_public_source_snapshot.py --verify-files --verify-checksums --verify-licences --verify-processed
uv run --frozen --all-groups python scripts/check_public_source_fetch_scripts.py --require-raw
uv run --frozen --all-groups python scripts/check_public_source_transform_scripts.py --require-raw
uv run --frozen --all-groups python scripts/check_public_source_readiness_matrix.py --strict
uv run --frozen --all-groups python scripts/check_transformed_schemas.py --require-processed
uv run --frozen --all-groups python scripts/check_calibration_target_readiness.py
uv run --frozen --all-groups python scripts/check_posterior_predictive_checks.py
uv run --frozen --all-groups python scripts/run_public_aggregate_calibration.py --check-only
```

## Why Calibration Is Still Readiness-Only

The public aggregate calibration runner correctly keeps:

```yaml
calibration_status: calibration_readiness_only
claim_level: public_benchmark
```

The remaining blocker is no longer source acquisition. CAL-G-003 and CAL-G-004 now have public numeric validation evidence, but no model-vs-holdout or model-vs-gradient comparison has passed. CAL-G-002 temporal holdout and CAL-G-005 published policy-shock validation still report `public_data_unavailable`.

## Claim Boundary

The public model remains not valid for:

- precise fiscal savings
- ED reductions
- hospital-demand reductions
- workforce effects
- implementation impacts
- causal effects

No private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation are used in the public model path.

## Next Evidence Work

The next substantive step is to locate and register public aggregate validation datasets for:

1. Temporal holdout validation.
2. Geographic or rural holdout validation.
3. Subgroup gradient validation.
4. Published policy-shock plausibility validation.

Only after those validation families have public source artefacts, verified checksums, processed outputs, and passing gates should the calibration status be considered for upgrade.
