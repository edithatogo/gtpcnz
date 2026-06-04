# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-051-A | `ontology-contract` | Expand strict parameter fields, distributions, bounds, formula refs, and claim-boundary metadata. | models/primarycare_model/contracts/public_parameters.py, models/primarycare_model/validation/public_parameter_loader.py, models/primarycare_model/registries/public/parameters.public.v1.yaml, scripts/check_parameter_traceability.py, models/tests/test_parameter_traceability.py, docs/model/public-parameter-ontology-v1.md | Gates pass or blocker logged. |
| WP-051-B | `loader-defaults` | Keep public runtime defaults loaded only from `registries/public/parameters.public.v1.yaml`. | models/primarycare_model/contracts/public_parameters.py, models/primarycare_model/validation/public_parameter_loader.py, models/primarycare_model/registries/public/parameters.public.v1.yaml, scripts/check_parameter_traceability.py, models/tests/test_parameter_traceability.py, docs/model/public-parameter-ontology-v1.md | Gates pass or blocker logged. |
| WP-051-C | `formula-trace` | Link every formula coefficient to a public parameter id and document gaps as not-ready. | models/primarycare_model/contracts/public_parameters.py, models/primarycare_model/validation/public_parameter_loader.py, models/primarycare_model/registries/public/parameters.public.v1.yaml, scripts/check_parameter_traceability.py, models/tests/test_parameter_traceability.py, docs/model/public-parameter-ontology-v1.md | Gates pass or blocker logged. |
| WP-051-D | `traceability-tests` | Add failing tests for any missing distribution, source, bound, or formula reference. | models/primarycare_model/contracts/public_parameters.py, models/primarycare_model/validation/public_parameter_loader.py, models/primarycare_model/registries/public/parameters.public.v1.yaml, scripts/check_parameter_traceability.py, models/tests/test_parameter_traceability.py, docs/model/public-parameter-ontology-v1.md | Gates pass or blocker logged. |

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
