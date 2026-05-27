"""Typed contracts for GTPCNZ model inputs, scenarios, engines and outputs."""

from models.primarycare_model.contracts.parameters import ParameterDefinition, ParameterValue
from models.primarycare_model.contracts.scenarios import EducationalLeverDefinition, RuntimeScenarioDefinition

ToyLeverDefinition = EducationalLeverDefinition

__all__ = [
    "EducationalLeverDefinition",
    "ParameterDefinition",
    "ParameterValue",
    "RuntimeScenarioDefinition",
    "ToyLeverDefinition",
]
