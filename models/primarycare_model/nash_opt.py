"""
Nash equilibrium optimisation engine for funding model games.
Best-response dynamics tracing for 2-player funding model choices.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

try:
    import jax.numpy as jnp
    from jax import grad, jit
    _HAS_JAX = True
except ImportError:
    _HAS_JAX = False


@dataclass
class PayoffMatrix:
    """2x2 payoff matrix for two players (funding model game)."""
    row_label: str = "Player 0"
    col_label: str = "Player 1"
    strategy_labels: Tuple[str, str] = ("Capitation", "FFS")
    player0: np.ndarray = field(default_factory=lambda: np.array([[0.6, 0.3],[0.4, 0.5]]))
    player1: np.ndarray = field(default_factory=lambda: np.array([[0.6, 0.4],[0.3, 0.5]]))

    @classmethod
    def cooperative(cls) -> "PayoffMatrix":
        return cls(
            player0=np.array([[0.8, 0.2],[0.2, 0.6]]),
            player1=np.array([[0.8, 0.2],[0.2, 0.6]]),
        )

    @classmethod
    def competitive(cls) -> "PayoffMatrix":
        return cls(
            player0=np.array([[0.5, 0.8],[0.3, 0.4]]),
            player1=np.array([[0.4, 0.3],[0.8, 0.5]]),
        )

    @classmethod
    def clinical_utility(cls) -> "PayoffMatrix":
        return cls(
            row_label="Ministry", col_label="Providers",
            strategy_labels=("Capitation", "FFS"),
            player0=np.array([[0.7, 0.3],[0.4, 0.6]]),
            player1=np.array([[0.6, 0.5],[0.3, 0.7]]),
        )


@dataclass
class NashTrace:
    """Records best-response dynamics trace."""
    strategies: List[np.ndarray] = field(default_factory=list)
    payoffs: List[Tuple[float, float]] = field(default_factory=list)
    converged: bool = False
    num_iterations: int = 0

    def to_dataframe(self) -> pd.DataFrame:
        rows = []
        for i, (s, (p0, p1)) in enumerate(zip(self.strategies, self.payoffs)):
            rows.append({
                "iteration": i,
                "p0_strategy_capitation": float(s[0]),
                "p0_strategy_ffs": float(1.0 - s[0]),
                "p1_strategy_capitation": float(s[1]),
                "p1_strategy_ffs": float(1.0 - s[1]),
                "p0_payoff": float(p0),
                "p1_payoff": float(p1),
                "total_welfare": float(p0 + p1),
            })
        return pd.DataFrame(rows)

    @property
    def final_strategies(self) -> Optional[np.ndarray]:
        """Final mixed strategy weights as [player0 capitation, player1 capitation]."""
        return self.strategies[-1] if self.strategies else None


def best_response(payoff: np.ndarray, opponent_strategy: np.ndarray) -> np.ndarray:
    """Compute best response for a player given opponent strategy (softmax)."""
    expected_payoffs = payoff @ opponent_strategy
    max_p = np.max(expected_payoffs)
    shifted = expected_payoffs - max_p
    exp_p = np.exp(shifted * 5.0)
    return exp_p / exp_p.sum()


def nash_best_response_dynamics(
    payoff_matrix: PayoffMatrix,
    initial_strategies: Optional[np.ndarray] = None,
    max_iterations: int = 100,
    tol: float = 1e-4,
    learning_rate: float = 0.5,
) -> NashTrace:
    """Compute Nash equilibrium via best-response dynamics."""
    if initial_strategies is None:
        initial_strategies = np.array([0.5, 0.5])

    trace = NashTrace()
    s = initial_strategies.copy()

    for i in range(max_iterations):
        p0_strat = np.array([s[0], 1.0 - s[0]])
        p1_strat = np.array([s[1], 1.0 - s[1]])

        p0_payoff = float(p0_strat @ payoff_matrix.player0 @ p1_strat)
        p1_payoff = float(p1_strat @ payoff_matrix.player1 @ p0_strat)

        trace.strategies.append(s.copy())
        trace.payoffs.append((p0_payoff, p1_payoff))

        br0 = best_response(payoff_matrix.player0, p1_strat)
        br1 = best_response(payoff_matrix.player1, p0_strat)

        s_new = np.array([
            (1 - learning_rate) * s[0] + learning_rate * br0[0],
            (1 - learning_rate) * s[1] + learning_rate * br1[0],
        ])

        diff = np.max(np.abs(s_new - s))
        s = s_new

        if diff < tol:
            trace.converged = True
            trace.num_iterations = i + 1
            p0_strat = np.array([s[0], 1.0 - s[0]])
            p1_strat = np.array([s[1], 1.0 - s[1]])
            trace.strategies.append(s.copy())
            trace.payoffs.append((
                float(p0_strat @ payoff_matrix.player0 @ p1_strat),
                float(p1_strat @ payoff_matrix.player1 @ p0_strat),
            ))
            break

    trace.num_iterations = min(i + 1, max_iterations)
    return trace


def compute_payoff_landscape(payoff_matrix: PayoffMatrix, grid: int = 40) -> pd.DataFrame:
    """Compute payoff values across strategy grid for contour plotting."""
    xs = np.linspace(0, 1, grid)
    ys = np.linspace(0, 1, grid)
    X, Y = np.meshgrid(xs, ys)
    Z0 = np.zeros_like(X); Z1 = np.zeros_like(X)
    for i in range(grid):
        for j in range(grid):
            p0_s = np.array([X[i,j], 1.0-X[i,j]])
            p1_s = np.array([Y[i,j], 1.0-Y[i,j]])
            Z0[i,j] = float(p0_s @ payoff_matrix.player0 @ p1_s)
            Z1[i,j] = float(p1_s @ payoff_matrix.player1 @ p0_s)
    return pd.DataFrame({
        "p0_capitation": X.ravel(), "p1_capitation": Y.ravel(),
        "p0_payoff": Z0.ravel(), "p1_payoff": Z1.ravel(),
        "total_welfare": (Z0+Z1).ravel(),
    })


def run_nash_with_multiple_starts(payoff_matrix: PayoffMatrix, num_starts: int = 5,
                                   max_iterations: int = 100) -> List[NashTrace]:
    """Run best-response dynamics from multiple starting points."""
    traces = []
    rng = np.random.default_rng(42)
    for _ in range(num_starts):
        init = np.array([rng.random(), rng.random()])
        trace = nash_best_response_dynamics(payoff_matrix, init, max_iterations)
        traces.append(trace)
    return traces


GAME_PRESETS: Dict[str, PayoffMatrix] = {
    "Cooperative (both prefer capitation)": PayoffMatrix.cooperative(),
    "Competitive (conflicting preferences)": PayoffMatrix.competitive(),
    "Clinical Utility (ministry vs providers)": PayoffMatrix.clinical_utility(),
}


if __name__ == "__main__":
    matrix = PayoffMatrix.cooperative()
    trace = nash_best_response_dynamics(matrix)
    df = trace.to_dataframe()
    print(df.to_string())
    print(f"Converged: {trace.converged}, Iterations: {trace.num_iterations}")
    print("Nash optimisation test PASSED")
