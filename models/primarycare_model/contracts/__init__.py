"""Typed contracts for GTPCNZ model inputs, scenarios, engines and outputs."""

from models.primarycare_model.contracts.engine import EngineInput, EngineOutput, EngineProtocol, UncertaintySummary
from models.primarycare_model.contracts.inputs import InputDataset, InputField, ProvenanceEntry, ProvenanceStatus
from models.primarycare_model.contracts.oia import ComponentType, OIAComponentEntry
from models.primarycare_model.contracts.parameters import (
    ParameterDefinition,
    ParameterValue,
    ParameterVector,
    StrictContract,
)
from models.primarycare_model.contracts.results import ResultManifest, ScenarioResult
from models.primarycare_model.contracts.scenarios import (
    EducationalLeverDefinition,
    RuntimeScenarioDefinition,
    ScenarioOverride,
)

ToyLeverDefinition = EducationalLeverDefinition

__all__ = [
    "ComponentType",
    "EducationalLeverDefinition",
    "EngineInput",
    "EngineOutput",
    "EngineProtocol",
    "InputDataset",
    "InputField",
    "OIAComponentEntry",
    "ParameterDefinition",
    "ParameterValue",
    "ParameterVector",
    "ProvenanceEntry",
    "ProvenanceStatus",
    "ResultManifest",
    "RuntimeScenarioDefinition",
    "ScenarioOverride",
    "ScenarioResult",
    "StrictContract",
    "ToyLeverDefinition",
    "UncertaintySummary",
]
