"""
Pydantic v2 schemas for the Primary Care Funding Architecture simulation.

Defines the core data models used throughout the simulation engine,
including configuration, scenario parameters, patient/provider profiles,
policy parameters, and simulation results.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class FundingModel(StrEnum):
    CAPITATION = "capitation"
    FFS = "ffs"
    HYBRID = "hybrid"


class Ethnicity(StrEnum):
    EUROPEAN = "european"
    MAORI = "maori"
    PACIFIC = "pacific"
    ASIAN = "asian"
    MELAA = "melaa"
    OTHER = "other"


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNSPECIFIED = "unspecified"


class EnrollmentStatus(StrEnum):
    ENROLLED = "enrolled"
    CASUAL = "casual"
    PENDING = "pending"
    DECLINED = "declined"


class ProviderType(StrEnum):
    GP = "gp"
    NURSE = "nurse"
    PRACTICE = "practice"

# placeholder

class SimulationConfig(BaseModel):
    """Top-level configuration for a simulation run."""

    seed: int = Field(default=42, ge=0, description="Random seed for reproducibility")
    num_patients: int = Field(default=10_000, gt=0, description="Number of synthetic patients")
    num_providers: int = Field(default=50, gt=0, description="Number of provider entities")
    time_horizon_months: int = Field(default=36, gt=0, le=120, description="Simulation duration in months")
    tick_interval_days: int = Field(default=1, gt=0, le=90, description="Tick granularity in days")

    @field_validator("tick_interval_days")
    @classmethod
    def tick_interval_must_divide_month(cls, v: int) -> int:
        if 30 % v != 0:
            raise ValueError(f"tick_interval_days={v} does not evenly divide 30")
        return v

    @field_validator("num_patients")
    @classmethod
    def patients_must_be_reasonable(cls, v: int) -> int:
        if v > 1_000_000:
            raise ValueError(f"num_patients={v} exceeds 1M")
        return v


class PolicyParams(BaseModel):
    """A configurable policy intervention applied during the simulation."""

    name: str = Field(..., min_length=1, description="Unique identifier for the policy")
    description: str | None = Field(None, description="Free-text description of the policy intent")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Arbitrary key-value policy parameters")
    target_population: str | None = Field(None, description="CQL-like filter expression for target cohort")
    start_month: int = Field(..., ge=0, description="Month offset (0-based) when policy starts")
    end_month: int | None = Field(None, ge=0, description="Month offset when policy ends; None = no end")

    @model_validator(mode="after")
    def validate_end_after_start(self) -> PolicyParams:
        if self.end_month is not None and self.end_month <= self.start_month:
            raise ValueError(f"end_month ({self.end_month}) must be > start_month ({self.start_month})")
        return self

class ScenarioParams(BaseModel):
    """A named simulation scenario bundling policy parameters with a funding model."""

    name: str = Field(..., min_length=1, description="Human-readable scenario name")
    description: str | None = Field(None, description="Longer description of the scenario rationale")
    policy_params: list[PolicyParams] = Field(default_factory=list, description="Active policies in this scenario")
    funding_model: FundingModel = Field(..., description="Funding model type (capitation / ffs / hybrid)")
    capitation_rate: float | None = Field(None, ge=0.0, description="Per-patient-per-month capitation rate (NZD)")
    ffs_fee_schedule: dict[str, float] | None = Field(None, description="FFS schedule mapping visit type codes to NZD amounts")

    @model_validator(mode="after")
    def validate_funding_params(self) -> ScenarioParams:
        if self.funding_model == FundingModel.CAPITATION and self.capitation_rate is None:
            raise ValueError("capitation_rate required when funding_model='capitation'")
        if self.funding_model == FundingModel.FFS and (self.ffs_fee_schedule is None or len(self.ffs_fee_schedule) == 0):
            raise ValueError("ffs_fee_schedule required when funding_model='ffs'")
        if self.funding_model == FundingModel.HYBRID:
            if self.capitation_rate is None:
                raise ValueError("capitation_rate required when funding_model='hybrid'")
            if self.ffs_fee_schedule is None or len(self.ffs_fee_schedule) == 0:
                raise ValueError("ffs_fee_schedule required when funding_model='hybrid'")
        return self


class PatientProfile(BaseModel):
    """Demographics and health-status attributes for a synthetic patient."""

    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    gender: Gender = Field(..., description="Patient gender")
    ethnicity: Ethnicity = Field(..., description="Patient ethnicity group")
    deprivation_index: int = Field(..., ge=1, le=10, description="NZDep2018 deprivation decile (1=least, 10=most)")
    comorbidities: list[str] = Field(default_factory=list, description="Chronic condition codes e.g. ['diabetes','asthma']")
    enrollment_status: EnrollmentStatus = Field(default=EnrollmentStatus.ENROLLED, description="Current enrollment status")

    @field_validator("comorbidities")
    @classmethod
    def deduplicate_comorbidities(cls, v: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in v:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result


class ProviderProfile(BaseModel):
    """Attributes of a primary care provider (practice, GP, or nurse)."""

    id: str = Field(..., min_length=1, description="Unique provider identifier")
    type: ProviderType = Field(..., description="Role category (gp / nurse / practice)")
    region: str = Field(..., min_length=1, description="Geographic region or DHB code")
    patient_list: list[str] = Field(default_factory=list, description="Patient IDs rostered to this provider")
    capacity: int = Field(default=1500, ge=0, description="Maximum number of enrolled patients")
    capitation_panel_size: int = Field(default=0, ge=0, description="Patients funded via capitation")


class MonthlyMetrics(BaseModel):
    """Per-month aggregated metrics produced by a simulation run."""

    month: int = Field(..., ge=0, description="Month offset from simulation start (0-based)")
    total_patients: int = Field(..., ge=0, description="Active patient count at end of month")
    total_providers: int = Field(..., ge=0, description="Active provider count at end of month")
    total_visits: int = Field(..., ge=0, description="Total GP/nurse visits during the month")
    total_capitation_payments: float = Field(..., ge=0.0, description="Total capitation funding disbursed (NZD)")
    total_ffs_payments: float = Field(..., ge=0.0, description="Total fee-for-service payments (NZD)")
    total_funding: float = Field(..., ge=0.0, description="Aggregate funding flow for the month (NZD)")
    avg_wait_time_days: float | None = Field(None, ge=0.0, description="Average patient wait time (days)")
    unmet_demand: int = Field(default=0, ge=0, description="Appointment requests that could not be scheduled")


class SimulationResult(BaseModel):
    """Complete output record for one simulation + scenario combination."""

    scenario_name: str = Field(..., min_length=1, description="Name of the scenario that was run")
    monthly_metrics: list[MonthlyMetrics] = Field(..., description="Time-series of per-month metrics")
    summary_metrics: dict[str, Any] = Field(default_factory=dict, description="Aggregated KPIs")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Run-level metadata")

    @field_validator("monthly_metrics")
    @classmethod
    def at_least_one_month(cls, v: list[MonthlyMetrics]) -> list[MonthlyMetrics]:
        if len(v) < 1:
            raise ValueError("monthly_metrics must contain at least one entry")
        return v

    def to_flat_dict(self) -> dict[str, Any]:
        """Flatten result into a single dict for DataFrame construction."""
        return {"scenario_name": self.scenario_name, **self.summary_metrics, **self.metadata}
