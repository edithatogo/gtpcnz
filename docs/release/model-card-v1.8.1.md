# GTPCNZ public model card v1.8.1

Claim level: empirically_supported_if_gated.
Calibration status: public_aggregate_validated.
Interpretation: Public aggregate calibration passed registered public target and validation gates; not-valid-for warnings still exclude precise fiscal, ED, hospital-demand, workforce, implementation-impact, and causal claims.
Not valid for: precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, causal effects.
Inputs: public or published aggregate sources only.

## Validation gates

- CAL-G-001: passed (baseline_public_aggregate_reproduction)
- CAL-G-002: passed (temporal_holdout_validation)
- CAL-G-003: passed (geographic_holdout_validation)
- CAL-G-004: passed (subgroup_gradient_validation)
- CAL-G-005: passed (public_policy_shock_plausibility)
- CAL-G-006: passed (posterior_predictive_checks)
- CAL-G-007: passed (claim_level_downgrade)
