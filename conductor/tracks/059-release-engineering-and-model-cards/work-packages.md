# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-059-A | `version-consistency` | Align VERSION, pyproject, app version and generated artefact names. | VERSION, pyproject.toml, models/primarycare_model/version.py, scripts/check_version_consistency.py, scripts/generate_release_model_card.py, scripts/generate_release_manifest.py, docs/release/**, models/tests/test_release_engineering.py, .github/workflows/** | Gates pass or blocker logged. |
| WP-059-B | `model-card` | Generate claim-gated model card with source and not-valid-for fields. | VERSION, pyproject.toml, models/primarycare_model/version.py, scripts/check_version_consistency.py, scripts/generate_release_model_card.py, scripts/generate_release_manifest.py, docs/release/**, models/tests/test_release_engineering.py, .github/workflows/** | Gates pass or blocker logged. |
| WP-059-C | `release-manifest` | Generate hashes for source snapshot, parameters, model, outputs and gate statuses. | VERSION, pyproject.toml, models/primarycare_model/version.py, scripts/check_version_consistency.py, scripts/generate_release_model_card.py, scripts/generate_release_manifest.py, docs/release/**, models/tests/test_release_engineering.py, .github/workflows/** | Gates pass or blocker logged. |
| WP-059-D | `ci-release-gates` | Wire public-only, calibration, VOI, visual, accessibility and release gates into CI. | VERSION, pyproject.toml, models/primarycare_model/version.py, scripts/check_version_consistency.py, scripts/generate_release_model_card.py, scripts/generate_release_manifest.py, docs/release/**, models/tests/test_release_engineering.py, .github/workflows/** | Gates pass or blocker logged. |

Handoff format:

```text
Work package:
Files changed:
Gates run:
Result:
Claim-boundary status:
Residual blockers:
Follow-on owner:
```
