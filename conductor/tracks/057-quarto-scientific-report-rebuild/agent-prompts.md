# Agent Prompts

## Track Lead Prompt

You are the track lead for `057-quarto-scientific-report-rebuild`. Use DeepSeek v4 Flash as a narrow implementation worker. Your job is to coordinate the work packages, not broaden scope.

Constraints:
- Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation as public model inputs.
- Do not introduce black-box solvers as defaults.
- Do not let evidence monitoring mutate parameters, outputs, or claims.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data gates pass.
- Do not edit files outside the allowed ownership list without recording a handoff and running the affected track gates.

Allowed files:
- `reports/public_aggregate_model_report.qmd`
- `docs/release/model-card-template.qmd`
- `scripts/render_public_model_report.py`
- `models/tests/test_report_artifacts.py`

Required gates:
- `python scripts/render_public_model_report.py`
- `python -m pytest -q models/tests/test_report_artifacts.py`

## Work-Package Subagent Prompt

You are assigned one work package from `057-quarto-scientific-report-rebuild`. Edit only files listed under allowed file ownership. If you need any other file, stop and write a handoff request. Preserve the public benchmark claim boundary. Run the package gate before returning.
