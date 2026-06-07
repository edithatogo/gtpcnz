"""Protocols, base input/output types and uncertainty summaries for pure calculation engines."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from pydantic import Field

from models.primarycare_model.contracts.parameters import StrictContract

InputT = TypeVar("InputT", contravariant=True)
OutputT = TypeVar("OutputT", covariant=True)


@runtime_checkable
class EngineProtocol(Protocol[InputT, OutputT]):
    """A pure calculation engine boundary."""

    engine_id: str

    def run(self, inputs: InputT) -> OutputT:
        """Run a deterministic calculation for the supplied validated inputs."""
        raise NotImplementedError


class EngineInput(StrictContract):
    """Base input contract accepted by all calculation engines.

    Subclass to add engine-specific fields.
    """

    scenario_id: str = Field(min_length=1)
    parameters: StrictContract | None = None
    seed: int | None = None
    claim_boundary: str = Field(min_length=1)


class EngineOutput(StrictContract):
    """Base output contract returned by all calculation engines.

    Subclass to add engine-specific result fields.
    """

    manifest: ResultManifest


class UncertaintySummary(StrictContract):
    """Per-metric stochastic uncertainty statistics."""

    metric: str = Field(min_length=1)
    mean: float
    std: float = 0.0
    p05: float
    p50: float
    p95: float
    draws: int = 0


# late import to avoid circularity
from models.primarycare_model.contracts.results import ResultManifest  # noqa: E402
