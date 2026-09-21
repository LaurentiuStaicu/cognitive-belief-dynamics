from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StaticDirectedNetwork:
    """Small explicit directed network for structural CBD experiments.

    An edge means only that a synthetic transmission policy may route from
    sender to recipient. It does not imply friendship, attention, trust,
    endorsement, or an empirically measured platform relation.
    """

    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if len(set(self.nodes)) != len(self.nodes):
            raise ValueError("network nodes must be unique")
        if len(set(self.edges)) != len(self.edges):
            raise ValueError("network edges must be unique")
        known = set(self.nodes)
        for sender, recipient in self.edges:
            if sender not in known or recipient not in known:
                raise ValueError("every network edge endpoint must be a declared node")

    def eligible_recipients(self, sender_id: str) -> tuple[str, ...]:
        """Return recipients in declared edge order."""
        return tuple(recipient for sender, recipient in self.edges if sender == sender_id)
