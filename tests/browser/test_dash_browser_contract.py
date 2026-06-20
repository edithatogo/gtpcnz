from __future__ import annotations

from dash.development.base_component import Component


def _walk(component: object):
    yield component
    if isinstance(component, Component):
        children = getattr(component, "children", None)
        if isinstance(children, (list, tuple)):
            for child in children:
                yield from _walk(child)
        elif children is not None:
            yield from _walk(children)


def _text(component: object) -> str:
    return "\n".join(node for node in _walk(component) if isinstance(node, str))


def test_dash_browser_contract_routes_include_caveats_and_downloads() -> None:
    from dash_app import app as dash_app

    route_text = {
        route: _text(dash_app.render_page(route))
        for route in (
            "/",
            "/reference-scenarios",
            "/live-model",
            "/guided",
            "/scenario-builder",
            "/model-surface",
            "/calibration-diagnostics",
            "/advanced-visuals",
            "/runtime-health",
            "/public-cockpit",
        )
    }

    assert "GTPCNZ interactive model lab" in route_text["/"]
    assert "Download CSV" in route_text["/reference-scenarios"]
    assert "Table fallback" in route_text["/live-model"]
    assert "Run provenance" in route_text["/live-model"]
    assert "not calibrated and not a policy forecast" in route_text["/scenario-builder"]
    assert "Surface coverage status" in route_text["/model-surface"]
    assert "Posterior predictive checks" in route_text["/calibration-diagnostics"]
    assert "Value of information" in route_text["/advanced-visuals"]
    assert "not model-validation evidence" in route_text["/runtime-health"]
    assert "Public cockpit" in route_text["/public-cockpit"]


def test_dash_browser_contract_layout_contains_all_public_nav_labels() -> None:
    from dash_app import app as dash_app
    from models.primarycare_model.dashboard_service import DASH_EXTRA_PUBLIC_ROUTES, STREAMLIT_PUBLIC_TABS

    text = _text(dash_app.app.layout())

    for label, _href in (*STREAMLIT_PUBLIC_TABS, *DASH_EXTRA_PUBLIC_ROUTES):
        assert label in text
