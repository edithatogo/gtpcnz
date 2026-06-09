# CAL-G-005 public policy-shock plausibility lane

This lane registers published public-policy shock references that may later support a public numeric pre/post plausibility comparison.

Current status: readiness-only.

Claim boundary: the registered evidence does not support causal claims, effect-size claims, fiscal savings, hospital-demand reductions, workforce effects, or implementation-impact claims. CAL-G-005 can pass only after a public numeric pre/post shock comparison is registered and passes the lane tolerance rules.

The machine-readable registry is `models/primarycare_model/registries/public/policy_shock_plausibility.public.v1.yaml`. The validation entry point is `scripts/check_public_policy_shock_plausibility.py`.

## Numeric comparison scaffold

Each registered shock row declares the required public comparison artifact columns:

- `shock_id`
- `metric_id`
- `pre_period`
- `post_period`
- `pre_value`
- `post_value`
- `observed_delta`
- `observed_direction`
- `modelled_direction`
- `comparison_result`

The checker validates a registered artifact strictly: the artifact must exist, include those columns, include rows for the registered `shock_id`, and provide numeric `pre_value` and `post_value` fields. The accepted machine statuses are `artifact_not_registered`, `artifact_missing`, `artifact_invalid`, `numeric_pre_post_ready`, `comparison_passed`, and `comparison_failed`.

As of this registry version, no public numeric pre/post policy-shock comparison artifact is registered. The lane therefore remains `public_validation_source_registered` / `calibration_readiness_only`. The checker exits successfully for evidence reporting and fails only when `--require-pass` is used.
