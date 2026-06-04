"""Policy cockpit contract surface for the public model."""

from __future__ import annotations

from models.primarycare_model.calibration.public_aggregate_calibration import run_public_aggregate_calibration
from models.primarycare_model.ui.charts import ChartContract
from models.primarycare_model.uncertainty.structural_ensemble import run_structural_ensemble
from models.primarycare_model.voi.full_voi import run_full_voi

REQUIRED_SECTIONS = (
    "cockpit", "scenario_frontier", "causal_graph", "policy_manifold", "calibration",
    "uncertainty", "voi", "equity", "sources", "release", "downloads",
)

REQUIRED_VISUALS = (
    "Executive scenario cards",
    "Scenario frontier plot",
    "Interactive causal pathway graph",
    "Policy manifold/topology plot",
    "Tornado chart with parameter IDs",
    "Waterfall chart with formula provenance",
    "VOI evidence-priority chart",
    "Structural ensemble uncertainty chart",
    "Calibration observed-versus-simulated diagnostics",
    "Posterior predictive check visuals",
    "Equity small multiples where public data permit",
    "Source freshness panel",
    "Release audit panel",
    "Downloadable scenario report card",
)


def _chart_for_visual(visual: str, rows: tuple[dict[str, object], ...], calibration_status: str) -> ChartContract:
    return ChartContract(
        title=visual,
        unit="index",
        source_snapshot_id="public-snapshot-v1",
        interpretation_note="Public aggregate benchmark surface; read directionally and keep claim boundaries visible.",
        data=rows,
        calibration_status=calibration_status,
    )


def build_policy_cockpit_payload() -> dict[str, object]:
    calibration = run_public_aggregate_calibration()
    structural = run_structural_ensemble()
    voi = run_full_voi()
    rows = tuple({"parameter_group": key, "evppi": value} for key, value in voi.evppi.items())
    calibration_status = str(calibration["calibration_status"])
    return {
        "sections": REQUIRED_SECTIONS,
        "calibration": calibration,
        "structural_uncertainty": structural,
        "voi": voi.model_dump(),
        "charts": [_chart_for_visual(visual, rows, calibration_status).as_payload() for visual in REQUIRED_VISUALS],
    }
