# Calibration starter report v1.5.0

This report starts, but does not complete, a fully calibrated predictive model.

The starter model uses synthetic observations to exercise the pipeline. The fitted parameter table and observed-versus-predicted plots are generated in `outputs/`.

## Demonstration outputs

- `outputs/calibration-synthetic-observed-v1.5.0.csv`
- `outputs/calibration-fitted-predicted-v1.5.0.csv`
- `outputs/calibration-parameter-estimates-v1.5.0.csv`
- `outputs/calibration-scenario-comparison-v1.5.0.csv`
- `outputs/calibration-observed-vs-predicted-primary-v1.5.0.png`
- `outputs/calibration-observed-vs-predicted-ed-v1.5.0.png`
- `outputs/calibration-observed-vs-predicted-cost-v1.5.0.png`
- `outputs/calibration-parameter-recovery-v1.5.0.png`

## Scenario comparison from synthetic starter

| scenario    |   mean_primary_contacts |   mean_unmet_need |   mean_ed_presentations |   mean_ambulance_conveyances |   mean_public_cost |
|:------------|------------------------:|------------------:|------------------------:|-----------------------------:|-------------------:|
| baseline    |                  1212.5 |         208.046   |                 381.236 |                     170.296  |        1.85331e+06 |
| full_hybrid |                  1810.5 |           5.71372 |                 224.428 |                      72.5962 |        1.57615e+06 |

## Interpretation

The synthetic demonstration is a software and workflow check only. It should not be interpreted as evidence about New Zealand effect sizes. The next stage is to replace synthetic observations with linked monthly data and replace the placeholder equations with empirically estimated submodels.
