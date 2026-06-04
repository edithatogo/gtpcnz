# Contracts

Primary contract: `CON-UNC-001`.

Allowed file ownership:
- `models/primarycare_model/contracts/structural_models.py`
- `models/primarycare_model/uncertainty/**`
- `models/primarycare_model/registries/public/structural_models.public.v1.yaml`
- `docs/model/structural-uncertainty-v1.md`
- `docs/diagrams/structural-ensemble.mmd`
- `models/tests/test_structural_ensemble.py`

Forbidden or handoff-required files:
- `data/linked-nz/**`
- `models/primarycare_model/app.py`

Claim-boundary forbidden moves:
- Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation as public model inputs.
- Do not introduce black-box solvers as defaults.
- Do not let evidence monitoring mutate parameters, outputs, or claims.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data gates pass.
- Do not edit files outside the allowed ownership list without recording a handoff and running the affected track gates.

Collision rule:

A Cline subagent must stop and write a handoff note before editing a file outside this track's allowed globs or before touching a file owned by another active work package. The coordinator may then move that task to the owning track or create a narrow follow-on work package.
