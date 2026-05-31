"""Graph pathway helpers for referral bottleneck exploration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

try:  # pragma: no cover - optional accelerator dependency
    import jax
    import jax.numpy as jnp
    HAS_JAX = True
except ModuleNotFoundError:  # pragma: no cover - lean runtime fallback
    jax = None
    jnp = np
    HAS_JAX = False

try:
    import jraph
except ImportError:  # pragma: no cover - optional dependency
    jraph = None

from .schemas import ScenarioParams, SimulationConfig

RNGKey = Any


@dataclass(frozen=True)
class ReferralGraph:
    """Bipartite referral graph between practices and patient cohorts."""

    n_practices: int
    n_cohorts: int
    senders: jnp.ndarray
    receivers: jnp.ndarray
    edge_weights: jnp.ndarray
    practice_features: jnp.ndarray
    cohort_features: jnp.ndarray
    node_targets: jnp.ndarray | None = None

    @property
    def n_nodes(self) -> int:
        return self.n_practices + self.n_cohorts

    @property
    def n_edges(self) -> int:
        return int(self.senders.shape[0])

    def to_jraph(self) -> Any:
        """Convert to jraph.GraphsTuple when jraph is installed."""
        if jraph is None:
            raise ImportError("Install jraph to convert ReferralGraph to GraphsTuple.")
        return jraph.GraphsTuple(
            nodes=jnp.concatenate([self.practice_features, self.cohort_features], axis=0),
            edges=self.edge_weights[:, None],
            senders=self.senders,
            receivers=self.receivers,
            globals=jnp.array([jnp.mean(self.edge_weights)]),
            n_node=jnp.array([self.n_nodes], dtype=jnp.int32),
            n_edge=jnp.array([self.n_edges], dtype=jnp.int32),
        )

    @classmethod
    def from_simulation(
        cls,
        config: SimulationConfig,
        scenario: ScenarioParams,
        rng_key: RNGKey,
        n_practices: int = 50,
        n_cohorts: int = 20,
        edge_density: float = 0.15,
    ) -> ReferralGraph:
        """Construct a synthetic referral graph from simulation settings."""
        if not HAS_JAX:
            raise ModuleNotFoundError(
                "Install jax to construct a synthetic referral graph from simulation settings."
            )
        del config
        key_practice, key_cohort, key_edges, key_weights = jax.random.split(rng_key, 4)
        practice_features = jax.random.uniform(key_practice, (n_practices, 5))
        cohort_features = jax.random.uniform(key_cohort, (n_cohorts, 5))
        n_edges = max(1, int(n_practices * n_cohorts * edge_density))
        senders = jax.random.randint(key_edges, (n_edges,), 0, n_practices)
        receivers = n_practices + jax.random.randint(key_weights, (n_edges,), 0, n_cohorts)
        capitation_rate = scenario.capitation_rate or 80.0
        edge_weights = (capitation_rate / 100.0) * jax.random.uniform(
            key_weights,
            (n_edges,),
            minval=0.3,
            maxval=1.0,
        )
        targets = (practice_features[:, 0] < 0.4).astype(jnp.float32)
        return cls(
            n_practices=n_practices,
            n_cohorts=n_cohorts,
            senders=senders.astype(jnp.int32),
            receivers=receivers.astype(jnp.int32),
            edge_weights=edge_weights.astype(jnp.float32),
            practice_features=practice_features.astype(jnp.float32),
            cohort_features=cohort_features.astype(jnp.float32),
            node_targets=targets,
        )


def referral_pressure_scores(graph: ReferralGraph) -> np.ndarray:
    """Score practices by weighted outgoing referral pressure and capacity proxy."""
    scores = np.zeros(graph.n_practices, dtype=np.float64)
    for sender, weight in zip(np.asarray(graph.senders), np.asarray(graph.edge_weights)):
        if 0 <= sender < graph.n_practices:
            scores[int(sender)] += float(weight)
    if scores.max() > 0:
        scores = scores / scores.max()
    capacity_proxy = np.asarray(graph.practice_features[:, 0], dtype=np.float64)
    return np.clip(0.7 * scores + 0.3 * (1.0 - capacity_proxy), 0.0, 1.0)


__all__ = [
    "ReferralGraph",
    "referral_pressure_scores",
]
