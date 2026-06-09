# Implementation Log

- Track opened after CAL-G-005 and release-manifest refresh were merged.
- Scope is claim-surface review and wording consistency only.
- No new evidence, model parameter, or validation-gate change is made by opening this track.
- Updated cockpit chart defaults and report-card payload tests so current UI surfaces expose `public_aggregate_validated` / `empirically_supported_if_gated` by default while preserving not-valid-for warnings.
- Updated README current-status wording and model-card links so the current release model card is primary and the v1.7.2 model card is historical.
- Updated calibration methods, CAL-G-005 policy-shock, historical model-card, and claim-boundary docs to distinguish aggregate validation from precision, implementation-impact, and causal claims.
- Added regression coverage in `models/tests/test_release_engineering.py` to prevent current surfaces from reverting to readiness-only status text.
- Search check: no current-facing matches for "Current public status remains `calibration_readiness_only`", "Until the public aggregate calibration and validation gates pass", or "all public outputs remain `public_benchmark` / `calibration_readiness_only`" in README, report, current docs, UI, or tests.
