# Release notes v1.5.0

## Purpose

This release responds to three requirements:

1. make the Substack posts comprehensively hyperlinked and longer;
2. add more explanatory microeconomic and workflow diagrams;
3. start, but not complete, the empirically calibrated predictive model pathway.

## Substack changes

- 18 expanded posts in `docs/substack-ready/posts-v1.5.0/`.
- Most posts now sit around 1,900-2,200 words.
- Each post includes a figure, a plain-English explainer, a game table, modelling implications, empirical tests and a source list.
- Publication calendar: twice weekly on Tuesdays and Fridays from 12 May 2026 to 10 July 2026.

## Calibrated model starter

- New module: `models/primarycare_model/calibration_v150.py`.
- New tests: `models/tests/test_calibration_v150.py`.
- Synthetic calibration demonstration in `outputs/`.
- Calibration build plan and data schema in `docs/calibration/`.

## Caveat

The calibration starter is not empirical calibration. It is the first executable pipeline ready to accept linked NZ data when available.
