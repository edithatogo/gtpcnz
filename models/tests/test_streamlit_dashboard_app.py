from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[2] / "streamlit_app.py"
APP_SOURCE_PATH = APP_PATH.parents[0] / "models" / "primarycare_model" / "app.py"
LEVER_REGISTRY_PATH = APP_PATH.parents[0] / "models" / "primarycare_model" / "registries" / "educational_levers.v1.yaml"
FULL_CAVEAT = (
    "This is a public-data anchored benchmark and educational explainer. "
    "It is not linked-data calibrated and not a patient-level forecast. "
    "It should not be used to claim precise fiscal savings, hospital-demand reductions, "
    "workforce effects, or implementation impacts."
)


def _run_app() -> AppTest:
    at = AppTest.from_file(str(APP_PATH), default_timeout=90).run()
    assert not at.exception
    return at


def _markdown_text(at: AppTest) -> str:
    elements = [*at.markdown, *at.warning, *at.caption]
    return "\n".join(str(item.value) for item in elements)


def _source_text() -> str:
    return (
        APP_SOURCE_PATH.read_text(encoding="utf-8")
        + "\n"
        + LEVER_REGISTRY_PATH.read_text(encoding="utf-8")
    )


def _compact(text: str) -> str:
    return " ".join(text.split())


def test_streamlit_dashboard_smoke_loads_without_exceptions():
    at = _run_app()

    markdown = _markdown_text(at)
    assert "public-data anchored benchmark" in markdown
    assert "not a patient-level forecast" in markdown
    assert "Reference scenarios" in markdown


def test_streamlit_dashboard_exposes_core_navigation():
    at = _run_app()

    tab_labels = [tab.label for tab in at.tabs]
    for required_tab in [
        "Start here",
        "Post guide",
        "Current state",
        "Reference scenarios",
        "Microeconomics",
        "Game theory",
        "Live model",
        "Methodology",
        "Explainer",
        "Evidence/OIA",
        "Calibration",
        "Glossary",
    ]:
        assert any(required_tab in label for label in tab_labels)


def test_streamlit_dashboard_exposes_layout_contract():
    at = _run_app()

    expander_labels = [expander.label for expander in at.expander]
    metric_labels = [metric.label for metric in at.metric]
    assert "How to read this dashboard" in expander_labels
    assert "Educational explainer controls" in expander_labels
    assert "Reference scenarios" in metric_labels
    assert "Claim boundary" in metric_labels
    assert "Calibration" in metric_labels


def test_streamlit_dashboard_covers_composite_model_visuals():
    source = _source_text()

    required_visual_sections = [
        "Recalculate reference scenarios",
        "Live versus precomputed delta",
        "Tornado sensitivity",
        "Waterfall: hybrid viability decomposition",
        "Ensemble Monte Carlo",
        "Cohort-stratified comparison",
        "Variance decomposition",
        "Scenario × subgroup heatmap",
        "Policy shock sequences",
        "Outcome clustering",
        "Composite meta-analysis",
        "Stress-test scenarios",
        "Equity × complexity interaction scan",
        "Regime sweep",
        "Agent subgroup replay",
        "Phase portrait",
        "Uncertainty ribbon",
        "Value of information",
        "Distribution-based calibration ranges",
        "Budget impact with Bass policy diffusion",
        "Animated parameter sweep",
        "Scenario morph animation",
        "Animated regime sweep",
    ]
    required_runtime_models = [
        "run_reference_calculation",
        "build_waterfall_data",
        "run_tornado_sensitivity",
        "run_ensemble_mc",
        "run_cohort_stratified",
        "run_variance_decomposition",
        "run_heatmap_matrix",
        "run_policy_shock_sequence",
        "run_stochastic_replay",
        "run_stock_flow_trace",
        "run_agent_lens",
        "run_outcome_clustering",
        "run_composite_meta_analysis",
        "run_stress_test_scenarios",
        "run_interaction_scan",
        "run_regime_sweep",
        "run_agent_subgroup_replay",
        "run_phase_portrait",
        "run_uncertainty_ribbon",
        "run_voi_analysis",
    ]

    for label in required_visual_sections:
        assert label in source
    for function_name in required_runtime_models:
        assert source.count(function_name) >= 2
    assert source.count("st.plotly_chart") >= 35
    assert source.count("animation_frame") >= 3
    assert "build_scenario_morph_frames" in source


def test_streamlit_dashboard_contract_first_screen_and_wording():
    at = _run_app()
    markdown = _markdown_text(at)
    source = _source_text()

    assert "GTPCNZ: funding architecture explainer" in str(at.title[0].value)
    assert _compact(FULL_CAVEAT) in _compact(markdown)
    for required_phrase in [
        "explainer",
        "public-data anchored benchmark",
        "reference scenario",
        "educational explainer",
        "model-generated index",
        "not linked-data calibrated",
        "not a patient-level forecast",
        "educational sliders do not rerun the full parameterised model",
        "0 means absent/weak; 100 means strong/reliably implemented",
        "qualitative teaching levers, not estimated structural parameters",
        "Do not convert index differences into dollars saved",
        "Uncapped does not mean uncontrolled",
    ]:
        assert required_phrase in markdown or required_phrase in source

    forbidden_claims = [
        "calibrated simulator",
        "government endorsement",
    ]
    for forbidden in forbidden_claims:
        allowed_negated = source.replace("not a patient-level forecast", "").replace("not observed New Zealand outcomes", "")
        assert forbidden not in allowed_negated


def test_streamlit_dashboard_contract_current_state_and_crosswalk():
    at = _run_app()
    markdown = _markdown_text(at)
    source = _source_text()

    for current_state_component in [
        "capitation reweighting",
        "primary care access target",
        "National Primary Care Dataset",
        "digital access and telehealth",
        "urgent and after-hours care",
        "PHO accountability and commissioning",
    ]:
        assert current_state_component.lower() in (markdown + "\n" + source).lower()

    for post_title in [
        "Are we buying hospital growth by rationing cheaper care upstream?",
        "Fee-for-service, capitation and blended funding",
        "Marginal supply",
        "Why formulas do not solve games",
        "Current reform pathway",
        "What I mean by uncapping primary care funding",
    ]:
        assert post_title in markdown or post_title in source

    for crosswalk_field in [
        "Quarto / report destination",
        "Streamlit module",
        "GitHub Pages card",
        "Static visual",
        "Dynamic visual",
        "Status / caveat",
    ]:
        assert crosswalk_field in source


def test_streamlit_dashboard_contract_visual_gallery_inventory():
    _run_app()
    source = _source_text()

    required_visual_inventory = [
        "Reference scenario viability",
        "Supply generation versus hospital pressure",
        "Scenario score matrix",
        "Selected scenario profile",
        "Educational explainer output",
        "Project readiness",
        "Marginal supply response",
        "Capitation budget constraint",
        "Scheduled activity payment",
        "Co-payment/access barrier mix",
        "Claims audit game",
        "Coordination game",
        "Gaming-risk frontier",
        "Public explainer architecture",
        "Current reform pathway",
        "Public project status",
        "Figure and table inventory",
        "Post reading map",
        "Educational parameter dictionary",
        "Calibration readiness",
        "OIA tracker",
        "Model gap map",
    ]
    for item in required_visual_inventory:
        assert item in source

    for renderer in [
        "render_current_state_diagram",
        "render_reference_viability",
        "render_reference_scatter",
        "render_reference_heatmap",
        "render_scenario_profile_radar",
        "render_educational_chart",
        "render_readiness_chart",
        "render_microeconomics_lab",
        "render_game_theory_lab",
    ]:
        assert renderer in source


def test_streamlit_dashboard_contract_educational_controls_and_safety_labels():
    at = _run_app()
    markdown = _markdown_text(at)
    source = _source_text()

    for public_label in [
        "Payment for extra primary care activity",
        "Stable population-based base funding",
        "Whole-population local accountability",
        "Claim rules and audit strength",
        "Equity and co-payment protection",
        "Flexible workforce scope",
        "Local in-person care capacity",
    ]:
        assert public_label in source

    for safety_label in [
        "Educational explainer",
        "Model-generated index",
        "Evidence readiness",
        "Calibration readiness",
    ]:
        assert safety_label in markdown or safety_label in source
