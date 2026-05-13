# Post-to-surface crosswalk contract v1.8.2

## Purpose

The public model surfaces must work as companions to the public post sequence. A reader should be able to start from any post and know where the same idea is explained in the Quarto report, Streamlit dashboard and GitHub Pages site.

This public copy governs the deployed `gtpcnz` repository. It may reference post titles and reading-guide labels, but it must stay free of private working drafts.

## Required public reading map

Each public surface must expose, or link to, a reading map with:

- post ID and public title;
- reader question;
- Quarto section;
- Streamlit page, tab or module;
- GitHub Pages card or gallery item;
- static visual;
- dynamic visual, toy module or simulation;
- status label and caveat.

## First-six post crosswalk

| Post | Public title | Quarto destination | Streamlit destination | Required static visual | Required dynamic visual |
|---|---|---|---|---|---|
| 01 | Are we buying hospital growth by rationing cheaper care upstream? | Executive summary; hospital spillover pathway; scenario interpretation | Start here; Current state; Reference scenarios | One patient, three pathways; hospital spillover flow | Supply versus hospital-pressure scenario plot |
| 02 | Fee-for-service, capitation and blended funding | Funding model explainer; formula appendix | Funding models module; Toy explainer | Who bears the cost; capitation versus scheduled activity diagram | Funding comparison toy module |
| 03 | Marginal supply | Microeconomics section | Microeconomics lab | Marginal revenue versus marginal cost diagram | Slider-driven marginal supply simulation |
| 04 | Why formulas do not solve games | Game theory section; controls section | Game theory lab | Payoff matrix; best-response or controls-stack diagram | Toy incentive game, gaming-risk frontier or best-response simulation |
| 05 | Current reform pathway | Current reform comparator section | Current state; Reference scenarios | Current reform pathway map | F0/current reform versus selected scenario comparison |
| 06 | What I mean by uncapping primary care funding | Controlled scheduled payment section | Toy explainer; Microeconomics lab | Scheduled payment with controls; controls stack | Activity/payment/control toy simulation |

## Game-theory extension

Later game-theory appendices or long-form posts referenced by the public report or dashboard must have corresponding public companion modules.

| Theme | Quarto requirement | Streamlit requirement | Required visual set |
|---|---|---|---|
| Hospital salience and allocation game | Static game narrative and payoff/attention diagram | Allocation-priority toy simulation or guided explanation | Static payoff/priority map plus dynamic priority slider |
| Capitation marginal-supply game | Static best-response explanation | Marginal supply simulation | MR/MC diagram plus dynamic gap plot |
| PHO function/friction/cherry-picking | Place accountability section | Gaming-risk frontier module | Cherry-picking decision tree plus dynamic risk frontier |
| ACC, ambulance and urgent care | Spillover and boundary section | Pathway stress module | System boundary flow plus pathway stress chart |
| Co-payments and equity | Equity and access section | Co-payment barrier module | Demand/access barrier diagram plus dynamic access-risk plot |
| The 19 games map | Summary game map appendix | Game map navigator | Static map plus guided dynamic stepper |
| Hybrid game | Why no single lever is enough | Scenario profile module | Controls stack plus dynamic scenario profile |
| Game-informed MCDA | Decision support section | MCDA explainer module, if included | Criteria matrix plus optional weighting toy |

## Surface rules

- GitHub Pages must show visual reading-map cards before document-link lists.
- Quarto must include a "How the posts map to this report and dashboard" section near the top.
- Streamlit must include a visible "Post guide" or "Reading map" page/tab.
- Game-theory modules must be labelled as toy teaching simulations, not estimates.
- Microeconomics diagrams must use plain-language labels and avoid unexplained shorthand.
- Scenario plots must use "model-generated index" wording.
- F0/current reform must remain the comparator.
- The full model caveat must remain visible on entry surfaces and any toy/simulation page.
