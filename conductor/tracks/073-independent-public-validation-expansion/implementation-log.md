# Implementation Log

- Track opened to govern validation expansion beyond the current PHO access and capitation schedule evidence.
- Added `models/primarycare_model/registries/public/validation_source_candidates.public.v1.yaml` as a typed candidate registry outside the runtime public source snapshot.
- Registered the Ministry of Health planning and performance historical measures page as an independent public retrieval-plan candidate for hospital-pressure and avoidable-admission validation families.
- Recorded HQSC Atlas of Healthcare Variation PHO analyses as a public candidate pending domain-specific export locator, grain, licence, and independence review.
- Rejected the New Zealand Health Survey regional release for independent-validation counting where the same survey family already supports `src_nz_health_survey` calibration target evidence.
- Added `models/primarycare_model/contracts/validation_sources.py`, `models/primarycare_model/data/public_validation_sources.py`, `scripts/check_public_validation_source_candidates.py`, and `models/tests/test_public_validation_source_candidates.py`.
- Wired the candidate checker into `scripts/check_repo_health.py`.
- Documentation is in `docs/model/independent-public-validation-source-expansion-v1.md`.
- Current aggregate validation status remains governed by already-merged CAL-G-001 through CAL-G-007 checks. Track 073 does not load candidate sources into runtime and does not upgrade precision, hospital-demand, ED, workforce, implementation, fiscal, or causal claims.
