from __future__ import annotations

from cognitive_epistemic_model.events import DecisionEvent, ExposureEvent
from cognitive_epistemic_model.network import StaticDirectedNetwork
from cognitive_epistemic_model.simulation import LogEntry
from cognitive_epistemic_model.transmission import ForcedPassThroughPolicy


def _decision() -> DecisionEvent:
    return DecisionEvent(
        time=2.0,
        agent_id="A",
        claim_id="C1",
        source_id="S1",
        evidence_signal=0.0,
    )


def _log(share: bool) -> LogEntry:
    return LogEntry(
        time=2.0,
        event_type="DecisionEvent",
        agent_id="A",
        payload={"claim_id": "C1", "source_id": "S1", "evidence_signal": 0.0},
        state_change={"before": {}, "after": {}},
        observation={"share": share},
    )


def test_forced_policy_share_true_routes_only_over_declared_edges() -> None:
    network = StaticDirectedNetwork(
        nodes=("A", "B", "C"),
        edges=(("A", "B"),),
    )
    proposals = ForcedPassThroughPolicy(delay=3.0).propose(_decision(), _log(True), network)

    assert len(proposals) == 1
    proposal = proposals[0]
    assert proposal.sender_id == "A"
    assert proposal.recipient_id == "B"
    assert proposal.event == ExposureEvent(
        time=5.0,
        agent_id="B",
        claim_id="C1",
        source_id="S1",
    )


def test_forced_policy_share_false_generates_nothing() -> None:
    network = StaticDirectedNetwork(nodes=("A", "B"), edges=(("A", "B"),))
    assert ForcedPassThroughPolicy(delay=1.0).propose(_decision(), _log(False), network) == ()


def test_static_network_is_directed_and_preserves_declared_order() -> None:
    network = StaticDirectedNetwork(
        nodes=("A", "B", "C"),
        edges=(("A", "C"), ("A", "B"), ("B", "A")),
    )
    assert network.eligible_recipients("A") == ("C", "B")
    assert network.eligible_recipients("B") == ("A",)
    assert network.eligible_recipients("C") == ()


def test_network_rejects_unknown_edge_endpoint() -> None:
    try:
        StaticDirectedNetwork(nodes=("A",), edges=(("A", "B"),))
    except ValueError as exc:
        assert "declared node" in str(exc)
    else:
        raise AssertionError("invalid edge endpoint was accepted")


def test_policy_rejects_zero_or_negative_delay() -> None:
    for delay in (0.0, -1.0):
        try:
            ForcedPassThroughPolicy(delay=delay)
        except ValueError as exc:
            assert "strictly positive" in str(exc)
        else:
            raise AssertionError("non-positive delay was accepted")
