# Plan: Streamlit Post-Aligned Interactive Labs

Status: Complete.

## Phase 1: Post Guide

1. Add a visible reading-map tab or page.
2. Map posts 01-06 to dashboard modules and Quarto report destinations.
3. Add links to the report, GitHub Pages and model card where appropriate.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 2: Microeconomics Lab

1. Add marginal supply simulation.
2. Add co-payment/access barrier simulation.
3. Add capitation or budget-constraint explanation.
4. Add plain-language definitions and caveats for each slider.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 3: Game Theory Lab

1. Add payoff/best-response module.
2. Add gaming-risk frontier or controls-stack simulation.
3. Connect the module to Post 04 and later game-theory appendix themes.
4. Label simulations as toy teaching modules.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 4: Scenario Integration

1. Keep reference scenario plots separate from toy simulations.
2. Add F0/current reform comparator selectors where relevant.
3. Ensure all outputs use model-generated index wording.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Validation

```powershell
python -m py_compile streamlit_app.py models/primarycare_model/app.py models/primarycare_model/scenario_service.py
pytest -q models/tests
rg -n "Post guide|Reading map|Microeconomics lab|Game theory lab|model-generated index|toy teaching|F0|current reform" models/primarycare_model/app.py models/tests
```

## Review Evidence

- 2026-05-13 setup-phase review: track registered and cross-referenced to Track 029 and the post-surface crosswalk contract.
- Metadata validation passed with `python -m json.tool`.
- Findings: no high-severity setup findings. Implementation was pending at setup time; the later 2026-05-13 implementation pass below records the delivered Streamlit updates, while Track 036 release closeout remains pending.
- 2026-05-13 implementation pass: `public/gtpcnz/models/primarycare_model/app.py` updated with a visible Post guide / Reading map, Microeconomics lab, Game theory lab, page-local sliders, two microeconomics simulations, two game-theory simulations, and explicit "what this shows / how to read / what it does not prove" notes.
- Scoped validation passed: `pytest -q -p no:cacheprovider models/tests` in `public/gtpcnz` included `models/tests/test_streamlit_post_labs.py` and the existing Streamlit smoke tests.
- Python syntax validation passed by compiling `streamlit_app.py`, `models/primarycare_model/app.py` and `models/primarycare_model/scenario_service.py` to an external writable pycompile target because OneDrive denied local `__pycache__` writes.
- Review result: no high-severity findings found in the scoped implementation review.
