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
| Calibration state | `public_aggregate_validated` |
| Claim level | `empirically_supported_if_gated` |

Detailed evidence is recorded in `docs/model/public-source-calibration-evidence-v1.md`.

## Verified Public Source Families

The public runtime source path now has raw and processed evidence for:

- Health NZ capitation rates public reference page, including the bounded CAL-G-005 directional comparison artifact derived from the checked-in public table extract.
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

## Current Calibration Boundary

The public aggregate calibration runner now reports:

```yaml
calibration_status: public_aggregate_validated
claim_level: empirically_supported_if_gated
```

Source acquisition is no longer the blocker for the registered public aggregate validation lane. CAL-G-002 now has Q3/Q4 public temporal evidence and passes its registered district-level temporal holdout comparison. CAL-G-003 also passes a district-level public geographic holdout using Q3 training-period persistence against the Q4 holdout. CAL-G-004 passes district-subgroup public subgroup-gradient holdouts at ethnicity/deprivation grain. CAL-G-005 passes a bounded directional public policy-condition comparison derived from the checked-in Health NZ capitation schedule extract.

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

The next substantive step is to harden release-facing claim governance around the validated aggregate lane:

1. Release-gate review now that all registered CAL-G validation gates pass together.
2. Additional independent regional, rurality-grain, subgroup-gradient, or policy-shock public validation targets where public data permit.
3. Bounded PHO Services Agreement table extraction if it is to move from `reference_only` to a numeric comparison lane.

Even after the aggregate validation upgrade, the model remains not valid for precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless separate claim-specific evidence gates pass.
