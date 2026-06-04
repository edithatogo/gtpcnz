# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-058-A | `scope-decision` | State whether AU is first-class or comparative context only. | docs/decisions/australia-scope-decision-v1.md, models/primarycare_model/registries/public/jurisdictions.public.v1.yaml, models/tests/test_jurisdiction_claims.py, README.md | Gates pass or blocker logged. |
| WP-058-B | `jurisdiction-registry` | Register jurisdiction status and claim boundary. | docs/decisions/australia-scope-decision-v1.md, models/primarycare_model/registries/public/jurisdictions.public.v1.yaml, models/tests/test_jurisdiction_claims.py, README.md | Gates pass or blocker logged. |
| WP-058-C | `unsupported-claim-scan` | Remove or downgrade unsupported Australia model claims. | docs/decisions/australia-scope-decision-v1.md, models/primarycare_model/registries/public/jurisdictions.public.v1.yaml, models/tests/test_jurisdiction_claims.py, README.md | Gates pass or blocker logged. |
| WP-058-D | `scope-tests` | Test AU comparative-only status unless AU-specific public artefacts exist. | docs/decisions/australia-scope-decision-v1.md, models/primarycare_model/registries/public/jurisdictions.public.v1.yaml, models/tests/test_jurisdiction_claims.py, README.md | Gates pass or blocker logged. |

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
