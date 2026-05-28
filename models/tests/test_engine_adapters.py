"""Tests for engine adapters."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from models.primarycare_model.contracts.engine import EngineProtocol
from models.primarycare_model.engines import (
    AgentBasedModelAdapter,
    BassDiffusionAdapter,
    ModelPredictiveControlAdapter,
    MonteCarloAdapter,
    NashOptimisationAdapter,
    SensitivityAnalysisAdapter,
    SystemDynamicsAdapter,
)
from models.primarycare_model.engines.abm_adapter import ABMInput, ABMOutput
from models.primarycare_model.engines.diffusion_adapter import DiffusionInput, DiffusionOutput
from models.primarycare_model.engines.jax_mc_adapter import MCInput, MCOutput
from models.primarycare_model.engines.mpc_adapter import MPCInput, MPCOutput
from models.primarycare_model.engines.nash_opt_adapter import NashInput, NashOutput
from models.primarycare_model.engines.sd_adapter import SDInput, SDOutput
from models.primarycare_model.engines.sensitivity_adapter import SensitivityInput, SensitivityOutput

CLAIM = "test"

def test_all_adapters_can_be_instantiated():
    for a in [SystemDynamicsAdapter(), AgentBasedModelAdapter(),
              BassDiffusionAdapter(), MonteCarloAdapter(),
              ModelPredictiveControlAdapter(), NashOptimisationAdapter(),
              SensitivityAnalysisAdapter()]:
        assert isinstance(a, EngineProtocol)

def test_all_adapters_have_engine_id():
    for a in [SystemDynamicsAdapter(), AgentBasedModelAdapter(),
              BassDiffusionAdapter(), MonteCarloAdapter(),
              ModelPredictiveControlAdapter(), NashOptimisationAdapter(),
              SensitivityAnalysisAdapter()]:
        assert hasattr(a, 'engine_id') and isinstance(a.engine_id, str) and len(a.engine_id) > 0

def test_sd_adapter_accepts_valid_input():
    a = SystemDynamicsAdapter()
    inp = SDInput(scenario_id="F4", months=24, seed=42, claim_boundary=CLAIM,
                  activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                  scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                  governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                  budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    out = a.run(inp)
    assert isinstance(out, SDOutput)
    assert 0 <= out.scenario_result.hybrid_viability_score <= 100
    assert len(out.monthly_trace) == 24

def test_sd_adapter_deterministic():
    a = SystemDynamicsAdapter()
    kw = dict(scenario_id="F0", months=12, seed=42, claim_boundary=CLAIM,
              activity_signal=50.0, capitation=50.0, place_accountability=50.0,
              scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
              governance=50.0, equity_protection=50.0, copayment_burden=50.0,
              budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    o1, o2 = a.run(SDInput(**kw)), a.run(SDInput(**kw))
    assert o1.scenario_result.hybrid_viability_score == o2.scenario_result.hybrid_viability_score
    assert o1.monthly_trace == o2.monthly_trace

def test_sd_adapter_rejects_out_of_range_months():
    with pytest.raises(ValidationError):
        SDInput(scenario_id="F0", months=200, seed=42, claim_boundary=CLAIM,
                activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)

def test_abm_adapter_runs():
    a = AgentBasedModelAdapter()
    inp = ABMInput(scenario_id="F4", population_size=100, months=6, seed=42, claim_boundary=CLAIM,
                   activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                   scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                   governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                   budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    out = a.run(inp)
    assert isinstance(out, ABMOutput)
    assert len(out.agent_data) == 100

def test_abm_adapter_deterministic():
    a = AgentBasedModelAdapter()
    kw = dict(scenario_id="F0", population_size=80, months=6, seed=42, claim_boundary=CLAIM,
              activity_signal=50.0, capitation=50.0, place_accountability=50.0,
              scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
              governance=50.0, equity_protection=50.0, copayment_burden=50.0,
              budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    o1, o2 = a.run(ABMInput(**kw)), a.run(ABMInput(**kw))
    assert o1.scenario_result.access_score == o2.scenario_result.access_score
    assert o1.agent_data == o2.agent_data

def test_diffusion_adapter_runs():
    a = BassDiffusionAdapter()
    inp = DiffusionInput(scenario_id="F4", months=36, seed=42, claim_boundary=CLAIM,
                         p_coefficient=0.03, q_coefficient=0.40, market_potential=1000.0,
                         initial_adopters=10.0, activity_signal=50.0, scope_capacity=50.0, governance=50.0)
    out = a.run(inp)
    assert isinstance(out, DiffusionOutput)
    assert out.cumulative_adopters > 0
    assert 1 <= out.peak_adoption_month <= 36

def test_diffusion_adapter_deterministic():
    a = BassDiffusionAdapter()
    kw = dict(scenario_id="F0", months=24, seed=42, claim_boundary=CLAIM,
              p_coefficient=0.02, q_coefficient=0.30, market_potential=500.0,
              initial_adopters=5.0, activity_signal=50.0, scope_capacity=50.0, governance=50.0)
    o1, o2 = a.run(DiffusionInput(**kw)), a.run(DiffusionInput(**kw))
    assert o1.cumulative_adopters == o2.cumulative_adopters
    assert o1.peak_adoption_month == o2.peak_adoption_month

def test_mc_adapter_runs():
    a = MonteCarloAdapter()
    inp = MCInput(scenario_id="F4", draws=20, seed=42, claim_boundary=CLAIM, perturbation_sd=0.05,
                  activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                  scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                  governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                  budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    out = a.run(inp)
    assert isinstance(out, MCOutput)
    assert len(out.draw_data) == 20
    assert len(out.uncertainty_summaries) >= 5

def test_mc_adapter_deterministic():
    a = MonteCarloAdapter()
    kw = dict(scenario_id="F0", draws=15, seed=42, claim_boundary=CLAIM, perturbation_sd=0.05,
              activity_signal=50.0, capitation=50.0, place_accountability=50.0,
              scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
              governance=50.0, equity_protection=50.0, copayment_burden=50.0,
              budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    o1, o2 = a.run(MCInput(**kw)), a.run(MCInput(**kw))
    assert o1.scenario_result.hybrid_viability_score == o2.scenario_result.hybrid_viability_score

def test_mc_adapter_uncertainty_summaries():
    a = MonteCarloAdapter()
    inp = MCInput(scenario_id="F4", draws=50, seed=42, claim_boundary=CLAIM, perturbation_sd=0.08,
                  activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                  scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                  governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                  budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    out = a.run(inp)
    for s in out.uncertainty_summaries:
        assert s.p05 <= s.p50 <= s.p95
        assert s.draws == 50

def test_mpc_adapter_runs():
    a = ModelPredictiveControlAdapter()
    inp = MPCInput(scenario_id="F4", seed=42, claim_boundary=CLAIM, horizon=12, n_control_steps=3,
                   activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                   scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                   governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                   budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    out = a.run(inp)
    assert isinstance(out, MPCOutput)
    assert len(out.control_trajectory) == 12
    assert len(out.optimised_levers) == 12

def test_mpc_adapter_optimised_levers_in_bounds():
    a = ModelPredictiveControlAdapter()
    inp = MPCInput(scenario_id="F4", seed=42, claim_boundary=CLAIM, horizon=6, n_control_steps=2,
                   activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                   scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                   governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                   budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)
    out = a.run(inp)
    for v in out.optimised_levers.values():
        assert 0.0 <= v <= 100.0

def test_nash_adapter_runs():
    a = NashOptimisationAdapter()
    inp = NashInput(scenario_id="F4", seed=42, claim_boundary=CLAIM,
                    funder_audit=50.0, funder_place_accountability=60.0,
                    provider_effort=50.0, provider_scope_utilisation=50.0,
                    budget_tightness=60.0, complexity=50.0, activity_signal=70.0)
    out = a.run(inp)
    assert isinstance(out, NashOutput)
    assert 0 <= out.equilibrium_funder_audit <= 100
    assert 0 <= out.equilibrium_provider_effort <= 100

def test_nash_adapter_converges():
    a = NashOptimisationAdapter()
    inp = NashInput(scenario_id="F4", max_iterations=100, seed=42, claim_boundary=CLAIM,
                    funder_audit=50.0, funder_place_accountability=60.0,
                    provider_effort=50.0, provider_scope_utilisation=50.0,
                    budget_tightness=60.0, complexity=50.0, activity_signal=70.0)
    out = a.run(inp)
    assert out.iterations_to_converge <= 100

def test_sensitivity_adapter_runs():
    a = SensitivityAnalysisAdapter()
    inp = SensitivityInput(scenario_id="F4", seed=42, claim_boundary=CLAIM,
                           baseline_activity_signal=50.0, baseline_capitation=50.0,
                           baseline_place_accountability=50.0, baseline_scope_capacity=50.0,
                           baseline_urgent_ambulance=50.0, baseline_data_visibility=50.0,
                           baseline_governance=50.0, baseline_equity_protection=50.0,
                           baseline_copayment_burden=50.0, baseline_budget_tightness=50.0,
                           baseline_hospital_salience=50.0, baseline_complexity=50.0,
                           low_percentile=25.0, high_percentile=75.0, delta_step=10.0)
    out = a.run(inp)
    assert isinstance(out, SensitivityOutput)
    assert len(out.oat_sensitivities) == 24

def test_engine_input_rejects_empty_scenario_id():
    with pytest.raises(ValidationError):
        SDInput(scenario_id="", months=12, seed=42, claim_boundary=CLAIM,
                activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)

def test_engine_input_rejects_empty_claim_boundary():
    with pytest.raises(ValidationError):
        SDInput(scenario_id="F0", months=12, seed=42, claim_boundary="",
                activity_signal=50.0, capitation=50.0, place_accountability=50.0,
                scope_capacity=50.0, urgent_ambulance=50.0, data_visibility=50.0,
                governance=50.0, equity_protection=50.0, copayment_burden=50.0,
                budget_tightness=50.0, hospital_salience=50.0, complexity=50.0)

def test_engine_modules_do_not_import_streamlit():
    import ast
    from pathlib import Path
    engines_dir = Path("models/primarycare_model/engines")
    for py_file in engines_dir.rglob("*.py"):
        if py_file.name.startswith("_"):
            continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name != "streamlit"
                    assert not alias.name.startswith("streamlit.")
            if isinstance(node, ast.ImportFrom) and node.module:
                assert node.module != "streamlit"
                assert not node.module.startswith("streamlit.")
