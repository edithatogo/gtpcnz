# Repo index v1.7.0

## Current release

**v1.7.0 — full parameterised model scaffold.**

This release continues building the calibrated-model pathway, but does not claim empirical calibration. It expands the model into a fully specified parameterisation framework with explicit parameters, bounds, scenario values, data-input contracts, monthly dynamics, sensitivity analysis and visual outputs.

## Key artefacts

```text
models/primarycare_model/full_parameterised_model_v170.py
models/tests/test_full_parameterised_model_v170.py
scripts/run_full_parameterised_model_v170.py

docs/calibration/full-parameterised-model-build-report-v1.7.0.md
docs/calibration/parameterisation-data-contract-v1.7.0.md
docs/calibration/real-data-update-pathway-v1.7.0.md
docs/calibration/full-parameter-register-v1.7.0.csv
docs/calibration/data-input-contract-v1.7.0.csv
docs/calibration/scenario-parameter-matrix-v1.7.0.csv
docs/calibration/full-parameterised-summary-results-v1.7.0.csv
docs/calibration/full-parameterised-monthly-results-v1.7.0.csv
docs/calibration/full-parameterised-sensitivity-v1.7.0.csv
docs/calibration/calibration-target-matrix-v1.7.0.csv

outputs/full-parameterised-model-build-report-v1.7.0.md
outputs/full-parameter-register-v1.7.0.csv
outputs/data-input-contract-v1.7.0.csv
outputs/scenario-parameter-matrix-v1.7.0.csv
outputs/full-parameterised-summary-results-v1.7.0.csv
outputs/full-parameterised-monthly-results-v1.7.0.csv
outputs/full-parameterised-sensitivity-v1.7.0.csv
outputs/full-parameterised-dashboard-table-v1.7.0.csv
outputs/calibration-target-matrix-v1.7.0.csv
outputs/model-logic-map-v1.7.0.csv
outputs/figures/full-parameterised-*.png
```

## Headline result

The full hybrid upstream architecture ranks first in the scaffold. Controlled uncapped medical fee-for-service plus place accountability ranks above uncapped fee-for-service without place accountability. The weak-control uncapped option ranks last after risk adjustment.

## Caveat

The model is fully specified and parameterised at the scaffold level. It is not empirically calibrated or predictive until real data replace the priors and the model passes validation tests.
