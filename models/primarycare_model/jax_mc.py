"""Monte Carlo simulation helpers for primary care funding models.

The module uses JAX/XLA when available. The public dashboard and ordinary test
suite must still import and run without JAX installed, so all public APIs have a
deterministic NumPy fallback with the same shapes and summary semantics.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import pyarrow as pa

try:  # pragma: no cover - exercised only in JAX-enabled environments
    import jax
    import jax.numpy as jnp
    import jax.random as jrandom

    HAS_JAX = True
except ModuleNotFoundError:  # pragma: no cover - current CI/runtime fallback
    jax = None
    jnp = None
    jrandom = None
    HAS_JAX = False

from .data_layer import MONTHLY_METRICS_ARROW_SCHEMA
from .schemas import MonthlyMetrics, ScenarioParams, SimulationConfig, SimulationResult

SimState = Any
SweepParams = Any


def _scenario_base_params(scenario: ScenarioParams) -> np.ndarray:
    cap_rate = scenario.capitation_rate or 80.0
    ffs_gp = 45.0
    ffs_nurse = 25.0
    if scenario.ffs_fee_schedule:
        ffs_gp = scenario.ffs_fee_schedule.get("gp_visit", 45.0)
        ffs_nurse = scenario.ffs_fee_schedule.get("nurse_visit", 25.0)
    return np.asarray([cap_rate, ffs_gp, ffs_nurse, 0.05, 0.03, 0.5, 2.0], dtype=float)


def _numpy_step(state: np.ndarray, params: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    cap_rate, ffs_gp, ffs_nurse, demand_elast, supply_elast, equity_w, _wait_penalty = params
    patients = float(state[0])
    providers = float(state[1])

    demand = max(0.0, patients * 0.15 * (1.0 + demand_elast * rng.normal()))
    supply = max(0.0, providers * 150.0 * (1.0 + supply_elast * rng.normal()))
    visits = min(demand, supply)
    gp_visits = visits * 0.7
    nurse_visits = visits * 0.3

    avg_wait = float(np.clip(demand / (supply + 1e-8) * 5.0, 0.0, 60.0))
    unmet = max(0.0, demand - supply)
    cap_payments = patients * cap_rate * (1.0 + 0.02 * equity_w)
    ffs_payments = gp_visits * ffs_gp + nurse_visits * ffs_nurse
    total_funding = cap_payments + ffs_payments

    net_funding = total_funding - providers * 5000.0
    exit_rate = 0.0
    if net_funding < 0:
        exit_rate = float(np.clip(abs(net_funding) / (total_funding + 1e-8) * 0.05, 0.0, 0.2))
    providers_next = max(1.0, providers * (1.0 - exit_rate))

    return np.asarray(
        [
            int(patients),
            int(providers_next),
            int(round(visits)),
            cap_payments,
            ffs_payments,
            total_funding,
            avg_wait,
            int(unmet),
        ],
        dtype=float,
    )


def _numpy_trajectory(params: np.ndarray, n_steps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    state = np.asarray([10000.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    rows = []
    for _ in range(n_steps):
        state = _numpy_step(state, params, rng)
        rows.append(state)
    return np.vstack(rows)


if HAS_JAX:  # pragma: no cover - depends on optional JAX runtime

    @jax.jit
    def _jax_step(state: Any, params: Any, key: Any) -> Any:
        cap_rate = params[0]
        ffs_gp = params[1]
        ffs_nurse = params[2]
        demand_elast = params[3]
        supply_elast = params[4]
        equity_w = params[5]
        patients = state[0]
        providers = state[1]

        key_demand, key_supply = jrandom.split(key)
        demand = jnp.maximum(0.0, patients * 0.15 * (1.0 + demand_elast * jrandom.normal(key_demand)))
        supply = jnp.maximum(0.0, providers * 150.0 * (1.0 + supply_elast * jrandom.normal(key_supply)))
        visits = jnp.minimum(demand, supply)

        avg_wait = jnp.clip(demand / (supply + 1e-8) * 5.0, 0.0, 60.0)
        unmet = jnp.maximum(0.0, demand - supply).astype(jnp.int32)
        cap_payments = patients * cap_rate * (1.0 + 0.02 * equity_w)
        ffs_payments = visits * 0.7 * ffs_gp + visits * 0.3 * ffs_nurse
        total_funding = cap_payments + ffs_payments
        net_funding = total_funding - providers * 5000.0
        exit_rate = jnp.where(
            net_funding < 0,
            jnp.clip(jnp.abs(net_funding) / (total_funding + 1e-8) * 0.05, 0.0, 0.2),
            0.0,
        )
        providers_next = jnp.maximum(1.0, providers * (1.0 - exit_rate)).astype(jnp.int32)

        return jnp.array(
            [
                patients.astype(jnp.int32),
                providers_next,
                jnp.round(visits).astype(jnp.int32),
                cap_payments,
                ffs_payments,
                total_funding,
                avg_wait,
                unmet,
            ]
        )

    @jax.jit(static_argnums=(1,))
    def _run_trajectory(params: Any, n_steps: int, key: Any) -> Any:
        keys = jrandom.split(key, num=n_steps)

        def scan_fn(carry: Any, step_key: Any) -> tuple[Any, Any]:
            state = _jax_step(carry, params, step_key)
            return state, state

        init_state = jnp.array([10000.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=jnp.float32)
        _, trajectory = jax.lax.scan(scan_fn, init_state, keys)
        return trajectory

    @jax.jit(static_argnums=(2,))
    def _batch_trajectories(params_batch: Any, key_batch: Any, n_steps: int) -> Any:
        return jax.vmap(_run_trajectory, in_axes=(0, None, 0))(params_batch, n_steps, key_batch)

else:
    _run_trajectory = None
    _batch_trajectories = None


@dataclass(frozen=True)
class MCSweepResult:
    """Container for Monte Carlo sweep results."""

    trajectories: Any
    params_used: Any
    seeds_used: Any
    wall_time_s: float
    engine: str = "numpy"

    def to_arrow(self) -> pa.Table:
        """Flatten trajectories into an Arrow table."""
        trajectories = np.asarray(self.trajectories)
        batch_size, n_steps, _ = trajectories.shape
        rows: list[dict[str, Any]] = []
        for batch_idx in range(batch_size):
            for month in range(n_steps):
                rows.append(
                    {
                        "month": month,
                        "total_patients": int(trajectories[batch_idx, month, 0]),
                        "total_providers": int(trajectories[batch_idx, month, 1]),
                        "total_visits": int(trajectories[batch_idx, month, 2]),
                        "total_capitation_payments": float(trajectories[batch_idx, month, 3]),
                        "total_ffs_payments": float(trajectories[batch_idx, month, 4]),
                        "total_funding": float(trajectories[batch_idx, month, 5]),
                        "avg_wait_time_days": float(trajectories[batch_idx, month, 6]),
                        "unmet_demand": int(trajectories[batch_idx, month, 7]),
                    }
                )

        arrays = [pa.array([row[field.name] for row in rows], type=field.type) for field in MONTHLY_METRICS_ARROW_SCHEMA]
        return pa.Table.from_arrays(arrays, schema=MONTHLY_METRICS_ARROW_SCHEMA)

    def to_monthly_metrics_list(self, batch_idx: int = 0) -> list[MonthlyMetrics]:
        """Convert one trajectory to MonthlyMetrics records."""
        trajectories = np.asarray(self.trajectories)
        n_steps = trajectories.shape[1]
        return [
            MonthlyMetrics(
                month=month,
                total_patients=int(trajectories[batch_idx, month, 0]),
                total_providers=int(trajectories[batch_idx, month, 1]),
                total_visits=int(trajectories[batch_idx, month, 2]),
                total_capitation_payments=float(trajectories[batch_idx, month, 3]),
                total_ffs_payments=float(trajectories[batch_idx, month, 4]),
                total_funding=float(trajectories[batch_idx, month, 5]),
                avg_wait_time_days=float(trajectories[batch_idx, month, 6]),
                unmet_demand=int(trajectories[batch_idx, month, 7]),
            )
            for month in range(n_steps)
        ]


@dataclass(frozen=True)
class MCConfig:
    """Configuration for the Streamlit rolling Monte Carlo visualisation."""

    num_iterations: int = 500
    num_batches: int = 10
    perturbation_std: float = 0.08
    seed: int = 42
    target_metrics: tuple[str, ...] = (
        "access_rate",
        "hospital_pressure_index",
        "equity_gap_index",
        "fiscal_risk_index",
        "unmet_need_index",
        "provider_utilisation",
    )


@dataclass(frozen=True)
class RollingMCResult:
    """Page-facing Monte Carlo result with metric arrays and rolling CIs."""

    metrics: dict[str, np.ndarray]

    def rolling_ci(
        self,
        metric: str,
        window: int = 50,
        ci_percentiles: tuple[float, float] = (5.0, 95.0),
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        values = np.asarray(self.metrics.get(metric, np.array([])), dtype=float)
        if values.size == 0:
            empty = np.array([])
            return empty, empty, empty

        window = max(1, min(window, values.size))
        means: list[float] = []
        lower: list[float] = []
        upper: list[float] = []
        p_low, p_high = ci_percentiles
        for end in range(window, values.size + 1):
            chunk = values[end - window : end]
            means.append(float(np.mean(chunk)))
            lower.append(float(np.percentile(chunk, p_low)))
            upper.append(float(np.percentile(chunk, p_high)))
        return np.asarray(means), np.asarray(lower), np.asarray(upper)


def run_monte_carlo(config: MCConfig, progress_callback: Any | None = None) -> RollingMCResult:
    """Run a batched stochastic sweep for the Streamlit rolling histogram page."""
    total = max(1, int(config.num_iterations))
    batches = max(1, min(int(config.num_batches), total))
    base_batch = total // batches
    remainder = total % batches
    rng = np.random.default_rng(int(config.seed))
    collected: dict[str, list[float]] = {metric: [] for metric in config.target_metrics}

    for batch_idx in range(batches):
        batch_size = base_batch + (1 if batch_idx < remainder else 0)
        shocks = rng.normal(size=(batch_size, 6))
        width = float(config.perturbation_std)
        batch_metrics = {
            "access_rate": np.clip(0.78 + width * shocks[:, 0], 0.0, 1.0),
            "hospital_pressure_index": np.clip(0.34 + width * shocks[:, 1], 0.0, 1.0),
            "equity_gap_index": np.clip(0.22 + width * shocks[:, 2], 0.0, 1.0),
            "fiscal_risk_index": np.clip(0.41 + width * shocks[:, 3], 0.0, 1.0),
            "unmet_need_index": np.clip(0.18 + width * shocks[:, 4], 0.0, 1.0),
            "provider_utilisation": np.clip(0.71 + width * shocks[:, 5], 0.0, 1.0),
        }

        visible_batch: dict[str, float] = {}
        for metric in config.target_metrics:
            values = np.asarray(batch_metrics.get(metric, np.array([])), dtype=float)
            collected[metric].extend(values.tolist())
            if values.size:
                visible_batch[metric] = float(np.mean(values))
        if progress_callback is not None:
            progress_callback(batch_idx, visible_batch)

    return RollingMCResult(metrics={metric: np.asarray(values, dtype=float) for metric, values in collected.items()})


def generate_sweep_params(
    config: SimulationConfig,
    scenario: ScenarioParams,
    batch_size: int,
    key: Any | None = None,
) -> tuple[Any, Any]:
    """Generate parameter batches and per-run keys/seeds for MC sweeps."""
    base_params = _scenario_base_params(scenario)
    batch_size = max(1, int(batch_size))

    if HAS_JAX and key is not None:  # pragma: no cover - optional JAX lane
        base = jnp.asarray(base_params)
        subkeys = jrandom.split(key, batch_size + 1)
        key_batch = jnp.asarray(subkeys[:batch_size])
        noise = jrandom.normal(subkeys[batch_size], shape=(batch_size, 7)) * 0.02
        noise = noise.at[:, 0:3].multiply(base[0:3])
        return jnp.clip(base[None, :] + noise, 0.0, None), key_batch

    rng = np.random.default_rng(config.seed)
    noise = rng.normal(size=(batch_size, 7)) * 0.02
    noise[:, 0:3] *= base_params[0:3]
    params_batch = np.clip(base_params[None, :] + noise, 0.0, None)
    return params_batch, np.arange(config.seed, config.seed + batch_size, dtype=np.uint32)


def run_mc_sweep(
    config: SimulationConfig,
    scenario: ScenarioParams,
    batch_size: int = 64,
    seed: int | None = None,
) -> MCSweepResult:
    """Run a Monte Carlo sweep over parallel simulation trajectories."""
    seed = int(seed if seed is not None else config.seed)
    n_steps = config.time_horizon_months
    batch_size = max(1, int(batch_size))

    if HAS_JAX:  # pragma: no cover - optional JAX lane
        key = jrandom.PRNGKey(seed)
        params_batch, key_batch = generate_sweep_params(config, scenario, batch_size, key)
        start = time.perf_counter()
        trajectories = _batch_trajectories(params_batch, key_batch, n_steps)
        wall_time_s = time.perf_counter() - start
        return MCSweepResult(
            trajectories=trajectories,
            params_used=params_batch,
            seeds_used=np.arange(seed, seed + batch_size),
            wall_time_s=wall_time_s,
            engine="jax",
        )

    params_batch, seeds = generate_sweep_params(config, scenario, batch_size)
    start = time.perf_counter()
    trajectories = np.stack([_numpy_trajectory(params_batch[idx], n_steps, int(seeds[idx])) for idx in range(batch_size)])
    wall_time_s = time.perf_counter() - start
    return MCSweepResult(
        trajectories=trajectories,
        params_used=params_batch,
        seeds_used=seeds,
        wall_time_s=wall_time_s,
        engine="numpy",
    )


def run_deterministic(config: SimulationConfig, scenario: ScenarioParams) -> SimulationResult:
    """Run a single deterministic simulation trajectory."""
    sweep = run_mc_sweep(config, scenario, batch_size=1, seed=config.seed)
    metrics = sweep.to_monthly_metrics_list(batch_idx=0)
    summary = {
        "total_visits_sum": sum(metric.total_visits for metric in metrics),
        "total_funding_sum": sum(metric.total_funding for metric in metrics),
        "final_patients": metrics[-1].total_patients,
        "final_providers": metrics[-1].total_providers,
        "mean_wait_days": float(np.mean([metric.avg_wait_time_days or 0.0 for metric in metrics])),
        "total_unmet_demand": sum(metric.unmet_demand for metric in metrics),
        "engine": sweep.engine,
    }
    return SimulationResult(
        scenario_name=scenario.name,
        monthly_metrics=metrics,
        summary_metrics=summary,
        metadata={
            "seed": config.seed,
            "num_patients": config.num_patients,
            "num_providers": config.num_providers,
            "time_horizon_months": config.time_horizon_months,
            "funding_model": scenario.funding_model.value,
        },
    )


def compute_summary_stats(
    result: MCSweepResult,
    ci_percentiles: tuple[float, float] = (5.0, 95.0),
) -> dict[str, Any]:
    """Compute summary stats across MC batch trajectories."""
    trajectories = np.asarray(result.trajectories)
    batch_size, n_steps, _ = trajectories.shape
    total_funding = trajectories[:, :, 5]
    total_visits = trajectories[:, :, 2]
    total_unmet = trajectories[:, :, 7]
    avg_wait = trajectories[:, :, 6]
    final_patients = trajectories[:, -1, 0]
    final_providers = trajectories[:, -1, 1]
    p_low, p_high = ci_percentiles
    return {
        "batch_size": batch_size,
        "n_steps": n_steps,
        "total_funding_mean": float(np.mean(total_funding)),
        "total_funding_median": float(np.median(total_funding)),
        "total_funding_p5": float(np.percentile(total_funding, p_low)),
        "total_funding_p95": float(np.percentile(total_funding, p_high)),
        "total_visits_mean": float(np.mean(total_visits)),
        "total_visits_median": float(np.median(total_visits)),
        "total_unmet_mean": float(np.mean(total_unmet)),
        "total_unmet_median": float(np.median(total_unmet)),
        "avg_wait_mean": float(np.mean(avg_wait)),
        "avg_wait_p5": float(np.percentile(avg_wait, p_low)),
        "avg_wait_p95": float(np.percentile(avg_wait, p_high)),
        "final_patients_mean": float(np.mean(final_patients)),
        "final_patients_std": float(np.std(final_patients)),
        "final_providers_mean": float(np.mean(final_providers)),
        "final_providers_std": float(np.std(final_providers)),
        "wall_time_s": result.wall_time_s,
        "engine": result.engine,
    }


__all__ = [
    "HAS_JAX",
    "MCConfig",
    "MCSweepResult",
    "RollingMCResult",
    "SimState",
    "SweepParams",
    "compute_summary_stats",
    "generate_sweep_params",
    "run_deterministic",
    "run_mc_sweep",
    "run_monte_carlo",
]
