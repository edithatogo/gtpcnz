# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-060-A | `candidate-contract` | Create candidate records with relevance, quality, transferability, contradiction and affected parameters. | models/primarycare_model/evidence/**, models/primarycare_model/contracts/evidence_candidates.py, scripts/monitor_public_evidence.py, docs/evidence/public-evidence-monitoring-v1.md, models/tests/test_public_evidence_monitor.py | Gates pass or blocker logged. |
| WP-060-B | `monitor-runner` | Detect public-source update candidates without mutating registries. | models/primarycare_model/evidence/**, models/primarycare_model/contracts/evidence_candidates.py, scripts/monitor_public_evidence.py, docs/evidence/public-evidence-monitoring-v1.md, models/tests/test_public_evidence_monitor.py | Gates pass or blocker logged. |
| WP-060-C | `review-gate` | Force `review_required=true` and `may_update_model=false`. | models/primarycare_model/evidence/**, models/primarycare_model/contracts/evidence_candidates.py, scripts/monitor_public_evidence.py, docs/evidence/public-evidence-monitoring-v1.md, models/tests/test_public_evidence_monitor.py | Gates pass or blocker logged. |
| WP-060-D | `monitor-tests` | Prove no candidate can alter parameters, outputs or claims. | models/primarycare_model/evidence/**, models/primarycare_model/contracts/evidence_candidates.py, scripts/monitor_public_evidence.py, docs/evidence/public-evidence-monitoring-v1.md, models/tests/test_public_evidence_monitor.py | Gates pass or blocker logged. |

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
