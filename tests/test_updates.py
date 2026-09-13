import math

from cognitive_epistemic_model.updates import (
    decay_correction,
    encode_correction,
    update_familiarity,
    update_reliability,
)


def test_familiarity_reference_value():
    assert math.isclose(update_familiarity(0.2, 0.25), 0.4)


def test_bounds_grid():
    vals = [0.0, 0.1, 0.5, 0.9, 1.0]
    alphas = [0.0, 0.2, 0.7, 1.0]
    for x in vals:
        for a in alphas:
            assert 0 <= update_familiarity(x, a) <= 1
            assert 0 <= encode_correction(x, a) <= 1
            assert 0 <= update_reliability(x, a, 0.0) <= 1
            assert 0 <= update_reliability(x, a, 1.0) <= 1


def test_monotonicity():
    assert update_familiarity(0.2, 0.3) >= 0.2
    assert encode_correction(0.2, 0.3) >= 0.2
    assert decay_correction(0.8, 0.1, 2.0) <= 0.8
    assert update_reliability(0.5, 0.2, 1.0) >= 0.5
    assert update_reliability(0.5, 0.2, 0.0) <= 0.5
