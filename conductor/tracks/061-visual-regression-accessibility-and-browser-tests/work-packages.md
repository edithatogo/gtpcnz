# Work Packages

Recommended Cline model: DeepSeek v4 Flash.

Parallelism policy:

- Run these packages in parallel only if their files do not overlap.
- Keep each package to one subagent and one level of delegation.
- Escalate to the coordinator for any cross-track edit.

| Work package | Subagent role | Task | Allowed files | Stop condition |
|---|---|---|---|---|
| WP-061-A | `browser-smoke` | Confirm core cockpit sections render when browser runtime is available. | tests/browser/**, scripts/run_visual_regression.py, scripts/run_accessibility_audit.py, docs/testing/visual-regression-and-accessibility-v1.md | Gates pass or blocker logged. |
| WP-061-B | `visual-baseline` | Require approval for visual snapshot changes. | tests/browser/**, scripts/run_visual_regression.py, scripts/run_accessibility_audit.py, docs/testing/visual-regression-and-accessibility-v1.md | Gates pass or blocker logged. |
| WP-061-C | `a11y-audit` | Check headings, labels, table fallbacks, contrast warnings and non-colour-only encoding. | tests/browser/**, scripts/run_visual_regression.py, scripts/run_accessibility_audit.py, docs/testing/visual-regression-and-accessibility-v1.md | Gates pass or blocker logged. |
| WP-061-D | `browser-docs` | Document when browser/runtime blockers make gates advisory rather than complete. | tests/browser/**, scripts/run_visual_regression.py, scripts/run_accessibility_audit.py, docs/testing/visual-regression-and-accessibility-v1.md | Gates pass or blocker logged. |

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
