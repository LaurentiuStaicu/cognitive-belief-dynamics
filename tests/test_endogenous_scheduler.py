from __future__ import annotations

from copy import deepcopy

import pytest
from hypothesis import given, strategies as st

from cognitive_epistemic_model.endogenous import run_endogenous
from cognitive_epistemic_model.events import CorrectionEvent, DecisionEvent, ExposureEvent
from cognitive_epistemic_model.network import StaticDirectedNetwork
from cognitive_epistemic_model.simulation import Simulator
from cognitive_epistemic_model.state import AgentState
from cognitive_epistemic_model.transmission import ForcedPassThroughPolicy


def _agents() -> dict[str, AgentState]:
    return {
        "A": AgentState(agent_id="A"),
        "B": AgentState(agent_id="B"),
        "C": AgentState(agent_id="C"),
    }


def test_f1a_dyad_share_generates_delayed_recipient_exposure() -> None:
    agents = _agents()
    # Extreme synthetic software fixture: chosen prospectively to make the
    # Share=true integration path deterministic, not as a behavioral parameter.
    agents["A"].sharing_bias = 100.0
    sim = Simulator(agents, seed=20260921)
    network = StaticDirectedNetwork(nodes=("A", "B"), edges=(("A", "B"),))
    policy = ForcedPassThroughPolicy(delay=2.0)

    result = run_endogenous(
        sim,
        [
            DecisionEvent(
                time=1.0,
                agent_id="A",
                claim_id="C1",
                source_id="S1",
                evidence_signal=0.0,
            )
        ],
        network=network,
        policy=policy,
    )

    assert result.stop_reason == "completed"
    assert result.remaining_events == 0
    assert [entry.event_type for entry in result.log] == ["DecisionEvent", "ExposureEvent"]
    assert result.log[0].observation is not None
    assert result.log[0].observation["share"] is True
    assert result.log[1].agent_id == "B"
    assert result.log[1].time == 3.0
    assert agents["B"].f("C1") == pytest.approx(sim.params.alpha_f)

    parent, child = result.trace
    assert parent.origin == "EXOGENOUS"
    assert parent.generated_notice_ids == (child.notice_id,)
    assert child.origin == "ENDOGENOUS"
    assert child.parent_notice_id == parent.notice_id
    assert child.sender_id == "A"
    assert child.recipient_id == "B"
    assert child.scheduled_time > parent.scheduled_time


def test_f1a_does_not_generate_recipient_decision() -> None:
    agents = _agents()
    agents["A"].sharing_bias = 100.0
    sim = Simulator(agents, seed=20260921)

    result = run_endogenous(
        sim,
        [
            DecisionEvent(
                time=1.0,
                agent_id="A",
                claim_id="C1",
                source_id="S1",
                evidence_signal=0.0,
            )
        ],
        network=StaticDirectedNetwork(nodes=("A", "B"), edges=(("A", "B"),)),
        policy=ForcedPassThroughPolicy(delay=1.0),
    )

    assert [entry.event_type for entry in result.log].count("DecisionEvent") == 1
    assert result.log[-1].event_type == "ExposureEvent"


def test_disabled_endogenous_layer_matches_open_loop_runner() -> None:
    events = [
        ExposureEvent(time=0.0, agent_id="A", claim_id="C1", source_id="S1"),
        CorrectionEvent(time=1.0, agent_id="A", claim_id="C1", direction=-1.0),
        DecisionEvent(
            time=2.0,
            agent_id="A",
            claim_id="C1",
            source_id="S1",
            evidence_signal=0.2,
        ),
    ]
    reference_agents = _agents()
    experimental_agents = deepcopy(reference_agents)

    reference = Simulator(reference_agents, seed=17)
    experimental = Simulator(experimental_agents, seed=17)

    reference_log = reference.run(events)
    result = run_endogenous(experimental, events)

    assert list(result.log) == reference_log
    assert experimental_agents == reference_agents
    assert result.stop_reason == "completed"
    assert all(item.origin == "EXOGENOUS" for item in result.trace)


def test_initial_same_time_order_matches_stable_open_loop_order() -> None:
    events = [
        ExposureEvent(time=1.0, agent_id="A", claim_id="C1", source_id="S1"),
        ExposureEvent(time=1.0, agent_id="A", claim_id="C2", source_id="S1"),
        ExposureEvent(time=1.0, agent_id="A", claim_id="C3", source_id="S1"),
    ]
    reference = Simulator(_agents(), seed=3)
    experimental = Simulator(_agents(), seed=3)

    reference.run(events)
    result = run_endogenous(experimental, events)

    assert [entry.payload["claim_id"] for entry in result.log] == ["C1", "C2", "C3"]
    assert list(result.log) == reference.log


def test_horizon_stops_before_future_generated_event() -> None:
    agents = _agents()
    agents["A"].sharing_bias = 100.0
    result = run_endogenous(
        Simulator(agents, seed=20260921),
        [
            DecisionEvent(
                time=1.0,
                agent_id="A",
                claim_id="C1",
                source_id="S1",
                evidence_signal=0.0,
            )
        ],
        network=StaticDirectedNetwork(nodes=("A", "B"), edges=(("A", "B"),)),
        policy=ForcedPassThroughPolicy(delay=5.0),
        until=2.0,
    )

    assert result.stop_reason == "horizon"
    assert result.remaining_events == 1
    assert agents["B"].f("C1") == 0.0


def test_max_events_guard_is_deterministic() -> None:
    result = run_endogenous(
        Simulator(_agents(), seed=1),
        [
            ExposureEvent(time=0.0, agent_id="A", claim_id="C1", source_id="S1"),
            ExposureEvent(time=1.0, agent_id="A", claim_id="C1", source_id="S1"),
        ],
        max_events=1,
    )
    assert result.stop_reason == "max_events"
    assert len(result.log) == 1
    assert result.remaining_events == 1


@given(st.lists(st.integers(min_value=0, max_value=20), min_size=0, max_size=20))
def test_processed_times_are_non_decreasing(times: list[int]) -> None:
    events = [
        ExposureEvent(
            time=float(time),
            agent_id="A",
            claim_id=f"C{index}",
            source_id="S1",
        )
        for index, time in enumerate(times)
    ]
    result = run_endogenous(Simulator(_agents(), seed=1), events)
    processed = [entry.scheduled_time for entry in result.trace]
    assert processed == sorted(processed)
