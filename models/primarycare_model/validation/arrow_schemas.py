"""PyArrow schemas aligned with Pandera schemas and Pydantic contracts.

PyArrow is intentionally optional. When available, these schemas provide
strict columnar typing for Arrow-backed DataFrames. When unavailable, a
compatibility helper provides fallback dtype maps for pandas-only paths.

All column names and types are aligned with:
- pandera_schemas.ReferenceResultSchema
- contracts.parameters.ParameterDefinition
- contracts.scenarios.RuntimeScenarioDefinition
- contracts.engine.UncertaintySummary
- Runtime calculation frames produced by runtime_lab
"""

from __future__ import annotations

from typing import Any

try:
    import pyarrow as pa
except ImportError:
    pa = None  # type: ignore[assignment]

PyArrowSchema = Any


# -- Registry frames --------------------------------------------------------

def parameter_registry_schema() -> PyArrowSchema | None:
    """PyArrow schema for a parameter-definition registry table."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("parameter_id", pa.string(), nullable=False),
        pa.field("label", pa.string(), nullable=False),
        pa.field("value_type", pa.string(), nullable=False),
        pa.field("unit", pa.string(), nullable=False),
        pa.field("default_value", pa.string(), nullable=False),
        pa.field("lower_bound", pa.float64(), nullable=True),
        pa.field("upper_bound", pa.float64(), nullable=True),
        pa.field("category_values", pa.list_(pa.string()), nullable=True),
        pa.field("description", pa.string(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
        pa.field("sensitivity_class", pa.string(), nullable=False),
        pa.field("evidence_tier", pa.string(), nullable=False),
        pa.field("tags", pa.list_(pa.string()), nullable=True),
    ])

def educational_lever_registry_schema() -> PyArrowSchema | None:
    """PyArrow schema for an educational-lever registry table."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("field_name", pa.string(), nullable=False),
        pa.field("public_label", pa.string(), nullable=False),
        pa.field("health_economics_meaning", pa.string(), nullable=False),
        pa.field("high_value_meaning", pa.string(), nullable=False),
        pa.field("educational_output_effect", pa.string(), nullable=False),
        pa.field("slider_help", pa.string(), nullable=False),
        pa.field("default_value", pa.int64(), nullable=False),
        pa.field("lower_bound", pa.int64(), nullable=False),
        pa.field("upper_bound", pa.int64(), nullable=False),
        pa.field("step", pa.int64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
        pa.field("claim_boundary", pa.string(), nullable=False),
    ])

def scenario_registry_schema() -> PyArrowSchema | None:
    """PyArrow schema for a runtime-scenario registry table."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("scenario_id", pa.string(), nullable=False),
        pa.field("scenario_name", pa.string(), nullable=False),
        pa.field("description", pa.string(), nullable=False),
        pa.field("scenario_kind", pa.string(), nullable=False),
        pa.field("activity_signal", pa.float64(), nullable=False),
        pa.field("capitation", pa.float64(), nullable=False),
        pa.field("place_accountability", pa.float64(), nullable=False),
        pa.field("scope_capacity", pa.float64(), nullable=False),
        pa.field("urgent_ambulance", pa.float64(), nullable=False),
        pa.field("data_visibility", pa.float64(), nullable=False),
        pa.field("governance", pa.float64(), nullable=False),
        pa.field("equity_protection", pa.float64(), nullable=False),
        pa.field("copayment_burden", pa.float64(), nullable=False),
        pa.field("budget_tightness", pa.float64(), nullable=False),
        pa.field("hospital_salience", pa.float64(), nullable=False),
        pa.field("complexity", pa.float64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
        pa.field("claim_boundary", pa.string(), nullable=False),
    ])

def input_dataset_registry_schema() -> PyArrowSchema | None:
    """PyArrow schema for an input-dataset registry table."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("dataset_id", pa.string(), nullable=False),
        pa.field("label", pa.string(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
        pa.field("sensitivity_class", pa.string(), nullable=False),
        pa.field("fields", pa.list_(pa.struct([
                    pa.field("field_name", pa.string(), nullable=False),
                    pa.field("data_type", pa.string(), nullable=False),
                    pa.field("unit", pa.string(), nullable=False),
                    pa.field("required", pa.bool_(), nullable=False),
                    pa.field("description", pa.string(), nullable=False),
                ])), nullable=True),
        pa.field("claim_boundary", pa.string(), nullable=False),
    ])

def input_table_schema() -> PyArrowSchema | None:
    """PyArrow schema for a generic input-data table."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("dataset_id", pa.string(), nullable=False),
        pa.field("row_index", pa.int64(), nullable=False),
    ])# -- Calculation output frames ----------------------------------------------

def reference_result_schema() -> PyArrowSchema | None:
    """PyArrow schema for the public reference-scenario result frame."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("scenario_id", pa.string(), nullable=False),
        pa.field("scenario_name", pa.string(), nullable=False),
        pa.field("description", pa.string(), nullable=False),
        pa.field("hybrid_viability_score", pa.float64(), nullable=False),
        pa.field("access_score", pa.float64(), nullable=False),
        pa.field("supply_generation_score", pa.float64(), nullable=False),
        pa.field("equity_legitimacy_score", pa.float64(), nullable=False),
        pa.field("governance_resilience_score", pa.float64(), nullable=False),
        pa.field("hospital_deflection_score", pa.float64(), nullable=False),
        pa.field("fiscal_risk_score", pa.float64(), nullable=False),
        pa.field("gaming_risk_score", pa.float64(), nullable=False),
        pa.field("hospital_pressure_score", pa.float64(), nullable=False),
        pa.field("mean_last12_public_cost_index", pa.float64(), nullable=False),
        pa.field("rank_by_hybrid_viability", pa.int64(), nullable=False),
        pa.field("mean_last12_primary_contacts_per_1000", pa.float64(), nullable=True),
        pa.field("mean_last12_unmet_need_index", pa.float64(), nullable=True),
        pa.field("mean_last12_ed_events_per_100k", pa.float64(), nullable=True),
        pa.field("mean_last12_admissions_per_100k", pa.float64(), nullable=True),
        pa.field("mean_last12_ambulance_conveyances_per_100k", pa.float64(), nullable=True),
        pa.field("mean_last12_hospital_pressure_index", pa.float64(), nullable=True),
        pa.field("calculation_status", pa.string(), nullable=True),
        pa.field("scenario_role", pa.string(), nullable=True),
        pa.field("claim_boundary", pa.string(), nullable=True),
    ])

def monthly_metrics_schema() -> PyArrowSchema | None:
    """PyArrow schema for the stock-flow monthly metrics frame."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("month", pa.int64(), nullable=False),
        pa.field("scenario_id", pa.string(), nullable=False),
        pa.field("need_generated", pa.float64(), nullable=False),
        pa.field("primary_contacts", pa.float64(), nullable=False),
        pa.field("ambulance_resolved", pa.float64(), nullable=False),
        pa.field("unmet_need", pa.float64(), nullable=False),
        pa.field("primary_capacity", pa.float64(), nullable=False),
        pa.field("hospital_pressure", pa.float64(), nullable=False),
        pa.field("fiscal_pressure", pa.float64(), nullable=False),
        pa.field("calculation_status", pa.string(), nullable=True),
    ])

def simulation_trace_schema() -> PyArrowSchema | None:
    """PyArrow schema for a per-scenario calculation trace."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("calculation", pa.string(), nullable=False),
        pa.field("formula_sketch", pa.string(), nullable=False),
        pa.field("index_value", pa.float64(), nullable=False),
    ])

def stochastic_draw_schema() -> PyArrowSchema | None:
    """PyArrow schema for the full Monte Carlo draw frame."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("draw", pa.int64(), nullable=False),
        pa.field("scenario_id", pa.string(), nullable=False),
        pa.field("scenario_name", pa.string(), nullable=False),
        pa.field("hybrid_viability_score", pa.float64(), nullable=False),
        pa.field("access_score", pa.float64(), nullable=False),
        pa.field("supply_generation_score", pa.float64(), nullable=False),
        pa.field("equity_legitimacy_score", pa.float64(), nullable=False),
        pa.field("governance_resilience_score", pa.float64(), nullable=False),
        pa.field("hospital_deflection_score", pa.float64(), nullable=False),
        pa.field("fiscal_risk_score", pa.float64(), nullable=False),
        pa.field("gaming_risk_score", pa.float64(), nullable=False),
        pa.field("hospital_pressure_score", pa.float64(), nullable=False),
        pa.field("calculation_status", pa.string(), nullable=True),
    ])


# -- Uncertainty / summary frames -------------------------------------------

def uncertainty_summary_schema() -> PyArrowSchema | None:
    """PyArrow schema for the per-metric uncertainty summary."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("metric", pa.string(), nullable=False),
        pa.field("mean", pa.float64(), nullable=False),
        pa.field("std", pa.float64(), nullable=False),
        pa.field("p05", pa.float64(), nullable=False),
        pa.field("p50", pa.float64(), nullable=False),
        pa.field("p95", pa.float64(), nullable=False),
        pa.field("draws", pa.int64(), nullable=False),
    ])

def agent_frame_schema() -> PyArrowSchema | None:
    """PyArrow schema for the agent-lens patient-level frame."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("patient_id", pa.int64(), nullable=False),
        pa.field("high_need_score", pa.float64(), nullable=False),
        pa.field("rural", pa.bool_(), nullable=False),
        pa.field("access_barrier", pa.float64(), nullable=False),
        pa.field("access_probability", pa.float64(), nullable=False),
        pa.field("served_contacts", pa.int64(), nullable=False),
        pa.field("unmet_attempts", pa.int64(), nullable=False),
    ])

def agent_summary_schema() -> PyArrowSchema | None:
    """PyArrow schema for the agent-lens summary frame."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("metric", pa.string(), nullable=False),
        pa.field("value", pa.float64(), nullable=False),
    ])


# -- Public export ----------------------------------------------------------

def public_export_schema() -> PyArrowSchema | None:
    """PyArrow schema for the public-facing export table."""
    if pa is None:
        return None
    return pa.schema([
        pa.field("scenario_id", pa.string(), nullable=False),
        pa.field("scenario_name", pa.string(), nullable=False),
        pa.field("description", pa.string(), nullable=False),
        pa.field("scenario_role", pa.string(), nullable=True),
        pa.field("hybrid_viability_score", pa.float64(), nullable=False),
        pa.field("access_score", pa.float64(), nullable=False),
        pa.field("supply_generation_score", pa.float64(), nullable=False),
        pa.field("equity_legitimacy_score", pa.float64(), nullable=False),
        pa.field("governance_resilience_score", pa.float64(), nullable=False),
        pa.field("hospital_deflection_score", pa.float64(), nullable=False),
        pa.field("fiscal_risk_score", pa.float64(), nullable=False),
        pa.field("gaming_risk_score", pa.float64(), nullable=False),
        pa.field("hospital_pressure_score", pa.float64(), nullable=False),
        pa.field("mean_last12_public_cost_index", pa.float64(), nullable=False),
        pa.field("rank_by_hybrid_viability", pa.int64(), nullable=False),
        pa.field("claim_boundary", pa.string(), nullable=True),
        pa.field("calculation_status", pa.string(), nullable=True),
    ])


# -- Compatibility helper ---------------------------------------------------

def as_pandas_dtypes(schema: PyArrowSchema | None) -> dict[str, str]:
    """Convert a PyArrow schema to a pandas dtype dictionary."""
    if pa is None or schema is None:
        return {}
    try:
        result = {}
        for field in schema:
            type_str = str(field.type)
            if type_str.startswith("list<") or type_str.startswith("struct<") or type_str == "string":
                result[field.name] = "object"
            elif type_str in ("int64", "int32", "int16", "int8"):
                result[field.name] = "int64"
            elif type_str in ("float64", "float32"):
                result[field.name] = "float64"
            elif type_str == "bool":
                result[field.name] = "bool"
            else:
                result[field.name] = "object"
        return result
    except Exception:
        return {}


# -- Schema lookup ----------------------------------------------------------

_SCHEMA_REGISTRY: dict[str, PyArrowSchema | None] = {
    "parameter_registry": parameter_registry_schema(),
    "educational_lever_registry": educational_lever_registry_schema(),
    "scenario_registry": scenario_registry_schema(),
    "input_dataset_registry": input_dataset_registry_schema(),
    "input_table": input_table_schema(),
    "reference_result": reference_result_schema(),
    "monthly_metrics": monthly_metrics_schema(),
    "simulation_trace": simulation_trace_schema(),
    "stochastic_draw": stochastic_draw_schema(),
    "uncertainty_summary": uncertainty_summary_schema(),
    "agent_frame": agent_frame_schema(),
    "agent_summary": agent_summary_schema(),
    "public_export": public_export_schema(),
}

def get_schema(name: str) -> PyArrowSchema | None:
    """Retrieve a named PyArrow schema, or None if unavailable."""
    return _SCHEMA_REGISTRY.get(name)

def registered_schema_names() -> list[str]:
    """Return sorted list of available schema names."""
    return sorted(_SCHEMA_REGISTRY)
