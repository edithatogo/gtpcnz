from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from dash import Dash, Input, Output, State, dash_table, dcc, html

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.primarycare_model.dashboard_service import (  # noqa: E402
    CLAIM_BOUNDARY_TEXT,
    EDUCATIONAL_LEVER_DEFINITIONS,
    FULL_PUBLIC_CAVEAT,
    HUGGINGFACE_SPACE_URL,
    MetricCard,
    calibration_readiness,
    comparison_bundle,
    educational_defaults,
    public_links,
    reference_results,
    reference_summary,
    scenario_options,
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
        [
            dcc.Link("Start", href="/", className="nav-link"),
            dcc.Link("Compare scenarios", href="/compare", className="nav-link"),
            dcc.Link("Simulation lab", href="/simulation", className="nav-link"),
            dcc.Link("Evidence and methods", href="/evidence", className="nav-link"),
        ],
        className="nav",
    )


def _page_shell(children: list[object]) -> html.Main:
    return html.Main(children, className="page-shell")


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


def compare_page() -> html.Main:
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
                                value=DEFAULT_SCENARIOS,
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
        ]
    )


def _educational_sliders() -> list[html.Div]:
    defaults = educational_defaults()
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


def simulation_page() -> html.Main:
    return _page_shell(
        [
            html.Section(
                [
                    html.Div(
                        [
                            html.P("Bounded interactive runs", className="eyebrow"),
                            html.H1("Simulation lab"),
                            html.P(
                                "Live calculations stay capped and labelled as teaching outputs.",
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
                                value="uncertainty",
                                className="segmented-control",
                            ),
                            html.Label("Scenario", htmlFor="simulation-scenario", className="control-label"),
                            dcc.Dropdown(
                                id="simulation-scenario",
                                options=scenario_options(),
                                value="F4",
                                clearable=False,
                            ),
                            html.Label("Draws", htmlFor="simulation-draws", className="control-label"),
                            dcc.Slider(id="simulation-draws", min=10, max=500, step=10, value=100),
                            html.Label("Months", htmlFor="simulation-months", className="control-label"),
                            dcc.Slider(id="simulation-months", min=12, max=60, step=6, value=36),
                            html.Label("Synthetic population", htmlFor="simulation-population", className="control-label"),
                            dcc.Slider(id="simulation-population", min=50, max=500, step=10, value=180),
                            html.Label("Seed", htmlFor="simulation-seed", className="control-label"),
                            dcc.Input(id="simulation-seed", type="number", min=1, max=999999, step=1, value=20260526),
                            html.Div(_educational_sliders(), className="educational-grid"),
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
        ]
    )


def evidence_page() -> html.Main:
    readiness = calibration_readiness()
    return _page_shell(
        [
            html.Section(
                [
                    html.P("Evidence boundary", className="eyebrow"),
                    html.H1("Evidence and methods"),
                    html.P(CLAIM_BOUNDARY_TEXT, className="lede"),
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
            if (pathname === "/compare") { return "Compare scenarios"; }
            if (pathname === "/simulation") { return "Simulation lab"; }
            if (pathname === "/evidence") { return "Evidence and methods"; }
            return "Start";
        }
        """,
        Output("active-section-label", "children"),
        Input("url", "pathname"),
    )

    return app


app = create_app()
server = app.server


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname: str | None) -> html.Main:
    if pathname in (None, "/", "/start"):
        return start_page()
    if pathname == "/compare":
        return compare_page()
    if pathname == "/simulation":
        return simulation_page()
    if pathname == "/evidence":
        return evidence_page()
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
    app.run(host="0.0.0.0", port=7860, debug=False)
