from __future__ import annotations

import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk import (
    generate_resampling_risk_boundaries,
    replay_exceedance_stream,
    spending_allowance,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_resampling_risk_controller_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def table(max_n: int = 199):
    config = load_config()
    return generate_resampling_risk_boundaries(
        alpha=float(config["alpha"]),
        epsilon=float(config["epsilon"]),
        halfspend=float(config["halfspend"]),
        max_n=max_n,
        probability_tolerance=float(config["probability_tolerance"]),
    )


def test_controller_config_preserves_closed_scientific_boundary() -> None:
    config = load_config()
    assert config["alpha"] == 0.05
    assert config["epsilon"] == 0.001
    assert config["halfspend"] == 1000
    assert config["replay_max_attempts"] == 199
    assert config["replay_source"]["expected_restriction_runs"] == 750
    assert config["replay_source"]["expected_bootstrap_fit_failures"] == 0
    assert not any(config["execution_boundary"].values())


def test_spending_sequence_is_increasing_and_below_epsilon() -> None:
    values = [
        spending_allowance(
            n,
            epsilon=0.001,
            halfspend=1000,
        )
        for n in range(1, 200)
    ]
    assert values == sorted(values)
    assert all(0.0 < value < 0.001 for value in values)
    assert values[-1] == pytest.approx(0.001 * 199 / 1199)


def test_boundary_recursion_respects_spending_and_probability_mass() -> None:
    boundaries = table()
    assert boundaries.row(1).lower == -1
    assert boundaries.row(1).upper == 2

    previous_spending = 0.0
    for row in boundaries.rows:
        assert row.spending_allowance >= previous_spending
        assert (
            row.cumulative_lower_probability
            <= row.spending_allowance + boundaries.probability_tolerance
        )
        assert (
            row.cumulative_upper_probability
            <= row.spending_allowance + boundaries.probability_tolerance
        )
        assert row.lower < row.upper
        assert 0.0 <= row.survivor_probability <= 1.0
        total = (
            row.survivor_probability
            + row.cumulative_lower_probability
            + row.cumulative_upper_probability
        )
        assert total == pytest.approx(1.0, abs=1e-12)
        previous_spending = row.spending_allowance

    assert boundaries.row(99).lower == -1
    assert boundaries.row(99).upper == 17
    assert boundaries.row(199).lower == 0
    assert boundaries.row(199).upper == 25


def test_boundary_generation_is_deterministic() -> None:
    first = table().to_dict()
    second = table().to_dict()
    assert first == second


def test_clear_not_reject_stream_stops_at_upper_boundary() -> None:
    result = replay_exceedance_stream(
        [1] * 199,
        boundaries=table(),
    )
    assert result.status == "SEQUENTIAL_DECISION"
    assert result.decision == "NOT_REJECT_P_GT_ALPHA"
    assert result.boundary_hit == "UPPER"
    assert result.stopping_n == 5
    assert result.stopping_sum == 5


def test_clear_reject_stream_can_require_many_draws_under_small_risk() -> None:
    result = replay_exceedance_stream(
        [0] * 199,
        boundaries=table(),
    )
    assert result.status == "SEQUENTIAL_DECISION"
    assert result.decision == "REJECT_P_LE_ALPHA"
    assert result.boundary_hit == "LOWER"
    assert result.stopping_n == 173
    assert result.stopping_sum == 0


def test_near_threshold_stream_remains_unresolved() -> None:
    stream = [1 if index % 20 == 0 else 0 for index in range(1, 200)]
    result = replay_exceedance_stream(
        stream,
        boundaries=table(),
    )
    assert result.status == "SEQUENTIAL_UNRESOLVED"
    assert result.decision is None
    assert result.terminal_n == 199
    assert result.terminal_sum == 9
    assert result.terminal_lower == 0
    assert result.terminal_upper == 25


def test_bootstrap_refit_failure_fails_closed() -> None:
    result = replay_exceedance_stream(
        [0, 0, None, 0],
        boundaries=table(),
    )
    assert result.status == "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    assert result.decision is None
    assert result.failure_n == 3


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"alpha": 0.0}, "alpha"),
        ({"alpha": 1.0}, "alpha"),
        ({"epsilon": 0.0}, "epsilon"),
        ({"epsilon": 0.3}, "epsilon"),
        ({"halfspend": 0.0}, "halfspend"),
        ({"max_n": 0}, "max_n"),
        ({"probability_tolerance": 0.0}, "probability_tolerance"),
    ],
)
def test_invalid_controller_parameters_fail_closed(
    kwargs: dict,
    message: str,
) -> None:
    params = {
        "alpha": 0.05,
        "epsilon": 0.001,
        "halfspend": 1000.0,
        "max_n": 199,
        "probability_tolerance": 1e-12,
    }
    params.update(kwargs)
    with pytest.raises(ValueError, match=message):
        generate_resampling_risk_boundaries(**params)


def test_decision_is_terminal_with_respect_to_longer_prefixes() -> None:
    boundaries = table()
    short = replay_exceedance_stream(
        [1] * 5,
        boundaries=boundaries,
    )
    long = replay_exceedance_stream(
        [1] * 199,
        boundaries=boundaries,
    )
    assert short.decision == long.decision
    assert short.stopping_n == long.stopping_n == 5
