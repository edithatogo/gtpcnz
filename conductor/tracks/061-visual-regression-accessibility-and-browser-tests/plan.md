# Plan

Execution wave: `3`.

Depends on:
- `056-streamlit-policy-cockpit-and-visual-grammar`

Blocks:
- `059-release-engineering-and-model-cards`

Safe parallel tracks:
- `057-quarto-scientific-report-rebuild`

Work packages:

| Work package | Subagent role | Task | Contract | Required gate |
|---|---|---|---|---|
| WP-061-A | `browser-smoke` | Confirm core cockpit sections render when browser runtime is available. | CON-VIS-001 | python scripts/run_visual_regression.py --check-only, python scripts/run_accessibility_audit.py --check-only |
| WP-061-B | `visual-baseline` | Require approval for visual snapshot changes. | CON-VIS-001 | python scripts/run_visual_regression.py --check-only, python scripts/run_accessibility_audit.py --check-only |
| WP-061-C | `a11y-audit` | Check headings, labels, table fallbacks, contrast warnings and non-colour-only encoding. | CON-VIS-001 | python scripts/run_visual_regression.py --check-only, python scripts/run_accessibility_audit.py --check-only |
| WP-061-D | `browser-docs` | Document when browser/runtime blockers make gates advisory rather than complete. | CON-VIS-001 | python scripts/run_visual_regression.py --check-only, python scripts/run_accessibility_audit.py --check-only |

Completion sequence:

1. Confirm dependencies have passed their gates.
2. Assign work packages only within the allowed file globs.
3. Run every required gate listed in `acceptance.md`.
4. Update `implementation-log.md` with files changed, commands run, residual blockers, and claim-boundary status.
5. Run `python scripts/check_conductor_parallel_tracks.py` before marking the track ready for release-wave coordination.
