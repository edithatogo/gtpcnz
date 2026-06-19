# Streamlit dashboard contract audit v1.8.1

## Audit conclusion

Status: pass.

The Streamlit dashboard satisfies the v1.8.1 content and presentation contract after the current-state, diagram, table and explanation updates.

Migration status: pass for Streamlit compatibility. The future interactive surface is being implemented as a Plotly Dash app on Hugging Face Spaces; this audit remains the compatibility/reference baseline until the Dash parity gates replace it.

## Evidence matrix

| Contract requirement | Implementation evidence | Status |
|---|---|---|
| First screen identifies the dashboard as an explainer | `models/primarycare_model/app.py` title: `GTPCNZ: funding architecture explainer` | Pass |
| Full model caveat appears in the dashboard | `caveat_box()` renders the full caveat | Pass |
| Reader guide explains reference scenarios versus educational sliders | `render_reader_guide()` | Pass |
| Interpretation rules are visible | `render_interpretation_rules()` | Pass |
| Current reform pathway is explained as comparator | `render_current_state()` and `build_current_reform_table()` | Pass |
| Current state includes capitation, access target, NPCD, digital access, urgent care and PHO accountability | `build_current_reform_table()` | Pass |
| Static current-state table exists | `st.dataframe(build_current_reform_table())` | Pass |
| Static project-status table exists | `build_public_status_table()` | Pass |
| Static architecture diagram exists | `render_current_state_diagram()` uses `st.graphviz_chart()` | Pass |
| Dynamic reference-scenario viability chart exists | `render_reference_viability()` uses Plotly | Pass |
| Dynamic supply-generation versus hospital-pressure chart exists | `render_reference_scatter()` uses Plotly | Pass |
| Dynamic scenario score heatmap exists | `render_reference_heatmap()` uses Plotly `px.imshow()` | Pass |
| Dynamic selected scenario radar/profile chart exists | `render_scenario_profile_radar()` uses Plotly `go.Scatterpolar()` | Pass |
| Dynamic educational explainer chart exists | `render_educational_chart()` uses Plotly | Pass |
| Dynamic project readiness chart exists | `render_readiness_chart()` uses Plotly | Pass |
| Static/dynamic figure inventory exists | `render_figure_inventory()` lists static tables, static diagram and dynamic figures | Pass |
| Evidence/OIA table exists | `cached_oia_tracker()` and Evidence & OIA tab | Pass |
| Calibration-readiness table exists | `build_calibration_readiness_table()` and Calibration readiness tab | Pass |
| Plain-English glossary exists | Glossary tab and `Learn the 'Big Words'` expander | Pass |
| Educational sliders are not presented as forecast controls | Sidebar and educational-explainer text say they are educational and do not rerun the full benchmark | Pass |
| Educational parameter dictionary exists | `render_educational_parameter_dictionary()` presents public labels, health-economics meanings, high-value meanings and educational-output effects | Pass |
| Educational slider scale is defined | Sidebar says `0 means absent/weak; 100 means strong/reliably implemented` | Pass |
| Educational labels are plain policy levers rather than unexplained internal names | `EDUCATIONAL_LEVER_DEFINITIONS` provides labels such as `Payment for extra primary care activity`, `Stable population-based base funding` and `Whole-population local accountability` | Pass |
| Outputs are described as model-generated indices, not observed outcomes | Reference chart captions and glossary | Pass |
| No deprecated Streamlit `use_container_width` usage in app | Regression test asserts absence | Pass |
| Public Streamlit URL is documented | README, index, dashboard docs and deployment docs | Pass |
| Dash/Hugging Face migration is documented without deleting Streamlit compatibility | README, index, dashboard docs and Dash deployment guide | Pass |

## Validation evidence

Local validation after implementation:

- Contract/dashboard tests passed.
- Model package compilation passed.
- Streamlit entrypoint and dashboard modules passed Python syntax checks.

Remote validation after push:

- GitHub CI: success.
- Publish Quarto site: success.
- GitHub Pages: HTTP 200.
- Streamlit app URL: HTTP 200.

Dash migration validation after implementation:

- Focused Dash app and service-layer tests must pass before Dash becomes the primary interactive URL.
- Hugging Face Space build success is required before Streamlit is deprecated.
