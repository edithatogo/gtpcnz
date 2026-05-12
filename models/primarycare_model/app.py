from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


APP_VERSION = "1.7.2"
ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = ROOT / "outputs" / "full-parameterised-summary-results-v1.7.0.csv"
OIA_TRACKER_PATH = ROOT / "docs" / "audit" / "oia-request-tracker.csv"


@st.cache_data(show_spinner=False)
def load_model_results(path: str) -> pd.DataFrame:
    source = Path(path)
    if not source.exists():
        return pd.DataFrame(
            columns=[
                "scenario_name",
                "hybrid_viability_score",
                "supply_generation_score",
                "hospital_pressure_score",
            ]
        )
    return pd.read_csv(source)


@st.cache_data(show_spinner=False)
def load_oia_tracker(path: str) -> pd.DataFrame:
    source = Path(path)
    if not source.exists():
        return pd.DataFrame()
    return pd.read_csv(source)


def score_user_model(benefit_level: int, capitation_weight: int, equity_focus: str) -> dict[str, float]:
    equity_bonus = {"Low": 0, "Medium": 5, "High": 10}[equity_focus]
    supply = benefit_level * 0.8
    pressure = max(0, 100 - (benefit_level * 0.5 + capitation_weight * 0.2 + equity_bonus * 0.5))
    viability = benefit_level * 0.4 + capitation_weight * 0.3 + equity_bonus
    return {
        "supply": round(supply, 1),
        "pressure": round(pressure, 1),
        "viability": round(viability, 1),
    }


def render_viability_chart(df: pd.DataFrame, user_score: float) -> None:
    chart_df = df[["scenario_name", "hybrid_viability_score"]].copy()
    chart_df.loc[len(chart_df)] = ["Your settings", user_score]
    chart_df["type"] = chart_df["scenario_name"].eq("Your settings").map(
        {True: "Your settings", False: "Reference scenario"}
    )

    fig = px.bar(
        chart_df.sort_values("hybrid_viability_score"),
        x="hybrid_viability_score",
        y="scenario_name",
        color="type",
        orientation="h",
        labels={"hybrid_viability_score": "Hybrid viability score", "scenario_name": ""},
        color_discrete_map={"Reference scenario": "#9aa3a7", "Your settings": "#147a4f"},
    )
    fig.update_layout(height=520, legend_title_text="", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)


def render_supply_pressure_chart(df: pd.DataFrame, scores: dict[str, float]) -> None:
    fig = px.scatter(
        df,
        x="supply_generation_score",
        y="hospital_pressure_score",
        hover_name="scenario_name",
        labels={
            "supply_generation_score": "Supply generation score",
            "hospital_pressure_score": "Hospital pressure score",
        },
    )
    fig.add_trace(
        go.Scatter(
            x=[scores["supply"]],
            y=[scores["pressure"]],
            mode="markers+text",
            text=["Your settings"],
            textposition="top center",
            marker=dict(size=14, color="#b42318"),
            name="Your settings",
        )
    )
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)


def render_app() -> None:
    st.set_page_config(page_title="GTPCNZ", page_icon="🩺", layout="wide")

    st.title("🩺 GTPCNZ: The Funding Dashboard")
    st.markdown(
        """
        Explore a demonstrative primary care funding model. The dashboard shows how
        blended payment settings can change supply generation, hospital pressure,
        and overall model viability.
        """
    )
    st.warning(
        "This is a source-informed parameterised scaffold, not a real-data calibrated forecast."
    )

    st.sidebar.header("Change the rules")
    benefit_level = st.sidebar.slider(
        "Pay-per-visit (FFS) Level",
        0,
        100,
        50,
        help="How much extra a provider is paid when they deliver eligible care.",
    )
    capitation_weight = st.sidebar.slider(
        "'Subscription' (Capitation) Weight",
        0,
        100,
        70,
        help="How much baseline funding supports enrolled population responsibility.",
    )
    equity_focus = st.sidebar.select_slider(
        "Equity & Fairness Focus",
        options=["Low", "Medium", "High"],
        value="Medium",
        help="How strongly the model weights targeted support for higher-need groups.",
    )

    df = load_model_results(str(RESULTS_PATH))
    scores = score_user_model(benefit_level, capitation_weight, equity_focus)

    metric_cols = st.columns(3)
    metric_cols[0].metric("Your viability score", scores["viability"])
    metric_cols[1].metric("Estimated supply score", scores["supply"])
    metric_cols[2].metric("Estimated hospital pressure", scores["pressure"])

    tab1, tab2, tab3 = st.tabs(["Simulator", "Evidence tracker", "Plain English"])

    with tab1:
        if df.empty:
            st.error(f"Could not find model results at {RESULTS_PATH}")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Model comparison")
                render_viability_chart(df, scores["viability"])
            with col2:
                st.subheader("Supply vs hospital pressure")
                render_supply_pressure_chart(df, scores)

    with tab2:
        st.subheader("Official Information Act tracker")
        oia_df = load_oia_tracker(str(OIA_TRACKER_PATH))
        if oia_df.empty:
            st.info("OIA tracker data is not available in this checkout.")
        else:
            st.dataframe(oia_df, use_container_width=True, hide_index=True)
        st.caption("OIA responses are needed before treating this as a calibrated real-world model.")

    with tab3:
        st.subheader("Terms used in the model")
        st.markdown(
            """
            - **Capitation:** baseline funding for enrolled population responsibility.
            - **Fee-for-service:** payment for a specific eligible service.
            - **Uncapped:** no fixed activity-envelope ceiling.
            - **Controlled:** rules, documentation, clinical governance, and audit still apply.
            - **Parameterised scaffold:** a transparent model structure that still needs real calibration data.
            """
        )

    with st.expander("Learn the 'Big Words'"):
        st.markdown(
            """
            The core idea is not unlimited spending. The model tests whether primary care
            can be allowed to grow activity when people need care, while controlling that
            growth through item rules, provider eligibility, documentation, audit, and
            place-based accountability.
            """
        )

    st.caption(f"GTPCNZ v{APP_VERSION}. Demonstrative simulator only.")


if __name__ == "__main__":
    render_app()
