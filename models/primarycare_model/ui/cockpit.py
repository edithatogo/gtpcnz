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


def build_policy_cockpit_payload() -> dict[str, object]:
    calibration = run_public_aggregate_calibration()
    structural = run_structural_ensemble()
    voi = run_full_voi()
    chart = ChartContract(
        title="VOI evidence priority",
        unit="expected decision value index",
        source_snapshot_id="public-snapshot-v1",
        interpretation_note="Decision-uncertainty analysis only; not a forecast.",
        data=tuple({"parameter_group": key, "evppi": value} for key, value in voi.evppi.items()),
        calibration_status=str(calibration["calibration_status"]),
    )
    return {
        "sections": REQUIRED_SECTIONS,
        "calibration": calibration,
        "structural_uncertainty": structural,
        "voi": voi.model_dump(),
        "charts": [chart.as_payload()],
    }
