"""Typed engine adapter entrypoints for GTPCNZ model calculation engines.

Each adapter in this package implements the ``EngineProtocol`` and provides a
pure, deterministic (or seeded-stochastic) calculation method.  No Streamlit
imports are permitted in this package.
"""

from models.primarycare_model.engines.abm_adapter import AgentBasedModelAdapter
from models.primarycare_model.engines.diffusion_adapter import BassDiffusionAdapter
from models.primarycare_model.engines.jax_mc_adapter import MonteCarloAdapter
from models.primarycare_model.engines.mpc_adapter import ModelPredictiveControlAdapter
from models.primarycare_model.engines.nash_opt_adapter import NashOptimisationAdapter
from models.primarycare_model.engines.sd_adapter import SystemDynamicsAdapter
from models.primarycare_model.engines.sensitivity_adapter import SensitivityAnalysisAdapter

__all__ = [
    "AgentBasedModelAdapter",
    "BassDiffusionAdapter",
    "ModelPredictiveControlAdapter",
    "MonteCarloAdapter",
    "NashOptimisationAdapter",
    "SensitivityAnalysisAdapter",
    "SystemDynamicsAdapter",
]
