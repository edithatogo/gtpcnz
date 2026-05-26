import numpy as np

from primarycare_model.diffusion import BassDiffusionParams, simulate_bass
from primarycare_model.ipc import ArrowMemoryChannel
from primarycare_model.jax_mc import MCConfig, compute_summary_stats, run_deterministic, run_mc_sweep, run_monte_carlo
from primarycare_model.mpc import compute_mpc_cost, optimize_policy
from primarycare_model.nash_opt import PayoffMatrix, nash_best_response_dynamics
from primarycare_model.sensitivity import compute_sobol_indices, param_ranges_to_table, scale_samples_to_params
from primarycare_model.schemas import FundingModel, ScenarioParams, SimulationConfig
from primarycare_model.shap_explainer import FEATURE_NAMES, SHAPAttribution
from scripts.bayesian_opt import run_bayesian_optimization


def test_jax_mc_imports_and_runs_without_required_jax():
    config = SimulationConfig(seed=7, time_horizon_months=3)
    scenario = ScenarioParams(
        name="hybrid-test",
        funding_model=FundingModel.HYBRID,
        capitation_rate=82.0,
        ffs_fee_schedule={"gp_visit": 47.0, "nurse_visit": 28.0},
    )

    sweep = run_mc_sweep(config, scenario, batch_size=2)
    assert sweep.trajectories.shape == (2, 3, 8)
    assert sweep.to_arrow().num_rows == 6

    stats = compute_summary_stats(sweep)
    assert stats["batch_size"] == 2
    assert stats["n_steps"] == 3
    assert stats["engine"] in {"numpy", "jax"}

    deterministic = run_deterministic(config, scenario)
    assert deterministic.scenario_name == "hybrid-test"
    assert len(deterministic.monthly_metrics) == 3


def test_rolling_monte_carlo_is_seeded_and_bounded():
    result = run_monte_carlo(MCConfig(num_iterations=10, num_batches=3, seed=11))
    assert set(result.metrics) >= {"access_rate", "hospital_pressure_index", "provider_utilisation"}
    assert all(len(values) == 10 for values in result.metrics.values())
    assert all(np.all((values >= 0.0) & (values <= 1.0)) for values in result.metrics.values())

    mean, lower, upper = result.rolling_ci("access_rate", window=4)
    assert len(mean) == 7
    assert np.all(lower <= mean)
    assert np.all(mean <= upper)


def test_bass_diffusion_and_nash_outputs_are_chart_ready():
    diffusion = simulate_bass(BassDiffusionParams(T=5, M=100, initial_adopters=4, num_regions=3))
    assert list(diffusion.time_series.columns) == [
        "year",
        "adopters",
        "new_adopters",
        "adoption_rate",
        "remaining",
        "p",
        "q",
        "M",
    ]
    assert diffusion.region_time_series is not None
    assert diffusion.time_series["adoption_rate"].between(0, 1).all()

    trace = nash_best_response_dynamics(PayoffMatrix.clinical_utility(), max_iterations=25)
    frame = trace.to_dataframe()
    assert not frame.empty
    assert {"p0_payoff", "p1_payoff", "total_welfare"}.issubset(frame.columns)


def test_shap_attribution_serialises_to_arrow_tables():
    data = np.array([[80.0, 45.0, 25.0], [90.0, 50.0, 30.0]])
    values = np.array([[0.2, -0.1, 0.05], [0.1, 0.03, -0.02]])
    attribution = SHAPAttribution(
        scenario_name="test",
        feature_names=FEATURE_NAMES[:3],
        shap_values=values,
        base_values=np.array(1.0),
        data=data,
        explainer_type="synthetic-test",
    )

    assert attribution.to_arrow_table().num_rows == 6
    summary = attribution.to_summary_table()
    assert summary.num_rows == 3
    assert summary.column("importance_rank").to_pylist() == [1, 2, 3]


def test_arrow_memory_channel_round_trips_sweep_table():
    config = SimulationConfig(seed=3, time_horizon_months=2)
    scenario = ScenarioParams(
        name="capitation-test",
        funding_model=FundingModel.CAPITATION,
        capitation_rate=80.0,
    )
    table = run_mc_sweep(config, scenario, batch_size=1).to_arrow()

    channel = ArrowMemoryChannel()
    channel.open(table.schema)
    channel.write_table(table)
    channel.close()

    round_tripped = channel.read_all()
    assert round_tripped.num_rows == table.num_rows
    assert round_tripped.schema == table.schema


def test_sensitivity_mpc_and_bayesian_optimisation_fallbacks_run():
    assert param_ranges_to_table().num_rows >= 7
    scaled = scale_samples_to_params(np.full((2, 7), 0.5))
    assert scaled.shape == (2, 7)

    sobol = compute_sobol_indices(n_eval=32)
    assert len(sobol["param_names"]) == 7
    assert np.asarray(sobol["S1"]).shape == (7,)

    state = np.array([10000.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    base_params = np.array([80.0, 45.0, 25.0, 0.05, 0.03, 0.5, 2.0])
    params, costs = optimize_policy(state, base_params, n_steps=2, n_iterations=3)
    assert params.shape == base_params.shape
    assert costs
    assert compute_mpc_cost(np.tile(state, (2, 1))) >= 0

    bounds = np.array([[0.0, 1.0], [0.0, 1.0]])
    result = run_bayesian_optimization(lambda x: float(np.sum((x - 0.25) ** 2)), bounds, n_init=3, n_iter=2)
    assert result["best_params"].shape == (2,)
    assert result["all_params"].shape[0] == 5
