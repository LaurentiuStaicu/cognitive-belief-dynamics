import inspect

from cognitive_epistemic_model.model import compute_belief


def test_truth_state_not_in_belief_api():
    names = set(inspect.signature(compute_belief).parameters)
    assert "truth" not in names
    assert "truth_state" not in names
