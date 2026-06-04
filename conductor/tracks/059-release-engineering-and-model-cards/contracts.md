# Contracts

Primary contract: `CON-REL-001`.

Allowed file ownership:
- `VERSION`
- `pyproject.toml`
- `models/primarycare_model/version.py`
- `scripts/check_version_consistency.py`
- `scripts/generate_release_model_card.py`
- `scripts/generate_release_manifest.py`
- `docs/release/**`
- `models/tests/test_release_engineering.py`
- `.github/workflows/**`

Forbidden or handoff-required files:
- `models/primarycare_model/registries/templates/**`
- `data/linked-nz/**`

Claim-boundary forbidden moves:
- Do not use private administrative data, patient-level data, confidential OIA responses, stakeholder analysis, or unpublished expert elicitation as public model inputs.
- Do not introduce black-box solvers as defaults.
- Do not let evidence monitoring mutate parameters, outputs, or claims.
- Do not claim precise fiscal savings, ED reductions, hospital-demand reductions, workforce effects, implementation impacts, or causal effects unless the relevant public-data gates pass.
- Do not edit files outside the allowed ownership list without recording a handoff and running the affected track gates.

Collision rule:

A Cline subagent must stop and write a handoff note before editing a file outside this track's allowed globs or before touching a file owned by another active work package. The coordinator may then move that task to the owning track or create a narrow follow-on work package.
