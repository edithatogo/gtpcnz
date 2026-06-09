# Public Evidence Acquisition Governance v1

Track 070 defines the execution shell for public evidence acquisition and records the first acquisition execution step after Track 069.

The Health NZ Q3 2025 access-to-primary-care workbook was acquired from the public PHO access workbook archive family and processed beside the existing Q4 2025 workbook. This creates two public temporal periods for CAL-G-002 acquisition readiness. It is evidence acquisition, not validation success.

## Execution Boundary

Future evidence acquisition must stay within public or published aggregate sources. The public runtime path must not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation.

Each candidate source should move through these stages before model use:

1. Public-source discovery and scope fit.
2. Licence/access review.
3. Raw artefact retrieval.
4. SHA-256 checksum capture.
5. Transform into a registered processed artefact.
6. Schema validation.
7. Calibration or validation gate review.

Missing evidence at any stage is a blocker, not a reason to create placeholder data.

## Executed Acquisition

For `src_hnz_pho_access_timeseries`, the public raw source directory now contains:

- `access-to-primary-care-stats-2025-q3.xlsx`, downloaded from `https://static.info.content.health.nz/docs/about-us/health-data/Primary%20care/access-to-primary-care-stats-2025-q3.xlsx`
- `access-to-primary-care-stats-2025-q4.xlsx`, downloaded from `https://static.info.content.health.nz/docs/about-us/health-data/Primary%20care/access-to-primary-care-stats-2025-q4.xlsx`

Both raw workbooks are checked into `data/public_raw/src_hnz_pho_access_timeseries/` so the temporal validation evidence is reproducible from the repository checkout.

The deterministic transform processes all matching `access-to-primary-care-stats-*.xlsx` workbooks and derives the public reporting period from each filename. The processed numeric extract contains `2025-Q3` and `2025-Q4` rows, and `python scripts/check_public_temporal_period_acquisition.py --require-ready` passes.

The temporal holdout comparison now passes using district-level public persistence: Q3 is the training period, Q4 is the holdout period, and each district is compared with its own Q3 public aggregate rate.

CAL-G-003 and CAL-G-004 now pass using the same public Q3/Q4 workbook family at district and district-subgroup grain. CAL-G-005 now passes a bounded directional public policy-condition comparison derived from the checked-in Health NZ capitation schedule extract. Track 072 found the current PHO Services Agreement public URL returns HTML under the expected PDF filename, so it remains public `reference_only` evidence with a machine-readable extraction blocker.

## Claim Boundary

The current public aggregate calibration lane now reports `public_aggregate_validated` / `empirically_supported_if_gated` because all registered public validation gates pass. Track 070 does not support precise impact claims.

Any future upgrade beyond aggregate validation requires claim-specific public source artefacts, verified checksums, processed outputs, schema-valid rows, and passing validation gates for the relevant claim families. Readiness evidence, acquisition governance, or aggregate validation alone do not support claims of precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects.
