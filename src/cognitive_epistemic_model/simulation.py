from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from .events import CorrectionEvent, DecisionEvent, Event, ExposureEvent, SourceFeedbackEvent
from .model import Judgment, judge
from .state import AgentState, ModelParams
from .updates import decay_correction, encode_correction, update_familiarity, update_reliability


@dataclass(frozen=True)
class LogEntry:
    time: float
    event_type: str
    agent_id: str
    payload: dict
    state_change: dict
    observation: dict | None = None


class Simulator:
    def __init__(self, agents: dict[str, AgentState], params: ModelParams | None = None, seed: int = 1):
        self.agents = agents
        self.params = params or ModelParams()
        self.rng = np.random.default_rng(seed)
        self.seed = seed
        self.time = 0.0
        self.log: list[LogEntry] = []
        self._last_decay_time: dict[tuple[str, str], float] = {}
        self._correction_direction: dict[tuple[str, str], float] = {}

    def _decay_claim_correction(self, agent: AgentState, claim_id: str, now: float) -> None:
        key = (agent.agent_id, claim_id)
        last = self._last_decay_time.get(key, now)
        dt = now - last
        if dt > 0 and claim_id in agent.correction_access:
            agent.correction_access[claim_id] = decay_correction(
                agent.correction_access[claim_id], self.params.lambda_c, dt
            )
        self._last_decay_time[key] = now

    def run(self, events: Iterable[Event]) -> list[LogEntry]:
        # Stable chronological order: input order resolves simultaneous events.
        for event in sorted(events, key=lambda event: event.time):
            self.step(event)
        return self.log

    def step(self, event: Event) -> Judgment | None:
        if event.time < self.time:
            raise ValueError("events must be processed in non-decreasing time order")
        self.time = event.time
        agent = self.agents[event.agent_id]
        before: dict = {}
        after: dict = {}
        observation = None

        if isinstance(event, ExposureEvent):
            before["familiarity"] = agent.f(event.claim_id)
            agent.familiarity[event.claim_id] = update_familiarity(before["familiarity"], self.params.alpha_f)
            after["familiarity"] = agent.familiarity[event.claim_id]

        elif isinstance(event, CorrectionEvent):
            self._decay_claim_correction(agent, event.claim_id, event.time)
            before["correction_access"] = agent.c(event.claim_id)
            agent.correction_access[event.claim_id] = encode_correction(before["correction_access"], self.params.alpha_c)
            self._correction_direction[(agent.agent_id, event.claim_id)] = event.direction
            after["correction_access"] = agent.correction_access[event.claim_id]

        elif isinstance(event, SourceFeedbackEvent):
            before["reliability_estimate"] = agent.t(event.source_id)
            agent.reliability_estimate[event.source_id] = update_reliability(
                before["reliability_estimate"], self.params.alpha_t, 1.0 if event.confirmed else 0.0
            )
            after["reliability_estimate"] = agent.reliability_estimate[event.source_id]

        elif isinstance(event, DecisionEvent):
            self._decay_claim_correction(agent, event.claim_id, event.time)
            direction = self._correction_direction.get((agent.agent_id, event.claim_id), 0.0)
            j = judge(
                prior_belief=agent.b0(event.claim_id),
                familiarity=agent.f(event.claim_id),
                correction_access=agent.c(event.claim_id),
                correction_direction=direction,
                evidence_signal=event.evidence_signal,
                reliability_estimate=agent.t(event.source_id),
                accuracy_baseline=agent.accuracy_baseline,
                accuracy_cue=event.accuracy_cue,
                reward_context=event.reward_context,
                sharing_bias=agent.sharing_bias,
                params=self.params,
            )
            share = bool(self.rng.random() < j.share_probability)
            observation = {**asdict(j), "share": share}
        else:
            raise TypeError(f"unsupported event type: {type(event)!r}")

        payload = asdict(event)
        payload.pop("time", None)
        payload.pop("agent_id", None)
        self.log.append(
            LogEntry(
                time=event.time,
                event_type=type(event).__name__,
                agent_id=event.agent_id,
                payload=payload,
                state_change={"before": before, "after": after},
                observation=observation,
            )
        )
        return None if observation is None else j
