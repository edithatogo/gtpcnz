# Plan: Visual Contract and Public Visual Narrative

Status: Complete.

## Phase 1: Contract and inventory

1. Record the visual contract matrix in this track.
2. Inventory current figures across Quarto, GitHub Pages and Streamlit.
3. Identify which current visuals can be reused, which need redesign, and which are missing.
4. Map public posts/themes to report sections and Streamlit tabs/pages.
5. Apply Track 030 workflows for diagram production, alt text, captions, thumbnails, tables and hyperlinks.
6. Add `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md` as the binding post-by-post crosswalk.
7. Register child tracks 031-036 as the implementation plan for this umbrella contract.

Review gate: after this phase, run `$conductor-review` for Track 029, apply safe in-scope fixes, rerun document validation, and only then progress to child-track implementation.

## Phase 2: GitHub Pages landing page

1. Replace the directory-like homepage with a public visual landing page.
2. Add visual preview cards for:
   - public argument map;
   - current reform pathway;
   - scenario rank chart;
   - evidence tracker status;
   - calibration readiness.
3. Keep direct links to the report, dashboard, model card, claim boundaries, evidence tracker and calibration page.
4. Add a clear Streamlit callout for `https://gtpcnz.streamlit.app/`.
5. Add a "visual reading path" that mirrors the public post sequence.
6. Put the caveat and two primary actions above the fold: read report and open dashboard.

## Phase 3: Quarto report visuals

1. Add conceptual diagrams before scenario outputs:
   - marginal payment gap;
   - scheduled activity payment with controls;
   - hospital spillover flow.
2. Add static scenario plots:
   - scenario rank bar chart;
   - scenario score heatmap;
   - F0 vs F4 comparison;
   - risk-return scatter if space allows.
3. Add captions with status labels and claim boundaries.
4. If dynamic Quarto visuals are used, add static fallbacks for PDF and accessibility.
5. Structure the report as a guided visual essay: visual first, explanation second, table third.
6. Put evidence and calibration visuals near the end as the transition from public explanation to next work.

## Phase 4: Streamlit interactive visual layer

1. Align tabs/pages with public post themes.
2. Add a visible post-alignment guide.
3. Add dynamic microeconomics visuals:
   - marginal payment gap;
   - co-payment barrier;
   - controls/gaming-risk frontier.
4. Add model-index plots:
   - F0 vs selected scenario;
   - risk-return scatter;
   - scenario small multiples or profile cards.
5. Add evidence and calibration status visuals:
   - evidence tracker status chart;
   - calibration readiness heatmap.
6. Add a choose-your-path opening panel for overview, current pathway, economics, scenarios and evidence.
7. Prefer page-local sliders beside the visual they affect rather than relying only on the global sidebar.
8. Default scenario comparisons to F0/current reform pathway versus the selected alternative.
9. Put status visuals before tables on evidence and calibration pages.

## Phase 5: Tests and documentation

1. Update dashboard contract and audit docs to reference Track 029.
2. Add tests for:
   - required visual contract entries;
   - Quarto render targets;
   - Streamlit diagram/plot labels;
   - model caveat preservation;
   - static/dynamic visual inventory completeness.
3. Run:

```bash
python -m compileall models
pytest -q
quarto render --to html
python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py
```

## Phase 6: Release

1. Commit the public visual implementation in the public `gtpcnz` submodule.
2. Push public `gtpcnz` main.
3. Verify GitHub CI and Quarto Pages deployment.
4. Verify `https://edithatogo.github.io/gtpcnz/`.
5. Verify `https://gtpcnz.streamlit.app/`.
6. Commit the updated submodule pointer in the parent repository.

## Implementation notes

- Use static visuals first where the message must be stable.
- Use dynamic visuals only where interaction teaches something a static chart cannot.
- Keep all visuals general-audience readable.
- Prefer simple labels over economics shorthand.
- Keep the formal caveat unchanged.
- Do not expand claims beyond the model-generated index boundary.
- Treat Track 029 as the umbrella contract. Granular implementation belongs to Tracks 031-036.
- Optimise execution for subagents by assigning disjoint write scopes:
  - Track 031 owns crosswalk contracts and tests.
  - Track 032 owns Quarto report sections and Quarto-specific tests.
  - Track 033 owns Streamlit app modules and dashboard-specific tests.
  - Track 034 owns GitHub Pages homepage/gallery and site navigation tests.
  - Track 035 owns shared game-theory and microeconomics visual/simulation specifications.
  - Track 036 owns integrated validation, review closeout, deployment proof and release evidence.
- At the end of every child-track phase, run `$conductor-review`, apply safe fixes, rerun validation and record the evidence before progressing.

## Review evidence

- 2026-05-13 setup-phase review: checked Track 029/031-036 registration against `conductor/product-guidelines.md`, `conductor/tech-stack.md` and `conductor/workflow.md`.
- Scoped validation passed: `rg -n "post-surface-crosswalk|Post 04|Game theory lab|Microeconomics lab|031|032|033|034|035|036|conductor-review|Review gate" ...`.
- Metadata validation passed for Tracks 031-036 using `python -m json.tool`.
- Findings: no high-severity findings in the contract/track setup. Implementation was pending at setup time; the later implementation passes for Tracks 032-035 are now recorded in their plans, while Track 036 closeout remains pending.
