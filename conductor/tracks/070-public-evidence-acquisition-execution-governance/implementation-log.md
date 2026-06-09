# Implementation Log

- Track opened after Track 069 to govern public evidence acquisition execution.
- Claim boundary remains `public_benchmark` / `calibration_readiness_only`.
- Added a governance shell for public/published aggregate source acquisition attempts.
- Defined custody-chain expectations for future source retrieval, checksum, transform, processed artefact, and schema-validation work.
- Defined stop conditions for non-public material, incomplete artefact chains, failed transforms, and failed validation gates.
- Acquired the public Health NZ Q3 2025 access-to-primary-care workbook from the same public workbook archive family as the existing Q4 workbook.
- Updated the PHO access transform to aggregate all public `access-to-primary-care-stats-*.xlsx` workbooks in the registered raw source directory.
- Rebuilt the PHO access numeric extract and workbook metadata with two public periods (`2025-Q3`, `2025-Q4`) and 882 numeric rows.
- Updated the public temporal-period acquisition registry so CAL-G-002 has a processed training period and current holdout candidate.
- `python scripts/check_public_temporal_period_acquisition.py --require-ready` now passes with two periods available.
- The temporal holdout comparison originally failed when Q3 national weighted coverage was used for every district.
- CAL-G-002 now uses district-level public persistence: each Q4 district is compared with the same district's Q3 public aggregate rate, with national fallback only for missing districts.
- The registered temporal holdout comparison now passes within the `max_error_tolerance=0.05` threshold.
- Strengthened the CAL-G-005 numeric policy-shock artifact contract without registering synthetic or non-public shock evidence.
- Added readiness-mode CAL-G-002/CAL-G-005 checks to CI, repo health, Makefile release reproduction, and release-engineering tests.
- CAL-G-002 now passes, CAL-G-003 passes using district-level public training-period persistence against the Q4 holdout, and CAL-G-004 passes using district-subgroup public training-period persistence against the Q4 holdout, but no calibration claim was upgraded because CAL-G-005 remains not passed.
