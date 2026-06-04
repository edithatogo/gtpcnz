# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-054-A | `dag-registry` | Maintain at least eight structural DAG entries with edges, exclusions, weights and source basis. | models/primarycare_model/contracts/structural_models.py, models/primarycare_model/uncertainty/**, models/primarycare_model/registries/public/structural_models.public.v1.yaml, docs/model/structural-uncertainty-v1.md, docs/diagrams/structural-ensemble.mmd, models/tests/test_structural_ensemble.py | Gates pass or blocker logged. |
| WP-054-B | `ensemble-runner` | Report structural intervals as assumption sensitivity only. | models/primarycare_model/contracts/structural_models.py, models/primarycare_model/uncertainty/**, models/primarycare_model/registries/public/structural_models.public.v1.yaml, docs/model/structural-uncertainty-v1.md, docs/diagrams/structural-ensemble.mmd, models/tests/test_structural_ensemble.py | Gates pass or blocker logged. |
| WP-054-C | `diagram-docs` | Keep Mermaid DAG docs aligned with registry structures. | models/primarycare_model/contracts/structural_models.py, models/primarycare_model/uncertainty/**, models/primarycare_model/registries/public/structural_models.public.v1.yaml, docs/model/structural-uncertainty-v1.md, docs/diagrams/structural-ensemble.mmd, models/tests/test_structural_ensemble.py | Gates pass or blocker logged. |
| WP-054-D | `uncertainty-tests` | Test required models, interval shape, and claim-boundary labels. | models/primarycare_model/contracts/structural_models.py, models/primarycare_model/uncertainty/**, models/primarycare_model/registries/public/structural_models.public.v1.yaml, docs/model/structural-uncertainty-v1.md, docs/diagrams/structural-ensemble.mmd, models/tests/test_structural_ensemble.py | Gates pass or blocker logged. |

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
