"""Bayesian-style optimisation helpers for policy parameter search.

This lightweight implementation avoids a hard JAX dependency so the public
repository remains importable in the default Streamlit/test environment.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass
class GPState:
    X: np.ndarray
    y: np.ndarray
    length_scale: float = 1.0
    signal_variance: float = 1.0
    noise_variance: float = 0.01


def _rbf_kernel(x1: np.ndarray, x2: np.ndarray, length_scale: float, signal_var: float) -> np.ndarray:
    sq_dist = np.sum((x1[:, None, :] - x2[None, :, :]) ** 2, axis=-1)
    return signal_var * np.exp(-0.5 * sq_dist / (length_scale**2))


def gp_predict(gp: GPState, x_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x_test = np.asarray(x_test, dtype=float)
    K = _rbf_kernel(gp.X, gp.X, gp.length_scale, gp.signal_variance)
    K = K + gp.noise_variance * np.eye(gp.X.shape[0])
    K_s = _rbf_kernel(gp.X, x_test, gp.length_scale, gp.signal_variance)
    K_ss = _rbf_kernel(x_test, x_test, gp.length_scale, gp.signal_variance) + gp.noise_variance
    K_inv = np.linalg.pinv(K)
    mu = K_s.T @ K_inv @ gp.y
    sigma = K_ss - K_s.T @ K_inv @ K_s
    return mu, np.sqrt(np.clip(np.diag(sigma), 0.0, None))


def _normal_pdf(z: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * z**2) / np.sqrt(2.0 * np.pi)


def _normal_cdf(z: np.ndarray) -> np.ndarray:
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / np.sqrt(2.0)))


def expected_improvement(mu: np.ndarray, sigma: np.ndarray, y_best: float, xi: float = 0.01) -> np.ndarray:
    """Expected improvement for minimisation objectives."""
    improvement = y_best - mu - xi
    z = improvement / (sigma + 1e-10)
    return np.where(sigma > 0.0, improvement * _normal_cdf(z) + sigma * _normal_pdf(z), 0.0)


def probability_of_improvement(mu: np.ndarray, sigma: np.ndarray, y_best: float) -> np.ndarray:
    """Probability of improvement for minimisation objectives."""
    return _normal_cdf((y_best - mu) / (sigma + 1e-10))


def lower_confidence_bound(mu: np.ndarray, sigma: np.ndarray, kappa: float = 2.0) -> np.ndarray:
    """Lower confidence bound acquisition for minimisation objectives."""
    return -(mu - kappa * sigma)


def bayesian_optimization_step(
    gp: GPState,
    bounds: np.ndarray,
    seed: int = 42,
    n_candidates: int = 1000,
    acq: str = "ei",
) -> tuple[np.ndarray, dict[str, float]]:
    bounds = np.asarray(bounds, dtype=float)
    rng = np.random.default_rng(seed)
    candidates = rng.uniform(size=(n_candidates, bounds.shape[0]))
    candidates = bounds[:, 0] + candidates * (bounds[:, 1] - bounds[:, 0])
    mu, sigma = gp_predict(gp, candidates)
    y_best = float(np.min(gp.y))
    if acq == "ei":
        acq_vals = expected_improvement(mu, sigma, y_best)
    elif acq == "pi":
        acq_vals = probability_of_improvement(mu, sigma, y_best)
    elif acq == "lcb":
        acq_vals = lower_confidence_bound(mu, sigma)
    else:
        raise ValueError(f"Unknown acquisition function: {acq}")
    best_idx = int(np.argmax(acq_vals))
    return candidates[best_idx], {"acq_max": float(acq_vals[best_idx]), "y_best": y_best}


def run_bayesian_optimization(
    objective_fn: Callable[[np.ndarray], float],
    bounds: np.ndarray,
    n_init: int = 5,
    n_iter: int = 20,
    seed: int = 42,
    acq: str = "ei",
) -> dict[str, object]:
    bounds = np.asarray(bounds, dtype=float)
    rng = np.random.default_rng(seed)
    x_init = rng.uniform(size=(n_init, bounds.shape[0]))
    x_init = bounds[:, 0] + x_init * (bounds[:, 1] - bounds[:, 0])
    y_init = np.asarray([objective_fn(row) for row in x_init], dtype=float)

    x_all = [row for row in x_init]
    y_all = [float(value) for value in y_init]
    gp = GPState(X=x_init, y=y_init)
    for iteration in range(n_iter):
        x_next, _info = bayesian_optimization_step(gp, bounds, seed + iteration + 1, acq=acq)
        y_next = float(objective_fn(x_next))
        x_all.append(x_next)
        y_all.append(y_next)
        gp = GPState(
            X=np.asarray(x_all),
            y=np.asarray(y_all),
            length_scale=gp.length_scale,
            signal_variance=gp.signal_variance,
            noise_variance=gp.noise_variance,
        )

    best_idx = int(np.argmin(np.asarray(y_all)))
    return {
        "best_params": np.asarray(x_all[best_idx]),
        "best_value": float(y_all[best_idx]),
        "all_params": np.asarray(x_all),
        "all_values": np.asarray(y_all),
        "n_iterations": n_iter,
    }


__all__ = [
    "GPState",
    "bayesian_optimization_step",
    "expected_improvement",
    "gp_predict",
    "lower_confidence_bound",
    "probability_of_improvement",
    "run_bayesian_optimization",
]
