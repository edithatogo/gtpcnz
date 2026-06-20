from __future__ import annotations

from collections.abc import Iterable

from dash.development.base_component import Component


def _walk(component: object) -> Iterable[object]:
    yield component
    if isinstance(component, Component):
        children = getattr(component, "children", None)
        if isinstance(children, (list, tuple)):
            for child in children:
                yield from _walk(child)
        elif children is not None:
            yield from _walk(children)


def _text(component: object) -> str:
    values: list[str] = []
    for node in _walk(component):
        if isinstance(node, str):
            values.append(node)
    return "\n".join(values)


def test_dash_app_imports_and_exposes_required_routes() -> None:
    from dash_app import app as dash_app
    from models.primarycare_model.dashboard_service import STREAMLIT_PUBLIC_TABS

    layout = dash_app.app.layout()
    text = _text(layout)

    assert dash_app.app.title == "GTPCNZ interactive model lab"
    assert dash_app.server is not None
    assert "GTPCNZ" in text
    assert "This is a public-data anchored benchmark and educational explainer" in text
    for label, href in STREAMLIT_PUBLIC_TABS:
        assert label in text
        assert f'href="{href}"' not in text  # Dash components keep href as props, not rendered HTML here.
        assert dash_app.render_page(href) is not None


def test_dash_routes_cover_streamlit_public_tabs_and_legacy_aliases() -> None:
    from dash_app import app as dash_app
    from models.primarycare_model.dashboard_service import DASH_ROUTE_ALIASES, STREAMLIT_PUBLIC_TABS

    expected_labels = {label for label, _href in STREAMLIT_PUBLIC_TABS}
    assert expected_labels == {
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
    }

    route_text = {href: _text(dash_app.render_page(href)) for _label, href in STREAMLIT_PUBLIC_TABS}
    assert "Post guide" in route_text["/post-guide"]
    assert "Current state" in route_text["/current-state"]
    assert "Microeconomics" in route_text["/microeconomics"]
    assert "Game theory" in route_text["/game-theory"]
    assert "Live model" in route_text["/live-model"]
    assert "Evidence/OIA" in route_text["/evidence-oia"]
    assert "Public cockpit" in route_text["/public-cockpit"]
    assert "Glossary" in route_text["/glossary"]

    for alias, canonical in DASH_ROUTE_ALIASES.items():
        assert _text(dash_app.render_page(alias)) == _text(dash_app.render_page(canonical))


def test_dash_extra_public_routes_for_guided_builder_and_health() -> None:
    from dash_app import app as dash_app

    guided_text = _text(dash_app.render_page("/guided"))
    builder_text = _text(dash_app.render_page("/scenario-builder", "?scheduled_benefit_level=90"))
    surface_text = _text(dash_app.render_page("/model-surface"))
    diagnostics_text = _text(dash_app.render_page("/calibration-diagnostics"))
    advanced_text = _text(dash_app.render_page("/advanced-visuals"))
    health_text = _text(dash_app.render_page("/runtime-health"))
    live_text = _text(dash_app.render_page("/live-model", "?kind=stock-flow&scenario=F8&months=60&seed=123"))

    assert "Guided mode" in guided_text
    assert "Scenario builder" in builder_text
    assert "Custom scenario comparison" in builder_text
    assert "Runtime health" in health_text
    assert "not model-validation evidence" in health_text
    assert "Share this live model state" in live_text
    assert "Model surface" in surface_text
    assert "Surface coverage status" in surface_text
    assert "Calibration diagnostics" in diagnostics_text
    assert "Posterior predictive checks" in diagnostics_text
    assert "Advanced visuals" in advanced_text
    assert "Value of information" in advanced_text
    assert "Run provenance" in live_text


def test_dash_pages_render_public_caveat_and_deployment_posture() -> None:
    from dash_app import app as dash_app

    start_text = _text(dash_app.start_page())
    compare_text = _text(dash_app.compare_page())
    simulation_text = _text(dash_app.simulation_page())
    evidence_text = _text(dash_app.evidence_page())

    assert "GTPCNZ interactive model lab" in start_text
    assert "Hugging Face Space" in start_text
    assert "Compare model-generated indices" in compare_text
    assert "Table fallback" in compare_text
    assert "Live calculations stay capped" in simulation_text
    assert "Tornado sensitivity" in simulation_text
    assert "Run simulation" in simulation_text
    assert "Download CSV" in simulation_text
    assert "Table fallback" in simulation_text
    assert "Canonical definitions" in evidence_text
    assert "not linked-data calibrated" in evidence_text
    assert "GitHub Pages remains the public narrative front door" in evidence_text
    assert "Streamlit remains a compatibility surface" in evidence_text


def test_dash_app_callback_surface_and_service_update_functions() -> None:
    from dash_app import app as dash_app

    assert len(dash_app.app.callback_map) >= 5
    comparison = dash_app.update_comparison(["F0", "F4"], [])
    simulation = dash_app.update_simulation(
        0,
        "uncertainty",
        "F4",
        20,
        123,
        12,
        60,
        *[50 for _ in dash_app.EDUCATIONAL_FIELDS],
    )

    assert comparison[0].layout.title.text == "Reference scenario index comparison"
    assert comparison[1].layout.title.text == "Supply generation versus hospital pressure"
    assert "Do not convert" in comparison[2]
    assert simulation[0].layout.title.text == "Seeded uncertainty demo for F4"
    assert simulation[3]["rows"] > 0
