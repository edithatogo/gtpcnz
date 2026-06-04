# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-050-A | `registry-classifier` | Classify every model-facing registry value as public-runtime or excluded-template without changing public claims. | models/primarycare_model/registries/public/**, models/primarycare_model/registries/templates/**, scripts/check_public_only_boundary.py, models/tests/test_public_only_boundary.py | Gates pass or blocker logged. |
| WP-050-B | `quarantine-migration` | Move sensitive/confidential/linked-data/stakeholder examples into templates marked excluded from public runtime. | models/primarycare_model/registries/public/**, models/primarycare_model/registries/templates/**, scripts/check_public_only_boundary.py, models/tests/test_public_only_boundary.py | Gates pass or blocker logged. |
| WP-050-C | `boundary-gate` | Harden `scripts/check_public_only_boundary.py` against forbidden values and self-reference false positives. | models/primarycare_model/registries/public/**, models/primarycare_model/registries/templates/**, scripts/check_public_only_boundary.py, models/tests/test_public_only_boundary.py | Gates pass or blocker logged. |
| WP-050-D | `mirror-and-tests` | Synchronise public registries into the public mirror and prove the gate/test pair passes. | models/primarycare_model/registries/public/**, models/primarycare_model/registries/templates/**, scripts/check_public_only_boundary.py, models/tests/test_public_only_boundary.py | Gates pass or blocker logged. |

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
