from __future__ import annotations

from math import isclose

import pytest

from cognitive_epistemic_model.world_model import (
    WorldModelInputError,
    bayes_update,
    binary_uncertainty,
    initial_state,
    update_state,
)


def test_likelihood_ratio_sign_semantics():
    prior = 0.4
    assert bayes_update(prior, 2.0) > prior
    assert bayes_update(prior, 0.5) < prior
    assert bayes_update(prior, 1.0) == prior


def test_odds_form_reference_case():
    # prior odds 1:3, LR 3 -> posterior odds 1:1
    assert isclose(bayes_update(0.25, 3.0), 0.5, abs_tol=1e-12)


def test_sequential_updates_accumulate_in_log_evidence_space():
    state = initial_state(0.2)
    state = update_state(state, 4.0)
    state = update_state(state, 0.5)
    direct = bayes_update(0.2, 2.0)
    assert isclose(state.probability, direct, abs_tol=1e-12)
    assert isclose(state.cumulative_log2_likelihood_ratio, 1.0, abs_tol=1e-12)
    assert state.update_count == 2


def test_binary_uncertainty_invariants():
    assert binary_uncertainty(0.0) == 0.0
    assert binary_uncertainty(1.0) == 0.0
    assert binary_uncertainty(0.5) == 1.0
    assert isclose(binary_uncertainty(0.2), binary_uncertainty(0.8), abs_tol=1e-12)


def test_operator_fails_closed_instead_of_inventing_diagnosticity():
    for invalid_lr in (0.0, -1.0, float("inf"), float("nan")):
        with pytest.raises(WorldModelInputError):
            bayes_update(0.5, invalid_lr)


def test_probability_bounds_are_enforced():
    for invalid_p in (-0.01, 1.01, float("inf"), float("nan")):
        with pytest.raises(WorldModelInputError):
            initial_state(invalid_p)
