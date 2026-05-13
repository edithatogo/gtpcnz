# Game-Theory and Microeconomics Simulation Spec v1.8.2

## Purpose

This document defines the reusable public module contract for Track 035. It gives Track 032 a stable static-visual spec and Track 033 a stable Streamlit simulation spec without forcing either track to invent labels, formulas, or wording on the fly.

The same module definitions apply across the public site, the Quarto report, the Streamlit dashboard, and the GitHub Pages reading map.

## Shared module contract

Every module in this layer must define:

- `reader_question`: one plain-English question the reader can answer by using the module.
- `target_posts`: the public posts or appendices that should reuse the module.
- `target_surfaces`: the public surfaces that must carry the same labels and caveats.
- `static_visual`: the Quarto or rendered conceptual visual used as the fixed explainer.
- `dynamic_streamlit`: the Streamlit module or toy simulation used for guided exploration.
- `inputs`: the minimal set of sliders, selectors, or toggles the user needs.
- `outputs`: the values, labels, or narrative results the module returns.
- `formula_sketch`: a short, readable formula or relationship sketch.
- `caveat`: the limit of what the module can and cannot show.
- `status_label`: the required status label for the static and dynamic pieces.
- `accessibility_notes`: the baseline accessibility rules for the module.
- `tests_to_be_added_by_track_033`: the validation checks Track 033 must add.

Shared labeling rules:

- Use `conceptual explainer` for hand-authored static diagrams.
- Use `toy teaching simulation` for interactive modules that are explanatory rather than empirical.
- Use `model-generated index` only for scenario outputs that come from the model layer.
- Do not label a toy module as a forecast, prediction, estimate, effect, saving, or demand reduction.
- Default slider scales to `0 = absent or weak` and `100 = strong or reliably implemented` unless the module explicitly says otherwise.

## Microeconomics modules

| Module | Reader question | Target posts | Target surfaces | Static visual | Dynamic Streamlit simulation | Inputs | Outputs | Formula sketch | Caveat / status label | Accessibility notes | Tests to be added by Track 033 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Marginal revenue versus marginal cost | When does one more consult stop being worth it? | Post 03 `Marginal supply`; Post 06 `What I mean by uncapping primary care funding` | Quarto microeconomics section; Streamlit microeconomics lab; GitHub Pages reading-map card | MR/MC crossing diagram with a shaded viable zone | Slider-driven marginal-supply explorer that shifts MR and MC curves | Payment per unit; marginal cost slope; fixed cost; demand pressure | Viable quantity band; break-even point; gap size | `viable if MR(q) >= MC(q)` and `q*` where `MR(q) = MC(q)` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not an estimate of real demand | Label axes in words; add keyboard step sizes; provide a text summary of the crossing point | Schema test for required fields; label test for MR/MC wording; no forecast or savings wording; alt-text check |
| Capitation budget constraint | Why can a fair per-patient budget still feel tight when demand rises? | Post 02 `Fee-for-service, capitation and blended funding`; Post 03 `Marginal supply`; Post 06 `What I mean by uncapping primary care funding` | Quarto funding-model section; Streamlit toy explainer page; GitHub Pages reading-map card | Enrolled-patient budget box with a demand path overlay | Capitation budget simulator that shows pressure as enrolment and demand change | Enrolled patients; capitation rate; expected cost; demand growth | Budget; shortfall or surplus; pressure flag | `budget = enrolled_patients * capitation_rate`; `headroom = budget - expected_cost` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; shows budget pressure only | Use plain-language axes; show a numeric budget summary; do not rely on colour alone | Schema test for field presence; sum check for budget arithmetic; no causal claim wording; keyboard control check |
| Scheduled payment with controls | How can payment be uncapped without losing control? | Post 02 `Fee-for-service, capitation and blended funding`; Post 06 `What I mean by uncapping primary care funding` | Quarto controlled-payment section; Streamlit microeconomics lab; GitHub Pages card | Controls-stack diagram layered over activity payment | Activity-payment-control toy simulation with toggles for audit and rule strength | Activity volume; activity rate; rule strength; audit strength; place-accountability strength | Gross payment; control adjustment; net incentive score | `payment = base + rate * units - control_penalty` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not a claim that uncapping means no controls | Use separate labels for each control; add a textual explanation of how the stack changes payment | Schema test for required control fields; label test for "uncapped but controlled"; no estimate wording; mobile layout check |
| Co-payment / access barrier | When does a co-payment become an access barrier? | Post 02 `Fee-for-service, capitation and blended funding`; co-payment appendix or later equity post | Quarto equity section; Streamlit access-barrier module; GitHub Pages card | Demand curve shifted by out-of-pocket cost | Access-barrier toy simulation that shows how uptake changes with cost | Co-payment; income proxy; urgency; travel burden | Expected access rate; barrier score; equity flag | `effective_price = copay + other_burden`; `utilization = f(need, income, effective_price)` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not an equity-effect estimate | Use plain-language axis titles; add a text summary for the highest-barrier case; keep colour choices accessible | Schema test for barrier fields; wording test for no causal-effect claim; accessibility test for contrast and keyboard use |
| Who bears the cost | Who pays in each funding design? | Post 02 `Fee-for-service, capitation and blended funding`; Post 06 `What I mean by uncapping primary care funding` | Quarto cost-sharing section; Streamlit comparison module; GitHub Pages card | Cost-share bar or stacked-bar chart across government, practice, and patient | Cost-sharing slider compare that shows how burden moves across actors | Government share; practice share; patient share; admin overhead | Cost shares; burden summary; warning if shares do not sum to 1 | `government + practice + patient = 1` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not a policy recommendation engine | Use direct text labels on every share; provide a tabular summary as well as the chart | Schema test for share totals; label test for actor names; no recommendation wording; screen-reader summary check |

## Game-theory modules

| Module | Reader question | Target posts | Target surfaces | Static visual | Dynamic Streamlit simulation | Inputs | Outputs | Formula sketch | Caveat / status label | Accessibility notes | Tests to be added by Track 033 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Formula does not solve game | Why does a formula still need a game-theory check? | Post 04 `Why formulas do not solve games`; 19-games intro or appendix | Quarto game-theory section; Streamlit game-theory lab; GitHub Pages reading-map card | Incentive loop or response diagram | Toy incentive game with choice and response sliders | Base payment; audit strength; gaming payoff; coordination cost | Chosen action; response shift; exploitability score | `U_i = benefit_i(action_i, action_-i, controls) - cost_i` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not a forecast of behaviour | Show each player's payoff in text; avoid colour-only signalling; provide a clear step-by-step explanation | Schema test for strategic fields; wording test for "formula does not solve" label; no forecast wording; keyboard interaction check |
| Provider/system payoff matrix | What happens when care generation and gaming each pay differently? | Post 04 `Why formulas do not solve games`; hospital-salience or allocation-game appendix | Quarto payoff section; Streamlit payoff-matrix explorer; GitHub Pages card | 2x2 payoff matrix with care and gaming outcomes | Payoff-matrix explorer that shows how values shift with controls | Care effort; gaming effort; monitoring intensity | Payoff cells; dominant-strategy hint; risk flag | `payoff = care_value + gaming_return - control_cost` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not an observed outcome table | Add matrix captions; support keyboard navigation; keep numeric labels visible | Schema test for matrix fields; label test for payoff cells; no empirical-effect wording; accessibility check |
| Best-response or controls-stack diagram | Which controls change the best response? | Post 04 `Why formulas do not solve games`; hybrid-game appendix; PHO / cherry-picking theme | Quarto controls section; Streamlit controls-stack module; GitHub Pages card | Controls stack layered over a decision tree or best-response map | Controls-stack simulator that shows best-response shifts | Audit; item rules; place accountability; exception handling | Best-response shift; residual gaming zone; control-strength index | `best_response_i = argmax U_i(action_i, action_-i, controls)` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not a policy effectiveness estimate | Describe each control in words; keep symbols secondary; add a plain-language summary for the active control mix | Schema test for control fields; ordering test for stack labels; no effect-size wording; focus-state check |
| Gaming-risk frontier | How much gaming risk remains as access expands? | Post 04 `Why formulas do not solve games`; PHO / cherry-picking appendix; hybrid-game appendix | Quarto trade-off section; Streamlit risk-frontier module; GitHub Pages card | Frontier curve or two-axis trade-off plot | Risk-frontier slider that moves along the access-control trade-off | Access gain; control strength; monitoring cost; provider response | Frontier point; risk band; access-gain score | `risk = g(access_gain, control_strength, monitoring_cost)` | Static: `conceptual explainer`; dynamic: `toy teaching simulation`; not a measured frontier | Use full-word axis titles; include a text summary of the chosen point; avoid colour-only risk zones | Schema test for frontier fields; wording test for no forecast/reduction claim; axis-label accessibility check |
| 19-games navigator or stepper | How do the different strategic games fit together? | 19-games map appendix; later game-theory extension posts | Quarto map appendix; Streamlit navigator page; GitHub Pages reading-map card | Game map or card grid | Stepper / navigator that moves between named game modules | Selected game; theme; control family; reading depth | Current game card; related posts; related module links | `selected_state = f(game, theme, control_family)` | Static: `conceptual explainer`; dynamic: `toy teaching simulation` for navigation only; not a simulation of outcomes | Make keyboard stepper controls visible; include a short summary for each card; show focus state | Schema test for navigator fields; link-target test for every card; accessibility test for keyboard navigation |

## Shared validation contract

Track 033 should add tests that verify the following across all modules:

- Every module has the required fields listed in the shared module contract.
- Every module has one clear reader question and one stable target-post mapping.
- Static visuals use the required conceptual or toy labels instead of outcome language.
- Dynamic modules are labelled as toy teaching simulations unless they are later promoted to model-generated indices.
- No module claims to forecast, predict, estimate, or quantify an empirical effect unless the model layer has been separately validated.
- Every module includes a readable formula sketch and a plain-language caveat.
- Every module includes accessibility notes for keyboard use, text summaries, and non-colour-dependent labels.

