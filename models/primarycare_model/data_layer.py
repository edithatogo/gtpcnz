"""
Data layer module for the Primary Care Funding Architecture simulation.

Provides Arrow schema definitions, zero-copy conversion functions
between pydantic models, Arrow Tables, and Polars DataFrames, as well
as IPC serialisation helpers and example Polars aggregation queries.
"""

from __future__ import annotations

import io
from datetime import datetime
from typing import Any, Dict, List, Optional

import pyarrow as pa
import pyarrow.ipc as ipc

try:
    import polars as pl
except ModuleNotFoundError:  # pragma: no cover - exercised in lean runtimes
    pl = None

from .schemas import (
    EnrollmentStatus,
    Ethnicity,
    FundingModel,
    Gender,
    MonthlyMetrics,
    PatientProfile,
    PolicyParams,
    ProviderProfile,
    ProviderType,
    ScenarioParams,
    SimulationConfig,
    SimulationResult,
)

# ---------------------------------------------------------------------------
# Arrow schema definitions mirroring the pydantic models
# ---------------------------------------------------------------------------

PATIENT_ARROW_SCHEMA = pa.schema([
    pa.field("age", pa.int32(), nullable=False),
    pa.field("gender", pa.utf8(), nullable=False),
    pa.field("ethnicity", pa.utf8(), nullable=False),
    pa.field("deprivation_index", pa.int32(), nullable=False),
    pa.field("comorbidities", pa.list_(pa.utf8()), nullable=True),
    pa.field("enrollment_status", pa.utf8(), nullable=False),
])

PROVIDER_ARROW_SCHEMA = pa.schema([
    pa.field("id", pa.utf8(), nullable=False),
    pa.field("type", pa.utf8(), nullable=False),
    pa.field("region", pa.utf8(), nullable=False),
    pa.field("patient_list", pa.list_(pa.utf8()), nullable=True),
    pa.field("capacity", pa.int32(), nullable=False),
    pa.field("capitation_panel_size", pa.int32(), nullable=False),
])

CONFIG_ARROW_SCHEMA = pa.schema([
    pa.field("seed", pa.int32(), nullable=False),
    pa.field("num_patients", pa.int32(), nullable=False),
    pa.field("num_providers", pa.int32(), nullable=False),
    pa.field("time_horizon_months", pa.int32(), nullable=False),
    pa.field("tick_interval_days", pa.int32(), nullable=False),
])

SCENARIO_ARROW_SCHEMA = pa.schema([
    pa.field("name", pa.utf8(), nullable=False),
    pa.field("description", pa.utf8(), nullable=True),
    pa.field("funding_model", pa.utf8(), nullable=False),
    pa.field("capitation_rate", pa.float64(), nullable=True),
    pa.field("ffs_fee_schedule", pa.map_(pa.utf8(), pa.float64()), nullable=True),
])

POLICY_ARROW_SCHEMA = pa.schema([
    pa.field("name", pa.utf8(), nullable=False),
    pa.field("description", pa.utf8(), nullable=True),
    pa.field("target_population", pa.utf8(), nullable=True),
    pa.field("start_month", pa.int32(), nullable=False),
    pa.field("end_month", pa.int32(), nullable=True),
])

MONTHLY_METRICS_ARROW_SCHEMA = pa.schema([
    pa.field("month", pa.int32(), nullable=False),
    pa.field("total_patients", pa.int32(), nullable=False),
    pa.field("total_providers", pa.int32(), nullable=False),
    pa.field("total_visits", pa.int32(), nullable=False),
    pa.field("total_capitation_payments", pa.float64(), nullable=False),
    pa.field("total_ffs_payments", pa.float64(), nullable=False),
    pa.field("total_funding", pa.float64(), nullable=False),
    pa.field("avg_wait_time_days", pa.float64(), nullable=True),
    pa.field("unmet_demand", pa.int32(), nullable=False),
])

# ---------------------------------------------------------------------------
# SHAP attribution schema — feature-level SHAP values per simulation tick
# ---------------------------------------------------------------------------

SHAP_ARROW_SCHEMA = pa.schema([
    pa.field("scenario_name", pa.utf8(), nullable=False),
    pa.field("month", pa.int32(), nullable=False),
    pa.field("batch_idx", pa.int32(), nullable=False),
    pa.field("feature_name", pa.utf8(), nullable=False),
    pa.field("shap_value", pa.float64(), nullable=False),
    pa.field("feature_value", pa.float64(), nullable=True),
    pa.field("base_value", pa.float64(), nullable=False),
    pa.field("explainer_type", pa.utf8(), nullable=False),
])

SHAP_SUMMARY_ARROW_SCHEMA = pa.schema([
    pa.field("scenario_name", pa.utf8(), nullable=False),
    pa.field("feature_name", pa.utf8(), nullable=False),
    pa.field("mean_abs_shap", pa.float64(), nullable=False),
    pa.field("std_shap", pa.float64(), nullable=False),
    pa.field("mean_feature_value", pa.float64(), nullable=True),
    pa.field("importance_rank", pa.int32(), nullable=False),
])


# ---------------------------------------------------------------------------
# Telemetry schema for simulation run logs
# ---------------------------------------------------------------------------

TELEMETRY_ARROW_SCHEMA = pa.schema([
    pa.field("timestamp", pa.timestamp("us"), nullable=False),
    pa.field("run_id", pa.utf8(), nullable=False),
    pa.field("scenario_name", pa.utf8(), nullable=False),
    pa.field("tick", pa.int32(), nullable=False),
    pa.field("month", pa.int32(), nullable=False),
    pa.field("patient_count", pa.int32(), nullable=False),
    pa.field("provider_count", pa.int32(), nullable=False),
    pa.field("total_visits", pa.int32(), nullable=False),
    pa.field("capitation_flow", pa.float64(), nullable=False),
    pa.field("ffs_flow", pa.float64(), nullable=False),
    pa.field("total_funding_flow", pa.float64(), nullable=False),
    pa.field("avg_wait_days", pa.float64(), nullable=True),
    pa.field("unmet_demand", pa.int32(), nullable=False),
    pa.field("cpu_usage_pct", pa.float64(), nullable=True),
    pa.field("memory_mb", pa.float64(), nullable=True),
])


# ---------------------------------------------------------------------------
# Conversion helpers: pydantic -> Arrow Table
# ---------------------------------------------------------------------------


def patients_to_table(patients: List[PatientProfile]) -> pa.Table:
    """Convert a list of PatientProfile pydantic models to an Arrow Table."""
    arrays = [
        pa.array([p.age for p in patients], type=pa.int32()),
        pa.array([p.gender.value for p in patients], type=pa.utf8()),
        pa.array([p.ethnicity.value for p in patients], type=pa.utf8()),
        pa.array([p.deprivation_index for p in patients], type=pa.int32()),
        pa.array([p.comorbidities for p in patients], type=pa.list_(pa.utf8())),
        pa.array([p.enrollment_status.value for p in patients], type=pa.utf8()),
    ]
    return pa.Table.from_arrays(arrays, schema=PATIENT_ARROW_SCHEMA)


def providers_to_table(providers: List[ProviderProfile]) -> pa.Table:
    """Convert a list of ProviderProfile pydantic models to an Arrow Table."""
    arrays = [
        pa.array([p.id for p in providers], type=pa.utf8()),
        pa.array([p.type.value for p in providers], type=pa.utf8()),
        pa.array([p.region for p in providers], type=pa.utf8()),
        pa.array([p.patient_list for p in providers], type=pa.list_(pa.utf8())),
        pa.array([p.capacity for p in providers], type=pa.int32()),
        pa.array([p.capitation_panel_size for p in providers], type=pa.int32()),
    ]
    return pa.Table.from_arrays(arrays, schema=PROVIDER_ARROW_SCHEMA)


def config_to_table(config: SimulationConfig) -> pa.Table:
    """Convert a SimulationConfig to a single-row Arrow Table."""
    arrays = [
        pa.array([config.seed], type=pa.int32()),
        pa.array([config.num_patients], type=pa.int32()),
        pa.array([config.num_providers], type=pa.int32()),
        pa.array([config.time_horizon_months], type=pa.int32()),
        pa.array([config.tick_interval_days], type=pa.int32()),
    ]
    return pa.Table.from_arrays(arrays, schema=CONFIG_ARROW_SCHEMA)


def metrics_to_table(metrics: List[MonthlyMetrics]) -> pa.Table:
    """Convert a list of MonthlyMetrics to an Arrow Table."""
    arrays = [
        pa.array([m.month for m in metrics], type=pa.int32()),
        pa.array([m.total_patients for m in metrics], type=pa.int32()),
        pa.array([m.total_providers for m in metrics], type=pa.int32()),
        pa.array([m.total_visits for m in metrics], type=pa.int32()),
        pa.array([m.total_capitation_payments for m in metrics], type=pa.float64()),
        pa.array([m.total_ffs_payments for m in metrics], type=pa.float64()),
        pa.array([m.total_funding for m in metrics], type=pa.float64()),
        pa.array([m.avg_wait_time_days for m in metrics], type=pa.float64()),
        pa.array([m.unmet_demand for m in metrics], type=pa.int32()),
    ]
    return pa.Table.from_arrays(arrays, schema=MONTHLY_METRICS_ARROW_SCHEMA)

# ---------------------------------------------------------------------------
# Zero-copy: Arrow Table -> Polars DataFrame
# ---------------------------------------------------------------------------


def _require_polars() -> Any:
    if pl is None:
        raise ImportError("Install polars to use dataframe conversion and aggregation helpers.")
    return pl


def table_to_dataframe(table: pa.Table) -> pl.DataFrame:
    """Convert an Arrow Table to a Polars DataFrame (zero-copy)."""
    polars = _require_polars()
    return polars.from_arrow(table)


def dataframe_to_table(df: pl.DataFrame) -> pa.Table:
    """Convert a Polars DataFrame back to an Arrow Table (zero-copy)."""
    return df.to_arrow()


# ---------------------------------------------------------------------------
# Telemetry conversion helpers
# ---------------------------------------------------------------------------


def telemetry_to_table(records: List[Dict[str, Any]]) -> pa.Table:
    """Convert a list of telemetry dicts to an Arrow Table.

    Expected dict keys match TELEMETRY_ARROW_SCHEMA field names.
    """
    arrays = []
    for field in TELEMETRY_ARROW_SCHEMA:
        col = pa.array(
            [r.get(field.name, None) for r in records],
            type=field.type,
        )
        arrays.append(col)
    return pa.Table.from_arrays(arrays, schema=TELEMETRY_ARROW_SCHEMA)


def telemetry_to_dataframe(records: List[Dict[str, Any]]) -> pl.DataFrame:
    """Convert telemetry dicts directly to a Polars DataFrame."""
    table = telemetry_to_table(records)
    return table_to_dataframe(table)


# ---------------------------------------------------------------------------
# IPC serialisation helpers
# ---------------------------------------------------------------------------

IPC_WRITE_OPTIONS = ipc.IpcWriteOptions(
    compression="zstd",
)
IPC_OPTIONS = IPC_WRITE_OPTIONS


def write_record_batches(table: pa.Table, sink: io.IOBase) -> int:
    """Write an Arrow Table as IPC record batches to a writable stream.

    Parameters
    ----------
    table : pa.Table
        Table to serialise.
    sink : io.IOBase
        A writable binary stream (file, BytesIO, etc.).

    Returns
    -------
    int
        Number of record batches written.
    """
    batch_count = 0
    with ipc.new_stream(sink, table.schema, options=IPC_WRITE_OPTIONS) as writer:
        for batch in table.to_batches():
            writer.write_batch(batch)
            batch_count += 1
    return batch_count


def read_record_batches(source: io.IOBase) -> pa.Table:
    """Read IPC record batches from a readable stream back into an Arrow Table.

    Parameters
    ----------
    source : io.IOBase
        A readable binary stream.

    Returns
    -------
    pa.Table
        The reconstructed table.
    """
    batches: List[pa.RecordBatch] = []
    with ipc.open_stream(source) as reader:
        for batch in reader:
            batches.append(batch)
    if not batches:
        return pa.Table.from_batches([], schema=pa.schema([]))
    return pa.Table.from_batches(batches)


def serialise_to_bytes(table: pa.Table) -> bytes:
    """Serialise an Arrow Table to compressed IPC bytes."""
    buf = io.BytesIO()
    write_record_batches(table, buf)
    return buf.getvalue()


def deserialise_from_bytes(data: bytes) -> pa.Table:
    """Deserialise IPC bytes back into an Arrow Table."""
    buf = io.BytesIO(data)
    return read_record_batches(buf)


# ---------------------------------------------------------------------------
# Result serialisation
# ---------------------------------------------------------------------------


def result_to_table(result: SimulationResult) -> pa.Table:
    """Convert a SimulationResult to an Arrow Table of monthly metrics."""
    return metrics_to_table(result.monthly_metrics)


def result_to_dataframe(result: SimulationResult) -> pl.DataFrame:
    """Convert a SimulationResult to a Polars DataFrame."""
    polars = _require_polars()
    flat = [
        {
            "scenario_name": result.scenario_name,
            **m.model_dump(),
            **result.summary_metrics,
            **result.metadata,
        }
        for m in result.monthly_metrics
    ]
    return polars.DataFrame(flat)


# ---------------------------------------------------------------------------
# Polars query examples for common aggregations
# ---------------------------------------------------------------------------


def aggregate_by_ethnicity(metrics_df: pl.DataFrame, patients_df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate monthly metrics stratified by patient ethnicity.

    Parameters
    ----------
    metrics_df : pl.DataFrame
        Monthly metrics data with 'month' and 'total_patients' columns.
    patients_df : pl.DataFrame
        Patient profiles with 'ethnicity' column.

    Returns
    -------
    pl.DataFrame
        Aggregated summary by ethnicity group.
    """
    polars = _require_polars()
    return (
        patients_df
        .group_by("ethnicity")
        .agg([
            polars.count().alias("patient_count"),
            polars.col("age").mean().alias("avg_age"),
            polars.col("deprivation_index").mean().alias("avg_deprivation"),
            polars.col("comorbidities").list.len().mean().alias("avg_comorbidities"),
        ])
        .sort("ethnicity")
    )


def aggregate_by_region(metrics_df: pl.DataFrame, providers_df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate monthly metrics stratified by provider region.

    Parameters
    ----------
    metrics_df : pl.DataFrame
        Monthly metrics with 'total_visits', 'total_funding' columns.
    providers_df : pl.DataFrame
        Provider profiles with 'region' column.

    Returns
    -------
    pl.DataFrame
        Aggregated summary by region.
    """
    polars = _require_polars()
    return (
        providers_df
        .group_by("region")
        .agg([
            polars.count().alias("provider_count"),
            polars.col("capacity").sum().alias("total_capacity"),
            polars.col("capitation_panel_size").sum().alias("total_capitation_panel"),
        ])
        .sort("region")
    )


def aggregate_by_month(metrics_df: pl.DataFrame) -> pl.DataFrame:
    """Compute summary statistics per month across all scenarios.

    Parameters
    ----------
    metrics_df : pl.DataFrame
        Monthly metrics with 'month', 'total_funding',
        'total_visits', 'unmet_demand' columns.

    Returns
    -------
    pl.DataFrame
        Per-month aggregated statistics.
    """
    polars = _require_polars()
    return (
        metrics_df
        .group_by("month")
        .agg([
            polars.col("total_patients").first().alias("patients"),
            polars.col("total_providers").first().alias("providers"),
            polars.col("total_visits").sum().alias("total_visits"),
            polars.col("total_funding").sum().alias("total_funding"),
            polars.col("total_capitation_payments").sum().alias("total_capitation"),
            polars.col("total_ffs_payments").sum().alias("total_ffs"),
            polars.col("unmet_demand").sum().alias("total_unmet_demand"),
            polars.col("avg_wait_time_days").mean().alias("mean_wait_days"),
        ])
        .sort("month")
    )


def funding_flow_summary(metrics_df: pl.DataFrame) -> pl.DataFrame:
    """Break down total funding flow by funding source across all months.

    Parameters
    ----------
    metrics_df : pl.DataFrame
        Monthly metrics with funding columns.

    Returns
    -------
    pl.DataFrame
        Single-row summary of capitation vs FFS proportions.
    """
    polars = _require_polars()
    return (
        metrics_df
        .select([
            polars.col("total_capitation_payments").sum().alias("total_capitation"),
            polars.col("total_ffs_payments").sum().alias("total_ffs"),
            polars.col("total_funding").sum().alias("total_funding"),
        ])
        .with_columns([
            (polars.col("total_capitation") / polars.col("total_funding") * 100).alias("capitation_pct"),
            (polars.col("total_ffs") / polars.col("total_funding") * 100).alias("ffs_pct"),
        ])
    )


# ---------------------------------------------------------------------------
# SHAP attribution conversion helpers
# ---------------------------------------------------------------------------


def shap_records_to_table(
    records: list[dict[str, Any]],
) -> pa.Table:
    """Convert a list of SHAP attribution dicts to an Arrow Table.

    Expected keys: scenario_name, month, batch_idx, feature_name,
    shap_value, feature_value, base_value, explainer_type.
    """
    arrays = []
    for field in SHAP_ARROW_SCHEMA:
        col = pa.array(
            [r.get(field.name, None) for r in records],
            type=field.type,
        )
        arrays.append(col)
    return pa.Table.from_arrays(arrays, schema=SHAP_ARROW_SCHEMA)


def shap_summary_to_table(
    records: list[dict[str, Any]],
) -> pa.Table:
    """Convert a list of SHAP summary dicts to an Arrow Table.

    Expected keys: scenario_name, feature_name, mean_abs_shap,
    std_shap, mean_feature_value, importance_rank.
    """
    arrays = []
    for field in SHAP_SUMMARY_ARROW_SCHEMA:
        col = pa.array(
            [r.get(field.name, None) for r in records],
            type=field.type,
        )
        arrays.append(col)
    return pa.Table.from_arrays(arrays, schema=SHAP_SUMMARY_ARROW_SCHEMA)
