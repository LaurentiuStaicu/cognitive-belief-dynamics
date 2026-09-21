from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING

from .events import DecisionEvent, Event, ExposureEvent
from .network import StaticDirectedNetwork

if TYPE_CHECKING:
    from .simulation import LogEntry


@dataclass(frozen=True)
class TransmissionProposal:
    event: ExposureEvent
    sender_id: str
    recipient_id: str
    delay: float
    policy_id: str


class TransmissionPolicy(Protocol):
    policy_id: str

    def propose(
        self,
        event: Event,
        completed_log: "LogEntry",
        network: StaticDirectedNetwork,
    ) -> tuple[TransmissionProposal, ...]:
        ...


@dataclass(frozen=True)
class ForcedPassThroughPolicy:
    """Architecture-only Share -> realised Exposure test policy.

    This is deliberately synthetic. It contains no ranking model, empirical
    reach probability, attention model, or calibrated diffusion parameter.
    """

    delay: float
    policy_id: str = "POLICY.F1A.FORCED_PASS_THROUGH.V1"

    def __post_init__(self) -> None:
        if self.delay <= 0:
            raise ValueError("synthetic transmission delay must be strictly positive")

    def propose(
        self,
        event: Event,
        completed_log: "LogEntry",
        network: StaticDirectedNetwork,
    ) -> tuple[TransmissionProposal, ...]:
        if not isinstance(event, DecisionEvent):
            return ()
        observation = completed_log.observation
        if observation is None or observation.get("share") is not True:
            return ()

        proposals: list[TransmissionProposal] = []
        for recipient_id in network.eligible_recipients(event.agent_id):
            proposals.append(
                TransmissionProposal(
                    event=ExposureEvent(
                        time=event.time + self.delay,
                        agent_id=recipient_id,
                        claim_id=event.claim_id,
                        source_id=event.source_id,
                    ),
                    sender_id=event.agent_id,
                    recipient_id=recipient_id,
                    delay=self.delay,
                    policy_id=self.policy_id,
                )
            )
        return tuple(proposals)
