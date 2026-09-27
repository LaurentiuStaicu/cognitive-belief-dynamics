from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
    replay_retained_paired_bootstrap,
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


def snapshot(attempts: list[float], observed: float) -> list[dict]:
    rows = []
    for draws in (49, 99, 199):
        prefix = attempts[:draws]
        exceedances = sum(value >= observed for value in prefix)
        p_value = (1 + exceedances) / (1 + draws)
        rows.append(
            {
                "bootstrap_draws": draws,
                "bootstrap_draws_successful": draws,
                "bootstrap_fit_failures": 0,
                "critical_value": 0.0,
                "p_value": p_value,
                "rejected": p_value <= 0.05,
                "bootstrap_calibration_failure": False,
            }
        )
    return rows


def run_payload(
    run_id: str,
    attempts: list[float | None],
    *,
    observed: float = 0.5,
    role: str = "CBD_DEPARTURE_DETECTION",
) -> dict:
    minimum_success = {49: 45, 99: 90, 199: 180}
    snapshots = []
    for draws in (49, 99, 199):
        prefix = attempts[:draws]
        successful = [
            float(value) for value in prefix if value is not None
        ]
        failures = draws - len(successful)
        if len(successful) < minimum_success[draws]:
            snapshots.append(
                {
                    "bootstrap_draws": draws,
                    "bootstrap_draws_successful": len(successful),
                    "bootstrap_fit_failures": failures,
                    "critical_value": None,
                    "p_value": None,
                    "rejected": None,
                    "bootstrap_calibration_failure": True,
                }
            )
            continue
        exceedances = sum(value >= observed for value in successful)
        p_value = (1 + exceedances) / (1 + len(successful))
        snapshots.append(
            {
                "bootstrap_draws": draws,
                "bootstrap_draws_successful": len(successful),
                "bootstrap_fit_failures": failures,
                "critical_value": 0.0,
                "p_value": p_value,
                "rejected": p_value <= 0.05,
                "bootstrap_calibration_failure": False,
            }
        )
    return {
        "run_id": run_id,
        "dataset_id": "DATASET|" + run_id,
        "dataset_sha256": "a" * 64,
        "bootstrap_stream_seed": 123,
        "identity": "CASE",
        "identity_type": "DEPARTURE",
        "restriction": "CBD_COMPLEMENT_RESTRICTION",
        "role": role,
        "anchor_id": "CBD_ANCHOR_1",
        "axis": "COMPLEMENT_RELATION_VIOLATION",
        "sign": 1,
        "target_mean_bernoulli_kl": 0.002,
        "evaluation_replicate": 0,
        "observed_statistic": observed,
        "fit_failure": False,
        "bootstrap_attempt_statistics": attempts,
        "snapshots": snapshots,
    }


def mini_config(run_count: int) -> dict:
    config = copy.deepcopy(load_config())
    config["replay_source"]["expected_restriction_runs"] = run_count
    return config


def test_canonical_attempt_hash_is_deterministic_and_sensitive() -> None:
    first = canonical_attempt_sequence_sha256([0.1, None, 0.2])
    second = canonical_attempt_sequence_sha256([0.1, None, 0.2])
    changed = canonical_attempt_sequence_sha256([0.1, None, 0.3])
    assert first == second
    assert first != changed
    assert len(first) == 64

    with pytest.raises(ValueError):
        canonical_attempt_sequence_sha256([float("nan")])


def test_replay_preserves_unresolved_and_resolved_decisions() -> None:
    reject_attempts = [0.0] * 199
    nonreject_attempts = [1.0] * 199
    near_attempts = [
        1.0 if index % 20 == 0 else 0.0
        for index in range(1, 200)
    ]
    retained = {
        "authoritative": False,
        "restriction_run_count": 3,
        "restriction_runs": [
            run_payload("REJECT", reject_attempts),
            run_payload("NOT_REJECT", nonreject_attempts),
            run_payload("UNRESOLVED", near_attempts),
        ],
    }

    result = replay_retained_paired_bootstrap(
        retained,
        mini_config(3),
    )
    rows = {row["run_id"]: row for row in result["replay_rows"]}

    assert rows["REJECT"]["decision"] == "REJECT_P_LE_ALPHA"
    assert rows["REJECT"]["stopping_n"] == 173
    assert rows["REJECT"]["fixed_199_plus_one_p_value"] == 0.005

    assert rows["NOT_REJECT"]["decision"] == "NOT_REJECT_P_GT_ALPHA"
    assert rows["NOT_REJECT"]["stopping_n"] == 5
    assert rows["NOT_REJECT"]["fixed_199_plus_one_p_value"] == 1.0

    assert rows["UNRESOLVED"]["status"] == "SEQUENTIAL_UNRESOLVED"
    assert rows["UNRESOLVED"]["decision"] is None
    assert rows["UNRESOLVED"]["full_prefix_sum_199"] == 9
    assert rows["UNRESOLVED"]["fixed_199_plus_one_p_value"] == 0.05
    assert rows["UNRESOLVED"][
        "sequential_vs_fixed_199_disagreement"
    ] is None

    summary = result["global_summary"]
    assert summary["run_count"] == 3
    assert summary["resolved_by_49_count"] == 1
    assert summary["resolved_by_99_count"] == 1
    assert summary["resolved_by_199_count"] == 2
    assert summary["unresolved_at_199_count"] == 1


def test_replay_checkpoint_hashes_exact_attempt_sequence() -> None:
    attempts = [0.0] * 199
    retained = {
        "authoritative": False,
        "restriction_run_count": 1,
        "restriction_runs": [run_payload("ONE", attempts)],
    }
    result = replay_retained_paired_bootstrap(
        retained,
        mini_config(1),
    )
    checkpoint = result["stream_checkpoints"][0]
    assert checkpoint["run_id"] == "ONE"
    assert checkpoint["attempt_sequence_sha256"] == (
        canonical_attempt_sequence_sha256(attempts)
    )
    assert checkpoint["bootstrap_stream_seed"] == 123


def test_replay_verifies_retained_fixed_199_p_value() -> None:
    attempts = [0.0] * 199
    run = run_payload("BAD_P", attempts)
    run["snapshots"][-1]["p_value"] = 0.123
    retained = {
        "authoritative": False,
        "restriction_run_count": 1,
        "restriction_runs": [run],
    }
    with pytest.raises(ValueError, match="p-value mismatch"):
        replay_retained_paired_bootstrap(
            retained,
            mini_config(1),
        )


def test_replay_fails_closed_on_unexpected_bootstrap_refit_failure() -> None:
    attempts: list[float | None] = [0.0] * 199
    attempts[10] = None
    retained = {
        "authoritative": False,
        "restriction_run_count": 1,
        "restriction_runs": [run_payload("FAILED", attempts)],
    }
    with pytest.raises(
        ValueError,
        match=(
            "199-draw calibration failure|"
            "failure count does not match frozen replay source"
        ),
    ):
        replay_retained_paired_bootstrap(
            retained,
            mini_config(1),
        )


def test_replay_boundary_keeps_scientific_stage_closed() -> None:
    attempts = [1.0] * 199
    retained = {
        "authoritative": False,
        "restriction_run_count": 1,
        "restriction_runs": [run_payload("BOUNDARY", attempts)],
    }
    result = replay_retained_paired_bootstrap(
        retained,
        mini_config(1),
    )
    assert result["authoritative"] is False
    assert "does not select a bootstrap draw count" in (
        result["interpretation_boundary"]
    )
    assert "human N" in result["interpretation_boundary"]
    assert "runtime F1b" in result["interpretation_boundary"]
