# Spec: Game-Theory and Microeconomics Simulation Layer

## Problem

The current public dashboard/report explain scenarios but do not yet provide enough intuitive game-theory or microeconomics visuals. The parameters also need plain-language meaning before they can be used in dynamic teaching modules.

## Goal

Define the reusable visual and toy-simulation layer that Quarto and Streamlit implement.

## Owned Files

Primary:

- visual/simulation specification docs under `docs/public-site/`;
- shared helper functions under `models/primarycare_model/` if implementation needs reusable formulas;
- tests that validate formula labels, caveats and output schemas.

Implementation consumers:

- Track 032 implements static Quarto visuals.
- Track 033 implements dynamic Streamlit labs.
- Track 034 previews selected visuals on GitHub Pages.

## Required Microeconomics Modules

1. Marginal revenue versus marginal cost: explains why extra activity may not be viable under fixed or weak marginal payment.
2. Capitation budget constraint: explains baseline fairness versus rising demand.
3. Scheduled activity payment with controls: explains uncapped but controlled activity payment.
4. Co-payment/access barrier: explains equity risk when costs shift to patients.
5. Who bears the cost: compares government, practice and patient cost-bearing under funding designs.

## Required Game-Theory Modules

1. Formula does not solve game: shows how actors respond to incentives and constraints.
2. Provider/system payoff matrix: illustrates viable care generation versus gaming risk.
3. Best-response or controls-stack diagram: shows how audit, item rules and place accountability change incentives.
4. Gaming-risk frontier: shows toy trade-off between access expansion and gaming/fiscal risk.
5. 19-games navigator or stepper: guides readers through the strategic map without overwhelming them.

## Labelling Rules

- Use "toy teaching simulation" for dynamic modules that are not scenario outputs.
- Use "conceptual explainer" for hand-authored diagrams.
- Use "model-generated index" for scenario outputs only.
- Do not label toy outputs as forecasts, predictions, effects, savings or demand reductions.
- Define each slider as 0 = absent/weak and 100 = strong/reliably implemented unless a module explicitly uses another scale with explanation.

## Parallelisation

This track is a sidecar design/specification track and should run before or beside Track 032/033 implementation.

Suggested subagent split:

- Subagent A designs microeconomics module specs and labels.
- Subagent B designs game-theory module specs and labels.
- Subagent C designs testable schema expectations for toy modules.

No subagent should edit public deployment files in this track unless promoted to Track 032 or 033 implementation.

## Acceptance Criteria

1. A reusable visual/simulation spec exists for each required microeconomics module.
2. A reusable visual/simulation spec exists for each required game-theory module.
3. Each module has plain-language reader question, inputs, output, chart type, caveat and target surfaces.
4. Track 032 and Track 033 can implement from this spec without inventing labels or formulas ad hoc.
5. `$conductor-review` has been run and high-severity findings have been fixed or explicitly blocked.
