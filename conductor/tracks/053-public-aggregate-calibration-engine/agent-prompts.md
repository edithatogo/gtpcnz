# Agent Prompts

## Track Lead Prompt

You are the track lead for `053-public-aggregate-calibration-engine`. Use DeepSeek v4 Flash as a narrow implementation worker. Your job is to coordinate the work packages, not broaden scope.

Constraints:
- Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation as public model inputs.
- Do not introduce black-box solvers as defaults.
- Do not let evidence monitoring mutate parameters, outputs, or claims.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data gates pass.
- Do not edit files outside the allowed ownership list without recording a handoff and running the affected track gates.

Allowed files:
- `models/primarycare_model/calibration/**`
- `models/primarycare_model/contracts/calibration_targets.py`
- `models/primarycare_model/registries/public/calibration_targets.public.v1.yaml`
- `scripts/run_public_aggregate_calibration.py`
- `docs/calibration/public-aggregate-calibration-methods-v1.md`
- `models/tests/test_public_aggregate_calibration.py`

Required gates:
- `python scripts/run_public_aggregate_calibration.py --check-only`
- `python -m pytest -q models/tests/test_public_aggregate_calibration.py`

## Work-Package Subagent Prompt

You are assigned one work package from `053-public-aggregate-calibration-engine`. Edit only files listed under allowed file ownership. If you need any other file, stop and write a handoff request. Preserve the public benchmark claim boundary. Run the package gate before returning.
