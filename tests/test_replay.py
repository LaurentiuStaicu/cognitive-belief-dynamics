from dataclasses import asdict

from cognitive_epistemic_model.events import DecisionEvent, ExposureEvent, CorrectionEvent, SourceFeedbackEvent
from cognitive_epistemic_model.simulation import Simulator
from cognitive_epistemic_model.state import AgentState


def run(seed):
    a = AgentState(agent_id="A", prior_belief={"C": 0.4})
    sim = Simulator({"A": a}, seed=seed)
    sim.run([DecisionEvent(0, "A", "C", "S", 0.1, reward_context=0.5)])
    return [asdict(x) for x in sim.log]


def test_same_seed_same_run():
    assert run(123) == run(123)


def test_mixed_events_are_processed_chronologically():
    sim = Simulator({"A": AgentState(agent_id="A")})
    log = sim.run([
        DecisionEvent(3, "A", "C", "S", 0.0),
        CorrectionEvent(2, "A", "C"),
        ExposureEvent(0, "A", "C", "S"),
        SourceFeedbackEvent(1, "A", "S", True),
    ])
    assert [entry.time for entry in log] == [0, 1, 2, 3]
    assert log[-1].observation is not None


def test_simultaneous_events_preserve_input_order():
    sim = Simulator({"A": AgentState(agent_id="A")})
    log = sim.run([
        ExposureEvent(0, "A", "C", "S"),
        DecisionEvent(0, "A", "C", "S", 0.0),
        CorrectionEvent(0, "A", "C"),
    ])
    assert [entry.event_type for entry in log] == [
        "ExposureEvent", "DecisionEvent", "CorrectionEvent"
    ]
