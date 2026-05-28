# Visualisations and Tables Report

## Findings

The repo has a solid public visual layer. The Streamlit app uses charts, tables, tabs, and small explainer panels in a way that is readable for a general audience, and the Quarto report mirrors the same story in static form. The core patterns are:
- heatmap-style scenario comparison
- selected-scenario radar/profile chart
- calibration-readiness table
- evidence tracker table
- public report figures and callouts

The current implementation is functional, but not yet bleeding edge in visual design or analytical depth. Most visuals are descriptive and comparative, not interactive analytical instruments. That is the right choice for a public explainer, but it leaves room for a stronger reading experience.

## Evidence

- `models/primarycare_model/app.py:1249-1319` renders the heatmap and radar/profile chart with Plotly.
- `models/primarycare_model/app.py:1405-1518` renders the reference summary table, uncertainty table, stock-flow table, agent-lens table, and gap map table.
- `models/primarycare_model/app.py:1634-1712` wires the tabs, tables, and charts into the Streamlit app.
- `docs/public-site/streamlit-dashboard-contract-v1.8.1.md:34-68` lists the required dashboard visuals and tables.
- `docs/public-site/streamlit-dashboard-audit-v1.8.1.md:15-35` marks the required visuals as present.
- `reports/primary_care_architecture.qmd:100-274` contains the static report diagrams and comparison table.
- `index.qmd:12-31` exposes the public reading map and links the visual gallery.

## Completion Assessment

Completed for public explanation. Not completed as a polished analytical dashboard system.

What is finished:
- core comparison visuals exist
- the required public tables are present
- the dashboard contract is explicit
- the report and homepage expose the reading path

What is still thin:
- chart accessibility details are not consistently documented alongside each figure
- the visuals are descriptive rather than diagnostic
- there is no unified visual grammar for uncertainty, provenance, and caveat strength
- the public site still relies on parallel contract/audit documents rather than a single coherent visual spec

## Bleeding-edge Recommendations

1. Add an interaction-state legend that explains what each visualization is for and what it cannot claim.
2. Add accessible text summaries below every chart and table, especially for heatmaps and radar charts.
3. Add uncertainty overlays to the scenario visuals so readers can see spread and sensitivity in the same frame.
4. Add a visual provenance badge for each table/chart row set, showing source and freshness.
5. Add a “compare two scenarios” mode with synchronized charts and deltas.

## Risks

- Radar charts can encourage over-reading of shape similarity.
- Heatmaps can hide scale semantics if axis labels are not plain-language enough.
- Tables can become too dense for general readers without short summaries.
- A public visual layer can look complete while still under-explaining what is empirical versus illustrative.
