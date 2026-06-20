from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import parse_qs, urlencode

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure

from models.primarycare_model.calibration.public_aggregate_calibration import run_public_aggregate_calibration
from models.primarycare_model.runtime_lab import (
    BUDGET_IMPACT_NOTE,
    CANONICAL_DEFS,
    DEFAULT_ABM_POPULATION,
    DEFAULT_MONTE_CARLO_DRAWS,
    GITHUB_PAGES_URL,
    MAX_ABM_POPULATION,
    MAX_MONTE_CARLO_DRAWS,
    MAX_MONTHS,
    SCENARIOS,
    SCORE_GUIDE_ENTRIES,
    STREAMLIT_URL,
    SUBSTACK_POSTS,
    SUBSTACK_SERIES_URL,
    build_evidence_table,
    build_waterfall_data,
    calculate_indices,
    calibrate_all_scenarios,
    create_animation_frames,
    diminishing_return,
    get_runtime_scenario,
    model_gap_map,
    run_agent_lens,
    run_budget_impact,
    run_composite_meta_analysis,
    run_heatmap_matrix,
    run_interaction_scan,
    run_outcome_clustering,
    run_phase_portrait,
    run_policy_shock_sequence,
    run_reference_calculation,
    run_regime_sweep,
    run_stochastic_uncertainty,
    run_stock_flow_trace,
    run_tornado_sensitivity,
    run_variance_decomposition,
    run_voi_analysis,
    strategic_response,
)
from models.primarycare_model.scenario_service import (
    CLAIM_BOUNDARY_TEXT as CLAIM_BOUNDARY_TEXT,
)
from models.primarycare_model.scenario_service import (
    EDUCATIONAL_LEVER_DEFINITIONS,
    EducationalSettings,
    build_calibration_readiness_table,
    load_first_existing,
    load_scenario_results,
    score_educational_settings,
    summarise_reference_results,
)
from models.primarycare_model.ui.cockpit import build_policy_cockpit_payload
from models.primarycare_model.version import __version__ as APP_VERSION

ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = ROOT / "outputs" / "full-parameterised-summary-results-v1.8.1.csv"

HUGGINGFACE_SPACE_REPO = "https://huggingface.co/spaces/edithatogo/gtpcnz-dashboard"
HUGGINGFACE_SPACE_URL = "https://edithatogo-gtpcnz-dashboard.hf.space/"

FULL_PUBLIC_CAVEAT = (
    "This is a public-data anchored benchmark and educational explainer. "
    "It is not linked-data calibrated and not a patient-level forecast. "
    "It should not be used to claim precise fiscal savings, ED reductions, "
    "hospital-demand reductions, workforce effects, implementation impacts, or causal effects."
)

SimulationKind = Literal["uncertainty", "stock-flow", "agent-lens", "educational"]

STREAMLIT_PUBLIC_TABS: tuple[tuple[str, str], ...] = (
    ("Start here", "/"),
    ("Post guide", "/post-guide"),
    ("Current state", "/current-state"),
    ("Reference scenarios", "/reference-scenarios"),
    ("Microeconomics", "/microeconomics"),
    ("Game theory", "/game-theory"),
    ("Live model", "/live-model"),
    ("Methodology", "/methodology"),
    ("Explainer", "/explainer"),
    ("Evidence/OIA", "/evidence-oia"),
    ("Calibration", "/calibration"),
    ("Public cockpit", "/public-cockpit"),
    ("Glossary", "/glossary"),
)

DASH_ROUTE_ALIASES = {
    "/start": "/",
    "/compare": "/reference-scenarios",
    "/simulation": "/live-model",
    "/evidence": "/methodology",
}

DASH_EXTRA_PUBLIC_ROUTES: tuple[tuple[str, str], ...] = (
    ("Guided mode", "/guided"),
    ("Scenario builder", "/scenario-builder"),
    ("Model surface", "/model-surface"),
    ("Calibration diagnostics", "/calibration-diagnostics"),
    ("Advanced visuals", "/advanced-visuals"),
    ("Runtime health", "/runtime-health"),
)

OIA_TRACKER_CANDIDATES = (
    ROOT / "docs" / "audit" / "oia-request-tracker.csv",
    ROOT / "data" / "evidence" / "oia_request_tracker.csv",
)


@dataclass(frozen=True)
class MetricCard:
    label: str
    value: str
    detail: str


@dataclass(frozen=True)
class ChartBundle:
    title: str
    figure: Figure
    table: pd.DataFrame
    interpretation: str
    warning: str = FULL_PUBLIC_CAVEAT
    csv_filename: str = "gtpcnz-dashboard-data.csv"
    calculation_mode: str = "model_generated_index"
    source_snapshot_id: str = "public-benchmark-v1.8.1"
    seed: int | None = None
    caps: str = "Bounded public benchmark runtime."


@dataclass(frozen=True)
class DashboardState:
    route: str = "/reference-scenarios"
    scenarios: tuple[str, ...] = ("F0", "F4")
    simulation_kind: SimulationKind = "uncertainty"
    scenario_id: str = "F4"
    draws: int = DEFAULT_MONTE_CARLO_DRAWS
    seed: int = 20260526
    months: int = 36
    population_size: int = DEFAULT_ABM_POPULATION
    educational_settings: tuple[tuple[str, int], ...] = ()


@dataclass(frozen=True)
class RuntimeHealth:
    app_title: str
    app_version: str
    git_sha: str
    build_time: str
    python_runtime: str
    huggingface_space_url: str
    github_pages_url: str
    dependency_runtime: str
    cache_status: str
    pixi_status: str
    claim_boundary: str = FULL_PUBLIC_CAVEAT


def public_links() -> dict[str, str]:
    return {
        "github_pages": GITHUB_PAGES_URL,
        "huggingface_space": HUGGINGFACE_SPACE_URL,
        "huggingface_repo": HUGGINGFACE_SPACE_REPO,
        "streamlit_compatibility": STREAMLIT_URL,
        "substack_series": SUBSTACK_SERIES_URL,
    }


def _valid_scenario_ids() -> set[str]:
    return {scenario.scenario_id for scenario in SCENARIOS}


def _clamp_int(value: object, default: int, lower: int, upper: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return int(min(max(parsed, lower), upper))


def _first_query_value(query: dict[str, list[str]], key: str, default: str) -> str:
    values = query.get(key)
    if not values:
        return default
    return values[0] or default


def parse_dashboard_state(pathname: str | None = None, search: str | None = None) -> DashboardState:
    query = parse_qs((search or "").lstrip("?"), keep_blank_values=False)
    route = DASH_ROUTE_ALIASES.get(pathname or "/", pathname or "/")
    scenario_ids = _valid_scenario_ids()
    scenarios = tuple(sid for sid in _first_query_value(query, "scenarios", "F0,F4").split(",") if sid in scenario_ids)
    scenario_id = _first_query_value(query, "scenario", "F4")
    if scenario_id not in scenario_ids:
        scenario_id = "F4"
    kind = _first_query_value(query, "kind", "uncertainty")
    if kind not in ("uncertainty", "stock-flow", "agent-lens", "educational"):
        kind = "uncertainty"
    settings = educational_defaults()
    for definition in EDUCATIONAL_LEVER_DEFINITIONS:
        if definition.field_name in query:
            settings[definition.field_name] = _clamp_int(
                query[definition.field_name][0],
                settings[definition.field_name],
                int(definition.lower_bound),
                int(definition.upper_bound),
            )
    return DashboardState(
        route=route,
        scenarios=scenarios or ("F0", "F4"),
        simulation_kind=kind,  # type: ignore[arg-type]
        scenario_id=scenario_id,
        draws=_clamp_int(_first_query_value(query, "draws", str(DEFAULT_MONTE_CARLO_DRAWS)), DEFAULT_MONTE_CARLO_DRAWS, 10, MAX_MONTE_CARLO_DRAWS),
        seed=_clamp_int(_first_query_value(query, "seed", "20260526"), 20260526, 1, 999999),
        months=_clamp_int(_first_query_value(query, "months", "36"), 36, 6, MAX_MONTHS),
        population_size=_clamp_int(_first_query_value(query, "population", str(DEFAULT_ABM_POPULATION)), DEFAULT_ABM_POPULATION, 50, MAX_ABM_POPULATION),
        educational_settings=tuple(sorted(settings.items())),
    )


def serialize_dashboard_state(state: DashboardState) -> str:
    params: dict[str, str] = {
        "scenarios": ",".join(state.scenarios),
        "kind": state.simulation_kind,
        "scenario": state.scenario_id,
        "draws": str(state.draws),
        "seed": str(state.seed),
        "months": str(state.months),
        "population": str(state.population_size),
    }
    for key, value in state.educational_settings:
        params[key] = str(value)
    return f"{state.route}?{urlencode(params)}"


def chart_provenance_table(bundle: ChartBundle) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("App version", APP_VERSION),
            ("Calculation mode", bundle.calculation_mode),
            ("Source snapshot", bundle.source_snapshot_id),
            ("Seed", "" if bundle.seed is None else str(bundle.seed)),
            ("Runtime caps", bundle.caps),
            ("Rows", str(len(bundle.table))),
            ("Download", bundle.csv_filename),
            ("Claim boundary", bundle.warning),
        ],
        columns=["Field", "Value"],
    )


def runtime_health() -> RuntimeHealth:
    pixi_status = "not_checked"
    return RuntimeHealth(
        app_title="GTPCNZ interactive model lab",
        app_version=APP_VERSION,
        git_sha=os.getenv("GIT_SHA", os.getenv("SOURCE_VERSION", "unknown")),
        build_time=os.getenv("BUILD_TIME", "unknown"),
        python_runtime=sys.version.split()[0],
        huggingface_space_url=HUGGINGFACE_SPACE_URL,
        github_pages_url=GITHUB_PAGES_URL,
        dependency_runtime="Dash on Python; deployment target is Hugging Face Spaces Docker on free CPU Basic.",
        cache_status="In-memory Python process cache only; no Redis, paid workers, GPU, or persistent disk dependency.",
        pixi_status=pixi_status,
    )


def runtime_health_table() -> pd.DataFrame:
    health = runtime_health()
    return pd.DataFrame(
        [
            ("App title", health.app_title),
            ("App version", health.app_version),
            ("Git SHA", health.git_sha),
            ("Build time", health.build_time),
            ("Python runtime", health.python_runtime),
            ("Hugging Face Space", health.huggingface_space_url),
            ("GitHub Pages", health.github_pages_url),
            ("Dependency runtime", health.dependency_runtime),
            ("Cache status", health.cache_status),
            ("Pixi status", health.pixi_status),
            ("Claim boundary", health.claim_boundary),
        ],
        columns=["Area", "Status"],
    )


def scenario_options() -> list[dict[str, str]]:
    return [
        {
            "label": f"{scenario.scenario_id} - {scenario.scenario_name}",
            "value": scenario.scenario_id,
        }
        for scenario in SCENARIOS
    ]


@lru_cache(maxsize=1)
def _reference_results_cached() -> pd.DataFrame:
    if RESULTS_PATH.exists():
        return load_scenario_results(RESULTS_PATH)
    return run_reference_calculation(months=MAX_MONTHS)


def reference_results() -> pd.DataFrame:
    return _reference_results_cached().copy()


def reference_summary() -> pd.DataFrame:
    return summarise_reference_results(reference_results())


def start_metrics() -> tuple[MetricCard, ...]:
    df = reference_results()
    readiness = build_calibration_readiness_table()
    best = df.sort_values("hybrid_viability_score", ascending=False).iloc[0]
    return (
        MetricCard("Reference scenarios", str(len(df)), "Precomputed public benchmark scenarios."),
        MetricCard("Claim boundary", "Public benchmark", "Not linked-data calibrated or patient-level."),
        MetricCard("Calibration", "Readiness only", "Public aggregate gates only where documented."),
        MetricCard("Highest viability", str(best["scenario_id"]), f"{best['hybrid_viability_score']} index score."),
        MetricCard("Readiness rows", str(len(readiness)), "Evidence needed before real calibration."),
    )


def _selected_reference_rows(scenario_ids: tuple[str, ...]) -> pd.DataFrame:
    df = reference_results()
    if not scenario_ids:
        scenario_ids = ("F0", "F4")
    selected = df[df["scenario_id"].isin(scenario_ids)].copy()
    selected["_selected_order"] = pd.Categorical(selected["scenario_id"], categories=list(scenario_ids), ordered=True)
    return selected.sort_values("_selected_order").drop(columns=["_selected_order"])


def comparison_bundle(scenario_ids: tuple[str, ...]) -> ChartBundle:
    df = _selected_reference_rows(scenario_ids)
    score_cols = [
        "hybrid_viability_score",
        "access_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    chart_df = df.melt(
        id_vars=["scenario_id", "scenario_name"],
        value_vars=score_cols,
        var_name="metric",
        value_name="score",
    )
    chart_df["metric"] = chart_df["metric"].str.replace("_score", "", regex=False).str.replace("_", " ").str.title()
    fig = px.bar(
        chart_df,
        x="metric",
        y="score",
        color="scenario_id",
        barmode="group",
        title="Reference scenario index comparison",
        labels={"metric": "Index", "score": "Model-generated index score", "scenario_id": "Scenario"},
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20), legend_title_text="Scenario")
    return ChartBundle(
        title="Reference scenario comparison",
        figure=fig,
        table=df[["scenario_id", "scenario_name", *score_cols]],
        interpretation="Compare scenario differences as index-space reasoning only. Do not convert score gaps into dollars, beds, workforce or causal effects.",
        csv_filename="gtpcnz-reference-scenario-comparison.csv",
    )


def supply_pressure_bundle(scenario_ids: tuple[str, ...] = ()) -> ChartBundle:
    df = _selected_reference_rows(scenario_ids or tuple(s.scenario_id for s in SCENARIOS))
    fig = px.scatter(
        df,
        x="supply_generation_score",
        y="hospital_pressure_score",
        color="scenario_id",
        hover_name="scenario_name",
        size="hybrid_viability_score",
        title="Supply generation versus hospital pressure",
        labels={
            "supply_generation_score": "Supply generation index",
            "hospital_pressure_score": "Hospital pressure index",
            "scenario_id": "Scenario",
        },
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        title="Supply pressure frontier",
        figure=fig,
        table=df[
            [
                "scenario_id",
                "scenario_name",
                "supply_generation_score",
                "hospital_pressure_score",
                "hybrid_viability_score",
            ]
        ],
        interpretation="This shows the benchmark's internal supply-pressure tradeoff. It is not a measured hospital-demand effect.",
        csv_filename="gtpcnz-supply-pressure-frontier.csv",
    )


def scenario_heatmap_bundle() -> ChartBundle:
    df = reference_results()
    heatmap_columns = [
        "hybrid_viability_score",
        "supply_generation_score",
        "equity_legitimacy_score",
        "governance_resilience_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    matrix = df.set_index("scenario_id")[heatmap_columns].sort_index()
    fig = px.imshow(
        matrix,
        aspect="auto",
        color_continuous_scale="Viridis",
        title="Scenario score matrix: model-generated indices",
        labels={"x": "Index", "y": "Reference scenario", "color": "Index score"},
    )
    fig.update_layout(height=460, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        title="Scenario score matrix",
        figure=fig,
        table=matrix.reset_index(),
        interpretation="A compact replacement for the Streamlit heatmap: it compares index patterns across all reference scenarios.",
        csv_filename="gtpcnz-scenario-score-matrix.csv",
    )


def scenario_profile_bundle(scenario_id: str = "F4") -> ChartBundle:
    profile = scenario_profile(scenario_id)
    values = profile["score"].astype(float).tolist()
    labels = profile["metric"].tolist()
    fig = go.Figure(
        go.Scatterpolar(
            r=[*values, values[0]],
            theta=[*labels, labels[0]],
            fill="toself",
            name=scenario_id,
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=440,
        margin=dict(l=40, r=40, t=56, b=24),
        title=f"Selected scenario profile: {scenario_id}",
    )
    return ChartBundle(
        title="Scenario profile radar",
        figure=fig,
        table=profile,
        interpretation="Radar view of one reference scenario across the same public benchmark indices.",
        csv_filename=f"gtpcnz-{scenario_id}-scenario-profile.csv",
    )


@lru_cache(maxsize=64)
def uncertainty_bundle(
    scenario_id: str,
    draws: int = DEFAULT_MONTE_CARLO_DRAWS,
    seed: int = 20260526,
    sd: float = 0.08,
) -> ChartBundle:
    draws = int(min(max(10, draws), MAX_MONTE_CARLO_DRAWS))
    frame, summary = run_stochastic_uncertainty(scenario_id=scenario_id, draws=draws, seed=seed, sd=sd)
    fig = px.histogram(
        frame,
        x="hybrid_viability_score",
        nbins=32,
        marginal="box",
        title=f"Seeded uncertainty demo for {scenario_id}",
        labels={"hybrid_viability_score": "Hybrid viability index"},
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        title="Seeded stochastic uncertainty",
        figure=fig,
        table=summary,
        interpretation=(
            f"Seed {seed} with {draws} bounded draws. This is demonstrative uncertainty around "
            "public benchmark assumptions, not an empirical probability distribution."
        ),
        csv_filename=f"gtpcnz-{scenario_id}-uncertainty.csv",
    )


@lru_cache(maxsize=64)
def stock_flow_bundle(scenario_id: str, months: int = 36) -> ChartBundle:
    months = int(min(max(12, months), MAX_MONTHS))
    frame = run_stock_flow_trace(scenario_id=scenario_id, months=months)
    chart_df = frame.melt(
        id_vars=["month"],
        value_vars=["unmet_need", "primary_capacity", "hospital_pressure", "fiscal_pressure"],
        var_name="metric",
        value_name="value",
    )
    chart_df["metric"] = chart_df["metric"].str.replace("_", " ").str.title()
    fig = px.line(
        chart_df,
        x="month",
        y="value",
        color="metric",
        title=f"Stock-flow teaching trace for {scenario_id}",
        labels={"month": "Month", "value": "Index value", "metric": "Metric"},
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        title="Stock-flow trace",
        figure=fig,
        table=frame,
        interpretation="A bounded teaching trace showing internal model dynamics. It is not a forecast of monthly New Zealand activity.",
        csv_filename=f"gtpcnz-{scenario_id}-stock-flow.csv",
    )


@lru_cache(maxsize=64)
def agent_lens_bundle(
    scenario_id: str,
    population_size: int = DEFAULT_ABM_POPULATION,
    months: int = 12,
    seed: int = 20260526,
) -> ChartBundle:
    population_size = int(min(max(50, population_size), MAX_ABM_POPULATION))
    months = int(min(max(6, months), 24))
    agents, summary = run_agent_lens(
        scenario_id=scenario_id,
        population_size=population_size,
        months=months,
        seed=seed,
    )
    agents = agents.copy()
    agents["rural_status"] = agents["rural"].map({True: "Rural", False: "Non-rural"})
    fig = px.scatter(
        agents,
        x="high_need_score",
        y="access_probability",
        color="rural_status",
        opacity=0.72,
        render_mode="webgl",
        title=f"Agent-lens teaching replay for {scenario_id}",
        labels={
            "high_need_score": "Synthetic high-need score",
            "access_probability": "Access probability",
            "rural_status": "Synthetic location group",
        },
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        title="Agent-lens replay",
        figure=fig,
        table=summary,
        interpretation=(
            f"Seed {seed}, {population_size} synthetic agents, {months} months. "
            "This is a teaching lens for allocation logic, not patient-level simulation evidence."
        ),
        csv_filename=f"gtpcnz-{scenario_id}-agent-lens.csv",
    )


def educational_defaults() -> dict[str, int]:
    return {definition.field_name: int(definition.default_value) for definition in EDUCATIONAL_LEVER_DEFINITIONS}


def post_reading_map_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Post": post_id,
                "Public title": post["title"],
                "Substack URL": post["url"],
                "GitHub Pages": GITHUB_PAGES_URL,
                "Hugging Face dashboard": HUGGINGFACE_SPACE_URL,
                "Streamlit module": "; ".join(post.get("models", [])),
                "Status / caveat": "Public aggregate validation where gated; not linked-data calibrated or a patient-level forecast.",
            }
            for post_id, post in SUBSTACK_POSTS.items()
        ]
    )


def current_reform_table() -> pd.DataFrame:
    rows = [
        ("Capitation reweighting", "Changing how baseline enrolled-population funding is allocated.", "May improve fairness of distribution, but does not by itself create a strong payment signal for the next clinically necessary appointment."),
        ("Primary care access target", "A public target for getting people timely primary care access.", "Useful as a signal, but targets need workforce, funding and data support to change behaviour."),
        ("National Primary Care Dataset", "A data programme intended to improve visibility of primary care activity and access.", "Important for future calibration; not yet enough on its own to prove the model's assumptions."),
        ("Digital access and telehealth", "Online and remote access routes for some care needs.", "Can help access, but cannot replace local in-person care for every patient, place or condition."),
        ("Urgent and after-hours care work", "Policy attention to alternatives before emergency department presentation.", "May matter, but needs funding architecture and workforce support to shift demand safely."),
        ("PHO accountability and commissioning", "Use of organisations and contracts to manage enrolled-population responsibility.", "Central to place accountability, but pass-through, transaction costs and incentives need verification."),
    ]
    return pd.DataFrame(rows, columns=["Current pathway component", "Plain-English meaning", "Why it matters for this model"])


def public_status_table() -> pd.DataFrame:
    rows = [
        ("Model status", "Public-data anchored benchmark", "Ready for explanation; not ready for forecasting."),
        ("Dashboard status", "Dash on Hugging Face plus Streamlit compatibility", "Dash is the migration target; Streamlit remains the parity baseline until retired."),
        ("Evidence status", "Evidence readiness", "OIA/data requests still need submission or update."),
        ("Calibration status", "Readiness mapped", "Real linked data and validation tests still required."),
        ("Claim status", "Bounded", "No precise fiscal, hospital-demand, workforce or implementation-impact claims."),
        ("Deployment status", "GitHub Pages and Hugging Face", "GitHub is source/front door; Hugging Face hosts the interactive lab."),
    ]
    return pd.DataFrame(rows, columns=["Area", "Current state", "What this means"])


def model_surface_status_table() -> pd.DataFrame:
    rows = [
        ("Reference scenarios", "surfaced", "/reference-scenarios", "Precomputed public scenario indices with comparison, scatter, heatmap, profile and budget-impact views."),
        ("Microeconomics labs", "surfaced", "/microeconomics", "Marginal supply, capitation budget, scheduled payment and access route mix."),
        ("Game theory labs", "surfaced", "/game-theory", "Claims audit, coordination and gaming-risk frontier views."),
        ("Monte Carlo uncertainty", "surfaced", "/live-model", "Seeded bounded uncertainty run; demonstrative intervals only."),
        ("Stock-flow dynamics", "surfaced", "/live-model", "Bounded monthly teaching trace; not a forecast."),
        ("ABM agent lens", "surfaced", "/live-model", "Capped synthetic-agent allocation lens; not patient-level evidence."),
        ("Sensitivity / decomposition", "surfaced", "/live-model", "Tornado, waterfall, variance and phase portrait diagnostics."),
        ("Outcome clustering", "surfaced", "/methodology", "Internal model-structure grouping over benchmark scenarios."),
        ("Budget impact / diffusion", "surfaced", "/reference-scenarios", "Illustrative Bass diffusion budget view, not a fiscal forecast."),
        ("VOI / evidence priority", "surfaced", "/advanced-visuals", "Seeded EVPI/EVPPI teaching view for evidence-priority ranking."),
        ("Structural uncertainty", "surfaced", "/advanced-visuals", "Public structural-model registry interval and weights."),
        ("Policy shocks", "surfaced", "/advanced-visuals", "Abrupt-change teaching sequence for hospital and fiscal pressure."),
        ("Linked-data calibration", "deferred_public_boundary", "/calibration-diagnostics", "Readiness-only until source-ready public/linked validation gates pass."),
        ("Patient-level forecasting", "retired", "/runtime-health", "Out of public scope; claim boundary prohibits patient-level forecasts."),
    ]
    return pd.DataFrame(rows, columns=["Model surface", "Status", "Dash route", "Boundary / implementation note"])


def model_gap_bundle() -> ChartBundle:
    table = model_gap_map()
    counts = table.groupby("tier", as_index=False).size().rename(columns={"size": "Items"})
    fig = px.bar(
        counts,
        x="tier",
        y="Items",
        title="Model surface map: current assets and remaining gaps",
        labels={"tier": "Tier", "Items": "Mapped assets or gaps"},
    )
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=56, b=20), showlegend=False)
    return ChartBundle(
        "Model gap map",
        fig,
        table,
        "Shows which modelling surfaces are executable, partially surfaced, or still deferred. This is a coverage map, not validation evidence.",
        csv_filename="gtpcnz-model-gap-map.csv",
        calculation_mode="model_surface_inventory",
    )


def readiness_chart_bundle() -> ChartBundle:
    table = pd.DataFrame(
        [
            ("Public explanation", 85),
            ("Scenario comparison", 75),
            ("Evidence inventory", 55),
            ("Stakeholder validation", 25),
            ("Real-data calibration", 10),
        ],
        columns=["Readiness area", "Illustrative readiness index"],
    )
    fig = px.bar(
        table,
        x="Illustrative readiness index",
        y="Readiness area",
        orientation="h",
        title="What is mature and what is still early",
        range_x=[0, 100],
    )
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=56, b=20), showlegend=False)
    return ChartBundle(
        title="Project readiness",
        figure=fig,
        table=table,
        interpretation="Project-status visual only. It is not an empirical performance result.",
        csv_filename="gtpcnz-project-readiness.csv",
    )


def figure_inventory_table() -> pd.DataFrame:
    rows = [
        ("Static table", "Current reform pathway", "Current state", "Explains the real comparator in plain English."),
        ("Static table", "Post reading map", "Post guide", "Maps posts to report sections, dashboard modules, visuals and caveats."),
        ("Dynamic bar chart", "Reference scenario viability", "Reference scenarios", "Compares model-generated viability indices."),
        ("Dynamic scatter plot", "Supply generation versus hospital pressure", "Reference scenarios", "Shows the internal supply-pressure tradeoff."),
        ("Dynamic heatmap", "Scenario score matrix", "Reference scenarios", "Shows multiple indices across scenarios at once."),
        ("Dynamic radar chart", "Selected scenario profile", "Reference scenarios", "Shows one selected scenario across dimensions."),
        ("Dynamic line/bar/stacked charts", "Microeconomics labs", "Microeconomics", "Shows marginal supply, capitation constraint, scheduled payment and access mix."),
        ("Dynamic payoff charts", "Game theory labs", "Game theory", "Shows audit, coordination and gaming-risk incentives."),
        ("Dynamic stochastic charts", "Uncertainty, stock-flow, agent lens", "Live model", "Shows bounded seeded teaching simulations."),
        ("Dynamic sensitivity charts", "Tornado, waterfall, variance, phase portrait", "Live model", "Shows live model diagnostics from runtime helpers."),
        ("Static/dynamic tables", "Evidence, OIA, calibration readiness", "Evidence/OIA and Calibration", "Shows sources and what is still needed before calibration."),
        ("Contract panel", "Public cockpit", "Public cockpit", "Shows cockpit sections, required visuals, provenance, VOI and downloads."),
    ]
    return pd.DataFrame(rows, columns=["Type", "Figure or table", "Dash route", "Purpose"])


def educational_parameter_dictionary() -> pd.DataFrame:
    return pd.DataFrame(
        [
            (
                definition.public_label,
                definition.health_economics_meaning,
                definition.high_value_meaning,
                definition.educational_output_effect,
            )
            for definition in EDUCATIONAL_LEVER_DEFINITIONS
        ],
        columns=[
            "Educational lever",
            "Health-economics meaning",
            "What a high value means",
            "How it affects the educational output",
        ],
    )


def canonical_definitions_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Metric": key,
                "Label": value["label"],
                "Short name": value["short"],
                "Range": value["range"],
                "Meaning": value["meaning"],
                "Higher is": value["higher_is"],
            }
            for key, value in CANONICAL_DEFS.items()
        ]
    )


def score_guide_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Metric": label,
                "Range": rng,
                "Meaning": meaning,
                "Higher is": direction,
                "Thresholds": "; ".join(f"{key}: {value}" for key, value in thresholds.items()),
                "Formula": formula,
                "Components": components,
            }
            for _key, label, rng, meaning, direction, thresholds, formula, components in SCORE_GUIDE_ENTRIES
        ]
    )


def educational_bundle(settings: dict[str, int] | None = None) -> ChartBundle:
    values = educational_defaults()
    if settings:
        for definition in EDUCATIONAL_LEVER_DEFINITIONS:
            if definition.field_name in settings:
                values[definition.field_name] = int(settings[definition.field_name])
    scores = score_educational_settings(EducationalSettings(**values))
    table = pd.DataFrame(
        [
            {
                "metric": key.replace("educational_", "").replace("_score", "").replace("_", " ").title(),
                "score": value,
            }
            for key, value in scores.items()
        ]
    )
    fig = px.bar(
        table,
        x="metric",
        y="score",
        title="Educational lever output",
        labels={"metric": "Educational output", "score": "Teaching index score"},
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20), showlegend=False)
    return ChartBundle(
        title="Educational explainer",
        figure=fig,
        table=table,
        interpretation="Slider output is a qualitative teaching artefact. It does not rerun the full parameterised model.",
        csv_filename="gtpcnz-educational-explainer.csv",
        calculation_mode="educational_slider_output",
    )


def custom_scenario_comparison_bundle(settings: dict[str, int] | None = None) -> ChartBundle:
    values = educational_defaults()
    if settings:
        values.update({key: int(value) for key, value in settings.items() if key in values})
    educational_scores = score_educational_settings(EducationalSettings(**values))
    reference = _selected_reference_rows(("F0", "F4", "F8"))
    custom_row = {
        "scenario_id": "CUSTOM",
        "scenario_name": "Custom educational scenario",
        "hybrid_viability_score": educational_scores["educational_viability_score"],
        "supply_generation_score": educational_scores["educational_supply_score"],
        "hospital_pressure_score": educational_scores["educational_hospital_pressure_score"],
        "gaming_risk_score": educational_scores["educational_gaming_risk_score"],
        "calculation_status": "educational scenario builder output; not calibrated and not a policy forecast",
    }
    cols = [
        "scenario_id",
        "scenario_name",
        "hybrid_viability_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    table = pd.concat([reference[cols], pd.DataFrame([custom_row])[cols]], ignore_index=True)
    chart_df = table.melt(
        id_vars=["scenario_id", "scenario_name"],
        value_vars=[
            "hybrid_viability_score",
            "supply_generation_score",
            "hospital_pressure_score",
            "gaming_risk_score",
        ],
        var_name="metric",
        value_name="score",
    )
    chart_df["metric"] = chart_df["metric"].str.replace("_score", "", regex=False).str.replace("_", " ").str.title()
    fig = px.bar(
        chart_df,
        x="metric",
        y="score",
        color="scenario_id",
        barmode="group",
        title="Custom educational scenario versus public reference scenarios",
        labels={"metric": "Index", "score": "Model-generated/educational index", "scenario_id": "Scenario"},
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=56, b=20), legend_title_text="Scenario")
    return ChartBundle(
        title="Custom scenario comparison",
        figure=fig,
        table=table,
        interpretation="The custom scenario is a bounded educational scenario-builder output. It is not calibrated and must not be treated as a policy forecast.",
        csv_filename="gtpcnz-custom-educational-scenario.csv",
        calculation_mode="custom_educational_scenario",
        caps="Educational slider bounds 0-100; compared only with public reference scenario indices.",
    )


def custom_scenario_export_records(settings: dict[str, int] | None = None) -> list[dict[str, object]]:
    values = educational_defaults()
    if settings:
        values.update({key: int(value) for key, value in settings.items() if key in values})
    return [
        {
            "field": key,
            "value": value,
            "claim_boundary": FULL_PUBLIC_CAVEAT,
            "calculation_mode": "custom_educational_scenario",
            "app_version": APP_VERSION,
        }
        for key, value in sorted(values.items())
    ]


def microeconomics_bundles() -> tuple[ChartBundle, ...]:
    payment_rows = []
    for signal in range(0, 101, 5):
        sig_frac = signal / 100.0
        saturation = strategic_response(sig_frac, 0.35 + 0.12 * 0.30, 5.0)
        supply = 130 + 95 * saturation * diminishing_return(0.48, 2.6) - 24 * diminishing_return(0.30, 2.0)
        payment_rows.append({"payment_signal": signal, "appointments_per_period": round(supply, 1)})
    payment_df = pd.DataFrame(payment_rows)
    payment_fig = px.line(
        payment_df,
        x="payment_signal",
        y="appointments_per_period",
        markers=True,
        title="Microeconomics lab 1: marginal supply response",
        labels={"payment_signal": "Marginal payment signal", "appointments_per_period": "Illustrative appointments"},
    )
    payment_fig.update_layout(height=380, margin=dict(l=20, r=20, t=56, b=20))

    budget_df = pd.DataFrame(
        [
            {"item": "Capitation envelope", "nzd": 880000},
            {"item": "Population need pressure", "nzd": 1020000},
            {"item": "Residual pressure", "nzd": 140000},
        ]
    )
    budget_fig = px.bar(
        budget_df,
        x="item",
        y="nzd",
        title="Microeconomics lab 2: capitation budget constraint",
        labels={"item": "", "nzd": "Illustrative NZD"},
    )
    budget_fig.update_layout(height=360, margin=dict(l=20, r=20, t=56, b=20), showlegend=False)

    scheduled_df = pd.DataFrame(
        [
            {"component": "Gross scheduled payment", "nzd": 98},
            {"component": "Documentation/control cost", "nzd": -11},
            {"component": "Net payment signal", "nzd": 87},
        ]
    )
    scheduled_fig = px.bar(
        scheduled_df,
        x="component",
        y="nzd",
        title="Microeconomics lab 3: scheduled activity payment",
        labels={"component": "", "nzd": "Illustrative NZD per activity"},
    )
    scheduled_fig.update_layout(height=360, margin=dict(l=20, r=20, t=56, b=20), showlegend=False)

    access_rows = []
    for need_band, barrier in (("Low barrier", 20), ("Moderate barrier", 50), ("High barrier", 80)):
        local_share = max(12.0, 72 - 0.45 * barrier)
        digital_share = min(38.0, 18 + 0.16 * barrier)
        deferred_share = max(0.0, 100 - local_share - digital_share)
        for route, share in (
            ("Local in-person", local_share),
            ("Digital / remote", digital_share),
            ("Deferred / unmet", deferred_share),
        ):
            access_rows.append({"need_band": need_band, "route": route, "share": round(share, 1)})
    access_df = pd.DataFrame(access_rows)
    access_fig = px.bar(
        access_df,
        x="need_band",
        y="share",
        color="route",
        title="Microeconomics lab 4: access route mix",
        labels={"need_band": "Need/access-barrier band", "share": "Share of need", "route": "Route"},
    )
    access_fig.update_layout(height=380, margin=dict(l=20, r=20, t=56, b=20))

    return (
        ChartBundle("Marginal supply response", payment_fig, payment_df, "Shows the Streamlit marginal-supply lab as a bounded deterministic curve.", csv_filename="gtpcnz-micro-marginal-supply.csv"),
        ChartBundle("Capitation budget constraint", budget_fig, budget_df, "Shows capitation as a finite envelope against illustrative need pressure.", csv_filename="gtpcnz-micro-capitation-budget.csv"),
        ChartBundle("Scheduled activity payment", scheduled_fig, scheduled_df, "Shows gross scheduled payment, control cost and net signal.", csv_filename="gtpcnz-micro-scheduled-payment.csv"),
        ChartBundle("Access route mix", access_fig, access_df, "Shows local, digital and deferred shares across access-barrier bands.", csv_filename="gtpcnz-micro-access-mix.csv"),
    )


def game_theory_bundles() -> tuple[ChartBundle, ...]:
    audit_rows = []
    quality = 0.62
    place = 0.58
    gain = 0.55
    penalty = 0.60
    for audit_level in range(0, 101, 5):
        audit = audit_level / 100.0
        honest_bonus = strategic_response(0.42 * quality + 0.34 * place + 0.24 * audit, 0.48, 7.0)
        detection_risk = strategic_response(0.55 * audit + 0.25 * penalty + 0.20 * place, 0.46, 7.0)
        gaming_attraction = strategic_response(0.62 * gain + 0.22 * (1 - quality) + 0.16 * (1 - place), 0.42, 7.0)
        audit_rows.extend(
            [
                {"audit_strength": audit_level, "strategy": "Honest payoff", "payoff": round(48 + 34 * honest_bonus + 14 * diminishing_return(gain) - 8 * diminishing_return(audit, 2.0), 1)},
                {"audit_strength": audit_level, "strategy": "Gaming payoff", "payoff": round(48 + 42 * gaming_attraction - 36 * detection_risk - 8 * diminishing_return(audit, 1.8), 1)},
            ]
        )
    audit_df = pd.DataFrame(audit_rows)
    audit_fig = px.line(
        audit_df,
        x="audit_strength",
        y="payoff",
        color="strategy",
        title="Game theory lab 1: claims audit game",
        labels={"audit_strength": "Audit strength", "payoff": "Illustrative payoff", "strategy": "Strategy"},
    )
    audit_fig.update_layout(height=380, margin=dict(l=20, r=20, t=56, b=20))

    coordination_rows = []
    for place_level in range(0, 101, 5):
        place_frac = place_level / 100.0
        coop_signal = 0.46 * place_frac + 0.30 * quality + 0.24 * 0.65
        cherry_signal = 0.52 * (1 - place_frac) + 0.28 * gain + 0.20 * (1 - quality)
        coordination_rows.extend(
            [
                {"place_accountability": place_level, "strategy": "Cooperate", "payoff": round(46 + 48 * strategic_response(coop_signal, 0.48, 7.0), 1)},
                {"place_accountability": place_level, "strategy": "Cherry-pick", "payoff": round(46 + 48 * strategic_response(cherry_signal, 0.32, 7.0), 1)},
            ]
        )
    coordination_df = pd.DataFrame(coordination_rows)
    coordination_fig = px.line(
        coordination_df,
        x="place_accountability",
        y="payoff",
        color="strategy",
        title="Game theory lab 2: payoff and best response",
        labels={"place_accountability": "Place accountability", "payoff": "Illustrative payoff", "strategy": "Strategy"},
    )
    coordination_fig.update_layout(height=380, margin=dict(l=20, r=20, t=56, b=20))

    frontier_rows = []
    for controls in range(0, 101, 5):
        ctrl_frac = controls / 100.0
        risk_signal = 0.48 * gain + 0.30 * (1 - ctrl_frac) + 0.22 * (1 - place)
        access_signal = 0.42 * gain + 0.34 * ctrl_frac + 0.24 * quality
        frontier_rows.append(
            {
                "control_strength": controls,
                "gaming_risk": round(100 * strategic_response(risk_signal, 0.10, 7.0), 1),
                "access_gain": round(100 * strategic_response(access_signal, 0.35, 6.5), 1),
            }
        )
    frontier_df = pd.DataFrame(frontier_rows)
    frontier_fig = px.scatter(
        frontier_df,
        x="access_gain",
        y="gaming_risk",
        color="control_strength",
        title="Game theory lab 3: gaming-risk frontier",
        labels={"access_gain": "Access gain", "gaming_risk": "Gaming risk", "control_strength": "Control strength"},
    )
    frontier_fig.update_layout(height=380, margin=dict(l=20, r=20, t=56, b=20))

    return (
        ChartBundle("Claims audit game", audit_fig, audit_df, "Shows honest versus gaming payoffs as audit strength rises.", csv_filename="gtpcnz-game-audit-payoffs.csv"),
        ChartBundle("Coordination game", coordination_fig, coordination_df, "Shows how place accountability shifts cooperate versus cherry-pick incentives.", csv_filename="gtpcnz-game-coordination-payoffs.csv"),
        ChartBundle("Gaming-risk frontier", frontier_fig, frontier_df, "Shows access gain and gaming risk as controls change.", csv_filename="gtpcnz-game-risk-frontier.csv"),
    )


def simulation_bundle(
    kind: SimulationKind,
    scenario_id: str,
    draws: int = DEFAULT_MONTE_CARLO_DRAWS,
    seed: int = 20260526,
    months: int = 36,
    population_size: int = DEFAULT_ABM_POPULATION,
    educational_settings: dict[str, int] | None = None,
) -> ChartBundle:
    if kind == "uncertainty":
        return uncertainty_bundle(scenario_id=scenario_id, draws=draws, seed=seed)
    if kind == "stock-flow":
        return stock_flow_bundle(scenario_id=scenario_id, months=months)
    if kind == "agent-lens":
        return agent_lens_bundle(scenario_id=scenario_id, population_size=population_size, months=months, seed=seed)
    return educational_bundle(educational_settings)


@lru_cache(maxsize=16)
def live_model_diagnostic_bundles(scenario_id: str = "F4") -> tuple[ChartBundle, ...]:
    tornado_df = run_tornado_sensitivity(scenario_id, delta_step=10.0)
    tornado_fig = go.Figure()
    tornado_fig.add_trace(go.Bar(y=tornado_df["lever"], x=tornado_df["low_delta_viability"], name="Low delta", orientation="h"))
    tornado_fig.add_trace(go.Bar(y=tornado_df["lever"], x=tornado_df["high_delta_viability"], name="High delta", orientation="h"))
    tornado_fig.update_layout(
        barmode="relative",
        height=430,
        margin=dict(l=20, r=20, t=56, b=20),
        title=f"Tornado sensitivity for {scenario_id}",
        xaxis_title="Delta in hybrid viability",
        yaxis_title="Lever",
    )

    waterfall_df = build_waterfall_data(scenario_id)
    waterfall_fig = go.Figure(
        go.Waterfall(
            x=waterfall_df["component"],
            y=waterfall_df["contribution"],
            measure=["relative"] * len(waterfall_df),
        )
    )
    waterfall_fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=56, b=20),
        title=f"Hybrid viability decomposition for {scenario_id}",
        yaxis_title="Weighted contribution",
    )

    variance_df = run_variance_decomposition(scenario_id, draws=80, seed=260526)
    variance_fig = px.bar(
        variance_df,
        x="source",
        y="variance",
        color="source",
        text="proportion",
        title=f"Variance decomposition preview for {scenario_id}",
        labels={"source": "Variance source", "variance": "Variance", "proportion": "Share"},
    )
    variance_fig.update_layout(height=380, margin=dict(l=20, r=20, t=56, b=20), showlegend=False)

    phase_df = run_phase_portrait(scenario_id)
    phase_fig = px.scatter(
        phase_df,
        x="activity_signal",
        y="governance",
        size="magnitude",
        color="hybrid_viability",
        title=f"Phase portrait / vector field for {scenario_id}",
        labels={
            "activity_signal": "Activity signal",
            "governance": "Governance",
            "magnitude": "Gradient magnitude",
            "hybrid_viability": "Hybrid viability",
        },
    )
    phase_fig.update_layout(height=430, margin=dict(l=20, r=20, t=56, b=20))

    return (
        ChartBundle("Tornado sensitivity", tornado_fig, tornado_df, "One-at-a-time sensitivity preview, not a full causal attribution.", csv_filename=f"gtpcnz-{scenario_id}-tornado.csv"),
        ChartBundle("Hybrid viability decomposition", waterfall_fig, waterfall_df, "Shows the additive weighted structure behind hybrid viability.", csv_filename=f"gtpcnz-{scenario_id}-waterfall.csv"),
        ChartBundle("Variance decomposition", variance_fig, variance_df, "Separates structural, subgroup and stochastic variance components in a bounded preview.", csv_filename=f"gtpcnz-{scenario_id}-variance.csv"),
        ChartBundle("Phase portrait", phase_fig, phase_df, "Shows local directional gradients in two-dimensional parameter space.", csv_filename=f"gtpcnz-{scenario_id}-phase-portrait.csv"),
    )


def budget_impact_bundle(scenario_ids: tuple[str, ...] = ("F0", "F4"), enrolled_population: int = 4_500_000) -> ChartBundle:
    table = run_budget_impact(scenario_ids, enrolled_population=enrolled_population)
    chart_df = table[table["year"] != "Total"].astype({"year": int})
    fig = px.line(
        chart_df,
        x="year",
        y="discounted_budget_nzd",
        color="scenario_id",
        markers=True,
        title="Discounted budget impact by scenario with Bass diffusion",
        labels={"year": "Year", "discounted_budget_nzd": "Discounted budget NZD", "scenario_id": "Scenario"},
    )
    fig.update_layout(height=390, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        "Budget impact with Bass diffusion",
        fig,
        table,
        BUDGET_IMPACT_NOTE,
        csv_filename="gtpcnz-budget-impact-diffusion.csv",
    )


def methodology_bundles() -> tuple[ChartBundle, ...]:
    cluster_df = run_outcome_clustering(n_clusters=3)
    cluster_fig = px.scatter(
        cluster_df,
        x="scenario_id",
        y="mean_viability",
        color="cluster",
        size="mean_viability",
        hover_data=["top_metrics"],
        title="Outcome clustering: scenario group and mean viability",
        labels={"scenario_id": "Scenario", "mean_viability": "Mean hybrid viability", "cluster": "Outcome cluster"},
    )
    cluster_fig.update_layout(height=360, margin=dict(l=20, r=20, t=56, b=20))

    meta_df = run_composite_meta_analysis(n_points=36)
    meta_fig = px.scatter(
        meta_df,
        x="access_score",
        y="hospital_pressure_score",
        color="hybrid_viability_score",
        size="gaming_risk_score",
        title="Composite sweep across all benchmark levers",
        labels={"access_score": "Access index", "hospital_pressure_score": "Hospital pressure index", "hybrid_viability_score": "Viability", "gaming_risk_score": "Gaming risk"},
    )
    meta_fig.update_layout(height=390, margin=dict(l=20, r=20, t=56, b=20))

    return (
        ChartBundle("Outcome clustering", cluster_fig, cluster_df, "Groups benchmark scenarios by outcome pattern.", csv_filename="gtpcnz-outcome-clustering.csv"),
        ChartBundle("Composite meta-analysis", meta_fig, meta_df, "Samples benchmark levers to show broad internal model structure.", csv_filename="gtpcnz-composite-meta-analysis.csv"),
    )


def evidence_table() -> pd.DataFrame:
    return build_evidence_table()


def oia_tracker_table() -> pd.DataFrame:
    tracker = load_first_existing(OIA_TRACKER_CANDIDATES)
    if tracker.empty:
        return pd.DataFrame(
            [
                {
                    "Tracker status": "Unavailable in this checkout",
                    "Meaning": "OIA responses and linked data are still required before treating the model as calibrated.",
                }
            ]
        )
    return tracker


def calibration_benchmark_table() -> pd.DataFrame:
    return calibrate_all_scenarios()


def public_aggregate_calibration_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    payload = run_public_aggregate_calibration()
    checks = pd.DataFrame(payload["checks"])
    gates = pd.DataFrame(payload["validation_gates"])
    ppc_payload = payload["posterior_predictive_checks"]
    ppc = pd.DataFrame(
        [
            {
                "ppc_gate_id": ppc_payload.get("ppc_gate_id"),
                "ppc_status": ppc_payload.get("ppc_status"),
                "validation_gate_status": ppc_payload.get("validation_gate_status"),
                "failed_target_count": len(ppc_payload.get("failed_targets", [])),
                "target_row_count": len(ppc_payload.get("target_rows", [])),
                "not_valid_for": "; ".join(str(item) for item in ppc_payload.get("not_valid_for", [])),
                "interpretation_note": ppc_payload.get("interpretation_note"),
            }
        ]
    )
    if not checks.empty:
        checks["diagnostic_status"] = checks["passed"].map({True: "passed", False: "readiness_only"})
    if not gates.empty and "status" in gates.columns:
        gates["diagnostic_status"] = gates["status"]
    if not ppc.empty and "status" in ppc.columns:
        ppc["diagnostic_status"] = ppc["status"]
    return checks, gates, ppc


def calibration_error_bundle() -> ChartBundle:
    checks, _gates, _ppc = public_aggregate_calibration_tables()
    table = checks.copy()
    if table.empty:
        table = pd.DataFrame(
            [
                {
                    "target_id": "no-public-targets-loaded",
                    "relative_error": 0.0,
                    "tolerance": 0.0,
                    "diagnostic_status": "readiness_only",
                    "claim_boundary": FULL_PUBLIC_CAVEAT,
                }
            ]
        )
    fig = px.bar(
        table,
        x="target_id",
        y="relative_error",
        color="diagnostic_status",
        title="Public aggregate calibration diagnostic: relative error by registered target",
        labels={"target_id": "Registered target", "relative_error": "Relative error", "diagnostic_status": "Status"},
    )
    if "tolerance" in table.columns:
        fig.add_trace(
            go.Scatter(
                x=table["target_id"],
                y=table["tolerance"],
                mode="lines+markers",
                name="Tolerance",
            )
        )
    fig.update_layout(height=410, margin=dict(l=20, r=20, t=56, b=120))
    return ChartBundle(
        "Public aggregate calibration diagnostic",
        fig,
        table,
        "Readiness diagnostic only. Failed or source-not-ready targets do not support linked-data calibration, forecasts or causal claims.",
        csv_filename="gtpcnz-public-aggregate-calibration-diagnostic.csv",
        calculation_mode="calibration_readiness_diagnostic",
    )


def structural_uncertainty_bundle() -> ChartBundle:
    payload = build_policy_cockpit_payload()["structural_uncertainty"]
    table = pd.DataFrame(payload["models"])
    fig = px.bar(
        table,
        x="structural_model_id",
        y="score",
        color="plausibility_weight",
        title="Structural uncertainty registry: model variants and plausibility weights",
        labels={"structural_model_id": "Structural model", "score": "Illustrative score", "plausibility_weight": "Plausibility weight"},
    )
    fig.update_layout(height=390, margin=dict(l=20, r=20, t=56, b=110))
    return ChartBundle(
        "Structural uncertainty",
        fig,
        table,
        "Shows the public structural uncertainty registry as a bounded explanation of model-form uncertainty, not empirical confidence intervals.",
        csv_filename="gtpcnz-structural-uncertainty.csv",
        calculation_mode="structural_uncertainty_registry",
    )


def voi_priority_bundle() -> ChartBundle:
    table = run_voi_analysis(draws=80, seed=260526)
    fig = px.bar(
        table,
        x="metric",
        y="evpi",
        color="top_evppi_param",
        text="evpi_pct",
        title="Value of information: evidence-priority teaching view",
        labels={"metric": "Decision metric", "evpi": "EVPI", "top_evppi_param": "Top EVPPI parameter"},
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(height=390, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        "Value of information",
        fig,
        table,
        "Ranks where uncertainty reduction would be most valuable in this benchmark. It is a seeded teaching analysis, not a procurement or policy decision rule.",
        csv_filename="gtpcnz-value-of-information.csv",
        calculation_mode="seeded_voi_teaching_analysis",
        seed=260526,
        caps="80 draws; public reference scenarios only.",
    )


def equity_complexity_bundle(scenario_id: str = "F4") -> ChartBundle:
    table = run_heatmap_matrix(scenario_id)
    cols = [column for column in table.columns if column != "equity_level"]
    fig = px.imshow(
        table.set_index("equity_level")[cols],
        aspect="auto",
        text_auto=True,
        color_continuous_scale="Viridis",
        title=f"Equity by complexity heatmap for {scenario_id}",
        labels={"x": "Complexity level", "y": "Equity level", "color": "Hybrid viability"},
    )
    fig.update_layout(height=390, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        "Equity-complexity heatmap",
        fig,
        table,
        "Shows interaction structure across equity protection and complexity. It is deterministic model structure, not subgroup outcome evidence.",
        csv_filename=f"gtpcnz-{scenario_id}-equity-complexity-heatmap.csv",
    )


def policy_shock_bundle(scenario_id: str = "F4") -> ChartBundle:
    table = run_policy_shock_sequence(
        scenario_id,
        shock_field="governance",
        shock_delta=-20.0,
        post_shock_months=24,
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=table["month"], y=table["baseline_hospital_pressure"], mode="lines", name="Baseline hospital pressure"))
    fig.add_trace(go.Scatter(x=table["month"], y=table["shock_hospital_pressure"], mode="lines", name="Shock hospital pressure"))
    fig.add_trace(go.Scatter(x=table["month"], y=table["baseline_fiscal_pressure"], mode="lines", name="Baseline fiscal pressure", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=table["month"], y=table["shock_fiscal_pressure"], mode="lines", name="Shock fiscal pressure", line=dict(dash="dot")))
    fig.update_layout(
        title=f"Policy shock sequence for {scenario_id}: governance -20",
        xaxis_title="Month",
        yaxis_title="Index value",
        height=420,
        margin=dict(l=20, r=20, t=56, b=20),
        hovermode="x unified",
    )
    return ChartBundle(
        "Policy shock sequence",
        fig,
        table,
        "Shows an abrupt deterministic scenario perturbation. It is a teaching stress sequence, not a forecast of policy implementation.",
        csv_filename=f"gtpcnz-{scenario_id}-policy-shock-sequence.csv",
    )


def scenario_morph_bundle(scenario_id: str = "F4") -> ChartBundle:
    table = create_animation_frames(steps=6, scenario_id=scenario_id)
    fig = px.scatter(
        table,
        x="activity_signal",
        y="governance",
        color="hybrid_viability_score",
        size="hospital_pressure_score",
        animation_frame="frame",
        range_x=[0, 100],
        range_y=[0, 100],
        title=f"Scenario morph: activity signal by governance for {scenario_id}",
        labels={
            "activity_signal": "Activity signal",
            "governance": "Governance",
            "hybrid_viability_score": "Hybrid viability",
            "hospital_pressure_score": "Hospital pressure",
        },
    )
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        "Scenario morph",
        fig,
        table,
        "Animated model-structure sweep over two levers. It demonstrates model geometry, not observed policy dynamics.",
        csv_filename=f"gtpcnz-{scenario_id}-scenario-morph.csv",
    )


def advanced_visual_bundles() -> tuple[ChartBundle, ...]:
    return (
        voi_priority_bundle(),
        structural_uncertainty_bundle(),
        equity_complexity_bundle(),
        policy_shock_bundle(),
        scenario_morph_bundle(),
    )


def interaction_scan_bundle(scenario_id: str = "F4") -> ChartBundle:
    table = run_interaction_scan(scenario_id)
    pivot = table.pivot(index="equity_level", columns="complexity_level", values="hybrid_viability")
    fig = px.imshow(
        pivot,
        aspect="auto",
        text_auto=True,
        color_continuous_scale="Viridis",
        title=f"Interaction scan for {scenario_id}: equity protection by complexity",
        labels={"x": "Complexity level", "y": "Equity level", "color": "Hybrid viability"},
    )
    fig.update_layout(height=390, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        "Interaction scan",
        fig,
        table,
        "Deterministic interaction scan over two teaching levers. It does not estimate subgroup outcomes.",
        csv_filename=f"gtpcnz-{scenario_id}-interaction-scan.csv",
    )


def regime_sweep_bundle(scenario_id: str = "F4") -> ChartBundle:
    table = run_regime_sweep(scenario_id, param_x="activity_signal", param_y="governance")
    fig = px.scatter(
        table,
        x="activity_signal",
        y="governance",
        color="hybrid_viability_score",
        size="gaming_risk_score",
        hover_data=["hospital_pressure_score"],
        color_continuous_scale="Viridis",
        title=f"Regime sweep for {scenario_id}: activity signal by governance",
        labels={"activity_signal": "Activity signal", "governance": "Governance", "hybrid_viability_score": "Hybrid viability", "gaming_risk_score": "Gaming risk"},
    )
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=56, b=20))
    return ChartBundle(
        "Regime sweep",
        fig,
        table,
        "Shows bounded model regimes over two levers. It is a model geometry view, not observed regime evidence.",
        csv_filename=f"gtpcnz-{scenario_id}-regime-sweep.csv",
    )


def public_cockpit_summary() -> tuple[pd.DataFrame, pd.DataFrame]:
    cockpit = build_policy_cockpit_payload()
    sections = pd.DataFrame({"section": cockpit["sections"]})
    chart_rows = [
        {
            "title": chart["title"],
            "unit": chart["unit"],
            "claim_level": chart["claim_level"],
            "calibration_status": chart["calibration_status"],
            "uncertainty_type": chart["uncertainty_type"],
            "source_snapshot_id": chart["source_snapshot_id"],
            "interpretation_note": chart["interpretation_note"],
        }
        for chart in cockpit["charts"]
    ]
    return sections, pd.DataFrame(chart_rows)


def scenario_profile(scenario_id: str) -> pd.DataFrame:
    scenario = get_runtime_scenario(scenario_id)
    idx = calculate_indices(scenario)
    return pd.DataFrame(
        [{"metric": key.replace("_score", "").replace("_", " ").title(), "score": value} for key, value in idx.items()]
    )


def calibration_readiness() -> pd.DataFrame:
    return build_calibration_readiness_table()


def chart_bundle_to_records(bundle: ChartBundle) -> list[dict[str, object]]:
    return bundle.table.to_dict(orient="records")


def dataframe_to_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)
