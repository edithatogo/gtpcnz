from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = ROOT / "streamlit_app.py"
SUBSTACK_PREVIEW_DIR = ROOT / "docs" / "substack-ready" / "figures" / "preview-v1.7.2"


def _assert_nonempty_frame(value: Any, label: str) -> None:
    assert isinstance(value, pd.DataFrame), label
    assert not value.empty, label


def test_streamlit_entrypoint_renders_all_public_tabs_with_app_test() -> None:
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ENTRYPOINT), default_timeout=120).run()

    assert not at.exception
    assert [tab.label for tab in at.tabs] == [
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
        "Public cockpit",
        "Glossary",
    ]
    page_text = "\n".join(
        str(element.value)
        for collection in (at.title, at.header, at.subheader, at.markdown, at.warning, at.caption)
        for element in collection
    )
    for required in [
        "public-data anchored benchmark",
        "not linked-data calibrated",
        "not a patient-level forecast",
        "Reference scenarios",
        "Educational explainer",
        "Value of information",
        "Distribution-based calibration",
        "Budget impact",
        "Public model cockpit",
        "Release audit panel",
    ]:
        assert required in page_text


def test_streamlit_runtime_function_inventory_executes_with_bounded_inputs() -> None:
    from models.primarycare_model import runtime_lab

    scenario = runtime_lab.get_runtime_scenario("F4")
    indices = runtime_lab.calculate_indices(scenario)

    assert runtime_lab.clamp(150) == 100
    assert 0 < runtime_lab.diminishing_return(0.5) < 1
    assert 0 < runtime_lab.strategic_response(0.5) < 1
    assert set(indices) >= {
        "hybrid_viability_score",
        "access_score",
        "supply_generation_score",
        "hospital_pressure_score",
        "gaming_risk_score",
    }

    frame_calls = {
        "reference": runtime_lab.run_reference_calculation(months=12),
        "trace": runtime_lab.calculation_trace("F4"),
        "stock_flow": runtime_lab.run_stock_flow_trace("F4", months=6),
        "tornado": runtime_lab.run_tornado_sensitivity("F4", delta_step=5),
        "waterfall": runtime_lab.build_waterfall_data("F4"),
        "ensemble": runtime_lab.run_ensemble_mc(draws=10, seed=260526),
        "cohort": runtime_lab.run_cohort_stratified("F4"),
        "variance": runtime_lab.run_variance_decomposition("F4", draws=50, seed=260526),
        "shock": runtime_lab.run_policy_shock_sequence("F4", pre_shock_months=3, post_shock_months=3),
        "stress": runtime_lab.run_stress_test_scenarios("F4"),
        "interaction": runtime_lab.run_interaction_scan("F4"),
        "regime": runtime_lab.run_regime_sweep("F4", steps=2),
        "phase": runtime_lab.run_phase_portrait("F4", grid=2),
        "ribbon": runtime_lab.run_uncertainty_ribbon("F4", months=6, draws=10, seed=260526),
        "heatmap": runtime_lab.run_heatmap_matrix("F4"),
        "all_calibration": runtime_lab.calibrate_all_scenarios(),
        "score_guide": runtime_lab.build_score_guide_dataframe(),
        "voi": runtime_lab.run_voi_analysis(draws=50, seed=260526),
        "budget": runtime_lab.run_budget_impact(time_horizon_years=2),
        "evidence": runtime_lab.build_evidence_table(),
        "clusters": runtime_lab.run_outcome_clustering(n_clusters=2, scenario_ids=("F0", "F4"), seed=260526),
        "meta": runtime_lab.run_composite_meta_analysis(n_points=5, seed=260526),
        "animation": runtime_lab.create_animation_frames(steps=2, scenario_id="F4"),
        "gap_map": runtime_lab.model_gap_map(),
    }
    for label, frame in frame_calls.items():
        _assert_nonempty_frame(frame, label)

    stochastic_draws, stochastic_summary = runtime_lab.run_stochastic_uncertainty("F4", draws=10, seed=260526)
    replay = runtime_lab.run_stochastic_replay("F4", draws=10, fixed_seed=260526, random_seed=260527)
    agents, agent_summary = runtime_lab.run_agent_lens("F4", population_size=50, months=3, seed=260526)
    base_summary, low_summary, high_summary = runtime_lab.run_agent_subgroup_replay(
        "F4", population_size=50, months=3, seed=260526
    )

    for label, frame in {
        "stochastic_draws": stochastic_draws,
        "stochastic_summary": stochastic_summary,
        "replay_fixed": replay["fixed"],
        "replay_random": replay["random"],
        "replay_summary": replay["summary"],
        "agents": agents,
        "agent_summary": agent_summary,
        "agent_subgroup_base": base_summary,
        "agent_subgroup_low": low_summary,
        "agent_subgroup_high": high_summary,
    }.items():
        _assert_nonempty_frame(frame, label)

    assert runtime_lab.validate_slider_value(50, "test", 0, 100)[0]
    assert runtime_lab.format_formula_markdown(runtime_lab.get_calculation_details("F4"))
    assert runtime_lab.calibrate_to_public_benchmarks(indices)["calibrated_gp_visits_per_1000"] > 0
    assert runtime_lab.calibrate_distribution(indices, n_draws=25, seed=260526)["dist_method"]


def test_streamlit_app_builders_and_publication_artifacts_are_connected() -> None:
    from models.primarycare_model import app as streamlit_app
    from models.primarycare_model import runtime_lab

    app_frames = {
        "scenario_morph": streamlit_app.build_scenario_morph_frames("F0", "F4", steps=3),
        "post_map": streamlit_app.build_post_reading_map_table(),
        "current_reform": streamlit_app.build_current_reform_table(),
        "public_status": streamlit_app.build_public_status_table(),
        "figure_inventory": streamlit_app.build_figure_inventory_table(),
        "parameter_dictionary": streamlit_app.build_educational_parameter_dictionary(),
    }
    for label, frame in app_frames.items():
        _assert_nonempty_frame(frame, label)

    for post_id, post in runtime_lab.SUBSTACK_POSTS.items():
        path = ROOT / str(post["file"])
        assert path.exists(), f"Substack post {post_id} is missing: {path}"
        assert path.stat().st_size > 1000, f"Substack post {post_id} is unexpectedly small"

    manifest_path = SUBSTACK_PREVIEW_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    assert manifest
    for post_number in range(1, 19):
        stem = f"pcf-v172-{post_number:02d}-preview"
        png = SUBSTACK_PREVIEW_DIR / f"{stem}.png"
        assert png.exists(), f"Missing Substack preview PNG for post {post_number:02d}"
        assert png.stat().st_size > 1000


def test_policy_cockpit_payload_covers_every_section_chart_and_download_contract() -> None:
    from models.primarycare_model.ui.accessibility import validate_chart_payload
    from models.primarycare_model.ui.cockpit import REQUIRED_SECTIONS, build_policy_cockpit_payload
    from models.primarycare_model.ui.downloads import scenario_report_card

    payload = build_policy_cockpit_payload()

    assert tuple(payload["sections"]) == REQUIRED_SECTIONS
    assert payload["calibration"]["calibration_status"] == "public_aggregate_validated"
    assert payload["calibration"]["claim_level"] == "empirically_supported_if_gated"
    assert payload["structural_uncertainty"]["structural_uncertainty_interval"]
    assert payload["voi"]["label"] in {
        "decision-uncertainty analysis; not a forecast",
        "decision-uncertainty analysis, not a forecast",
    }

    charts = payload["charts"]
    assert charts
    for chart in charts:
        assert validate_chart_payload(chart) == []
        assert chart["calibration_status"] == "public_aggregate_validated"
        assert chart["claim_level"] == "empirically_supported_if_gated"
        assert chart["downloadable_data"] == chart["table_fallback"]
        assert chart["not_valid_for_warning"]

    report_card = scenario_report_card(payload)
    report_payload = json.loads(report_card)
    assert report_payload["sections"] == list(REQUIRED_SECTIONS)
    assert report_payload["calibration"]["calibration_status"] == "public_aggregate_validated"
    assert "precise fiscal savings" in report_payload["calibration"]["not_valid_for"]
