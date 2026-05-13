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


def build_post_reading_map_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            (
                "01",
                "Are we buying hospital growth by rationing cheaper care upstream?",
                "Executive summary; hospital spillover pathway; scenario interpretation.",
                "Start here; Current state; Reference scenarios.",
                "Argument map and thesis; current reform comparator",
                "Argument map and thesis; current reform comparator",
                "Supply versus hospital-pressure plot; scenario rank chart",
            ),
            (
                "02",
                "Fee-for-service, capitation and blended funding",
                "Funding model explainer; formula appendix.",
                "Funding models module; Toy explainer.",
                "First-six launch post card; funding-model card",
                "Funding comparison toy module; capitation and payment diagram",
                "Toy funding comparison chart; blended-funding explainer",
            ),
            (
                "03",
                "Marginal supply",
                "Microeconomics section.",
                "Microeconomics lab.",
                "First-six launch post card; microeconomics card",
                "Marginal revenue versus marginal cost diagram",
                "Marginal supply simulation",
            ),
            (
                "04",
                "Why formulas do not solve games",
                "Game theory section; controls section.",
                "Game theory lab.",
                "First-six launch post card; game-theory extension card",
                "Payoff matrix; best-response or controls-stack diagram",
                "Toy incentive game; best-response simulation; gaming-risk frontier",
            ),
            (
                "05",
                "Current reform pathway",
                "Current reform comparator section.",
                "Current state; Reference scenarios.",
                "First-six launch post card; current reform card",
                "Current reform pathway map; F0/current reform comparator",
                "F0/current reform comparator selector; scenario comparison chart",
            ),
            (
                "06",
                "What I mean by uncapping primary care funding",
                "Controlled scheduled payment section.",
                "Toy explainer; Microeconomics lab.",
                "First-six launch post card; controlled-payment card",
                "Activity/payment/control simulation; uncapping explanation card",
                "Toy explainer output; scheduled-payment control simulation",
            ),
        ],
        columns=[
            "Post",
            "Public title",
            "Quarto / report destination",
            "Streamlit module",
            "GitHub Pages card",
            "Static visual",
            "Dynamic visual",
        ],
    )


def render_post_guide_and_reading_map() -> None:
    st.subheader("Post guide / Reading map")
    st.markdown(
        """
        This page is the navigation layer for the post and the dashboard.
        It separates the comparator, the model-generated indices, and the toy
        teaching simulations so the reader does not mix them together. The table
        below maps posts 01-06 to the report destination, Streamlit module, and
        public reading-map cards.
        """
    )
    st.dataframe(build_post_reading_map_table(), hide_index=True, width="stretch")
    st.markdown(
        """
        **Reading rules**

        - Start with the comparator: `F0` is the current reform pathway used as the baseline.
        - Treat scenario tables and charts as model-generated indices.
        - Treat the labs as toy teaching simulations only.
        - If you want a claim about New Zealand, you still need real data and validation.
        """
    )
    st.caption(
        "The post guide is a navigation aid. It does not add new evidence or turn the scaffold into a forecast."
    )


def render_microeconomics_activity_response_lab() -> None:
    st.markdown("### Microeconomics lab 1: marginal supply")
    st.markdown(
        """
        **What this shows:** a toy marginal-supply curve for eligible primary
        care activity as the scheduled payment signal changes.

        **How to read it:** move the sliders to see the curve shift up or down.
        A stronger marginal signal raises the toy volume, but the gain tapers at
        higher values.

        **What it does not prove:** this is not a measured New Zealand demand
        elasticity, and it is not a fiscal forecast.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        payment_signal = st.slider(
            "Marginal payment signal",
            0,
            100,
            58,
            key="micro_payment_signal",
            help="Higher values represent a stronger uncapped marginal payment signal for eligible activity.",
        )
        baseline_capacity = st.slider(
            "Baseline appointment capacity",
            40,
            260,
            130,
            key="micro_baseline_capacity",
            help="A higher value means the toy system starts with more capacity before the marginal response is added.",
        )
        response_responsiveness = st.slider(
            "Response responsiveness",
            0,
            100,
            48,
            key="micro_response_responsiveness",
            help="Higher values make the toy response curve steeper at low-to-mid payment levels.",
        )
        admin_friction = st.slider(
            "Administrative friction",
            0,
            100,
            30,
            key="micro_admin_friction",
            help="Higher values flatten the toy response because claims and administration are assumed to be harder.",
        )
    payment_levels = list(range(0, 101, 5))
    curve: list[float] = []
    for level in payment_levels:
        saturation = level / (level + 18 + admin_friction * 0.45) if level else 0.0
        uplift = (response_responsiveness + 18) * saturation * (0.55 + baseline_capacity / 520)
        value = baseline_capacity + uplift - admin_friction * 0.35
        curve.append(round(max(0.0, min(300.0, value)), 1))
    current_index = payment_levels.index(payment_signal - payment_signal % 5)
    current_value = curve[current_index]
    zero_value = curve[0]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=payment_levels,
            y=curve,
            mode="lines",
            name="Toy activity response",
            line=dict(color="#2f6f67", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[payment_levels[current_index]],
            y=[current_value],
            mode="markers",
            name="Current setting",
            marker=dict(size=11, color="#c47a2c"),
        )
    )
    fig.update_layout(
        title="Toy marginal supply response to the scheduled payment signal",
        xaxis_title="Marginal payment signal (0-100)",
        yaxis_title="Illustrative eligible appointments",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Toy appointments", f"{current_value:.1f}")
        metric_cols[1].metric("Increment vs no signal", f"{current_value - zero_value:+.1f}")
        metric_cols[2].metric("Activity ceiling", "300")
        st.caption(
            "This chart is a toy microeconomics simulation. It illustrates marginal supply direction and tapering, not observed response data."
        )


def render_microeconomics_capitation_budget_lab() -> None:
    st.markdown("### Microeconomics lab 2: capitation budget constraint")
    st.markdown(
        """
        **What this shows:** how an enrolment-based budget can still feel tight
        when expected costs and demand growth rise.

        **How to read it:** compare the capitation budget with the expected
        cost line. The gap is the toy headroom or shortfall.

        **What it does not prove:** this is not an estimate of real practice
        margins, and it is not a claim about New Zealand funding adequacy.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        enrolled_patients = st.slider(
            "Enrolled patients",
            200,
            5000,
            1400,
            key="micro_enrolled_patients",
            help="Higher values mean the toy practice carries more enrolled population responsibility.",
        )
        capitation_rate = st.slider(
            "Capitation rate per enrolled patient",
            40,
            240,
            120,
            key="micro_capitation_rate",
            help="Higher values mean the toy budget grows more strongly with enrolment.",
        )
        expected_cost_per_patient = st.slider(
            "Expected cost per patient",
            30,
            260,
            140,
            key="micro_expected_cost_per_patient",
            help="Higher values mean the toy cost base is more expensive to serve.",
        )
        demand_growth = st.slider(
            "Demand growth pressure",
            0,
            100,
            35,
            key="micro_demand_growth",
            help="Higher values make expected demand grow faster than the budget.",
        )
    budget = enrolled_patients * capitation_rate
    expected_cost = enrolled_patients * expected_cost_per_patient * (1 + demand_growth / 220)
    headroom = budget - expected_cost
    chart_df = pd.DataFrame(
        [
            {"Measure": "Capitation budget", "Value": budget},
            {"Measure": "Expected cost", "Value": expected_cost},
            {"Measure": "Budget headroom", "Value": max(0.0, headroom)},
            {"Measure": "Budget shortfall", "Value": max(0.0, -headroom)},
        ]
    )
    fig = px.bar(
        chart_df,
        x="Measure",
        y="Value",
        color="Measure",
        color_discrete_map={
            "Capitation budget": "#2f6f67",
            "Expected cost": "#c47a2c",
            "Budget headroom": "#4f7eb6",
            "Budget shortfall": "#d1495b",
        },
        title="Toy capitation budget constraint",
        labels={"Value": "Illustrative dollars or budget units", "Measure": ""},
    )
    fig.update_layout(showlegend=False, height=420, margin=dict(l=10, r=10, t=45, b=10))
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Budget", f"{budget:,.0f}")
        metric_cols[1].metric("Expected cost", f"{expected_cost:,.0f}")
        metric_cols[2].metric("Headroom", f"{headroom:,.0f}")
        st.caption(
            "This is a toy budget-constraint simulation. It shows capitation pressure and headroom, not a practice finance forecast."
        )


def render_microeconomics_scheduled_payment_lab() -> None:
    st.markdown("### Microeconomics lab 3: scheduled activity payment")
    st.markdown(
        """
        **What this shows:** how an uncapped scheduled payment can still be
        controlled through rules, scope and audit settings.

        **How to read it:** compare the gross scheduled payment with the control
        adjustment and the net toy payment.

        **What it does not prove:** this is not a fiscal estimate and not a
        claim that uncapping removes the need for controls.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        activity_units = st.slider(
            "Eligible activity units",
            0,
            1000,
            420,
            key="micro_activity_units",
            help="Higher values mean more eligible activity is being delivered in the toy system.",
        )
        scheduled_rate = st.slider(
            "Scheduled payment rate",
            0,
            180,
            85,
            key="micro_scheduled_rate",
            help="Higher values mean each eligible unit carries a stronger scheduled payment.",
        )
        control_strength = st.slider(
            "Control strength",
            0,
            100,
            55,
            key="micro_control_strength",
            help="Higher values mean audit and rule controls reduce the net payment more strongly.",
        )
        scope_flexibility = st.slider(
            "Scope flexibility",
            0,
            100,
            60,
            key="micro_scope_flexibility",
            help="Higher values mean the toy system can pay for a wider eligible scope.",
        )
    gross_payment = activity_units * scheduled_rate
    control_adjustment = gross_payment * (0.12 + control_strength / 320)
    scope_bonus = gross_payment * scope_flexibility / 700
    net_payment = gross_payment - control_adjustment + scope_bonus
    payment_df = pd.DataFrame(
        [
            {"Measure": "Gross scheduled payment", "Value": gross_payment},
            {"Measure": "Control adjustment", "Value": max(0.0, control_adjustment)},
            {"Measure": "Scope bonus", "Value": max(0.0, scope_bonus)},
            {"Measure": "Net scheduled payment", "Value": max(0.0, net_payment)},
        ]
    )
    fig = px.bar(
        payment_df,
        x="Measure",
        y="Value",
        color="Measure",
        color_discrete_map={
            "Gross scheduled payment": "#2f6f67",
            "Control adjustment": "#c47a2c",
            "Scope bonus": "#4f7eb6",
            "Net scheduled payment": "#6649a6",
        },
        title="Toy scheduled activity payment with controls",
        labels={"Value": "Illustrative payment units", "Measure": ""},
    )
    fig.update_layout(showlegend=False, height=420, margin=dict(l=10, r=10, t=45, b=10))
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Gross payment", f"{gross_payment:,.0f}")
        metric_cols[1].metric("Control adjustment", f"{control_adjustment:,.0f}")
        metric_cols[2].metric("Net payment", f"{net_payment:,.0f}")
        st.caption(
            "This is a toy scheduled-payment simulation. It shows how payment can be uncapped but still controlled."
        )


def render_microeconomics_access_mix_lab() -> None:
    st.markdown("### Microeconomics lab 4: co-payment / access barrier")
    st.markdown(
        """
        **What this shows:** how co-payment pressure, local in-person capacity,
        digital access and equity protection interact to shape the mix of care
        that is actually available.

        **How to read it:** higher bars mean a larger share of need is met by a
        relevant access route. Watch the deferred share when the barrier is weak.

        **What it does not prove:** this is not a measured service-mix model and
        it is not a substitute for linked utilisation or equity data.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        co_payment = st.slider(
            "Co-payment",
            0,
            100,
            24,
            key="micro_co_payment",
            help="Higher values mean the toy system pushes more price to the patient at the point of care.",
        )
        local_in_person = st.slider(
            "Local in-person care capacity",
            0,
            100,
            64,
            key="micro_local_in_person",
            help="Higher values mean the toy system retains more face-to-face capacity for hands-on care.",
        )
        digital_access = st.slider(
            "Digital access reach",
            0,
            100,
            52,
            key="micro_digital_access",
            help="Higher values mean more care can shift to digital channels where that is clinically suitable.",
        )
        equity_protection = st.slider(
            "Equity protection",
            0,
            100,
            68,
            key="micro_equity_protection",
            help="Higher values reduce the chance that access barriers are shifted onto higher-need groups.",
        )
        travel_barrier = st.slider(
            "Travel and geography friction",
            0,
            100,
            34,
            key="micro_travel_barrier",
            help="Higher values make the toy system more dependent on local in-person capacity.",
        )
    bands = [
        ("Low complexity", 0.92),
        ("Moderate complexity", 1.0),
        ("High complexity", 1.12),
    ]
    rows = []
    for label, complexity in bands:
        barrier_pressure = co_payment * 0.45 + travel_barrier * 0.18 + (100 - equity_protection) * 0.10
        local_share = local_in_person * complexity * (1.0 - travel_barrier / 260) * (1.0 - co_payment / 260)
        digital_share_value = digital_access * (1.0 - (complexity - 0.92) * 0.45) * (0.55 + equity_protection / 180)
        deferred_share = max(0.0, 100 - local_share - digital_share_value - equity_protection * 0.18 + barrier_pressure * 0.22)
        total = local_share + digital_share_value + deferred_share
        if total <= 0:
            total = 1.0
        rows.extend(
            [
                {"Need band": label, "Route": "Local in-person", "Share": round(100 * local_share / total, 1)},
                {"Need band": label, "Route": "Digital-suitable", "Share": round(100 * digital_share_value / total, 1)},
                {"Need band": label, "Route": "Deferred / unmet", "Share": round(100 * deferred_share / total, 1)},
            ]
        )
    mix_df = pd.DataFrame(rows)
    fig = px.bar(
        mix_df,
        x="Need band",
        y="Share",
        color="Route",
        barmode="stack",
        category_orders={"Need band": [band[0] for band in bands]},
        color_discrete_map={
            "Local in-person": "#2f6f67",
            "Digital-suitable": "#5f84c2",
            "Deferred / unmet": "#c47a2c",
        },
        title="Toy co-payment and access barrier mix across need bands",
        labels={"Share": "Share of need met (0-100)", "Need band": ""},
    )
    fig.update_layout(height=440, margin=dict(l=10, r=10, t=45, b=10))
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        covered_share = min(100.0, local_in_person * 0.55 + digital_access * 0.40 + equity_protection * 0.15 - travel_barrier * 0.10 - co_payment * 0.12)
        metric_cols[0].metric("Access coverage", f"{max(0.0, covered_share):.1f}")
        metric_cols[1].metric("Local care emphasis", f"{local_in_person:.0f}")
        metric_cols[2].metric("Deferred pressure", f"{max(0.0, 100 - covered_share):.1f}")
        st.caption(
            "This is a toy service-mix simulation. It shows how co-payments can become access barriers, not observed utilisation or unmet-need rates."
        )


def render_microeconomics_lab() -> None:
    st.subheader("Microeconomics lab")
    st.markdown(
        """
        This lab contains four guided toy simulations. They cover marginal
        supply, capitation budget constraint, scheduled activity payment and
        co-payment / access barrier logic.
        """
    )
    render_microeconomics_activity_response_lab()
    st.divider()
    render_microeconomics_capitation_budget_lab()
    st.divider()
    render_microeconomics_scheduled_payment_lab()
    st.divider()
    render_microeconomics_access_mix_lab()


def render_claims_audit_game_lab() -> None:
    st.markdown("### Game theory lab 1: formulas do not solve games")
    st.markdown(
        """
        **What this shows:** a toy strategic-behaviour game in which the payoff
        to honest claiming and claim inflation changes as audit strength rises.
        It is a reminder that formulas do not solve games by themselves.

        **How to read it:** look for the point where honest claiming overtakes
        gaming. That is the toy threshold at which the strategy mix flips.

        **What it does not prove:** this is not an estimated claim-compliance
        model and it does not predict provider behaviour.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        marginal_gain = st.slider(
            "Marginal gain from extra claims",
            0,
            100,
            62,
            key="game_marginal_gain",
            help="Higher values make gaming more attractive before audit and governance are applied.",
        )
        audit_cost = st.slider(
            "Audit cost / penalty strength",
            0,
            100,
            58,
            key="game_audit_cost",
            help="Higher values make claim inflation less attractive when auditing intensifies.",
        )
        claim_quality = st.slider(
            "Claim rule clarity",
            0,
            100,
            72,
            key="game_claim_quality",
            help="Higher values improve honest claiming and reduce the administrative advantage of gaming.",
        )
        place_accountability = st.slider(
            "Place accountability",
            0,
            100,
            64,
            key="game_place_accountability",
            help="Higher values raise the reputational and system-level cost of gaming within a local population.",
        )
    audit_levels = list(range(0, 101, 5))
    honest = []
    gaming = []
    for audit_level in audit_levels:
        honest_payoff = 52 + marginal_gain * 0.28 + claim_quality * 0.24 + place_accountability * 0.22 - audit_level * 0.08
        gaming_payoff = 52 + marginal_gain * 0.62 + (100 - claim_quality) * 0.12 + (100 - place_accountability) * 0.10 - audit_level * (0.26 + audit_cost / 240)
        honest.append(round(honest_payoff, 1))
        gaming.append(round(gaming_payoff, 1))
    selected_audit = audit_cost - audit_cost % 5
    selected_index = audit_levels.index(selected_audit)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=audit_levels, y=honest, mode="lines", name="Honest claiming", line=dict(color="#2f6f67", width=3)))
    fig.add_trace(go.Scatter(x=audit_levels, y=gaming, mode="lines", name="Claim inflation", line=dict(color="#c47a2c", width=3)))
    fig.add_trace(
        go.Scatter(
            x=[selected_audit],
            y=[gaming[selected_index]],
            mode="markers",
            name="Current audit setting",
            marker=dict(size=11, color="#444"),
        )
    )
    fig.update_layout(
        title="Toy strategic payoffs as audit strength rises",
        xaxis_title="Audit strength (0-100)",
        yaxis_title="Illustrative payoff",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        threshold = next((audit_levels[i] for i, value in enumerate(zip(honest, gaming)) if value[0] >= value[1]), None)
        metric_cols = st.columns(3)
        metric_cols[0].metric("Honest payoff now", f"{honest[selected_index]:.1f}")
        metric_cols[1].metric("Gaming payoff now", f"{gaming[selected_index]:.1f}")
        metric_cols[2].metric("Flip threshold", "Above current" if threshold is not None and threshold <= selected_audit else "Not reached")
        st.caption(
            "This is a toy game-theory simulation. It illustrates incentive direction and threshold logic, not observed compliance rates."
        )


def render_coordination_game_lab() -> None:
    st.markdown("### Game theory lab 2: payoff and best-response")
    st.markdown(
        """
        **What this shows:** a coordination game in which the value of
        cooperating rises when place accountability is stronger. The best
        response is the action with the higher payoff at the selected setting.

        **How to read it:** compare the cooperation line with the cherry-pick
        line. When cooperation sits above cherry-picking, the toy system is
        more stable for whole-population care.

        **What it does not prove:** this is not a calibrated model of provider
        competition or local commissioning outcomes.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        cooperation_gain = st.slider(
            "Cooperation gain",
            0,
            100,
            55,
            key="coordination_cooperation_gain",
            help="Higher values make coordinated whole-population care more attractive.",
        )
        cherry_pick_gain = st.slider(
            "Cherry-pick gain",
            0,
            100,
            48,
            key="coordination_cherry_pick_gain",
            help="Higher values make selective activity more attractive when accountability is weak.",
        )
        equity_protection = st.slider(
            "Equity protection",
            0,
            100,
            64,
            key="coordination_equity_protection",
            help="Higher values raise the cost of leaving harder-to-serve patients behind.",
        )
        scope_flexibility = st.slider(
            "Scope flexibility",
            0,
            100,
            60,
            key="coordination_scope_flexibility",
            help="Higher values improve the ability to cooperate with the right workforce mix.",
        )
        place_accountability = st.slider(
            "Place accountability",
            0,
            100,
            66,
            key="coordination_place_accountability",
            help="Higher values make whole-population coordination more valuable than cherry-picking.",
        )
    place_levels = list(range(0, 101, 5))
    cooperate = []
    cherry_pick = []
    for place_level in place_levels:
        coop_payoff = 50 + cooperation_gain * 0.38 + equity_protection * 0.25 + scope_flexibility * 0.20 + place_level * 0.24
        cherry_payoff = 50 + cherry_pick_gain * 0.56 + (100 - equity_protection) * 0.12 + (100 - scope_flexibility) * 0.10 - place_level * 0.34
        cooperate.append(round(coop_payoff, 1))
        cherry_pick.append(round(cherry_payoff, 1))
    selected_place = place_accountability - place_accountability % 5
    selected_index = place_levels.index(selected_place) if selected_place in place_levels else 0
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=place_levels, y=cooperate, mode="lines", name="Cooperate", line=dict(color="#2f6f67", width=3)))
    fig.add_trace(go.Scatter(x=place_levels, y=cherry_pick, mode="lines", name="Cherry-pick", line=dict(color="#c47a2c", width=3)))
    fig.add_trace(
        go.Scatter(
            x=[selected_place],
            y=[cooperate[selected_index]],
            mode="markers",
            name="Current place setting",
            marker=dict(size=11, color="#444"),
        )
    )
    fig.update_layout(
        title="Toy coordination payoffs as place accountability rises",
        xaxis_title="Place accountability (0-100)",
        yaxis_title="Illustrative payoff",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        threshold = next((place_levels[i] for i, value in enumerate(zip(cooperate, cherry_pick)) if value[0] >= value[1]), None)
        metric_cols = st.columns(3)
        metric_cols[0].metric("Cooperate payoff now", f"{cooperate[selected_index]:.1f}")
        metric_cols[1].metric("Cherry-pick payoff now", f"{cherry_pick[selected_index]:.1f}")
        metric_cols[2].metric("Coordination threshold", f"{threshold}" if threshold is not None else "Not reached")
        st.caption(
            "This is a toy payoff and best-response simulation. It shows how stronger place accountability can shift the incentive balance."
        )


def render_gaming_risk_frontier_lab() -> None:
    st.markdown("### Game theory lab 3: controls and gaming-risk frontier")
    st.markdown(
        """
        **What this shows:** a toy frontier that shows how access gains can be
        traded against gaming risk as controls and monitoring change.

        **How to read it:** move the sliders to see the frontier shift. Lower
        gaming risk is better, but the point is to inspect the trade-off rather
        than chase a single number.

        **What it does not prove:** this is not a measured gaming frontier and
        it is not a policy-effect estimate.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        access_gain = st.slider(
            "Access gain",
            0,
            100,
            58,
            key="game_access_gain",
            help="Higher values mean the toy design is trying to improve access more strongly.",
        )
        control_strength = st.slider(
            "Control strength",
            0,
            100,
            62,
            key="game_control_strength",
            help="Higher values mean rules and monitoring are tighter.",
        )
        monitoring_cost = st.slider(
            "Monitoring cost",
            0,
            100,
            34,
            key="game_monitoring_cost",
            help="Higher values mean the control system is more expensive to run.",
        )
        place_accountability = st.slider(
            "Place accountability",
            0,
            100,
            66,
            key="game_frontier_place_accountability",
            help="Higher values mean local responsibility is stronger.",
        )
    control_levels = list(range(0, 101, 5))
    gaming_risk = []
    access_score = []
    for level in control_levels:
        risk_value = 72 + access_gain * 0.18 - level * 0.36 - monitoring_cost * 0.12 - place_accountability * 0.08
        access_value = 34 + access_gain * 0.42 + level * 0.14 - monitoring_cost * 0.06 + place_accountability * 0.08
        gaming_risk.append(round(max(0.0, min(100.0, risk_value)), 1))
        access_score.append(round(max(0.0, min(100.0, access_value)), 1))
    selected_control = control_strength - control_strength % 5
    selected_index = control_levels.index(selected_control)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=control_levels,
            y=gaming_risk,
            mode="lines",
            name="Gaming risk",
            line=dict(color="#c47a2c", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=control_levels,
            y=access_score,
            mode="lines",
            name="Access gain",
            line=dict(color="#2f6f67", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[selected_control],
            y=[gaming_risk[selected_index]],
            mode="markers",
            name="Current control setting",
            marker=dict(size=11, color="#444"),
        )
    )
    fig.update_layout(
        title="Toy gaming-risk frontier as controls rise",
        xaxis_title="Control strength (0-100)",
        yaxis_title="Illustrative score",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Gaming risk now", f"{gaming_risk[selected_index]:.1f}")
        metric_cols[1].metric("Access gain now", f"{access_score[selected_index]:.1f}")
        metric_cols[2].metric("Control setting", f"{selected_control}")
        st.caption(
            "This is a toy controls-and-risk frontier. It shows the direction of the trade-off, not a measured frontier."
        )


def render_game_theory_lab() -> None:
    st.subheader("Game theory lab")
    st.markdown(
        """
        This lab contains three guided toy incentive simulations. They separate
        formula logic, payoff/best-response logic, and controls/gaming-risk
        frontier logic so the reader can inspect each piece on its own.
        """
    )
    render_claims_audit_game_lab()
    st.divider()
    render_coordination_game_lab()
    st.divider()
    render_gaming_risk_frontier_lab()


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
        "Post guide",
        "Current state",
        "Reference scenarios",
        "Microeconomics lab",
        "Game theory lab",
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
        render_post_guide_and_reading_map()

    with tabs[2]:
        render_current_state()

    with tabs[3]:
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

    with tabs[4]:
        render_microeconomics_lab()

    with tabs[5]:
        render_game_theory_lab()

    with tabs[6]:
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

    with tabs[7]:
        st.subheader("Evidence and Official Information Act tracker")
        tracker = cached_oia_tracker(tuple(str(p) for p in OIA_TRACKER_CANDIDATES))
        if tracker.empty:
            st.info("Evidence/OIA tracker data is not available in this checkout.")
        else:
            st.dataframe(tracker, width="stretch", hide_index=True)
        st.caption("OIA responses and linked data are needed before treating the model as calibrated.")

    with tabs[8]:
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

    with tabs[9]:
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
