from __future__ import annotations

import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

import pandas as pd
from dash import Dash, Input, Output, State, dash_table, dcc, html

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.dashboard_service import (  # noqa: E402
    CLAIM_BOUNDARY_TEXT,
    DASH_EXTRA_PUBLIC_ROUTES,
    DASH_ROUTE_ALIASES,
    EDUCATIONAL_LEVER_DEFINITIONS,
    FULL_PUBLIC_CAVEAT,
    HUGGINGFACE_SPACE_URL,
    STREAMLIT_PUBLIC_TABS,
    MetricCard,
    advanced_visual_bundles,
    budget_impact_bundle,
    calibration_benchmark_table,
    calibration_error_bundle,
    calibration_readiness,
    canonical_definitions_table,
    chart_provenance_table,
    comparison_bundle,
    current_reform_table,
    custom_scenario_comparison_bundle,
    custom_scenario_export_records,
    educational_defaults,
    educational_parameter_dictionary,
    evidence_table,
    figure_inventory_table,
    game_theory_bundles,
    live_model_diagnostic_bundles,
    methodology_bundles,
    microeconomics_bundles,
    model_gap_bundle,
    model_surface_status_table,
    oia_tracker_table,
    parse_dashboard_state,
    post_reading_map_table,
    public_aggregate_calibration_tables,
    public_cockpit_summary,
    public_links,
    public_status_table,
    readiness_chart_bundle,
    reference_results,
    reference_summary,
    runtime_health_table,
    scenario_heatmap_bundle,
    scenario_options,
    scenario_profile_bundle,
    score_guide_table,
    serialize_dashboard_state,
    simulation_bundle,
    start_metrics,
    supply_pressure_bundle,
)

APP_TITLE = "GTPCNZ interactive model lab"
DEFAULT_SCENARIOS = ["F0", "F4"]
EDUCATIONAL_FIELDS = tuple(definition.field_name for definition in EDUCATIONAL_LEVER_DEFINITIONS)


def _data_table(df: pd.DataFrame, table_id: str, page_size: int = 10) -> dash_table.DataTable:
    table = df.copy()
    table.columns = [str(column) for column in table.columns]
    for column in table.columns:
        table[column] = table[column].map(_table_cell)
    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": column.replace("_", " ").title(), "id": column} for column in table.columns],
        data=table.to_dict("records"),
        page_size=page_size,
        sort_action="native",
        filter_action="native",
        style_as_list_view=True,
        style_table={"overflowX": "auto"},
        style_cell={
            "fontFamily": "Inter, Segoe UI, Arial, sans-serif",
            "fontSize": "13px",
            "padding": "9px 10px",
            "minWidth": "110px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_header={
            "backgroundColor": "#f3f4f6",
            "fontWeight": "700",
            "border": "1px solid #d9dee7",
        },
        style_data={"border": "1px solid #e7eaf0"},
    )


def _table_cell(value: object) -> object:
    if isinstance(value, Mapping):
        return "; ".join(f"{key}: {item}" for key, item in value.items())
    if isinstance(value, str) or value is None:
        return value
    if isinstance(value, Sequence):
        return "; ".join(str(item) for item in value)
    return value


def _metric_card(metric: MetricCard) -> html.Div:
    return html.Div(
        [
            html.Span(metric.label, className="metric-label"),
            html.Strong(metric.value, className="metric-value"),
            html.Span(metric.detail, className="metric-detail"),
        ],
        className="metric-card",
    )


def _nav() -> html.Nav:
    return html.Nav(
        [dcc.Link(label, href=href, className="nav-link") for label, href in (*STREAMLIT_PUBLIC_TABS, *DASH_EXTRA_PUBLIC_ROUTES)],
        className="nav",
    )


def _page_shell(children: list[object]) -> html.Main:
    return html.Main(children, className="page-shell")


def _bundle_section(bundle, graph_id: str, page_size: int = 10) -> html.Section:
    return html.Section(
        [
            html.H2(bundle.title),
            dcc.Graph(figure=bundle.figure, id=graph_id, config={"displayModeBar": False}),
            html.P(bundle.interpretation, className="interpretation"),
            html.Details(
                [
                    html.Summary("Run provenance"),
                    _data_table(chart_provenance_table(bundle), f"{graph_id}-provenance-table", page_size=8),
                ],
                className="provenance-panel",
            ),
            html.H2("Table fallback", className="section-heading"),
            _data_table(bundle.table, f"{graph_id}-table", page_size=page_size),
        ],
        className="chart-stack",
    )


def _note_items(items: list[str]) -> html.Ul:
    return html.Ul([html.Li(item) for item in items], className="method-list")


def _shareable_link(pathname: str, search: str | None = None) -> html.Div:
    state = parse_dashboard_state(pathname, search)
    href = serialize_dashboard_state(state)
    return html.Div(
        [
            html.Span("Shareable state", className="metric-label"),
            html.A(href, href=href, className="surface-link"),
        ],
        className="shareable-link",
    )


def start_page() -> html.Main:
    links = public_links()
    return _page_shell(
        [
            html.Section(
                [
                    html.Div(
                        [
                            html.P("Public-data anchored benchmark", className="eyebrow"),
                            html.H1("GTPCNZ interactive model lab"),
                            html.P(
                                "A focused simulation surface for the primary-care funding architecture benchmark.",
                                className="lede",
                            ),
                        ],
                        className="intro-copy",
                    ),
                    html.Div([_metric_card(metric) for metric in start_metrics()], className="metric-grid"),
                ],
                className="intro-grid",
            ),
            html.Section(
                [
                    html.H2("Public surfaces"),
                    html.Div(
                        [
                            html.A("GitHub Pages front door", href=links["github_pages"], className="surface-link"),
                            html.A("Hugging Face Space", href=links["huggingface_space"], className="surface-link"),
                            html.A("Streamlit compatibility", href=links["streamlit_compatibility"], className="surface-link"),
                            html.A("Substack series", href=links["substack_series"], className="surface-link"),
                        ],
                        className="surface-grid",
                    ),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("Reference scenario summary"),
                    _data_table(reference_summary(), "start-summary-table", page_size=8),
                ],
                className="section-band",
            ),
        ]
    )


def post_guide_page() -> html.Main:
    links = public_links()
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Reading map", className="eyebrow"),
                    html.H1("Post guide"),
                    html.P(
                        "Maps the Substack series to GitHub Pages, the Hugging Face dashboard and the model modules without changing the claim boundary.",
                        className="lede",
                    ),
                    _note_items(
                        [
                            "Start with F0 as the current reform comparator.",
                            "Treat scenario tables and charts as model-generated indices.",
                            "Treat the labs as educational teaching simulations only.",
                            "A New Zealand outcome claim still needs real data and validation.",
                        ]
                    ),
                    html.Div(
                        [
                            html.A("Substack series", href=links["substack_series"], className="surface-link"),
                            html.A("GitHub Pages", href=links["github_pages"], className="surface-link"),
                            html.A("Hugging Face dashboard", href=links["huggingface_space"], className="surface-link"),
                        ],
                        className="surface-grid",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Reading map table"), _data_table(post_reading_map_table(), "post-guide-table", page_size=18)], className="section-band"),
        ]
    )


def current_state_page() -> html.Main:
    readiness = readiness_chart_bundle()
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Comparator and project status", className="eyebrow"),
                    html.H1("Current state"),
                    html.P(
                        "Separates what New Zealand is already doing, what this benchmark has built, and what evidence is still missing.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Current New Zealand reform pathway"), _data_table(current_reform_table(), "current-reform-table", page_size=8)], className="section-band"),
            html.Section([html.H2("Public project status"), _data_table(public_status_table(), "public-status-table", page_size=8)], className="section-band"),
            _bundle_section(readiness, "readiness-chart"),
            html.Section([html.H2("Figure and table inventory"), _data_table(figure_inventory_table(), "figure-inventory-table", page_size=12)], className="section-band"),
        ]
    )


def compare_page(search: str | None = None) -> html.Main:
    state = parse_dashboard_state("/reference-scenarios", search)
    return _page_shell(
        [
            html.Section(
                [
                    html.Div(
                        [
                            html.P("Reference scenarios", className="eyebrow"),
                            html.H1("Compare model-generated indices"),
                            html.P(
                                "Scenario differences are index-space reasoning under the public benchmark assumptions.",
                                className="lede",
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Scenarios", htmlFor="compare-scenarios", className="control-label"),
                            dcc.Dropdown(
                                id="compare-scenarios",
                                options=scenario_options(),
                                value=list(state.scenarios),
                                multi=True,
                                clearable=False,
                            ),
                            html.Button("Download CSV", id="compare-download-button", className="command-button"),
                            dcc.Download(id="compare-download"),
                        ],
                        className="control-panel",
                    ),
                ],
                className="two-column",
            ),
            html.Section([html.H2("Share this view"), _shareable_link("/reference-scenarios", search)], className="section-band"),
            html.Section(
                [
                    dcc.Graph(id="compare-bar-chart", config={"displayModeBar": False}),
                    dcc.Graph(id="compare-scatter-chart", config={"displayModeBar": False}),
                    html.P(id="compare-interpretation", className="interpretation"),
                    html.H2("Table fallback", className="section-heading"),
                    html.Div(id="compare-table"),
                ],
                className="chart-stack",
            ),
            _bundle_section(scenario_heatmap_bundle(), "reference-heatmap", page_size=10),
            _bundle_section(scenario_profile_bundle("F4"), "reference-profile", page_size=10),
            html.Section([html.H2("Score interpretation guide"), _data_table(score_guide_table(), "score-guide-table", page_size=8)], className="section-band"),
            _bundle_section(budget_impact_bundle(), "budget-impact", page_size=12),
        ]
    )


def microeconomics_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Educational economics labs", className="eyebrow"),
                    html.H1("Microeconomics"),
                    html.P(
                        "Dash replacements for the Streamlit marginal supply, capitation constraint, scheduled payment and access-mix labs.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            *[_bundle_section(bundle, f"micro-{index}", page_size=12) for index, bundle in enumerate(microeconomics_bundles(), start=1)],
        ]
    )


def game_theory_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Strategic behaviour labs", className="eyebrow"),
                    html.H1("Game theory"),
                    html.P(
                        "Dash replacements for Streamlit's audit game, coordination game and gaming-risk frontier.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            *[_bundle_section(bundle, f"game-{index}", page_size=12) for index, bundle in enumerate(game_theory_bundles(), start=1)],
        ]
    )


def _educational_sliders(defaults: dict[str, int] | None = None) -> list[html.Div]:
    defaults = defaults or educational_defaults()
    sliders: list[html.Div] = []
    for definition in EDUCATIONAL_LEVER_DEFINITIONS:
        sliders.append(
            html.Div(
                [
                    html.Label(definition.public_label, htmlFor=f"edu-{definition.field_name}", className="control-label"),
                    dcc.Slider(
                        id=f"edu-{definition.field_name}",
                        min=definition.lower_bound,
                        max=definition.upper_bound,
                        step=definition.step,
                        value=defaults[definition.field_name],
                        marks={
                            definition.lower_bound: str(definition.lower_bound),
                            definition.upper_bound: str(definition.upper_bound),
                        },
                        tooltip={"placement": "bottom", "always_visible": False},
                    ),
                ],
                className="slider-control",
            )
        )
    return sliders


def simulation_page(search: str | None = None) -> html.Main:
    state = parse_dashboard_state("/live-model", search)
    educational_values = dict(state.educational_settings) or educational_defaults()
    return _page_shell(
        [
            html.Section(
                [
                    html.Div(
                        [
                            html.P("Bounded interactive runs", className="eyebrow"),
                            html.H1("Live model"),
                            html.P(
                                "Live calculations stay capped and labelled as teaching outputs, with the Streamlit diagnostics now represented below.",
                                className="lede",
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Simulation view", htmlFor="simulation-kind", className="control-label"),
                            dcc.RadioItems(
                                id="simulation-kind",
                                options=[
                                    {"label": "Uncertainty", "value": "uncertainty"},
                                    {"label": "Stock-flow", "value": "stock-flow"},
                                    {"label": "Agent lens", "value": "agent-lens"},
                                    {"label": "Educational levers", "value": "educational"},
                                ],
                                value=state.simulation_kind,
                                className="segmented-control",
                            ),
                            html.Label("Scenario", htmlFor="simulation-scenario", className="control-label"),
                            dcc.Dropdown(
                                id="simulation-scenario",
                                options=scenario_options(),
                                value=state.scenario_id,
                                clearable=False,
                            ),
                            html.Label("Draws", htmlFor="simulation-draws", className="control-label"),
                            dcc.Slider(id="simulation-draws", min=10, max=500, step=10, value=state.draws),
                            html.Label("Months", htmlFor="simulation-months", className="control-label"),
                            dcc.Slider(id="simulation-months", min=12, max=60, step=6, value=state.months),
                            html.Label("Synthetic population", htmlFor="simulation-population", className="control-label"),
                            dcc.Slider(id="simulation-population", min=50, max=500, step=10, value=state.population_size),
                            html.Label("Seed", htmlFor="simulation-seed", className="control-label"),
                            dcc.Input(id="simulation-seed", type="number", min=1, max=999999, step=1, value=state.seed),
                            html.Div(_educational_sliders(educational_values), className="educational-grid"),
                            html.Div(
                                [
                                    html.Button("Run simulation", id="simulation-run-button", className="command-button primary"),
                                    html.Button("Download CSV", id="simulation-download-button", className="command-button"),
                                ],
                                className="command-row",
                            ),
                            dcc.Download(id="simulation-download"),
                        ],
                        className="control-panel",
                    ),
                ],
                className="two-column",
            ),
            html.Section([html.H2("Share this live model state"), _shareable_link("/live-model", search)], className="section-band"),
            html.Section(
                [
                    dcc.Store(id="simulation-summary-store"),
                    dcc.Graph(id="simulation-chart", config={"displayModeBar": False}),
                    html.P(id="simulation-interpretation", className="interpretation"),
                    html.H2("Table fallback", className="section-heading"),
                    html.Div(id="simulation-table"),
                ],
                className="chart-stack",
            ),
            *[_bundle_section(bundle, f"live-diagnostic-{index}", page_size=12) for index, bundle in enumerate(live_model_diagnostic_bundles("F4"), start=1)],
        ]
    )


def evidence_page() -> html.Main:
    methods = methodology_bundles()
    readiness = calibration_readiness()
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Evidence boundary", className="eyebrow"),
                    html.H1("Methodology"),
                    html.P(CLAIM_BOUNDARY_TEXT, className="lede"),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("Canonical definitions"),
                    _data_table(canonical_definitions_table(), "canonical-definitions-table", page_size=8),
                ],
                className="section-band",
            ),
            *[_bundle_section(bundle, f"methodology-{index}", page_size=12) for index, bundle in enumerate(methods, start=1)],
            html.Section(
                [
                    html.H2("Evidence and references"),
                    _data_table(evidence_table(), "evidence-table", page_size=10),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("Calibration readiness"),
                    _data_table(readiness, "readiness-table", page_size=10),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("Deployment posture"),
                    html.Ul(
                        [
                            html.Li("GitHub remains the source of truth."),
                            html.Li("GitHub Pages remains the public narrative front door."),
                            html.Li("Hugging Face Spaces hosts the zero-cost interactive Dash lab."),
                            html.Li("Streamlit remains a compatibility surface until the Dash lab passes release gates."),
                        ],
                        className="method-list",
                    ),
                ],
                className="section-band",
            ),
        ]
    )


def explainer_page() -> html.Main:
    default_bundle = simulation_bundle(
        kind="educational",
        scenario_id="F4",
        educational_settings=educational_defaults(),
    )
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Educational slider replacement", className="eyebrow"),
                    html.H1("Explainer"),
                    html.P(
                        "Plain-English lever dictionary and educational output from the same settings used by the live model control panel.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Educational parameter dictionary"), _data_table(educational_parameter_dictionary(), "educational-dictionary-table", page_size=8)], className="section-band"),
            _bundle_section(default_bundle, "explainer-educational", page_size=8),
        ]
    )


def evidence_oia_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Evidence and Official Information Act tracker", className="eyebrow"),
                    html.H1("Evidence/OIA"),
                    html.P(
                        "Public references plus the OIA tracker fallback. OIA responses and linked data are needed before treating the model as calibrated.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Evidence table"), _data_table(evidence_table(), "evidence-oia-evidence-table", page_size=10)], className="section-band"),
            html.Section([html.H2("OIA tracker"), _data_table(oia_tracker_table(), "oia-tracker-table", page_size=10)], className="section-band"),
        ]
    )


def calibration_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Calibration readiness", className="eyebrow"),
                    html.H1("Calibration"),
                    html.P(
                        "Shows what would be required before this became a real calibrated model. These are readiness and benchmark mappings, not observed outcome forecasts.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Calibration benchmark mapping"), _data_table(calibration_benchmark_table(), "calibration-benchmark-table", page_size=10)], className="section-band"),
            html.Section([html.H2("Calibration readiness"), _data_table(calibration_readiness(), "calibration-readiness-table", page_size=10)], className="section-band"),
        ]
    )


def public_cockpit_page() -> html.Main:
    sections, charts = public_cockpit_summary()
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Public contract cockpit", className="eyebrow"),
                    html.H1("Public cockpit"),
                    html.P(FULL_PUBLIC_CAVEAT, className="lede"),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Required cockpit sections"), _data_table(sections, "cockpit-sections-table", page_size=12)], className="section-band"),
            html.Section([html.H2("Required visuals, provenance and caveats"), _data_table(charts, "cockpit-charts-table", page_size=14)], className="section-band"),
        ]
    )


def glossary_page() -> html.Main:
    glossary_rows = pd.DataFrame(
        [
            ("Capitation", "Baseline funding for enrolled population responsibility."),
            ("Fee-for-service", "Payment for a specific eligible service."),
            ("Uncapped", "No fixed global ceiling on eligible activity."),
            ("Controlled", "Item rules, clinical governance, documentation, audit and accountability still apply."),
            ("Place-based accountability", "Responsibility for a whole local population, including hard-to-reach people."),
            ("Benchmark", "A transparent model structure that still needs real calibration data."),
            ("Reference scenario", "A model-generated scenario already stored in the project outputs."),
            ("Educational explainer", "A simplified interactive teaching tool, not the model forecast."),
            ("Model-generated index", "A 0-100 unitless score from benchmark logic, not an observed New Zealand outcome."),
        ],
        columns=["Term", "Plain-English definition"],
    )
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Plain-English definitions", className="eyebrow"),
                    html.H1("Glossary"),
                    html.P(
                        "Definitions carried forward from Streamlit, with the same distinction between benchmark outputs and calibrated evidence.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Terms"), _data_table(glossary_rows, "glossary-table", page_size=12)], className="section-band"),
        ]
    )


def guided_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Reader path", className="eyebrow"),
                    html.H1("Guided mode"),
                    html.P(
                        "A linear route through the public benchmark: comparator, scenarios, mechanisms, live uncertainty, then evidence gaps.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("1. Comparator"),
                    html.P("Start with F0 as the current reform pathway comparator, not a no-reform baseline."),
                    _data_table(current_reform_table(), "guided-current-reform-table", page_size=6),
                ],
                className="section-band",
            ),
            _bundle_section(comparison_bundle(("F0", "F4", "F8")), "guided-scenario-comparison", page_size=8),
            _bundle_section(microeconomics_bundles()[0], "guided-marginal-supply", page_size=8),
            _bundle_section(simulation_bundle("uncertainty", scenario_id="F4", draws=50, seed=20260526), "guided-uncertainty", page_size=8),
            html.Section(
                [
                    html.H2("5. Evidence gaps"),
                    html.P("Use the calibration route before interpreting any model index as an empirical result."),
                    _data_table(calibration_readiness(), "guided-calibration-readiness-table", page_size=8),
                ],
                className="section-band",
            ),
        ]
    )


def scenario_builder_page(search: str | None = None) -> html.Main:
    state = parse_dashboard_state("/scenario-builder", search)
    settings = dict(state.educational_settings) or educational_defaults()
    bundle = custom_scenario_comparison_bundle(settings)
    export_df = pd.DataFrame(custom_scenario_export_records(settings))
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Educational custom scenario", className="eyebrow"),
                    html.H1("Scenario builder"),
                    html.P(
                        "Build a bounded educational scenario and compare it with public reference scenarios. This is not calibrated and not a policy forecast.",
                        className="lede",
                    ),
                    _shareable_link("/scenario-builder", search),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("Current scenario inputs"),
                    _data_table(pd.DataFrame(sorted(settings.items()), columns=["Lever", "Value"]), "scenario-builder-inputs", page_size=8),
                ],
                className="section-band",
            ),
            _bundle_section(bundle, "scenario-builder-comparison", page_size=8),
            html.Section(
                [
                    html.H2("Export manifest fallback"),
                    _data_table(export_df, "scenario-builder-export", page_size=10),
                ],
                className="section-band",
            ),
        ]
    )


def model_surface_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Model coverage", className="eyebrow"),
                    html.H1("Model surface"),
                    html.P(
                        "Shows which modelling engines and diagnostics are now surfaced in Dash, which are still partial, and which remain outside the public claim boundary.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section([html.H2("Surface coverage status"), _data_table(model_surface_status_table(), "model-surface-status-table", page_size=16)], className="section-band"),
            _bundle_section(model_gap_bundle(), "model-gap-map", page_size=12),
        ]
    )


def calibration_diagnostics_page() -> html.Main:
    checks, gates, ppc = public_aggregate_calibration_tables()
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Readiness diagnostics", className="eyebrow"),
                    html.H1("Calibration diagnostics"),
                    html.P(
                        "Public aggregate calibration remains readiness-only unless registered public targets, source readiness, validation gates and posterior predictive checks pass.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            _bundle_section(calibration_error_bundle(), "calibration-error-diagnostic", page_size=10),
            html.Section([html.H2("Validation gates"), _data_table(gates, "calibration-validation-gates-table", page_size=10)], className="section-band"),
            html.Section([html.H2("Posterior predictive checks"), _data_table(ppc, "calibration-ppc-table", page_size=10)], className="section-band"),
            html.Section([html.H2("Registered target checks"), _data_table(checks, "calibration-target-checks-table", page_size=10)], className="section-band"),
        ]
    )


def advanced_visuals_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Higher-value public visuals", className="eyebrow"),
                    html.H1("Advanced visuals"),
                    html.P(
                        "Additional bounded visuals for evidence priority, structural uncertainty, equity-complexity interaction, policy shocks and scenario morphing. These explain model structure; they do not upgrade validation claims.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            *[_bundle_section(bundle, f"advanced-visual-{index}", page_size=10) for index, bundle in enumerate(advanced_visual_bundles(), start=1)],
        ]
    )


def runtime_health_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Operational metadata", className="eyebrow"),
                    html.H1("Runtime health"),
                    html.P(
                        "Deployment and runtime metadata for troubleshooting. This is not model-validation evidence.",
                        className="lede",
                    ),
                ],
                className="section-band",
            ),
            html.Section(
                [
                    html.H2("Runtime and deployment status"),
                    _data_table(runtime_health_table(), "runtime-health-table", page_size=12),
                ],
                className="section-band",
            ),
        ]
    )


def not_found_page() -> html.Main:
    return _page_shell([html.H1("Not found"), html.P("The requested lab page does not exist.")])


def create_app() -> Dash:
    app = Dash(__name__, suppress_callback_exceptions=True, title=APP_TITLE)
    app.layout = lambda: html.Div(
        [
            dcc.Location(id="url"),
            dcc.Store(id="reference-store", data=reference_results().to_dict("records")),
            html.Header(
                [
                    html.Div(
                        [
                            html.Span("GTPCNZ", className="brand-mark"),
                            html.Span("Interactive model lab", id="active-section-label", className="section-label"),
                        ],
                        className="brand-row",
                    ),
                    _nav(),
                ],
                className="topbar",
            ),
            html.Div(FULL_PUBLIC_CAVEAT, className="caveat-strip"),
            html.Div(id="page-content"),
            html.Footer(
                [
                    html.Span("Source: GitHub"),
                    html.A("Open Hugging Face Space", href=HUGGINGFACE_SPACE_URL),
                ],
                className="footer",
            ),
        ],
        className="app-root",
    )

    app.clientside_callback(
        """
        function(pathname) {
            const labels = {
                "/": "Start here",
                "/start": "Start here",
                "/post-guide": "Post guide",
                "/current-state": "Current state",
                "/reference-scenarios": "Reference scenarios",
                "/compare": "Reference scenarios",
                "/microeconomics": "Microeconomics",
                "/game-theory": "Game theory",
                "/live-model": "Live model",
                "/simulation": "Live model",
                "/methodology": "Methodology",
                "/evidence": "Methodology",
                "/explainer": "Explainer",
                "/evidence-oia": "Evidence/OIA",
                "/calibration": "Calibration",
                "/public-cockpit": "Public cockpit",
                "/glossary": "Glossary",
                "/guided": "Guided mode",
                "/scenario-builder": "Scenario builder",
                "/model-surface": "Model surface",
                "/calibration-diagnostics": "Calibration diagnostics",
                "/advanced-visuals": "Advanced visuals",
                "/runtime-health": "Runtime health"
            };
            if (labels[pathname]) { return labels[pathname]; }
            return "Start";
        }
        """,
        Output("active-section-label", "children"),
        Input("url", "pathname"),
    )

    return app


app = create_app()
server = app.server


@app.callback(Output("page-content", "children"), Input("url", "pathname"), Input("url", "search"))
def render_page(pathname: str | None, search: str | None = None) -> html.Main:
    canonical = DASH_ROUTE_ALIASES.get(pathname or "/", pathname or "/")
    if canonical == "/":
        return start_page()
    if canonical == "/post-guide":
        return post_guide_page()
    if canonical == "/current-state":
        return current_state_page()
    if canonical == "/reference-scenarios":
        return compare_page(search)
    if canonical == "/microeconomics":
        return microeconomics_page()
    if canonical == "/game-theory":
        return game_theory_page()
    if canonical == "/live-model":
        return simulation_page(search)
    if canonical == "/methodology":
        return evidence_page()
    if canonical == "/explainer":
        return explainer_page()
    if canonical == "/evidence-oia":
        return evidence_oia_page()
    if canonical == "/calibration":
        return calibration_page()
    if canonical == "/public-cockpit":
        return public_cockpit_page()
    if canonical == "/glossary":
        return glossary_page()
    if canonical == "/guided":
        return guided_page()
    if canonical == "/scenario-builder":
        return scenario_builder_page(search)
    if canonical == "/model-surface":
        return model_surface_page()
    if canonical == "/calibration-diagnostics":
        return calibration_diagnostics_page()
    if canonical == "/advanced-visuals":
        return advanced_visuals_page()
    if canonical == "/runtime-health":
        return runtime_health_page()
    return not_found_page()


@app.callback(
    Output("compare-bar-chart", "figure"),
    Output("compare-scatter-chart", "figure"),
    Output("compare-interpretation", "children"),
    Output("compare-table", "children"),
    Input("compare-scenarios", "value"),
    State("reference-store", "data"),
)
def update_comparison(selected: list[str] | None, _reference_records: list[dict[str, object]] | None):
    selected_ids = tuple(selected or DEFAULT_SCENARIOS)
    comparison = comparison_bundle(selected_ids)
    frontier = supply_pressure_bundle(selected_ids)
    return (
        comparison.figure,
        frontier.figure,
        comparison.interpretation,
        _data_table(comparison.table, "compare-table-data", page_size=10),
    )


@app.callback(
    Output("compare-download", "data"),
    Input("compare-download-button", "n_clicks"),
    State("compare-scenarios", "value"),
    prevent_initial_call=True,
)
def download_comparison(_n_clicks: int, selected: list[str] | None):
    bundle = comparison_bundle(tuple(selected or DEFAULT_SCENARIOS))
    return dcc.send_data_frame(bundle.table.to_csv, bundle.csv_filename, index=False)


simulation_states = [
    State("simulation-kind", "value"),
    State("simulation-scenario", "value"),
    State("simulation-draws", "value"),
    State("simulation-seed", "value"),
    State("simulation-months", "value"),
    State("simulation-population", "value"),
    *[State(f"edu-{field}", "value") for field in EDUCATIONAL_FIELDS],
]


@app.callback(
    Output("simulation-chart", "figure"),
    Output("simulation-interpretation", "children"),
    Output("simulation-table", "children"),
    Output("simulation-summary-store", "data"),
    Input("simulation-run-button", "n_clicks"),
    *simulation_states,
)
def update_simulation(
    _n_clicks: int | None,
    kind: str,
    scenario_id: str,
    draws: int,
    seed: int,
    months: int,
    population_size: int,
    *educational_values: int,
):
    settings = dict(zip(EDUCATIONAL_FIELDS, educational_values, strict=True))
    bundle = simulation_bundle(
        kind=kind,
        scenario_id=scenario_id,
        draws=int(draws),
        seed=int(seed),
        months=int(months),
        population_size=int(population_size),
        educational_settings=settings,
    )
    return (
        bundle.figure,
        bundle.interpretation,
        _data_table(bundle.table, "simulation-table-data", page_size=10),
        {"title": bundle.title, "rows": len(bundle.table), "csv_filename": bundle.csv_filename},
    )


simulation_download_states = [
    State("simulation-kind", "value"),
    State("simulation-scenario", "value"),
    State("simulation-draws", "value"),
    State("simulation-seed", "value"),
    State("simulation-months", "value"),
    State("simulation-population", "value"),
    *[State(f"edu-{field}", "value") for field in EDUCATIONAL_FIELDS],
]


@app.callback(
    Output("simulation-download", "data"),
    Input("simulation-download-button", "n_clicks"),
    *simulation_download_states,
    prevent_initial_call=True,
)
def download_simulation(
    _n_clicks: int,
    kind: str,
    scenario_id: str,
    draws: int,
    seed: int,
    months: int,
    population_size: int,
    *educational_values: int,
):
    settings = dict(zip(EDUCATIONAL_FIELDS, educational_values, strict=True))
    bundle = simulation_bundle(
        kind=kind,
        scenario_id=scenario_id,
        draws=int(draws),
        seed=int(seed),
        months=int(months),
        population_size=int(population_size),
        educational_settings=settings,
    )
    return dcc.send_data_frame(bundle.table.to_csv, bundle.csv_filename, index=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "7860")), debug=False)
