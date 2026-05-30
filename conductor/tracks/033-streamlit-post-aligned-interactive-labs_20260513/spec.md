# Spec: Streamlit Post-Aligned Interactive Labs

**Status:** Complete

## Problem

The Streamlit dashboard has dynamic charts, but it does not yet show a visible post guide or dedicated game-theory and microeconomics labs. The toy parameters still need clearer page-local explanations for general readers.

## Goal

Implement a Streamlit dashboard that acts as the interactive companion to the post sequence.

## Owned Files

Primary:

- `models/primarycare_model/app.py`
- `models/primarycare_model/scenario_service.py` if shared scenario outputs need new helpers
- `streamlit_app.py` only if entrypoint wiring changes
- public repo equivalents under `public/gtpcnz/`

Tests:

- dashboard claim wording tests
- Streamlit compile/smoke tests
- visual contract tests

## Requirements

1. Add a visible "Post guide" or "Reading map" tab/page.
2. Add a Microeconomics lab covering marginal supply, capitation budget constraint, scheduled activity payment and co-payment barrier.
3. Add a Game theory lab covering formulas-do-not-solve-games, payoff/best-response logic, controls and gaming-risk frontier.
4. Include at least two dynamic microeconomics simulations.
5. Include at least two dynamic game-theory or strategic-behaviour simulations.
6. Put "what this shows", "how to read it" and "what it does not prove" near each interactive module.
7. Prefer page-local sliders beside the affected visual.
8. Keep reference scenarios separate from toy slider settings.
9. Default scenario comparisons to F0/current reform.
10. Preserve the full model caveat and model-generated index wording.

## Parallelisation

This track can run in parallel with Track 032 and Track 034 after Track 035 defines simulation formulas and labels.

Suggested subagent split:

- Worker A owns the post guide tab/page and navigation labels.
- Worker B owns the Microeconomics lab.
- Worker C owns the Game theory lab.
- Worker D owns tests and smoke validation.

Workers must not edit Quarto report files or GitHub Pages homepage files.

## Acceptance Criteria

1. Dashboard contains a post guide or reading map.
2. Dashboard contains Microeconomics lab content and dynamic simulations.
3. Dashboard contains Game theory lab content and dynamic simulations.
4. Dashboard contains at least three conceptual/microeconomics visuals and at least four dynamic plots/simulations.
5. Tests verify required labels, caveats and crosswalk terms.
6. `python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py` passes.
7. `$conductor-review` has been run and high-severity findings have been fixed or explicitly blocked.