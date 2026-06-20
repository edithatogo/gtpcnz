from __future__ import annotations

import ast
from pathlib import Path

from plotly.graph_objects import Figure

from models.primarycare_model import dashboard_service as service


def test_dashboard_service_is_framework_neutral_and_exposes_public_links() -> None:
    source = Path("models/primarycare_model/dashboard_service.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module or ""
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
    }

    assert "streamlit" not in imported_modules
    links = service.public_links()
    assert links["github_pages"] == "https://edithatogo.github.io/gtpcnz/"
    assert links["huggingface_space"] == "https://edithatogo-gtpcnz-dashboard.hf.space/"
    assert links["streamlit_compatibility"] == "https://gtpcnz.streamlit.app/"


def test_dashboard_service_reference_and_chart_payloads_are_public_safe() -> None:
    reference = service.reference_results()
    summary = service.reference_summary()
    comparison = service.comparison_bundle(("F0", "F4"))
    frontier = service.supply_pressure_bundle(("F0", "F4"))

    assert not reference.empty
    assert not summary.empty
    assert comparison.table["scenario_id"].tolist() == ["F0", "F4"]
    assert isinstance(comparison.figure, Figure)
    assert isinstance(frontier.figure, Figure)
    assert "not linked-data calibrated" in comparison.warning
    assert "not a patient-level forecast" in frontier.warning


def test_dashboard_service_simulation_bundles_are_seeded_and_bounded() -> None:
    uncertainty = service.simulation_bundle("uncertainty", scenario_id="F4", draws=20, seed=123)
    uncertainty_again = service.simulation_bundle("uncertainty", scenario_id="F4", draws=20, seed=123)
    stock_flow = service.simulation_bundle("stock-flow", scenario_id="F4", months=12)
    agent = service.simulation_bundle("agent-lens", scenario_id="F4", population_size=60, months=6, seed=123)
    educational = service.simulation_bundle(
        "educational",
        scenario_id="F4",
        educational_settings=service.educational_defaults(),
    )

    assert uncertainty.table.equals(uncertainty_again.table)
    assert not stock_flow.table.empty
    assert not agent.table.empty
    assert not educational.table.empty
    assert "patient-level simulation evidence" in agent.interpretation
    assert "does not rerun the full parameterised model" in educational.interpretation


def test_dashboard_service_readiness_and_metrics_are_available() -> None:
    metrics = service.start_metrics()
    readiness = service.calibration_readiness()

    assert len(metrics) >= 4
    assert any(metric.label == "Claim boundary" for metric in metrics)
    assert not readiness.empty


def test_dashboard_state_round_trips_and_clamps_public_caps() -> None:
    state = service.parse_dashboard_state(
        "/live-model",
        "?scenarios=F0,F4,F8&kind=agent-lens&scenario=F8&draws=9999&seed=42&months=999&population=9999",
    )

    assert state.route == "/live-model"
    assert state.scenarios == ("F0", "F4", "F8")
    assert state.simulation_kind == "agent-lens"
    assert state.scenario_id == "F8"
    assert state.draws == service.MAX_MONTE_CARLO_DRAWS
    assert state.months == service.MAX_MONTHS
    assert state.population_size == service.MAX_ABM_POPULATION

    href = service.serialize_dashboard_state(state)
    reparsed = service.parse_dashboard_state("/live-model", href.split("?", 1)[1])
    assert reparsed == state


def test_custom_scenario_and_provenance_payloads_are_public_safe() -> None:
    bundle = service.custom_scenario_comparison_bundle(service.educational_defaults())
    provenance = service.chart_provenance_table(bundle)
    export_records = service.custom_scenario_export_records(service.educational_defaults())
    health = service.runtime_health_table()

    assert "CUSTOM" in bundle.table["scenario_id"].tolist()
    assert "not calibrated" in bundle.interpretation
    assert "Calculation mode" in provenance["Field"].tolist()
    assert all("claim_boundary" in record for record in export_records)
    assert "Runtime health" not in health.to_string()
    assert "Claim boundary" in health["Area"].tolist()


def test_model_surface_calibration_and_advanced_visuals_are_public_bounded() -> None:
    surface = service.model_surface_status_table()
    gap = service.model_gap_bundle()
    calibration = service.calibration_error_bundle()
    advanced = service.advanced_visual_bundles()

    assert {"surfaced", "deferred_public_boundary", "retired"}.issubset(set(surface["Status"]))
    assert "not validation evidence" in gap.interpretation
    assert "Readiness diagnostic only" in calibration.interpretation
    assert len(advanced) >= 5
    assert any(bundle.title == "Value of information" for bundle in advanced)
    assert all("not" in bundle.interpretation.lower() for bundle in advanced)
