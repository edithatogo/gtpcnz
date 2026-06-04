# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-055-A | `normative-net-benefit` | Keep weights editable and labelled as normative assumptions, not stakeholder preferences. | models/primarycare_model/voi/**, models/primarycare_model/contracts/voi.py, models/primarycare_model/registries/public/voi_parameter_groups.public.v1.yaml, scripts/run_voi.py, docs/model/value-of-information-methods-v1.md, models/tests/test_full_voi.py | Gates pass or blocker logged. |
| WP-055-B | `voi-metrics` | Implement EVPI, EVPPI, EVSI, ENBS, decision-error probability and rankings. | models/primarycare_model/voi/**, models/primarycare_model/contracts/voi.py, models/primarycare_model/registries/public/voi_parameter_groups.public.v1.yaml, scripts/run_voi.py, docs/model/value-of-information-methods-v1.md, models/tests/test_full_voi.py | Gates pass or blocker logged. |
| WP-055-C | `seeded-reproducibility` | Make stochastic VOI deterministic under a fixed seed. | models/primarycare_model/voi/**, models/primarycare_model/contracts/voi.py, models/primarycare_model/registries/public/voi_parameter_groups.public.v1.yaml, scripts/run_voi.py, docs/model/value-of-information-methods-v1.md, models/tests/test_full_voi.py | Gates pass or blocker logged. |
| WP-055-D | `voi-tests` | Test metric completeness, reproducibility, and `not a forecast` labelling. | models/primarycare_model/voi/**, models/primarycare_model/contracts/voi.py, models/primarycare_model/registries/public/voi_parameter_groups.public.v1.yaml, scripts/run_voi.py, docs/model/value-of-information-methods-v1.md, models/tests/test_full_voi.py | Gates pass or blocker logged. |

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
