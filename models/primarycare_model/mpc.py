"""Model predictive control helpers for funding adjustment paths."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class MPCConfig:
    horizon: int = 12
    dt: float = 1.0
    funding_weight: float = 1.0
    wait_time_weight: float = 10.0
    unmet_demand_weight: float = 5.0
    smoothness_weight: float = 0.1
    cap_rate_min: float = 40.0
    cap_rate_max: float = 160.0
    ffs_gp_min: float = 20.0
    ffs_gp_max: float = 90.0


DEFAULT_MPC_CONFIG = MPCConfig()


def _simulate_with_policy(state: np.ndarray, policy_params: np.ndarray, n_steps: int, key: Any = None) -> np.ndarray:
    """Simulate a policy path using the NumPy Monte Carlo step fallback."""
    from .jax_mc import _numpy_step

    params = np.asarray(policy_params, dtype=float)
    if params.ndim == 1:
        params = np.broadcast_to(params, (n_steps, params.shape[0]))
    rng_seed = 42 if key is None else int(np.asarray(key).ravel()[0])
    rng = np.random.default_rng(rng_seed)
    current = np.asarray(state, dtype=float)
    rows = []
    for step_params in params[:n_steps]:
        current = _numpy_step(current, step_params, rng)
        rows.append(current)
    return np.vstack(rows)


def compute_mpc_cost(trajectory: np.ndarray, config: MPCConfig = DEFAULT_MPC_CONFIG) -> float:
    """Compute a scalar MPC objective from a trajectory matrix."""
    values = np.asarray(trajectory, dtype=float)
    wait_times = values[:, 6]
    unmet = values[:, 7]
    funding = values[:, 5]
    return float(
        config.funding_weight * np.mean(funding)
        + config.wait_time_weight * np.mean(wait_times)
        + config.unmet_demand_weight * np.mean(unmet)
    )


def compute_policy_gradient(
    state: np.ndarray,
    base_params: np.ndarray,
    n_steps: int,
    key: Any = None,
    config: MPCConfig = DEFAULT_MPC_CONFIG,
    epsilon: float = 1e-3,
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate policy gradients with deterministic finite differences."""
    params = np.asarray(base_params, dtype=float)
    gradient = np.zeros_like(params)
    for idx in range(params.size):
        delta = np.zeros_like(params)
        delta[idx] = epsilon
        cost_hi = compute_mpc_cost(_simulate_with_policy(state, params + delta, n_steps, key), config)
        cost_lo = compute_mpc_cost(_simulate_with_policy(state, params - delta, n_steps, key), config)
        gradient[idx] = (cost_hi - cost_lo) / (2.0 * epsilon)
    return gradient, gradient.copy()


def optimize_policy(
    state: np.ndarray,
    base_params: np.ndarray,
    n_steps: int,
    key: Any = None,
    config: MPCConfig = DEFAULT_MPC_CONFIG,
    n_iterations: int = 50,
    lr: float = 0.01,
) -> tuple[np.ndarray, list[float]]:
    """Optimise policy parameters with clipped finite-difference descent."""
    params = np.asarray(base_params, dtype=float).copy()
    costs: list[float] = []
    lower = np.asarray([config.cap_rate_min, config.ffs_gp_min, 10.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    upper = np.asarray([config.cap_rate_max, config.ffs_gp_max, 50.0, 1.0, 1.0, 1.0, 10.0], dtype=float)
    for iteration in range(max(1, int(n_iterations))):
        gradient, _ = compute_policy_gradient(state, params, n_steps, key, config)
        params = np.clip(params - lr * gradient, lower, upper)
        if iteration % 10 == 0 or iteration == n_iterations - 1:
            costs.append(compute_mpc_cost(_simulate_with_policy(state, params, n_steps, key), config))
    return params, costs


def optimize_policy_jaxopt(
    state: np.ndarray,
    base_params: np.ndarray,
    n_steps: int,
    key: Any = None,
    config: MPCConfig = DEFAULT_MPC_CONFIG,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Compatibility wrapper; uses the local optimiser when jaxopt is absent."""
    params, costs = optimize_policy(state, base_params, n_steps, key, config, n_iterations=25)
    return params, {"state": "numpy-fallback", "costs": costs}


__all__ = [
    "MPCConfig",
    "DEFAULT_MPC_CONFIG",
    "compute_mpc_cost",
    "compute_policy_gradient",
    "optimize_policy",
    "optimize_policy_jaxopt",
]
