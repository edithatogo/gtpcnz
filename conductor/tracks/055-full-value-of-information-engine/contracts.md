# Contracts

Primary contract: `CON-VOI-001`.

Allowed file ownership:
- `models/primarycare_model/voi/**`
- `models/primarycare_model/contracts/voi.py`
- `models/primarycare_model/registries/public/voi_parameter_groups.public.v1.yaml`
- `scripts/run_voi.py`
- `docs/model/value-of-information-methods-v1.md`
- `models/tests/test_full_voi.py`

Forbidden or handoff-required files:
- `docs/qualitative/**`
- `data/templates/*stakeholder*`
- `models/primarycare_model/app.py`

Claim-boundary forbidden moves:
- Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation as public model inputs.
- Do not introduce black-box solvers as defaults.
- Do not let evidence monitoring mutate parameters, outputs, or claims.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data gates pass.
- Do not edit files outside the allowed ownership list without recording a handoff and running the affected track gates.

Collision rule:

A Cline subagent must stop and write a handoff note before editing a file outside this track's allowed globs or before touching a file owned by another active work package. The coordinator may then move that task to the owning track or create a narrow follow-on work package.
