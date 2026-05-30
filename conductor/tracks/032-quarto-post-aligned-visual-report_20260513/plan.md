# Plan: Quarto Post-Aligned Visual Report

Status: Complete.

## Phase 1: Structure and Anchors

1. Add the post reading map near the top of the report.
2. Add or normalize anchors/headings for the first six posts.
3. Cross-link to Streamlit modules and GitHub Pages where static links are available.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 2: Static Visual Essay

1. Add conceptual visuals before results.
2. Add microeconomics diagrams with plain-language axis labels.
3. Add game-theory diagrams for payoff, best response, controls and gaming risk.
4. Add captions, status labels and caveats.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 3: Scenario and Evidence Visuals

1. Keep F0/current reform visible as comparator.
2. Add or refine static scenario plots using model-generated index wording.
3. Add evidence and calibration status visuals where required by Track 029.
4. Confirm no precise fiscal, hospital-demand, workforce or implementation claims are introduced.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Validation

```powershell
quarto render --to html
rg -n "How the posts map|Why formulas do not solve games|model-generated index|current reform|payoff|best response|marginal|co-payment" reports/primary_care_architecture.qmd
```

## Review Evidence

- 2026-05-13 setup-phase review: track registered and cross-referenced to Track 029 and the post-surface crosswalk contract.
- Metadata validation passed with `python -m json.tool`.
- Findings: no high-severity setup findings. Implementation was pending at setup time; the later 2026-05-13 implementation pass below records the delivered Quarto updates, while Track 036 release closeout remains pending.
- 2026-05-13 implementation pass: public Quarto report updated in `public/gtpcnz/reports/primary_care_architecture.qmd` with a post-to-report/dashboard map, stable post anchors, explicit Post 04 game-theory section, two static game-theory diagrams, microeconomics diagrams, status labels and model-generated index wording.
- Scoped validation passed: `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz` included `models/tests/test_quarto_post_crosswalk.py`.
- Quarto validation passed after clearing opencode/kilo caches, npm cache and old temp files to resolve local disk pressure: `quarto render --to html` completed in `public/gtpcnz` and produced `_site/index.html`.
- Review result: no high-severity content findings found in the scoped implementation review.
