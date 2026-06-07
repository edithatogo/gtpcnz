# Implementation Log

2026-06-03: Initial public-only SOTA calibration scaffold added with strict claim-boundary posture.

2026-06-03: Cline/deepseek parallel execution controls added: dependency wave, file ownership, work packages, subagent prompts, collision rules, and exact gates.


2026-06-03: Wave 2 completion (Cline DeepSeek v4 Flash coordinator run).
  Work packages: All calibration engine work packages validated.
  Files changed: Verified models/primarycare_model/calibration/**, models/primarycare_model/contracts/calibration_targets.py, models/primarycare_model/registries/public/calibration_targets.public.v1.yaml, scripts/run_public_aggregate_calibration.py, docs/calibration/public-aggregate-calibration-methods-v1.md, models/tests/test_public_aggregate_calibration.py.
  Gates run:
    - python scripts/run_public_aggregate_calibration.py --check-only -> PASSED (calibration_readiness_only; claim_level: public_benchmark; all 3 targets source_ready=false)
    - python -m pytest -q models/tests/test_public_aggregate_calibration.py -> PASSED (1 passed)
  Result: Both gates pass. Calibration is readiness-only; no precise claims made.
  Claim-boundary status: calibration_readiness_only (not_valid_for: precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, causal effects).
  Residual blockers: All 3 calibration targets have source_ready=false; pending public data download/checksum verification.
  Follow-on owner: coordinator (053 complete; 056, 057, 059 unblocked).

2026-06-07: Calibration target readiness matrix gate added.
  Work package: WP-053-B (calibration-runner), WP-053-D (claim-downgrade), linked to Track 052 source readiness.
  Files changed: models/primarycare_model/calibration/calibration_target_readiness.py, scripts/check_calibration_target_readiness.py, models/tests/test_calibration_target_readiness.py, release gate wiring, docs/calibration/public-aggregate-calibration-methods-v1.md, docs/model/public-source-readiness-closeout-v1.md, conductor/state.md.
  Gates run:
    - python scripts/check_calibration_target_readiness.py -> PASSED (readiness-compatible default matrix)
    - python scripts/check_calibration_target_readiness.py --strict -> FAILED AS EXPECTED because linked public sources are not source_ready.
    - python -m pytest -q models/tests/test_calibration_target_readiness.py models/tests/test_public_aggregate_calibration.py models/tests/test_release_engineering.py -> PASSED
  Result: Public aggregate calibration now exposes target-level blockers joined to source readiness, relative error tolerance, and not-valid-for claim boundaries.
  Claim-boundary status: public_benchmark / calibration_readiness_only preserved. No target or calibration claim was promoted.
2026-06-07: Calibration validation gate matrix added.
  Work package: WP-053-C (ppc-and-holdouts), WP-053-D (claim-downgrade).
  Files changed: models/primarycare_model/calibration/calibration_validation_gates.py, scripts/check_calibration_validation_gates.py, models/tests/test_calibration_validation_gates.py, release gate wiring, docs/calibration/public-aggregate-calibration-methods-v1.md, docs/model/public-source-readiness-closeout-v1.md, conductor/state.md.
  Gates run:
    - python scripts/check_calibration_validation_gates.py -> PASSED (readiness-compatible default matrix)
    - python scripts/check_calibration_validation_gates.py --strict -> FAILED AS EXPECTED because baseline targets and public holdout/PPC datasets are not ready.
    - python -m pytest -q models/tests/test_calibration_validation_gates.py models/tests/test_calibration_target_readiness.py models/tests/test_public_aggregate_calibration.py models/tests/test_release_engineering.py -> PASSED
  Result: Public aggregate calibration now exposes baseline, temporal, geographic, subgroup, policy-shock, posterior-predictive, and claim-downgrade gate statuses without promoting claims.
  Claim-boundary status: public_benchmark / calibration_readiness_only preserved. No validation gate upgraded empirical claim status.
2026-06-07: Posterior predictive readiness gate added.
  Work package: WP-053-C (ppc-and-holdouts), linked to CAL-G-006.
  Files changed: models/primarycare_model/calibration/posterior_predictive_checks.py, scripts/check_posterior_predictive_checks.py, models/tests/test_posterior_predictive_checks.py, release gate wiring, docs/calibration/public-aggregate-calibration-methods-v1.md, docs/model/public-source-readiness-closeout-v1.md, conductor/state.md.
  Gates run:
    - python scripts/check_posterior_predictive_checks.py -> PASSED (readiness-compatible PPC report)
    - python scripts/check_posterior_predictive_checks.py --strict -> FAILED AS EXPECTED because CAL-G-006 and source-ready public targets are not yet passed.
    - python -m pytest -q models/tests/test_posterior_predictive_checks.py models/tests/test_calibration_validation_gates.py models/tests/test_calibration_target_readiness.py models/tests/test_release_engineering.py -> PASSED
  Result: Posterior predictive checks now expose target-level readiness, CAL-G-006 status, failed targets, blockers, and not-valid-for boundaries without promoting claims.
  Claim-boundary status: public_benchmark / calibration_readiness_only preserved. No PPC gate upgraded empirical claim status.
