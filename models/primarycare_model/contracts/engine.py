"""Protocols for pure calculation engines."""

from __future__ import annotations

from typing import Protocol, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class EngineProtocol(Protocol[InputT, OutputT]):
    """A pure calculation engine boundary."""

    engine_id: str

    def run(self, inputs: InputT) -> OutputT:
        """Run a deterministic calculation for the supplied validated inputs."""
