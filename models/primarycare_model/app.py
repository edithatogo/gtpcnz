from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.scenario_service import (
    CLAIM_BOUNDARY_TEXT,
    ToySettings,
    build_calibration_readiness_table,
    load_first_existing,
    load_scenario_results,
    score_toy_settings,
    summarise_reference_results,
)


APP_VERSION = "1.8.1"
ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = ROOT / "outputs" / "full-parameterised-summary-results-v1.7.0.csv"
OIA_TRACKER_CANDIDATES = [
    ROOT / "docs" / "audit" / "oia-request-tracker.csv",
    ROOT / "data" / "evidence" / "oia_request_tracker.csv",
]
MODEL_CARD_PATH = ROOT / "docs" / "calibration" / "model-card-v1.7.2.md"
CLAIM_BOUNDARIES_PATH = ROOT / "docs" / "launch" / "claim-boundaries-v1.7.2.md"


@st.cache_data(show_spinner=False)
def cached_scenario_results(path: str) -> pd.DataFrame:
    return load_scenario_results(path)


@st.cache_data(show_spinner=False)
def cached_oia_tracker(paths: tuple[str, ...]) -> pd.DataFrame:
    return load_first_existing(paths)


def caveat_box() -> None:
    st.warning(
        "This is a source-informed parameterised scaffold and educational explainer. "
        "It is not a real-data calibrated forecast and should not be used to claim "
        "precise fiscal savings, hospital-demand reductions, workforce effects, or implementation impacts."
    )


def render_reference_viability(df: pd.DataFrame) -> None:
    fig = px.bar(
        df.sort_values("hybrid_viability_score"),
        x="hybrid_viability_score",
        y="scenario_name",
        orientation="h",
        labels={"hybrid_viability_score": "Hybrid viability index", "scenario_name": ""},
        title="Reference scenario comparison — model-generated index",
    )
    fig.update_layout(height=560, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "These are model-generated indices from the source-informed scaffold, not observed New Zealand outcomes."
    )


def render_reference_scatter(df: pd.DataFrame) -> None:
    fig = px.scatter(
        df,
        x="supply_generation_score",
        y="hospital_pressure_score",
        size="hybrid_viability_score",
        hover_name="scenario_name",
        color="scenario_role",
        labels={
            "supply_generation_score": "Supply generation index",
            "hospital_pressure_score": "Hospital pressure index",
            "scenario_role": "Scenario role",
        },
        title="Supply generation versus hospital pressure",
    )
    fig.update_layout(height=560, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "A lower hospital-pressure score is better. These indices compare policy logics under assumptions; they are not calibrated forecasts."
    )


def render_toy_chart(scores: dict[str, float]) -> None:
    toy_df = pd.DataFrame(
        [
            ("Supply", scores["toy_supply_score"]),
            ("Governance", scores["toy_governance_score"]),
            ("Equity", scores["toy_equity_score"]),
            ("Viability", scores["toy_viability_score"]),
            ("Hospital pressure", scores["toy_hospital_pressure_score"]),
            ("Gaming risk", scores["toy_gaming_risk_score"]),
        ],
        columns=["index", "score"],
    )
    fig = px.bar(
        toy_df,
        x="score",
        y="index",
        orientation="h",
        title="Toy explainer output — not the model forecast",
        labels={"score": "Score", "index": ""},
    )
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")


def render_model_status() -> None:
    st.subheader("Model status")
    st.markdown(
        f"""
        **Status:** {CLAIM_BOUNDARY_TEXT}

        **What the model can do now**

        - Compare the relative logic of funding architectures.
        - Identify load-bearing assumptions.
        - Support stakeholder validation, public explanation and OIA/data planning.
        - Show why uncapped scheduled activity must be paired with controls.

        **What it cannot do yet**

        - Estimate precise emergency department reductions.
        - Estimate fiscal savings.
        - Prove workforce effects.
        - Replace equity review, stakeholder validation or real linked-data calibration.
        """
    )
    st.info(
        "Preferred wording: uncapped at the global activity-envelope level; controlled at the item, scope, audit, clinical-governance and place-accountability level."
    )
    st.markdown(
        f"Model card: `{MODEL_CARD_PATH.relative_to(ROOT)}`  \n"
        f"Claim boundaries: `{CLAIM_BOUNDARIES_PATH.relative_to(ROOT)}`"
    )


def render_app() -> None:
    st.set_page_config(page_title="GTPCNZ", page_icon="🩺", layout="wide")

    st.title("🩺 GTPCNZ: Funding Architecture Explainer")
    st.markdown(
        """
        Explore a source-informed model scaffold about primary care funding architecture
        in Aotearoa New Zealand. The dashboard separates **reference scenarios** from
        a small **toy explainer**. The toy sliders help explain the logic; they do not
        rerun the full parameterised model.
        """
    )
    caveat_box()

    df = cached_scenario_results(str(RESULTS_PATH))

    st.sidebar.header("Toy explainer levers")
    st.sidebar.caption("These sliders are educational. They do not rerun the full scaffold.")
    toy_settings = ToySettings(
        scheduled_benefit_level=st.sidebar.slider(
            "Scheduled fee-for-service / Pay-per-visit benefit level",
            0,
            100,
            55,
            help="Toy lever for the marginal payment signal for eligible primary medical activity.",
        ),
        capitation_support=st.sidebar.slider(
            "Capitation / Subscription population-responsibility support",
            0,
            100,
            70,
            help="Toy lever for baseline enrolled-population support.",
        ),
        place_accountability=st.sidebar.slider(
            "Place-based accountability",
            0,
            100,
            65,
            help="Toy lever for protection against cherry-picking and gaps for hard-to-reach populations.",
        ),
        audit_strength=st.sidebar.slider(
            "Item rules, documentation and audit",
            0,
            100,
            75,
            help="Toy lever for controlling gaming and low-value activity.",
        ),
        equity_protection=st.sidebar.slider(
            "Co-payment and equity protections",
            0,
            100,
            70,
            help="Toy lever for protecting access for high-need groups.",
        ),
        scope_flexibility=st.sidebar.slider(
            "Provider-scope flexibility",
            0,
            100,
            60,
            help="Toy lever for allowing appropriate providers to generate eligible primary care activity.",
        ),
        local_in_person_support=st.sidebar.slider(
            "Local in-person / rural support",
            0,
            100,
            60,
            help="Toy lever for supporting care that cannot be replaced by telehealth alone.",
        ),
    )
    toy_scores = score_toy_settings(toy_settings)

    tab_names = [
        "Start here",
        "Reference scenarios",
        "Toy explainer",
        "Evidence & OIA",
        "Calibration readiness",
        "Glossary",
    ]
    tabs = st.tabs(tab_names)

    with tabs[0]:
        st.subheader("Core thesis")
        st.markdown(
            """
            The proposal is not to abandon capitation. It is to use capitation for what
            it does well — continuity, enrolment, baseline viability and population
            responsibility — while adding an uncapped, scheduled, rules-based
            fee-for-service stream for eligible primary medical activity.

            **Uncapped does not mean uncontrolled.** It means scheduled, rules-based,
            audited, clinically governed and place-accountable.
            """
        )
        render_model_status()

    with tabs[1]:
        st.subheader("Reference scenarios from the scaffold")
        if df.empty:
            st.error(f"Could not find model results at `{RESULTS_PATH.relative_to(ROOT)}`.")
        else:
            st.dataframe(summarise_reference_results(df), hide_index=True, width="stretch")
            col1, col2 = st.columns(2)
            with col1:
                render_reference_viability(df)
            with col2:
                render_reference_scatter(df)

    with tabs[2]:
        st.subheader("Toy explainer")
        st.markdown(
            """
            These sliders are deliberately simple. They are useful for teaching the
            trade-offs, but they are **not** the 70-parameter scaffold and **not a calibrated prediction**.
            """
        )
        metric_cols = st.columns(3)
        metric_cols[0].metric("Toy viability", toy_scores["toy_viability_score"])
        metric_cols[1].metric("Toy supply", toy_scores["toy_supply_score"])
        metric_cols[2].metric("Toy hospital pressure", toy_scores["toy_hospital_pressure_score"])
        render_toy_chart(toy_scores)

    with tabs[3]:
        st.subheader("Evidence and Official Information Act tracker")
        tracker = cached_oia_tracker(tuple(str(p) for p in OIA_TRACKER_CANDIDATES))
        if tracker.empty:
            st.info("Evidence/OIA tracker data is not available in this checkout.")
        else:
            st.dataframe(tracker, width="stretch", hide_index=True)
        st.caption("OIA responses and linked data are needed before treating the model as calibrated.")

    with tabs[4]:
        st.subheader("What would make this a real calibrated model?")
        readiness = build_calibration_readiness_table()
        st.dataframe(readiness, width="stretch", hide_index=True)
        st.markdown(
            """
            The next stage is not more sliders. It is replacing source-informed priors
            with real data on appointments, payments, co-payments, workforce, ambulance
            pathways, emergency department presentations and hospital admissions.
            """
        )

    with tabs[5]:
        st.subheader("Plain-English glossary")
        st.markdown(
            """
            - **Capitation:** baseline funding for enrolled population responsibility.
            - **Fee-for-service:** payment for a specific eligible service.
            - **Uncapped:** no fixed global ceiling on eligible activity.
            - **Controlled:** item rules, clinical governance, documentation, audit and accountability still apply.
            - **Place-based accountability:** responsibility for a whole local population, including hard-to-reach people.
            - **Scaffold:** a transparent model structure that still needs real calibration data.
            - **Reference scenario:** a model-generated scenario already stored in the project outputs.
            - **Toy explainer:** a simplified interactive teaching tool, not the model forecast.
            """
        )
        with st.expander("Learn the 'Big Words'"):
            st.markdown(
                """
                - **Uncapped** means eligible activity is not limited by a fixed global activity envelope.
                - **Controlled** means item rules, provider scope, clinical governance, documentation, audit and place accountability still apply.
                - **Model-generated index** means the number comes from the scaffold logic, not from observed New Zealand outcomes.
                - **Toy explainer** means the slider result is a teaching aid, not a calibrated forecast.
                """
            )

    st.caption(f"GTPCNZ v{APP_VERSION}. Demonstrative explainer only — not a calibrated forecast.")


if __name__ == "__main__":
    render_app()
