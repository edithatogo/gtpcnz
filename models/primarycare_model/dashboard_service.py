from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from models.primarycare_model.runtime_lab import (
    DEFAULT_ABM_POPULATION,
    DEFAULT_MONTE_CARLO_DRAWS,
    GITHUB_PAGES_URL,
    MAX_ABM_POPULATION,
    MAX_MONTE_CARLO_DRAWS,
    MAX_MONTHS,
    SCENARIOS,
    STREAMLIT_URL,
    SUBSTACK_SERIES_URL,
    calculate_indices,
    get_runtime_scenario,
    run_agent_lens,
    run_reference_calculation,
    run_stochastic_uncertainty,
    run_stock_flow_trace,
)
from models.primarycare_model.scenario_service import (
    CLAIM_BOUNDARY_TEXT as CLAIM_BOUNDARY_TEXT,
)
from models.primarycare_model.scenario_service import (
    EDUCATIONAL_LEVER_DEFINITIONS,
    EducationalSettings,
    build_calibration_readiness_table,
    load_scenario_results,
    score_educational_settings,
    summarise_reference_results,
)

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


def public_links() -> dict[str, str]:
    return {
        "github_pages": GITHUB_PAGES_URL,
        "huggingface_space": HUGGINGFACE_SPACE_URL,
        "huggingface_repo": HUGGINGFACE_SPACE_REPO,
        "streamlit_compatibility": STREAMLIT_URL,
        "substack_series": SUBSTACK_SERIES_URL,
    }


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
