from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.scenario_service import (
    CLAIM_BOUNDARY_TEXT,
    TOY_LEVER_DEFINITIONS,
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


def render_reader_guide() -> None:
    st.markdown(
        """
        ### How to read this dashboard

        This dashboard explains the GTPCNZ model scaffold. It sets out the
        argument, the assumptions, and the evidence still needed before anyone
        could make a real-world claim from it.

        Keep this distinction in mind:

        - **Reference scenarios** are precomputed, model-generated indices from the
          source-informed scaffold.
        - **Toy explainer sliders** are simplified teaching controls. They are not
          the 70-parameter model and they do not estimate New Zealand outcomes.

        Read it in this order: start with the thesis, compare the reference
        scenarios, use the toy sliders to learn the mechanism, then check the
        evidence and calibration-readiness tabs before drawing conclusions.
        """
    )


def render_interpretation_rules() -> None:
    st.markdown(
        """
        ### Interpretation rules

        Use these outputs as structured reasoning, not as results from a
        validated forecast model.

        - Higher viability, access, supply and governance indices mean the policy
          logic performs better inside the scaffold assumptions.
        - Lower hospital-pressure and gaming-risk indices are preferable.
        - Differences between scenarios matter more than any single score.
        - A strong scenario still needs implementation design, equity review,
          stakeholder validation and real-data calibration.
        - Do not convert index differences into dollars saved, beds avoided,
          workforce numbers, ED reductions or implementation impacts.
        """
    )


def render_reference_scenario_explainer() -> None:
    st.markdown(
        """
        ### What the reference scenarios mean

        The reference scenarios are not predictions. They are named policy
        architectures used to compare the current reform pathway with alternative
        funding-rule combinations.

        - **F0 current reform comparator:** capitation reweighting, access targets,
          NPCD, digital access, urgent-care work and PHO accountability.
        - **Allocation-only reform:** improves distribution but keeps a weak
          marginal activity signal.
        - **Uncapped activity without enough controls:** tests the gaming and
          low-value-care risk.
        - **Full hybrid upstream architecture:** combines capitation, scheduled
          activity-sensitive payment, place accountability, controls, data and
          equity protections.

        Treat F0 as the comparator. New Zealand is not doing nothing. The
        question is whether the current pathway changes the supply game enough.
        """
    )


def render_toy_explainer_context() -> None:
    st.markdown(
        """
        ### What the toy sliders are for

        The sliders compress the problem into a few visible health-system
        levers. They are not parameters estimated from New Zealand data. They
        are teaching controls that show the direction of the argument.

        Each slider is scaled from **0 to 100**:

        - **0** means the lever is absent or very weak in the toy explanation.
        - **100** means the lever is strong and reliably implemented.

        The toy output is a teaching artefact. It should not be quoted as an
        estimated effect size.
        """
    )


def render_next_steps_context() -> None:
    st.markdown(
        """
        ### What would need to happen next

        A real empirical model would require linked or consistently comparable
        data on appointments, payments, co-payments, provider workforce, ambulance
        pathways, emergency department presentations, admissions, geography and
        equity strata.

        The immediate work is evidence collection and calibration readiness:
        submit or update the OIA requests, check public-source assumptions,
        map available datasets, and test whether the load-bearing assumptions
        survive stakeholder review.
        """
    )


def build_current_reform_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            (
                "Capitation reweighting",
                "Changing how baseline enrolled-population funding is allocated.",
                "May improve fairness of distribution, but does not by itself create a strong payment signal for the next clinically necessary appointment.",
            ),
            (
                "Primary care access target",
                "A public target for getting people timely primary care access.",
                "Useful as a signal, but targets need workforce, funding and data support to change behaviour.",
            ),
            (
                "National Primary Care Dataset",
                "A data programme intended to improve visibility of primary care activity and access.",
                "Important for future calibration; not yet enough on its own to prove the model's assumptions.",
            ),
            (
                "Digital access and telehealth",
                "Online and remote access routes for some care needs.",
                "Can help access, but cannot replace local in-person care for every patient, place or condition.",
            ),
            (
                "Urgent and after-hours care work",
                "Policy attention to alternatives before emergency department presentation.",
                "May matter, but needs funding architecture and workforce support to shift demand safely.",
            ),
            (
                "PHO accountability and commissioning",
                "Use of organisations and contracts to manage enrolled-population responsibility.",
                "Central to place accountability, but pass-through, transaction costs and incentives need verification.",
            ),
        ],
        columns=["Current pathway component", "Plain-English meaning", "Why it matters for this model"],
    )


def build_public_status_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Model status", "Source-informed scaffold", "Ready for explanation; not ready for forecasting."),
            ("Dashboard status", "Educational explainer", "Shows reference indices and toy mechanisms separately."),
            ("Evidence status", "Tracker created", "OIA/data requests still need submission or update."),
            ("Calibration status", "Readiness mapped", "Real linked data and validation tests still required."),
            ("Claim status", "Bounded", "No precise fiscal, hospital-demand, workforce or implementation-impact claims."),
            ("Deployment status", "Public GitHub Pages and Streamlit URLs", "Public surfaces are live and tested."),
        ],
        columns=["Area", "Current state", "What this means"],
    )


def build_figure_inventory_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Static table", "Current reform pathway", "Current state tab", "Explains the real comparator in plain English."),
            ("Static table", "Public project status", "Current state tab", "Shows what is mature and what is still early."),
            ("Static diagram", "Public explainer architecture", "Current state tab", "Shows how reform, the scaffold, the toy explainer, evidence and calibration fit together."),
            ("Dynamic bar chart", "Reference scenario viability", "Reference scenarios tab", "Compares model-generated viability indices."),
            ("Dynamic scatter plot", "Supply generation versus hospital pressure", "Reference scenarios tab", "Shows the trade-off between access/supply and hospital-pressure index."),
            ("Dynamic heatmap", "Scenario score matrix", "Reference scenarios tab", "Shows multiple indices across scenarios at once."),
            ("Dynamic radar chart", "Selected scenario profile", "Reference scenarios tab", "Shows one selected scenario across several dimensions."),
            ("Dynamic bar chart", "Toy explainer output", "Toy explainer tab", "Shows simplified teaching outputs from toy slider settings."),
            ("Dynamic bar chart", "Project readiness", "Current state tab", "Shows maturity of explanation, evidence, validation and calibration work."),
        ],
        columns=["Type", "Figure or table", "Location", "Purpose"],
    )


def build_toy_parameter_dictionary() -> pd.DataFrame:
    return pd.DataFrame(
        [
            (
                definition.public_label,
                definition.health_economics_meaning,
                definition.high_value_meaning,
                definition.toy_output_effect,
            )
            for definition in TOY_LEVER_DEFINITIONS
        ],
        columns=[
            "Toy lever",
            "Health-economics meaning",
            "What a high value means",
            "How it affects the toy output",
        ],
    )


def render_current_state_diagram() -> None:
    st.graphviz_chart(
        """
        digraph {
          graph [rankdir=LR, bgcolor="transparent"];
          node [shape=box, style="rounded,filled", fillcolor="#eef6f4", color="#2f6f67", fontname="Arial"];
          edge [color="#4f6f6a"];

          Reform [label="Current reform pathway\\n(capitation, access target, NPCD, urgent care)"];
          Gap [label="Question tested here\\nDoes this change marginal supply enough?"];
          Scaffold [label="GTPCNZ scaffold\\nsource-informed indices"];
          Toy [label="Toy explainer\\nlearning sliders only"];
          Evidence [label="Evidence and OIA tracker\\nwhat must be verified"];
          Calibration [label="Calibration readiness\\nreal data needed before forecasts"];

          Reform -> Gap -> Scaffold;
          Scaffold -> Toy;
          Scaffold -> Evidence -> Calibration;
        }
        """,
        width="stretch",
    )


def render_readiness_chart(status_df: pd.DataFrame) -> None:
    chart_df = pd.DataFrame(
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
        chart_df,
        x="Illustrative readiness index",
        y="Readiness area",
        orientation="h",
        title="What is mature and what is still early",
        labels={"Illustrative readiness index": "Readiness index (0-100)", "Readiness area": ""},
        range_x=[0, 100],
    )
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "This readiness chart is a project-status visual, not an empirical performance result."
    )


def render_figure_inventory() -> None:
    st.markdown("### Figure and table inventory")
    st.dataframe(build_figure_inventory_table(), hide_index=True, width="stretch")
    st.caption(
        "The dashboard mixes static explanation with dynamic charts. The charts explain model structure and relative indices; they are not empirical performance results."
    )


def render_current_state() -> None:
    st.subheader("Current state of the policy problem and the project")
    st.markdown(
        """
        This is the orientation page for a general reader. It separates three
        things that are easy to confuse: what New Zealand is already doing,
        what this project has built, and what evidence is still missing.
        """
    )

    st.markdown("### Current New Zealand reform pathway used as the comparator")
    st.dataframe(build_current_reform_table(), hide_index=True, width="stretch")
    st.caption(
        "The model treats the current reform pathway as the comparator. It does not pretend no reform is happening."
    )

    st.markdown("### How the public explainer fits together")
    render_current_state_diagram()

    st.markdown("### Public project status")
    status_df = build_public_status_table()
    st.dataframe(status_df, hide_index=True, width="stretch")
    render_readiness_chart(status_df)
    render_figure_inventory()


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
        title="Reference scenario comparison: model-generated index",
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


def render_reference_heatmap(df: pd.DataFrame) -> None:
    heatmap_columns = [
        "hybrid_viability_score",
        "supply_generation_score",
        "equity_legitimacy_score",
        "governance_resilience_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    existing = [column for column in heatmap_columns if column in df.columns]
    if not existing:
        st.info("Scenario heatmap cannot be shown because the expected score columns are unavailable.")
        return

    matrix = df.set_index("scenario_id")[existing].sort_index()
    fig = px.imshow(
        matrix,
        aspect="auto",
        color_continuous_scale="Viridis",
        labels={"x": "Model-generated index", "y": "Reference scenario", "color": "Index score"},
        title="Scenario score matrix: model-generated indices",
    )
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "This heatmap compares patterns across scenarios. It is a model-index view, not observed New Zealand performance data."
    )


def render_scenario_profile_radar(df: pd.DataFrame) -> None:
    required = [
        "scenario_id",
        "scenario_name",
        "hybrid_viability_score",
        "supply_generation_score",
        "equity_legitimacy_score",
        "governance_resilience_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    ]
    missing = [column for column in required if column not in df.columns]
    if missing:
        st.info(f"Scenario profile cannot be shown because columns are missing: {', '.join(missing)}.")
        return

    scenario_options = {
        f"{row.scenario_id} - {row.scenario_name}": row
        for row in df.sort_values("scenario_id").itertuples(index=False)
    }
    selected_label = st.selectbox("Choose a reference scenario profile", list(scenario_options))
    selected = scenario_options[selected_label]

    categories = [
        "Hybrid viability",
        "Supply generation",
        "Equity legitimacy",
        "Governance resilience",
        "Hospital pressure (inverted)",
        "Gaming risk (inverted)",
    ]
    values = [
        selected.hybrid_viability_score,
        selected.supply_generation_score,
        selected.equity_legitimacy_score,
        selected.governance_resilience_score,
        100 - selected.hospital_pressure_score,
        100 - selected.gaming_risk_score,
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=selected.scenario_id,
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=520,
        margin=dict(l=40, r=40, t=45, b=20),
        title=f"Selected scenario profile: {selected.scenario_id}",
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Hospital pressure and gaming risk are inverted here so that larger radar areas mean more favourable scaffold logic."
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
        title="Toy explainer output: not the model forecast",
        labels={"score": "Score", "index": ""},
    )
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")


def render_toy_parameter_dictionary() -> None:
    st.markdown("### Toy parameter dictionary")
    st.dataframe(build_toy_parameter_dictionary(), hide_index=True, width="stretch")
    st.caption(
        "These are qualitative teaching levers, not estimated structural parameters. They make the causal logic visible."
    )


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

    st.title("GTPCNZ: funding architecture explainer")
    st.markdown(
        """
        This is a source-informed model scaffold about primary care funding
        in Aotearoa New Zealand. The dashboard separates reference scenarios from
        a small toy explainer. The toy sliders help explain the logic; they do not
        rerun the full parameterised model.
        """
    )
    caveat_box()
    render_reader_guide()

    df = cached_scenario_results(str(RESULTS_PATH))

    st.sidebar.header("Toy explainer levers")
    st.sidebar.caption(
        "0 means absent/weak; 100 means strong/reliably implemented. These are educational levers, not estimated parameters."
    )
    slider_definitions = {definition.field_name: definition for definition in TOY_LEVER_DEFINITIONS}
    toy_settings = ToySettings(
        scheduled_benefit_level=st.sidebar.slider(
            slider_definitions["scheduled_benefit_level"].public_label,
            0,
            100,
            55,
            help=slider_definitions["scheduled_benefit_level"].slider_help,
        ),
        capitation_support=st.sidebar.slider(
            slider_definitions["capitation_support"].public_label,
            0,
            100,
            70,
            help=slider_definitions["capitation_support"].slider_help,
        ),
        place_accountability=st.sidebar.slider(
            slider_definitions["place_accountability"].public_label,
            0,
            100,
            65,
            help=slider_definitions["place_accountability"].slider_help,
        ),
        audit_strength=st.sidebar.slider(
            slider_definitions["audit_strength"].public_label,
            0,
            100,
            75,
            help=slider_definitions["audit_strength"].slider_help,
        ),
        equity_protection=st.sidebar.slider(
            slider_definitions["equity_protection"].public_label,
            0,
            100,
            70,
            help=slider_definitions["equity_protection"].slider_help,
        ),
        scope_flexibility=st.sidebar.slider(
            slider_definitions["scope_flexibility"].public_label,
            0,
            100,
            60,
            help=slider_definitions["scope_flexibility"].slider_help,
        ),
        local_in_person_support=st.sidebar.slider(
            slider_definitions["local_in_person_support"].public_label,
            0,
            100,
            60,
            help=slider_definitions["local_in_person_support"].slider_help,
        ),
    )
    toy_scores = score_toy_settings(toy_settings)

    tab_names = [
        "Start here",
        "Current state",
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
            it does well: continuity, enrolment, baseline viability and population
            responsibility. It then adds an uncapped, scheduled, rules-based
            fee-for-service stream for eligible primary medical activity.

            **Uncapped does not mean uncontrolled.** It means scheduled, rules-based,
            audited, clinically governed and place-accountable.
            """
        )
        render_model_status()
        render_interpretation_rules()

    with tabs[1]:
        render_current_state()

    with tabs[2]:
        st.subheader("Reference scenarios from the scaffold")
        render_reference_scenario_explainer()
        if df.empty:
            st.error(f"Could not find model results at `{RESULTS_PATH.relative_to(ROOT)}`.")
        else:
            st.dataframe(summarise_reference_results(df), hide_index=True, width="stretch")
            col1, col2 = st.columns(2)
            with col1:
                render_reference_viability(df)
            with col2:
                render_reference_scatter(df)
            st.markdown("### Additional dynamic views")
            render_reference_heatmap(df)
            render_scenario_profile_radar(df)

    with tabs[3]:
        st.subheader("Toy explainer")
        render_toy_explainer_context()
        render_toy_parameter_dictionary()
        st.markdown(
            """
            These sliders are deliberately simple. They teach the trade-offs, but
            they are not the 70-parameter scaffold and not a calibrated prediction.
            """
        )
        metric_cols = st.columns(3)
        metric_cols[0].metric("Toy viability", toy_scores["toy_viability_score"])
        metric_cols[1].metric("Toy supply", toy_scores["toy_supply_score"])
        metric_cols[2].metric("Toy hospital pressure", toy_scores["toy_hospital_pressure_score"])
        render_toy_chart(toy_scores)

    with tabs[4]:
        st.subheader("Evidence and Official Information Act tracker")
        tracker = cached_oia_tracker(tuple(str(p) for p in OIA_TRACKER_CANDIDATES))
        if tracker.empty:
            st.info("Evidence/OIA tracker data is not available in this checkout.")
        else:
            st.dataframe(tracker, width="stretch", hide_index=True)
        st.caption("OIA responses and linked data are needed before treating the model as calibrated.")

    with tabs[5]:
        st.subheader("What would make this a real calibrated model?")
        render_next_steps_context()
        readiness = build_calibration_readiness_table()
        st.dataframe(readiness, width="stretch", hide_index=True)
        st.markdown(
            """
            The next stage is not more sliders. It is replacing source-informed priors
            with real data on appointments, payments, co-payments, workforce, ambulance
            pathways, emergency department presentations and hospital admissions.
            """
        )

    with tabs[6]:
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
        with st.expander("Learn the big words"):
            st.markdown(
                """
                - **Uncapped** means eligible activity is not limited by a fixed global activity envelope.
                - **Controlled** means item rules, provider scope, clinical governance, documentation, audit and place accountability still apply.
                - **Model-generated index** means the number comes from the scaffold logic, not from observed New Zealand outcomes.
                - **Toy explainer** means the slider result is a teaching aid, not a calibrated forecast.
                """
            )

    st.caption(f"GTPCNZ v{APP_VERSION}. Demonstrative explainer only, not a calibrated forecast.")


if __name__ == "__main__":
    render_app()
