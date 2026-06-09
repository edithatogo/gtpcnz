# CAL-G-005 public policy-shock plausibility lane

This lane registers published public-policy shock references that may later support a public numeric pre/post plausibility comparison.

Current status: CAL-G-005 directional plausibility passed for the registered
numeric comparison lane. This contributes to the bounded aggregate validation
surface, not to precision, implementation-impact, or causal claims.

Claim boundary: the registered evidence does not support causal claims, effect-size claims, fiscal savings, hospital-demand reductions, workforce effects, or implementation-impact claims. CAL-G-005 is a directional public-policy plausibility check only.

The machine-readable registry is `models/primarycare_model/registries/public/policy_shock_plausibility.public.v1.yaml`. The validation entry point is `scripts/check_public_policy_shock_plausibility.py`.

## Numeric comparison scaffold

Each registered `numeric_comparison` shock row declares the required public comparison artifact columns:

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

The checker validates a registered artifact strictly: the artifact must exist, include those columns, include rows for the registered `shock_id`, and provide non-empty `metric_id`, `pre_period`, and `post_period` fields. `pre_value`, `post_value`, and `observed_delta` must be numeric, and `observed_delta` must equal `post_value - pre_value`. `observed_direction` and `modelled_direction` must be one of `increase`, `decrease`, or `no_change`; `observed_direction` must match `observed_delta`; and `comparison_result=passed` requires the observed and modelled directions to agree. The accepted machine statuses are `artifact_not_registered`, `artifact_missing`, `artifact_invalid`, `numeric_pre_post_ready`, `comparison_passed`, and `comparison_failed`.

Contract tests use synthetic CSV artifacts only. They are not public evidence and must not be registered as production comparison artifacts.

## Current public artifact

The production comparison artifact is
`data/public_processed/src_hnz_capitation_schedule/policy_shock_pre_post_comparison.csv`.
It is derived from the checked-in Health NZ capitation schedule extract
`data/public_processed/src_hnz_capitation_schedule/capitation_rates.csv`.

The comparison uses published rate conditions from the public schedule effective
2025-07-01:

- baseline condition: non-access practice annual N-rate;
- policy condition: access practice annual N-rate;
- checked metrics: 05-14 female and 05-14 male annual N-rates.

Both rows have positive public-schedule deltas and match the modelled
directional expectation that the access-practice condition is funded above the
non-access-practice condition for those metrics. This does not estimate patient
access, utilisation, fiscal savings, hospital-demand change, workforce effects,
implementation effects, or causal effects.

The PHO Services Agreement public reference remains registered with
`gate_role: reference_only`. Track 072 re-fetched the registry-pinned public URL
and found it currently returns HTML under the expected PDF filename, so the
processed artifact records `extraction_blocked`. It is not counted as a required
numeric comparison unless a replacement public PDF or machine-readable table
source is registered and satisfies the numeric comparison contract.
