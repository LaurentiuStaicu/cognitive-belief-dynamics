from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Iterable

from .events import Event
from .network import StaticDirectedNetwork
from .simulation import LogEntry, Simulator
from .transmission import TransmissionPolicy


@dataclass(frozen=True)
class EventNotice:
    notice_id: int
    sequence_id: int
    event: Event
    origin: str
    parent_notice_id: int | None = None
    generation_activity_id: str | None = None
    policy_id: str | None = None
    sender_id: str | None = None
    recipient_id: str | None = None

    @property
    def scheduled_time(self) -> float:
        return self.event.time


@dataclass(frozen=True)
class SchedulerTraceEntry:
    notice_id: int
    sequence_id: int
    scheduled_time: float
    event_type: str
    agent_id: str
    origin: str
    parent_notice_id: int | None
    generation_activity_id: str | None
    policy_id: str | None
    sender_id: str | None
    recipient_id: str | None
    log_index: int
    generated_notice_ids: tuple[int, ...]


@dataclass(frozen=True)
class EndogenousRunResult:
    log: tuple[LogEntry, ...]
    trace: tuple[SchedulerTraceEntry, ...]
    stop_reason: str
    remaining_events: int


def run_endogenous(
    simulator: Simulator,
    events: Iterable[Event],
    *,
    network: StaticDirectedNetwork | None = None,
    policy: TransmissionPolicy | None = None,
    until: float | None = None,
    max_events: int | None = None,
) -> EndogenousRunResult:
    """Run an additive experimental future-event scheduler around Simulator.step.

    Existing CBD cognitive semantics remain owned by Simulator.step(). The
    experimental layer only orders notices, observes canonical log entries,
    and optionally schedules future events returned by a transmission policy.
    """

    if policy is not None and network is None:
        raise ValueError("a network is required when a transmission policy is enabled")
    if max_events is not None and max_events <= 0:
        raise ValueError("max_events must be positive")

    queue: list[tuple[float, int, EventNotice]] = []
    next_sequence = 0

    def push(
        event: Event,
        *,
        origin: str,
        parent_notice_id: int | None = None,
        generation_activity_id: str | None = None,
        policy_id: str | None = None,
        sender_id: str | None = None,
        recipient_id: str | None = None,
    ) -> EventNotice:
        nonlocal next_sequence
        sequence_id = next_sequence
        next_sequence += 1
        notice = EventNotice(
            notice_id=sequence_id,
            sequence_id=sequence_id,
            event=event,
            origin=origin,
            parent_notice_id=parent_notice_id,
            generation_activity_id=generation_activity_id,
            policy_id=policy_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
        )
        heapq.heappush(queue, (event.time, sequence_id, notice))
        return notice

    for event in events:
        push(event, origin="EXOGENOUS")

    trace: list[SchedulerTraceEntry] = []
    processed = 0
    stop_reason = "completed"

    while queue:
        if max_events is not None and processed >= max_events:
            stop_reason = "max_events"
            break
        if until is not None and queue[0][0] > until:
            stop_reason = "horizon"
            break

        _, _, notice = heapq.heappop(queue)
        before_log_len = len(simulator.log)
        simulator.step(notice.event)
        if len(simulator.log) != before_log_len + 1:
            raise RuntimeError("Simulator.step() must append exactly one canonical LogEntry")

        completed_log = simulator.log[-1]
        if (
            completed_log.time != notice.event.time
            or completed_log.event_type != type(notice.event).__name__
            or completed_log.agent_id != notice.event.agent_id
        ):
            raise RuntimeError("canonical log entry does not match the processed notice")

        generated_notice_ids: list[int] = []
        if policy is not None:
            assert network is not None
            proposals = policy.propose(notice.event, completed_log, network)
            for proposal_index, proposal in enumerate(proposals):
                if proposal.delay <= 0 or proposal.event.time <= notice.event.time:
                    raise ValueError("generated events require strictly positive delay")
                if proposal.recipient_id not in simulator.agents:
                    raise ValueError("generated recipient must exist in simulator agents")
                if proposal.event.agent_id != proposal.recipient_id:
                    raise ValueError("generated event agent must match proposal recipient")

                child = push(
                    proposal.event,
                    origin="ENDOGENOUS",
                    parent_notice_id=notice.notice_id,
                    generation_activity_id=f"GEN.{notice.notice_id}.{proposal_index}",
                    policy_id=proposal.policy_id,
                    sender_id=proposal.sender_id,
                    recipient_id=proposal.recipient_id,
                )
                generated_notice_ids.append(child.notice_id)

        trace.append(
            SchedulerTraceEntry(
                notice_id=notice.notice_id,
                sequence_id=notice.sequence_id,
                scheduled_time=notice.scheduled_time,
                event_type=type(notice.event).__name__,
                agent_id=notice.event.agent_id,
                origin=notice.origin,
                parent_notice_id=notice.parent_notice_id,
                generation_activity_id=notice.generation_activity_id,
                policy_id=notice.policy_id,
                sender_id=notice.sender_id,
                recipient_id=notice.recipient_id,
                log_index=len(simulator.log) - 1,
                generated_notice_ids=tuple(generated_notice_ids),
            )
        )
        processed += 1

    return EndogenousRunResult(
        log=tuple(simulator.log),
        trace=tuple(trace),
        stop_reason=stop_reason,
        remaining_events=len(queue),
    )
