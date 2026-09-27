from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation as cont
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_resampling_risk_continuation_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def fake_payloads() -> tuple[dict, dict]:
    attempts = [float(index) / 1000.0 for index in range(199)]
    attempt_hash = canonical_attempt_sequence_sha256(attempts)
    runs = []
    checkpoints = []
    unresolved = []
    for index in range(224):
        run_id = f"RUN_{index:03d}"
        unresolved.append(run_id)
        runs.append(
            {
                "run_id": run_id,
                "identity": f"CASE_{index:03d}",
                "identity_type": "DEPARTURE",
                "restriction": "ADD_RESTRICTION",
                "role": "TEST_ROLE",
                "anchor_id": "ANCHOR",
                "axis": "AXIS",
                "sign": 1,
                "target_mean_bernoulli_kl": 0.002,
                "evaluation_replicate": index % 10,
                "dataset_id": f"DATASET_{index:03d}",
                "dataset_sha256": "a" * 64,
                "observed_statistic": 1.25,
                "bootstrap_stream_seed": 1000 + index,
                "bootstrap_attempt_statistics": list(attempts),
            }
        )
        checkpoints.append(
            {
                "run_id": run_id,
                "dataset_sha256": "a" * 64,
                "bootstrap_stream_seed": 1000 + index,
                "observed_statistic": 1.25,
                "attempt_sequence_sha256": attempt_hash,
            }
        )
    paired = {
        "restriction_run_count": len(runs),
        "restriction_runs": runs,
    }
    stage_b = {
        "unresolved_run_ids": unresolved,
        "stream_checkpoints": checkpoints,
        "integrity": {
            "stream_checkpoint_count": len(checkpoints),
        },
    }
    return paired, stage_b


def test_continuation_config_freezes_two_stage_contract() -> None:
    config = load_config()
    cont._validate_continuation_config(config)

    controller = config["controller"]
    assert controller["prior_max_attempts"] == 199
    assert controller["maximum_total_attempts"] == 10000
    assert controller["reporting_checkpoints"] == [
        199,
        499,
        999,
        1999,
        4999,
        10000,
    ]

    c1 = config["stage_c1"]
    assert c1["new_bootstrap_draw_indices_allowed"] is False
    assert c1["required_match_count"] == 224
    assert c1["shard_count"] == 8
    assert c1["observed_statistic_absolute_tolerance"] == 1e-10

    c2 = config["stage_c2"]
    assert c2["authorized_only_after_c1_pass"] is True
    assert c2["first_new_draw_index"] == 199
    assert c2["maximum_draw_index"] == 9999
    assert c2["maximum_total_attempts"] == 10000
    assert c2["shard_count"] == 16

    assert len(config["source"]["scientific_file_git_blob_sha"]) == 5
    assert not any(config["interpretation_boundary"].values())


def test_stable_shard_assignment_is_deterministic() -> None:
    ids = [f"RUN_{index:03d}" for index in range(224)]
    first = [cont.stable_shard_index(run_id, 8) for run_id in ids]
    second = [cont.stable_shard_index(run_id, 8) for run_id in ids]
    assert first == second
    assert set(first) == set(range(8))

    with pytest.raises(ValueError, match="positive"):
        cont.stable_shard_index("RUN", 0)


def test_bootstrap_draw_regeneration_is_draw_index_deterministic(
    monkeypatch,
) -> None:
    original = object()

    def fake_fit(dataset, restriction, *, scales):
        if dataset is original:
            return SimpleNamespace(
                statistic=1.25,
                restricted=object(),
            )
        return SimpleNamespace(
            statistic=float(dataset.value),
            restricted=object(),
        )

    def fake_simulate(template, fit, *, scales, rng):
        return SimpleNamespace(value=float(rng.random()))

    monkeypatch.setattr(cont, "fit_restriction_pair", fake_fit)
    monkeypatch.setattr(
        cont,
        "simulate_exact_design_under_restriction",
        fake_simulate,
    )
    monkeypatch.setattr(
        cont,
        "_scales",
        lambda config, *, generator: object(),
    )

    run = {
        "restriction": "ADD_RESTRICTION",
        "bootstrap_stream_seed": 987654,
    }
    config = {}
    observed_a, values_a = cont.regenerate_bootstrap_attempt_statistics(
        run,
        original,
        paired_config=config,
        draw_indices=(0, 17, 198),
    )
    observed_b, values_b = cont.regenerate_bootstrap_attempt_statistics(
        run,
        original,
        paired_config=config,
        draw_indices=(0, 17, 198),
    )
    _, values_c = cont.regenerate_bootstrap_attempt_statistics(
        run,
        original,
        paired_config=config,
        draw_indices=(0, 18, 198),
    )

    assert observed_a == observed_b == 1.25
    assert values_a == values_b
    assert values_a[0] == values_c[0]
    assert values_a[2] == values_c[2]
    assert values_a[1] != values_c[1]


def test_stage_c1_reproduces_all_224_and_combines(
    monkeypatch,
) -> None:
    paired, stage_b = fake_payloads()
    config = load_config()
    attempt_values = tuple(
        float(index) / 1000.0 for index in range(199)
    )

    monkeypatch.setattr(
        cont,
        "build_departure_case_map",
        lambda *args, **kwargs: {},
    )
    monkeypatch.setattr(
        cont,
        "regenerate_dataset_for_run",
        lambda *args, **kwargs: object(),
    )
    monkeypatch.setattr(
        cont,
        "dataset_fingerprint",
        lambda dataset: "a" * 64,
    )
    monkeypatch.setattr(
        cont,
        "regenerate_bootstrap_attempt_statistics",
        lambda run, dataset, *, paired_config, draw_indices: (
            float(run["observed_statistic"]),
            attempt_values,
        ),
    )

    partitions = [
        cont.qualify_continuation_partition(
            paired,
            stage_b,
            config,
            {},
            {},
            {},
            {},
            shard_index=shard,
        )
        for shard in range(8)
    ]
    assert sum(
        part["qualified_run_count"] for part in partitions
    ) == 224
    assert all(part["all_selected_runs_pass"] for part in partitions)

    combined = cont.combine_continuation_qualification_partitions(
        partitions,
        config,
    )
    assert combined["qualified_run_count"] == 224
    assert combined["qualification_pass_count"] == 224
    assert combined["qualification_failure_count"] == 0
    assert combined["gate_pass"] is True
    assert combined["next_gate"] == (
        "STAGE_C2_EXACT_CONTINUATION_TO_PROSPECTIVE_CAP_10000"
    )


def test_stage_c1_fails_closed_on_checkpoint_hash_mismatch(
    monkeypatch,
) -> None:
    paired, stage_b = fake_payloads()
    config = load_config()
    target = stage_b["unresolved_run_ids"][0]
    stage_b["stream_checkpoints"][0][
        "attempt_sequence_sha256"
    ] = "b" * 64

    shard = cont.stable_shard_index(target, 8)
    monkeypatch.setattr(
        cont,
        "build_departure_case_map",
        lambda *args, **kwargs: {},
    )

    with pytest.raises(ValueError, match="attempt hash mismatch"):
        cont.qualify_continuation_partition(
            paired,
            stage_b,
            config,
            {},
            {},
            {},
            {},
            shard_index=shard,
        )


def test_stage_c1_gate_stays_closed_on_observed_statistic_drift(
    monkeypatch,
) -> None:
    paired, stage_b = fake_payloads()
    config = load_config()
    attempt_values = tuple(
        float(index) / 1000.0 for index in range(199)
    )

    monkeypatch.setattr(
        cont,
        "build_departure_case_map",
        lambda *args, **kwargs: {},
    )
    monkeypatch.setattr(
        cont,
        "regenerate_dataset_for_run",
        lambda *args, **kwargs: object(),
    )
    monkeypatch.setattr(
        cont,
        "dataset_fingerprint",
        lambda dataset: "a" * 64,
    )
    monkeypatch.setattr(
        cont,
        "regenerate_bootstrap_attempt_statistics",
        lambda run, dataset, *, paired_config, draw_indices: (
            float(run["observed_statistic"]) + 1e-6,
            attempt_values,
        ),
    )

    partitions = [
        cont.qualify_continuation_partition(
            paired,
            stage_b,
            config,
            {},
            {},
            {},
            {},
            shard_index=shard,
        )
        for shard in range(8)
    ]
    combined = cont.combine_continuation_qualification_partitions(
        partitions,
        config,
    )
    assert combined["qualification_pass_count"] == 0
    assert combined["qualification_failure_count"] == 224
    assert combined["gate_pass"] is False
    assert combined["next_gate"] == (
        "BLOCKED_BY_STAGE_C1_REPRODUCTION_FAILURE"
    )


def test_stage_c1_combiner_rejects_missing_or_duplicate_shards() -> None:
    config = load_config()
    base = {
        "continuation_id": config["continuation_id"],
        "status": "NON_AUTHORITATIVE_STAGE_C1_REGENERATION_QUALIFICATION",
        "authoritative": False,
        "shard_count": 8,
        "rows": [],
    }
    parts = []
    for shard in range(8):
        row = copy.deepcopy(base)
        row["shard_index"] = shard
        parts.append(row)

    with pytest.raises(ValueError, match="partition count"):
        cont.combine_continuation_qualification_partitions(
            parts[:-1],
            config,
        )

    duplicate = list(parts)
    duplicate[-1] = copy.deepcopy(parts[0])
    with pytest.raises(ValueError, match="duplicate"):
        cont.combine_continuation_qualification_partitions(
            duplicate,
            config,
        )
