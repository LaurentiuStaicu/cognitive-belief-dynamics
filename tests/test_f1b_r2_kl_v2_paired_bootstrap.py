from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

import cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization as paired
import cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery as rr
from cognitive_epistemic_model.calibration.f1b_hierarchical_recovery import (
    RandomEffectScales,
)
from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R2Dataset,
)
from cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery import (
    R2Restriction,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def fake_cases() -> list[dict]:
    rows = []
    axes = (
        "STANDALONE_ACCURACY_MAIN_EFFECT",
        "COMPLEMENT_RELATION_VIOLATION",
        "COMBINED_VIOLATION",
    )
    for index in range(36):
        axis = axes[index % 3]
        rows.append(
            {
                "case_id": f"FAKE_V2_CASE_{index:02d}",
                "general_coefficients": [
                    -0.2,
                    0.5,
                    0.0,
                    0.4,
                    0.0,
                    0.0,
                ],
                "anchor_id": f"ANCHOR_{index % 2}",
                "axis": axis,
                "sign": -1 if (index // 2) % 2 == 0 else 1,
                "requested_mean_bernoulli_kl": (
                    0.001,
                    0.002,
                    0.003,
                )[index % 3],
                "achieved_mean_bernoulli_kl": (
                    0.001,
                    0.002,
                    0.003,
                )[index % 3],
                "nearest_add_rms_distance": 0.0,
                "add_compatibility_expected": (
                    axis == "STANDALONE_ACCURACY_MAIN_EFFECT"
                ),
            }
        )
    return rows


def fake_paired_result(*args, draw_counts, **kwargs):
    attempts = tuple(float(index) for index in range(max(draw_counts)))
    snapshots = tuple(
        SimpleNamespace(
            bootstrap_draws_requested=int(count),
            bootstrap_draws_successful=int(count),
            bootstrap_fit_failures=0,
            critical_value=float(count),
            p_value=1.0 / (count + 1),
            rejected=True,
            bootstrap_calibration_failure=False,
        )
        for count in draw_counts
    )
    return SimpleNamespace(
        restriction=kwargs.get("restriction", R2Restriction.ADD),
        observed_statistic=1.0,
        bootstrap_attempt_statistics=attempts,
        snapshots=snapshots,
        held_out_participant_delta=0.1,
        held_out_item_delta=0.2,
    )


def test_paired_config_freezes_pairing_without_authoritative_claims() -> None:
    config = load_config()
    assert config["seed"] == 2026092704
    assert config["bootstrap"]["draw_grid"] == [49, 99, 199]
    assert config["bootstrap"][
        "minimum_successful_draws_by_draw_count"
    ] == {"49": 45, "99": 90, "199": 180}
    assert config["evaluation_replicates"] == 10
    assert config["expected_unique_datasets"] == 390
    assert config["expected_restriction_runs"] == 750
    assert config["expected_snapshot_count"] == 2250
    assert config["expected_pair_comparison_count"] == 2250
    assert all(config["pairing_contract"].values())
    assert not any(config["execution_boundary"].values())


def test_bootstrap_prefix_snapshots_reuse_exact_attempt_prefixes(
    monkeypatch,
) -> None:
    observed = object()

    def fake_fit(dataset, restriction, *, scales, mask=None):
        statistic = (
            0.5
            if dataset is observed
            else float(dataset.value)
        )
        return SimpleNamespace(
            restriction=restriction,
            restricted=SimpleNamespace(),
            general=SimpleNamespace(),
            statistic=statistic,
        )

    def fake_simulate(template, restricted_fit, *, scales, rng):
        return SimpleNamespace(value=float(rng.random()))

    monkeypatch.setattr(rr, "fit_restriction_pair", fake_fit)
    monkeypatch.setattr(
        rr,
        "held_out_predictive_deltas",
        lambda *args, **kwargs: (0.1, 0.2),
    )
    monkeypatch.setattr(
        rr,
        "simulate_exact_design_under_restriction",
        fake_simulate,
    )

    scales = RandomEffectScales(
        participant_intercept_sd=0.1,
        item_intercept_sd=0.1,
        participant_slope_sd=0.1,
        item_slope_sd=0.1,
    )
    result = rr.bootstrap_restriction_test_prefix_snapshots(
        observed,
        R2Restriction.ADD,
        scales=scales,
        draw_counts=(49, 99, 199),
        minimum_successful_draws_by_count={49: 45, 99: 90, 199: 180},
        seed=12345,
        alpha=0.05,
    )
    prefix = rr.bootstrap_restriction_test_prefix_snapshots(
        observed,
        R2Restriction.ADD,
        scales=scales,
        draw_counts=(49,),
        minimum_successful_draws_by_count={49: 45},
        seed=12345,
        alpha=0.05,
    )

    assert len(result.bootstrap_attempt_statistics) == 199
    assert tuple(result.bootstrap_attempt_statistics[:49]) == (
        prefix.bootstrap_attempt_statistics
    )
    assert result.snapshots[0] == prefix.snapshots[0]
    assert [row.bootstrap_draws_requested for row in result.snapshots] == [
        49,
        99,
        199,
    ]


def test_dataset_fingerprint_covers_all_r2_arrays() -> None:
    dataset = R2Dataset(
        share=np.asarray([0, 1], dtype=int),
        belief=np.asarray([0.2, 0.8], dtype=float),
        accuracy_cue=np.asarray([0.0, 1.0], dtype=float),
        reward_context=np.asarray([-1.0, 1.0], dtype=float),
        participant=np.asarray([0, 1], dtype=int),
        item=np.asarray([1, 0], dtype=int),
    )
    same = R2Dataset(
        share=dataset.share.copy(),
        belief=dataset.belief.copy(),
        accuracy_cue=dataset.accuracy_cue.copy(),
        reward_context=dataset.reward_context.copy(),
        participant=dataset.participant.copy(),
        item=dataset.item.copy(),
    )
    changed = R2Dataset(
        share=np.asarray([1, 1], dtype=int),
        belief=dataset.belief.copy(),
        accuracy_cue=dataset.accuracy_cue.copy(),
        reward_context=dataset.reward_context.copy(),
        participant=dataset.participant.copy(),
        item=dataset.item.copy(),
    )
    assert paired.dataset_fingerprint(dataset) == paired.dataset_fingerprint(
        same
    )
    assert paired.dataset_fingerprint(dataset) != paired.dataset_fingerprint(
        changed
    )


def test_draw_counts_and_restrictions_share_one_departure_dataset(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        paired,
        "bootstrap_restriction_test_prefix_snapshots",
        fake_paired_result,
    )
    config = load_config()
    result = paired.run_paired_bootstrap_characterization(
        config,
        fake_cases(),
        replicate_indices=(0,),
    )

    assert result["unique_dataset_count"] == 39
    assert result["restriction_run_count"] == 75
    assert result["snapshot_count"] == 225
    assert result["pair_comparison_count"] == 225
    assert all(
        run["dataset_id"].startswith(
            config["characterization_id"] + "|"
        )
        for run in result["restriction_runs"]
    )
    assert any(
        "|NULL|" in run["dataset_id"]
        for run in result["restriction_runs"]
    )
    assert any(
        "|V2|" in run["dataset_id"]
        for run in result["restriction_runs"]
    )

    departure_groups: dict[str, list[dict]] = {}
    for run in result["restriction_runs"]:
        if run["identity_type"] == "DEPARTURE":
            departure_groups.setdefault(run["dataset_id"], []).append(run)
    assert len(departure_groups) == 36
    for runs in departure_groups.values():
        assert len(runs) == 2
        assert {run["restriction"] for run in runs} == {
            R2Restriction.CBD_COMPLEMENT.value,
            R2Restriction.ADD.value,
        }
        assert len({run["dataset_sha256"] for run in runs}) == 1
        for run in runs:
            assert [row["bootstrap_draws"] for row in run["snapshots"]] == [
                49,
                99,
                199,
            ]
            assert len(run["bootstrap_attempt_statistics"]) == 199


def test_case_order_does_not_change_dataset_identity_or_fingerprint(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        paired,
        "bootstrap_restriction_test_prefix_snapshots",
        fake_paired_result,
    )
    config = load_config()
    cases = fake_cases()
    forward = paired.run_paired_bootstrap_characterization(
        config,
        cases,
        replicate_indices=(0,),
    )
    reverse = paired.run_paired_bootstrap_characterization(
        config,
        list(reversed(cases)),
        replicate_indices=(0,),
    )
    f_map = {
        (run["dataset_id"], run["restriction"]): run["dataset_sha256"]
        for run in forward["restriction_runs"]
    }
    r_map = {
        (run["dataset_id"], run["restriction"]): run["dataset_sha256"]
        for run in reverse["restriction_runs"]
    }
    assert f_map == r_map


def test_replicate_partitions_recombine_and_fail_closed(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        paired,
        "bootstrap_restriction_test_prefix_snapshots",
        fake_paired_result,
    )
    config = load_config()
    cases = fake_cases()
    base = paired.run_paired_bootstrap_characterization(
        config,
        cases,
        replicate_indices=(0,),
    )

    partitions = []
    for shard in config["execution_partition_plan"]["shards"]:
        cloned_runs = []
        for replicate in shard["replicate_indices"]:
            for run in base["restriction_runs"]:
                cloned = copy.deepcopy(run)
                old_dataset = cloned["dataset_id"]
                new_dataset = old_dataset.replace(
                    "REPLICATE=0",
                    f"REPLICATE={replicate}",
                )
                cloned["dataset_id"] = new_dataset
                cloned["run_id"] = cloned["run_id"].replace(
                    old_dataset,
                    new_dataset,
                )
                cloned["evaluation_replicate"] = replicate
                cloned_runs.append(cloned)
        partition = copy.deepcopy(base)
        partition["execution_replicate_indices"] = list(
            shard["replicate_indices"]
        )
        partition["unique_dataset_count"] = 39 * len(
            shard["replicate_indices"]
        )
        partition["restriction_run_count"] = len(cloned_runs)
        partition["snapshot_count"] = len(cloned_runs) * 3
        partition["restriction_runs"] = cloned_runs
        partition["pair_comparisons"] = []
        partition["pair_aggregate"] = []
        partition["snapshot_aggregate"] = []
        partitions.append(partition)

    combined = paired.combine_paired_bootstrap_partitions(
        partitions,
        config,
    )
    assert combined["execution_replicate_indices"] == list(range(10))
    assert combined["unique_dataset_count"] == 390
    assert combined["restriction_run_count"] == 750
    assert combined["snapshot_count"] == 2250
    assert combined["pair_comparison_count"] == 2250

    with pytest.raises(ValueError, match="overlap"):
        paired.combine_paired_bootstrap_partitions(
            [partitions[0], partitions[0], *partitions[1:]],
            config,
        )

    with pytest.raises(ValueError, match="coverage incomplete"):
        paired.combine_paired_bootstrap_partitions(
            partitions[:-1],
            config,
        )
