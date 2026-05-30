# Spec: Visual Contract and Public Visual Narrative

**Status:** Complete

## Problem

The public site and dashboard are now safe, but they are still too text-heavy. A general reader should not have to infer the policy logic from tables and paragraphs. The public surfaces need a visual spine: conceptual microeconomics diagrams, static plots, dynamic explainer simulations and page structure that follows the same sequence as the public posts.

The current weakness is not only the number of figures. It is that the figures do not yet tell the argument in order.

## Goal

Create a visual contract that governs the Quarto report, GitHub Pages site and Streamlit dashboard.

The end state should let a general reader understand:

1. What the current reform pathway is.
2. Why capitation can be fair but still leave a marginal-supply gap.
3. What uncapped scheduled fee-for-service means.
4. Why controls, audit, co-payment protection and place accountability matter.
5. How the reference scenarios compare.
6. Why current outputs are model-generated indices, not observed New Zealand outcomes.
7. What evidence and calibration would be needed before real claims could be made.

## Audience

The visual layer is for a general reader: a journalist, clinician, policy staffer, patient advocate, public servant, student or interested member of the public.

Do not assume the reader understands:

- capitation;
- fee-for-service;
- marginal payment;
- supply response;
- co-payment barriers;
- hospital spillover;
- gaming risk;
- calibration;
- model-generated indices.

## General rules

- Every visual must have a plain-English title.
- Every model-derived visual must say whether it is conceptual, toy, model-generated or empirical.
- No visual may imply a calibrated fiscal, workforce, hospital-demand or implementation effect.
- The full model caveat must remain prominent on the public site and dashboard.
- Static Quarto visuals must have accessible captions.
- Dynamic Streamlit visuals must have a one-sentence "how to read this" note.
- Conceptual diagrams should use simple axes, arrows and labels rather than academic shorthand.
- The current reform pathway must remain the comparator, not a straw man.
- Substack content remains separately managed, but dashboard/report sections should align with the public post sequence.

## Quarto dynamic-image policy

Quarto can include dynamic visuals in HTML outputs, but the contract must distinguish static and dynamic uses.

Allowed dynamic Quarto options:

- Plotly figures rendered into the HTML report.
- Observable JS cells for lightweight interactive diagrams.
- HTML widgets or embedded JavaScript where dependency size is acceptable.
- Mermaid or Graphviz diagrams rendered as static or client-side diagrams.
- Embedded Streamlit links or screenshots, but not a full Streamlit runtime inside GitHub Pages.

Constraints:

- GitHub Pages is static hosting. Any dynamic Quarto visual must run client-side in the browser.
- PDF output needs static fallbacks or screenshots.
- Dynamic Quarto figures must not require private data, a server process or credentials.
- If a visual is essential to the argument, provide a static fallback image or static version in the report.

## Post-aligned page structure

Streamlit pages/tabs and the Quarto report should map to the public post sequence where possible. The post sequence is a reading path; the dashboard is the interactive companion.

The detailed post-by-post contract is now:

- `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md`

That contract is binding for implementation. The table below is the theme-level summary only.

| Post-aligned theme | Reader question | Quarto surface | Streamlit surface | Required visual mode |
|---|---|---|---|---|
| Start here / thesis | What is the argument? | Landing page summary and report executive summary | Start here tab | One-page visual map |
| Current reform pathway | What is New Zealand already doing? | Current reform section | Current state tab | Static pathway diagram plus table |
| Capitation and marginal supply | Why can fair allocation still constrain supply? | Microeconomics section | Toy microeconomics tab or section | Conceptual curve plus dynamic slider curve |
| Scheduled activity payment | What does uncapped scheduled FFS actually mean? | FFS explanation section | Toy explainer tab | Payment/activity diagram |
| Controls and gaming risk | Why does uncapped not mean uncontrolled? | Controls section | Toy explainer and reference scenarios | Decision tree or risk frontier |
| Equity and co-payments | Who could lose access if price shifts to patients? | Equity note and readiness section | Toy explainer and calibration readiness | Co-payment barrier diagram |
| Place accountability | How do we avoid cherry-picking? | Place accountability section | Current state / toy explainer | Population-responsibility diagram |
| Hospital spillover | How could unmet primary care become ED/ambulance pressure? | Scenario interpretation section | Reference scenarios | Flow diagram plus model-index plot |
| Reference scenarios | How do the model-generated scenarios compare? | Results section | Reference scenarios tab | Static and dynamic plots |
| Evidence and calibration | What would make this real? | Evidence tracker and calibration pages | Evidence/OIA and calibration tabs | Readiness heatmap and tracker status chart |

## Post-by-post requirements

The public surfaces must include an explicit reading map that cross-references each public post to:

- a named Quarto section or anchor;
- a named Streamlit page, tab or module;
- a GitHub Pages card, gallery item or report link;
- one static visual;
- one dynamic visual, toy module or simulation where interaction teaches the concept;
- a status label and caveat.

For the first six launch posts, this means:

| Post | Required Quarto surface | Required Streamlit surface | Minimum visual requirement |
|---|---|---|---|
| 01 upstream rationing and hospital growth | Executive summary, hospital spillover and scenario interpretation | Start here, Current state and Reference scenarios | Static patient-pathway/spillover diagram plus dynamic supply versus hospital-pressure plot |
| 02 FFS/capitation/blended funding | Funding model explanation and formula appendix | Funding models or Toy explainer module | Static funding-model comparison plus dynamic funding comparison toy |
| 03 marginal supply | Microeconomics section | Microeconomics lab | Static MR/MC or marginal-payment-gap diagram plus dynamic marginal supply simulation |
| 04 formulas do not solve games | Game theory and controls section | Game theory lab | Static payoff/best-response/control-stack diagram plus dynamic toy incentive game |
| 05 current reform pathway | Current reform comparator section | Current state and Reference scenarios | Static current reform map plus dynamic F0/current reform comparator plot |
| 06 uncapping primary care funding | Controlled scheduled activity payment section | Toy explainer and Microeconomics lab | Static scheduled-payment-with-controls diagram plus dynamic activity/control simulation |

Game-theory appendices and later posts must not be left as background material only. If the public site, report or dashboard refers to them, they must have a corresponding Quarto section and Streamlit module, with at least one static game-theory diagram and one dynamic or guided toy simulation.

## Visual contract matrix

| ID | Visual | Type | Primary audience purpose | Quarto report | GitHub Pages landing/site | Streamlit dashboard | Data source | Status label | Required caption / caveat |
|---|---|---|---|---|---|---|---|---|---|
| V01 | Public argument map | Conceptual diagram | Show the whole argument in one screen | Required | Required | Required | Hand-authored structure | Conceptual explainer | "This is the reading map, not model output." |
| V02 | Current reform pathway map | Conceptual pathway | Show that F0 is a real comparator | Required | Required | Required | Public policy summary | Public document + interpretation | "The current reform pathway is the comparator, not a no-reform straw man." |
| V03 | Marginal payment gap | Microeconomics diagram | Explain why capitation can leave extra activity underfunded | Required | Recommended | Required, dynamic version | Conceptual economics | Conceptual explainer | "Illustrative economics diagram, not an estimate." |
| V04 | Capitation budget constraint | Microeconomics diagram | Explain fixed baseline funding under rising demand | Required | Optional | Recommended | Conceptual economics | Conceptual explainer | "Shows the mechanism only." |
| V05 | Scheduled activity payment with controls | Microeconomics diagram | Explain uncapped but controlled payment | Required | Required | Required | Conceptual economics | Conceptual explainer | "Uncapped at global activity-envelope level; controlled by item, scope, audit and place accountability." |
| V06 | Co-payment barrier | Microeconomics diagram | Explain price/access inequity risk | Required | Recommended | Required, dynamic version | Conceptual economics | Conceptual explainer | "Illustrative; does not estimate patient demand elasticity." |
| V07 | Cherry-picking and gaming risk frontier | Conceptual plus plot | Show why controls and place accountability matter | Required | Recommended | Required, dynamic version | Scenario outputs plus toy settings | Model-generated/toy | "Risk scores are model-generated indices." |
| V08 | Hospital spillover flow | Flow diagram | Explain unmet primary care to ambulance/ED/admission pressure | Required | Required | Required | Conceptual pathway | Conceptual explainer | "Candidate causal pathway requiring validation." |
| V09 | Scenario rank bar chart | Static/dynamic plot | Compare hybrid viability indices | Required | Required preview | Existing, improve | `outputs/full-parameterised-summary-results-v1.7.0.csv` | Model-generated index | "Not observed New Zealand outcomes." |
| V10 | Scenario score heatmap | Static/dynamic plot | Compare all key indices across scenarios | Required | Recommended preview | Existing | Scenario CSV | Model-generated index | "Colour shows index score, not empirical performance." |
| V11 | F0 vs selected scenario profile | Static/dynamic plot | Make comparator logic visible | Required for F0 vs F4 | Required preview | Required, dynamic selector | Scenario CSV | Model-generated index | "F0 is the current reform comparator." |
| V12 | Risk-return scatter | Static/dynamic plot | Show viability against gaming/fiscal risk | Required | Recommended | Required | Scenario CSV | Model-generated index | "Relative benchmark comparison only." |
| V13 | Supply versus hospital pressure scatter | Static/dynamic plot | Show access/supply versus downstream pressure logic | Required | Recommended | Existing, refine | Scenario CSV | Model-generated index | "Hospital pressure is an index, not observed hospital demand." |
| V14 | Toy lever cards | Explanatory visual/table hybrid | Explain what each slider means | Optional | Optional | Required | `TOY_LEVER_DEFINITIONS` | Toy explainer | "Qualitative teaching levers, not estimated structural parameters." |
| V15 | Toy microeconomics simulation | Dynamic simulation | Show how marginal payment, audit and accountability change toy outputs | Optional static snapshot | Optional screenshot | Required | Toy formula | Toy explainer | "Teaching simulation only." |
| V16 | Co-payment/equity sensitivity simulation | Dynamic simulation | Show why equity protections matter | Optional static snapshot | Optional screenshot | Recommended | Toy formula | Toy explainer | "No demand elasticity is estimated." |
| V17 | Rural/local in-person capacity stress plot | Dynamic simulation | Show why telehealth cannot fully substitute local care | Optional static snapshot | Optional screenshot | Recommended | Toy formula | Toy explainer | "Illustrative mechanism only." |
| V18 | Evidence tracker status chart | Static/dynamic status visual | Show what evidence is public, pending or missing | Required | Required preview | Required | OIA/evidence tracker CSV | Evidence readiness | "Evidence status, not model performance." |
| V19 | Calibration readiness heatmap | Static/dynamic status visual | Show what is needed before calibration | Required | Required preview | Required | Calibration readiness table | Calibration readiness | "Readiness status, not validation result." |
| V20 | Claim boundary ladder | Conceptual diagram/table | Show what can and cannot be claimed | Required | Required | Recommended | Claim-boundary doc | Claim boundary | "Do not convert indices into savings, workforce or hospital-demand claims." |
| V21 | Public page/post alignment map | Navigation diagram | Help readers move between posts, report and dashboard | Required | Required | Recommended | Hand-authored structure | Navigation aid | "Reading guide, not evidence." |
| V22 | Static figure gallery | Page section | Make the site visually navigable | Optional | Required | Optional | Selected generated visuals | Mixed | "Each visual retains its own status label." |

## Additional recommended visuals and simulations

The following are useful for a general audience and should be considered during implementation:

1. A "one patient, three pathways" flow: timely primary care, delayed primary care, and hospital spillover.
2. A "practice day" capacity diagram: fixed clinicians, rising demand, and where funding affects marginal capacity.
3. A "who bears the cost" diagram: government, practice and patient under capitation-only, uncontrolled FFS and controlled hybrid.
4. A "controls stack" diagram: item rules, provider scope, documentation, audit, co-payment protections and place accountability.
5. A "what changes my mind" visual checklist based on the falsification section of the report.
6. A scenario small-multiple chart: each scenario gets the same compact profile card.
7. A readiness thermometer or traffic-light board for data availability.
8. A "claim ladder" graphic showing public document, theory, stakeholder intelligence, benchmark model and policy judgement.
9. A sensitivity tornado chart if toy or scenario sensitivity inputs are made available.
10. A simple animation or stepper in Streamlit that walks through the argument one step at a time.

## Surface-specific contract

Implementation of recurring production tasks is governed by Track 030:

- `conductor/tracks/030-publication-visual-workflows_20260513/spec.md`
- `docs/skills/`
- `docs/workflows/`

### GitHub Pages

The landing page must stop behaving like a directory. It should embed or preview:

- the public argument map;
- current reform pathway map;
- scenario rank chart;
- evidence tracker status chart;
- public calibration heatmap;
- links to the full report, Streamlit app, model card and claim boundaries.

UX requirement:

- The top of the page should answer "what am I looking at?" in one screen.
- The first scroll should show the argument map, the caveat and two clear actions: read the report or open the interactive dashboard.
- Visual preview cards should be clickable and should lead to the relevant report section or rendered page.
- The homepage should include a short "read this in order" rail that mirrors the post-aligned sequence.
- Evidence and calibration visuals should appear as status previews, not as buried document links.

### Quarto report

The report must become the static canonical visual explanation. It should include:

- conceptual diagrams before the results;
- static versions of the main scenario plots;
- figure captions with source-confidence labels;
- static fallbacks for any dynamic HTML visual;
- a clear distinction between conceptual diagrams, model-generated indices and evidence-readiness visuals.

UX requirement:

- The report should read as a guided visual essay, not as a technical appendix.
- Each major section should open with one visual, then explain it in plain language.
- Conceptual visuals should come before model-output plots so the reader understands the mechanism before seeing indices.
- Scenario plots should be grouped in a "what the benchmark shows" section with a repeated warning that these are model-generated indices.
- Evidence and calibration visuals should appear near the end as the bridge from explanation to next work.
- If Quarto HTML uses Plotly or Observable, the same section must still have a static fallback for PDF and accessibility.

### Streamlit dashboard

The dashboard must become the interactive companion to the posts and report. It should include:

- page/tab names aligned with the public post themes;
- dynamic versions of the microeconomics diagrams where useful;
- scenario comparison widgets;
- toy simulations that explain mechanisms without implying calibration;
- a figure inventory visible to the reader;
- plain-language "how to read this" notes above each interactive visual.

UX requirement:

- The dashboard should open with a short "choose your path" panel: overview, current pathway, economics, scenarios, evidence.
- Tabs/pages should map to the post-aligned themes rather than generic dashboard categories where possible.
- Each interactive page should start with a static explanation visual before sliders or charts.
- Sliders should sit beside the visual they affect, not only in a global sidebar, where the Streamlit layout allows it.
- Toy simulations should show immediate visual feedback but must remain labelled as teaching simulations.
- Reference scenario pages should always show F0/current reform as the comparator by default.
- The evidence/calibration pages should use status visuals first and tables second.

## Recommended UX improvements

These improvements should be treated as design recommendations for implementation, not as new policy claims.

1. Add a "visual reading path" on the GitHub Pages homepage: Argument, Current pathway, Economics, Scenarios, Evidence, Calibration.
2. Replace the current Streamlit global-slider feel with page-local interactive modules where possible. For example, the co-payment slider should live next to the co-payment barrier diagram.
3. Add a "F0 compared with..." selector across the scenario visuals so the current reform pathway is always visible.
4. Add a plain-language figure gallery on GitHub Pages. It should show thumbnails/previews and status labels for each visual.
5. Add a "one patient, three pathways" diagram. This is likely the clearest general-audience bridge between primary care access and hospital pressure.
6. Add a "practice day" capacity diagram. This will make the marginal-supply problem more intuitive than abstract payment language.
7. Add a "who bears the cost?" diagram comparing capitation-only, uncontrolled FFS and controlled hybrid funding.
8. Add an interactive Streamlit stepper that walks through the argument one screen at a time for readers who do not want to use sliders.
9. Add alt text or equivalent captions for every static image and diagram.
10. Add a mobile check to the acceptance tests or audit checklist, because general-audience readers may arrive from Substack or social links on phones.

## UX acceptance matrix

| Surface | First thing the reader sees | Main visual pattern | Interaction pattern | Exit path |
|---|---|---|---|---|
| GitHub Pages homepage | Argument map, caveat and two calls to action | Visual preview cards and reading path | Click through to rendered pages or Streamlit | Report, dashboard, model card, evidence tracker |
| Quarto report | Executive summary plus argument map | Guided visual essay with static diagrams and plots | Optional client-side Plotly/Observable in HTML, with static fallback | Evidence/calibration next-work section |
| Streamlit dashboard | Choose-your-path panel and caveat | Static explanation followed by dynamic visual module | Page-local sliders/selectors, scenario selectors and toy simulations | Link back to report, model card and claim boundaries |
| Evidence tracker page | Evidence status chart | Status chart first, table second | Filterable table if implemented in Streamlit | OIA/data next actions |
| Calibration readiness page | Readiness heatmap | Readiness heatmap first, data table second | Domain selector or status filter if implemented in Streamlit | Calibration protocol and validation backlog |

## Acceptance criteria

1. `conductor/tracks/029-visual-contract-public-visual-narrative_20260513/spec.md` contains the visual contract matrix.
2. The Quarto report includes at least five static visuals: three conceptual diagrams and two model-generated scenario plots.
3. The GitHub Pages landing page embeds at least four visual previews rather than only linking to pages.
4. The Streamlit dashboard includes at least three conceptual or microeconomics visuals and at least four dynamic plots/simulations.
5. Streamlit tabs/pages align with the public post themes or include a visible post-alignment guide.
6. Every visual has a status label: conceptual, toy, model-generated index, evidence readiness or public calibration.
7. Model-generated visuals use "index" wording and do not imply observed outcomes.
8. Dynamic Quarto visuals, if used, have static fallbacks for report/PDF use.
9. Tests assert that the visual contract, core diagrams, key plots and caveats are present.
10. Local validation passes: tests, Streamlit compile/smoke, and Quarto render.
11. `docs/public-site/post-surface-crosswalk-contract-v1.8.2.md` exists and maps the first six posts to Quarto, Streamlit, GitHub Pages, static visuals, dynamic visuals and implementation tracks.
12. The game-theory post and game-theory extension rows have explicit static game diagrams and dynamic or guided toy simulations.
13. Microeconomics rows have explicit static diagrams and dynamic Streamlit simulations with plain-language axis labels.
14. Each granular child track runs `$conductor-review`, applies in-scope fixes, reruns validation and records evidence before the next dependent phase proceeds.

## Out of scope

- Real-data calibration.
- New fiscal, hospital-demand, workforce or implementation-effect claims.
- Publishing or editing Substack posts directly.
- Adding private source documents to the public repository.
- Replacing the current caveat or claim-boundary framework.