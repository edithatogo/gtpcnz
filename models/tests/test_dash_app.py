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

    layout = dash_app.app.layout()
    text = _text(layout)

    assert dash_app.app.title == "GTPCNZ interactive model lab"
    assert dash_app.server is not None
    assert "GTPCNZ" in text
    assert "This is a public-data anchored benchmark and educational explainer" in text
    assert "Start" in text
    assert "Compare scenarios" in text
    assert "Simulation lab" in text
    assert "Evidence and methods" in text


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
    assert "Run simulation" in simulation_text
    assert "Download CSV" in simulation_text
    assert "Table fallback" in simulation_text
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
