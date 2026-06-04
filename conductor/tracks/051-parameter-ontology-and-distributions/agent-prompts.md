# Agent Prompts

## Track Lead Prompt

You are the track lead for `051-parameter-ontology-and-distributions`. Use DeepSeek v4 Flash as a narrow implementation worker. Your job is to coordinate the work packages, not broaden scope.

Constraints:
- Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation as public model inputs.
- Do not introduce black-box solvers as defaults.
- Do not let evidence monitoring mutate parameters, outputs, or claims.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data gates pass.
- Do not edit files outside the allowed ownership list without recording a handoff and running the affected track gates.

Allowed files:
- `models/primarycare_model/contracts/public_parameters.py`
- `models/primarycare_model/validation/public_parameter_loader.py`
- `models/primarycare_model/registries/public/parameters.public.v1.yaml`
- `scripts/check_parameter_traceability.py`
- `models/tests/test_parameter_traceability.py`
- `docs/model/public-parameter-ontology-v1.md`

Required gates:
- `python scripts/check_parameter_traceability.py`
- `python -m pytest -q models/tests/test_parameter_traceability.py`

## Work-Package Subagent Prompt

You are assigned one work package from `051-parameter-ontology-and-distributions`. Edit only files listed under allowed file ownership. If you need any other file, stop and write a handoff request. Preserve the public benchmark claim boundary. Run the package gate before returning.
