# Plan: Game-Theory and Microeconomics Simulation Layer

Status: Complete.

## Phase 1: Microeconomics Specs

1. Define marginal supply module.
2. Define capitation budget-constraint module.
3. Define scheduled payment with controls module.
4. Define co-payment/access barrier module.
5. Define who-bears-the-cost module.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 2: Game-Theory Specs

1. Define payoff matrix module.
2. Define best-response or controls-stack module.
3. Define gaming-risk frontier module.
4. Define 19-games navigator or stepper module.
5. Cross-reference Post 04 and later game-theory extension rows.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Phase 3: Testable Schema

1. Define shared labels, caveats and output names.
2. Define toy-input and toy-output schema expectations.
3. Define tests that Track 033 can use to prevent overclaiming.

Review gate: run scoped checks, run `$conductor-review`, apply safe fixes, rerun checks.

## Validation

```powershell
rg -n "marginal|capitation|scheduled payment|co-payment|payoff|best response|gaming-risk|toy teaching simulation|model-generated index" docs/public-site conductor/tracks/035-game-theory-microeconomics-simulation-layer_20260513
```

## Review Evidence

- 2026-05-13 setup-phase review: track registered and cross-referenced to Track 029 and the post-surface crosswalk contract.
- Metadata validation passed with `python -m json.tool`.
- Findings: no high-severity setup findings. Implementation was pending at setup time; the later 2026-05-13 implementation pass below records the delivered simulation-spec updates, while Track 036 release closeout remains pending.
- 2026-05-13 implementation pass: added `docs/public-site/game-theory-microeconomics-simulation-spec-v1.8.2.md` and mirrored it into `public/gtpcnz/docs/public-site/game-theory-microeconomics-simulation-spec-v1.8.2.md`.
- Spec now defines five microeconomics modules and five game-theory modules with reader question, target posts, target surfaces, static visual, dynamic simulation, inputs, outputs, formula sketch, caveat/status label, accessibility notes and Track 033 test expectations.
- Scoped validation passed by `rg` checks over the two spec files and this plan.
- Review result: no high-severity findings found in the scoped implementation review.
- 2026-05-13 spec-update review: added reusable microeconomics and game-theory module specs to the public-site spec and mirrored copy for the allowed Track 035 surfaces.
- Scoped validation: `rg -n "reader_question|target_posts|target_surfaces|static_visual|dynamic_streamlit|formula_sketch|caveat|status_label|accessibility_notes|tests_to_be_added_by_track_033" docs/public-site/game-theory-microeconomics-simulation-spec-v1.8.2.md public/gtpcnz/docs/public-site/game-theory-microeconomics-simulation-spec-v1.8.2.md conductor/tracks/035-game-theory-microeconomics-simulation-layer_20260513/plan.md` found the expected module-contract fields in both spec files and this plan.
