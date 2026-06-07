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

Strict mode must fail until every linked public source is `source_ready=true`, every target is within its public tolerance, raw source checksums are verified, and processed artifacts exist. The default mode reports target readiness without changing claim status.

The gate keeps these claim boundaries attached to every target:

- precise fiscal savings
- ED reductions
- hospital-demand reductions
- workforce effects
- implementation impacts
- causal effects

Current public status remains `calibration_readiness_only` because linked source rows have pending raw files, pending checksums, and pending processed outputs.
