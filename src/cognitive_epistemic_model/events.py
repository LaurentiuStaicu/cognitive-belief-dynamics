from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Event:
    time: float
    agent_id: str


@dataclass(frozen=True, order=True)
class ExposureEvent(Event):
    claim_id: str
    source_id: str


@dataclass(frozen=True, order=True)
class CorrectionEvent(Event):
    claim_id: str
    direction: float = -1.0


@dataclass(frozen=True, order=True)
class SourceFeedbackEvent(Event):
    source_id: str
    confirmed: bool


@dataclass(frozen=True, order=True)
class DecisionEvent(Event):
    claim_id: str
    source_id: str
    evidence_signal: float
    reward_context: float = 0.0
    accuracy_cue: bool = False
