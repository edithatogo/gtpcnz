# Public Aggregate Calibration Methods v1

Calibration uses public or published aggregate targets only. Passing checks can upgrade bounded outputs; failed or unavailable checks downgrade outputs to public benchmark status.

## Target Readiness Gate

Each calibration target is joined to the public source readiness matrix before any empirical calibration claim can be promoted. The readiness-compatible gate is:

```sh
python scripts/check_calibration_target_readiness.py
```

The strict calibration-upgrade gate is:

```sh
python scripts/check_calibration_target_readiness.py --strict
```

Strict mode fails unless every linked public source is `source_ready=true`, every target is within its public tolerance, raw source checksums are verified, and processed artifacts exist. In the current release, these strict source and target checks pass for the registered aggregate target set.

The gate keeps these claim boundaries attached to every target:

- precise fiscal savings
- ED reductions
- hospital-demand reductions
- workforce effects
- implementation impacts
- causal effects

Current public aggregate status is `public_aggregate_validated` / `empirically_supported_if_gated` for registered public aggregate gates only. This does not authorize precise fiscal, ED, hospital-demand, workforce, implementation-impact, or causal claims.

The public aggregate calibration runner emits this target matrix together with `validation_gates` and
`posterior_predictive_checks` sections:

```sh
python scripts/run_public_aggregate_calibration.py --check-only
```

Those nested sections are the report/model-card contract for aggregate validation status. They must not be
interpreted as precision, implementation-impact, or causal validation.
## Validation Gate Matrix

The public aggregate validation gates are reported by:

```sh
python scripts/check_calibration_validation_gates.py
```

The strict calibration-upgrade gate is:

```sh
python scripts/check_calibration_validation_gates.py --strict
```

The matrix covers:

- CAL-G-001 baseline public aggregate reproduction
- CAL-G-002 temporal holdout validation where public time series permit
- CAL-G-003 geographic/rural holdout validation where public regional data permit
- CAL-G-004 subgroup gradient validation where public subgroup data permit
- CAL-G-005 public policy shock plausibility where published shock data permit
- CAL-G-006 posterior predictive checks
- CAL-G-007 claim-level downgrade when any gate fails or is unavailable

Default mode reports the current gate matrix without mutating claims. Strict mode fails if source-ready public targets, processed artifacts, verified checksums, or public holdout/PPC data are unavailable. In the current release, CAL-G-001 through CAL-G-007 pass for the registered aggregate validation lane, while claim-specific precision and causal boundaries remain excluded.
## Posterior Predictive Check Readiness

Posterior predictive check readiness is reported by:

```sh
python scripts/check_posterior_predictive_checks.py
```

The strict PPC upgrade gate is:

```sh
python scripts/check_posterior_predictive_checks.py --strict
```

The PPC report is tied to CAL-G-006 in the validation gate matrix. Default mode reports the current PPC status and preserves not-valid-for claim boundaries. Strict mode fails unless linked public targets are source-ready, validation gates pass, and reproducible predictive checks can be run from verified public aggregate inputs.
