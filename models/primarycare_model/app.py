import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.primarycare_model.runtime_lab import (
    DEFAULT_ABM_POPULATION,
    DEFAULT_MONTE_CARLO_DRAWS,
    MAX_ABM_POPULATION,
    MAX_MONTE_CARLO_DRAWS,
    MAX_MONTHS,
    build_waterfall_data,
    calculation_trace,
    clamp,
    diminishing_return,
    format_formula_markdown,
    get_calculation_details,
    model_gap_map,
    run_agent_lens,
    run_cohort_stratified,
    run_ensemble_mc,
    run_heatmap_matrix,
    run_interaction_scan,
    run_phase_portrait,
    run_policy_shock_sequence,
    run_reference_calculation,
    run_regime_sweep,
    run_agent_subgroup_replay,
    run_stress_test_scenarios,
    run_uncertainty_ribbon,
    run_variance_decomposition,
    run_voi_analysis,
    calibrate_all_scenarios,
    build_score_guide_dataframe,
    CALIBRATION_NOTE,
    SCORE_GUIDE_ENTRIES,
    calibrate_distribution,
    CALIBRATION_DIST_NOTE,
    run_budget_impact,
    BUDGET_IMPACT_NOTE,
    CANONICAL_DEFS,
    build_evidence_table,
    run_stochastic_replay,
    run_stochastic_uncertainty,
    run_stock_flow_trace,
    run_tornado_sensitivity,
    strategic_response,
    validate_slider_value,
)
from models.primarycare_model.scenario_service import (
    CLAIM_BOUNDARY_TEXT,
    EDUCATIONAL_LEVER_DEFINITIONS,
    EducationalSettings,
    build_calibration_readiness_table,
    load_first_existing,
    load_scenario_results,
    score_educational_settings,
    summarise_reference_results,
)

APP_VERSION = "1.8.1"
ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = ROOT / "outputs" / "full-parameterised-summary-results-v1.7.0.csv"
OIA_TRACKER_CANDIDATES = [
    ROOT / "docs" / "audit" / "oia-request-tracker.csv",
    ROOT / "data" / "evidence" / "oia_request_tracker.csv",
]


# ── Phase 5: UI helper functions ────────────────────────────────────────


def _render_validation_badge(value: int | float, lower_bound: int, upper_bound: int, label: str) -> None:
    """Render a small inline validation badge beside a slider control."""
    badge, tooltip = validate_slider_value(value, label, lower_bound, upper_bound)
    bg = "#e6ffe6" if badge == "\u2705" else ("#fff3cd" if badge == "\u26a0\ufe0f" else "#f8d7da")
    color = "#155724" if badge == "\u2705" else ("#856404" if badge == "\u26a0\ufe0f" else "#721c24")
    html = f'<span style="background:{bg}; color:{color}; padding:1px 6px; border-radius:8px; font-size:0.75em; display:inline-block;" title="{tooltip}">{badge} {value}</span>'
    st.markdown(html, unsafe_allow_html=True)


def _render_result_manifest_badge(mode: str, scenario_id: str = "") -> None:
    """Render a colored result-manifest badge for a result display."""
    badge_map = {
        "precomputed": ("\U0001f4ca Public-data anchored", "#1e3a5f", "#d4e4f7"),
        "live_deterministic": ("\U0001f4d0 Deterministic", "#2f6f67", "#d5efeb"),
        "seeded_stochastic": ("\U0001f3b2 Stochastic demo", "#7b4c8c", "#e8dff0"),
        "educational": ("\U0001f4da Educational", "#c47a2c", "#fdf0d5"),
    }
    text, fg, bg = badge_map.get(mode, ("\U0001f52c Model-generated", "#333", "#eee"))
    html = f'<span style="background:{bg}; color:{fg}; padding:2px 8px; border-radius:10px; font-size:0.75em; font-weight:500; display:inline-block; margin-right:4px;">{text}</span>'
    if scenario_id:
        html += f'<span style="background:#f0f0f0; color:#555; padding:2px 6px; border-radius:10px; font-size:0.7em; display:inline-block;">{scenario_id}</span>'
    st.markdown(html, unsafe_allow_html=True)


def _render_calculation_expander(
    scenario_id: str | None = None,
    seed: int | None = None,
    draws: int | None = None,
    show_formulas: bool = True,
    result_validation: str | None = None,
) -> None:
    """Render a collapsible "Show calculation details" expander."""
    with st.expander("Show calculation details"):
        if show_formulas:
            st.markdown("**Deterministic formulas used**")
            details = get_calculation_details(scenario_id=scenario_id)
            st.markdown(format_formula_markdown(details))

        if seed is not None or draws is not None:
            meta_lines = []
            if seed is not None:
                meta_lines.append(f"- **Seed**: `{seed}`")
            if draws is not None:
                meta_lines.append(f"- **Draws**: `{draws}`")
            if meta_lines:
                st.markdown("**Stochastic configuration**")
                st.markdown("\n".join(meta_lines))

        if result_validation:
            st.markdown(f"**Result validation**: {result_validation}")

        st.markdown(
            "*This is a demonstrative calculation. It uses model-generated indices, "
            "not calibrated forecasts.*"
        )


def _render_seed_control(key_suffix: str = "") -> int:
    """Render a seed number input and return the current value."""
    return st.number_input(
        "Seed",
        min_value=1,
        max_value=999999,
        value=260526,
        step=1,
        key=f"seed_control_{key_suffix}",
        help="Fixed seed for reproducible stochastic runs. Change to see different perturbation patterns.",
    )


# ── End Phase 5 helpers ─────────────────────────────────────────────────





def render_reader_guide() -> None:
    st.markdown(
        """
        ### How to read this dashboard

        This dashboard explains the GTPCNZ public-data anchored benchmark. It sets out the
        argument, the assumptions, and the evidence still needed before anyone
        could make a real-world claim from it.

        Keep this distinction in mind:

        - **Reference scenarios** are precomputed, model-generated indices from the
          public-data anchored benchmark.
        - **Educational explainer sliders** are simplified teaching controls. They are not
          the 70-parameter model and they do not estimate New Zealand outcomes.

        - **Units used in the dashboard**:
          - model-generated indices use a 0-100 scale and are unitless scores;
          - policy-strength sliders use a 0-100 scale unless a label says otherwise;
          - appointment and activity charts use counts of appointments or eligible activity units;
          - budget and payment charts use illustrative NZD;
          - share charts use percentages of need met.

        Read it in this order: start with the thesis, compare the reference
        scenarios, use the educational sliders to learn the mechanism, then check the
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
          logic performs better inside the benchmark assumptions.
        - Lower hospital-pressure and gaming-risk indices are preferable.
        - Differences between scenarios matter more than any single score.
        - A strong scenario still needs implementation design, equity review,
          stakeholder validation and real-data calibration.
        - Do not convert index differences into dollars saved, beds avoided,
          workforce numbers, ED reductions or implementation impacts.
        """
    )


def render_big_words_expander() -> None:
    with st.expander("Learn the big words"):
        st.markdown(
            """
            - **Uncapped** means eligible activity is not limited by a fixed global activity envelope.
            - **Controlled** means item rules, provider scope, clinical governance, documentation, audit and place accountability still apply.
            - **Model-generated index** means the number comes from the benchmark logic, not from observed New Zealand outcomes.
            - **Educational explainer** means the slider result is a teaching aid, not a calibrated forecast.
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


def render_educational_explainer_context() -> None:
    st.markdown(
        """
        ### What the educational sliders are for

        The sliders compress the problem into a few visible health-system
        levers. They are not parameters estimated from New Zealand data. They
        are teaching controls that show the direction of the argument.

        Each slider is scaled from **0 to 100**:

        - **0** means the lever is absent or very weak in the educational explanation.
        - **100** means the lever is strong and reliably implemented.

        The educational output is a teaching artefact. It should not be quoted as an
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
                "Funding models module; educational explainer.",
                "First-six launch post card; funding-model card",
                "Funding comparison educational module; capitation and payment diagram",
                "Educational funding comparison chart; blended-funding explainer",
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
                "Educational incentive game; best-response simulation; gaming-risk frontier",
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
                "Educational explainer; Microeconomics lab.",
                "First-six launch post card; controlled-payment card",
                "Activity/payment/control simulation; uncapping explanation card",
                "Educational explainer output; scheduled-payment control simulation",
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
    st.subheader("🗺️ Post guide / Reading map")
    st.markdown(
        """
        This page is the navigation layer for the post and the dashboard.
        It separates the comparator, the model-generated indices, and the
        educational teaching simulations so the reader does not mix them
        together. The table
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
        - Treat the labs as educational teaching simulations only.
        - If you want a claim about New Zealand, you still need real data and validation.
        """
    )
    st.caption(
        "The post guide is a navigation aid. It does not add new evidence or turn the benchmark into a forecast."
    )


def render_microeconomics_activity_response_lab() -> None:
    st.markdown("### Microeconomics lab 1: marginal supply")
    with st.expander("How this works - inputs, assumptions, calculation, output"):
        st.markdown("#### Inputs")
        st.markdown(
            "- **Marginal payment signal (0-100):** strength of scheduled payment per activity unit."
            "\n- **Baseline appointment capacity:** starting volume before marginal response."
            "\n- **Response responsiveness (0-100):** steepness of supply response to the payment signal."
            "\n- **Administrative friction (0-100):** claims/compliance costs dampening response."
        )
        st.markdown("#### Assumptions")
        st.markdown(
            "1. Sigmoid supply response (strategic_response function)."
            "\n2. Diminishing returns on responsiveness and friction."
            "\n3. Fixed base capacity; marginal response adds."
            "\n4. Illustrative parameters, not estimated from NZ data."
        )
        st.markdown("#### Calculation")
        st.latex(r"supply = baseline + response_factor * sigmoid(payment_signal) - friction_penalty")
        st.markdown(
            "Sigmoid: `1 / (1 + exp(-steepness * (value - threshold)))`. "
            "Diminishing return: `(1 - exp(-rate * value)) / (1 - exp(-rate))`."
        )
        st.markdown("#### Output")
        st.markdown(
            "- **Appointments per period:** predicted volume at current signal."
            "\n- **Increment vs no signal:** extra supply from the payment signal."
            "\n- **Interpretation:** direction and shape of marginal supply response - "
            "not a forecast of NZ volumes."
        )
    st.markdown(
        """
        **What this shows:** an illustrative marginal-supply curve for eligible primary
        care activity as the scheduled payment signal changes.

        **How to read it:** move the sliders to see the curve shift up or down.
        A stronger marginal signal raises the illustrative volume, but the gain tapers at
        higher values.

        **What it does not prove:** this is not a measured New Zealand demand
        elasticity, and it is not a fiscal forecast.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        payment_signal = st.slider(
            "Marginal payment signal (0–100)",
            0,
            100,
            58,
            key="micro_payment_signal",
            help="Higher values represent a stronger uncapped marginal payment signal for eligible activity.",
        )
        baseline_capacity = st.slider(
            "Baseline appointment capacity (appointments per period)",
            40,
            260,
            130,
            key="micro_baseline_capacity",
            help="A higher value means the illustrative system starts with more capacity before the marginal response is added.",
        )
        response_responsiveness = st.slider(
            "Response responsiveness (0–100)",
            0,
            100,
            48,
            key="micro_response_responsiveness",
            help="Higher values make the illustrative response curve steeper at low-to-mid payment levels.",
        )
        admin_friction = st.slider(
            "Administrative friction (0–100)",
            0,
            100,
            30,
            key="micro_admin_friction",
            help="Higher values flatten the illustrative response because claims and administration are assumed to be harder.",
        )
    payment_levels = list(range(0, 101, 5))
    curve: list[float] = []
    for level in payment_levels:
        # Normalise sliders to 0-1 for shared helpers
        sig_frac = level / 100.0
        resp_frac = response_responsiveness / 100.0
        admin_frac = admin_friction / 100.0
        cap_frac = baseline_capacity / 260.0

        # Nonlinear saturation via strategic_response (sigmoid) replaces
        # raw Michaelis-Menten — both are bounded 0-1 curves with S-shape
        saturation = strategic_response(sig_frac, 0.35 + 0.12 * admin_frac, 5.0)
        # Responsiveness uses diminishing_return so gain tapers at high values
        resp_factor = diminishing_return(resp_frac, 2.5)
        uplift = (resp_factor * 40 + 18) * saturation * (0.55 + cap_frac)
        # Admin-friction penalty uses diminishing_return for nonlinear decay
        admin_penalty = admin_friction * diminishing_return(admin_frac, 2.0) * 0.35
        value = baseline_capacity + uplift - admin_penalty
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
            name="Illustrative activity response",
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
        title="Illustrative marginal supply response to the scheduled payment signal",
        xaxis_title="Marginal payment signal (0-100)",
        yaxis_title="Illustrative appointments per period",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Appointments", f"{current_value:.1f}")
        metric_cols[1].metric("Increment vs no signal", f"{current_value - zero_value:+.1f}")
        metric_cols[2].metric("Maximum appointments", "300")
        st.caption(
            "This chart is an illustrative microeconomics simulation. It uses appointment counts per representative period, not observed response data."
        )


def render_microeconomics_capitation_budget_lab() -> None:
    st.markdown("### Microeconomics lab 2: capitation budget constraint")
    st.markdown(
        """
        **What this shows:** how an enrolment-based budget can still feel tight
        when expected costs and demand growth rise.

        **How to read it:** compare the capitation budget with the expected
        cost line. The gap is the illustrative headroom or shortfall.

        **What it does not prove:** this is not an estimate of real practice
        margins, and it is not a claim about New Zealand funding adequacy.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        enrolled_patients = st.slider(
            "Enrolled patients (count)",
            200,
            5000,
            1400,
            key="micro_enrolled_patients",
            help="Higher values mean the illustrative practice carries more enrolled population responsibility.",
        )
        capitation_rate = st.slider(
            "Capitation rate per enrolled patient (NZD/patient)",
            40,
            240,
            120,
            key="micro_capitation_rate",
            help="Higher values mean the illustrative budget grows more strongly with enrolment.",
        )
        expected_cost_per_patient = st.slider(
            "Expected cost per patient (NZD/patient)",
            30,
            260,
            140,
            key="micro_expected_cost_per_patient",
            help="Higher values mean the illustrative cost base is more expensive to serve.",
        )
        demand_growth = st.slider(
            "Demand growth pressure (0–100)",
            0,
            100,
            35,
            key="micro_demand_growth",
            help="Higher values make expected demand grow faster than the budget.",
        )
    # Budget is a straightforward multiplication, but demand-driven cost growth
    # uses diminishing_return so the cost-pressure signal is nonlinear and bounded
    demand_frac = demand_growth / 100.0
    # Diminishing_return captures the idea that demand growth has a tapering
    # marginal effect on expected costs (nonlinear saturation)
    cost_multiplier = 1.0 + diminishing_return(demand_frac, 2.2) * 0.35
    budget = enrolled_patients * capitation_rate
    expected_cost = enrolled_patients * expected_cost_per_patient * cost_multiplier
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
        title="Illustrative capitation budget constraint (NZD)",
        labels={"Value": "NZD (illustrative)", "Measure": ""},
    )
    fig.update_layout(showlegend=False, height=420, margin=dict(l=10, r=10, t=45, b=10))
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Budget", f"{budget:,.0f}")
        metric_cols[1].metric("Expected cost", f"{expected_cost:,.0f}")
        metric_cols[2].metric("Headroom", f"{headroom:,.0f}")
        st.caption(
            "This is an illustrative budget-constraint simulation. It shows capitation pressure and headroom using NZD-like units, not a practice finance forecast."
        )


def render_microeconomics_scheduled_payment_lab() -> None:
    st.markdown("### Microeconomics lab 3: scheduled activity payment")
    st.markdown(
        """
        **What this shows:** how an uncapped scheduled payment can still be
        controlled through rules, scope and audit settings.

        **How to read it:** compare the gross scheduled payment with the control
        adjustment and the net illustrative payment.

        **What it does not prove:** this is not a fiscal estimate and not a
        claim that uncapping removes the need for controls.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        activity_units = st.slider(
            "Eligible activity units (count)",
            0,
            1000,
            420,
            key="micro_activity_units",
            help="Higher values mean more eligible activity is being delivered in the illustrative system.",
        )
        scheduled_rate = st.slider(
            "Scheduled payment rate (NZD/unit)",
            0,
            180,
            85,
            key="micro_scheduled_rate",
            help="Higher values mean each eligible unit carries a stronger scheduled payment.",
        )
        control_strength = st.slider(
            "Control strength (0–100)",
            0,
            100,
            55,
            key="micro_control_strength",
            help="Higher values mean audit and rule controls reduce the net payment more strongly.",
        )
        scope_flexibility = st.slider(
            "Scope flexibility (0–100)",
            0,
            100,
            60,
            key="micro_scope_flexibility",
            help="Higher values mean the illustrative system can pay for a wider eligible scope.",
        )
    gross_payment = activity_units * scheduled_rate
    # Control adjustment uses strategic_response so the audit effect is
    # S-shaped: weak at low control, steep in mid-range, saturating at high
    ctrl_frac = control_strength / 100.0
    control_rate = strategic_response(ctrl_frac, 0.40, 5.0) * 0.35
    control_adjustment = gross_payment * control_rate
    # Scope bonus uses diminishing_return so flexibility gains taper
    scope_frac = scope_flexibility / 100.0
    scope_rate = diminishing_return(scope_frac, 2.0) * 0.18
    scope_bonus = gross_payment * scope_rate
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
        title="Illustrative scheduled activity payment with controls (NZD)",
        labels={"Value": "NZD (illustrative)", "Measure": ""},
    )
    fig.update_layout(showlegend=False, height=420, margin=dict(l=10, r=10, t=45, b=10))
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Gross payment", f"{gross_payment:,.0f}")
        metric_cols[1].metric("Control adjustment", f"{control_adjustment:,.0f}")
        metric_cols[2].metric("Net payment", f"{net_payment:,.0f}")
        st.caption(
            "This is an illustrative scheduled-payment simulation. It shows how payment can be uncapped but still controlled."
        )


def render_microeconomics_access_mix_lab() -> None:
    st.markdown("### Microeconomics lab 4: co-payment / access barrier")
    with st.expander("How this works - inputs, assumptions, calculation, output"):
        st.markdown("#### Inputs")
        st.markdown("- **Co-payment (0-100):** out-of-pocket cost burden."
            "\\n- **Local in-person capacity (0-100):** face-to-face availability."
            "\\n- **Digital access reach (0-100):** telehealth and online access."
            "\\n- **Equity protection (0-100):** safeguards against access barriers."
            "\\n- **Travel friction (0-100):** distance and transport barriers.")
        st.markdown("#### Assumptions")
        st.markdown("1. Barriers reduce effective access via nonlinear (diminishing_return) functions."
            "\\n2. Digital can partly substitute for in-person care for suitable needs."
            "\\n3. Equity protection offsets the effect of co-payment and travel barriers."
            "\\n4. Deferred share is the residual - need not met through any access route.")
        st.markdown("#### Calculation")
        st.latex(r"local_share = f(capacity, copay, travel)")
        st.latex(r"digital_share = f(access, equity)")
        st.latex(r"deferred = 100 - local_share - digital_share - equity_offset")
        st.markdown("#### Output")
        st.markdown("- **Stacked bar chart:** share of need met through local, digital, or deferred."
            "\\n- **Access coverage metric:** composite score."
            "\\n- **Interpretation:** higher deferred share = access failure.")
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
            "Co-payment (0–100)",
            0,
            100,
            24,
            key="micro_co_payment",
            help="Higher values mean the illustrative system pushes more price to the patient at the point of care.",
        )
        local_in_person = st.slider(
            "Local in-person care capacity (0–100)",
            0,
            100,
            64,
            key="micro_local_in_person",
            help="Higher values mean the illustrative system retains more face-to-face capacity for hands-on care.",
        )
        digital_access = st.slider(
            "Digital access reach (0–100)",
            0,
            100,
            52,
            key="micro_digital_access",
            help="Higher values mean more care can shift to digital channels where that is clinically suitable.",
        )
        equity_protection = st.slider(
            "Equity protection (0–100)",
            0,
            100,
            68,
            key="micro_equity_protection",
            help="Higher values reduce the chance that access barriers are shifted onto higher-need groups.",
        )
        travel_barrier = st.slider(
            "Travel and geography friction (0–100)",
            0,
            100,
            34,
            key="micro_travel_barrier",
            help="Higher values make the illustrative system more dependent on local in-person capacity.",
        )
    bands = [
        ("Low complexity", 0.92),
        ("Moderate complexity", 1.0),
        ("High complexity", 1.12),
    ]
    rows = []
    for label, complexity in bands:
        # Normalise inputs for shared helpers
        copay_frac = co_payment / 100.0
        travel_frac = travel_barrier / 100.0
        equity_frac = equity_protection / 100.0
        local_frac = local_in_person / 100.0
        digital_frac = digital_access / 100.0
        # Barrier pressure uses diminishing_return so co-payment and travel
        # friction have a saturating (nonlinear) effect on access barriers
        barrier_pressure = 100 * (
            diminishing_return(copay_frac, 2.0) * 0.50
            + diminishing_return(travel_frac, 2.0) * 0.20
            + (1.0 - diminishing_return(equity_frac, 2.5)) * 0.12
        )
        # Local share uses strategic_response for nonlinear capacity erosion
        # by co-payment and travel friction
        local_base = local_in_person * complexity * (1.0 - travel_frac * 0.40)
        local_erosion = strategic_response(copay_frac + travel_frac, 0.50, 4.0)
        local_share = local_base * (1.0 - local_erosion * 0.25)
        # Digital share uses diminishing_return for equity-protection boost
        complex_penalty = 1.0 - (complexity - 0.92) * 0.40
        equity_boost = diminishing_return(equity_frac, 2.5) * 0.35
        digital_share_value = digital_access * complex_penalty * (0.50 + equity_boost)
        # Deferred share is the residual after nonlinear interaction
        deferred_share = max(0.0, 100 - local_share - digital_share_value - equity_protection * 0.15 + barrier_pressure * 0.18)
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
        title="Illustrative co-payment and access barrier mix across need bands",
        labels={"Share": "Share of need met (%)", "Need band": ""},
    )
    fig.update_layout(height=440, margin=dict(l=10, r=10, t=45, b=10))
    with chart:
        st.plotly_chart(fig, width="stretch")
        metric_cols = st.columns(3)
        # Access-coverage metric uses diminishing_return for each component
        # so contributions taper: strong local + digital + equity protection
        # nonlinearly reduce the access gap
        cov_local = local_in_person * diminishing_return(local_frac, 2.0) * 0.55
        cov_digital = digital_access * diminishing_return(digital_frac, 2.0) * 0.40
        cov_equity = equity_protection * diminishing_return(equity_frac, 2.5) * 0.15
        cov_barrier = travel_barrier * strategic_response(travel_frac, 0.30, 4.0) * 0.10
        cov_copay = co_payment * strategic_response(copay_frac, 0.25, 4.0) * 0.12
        covered_share = min(100.0, cov_local + cov_digital + cov_equity - cov_barrier - cov_copay)
        metric_cols[0].metric("Access coverage", f"{max(0.0, covered_share):.1f}")
        metric_cols[1].metric("Local care emphasis", f"{local_in_person:.0f}")
        metric_cols[2].metric("Deferred pressure", f"{max(0.0, 100 - covered_share):.1f}")
        st.caption(
            "This is an illustrative service-mix simulation. It shows how co-payments can become access barriers, not observed utilisation or unmet-need rates."
        )


def render_microeconomics_lab() -> None:
    st.subheader("📈 Microeconomics lab")
    st.markdown(
        """
        This lab contains four guided educational simulations. They cover marginal
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

    # ── Combined microeconomics model ────────────────────────────────
    st.markdown("### Combined microeconomics: interaction effects")
    st.markdown(
        "**What this shows:** how the marginal supply, budget, scheduled payment, "
        "and access barrier simulations interact. The sliders below control all "
        "four simulations simultaneously."
    )
    with st.expander("Run combined microeconomics analysis"):
        co_payment_all = st.slider("Co-payment (0-100)", 0, 100, 50, key="combined_copay")
        equity_all = st.slider("Equity protection (0-100)", 0, 100, 50, key="combined_equity")
        if st.button("Run combined analysis", key="combined_micro_btn"):
            with st.spinner("Computing combined microeconomics..."):
                base = get_runtime_scenario("F4")
                modified = replace(base, copayment_burden=float(co_payment_all),
                                   equity_protection=float(equity_all))
                idx = calculate_indices(modified)
                cols = st.columns(3)
                cols[0].metric("Viability", f"{idx['hybrid_viability_score']:.1f}")
                cols[1].metric("Access", f"{idx['access_score']:.1f}")
                cols[2].metric("Equity", f"{idx['equity_legitimacy_score']:.1f}")
                st.caption("Combined effect of co-payment and equity on benchmark indices. Higher access + equity = better.")
                # Cluster outcome
                cl_df = run_outcome_clustering(n_clusters=3)
                st.dataframe(cl_df, hide_index=True, width="stretch")
                st.caption("Outcome clustering shows how scenarios group by combined effects.")
        else:
            st.info("Click to compute combined microeconomics interaction effects.")


def render_claims_audit_game_lab() -> None:
    st.markdown("### Game theory lab 1: formulas do not solve games")
    with st.expander("How this works - inputs, assumptions, calculation, output"):
        st.markdown("#### Inputs")
        st.markdown("- **Marginal gain (0-100):** incentive to inflate claims."
            "\\n- **Audit cost/penalty (0-100):** deterrence from audit."
            "\\n- **Claim rule clarity (0-100):** rule transparency."
            "\\n- **Place accountability (0-100):** population responsibility.")
        st.markdown("#### Assumptions")
        st.markdown("1. Honest and gaming payoffs are sigmoid functions of input signals."
            "\\n2. Detection risk rises with audit via strategic_response."
            "\\n3. The flip threshold shows where honest overtakes gaming.")
        st.markdown("#### Calculation")
        st.latex(r"honest = f(quality, place, audit)")
        st.latex(r"gaming = f(gain, detection, audit)")
        st.markdown("#### Output")
        st.markdown("- **Two payoff lines:** honest vs gaming as audit changes."
            "\\n- **Flip threshold:** audit level where honest wins."
            "\\n- **Interpretation:** formulas alone do not solve gaming.")
    st.markdown(
        """
        **What this shows:** an illustrative strategic-behaviour game in which the payoff
        to honest claiming and claim inflation changes as audit strength rises.
        It is a reminder that formulas do not solve games by themselves.

        **How to read it:** look for the point where honest claiming overtakes
        gaming. That is the illustrative threshold at which the strategy mix flips.

        **What it does not prove:** this is an illustrative pedagogical simulation
        of claim-incentive logic. It is not a claim-compliance model and it does not simulate provider behaviour.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        marginal_gain = st.slider(
            "Marginal gain from extra claims (0–100)",
            0,
            100,
            62,
            key="game_marginal_gain",
            help="Higher values make gaming more attractive before audit and governance are applied.",
        )
        audit_cost = st.slider(
            "Audit cost / penalty strength (0–100)",
            0,
            100,
            58,
            key="game_audit_cost",
            help="Higher values make claim inflation less attractive when auditing intensifies.",
        )
        claim_quality = st.slider(
            "Claim rule clarity (0–100)",
            0,
            100,
            72,
            key="game_claim_quality",
            help="Higher values improve honest claiming and reduce the administrative advantage of gaming.",
        )
        place_accountability = st.slider(
            "Place accountability (0–100)",
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
        audit = audit_level / 100
        gain = marginal_gain / 100
        quality = claim_quality / 100
        place = place_accountability / 100
        penalty = audit_cost / 100
        honest_bonus = strategic_response(0.42 * quality + 0.34 * place + 0.24 * audit, 0.48, 7.0)
        detection_risk = strategic_response(0.55 * audit + 0.25 * penalty + 0.20 * place, 0.46, 7.0)
        gaming_attraction = strategic_response(0.62 * gain + 0.22 * (1 - quality) + 0.16 * (1 - place), 0.42, 7.0)
        honest_payoff = 48 + 34 * honest_bonus + 14 * diminishing_return(gain) - 8 * diminishing_return(audit, 2.0)  # nonlinear audit penalty
        gaming_payoff = 48 + 42 * gaming_attraction - 36 * detection_risk - 8 * diminishing_return(audit, 1.8)  # nonlinear audit penalty
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
        title="Illustrative strategic payoffs as audit strength rises",
        xaxis_title="Audit strength (0-100)",
        yaxis_title="Illustrative payoff",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        threshold = next((audit_levels[i] for i, value in enumerate(zip(honest, gaming, strict=False)) if value[0] >= value[1]), None)
        metric_cols = st.columns(3)
        metric_cols[0].metric("Honest payoff now", f"{honest[selected_index]:.1f}")
        metric_cols[1].metric("Gaming payoff now", f"{gaming[selected_index]:.1f}")
        metric_cols[2].metric("Flip threshold", "Above current" if threshold is not None and threshold <= selected_audit else "Not reached")
        st.caption(
            "This is an illustrative game-theory simulation. It illustrates incentive direction and threshold logic, not observed compliance rates."
        )


def render_coordination_game_lab() -> None:
    st.markdown("### Game theory lab 2: payoff and best-response")
    with st.expander("How this works - inputs, assumptions, calculation, output"):
        st.markdown("#### Inputs")
        st.markdown("- **Cooperation gain (0-100):** benefit of coordination."
            "\\n- **Cherry-pick gain (0-100):** benefit of selective activity."
            "\\n- **Equity protection (0-100):** cost of leaving patients behind."
            "\\n- **Scope flexibility (0-100):** workforce breadth."
            "\\n- **Place accountability (0-100):** population responsibility.")
        st.markdown("#### Assumptions")
        st.markdown("1. Cooperate and cherry-pick payoffs are sigmoid functions."
            "\\n2. Stronger place accountability shifts advantage to cooperation."
            "\\n3. All values are illustrative.")
        st.markdown("#### Calculation")
        st.latex(r"cooperate = f(cooperation, equity, scope, place)")
        st.latex(r"cherry\_pick = f(cherry, equity, scope, place)")
        st.markdown("#### Output")
        st.markdown("- **Two payoff lines:** cooperate vs cherry-pick as place rises."
            "\\n- **Coordination threshold:** place level where cooperation wins.")
    st.markdown(
        """
        **What this shows:** a coordination game in which the value of
        cooperating rises when place accountability is stronger. The best
        response is the action with the higher payoff at the selected setting.

        **How to read it:** compare the cooperation line with the cherry-pick
        line. When cooperation sits above cherry-picking, the illustrative system is
        more stable for whole-population care.

        **What it does not prove:** this is not a calibrated model of provider
        competition or local commissioning outcomes.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        cooperation_gain = st.slider(
            "Cooperation gain (0–100)",
            0,
            100,
            55,
            key="coordination_cooperation_gain",
            help="Higher values make coordinated whole-population care more attractive.",
        )
        cherry_pick_gain = st.slider(
            "Cherry-pick gain (0–100)",
            0,
            100,
            48,
            key="coordination_cherry_pick_gain",
            help="Higher values make selective activity more attractive when accountability is weak.",
        )
        equity_protection = st.slider(
            "Equity protection (0–100)",
            0,
            100,
            64,
            key="coordination_equity_protection",
            help="Higher values raise the cost of leaving harder-to-serve patients behind.",
        )
        scope_flexibility = st.slider(
            "Scope flexibility (0–100)",
            0,
            100,
            60,
            key="coordination_scope_flexibility",
            help="Higher values improve the ability to cooperate with the right workforce mix.",
        )
        place_accountability = st.slider(
            "Place accountability (0–100)",
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
        place = place_level / 100
        coop_signal = 0.38 * cooperation_gain / 100 + 0.25 * equity_protection / 100 + 0.20 * scope_flexibility / 100 + 0.24 * place
        cherry_signal = 0.56 * cherry_pick_gain / 100 + 0.12 * (1 - equity_protection / 100) + 0.10 * (1 - scope_flexibility / 100) - 0.34 * place
        coop_payoff = 46 + 48 * strategic_response(coop_signal, 0.48, 7.0)
        cherry_payoff = 46 + 48 * strategic_response(cherry_signal, 0.32, 7.0)
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
        title="Illustrative coordination payoffs as place accountability rises",
        xaxis_title="Place accountability (0-100)",
        yaxis_title="Illustrative payoff",
        height=420,
        margin=dict(l=10, r=10, t=45, b=10),
    )
    with chart:
        st.plotly_chart(fig, width="stretch")
        threshold = next((place_levels[i] for i, value in enumerate(zip(cooperate, cherry_pick, strict=False)) if value[0] >= value[1]), None)
        metric_cols = st.columns(3)
        metric_cols[0].metric("Cooperate payoff now", f"{cooperate[selected_index]:.1f}")
        metric_cols[1].metric("Cherry-pick payoff now", f"{cherry_pick[selected_index]:.1f}")
        metric_cols[2].metric("Coordination threshold", f"{threshold}" if threshold is not None else "Not reached")
        st.caption(
            "This is an illustrative payoff and best-response simulation. It shows how stronger place accountability can shift the incentive balance."
        )


def render_gaming_risk_frontier_lab() -> None:
    st.markdown("### Game theory lab 3: controls and gaming-risk frontier")
    with st.expander("How this works - inputs, assumptions, calculation, output"):
        st.markdown("#### Inputs")
        st.markdown("- **Access gain (0-100):** policy emphasis on improving access."
            "\\n- **Control strength (0-100):** rules and monitoring intensity."
            "\\n- **Monitoring cost (0-100):** admin cost of controls."
            "\\n- **Place accountability (0-100):** population responsibility.")
        st.markdown("#### Assumptions")
        st.markdown("1. Gaming risk rises with access pressure, falls with controls."
            "\\n2. Access gain is a trade-off with gaming risk."
            "\\n3. The frontier shows the policy trade-off space.")
        st.markdown("#### Calculation")
        st.latex(r"gaming\_risk = f(access, control, place, monitoring)")
        st.latex(r"access\_gain = f(access, control, place, monitoring)")
        st.markdown("#### Output")
        st.markdown("- **Gaming risk and access gain lines** as controls change."
            "\\n- **Interpretation:** the frontier shows the trade-off.")
    st.markdown(
        """
        **What this shows:** an illustrative frontier that shows how access gains can be
        traded against gaming risk as controls and monitoring change.

        **How to read it:** move the sliders to see the frontier shift. Lower
        gaming risk is better, but the point is to inspect the trade-off rather
        than chase a single number.

        **What it does not prove:** this is an illustrative pedagogical frontier
        simulation. It is not a measured gaming frontier and it is not a policy-effect result.
        """
    )
    controls, chart = st.columns([1, 1.8], vertical_alignment="top")
    with controls:
        access_gain = st.slider(
            "Access gain (0–100)",
            0,
            100,
            58,
            key="game_access_gain",
            help="Higher values mean the illustrative design is trying to improve access more strongly.",
        )
        control_strength = st.slider(
            "Control strength (0–100)",
            0,
            100,
            62,
            key="game_control_strength",
            help="Higher values mean rules and monitoring are tighter.",
        )
        monitoring_cost = st.slider(
            "Monitoring cost (0–100)",
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
        control = level / 100
        access_pressure = access_gain / 100
        monitoring = monitoring_cost / 100
        place = place_accountability / 100
        risk_signal = 0.54 * access_pressure - 0.42 * control - 0.16 * place + 0.14 * monitoring
        access_signal = 0.48 * access_pressure + 0.18 * diminishing_return(control) + 0.16 * place - 0.10 * diminishing_return(monitoring, 2.0)  # nonlinear monitoring cost
        risk_value = 100 * strategic_response(risk_signal, 0.10, 7.0)
        access_value = 100 * strategic_response(access_signal, 0.35, 6.5)
        gaming_risk.append(round(clamp(risk_value), 1))
        access_score.append(round(clamp(access_value), 1))
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
        title="Illustrative gaming-risk frontier as controls rise",
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
            "This is an illustrative controls-and-risk frontier. It shows the direction of the trade-off, not a measured frontier."
        )


def render_game_theory_lab() -> None:
    st.subheader("🎲 Game theory lab")
    st.markdown(
        """
        This lab contains three guided educational incentive simulations. They separate
        formula logic, payoff/best-response logic, and controls/gaming-risk
        frontier logic so the reader can inspect each piece on its own.
        """
    )
    render_claims_audit_game_lab()
    st.divider()
    render_coordination_game_lab()
    st.divider()
    render_gaming_risk_frontier_lab()

    # ── Combined game theory model ───────────────────────────────────
    st.markdown("### Combined game theory: interaction effects")
    st.markdown(
        "**What this shows:** how the claims audit, coordination, and gaming-risk "
        "frontier simulations interact. Below you can vary audit and place "
        "accountability to see combined effects on gaming risk and governance."
    )
    with st.expander("Run combined game theory analysis"):
        audit_combined = st.slider("Audit strength (0-100)", 0, 100, 60, key="combined_audit")
        place_combined = st.slider("Place accountability (0-100)", 0, 100, 65, key="combined_place")
        if st.button("Run combined game analysis", key="combined_game_btn"):
            with st.spinner("Computing combined game theory..."):
                base = get_runtime_scenario("F4")
                modified = replace(base, governance=float(audit_combined),
                                   place_accountability=float(place_combined))
                idx = calculate_indices(modified)
                cols = st.columns(3)
                cols[0].metric("Gaming risk", f"{idx['gaming_risk_score']:.1f}")
                cols[1].metric("Governance", f"{idx['governance_resilience_score']:.1f}")
                cols[2].metric("Viability", f"{idx['hybrid_viability_score']:.1f}")
                st.caption("Combined effect of audit and place accountability. Higher governance + lower gaming risk = better.")
                cl_df = run_outcome_clustering(n_clusters=3)
                st.dataframe(cl_df, hide_index=True, width="stretch")
                st.caption("Clustering shows how combined game theory parameters group scenarios.")
        else:
            st.info("Click to compute combined game theory interaction effects.")


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
            ("Model status", "Public-data anchored benchmark", "Ready for explanation; not ready for forecasting."),
            ("Dashboard status", "Educational explainer", "Shows reference indices and educational mechanisms separately."),
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
            ("Static diagram", "Public explainer architecture", "Current state tab", "Shows how reform, the benchmark, the educational explainer, evidence and calibration fit together."),
            ("Dynamic bar chart", "Reference scenario viability", "Reference scenarios tab", "Compares model-generated viability indices."),
            ("Dynamic scatter plot", "Supply generation versus hospital pressure", "Reference scenarios tab", "Shows the trade-off between access/supply and hospital-pressure index."),
            ("Dynamic heatmap", "Scenario score matrix", "Reference scenarios tab", "Shows multiple indices across scenarios at once."),
            ("Dynamic radar chart", "Selected scenario profile", "Reference scenarios tab", "Shows one selected scenario across several dimensions."),
            ("Dynamic bar chart", "Educational explainer output", "Educational explainer tab", "Shows simplified teaching outputs from educational slider settings."),
            ("Dynamic bar chart", "Project readiness", "Current state tab", "Shows maturity of explanation, evidence, validation and calibration work."),
            ("Dynamic tornado chart", "Tornado sensitivity", "Live model lab tab", "Shows OAT sensitivity of hybrid viability to each parameter lever."),
            ("Dynamic waterfall chart", "Hybrid viability decomposition", "Live model lab tab", "Shows weighted component contributions to hybrid viability."),
            ("Dynamic bar chart", "Ensemble Monte Carlo", "Live model lab tab", "Shows seeded stochastic uncertainty across all reference scenarios."),
            ("Dynamic grouped bar chart", "Cohort-stratified comparison", "Live model lab tab", "Compares index scores under low vs high subgroup parameter settings."),
            ("Dynamic bar chart", "Variance decomposition", "Live model lab tab", "Separates structural, subgroup, and stochastic variance contributions."),
            ("Dynamic heatmap", "Scenario × subgroup heatmap", "Live model lab tab", "Shows hybrid viability across equity × complexity levels."),
            ("Dynamic line chart", "Policy shock sequences", "Live model lab tab", "Models abrupt policy changes via stock-flow dynamics."),
            ("Dynamic line chart", "Uncertainty ribbon (stock-flow)", "Live model lab tab", "Shows seeded stochastic spread around hospital pressure path."),
            ("Dynamic violin chart", "Subgroup-stratified violin", "Live model lab tab", "Distribution of viability across equity subgroups."),
            ("Dynamic bar chart", "Stress-test scenarios", "Live model lab tab", "Extreme-but-plausible input scenarios vs baseline."),
            ("Dynamic heatmap", "Interaction scan", "Live model lab tab", "Detects equity × complexity interaction effects."),
            ("Dynamic heatmap", "Regime sweep (2D)", "Live model lab tab", "Maps viability across 2D parameter space."),
            ("Dynamic grouped bar chart", "Agent-based subgroup replay", "Live model lab tab", "Agent-level access patterns under different copayment settings."),
            ("Dynamic scatter chart", "Phase portrait / vector field", "Live model lab tab", "Gradient direction of hybrid viability in 2D parameter space."),
            ("Dynamic 3D surface", "3D payoff surface", "Live model lab tab", "3D surface of hybrid viability across two parameters."),
        ],
        columns=["Type", "Figure or table", "Location", "Purpose"],
    )


def build_educational_parameter_dictionary() -> pd.DataFrame:
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


def render_current_state_diagram() -> None:
    st.graphviz_chart(
        """
        digraph {
          graph [rankdir=LR, bgcolor="transparent"];
          node [shape=box, style="rounded,filled", fillcolor="#eef6f4", color="#2f6f67", fontname="Arial"];
          edge [color="#4f6f6a"];

          Reform [label="Current reform pathway\\n(capitation, access target, NPCD, urgent care)"];
          Gap [label="Question tested here\\nDoes this change marginal supply enough?"];
          Benchmark [label="GTPCNZ benchmark\\npublic-data anchored indices"];
          Educational [label="Educational explainer\\nlearning sliders only"];
          Evidence [label="Evidence and OIA tracker\\nwhat must be verified"];
          Calibration [label="Calibration readiness\\nreal data needed before forecasts"];

          Reform -> Gap -> Benchmark;
          Benchmark -> Educational;
          Benchmark -> Evidence -> Calibration;
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
    st.subheader("🏛️ Current state of the policy problem and the project")
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


@st.cache_data(show_spinner=False)
def cached_live_reference(months: int) -> pd.DataFrame:
    return run_reference_calculation(months=months)


@st.cache_data(show_spinner=False)
def cached_stochastic(scenario_id: str, draws: int, seed: int, sd: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    return run_stochastic_uncertainty(scenario_id=scenario_id, draws=draws, seed=seed, sd=sd)


@st.cache_data(show_spinner=False)
def cached_stock_flow(scenario_id: str, months: int) -> pd.DataFrame:
    return run_stock_flow_trace(scenario_id=scenario_id, months=months)


@st.cache_data(show_spinner=False)
def cached_agent_lens(scenario_id: str, population_size: int, months: int, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    return run_agent_lens(scenario_id=scenario_id, population_size=population_size, months=months, seed=seed)


def caveat_box() -> None:
    st.warning(CLAIM_BOUNDARY_TEXT)


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
        "These are model-generated indices from the public-data anchored benchmark, not observed New Zealand outcomes."
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
            r=[*values, values[0]],
            theta=[*categories, categories[0]],
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
        "Hospital pressure and gaming risk are inverted here so that larger radar areas mean more favourable benchmark logic."
    )


def render_educational_chart(scores: dict[str, float]) -> None:
    educational_df = pd.DataFrame(
        [
            ("Supply", scores["educational_supply_score"]),
            ("Governance", scores["educational_governance_score"]),
            ("Equity", scores["educational_equity_score"]),
            ("Viability", scores["educational_viability_score"]),
            ("Hospital pressure", scores["educational_hospital_pressure_score"]),
            ("Gaming risk", scores["educational_gaming_risk_score"]),
        ],
        columns=["index", "score"],
    )
    fig = px.bar(
        educational_df,
        x="score",
        y="index",
        orientation="h",
        title="Educational explainer output: not the model forecast",
        labels={"score": "Score (0-100)", "index": ""},
    )
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(fig, width="stretch")


def render_educational_parameter_dictionary() -> None:
    st.markdown("### Educational parameter dictionary")
    st.dataframe(build_educational_parameter_dictionary(), hide_index=True, width="stretch")
    st.caption(
        "These are policy-strength levers, not estimated parameters. They make the causal logic visible."
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


def render_live_model_lab(precomputed_df: pd.DataFrame) -> None:
    st.subheader("🔬 Live model lab")
    st.markdown(
        """
        This is the advanced inspection layer. It shows selected calculations being
        performed at runtime, then separates live calculation, cached stochastic
        demo and precomputed reference material. These are demonstrative
        model-generated indices, not linked-data calibrated or patient-level forecasts.
        """
    )

    live_months = st.slider("Live deterministic run length (months)", 12, MAX_MONTHS, 60, 12)
    started = time.perf_counter()
    live_df = cached_live_reference(live_months)
    elapsed_ms = (time.perf_counter() - started) * 1000
    st.caption(
        "Calculation source: live calculation, cached by settings. "
        f"Last runtime: {elapsed_ms:.1f} ms. "
        "The run-length control changes the derived last-12-month public-cost index."
    )

    st.markdown("### Recalculate reference scenarios")
    _render_result_manifest_badge("live_deterministic", f"months={live_months}")
    st.dataframe(
        live_df[
            [
                "rank_by_hybrid_viability",
                "scenario_id",
                "scenario_name",
                "hybrid_viability_score",
                "access_score",
                "supply_generation_score",
                "hospital_pressure_score",
                "gaming_risk_score",
                "mean_last12_public_cost_index",
                "calculation_status",
            ]
        ],
        hide_index=True,
        width="stretch",
    )

    if not precomputed_df.empty:
        compare_columns = [
            "hybrid_viability_score",
            "access_score",
            "supply_generation_score",
            "hospital_pressure_score",
            "gaming_risk_score",
            "mean_last12_public_cost_index",
        ]
        comparison = live_df[["scenario_id", *compare_columns]].merge(
            precomputed_df[["scenario_id", *compare_columns]],
            on="scenario_id",
            suffixes=("_live", "_precomputed"),
        )
        for column in compare_columns:
            comparison[f"{column}_delta"] = (
                comparison[f"{column}_live"].astype(float) - comparison[f"{column}_precomputed"].astype(float)
            ).round(2)
        delta_columns = ["scenario_id", *[f"{column}_delta" for column in compare_columns]]
        st.markdown("### Live versus precomputed delta")
        st.dataframe(comparison[delta_columns], hide_index=True, width="stretch")
        st.caption(
            "Deltas are an audit view of the compact public runtime recipe against the shipped precomputed benchmark output."
        )

    st.markdown("### Calculation trace")
    scenario_options = list(live_df["scenario_id"])
    selected_scenario = st.selectbox("Scenario for calculation trace", scenario_options, index=scenario_options.index("F4") if "F4" in scenario_options else 0)
    trace = calculation_trace(selected_scenario)
    st.dataframe(trace, hide_index=True, width="stretch")
    trace_fig = px.bar(
        trace,
        x="index_value",
        y="calculation",
        orientation="h",
        text="index_value",
        title="Calculation trace: selected model-generated indices",
        labels={"index_value": "Index value (0-100)", "calculation": ""},
        range_x=[0, 100],
    )
    trace_fig.update_layout(height=390, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(trace_fig, width="stretch")

    st.markdown("### Stochastic uncertainty")
    _render_result_manifest_badge("seeded_stochastic", selected_scenario)
    col_a, col_b, col_c = st.columns(3)
    draws = col_a.slider("Monte Carlo draws (count)", 10, MAX_MONTE_CARLO_DRAWS, DEFAULT_MONTE_CARLO_DRAWS, 10)
    seed = col_b.number_input("Seed", min_value=1, max_value=999999, value=260526, step=1)
    sd = col_c.slider("Perturbation width (± fraction)", 0.01, 0.20, 0.08, 0.01)
    draw_frame, uncertainty_summary = cached_stochastic(selected_scenario, draws, int(seed), float(sd))
    st.caption("Calculation source: cached stochastic demo; demonstrative uncertainty only; not an empirical probability.")
    st.dataframe(uncertainty_summary, hide_index=True, width="stretch")
    uncertainty_fig = px.violin(
        draw_frame,
        y="hybrid_viability_score",
        box=True,
        points=False,
        title=f"Seeded uncertainty replay: {selected_scenario} hybrid viability",
        labels={"hybrid_viability_score": "Hybrid viability index"},
    )
    uncertainty_fig.update_layout(height=360, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(uncertainty_fig, width="stretch")
    _render_calculation_expander(
        scenario_id=selected_scenario,
        seed=int(seed),
        draws=int(draws),
        result_validation=f"Perturbation width: {sd:.2f}; seeded run with {draws} draws.",
    )

    st.markdown("### Stochastic replay: fixed-seed versus random-seed")
    _render_result_manifest_badge("seeded_stochastic", selected_scenario)
    replay_cols = st.columns(3)
    replay_draws = replay_cols[0].slider(
        "Replay draws (count)", 10, MAX_MONTE_CARLO_DRAWS, 50, 10, key="replay_draws",
        help="Number of draws for each replay arm.",
    )
    replay_fixed_seed = replay_cols[1].number_input(
        "Fixed seed", min_value=1, max_value=999999, value=260526, step=1, key="replay_fixed_seed",
        help="Fixed seed for reproducible replay.",
    )
    replay_sd = replay_cols[2].slider(
        "Perturbation width (± fraction)", 0.01, 0.20, 0.08, 0.01, key="replay_sd",
        help="Width of the Gaussian perturbation applied to scenario parameters.",
    )
    replay_results = run_stochastic_replay(
        selected_scenario,
        draws=int(replay_draws),
        fixed_seed=int(replay_fixed_seed),
        sd=float(replay_sd),
    )
    st.dataframe(replay_results["summary"], hide_index=True, width="stretch")
    replay_fig = go.Figure()
    replay_fig.add_trace(
        go.Violin(
            y=replay_results["fixed"]["hybrid_viability_score"],
            name="Fixed seed",
            side="negative",
            line_color="#2f6f67",
            box_visible=True,
            meanline_visible=True,
        )
    )
    replay_fig.add_trace(
        go.Violin(
            y=replay_results["random"]["hybrid_viability_score"],
            name="Random seed",
            side="positive",
            line_color="#c47a2c",
            box_visible=True,
            meanline_visible=True,
        )
    )
    replay_fig.update_layout(
        title=f"Stochastic replay comparison: {selected_scenario} hybrid viability",
        yaxis_title="Hybrid viability index",
        height=400,
        margin=dict(l=10, r=10, t=45, b=10),
        violingap=0,
        violingroupgap=0,
        violinmode="overlay",
    )
    st.plotly_chart(replay_fig, width="stretch")
    st.caption(
        "Fixed-seed and random-seed runs use the same perturbation width. "
        "Differences illustrate stochastic uncertainty, not empirical probability."
    )

    st.markdown("### Stock-flow dynamics")
    stock_months = st.slider("Stock-flow months", 6, MAX_MONTHS, 36, 6)
    stock_flow = cached_stock_flow(selected_scenario, stock_months)
    stock_fig = px.line(
        stock_flow,
        x="month",
        y=["unmet_need", "primary_capacity", "hospital_pressure", "fiscal_pressure"],
        title="Live stock-flow trace: unmet need, capacity and pressure",
        labels={"value": "Index value", "month": "Month", "variable": "Trace"},
    )
    stock_fig.update_layout(height=440, margin=dict(l=10, r=10, t=45, b=10), hovermode="x unified")
    st.plotly_chart(stock_fig, width="stretch")
    st.dataframe(stock_flow.tail(12), hide_index=True, width="stretch")

    # ── Wave 1: Tornado sensitivity chart ──────────────────────────────
    st.markdown("### Tornado sensitivity")
    _render_result_manifest_badge("live_deterministic", selected_scenario)
    st.markdown(
        "**What this shows:** how each parameter lever affects hybrid viability "
        "and hospital pressure when perturbed up or down. "
        "Levers ranked by total absolute impact (most influential at top)."
    )
    tornado_step = st.slider(
        "Perturbation step (±)", 1, 50, 10, 1,
        key="tornado_step",
        help="How much each lever is shifted up/down from its baseline.",
    )
    if st.button("Run tornado analysis", key="run_tornado_btn"):
        with st.spinner("Running OAT sensitivity across 12 levers..."):
            tornado_df = run_tornado_sensitivity(selected_scenario, delta_step=float(tornado_step))
        st.dataframe(tornado_df, hide_index=True, width="stretch")
        tornado_fig = go.Figure()
        levers_sorted = tornado_df["lever"].tolist()
        tornado_fig.add_trace(go.Bar(
            y=levers_sorted,
            x=tornado_df["low_delta_viability"],
            orientation="h",
            name="Low perturbation",
            marker_color="#c47a2c",
        ))
        tornado_fig.add_trace(go.Bar(
            y=levers_sorted,
            x=tornado_df["high_delta_viability"],
            orientation="h",
            name="High perturbation",
            marker_color="#2f6f67",
        ))
        tornado_fig.update_layout(
            title=f"Tornado: hybrid viability sensitivity ({selected_scenario})",
            xaxis_title="Delta vs baseline index score",
            yaxis_title="",
            height=480,
            barmode="overlay",
            margin=dict(l=10, r=10, t=45, b=10),
        )
        st.plotly_chart(tornado_fig, width="stretch")
        st.caption(
            "Positive delta means the lever change improves the index. "
            "This is an OAT sensitivity analysis, not a full variance decomposition."
        )
    else:
        st.info("Click 'Run tornado analysis' to compute OAT sensitivity.")

    # ── Wave 1: Waterfall / decomposition chart ─────────────────────────
    st.markdown("### Waterfall: hybrid viability decomposition")
    _render_result_manifest_badge("live_deterministic", selected_scenario)
    st.markdown(
        "**What this shows:** how seven component indices combine to produce "
        "the hybrid viability score."
    )
    if st.button("Show waterfall", key="run_waterfall_btn"):
        wf_df = build_waterfall_data(selected_scenario)
        components = wf_df[~wf_df["is_total"]]["component"].tolist()
        contributions = wf_df[~wf_df["is_total"]]["contribution"].tolist()
        total_val = wf_df[wf_df["is_total"]]["contribution"].values[0]
        waterfall_fig = go.Figure(go.Waterfall(
            name="Contribution", orientation="v",
            measure=["relative"] * len(components) + ["total"],
            x=components + ["Hybrid viability"],
            y=contributions + [total_val],
            decreasing={"marker": {"color": "#c47a2c"}},
            increasing={"marker": {"color": "#2f6f67"}},
            totals={"marker": {"color": "#4f7eb6"}},
        ))
        waterfall_fig.update_layout(
            title=f"Hybrid viability decomposition ({selected_scenario})",
            height=440, margin=dict(l=10, r=10, t=45, b=10),
        )
        st.plotly_chart(waterfall_fig, width="stretch")
        st.dataframe(wf_df, hide_index=True, width="stretch")
        st.caption(
            "The waterfall shows the additive weighted structure of the "
            "hybrid viability formula."
        )
    else:
        st.info("Click 'Show waterfall' to view the decomposition.")

    st.markdown("### Agent lens")
    col_d, col_e, col_f = st.columns(3)
    population_size = col_d.slider("Agent population cap (agents)", 50, MAX_ABM_POPULATION, DEFAULT_ABM_POPULATION, 10)
    agent_months = col_e.slider("Agent months", 3, 24, 12, 3)
    agent_seed = col_f.number_input("Agent seed", min_value=1, max_value=999999, value=260526, step=1)
    agent_frame, agent_summary = cached_agent_lens(selected_scenario, population_size, agent_months, int(agent_seed))
    st.dataframe(agent_summary, hide_index=True, width="stretch")
    agent_fig = px.scatter(
        agent_frame,
        x="access_barrier",
        y="access_probability",
        size="served_contacts",
        color="rural",
        hover_data=["patient_id", "high_need_score", "unmet_attempts"],
        title="Capped agent lens: access barrier versus access probability",
        labels={"access_barrier": "Access barrier", "access_probability": "Access probability", "rural": "Rural flag"},
    )
    agent_fig.update_layout(height=430, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(agent_fig, width="stretch")
    st.caption(
        "The agent lens is a capped teaching view. It lets readers see allocation mechanics, not patient-level forecasts."
    )

    # ── Wave 1: Ensemble Monte Carlo ───────────────────────────────────
    st.markdown("### Ensemble Monte Carlo (all scenarios)")
    _render_result_manifest_badge("seeded_stochastic")
    st.markdown(
        "**What this shows:** seeded stochastic uncertainty across all 10 "
        "reference scenarios. Each scenario is perturbed with the same "
        "random seed for reproducibility."
    )
    ens_draws = st.slider(
        "Ensemble draws per scenario", 10, MAX_MONTE_CARLO_DRAWS, 50, 10,
        key="ens_draws",
        help="Number of Monte Carlo draws per scenario.",
    )
    ens_seed = st.number_input(
        "Ensemble seed", min_value=1, max_value=999999, value=260526, step=1,
        key="ens_seed",
        help="Fixed seed for reproducible ensemble runs.",
    )
    ens_sd = st.slider(
        "Ensemble perturbation (± fraction)", 0.01, 0.20, 0.08, 0.01,
        key="ens_sd",
    )
    if st.button("Run ensemble MC", key="run_ensemble_btn"):
        with st.spinner(f"Running {ens_draws} draws across all scenarios..."):
            ens_df = run_ensemble_mc(draws=int(ens_draws), seed=int(ens_seed), sd=float(ens_sd))
        st.dataframe(ens_df, hide_index=True, width="stretch")
        ens_fig = go.Figure()
        scenarios_ordered = sorted(ens_df["scenario_id"].tolist())
        ens_fig.add_trace(go.Bar(
            x=scenarios_ordered,
            y=ens_df.set_index("scenario_id").loc[scenarios_ordered, "mean"],
            name="Mean hybrid viability",
            marker_color="#2f6f67",
            error_y=dict(
                type="data", symmetric=False,
                array=ens_df.set_index("scenario_id").loc[scenarios_ordered, "p95"].values
                      - ens_df.set_index("scenario_id").loc[scenarios_ordered, "mean"].values,
                arrayminus=ens_df.set_index("scenario_id").loc[scenarios_ordered, "mean"].values
                          - ens_df.set_index("scenario_id").loc[scenarios_ordered, "p05"].values,
                color="#4f7eb6",
            ),
        ))
        ens_fig.update_layout(
            title="Ensemble uncertainty: hybrid viability across scenarios",
            xaxis_title="Scenario",
            yaxis_title="Hybrid viability index (p05/p50/p95)",
            height=440, margin=dict(l=10, r=10, t=45, b=10),
        )
        st.plotly_chart(ens_fig, width="stretch")
        st.caption(
            "Error bars show the 5th-95th percentile range. "
            "These are demonstrative uncertainty bounds, not empirical confidence intervals."
        )
    else:
        st.info("Click 'Run ensemble MC' to compute all-scenario stochastic uncertainty.")

    # ── Wave 1: Cohort-stratified comparison ───────────────────────────
    st.markdown("### Cohort-stratified comparison")
    _render_result_manifest_badge("live_deterministic", selected_scenario)
    st.markdown(
        "**What this shows:** how a subgroup parameter change shifts all "
        "model indices. Select a parameter and two values to compare."
    )
    cohort_field_name = st.selectbox(
        "Subgroup parameter",
        ["equity_protection", "copayment_burden", "complexity", "activity_signal", "place_accountability"],
        index=0,
        key="cohort_field",
    )
    low_val = st.slider(f"Low value for {cohort_field_name}", 0, 100, 25, 5, key="cohort_low")
    high_val = st.slider(f"High value for {cohort_field_name}", 0, 100, 75, 5, key="cohort_high")
    label_low = st.text_input("Label for low group", "Low value", key="cohort_label_low")
    label_high = st.text_input("Label for high group", "High value", key="cohort_label_high")
    if st.button("Compare cohorts", key="run_cohort_btn"):
        cs_df = run_cohort_stratified(
            selected_scenario, subgroup_field=cohort_field_name,
            low_value=float(low_val), high_value=float(high_val),
            label_low=label_low, label_high=label_high,
        )
        st.dataframe(cs_df, hide_index=True, width="stretch")
        cs_fig = go.Figure()
        metrics_list = cs_df["metric"].tolist()
        cs_fig.add_trace(go.Bar(
            x=metrics_list, y=cs_df[label_low], name=label_low, marker_color="#c47a2c",
        ))
        cs_fig.add_trace(go.Bar(
            x=metrics_list, y=cs_df[label_high], name=label_high, marker_color="#2f6f67",
        ))
        cs_fig.update_layout(
            title=f"Cohort comparison: {cohort_field_name} ({selected_scenario})",
            yaxis_title="Index score (0-100)", xaxis_title="",
            barmode="group", height=440, margin=dict(l=10, r=10, t=45, b=150),
        )
        st.plotly_chart(cs_fig, width="stretch")
        st.caption(
            "This comparison shows how changing one parameter shifts all "
            "model indices. It is a deterministic sensitivity test, not a "
            "subgroup forecast."
        )
    else:
        st.info("Click 'Compare cohorts' to run the stratified comparison.")

    st.markdown("### Model map and gaps")
    gap_df = model_gap_map()
    st.dataframe(gap_df, hide_index=True, width="stretch")
    gap_counts = gap_df.groupby("tier", as_index=False).size().rename(columns={"size": "items"})
    gap_fig = px.bar(
        gap_counts,
        x="tier",
        y="items",
        title="Current, comprehensive, SOTA and bleeding-edge map",
        labels={"tier": "Tier", "items": "Mapped assets or gaps"},
    )
    gap_fig.update_layout(height=340, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(gap_fig, width="stretch")

    # ── Wave 2: Variance decomposition ─────────────────────────────────
    st.markdown("### Variance decomposition")
    _render_result_manifest_badge("seeded_stochastic", selected_scenario)
    st.markdown("**What this shows:** separates total hybrid-viability variance into structural (parameter), subgroup (equity), and stochastic (residual) components.")
    if st.button("Run variance decomposition", key="run_vardec_btn"):
        with st.spinner("Running variance decomposition..."):
            vd_df = run_variance_decomposition(selected_scenario, draws=200, seed=260526)
        st.dataframe(vd_df, hide_index=True, width="stretch")
        vd_fig = px.bar(vd_df, x="source", y="variance", color="source", text="proportion",
                        title="Variance decomposition: what drives hybrid viability?",
                        color_discrete_map={"Structural (parameter)": "#2f6f67", "Subgroup (equity)": "#4f7eb6", "Stochastic (residual)": "#c47a2c"})
        vd_fig.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        vd_fig.update_layout(height=400, margin=dict(l=10, r=10, t=45, b=10), showlegend=False)
        st.plotly_chart(vd_fig, width="stretch")
        st.caption("Variance proportions sum to 1.0. Demonstrative seeded decomposition.")
    else:
        st.info("Click to run variance decomposition (200 draws).")

    # ── Wave 2: Heatmap matrix ─────────────────────────────────────────
    st.markdown("### Scenario × subgroup heatmap")
    _render_result_manifest_badge("live_deterministic", selected_scenario)
    st.markdown("**What this shows:** hybrid viability across equity protection and complexity levels.")
    if st.button("Build heatmap matrix", key="run_heatmap_btn"):
        hm_df = run_heatmap_matrix(selected_scenario)
        cols = [c for c in hm_df.columns if c != "equity_level"]
        hm_fig = px.imshow(hm_df.set_index("equity_level")[cols], aspect="auto", text_auto=True,
                           color_continuous_scale="Viridis",
                           labels={"x": "Complexity level", "y": "Equity level", "color": "Viability"},
                           title=f"Scenario × subgroup heatmap ({selected_scenario})")
        hm_fig.update_layout(height=400, margin=dict(l=10, r=10, t=45, b=10))
        st.plotly_chart(hm_fig, width="stretch")
        st.dataframe(hm_df, hide_index=True, width="stretch")
        st.caption("Rows = equity protection, columns = complexity. Higher values = stronger viability.")
    else:
        st.info("Click to build the heatmap matrix.")

    # ── Wave 2: Policy shock sequences ─────────────────────────────────
    st.markdown("### Policy shock sequences")
    _render_result_manifest_badge("live_deterministic", selected_scenario)
    st.markdown("**What this shows:** how an abrupt policy change affects hospital and fiscal pressure over time.")
    shock_field = st.selectbox("Shock parameter", ["activity_signal", "governance", "capitation", "equity_protection", "copayment_burden"], key="shock_field")
    shock_delta = st.slider("Shock change (±)", -50, 50, -20, 5, key="shock_delta")
    shock_months = st.slider("Post-shock months", 12, 48, 24, 6, key="shock_months")
    if st.button("Run shock sequence", key="run_shock_btn"):
        with st.spinner(f"Simulating shock..."):
            shock_df = run_policy_shock_sequence(selected_scenario, shock_field=shock_field, shock_delta=float(shock_delta), post_shock_months=int(shock_months))
        shock_fig = go.Figure()
        shock_fig.add_trace(go.Scatter(x=shock_df["month"], y=shock_df["baseline_hospital_pressure"], mode="lines", name="Baseline", line=dict(color="#4f7eb6", width=2, dash="dash")))
        shock_fig.add_trace(go.Scatter(x=shock_df["month"], y=shock_df["shock_hospital_pressure"], mode="lines", name=f"Shock", line=dict(color="#c47a2c", width=3)))
        shock_fig.update_layout(title=f"Policy shock: hospital pressure", xaxis_title="Month", yaxis_title="Hospital pressure", height=380, margin=dict(l=10, r=10, t=45, b=10), hovermode="x unified")
        st.plotly_chart(shock_fig, width="stretch")
        shock_fig2 = go.Figure()
        shock_fig2.add_trace(go.Scatter(x=shock_df["month"], y=shock_df["baseline_fiscal_pressure"], mode="lines", name="Baseline", line=dict(color="#4f7eb6", width=2, dash="dash")))
        shock_fig2.add_trace(go.Scatter(x=shock_df["month"], y=shock_df["shock_fiscal_pressure"], mode="lines", name=f"Shock", line=dict(color="#c47a2c", width=3)))
        shock_fig2.update_layout(title="Fiscal pressure response", xaxis_title="Month", yaxis_title="Fiscal pressure", height=340, margin=dict(l=10, r=10, t=45, b=10), hovermode="x unified")
        st.plotly_chart(shock_fig2, width="stretch")
        st.caption("Dashed = baseline. Solid = post-shock path. Applied at month 1.")
    else:
        st.info("Click to run the policy shock simulation.")


def render_app() -> None:
    st.set_page_config(page_title="GTPCNZ", page_icon="🩺", layout="wide")

    st.title("GTPCNZ: funding architecture explainer")
    st.markdown(
        """
        This is a public-data anchored benchmark about primary care funding
        in Aotearoa New Zealand. The dashboard separates reference scenarios from
        a small educational explainer. The educational sliders help explain the
        logic; they do not rerun the full parameterised model.
        """
    )
    caveat_box()
    render_reader_guide()
    render_big_words_expander()

    df = cached_scenario_results(str(RESULTS_PATH))

    st.sidebar.markdown("---")
    st.sidebar.header("🎓 Educational explainer")
    st.sidebar.caption(
        "These are teaching controls — they show the direction of the policy logic, "
        "not the 70-parameter benchmark."
    )
    st.sidebar.caption(
        "0 means absent/weak; 100 means strong/reliably implemented. These are policy-strength levers, not estimated parameters."
    )
    st.sidebar.markdown("---")
    slider_definitions = {definition.field_name: definition for definition in EDUCATIONAL_LEVER_DEFINITIONS}
    _sb_level = st.sidebar.slider(
        slider_definitions["scheduled_benefit_level"].public_label,
        slider_definitions["scheduled_benefit_level"].lower_bound,
        slider_definitions["scheduled_benefit_level"].upper_bound,
        slider_definitions["scheduled_benefit_level"].default_value,
        slider_definitions["scheduled_benefit_level"].step,
        help=slider_definitions["scheduled_benefit_level"].slider_help,
    )
    _cap_support = st.sidebar.slider(
        slider_definitions["capitation_support"].public_label,
        slider_definitions["capitation_support"].lower_bound,
        slider_definitions["capitation_support"].upper_bound,
        slider_definitions["capitation_support"].default_value,
        slider_definitions["capitation_support"].step,
        help=slider_definitions["capitation_support"].slider_help,
    )
    _place_acc = st.sidebar.slider(
        slider_definitions["place_accountability"].public_label,
        slider_definitions["place_accountability"].lower_bound,
        slider_definitions["place_accountability"].upper_bound,
        slider_definitions["place_accountability"].default_value,
        slider_definitions["place_accountability"].step,
        help=slider_definitions["place_accountability"].slider_help,
    )
    _audit_st = st.sidebar.slider(
        slider_definitions["audit_strength"].public_label,
        slider_definitions["audit_strength"].lower_bound,
        slider_definitions["audit_strength"].upper_bound,
        slider_definitions["audit_strength"].default_value,
        slider_definitions["audit_strength"].step,
        help=slider_definitions["audit_strength"].slider_help,
    )
    _equity_pro = st.sidebar.slider(
        slider_definitions["equity_protection"].public_label,
        slider_definitions["equity_protection"].lower_bound,
        slider_definitions["equity_protection"].upper_bound,
        slider_definitions["equity_protection"].default_value,
        slider_definitions["equity_protection"].step,
        help=slider_definitions["equity_protection"].slider_help,
    )
    _scope_flex = st.sidebar.slider(
        slider_definitions["scope_flexibility"].public_label,
        slider_definitions["scope_flexibility"].lower_bound,
        slider_definitions["scope_flexibility"].upper_bound,
        slider_definitions["scope_flexibility"].default_value,
        slider_definitions["scope_flexibility"].step,
        help=slider_definitions["scope_flexibility"].slider_help,
    )
    _local_in_person = st.sidebar.slider(
        slider_definitions["local_in_person_support"].public_label,
        slider_definitions["local_in_person_support"].lower_bound,
        slider_definitions["local_in_person_support"].upper_bound,
        slider_definitions["local_in_person_support"].default_value,
        slider_definitions["local_in_person_support"].step,
        help=slider_definitions["local_in_person_support"].slider_help,
    )
    educational_settings = EducationalSettings(
        scheduled_benefit_level=_sb_level,
        capitation_support=_cap_support,
        place_accountability=_place_acc,
        audit_strength=_audit_st,
        equity_protection=_equity_pro,
        scope_flexibility=_scope_flex,
        local_in_person_support=_local_in_person,
    )
    educational_scores = score_educational_settings(educational_settings)

    tab_names = [
        "📖 Start here",
        "🗺️ Post guide",
        "🏛️ Current state",
        "📊 Reference scenarios",
        "📈 Microeconomics lab",
        "🎲 Game theory lab",
        "🔬 Live model lab",
        "🎓 Educational explainer",
        "📋 Evidence & OIA",
        "🎯 Calibration readiness",
        "📖 Glossary",
    ]
    tabs = st.tabs(tab_names)

    with tabs[0]:
        st.subheader("📖 Core thesis")
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
        st.subheader("📊 Reference scenarios from the benchmark")
        # ── Calibrated public-stat parameters ────────────────────────
        st.markdown("### What these scores would mean in NZ terms")
        st.markdown(
            "The table below maps the model's 0\u2013100 benchmark indices onto "
            "real-world New Zealand public-data ranges using linear scaling. "
        )
        _render_result_manifest_badge("live_deterministic")
        cal_df = calibrate_all_scenarios()
        st.dataframe(cal_df, hide_index=True, width="stretch")
        st.caption(CALIBRATION_NOTE)
        st.markdown("")
        st.markdown(
            "For example: F4's access index of ~67 maps to approximately "
            "**4,300 GP visits per 1,000 enrolled patients per year** "
            "under the benchmark\u2019s assumptions. F0's access index of ~42 "
            "maps to approximately **3,900 visits**. The range represents "
            "the model\u2019s logic, not a calibrated prediction."
        )

        # ── Score interpretation guide ───────────────────────────────
        with st.expander("How to interpret each index (TeX formulae, thresholds, components)"):
            st.markdown("#### Index Interpretation Guide")
            st.markdown(
                "Each index is a 0\u2013100 unitless score calculated from a "
                "deterministic linear formula. The table below explains what "
                "each one measures, how to interpret the range, and the exact "
                "TeX formula used."
            )
            for entry in SCORE_GUIDE_ENTRIES:
                key, label, rng, meaning, direction, thresholds, formula, components = entry
                st.markdown(f"**{label}** ({rng})")
                st.markdown(f"- *Meaning:* {meaning}")
                st.markdown(f"- *Higher is:* {direction}")
                st.markdown(f"- *Thresholds:* " + "; ".join(f"{k}: {v}" for k, v in thresholds.items()))
                st.latex(formula)
                st.markdown(f"- *Components:* {components}")
                st.markdown("---")

        # ── Distribution-based calibration (alternative method) ──────
        with st.expander("Distribution-based calibration (beta-distribution method)"):
            st.markdown(
                "**Alternative approach:** instead of linear 0\u2013100 to min-max mapping, "
                "this method draws from beta distributions parametrised to NZ public-data "
                "ranges, with the model index acting as a centering parameter. "
                "This propagates uncertainty and produces plausible ranges."
            )
            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                if st.button("Run distribution calibration", key="run_dist_cal"):
                    with st.spinner("Drawing from beta distributions..."):
                        dist_rows = []
                        for sc in SCENARIOS:
                            idx = calculate_indices(sc)
                            cal = calibrate_distribution(idx)
                            dist_rows.append({
                                "scenario_id": sc.scenario_id,
                                "GP visits/1000": f"{cal['dist_gp_visits_per_1000']['mean']:.0f} [{cal['dist_gp_visits_per_1000']['p05']:.0f}\u2013{cal['dist_gp_visits_per_1000']['p95']:.0f}]",
                                "ED/100k": f"{cal['dist_ed_per_100k']['mean']:.0f} [{cal['dist_ed_per_100k']['p05']:.0f}\u2013{cal['dist_ed_per_100k']['p95']:.0f}]",
                                "Admissions/100k": f"{cal['dist_admissions_per_100k']['mean']:.0f} [{cal['dist_admissions_per_100k']['p05']:.0f}\u2013{cal['dist_admissions_per_100k']['p95']:.0f}]",
                                "Spend/capita NZD": f"${cal['dist_spend_per_capita_nzd']['mean']:.0f} [${cal['dist_spend_per_capita_nzd']['p05']:.0f}\u2013${cal['dist_spend_per_capita_nzd']['p95']:.0f}]",
                            })
                        st.dataframe(pd.DataFrame(dist_rows), hide_index=True, width="stretch")
                        st.caption(CALIBRATION_DIST_NOTE)
                else:
                    st.info("Click to generate distribution-based calibration (1000 beta draws per scenario).")

        # ── Budget impact analysis ────────────────────────────────────
        with st.expander("Budget impact with Bass policy diffusion"):
            st.markdown(
                "**Illustrative budget estimates** using calibrated spend-per-capita "
                "combined with a Bass diffusion curve (p=0.15 innovation, q=0.40 imitation) "
                "to model gradual policy adoption over 5 years."
            )
            bi_scenarios = st.multiselect("Scenarios for budget impact", ["F0","F3","F4","F8"], default=["F0","F4"], key="bi_scenarios")
            bi_pop = st.number_input("Enrolled population", min_value=100000, max_value=10000000, value=4500000, step=100000, key="bi_pop")
            if st.button("Run budget impact", key="run_bi_btn"):
                with st.spinner("Computing budget impact with diffusion..."):
                    bi_df = run_budget_impact(tuple(bi_scenarios), enrolled_population=int(bi_pop))
                totals = bi_df[bi_df["year"] == "Total"][["scenario_id", "discounted_budget_nzd", "undiscounted_budget_nzd"]]
                st.dataframe(bi_df[~bi_df["year"].astype(str).str.isdigit()].reset_index(drop=True), hide_index=True, width="stretch")
                bi_fig = px.line(
                    bi_df[bi_df["year"] != "Total"].astype({"year": int}),
                    x="year", y="discounted_budget_nzd", color="scenario_id",
                    markers=True,
                    title="Discounted budget impact by scenario (with Bass diffusion)",
                    labels={"year": "Year", "discounted_budget_nzd": "Discounted budget (NZD)", "scenario_id": "Scenario"},
                )
                bi_fig.update_layout(height=400, margin=dict(l=10, r=10, t=45, b=10))
                st.plotly_chart(bi_fig, width="stretch")
                st.caption(BUDGET_IMPACT_NOTE)
            else:
                st.info("Click to run budget impact with Bass policy diffusion.")

        # ── References section ────────────────────────────────────────
        with st.expander("References and data sources"):
            st.markdown(
                "#### References (CSL-JSON)\n"
                "A canonical reference list is maintained at "
                "`docs/references/gtpcnz-references-v1.8.5.json` (23 entries). "
                "Key sources used in this analysis:\n\n"
            )
            refs_text = [
                "- **SRC01\u201303**: NZ Ministry of Health / Health NZ capitation and NPCD",
                "- **SRC05**: NZ Health Survey (unmet need, cost barriers)",
                "- **SRC14\u201317**: Statistics NZ (population, NZDep, rural/urban classification)",
                "- **SRC18**: Health and Disability System Review (Tier 1 funding recommendations)",
                "- **SRC19**: Sapere capitation reweighting review",
                "- **SRC20\u201321**: VOI and Bass diffusion methodology",
                "- **SRC22**: HQSC Atlas of Healthcare Variation",
                "- **SRC23**: NZ Treasury Budget Update 2025",
            ]
            for line in refs_text:
                st.markdown(line)
            st.markdown(
                "\n\n*All sources are publicly available. The reference list is "
                "maintained alongside the model in the `docs/references/` directory.*"
            )

        render_reference_scenario_explainer()
        if df.empty:
            st.error(f"Could not find model results at `{RESULTS_PATH.relative_to(ROOT)}`.")
        else:
            _render_result_manifest_badge("precomputed", "F0-F9")
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
        render_live_model_lab(df)

    with tabs[7]:
        st.subheader("🎓 Educational explainer")
        render_educational_explainer_context()
        render_educational_parameter_dictionary()
        st.markdown(
            """
            These sliders are deliberately simple. They teach the trade-offs, but
            they are not the 70-parameter benchmark and not a calibrated prediction.
            """
        )
        _render_result_manifest_badge("educational", "sidebar-slider")
        metric_cols = st.columns(3)
        metric_cols[0].metric("Viability index", educational_scores["educational_viability_score"])
        metric_cols[1].metric("Supply index", educational_scores["educational_supply_score"])
        metric_cols[2].metric("Hospital pressure index", educational_scores["educational_hospital_pressure_score"])
        render_educational_chart(educational_scores)
        _render_calculation_expander(
            show_formulas=False,
            result_validation="Educational explainer scores use simplified strategic-response formulas with sigmoid activation (steepness 6.0-6.5). These are not the 70-parameter benchmark.",
        )

    with tabs[8]:
        st.subheader("📋 Evidence and Official Information Act tracker")
        tracker = cached_oia_tracker(tuple(str(p) for p in OIA_TRACKER_CANDIDATES))
        if tracker.empty:
            st.info("Evidence/OIA tracker data is not available in this checkout.")
        else:
            st.dataframe(tracker, width="stretch", hide_index=True)
        st.caption("OIA responses and linked data are needed before treating the model as calibrated.")

    with tabs[9]:
        st.subheader("🎯 What would make this a real calibrated model?")
        render_next_steps_context()
        readiness = build_calibration_readiness_table()
        st.dataframe(readiness, width="stretch", hide_index=True)
        st.markdown(
            """
            The next stage is not more sliders. It is replacing public-data anchored priors
            with real data on appointments, payments, co-payments, workforce, ambulance
            pathways, emergency department presentations and hospital admissions.
            """
        )

    with tabs[10]:
        st.subheader("📖 Plain-English glossary")
        st.markdown(
            """
            - **Capitation:** baseline funding for enrolled population responsibility.
            - **Fee-for-service:** payment for a specific eligible service.
            - **Uncapped:** no fixed global ceiling on eligible activity.
            - **Controlled:** item rules, clinical governance, documentation, audit and accountability still apply.
            - **Place-based accountability:** responsibility for a whole local population, including hard-to-reach people.
            - **Benchmark:** a transparent model structure that still needs real calibration data.
            - **Reference scenario:** a model-generated scenario already stored in the project outputs.
            - **Educational explainer:** a simplified interactive teaching tool, not the model forecast.
        """
        )
        render_big_words_expander()

    st.caption(f"GTPCNZ v{APP_VERSION}. Demonstrative explainer only, not a calibrated forecast.")


if __name__ == "__main__":
    render_app()
