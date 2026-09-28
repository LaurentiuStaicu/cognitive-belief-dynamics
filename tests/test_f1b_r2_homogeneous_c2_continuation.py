from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c2_continuation as c2_module

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c1_exact_replay import (
    canonical_json_sha256,
)
from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c2_continuation import (
    annotate_partition_runtime_cores,
    bind_c2_targets,
    combine_c2_partitions,
    continue_target_stream,
    validate_c2_environment,
    validate_c2_runtime_cores,
    validate_homogeneous_c2_config,
    validate_new_draw_indices,
    validate_retained_c1_result,
    validate_retained_h1_result,
    validate_retained_h2_result,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_homogeneous_c2_continuation_v1.json"
)
H1_RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_homogeneous_paired_h1_qualification_2026-09-28.json"
)
H2_RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_homogeneous_stage_b_rebuild_2026-09-28.json"
)
C1_RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_homogeneous_c1_exact_replay_2026-09-28.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_homogeneous_c2_contract_is_frozen_and_non_authoritative() -> None:
    config = load_config()
    validate_homogeneous_c2_config(config)

    c2 = config["stage_c2"]
    assert config["issue"] == 245
    assert config["candidate_environment"]["value"] == "Haswell"
    assert config["controller"]["prior_total_attempts"] == 199
    assert config["controller"]["maximum_total_attempts"] == 10000
    assert c2["target_stream_count"] == 224
    assert c2["first_new_draw_index"] == 199
    assert c2["maximum_new_draw_index"] == 9999
    assert c2["maximum_total_attempts"] == 10000
    assert c2["shard_count"] == 16
    assert c2["reporting_checkpoints_total_n"] == [
        199,
        499,
        999,
        1999,
        4999,
        10000,
    ]
    assert c2["historical_c2_inheritance_allowed"] is False
    assert not any(config["boundary"].values())


def test_homogeneous_c2_draw_indices_fail_closed() -> None:
    assert validate_new_draw_indices((199,)) == (199,)
    assert validate_new_draw_indices((199, 200, 201)) == (
        199,
        200,
        201,
    )
    assert validate_new_draw_indices(tuple(range(199, 10000)))[-1] == 9999

    with pytest.raises(ValueError, match="start at draw index 199"):
        validate_new_draw_indices((200,))
    with pytest.raises(ValueError, match="contiguous and increasing"):
        validate_new_draw_indices((199, 201))
    with pytest.raises(ValueError, match="exceeds 9999"):
        validate_new_draw_indices(tuple(range(199, 10001)))


def test_homogeneous_c2_contract_mutations_fail_closed() -> None:
    base = load_config()

    mutated = deepcopy(base)
    mutated["stage_c2"]["first_new_draw_index"] = 198
    with pytest.raises(ValueError, match="first new draw index"):
        validate_homogeneous_c2_config(mutated)

    mutated = deepcopy(base)
    mutated["stage_c2"]["maximum_new_draw_index"] = 10000
    with pytest.raises(ValueError, match="maximum new draw index"):
        validate_homogeneous_c2_config(mutated)

    mutated = deepcopy(base)
    mutated["stage_c2"]["stop_on_bootstrap_refit_failure"] = False
    with pytest.raises(ValueError, match="refit failure"):
        validate_homogeneous_c2_config(mutated)

    mutated = deepcopy(base)
    mutated["stage_c2"]["resolved_h2_streams_eligible"] = True
    with pytest.raises(ValueError, match="resolved H2"):
        validate_homogeneous_c2_config(mutated)

    mutated = deepcopy(base)
    mutated["controller"]["maximum_total_attempts"] = 9999
    with pytest.raises(ValueError, match="cap"):
        validate_homogeneous_c2_config(mutated)


def test_homogeneous_c2_environment_and_runtime_core_fail_closed() -> None:
    validate_c2_environment({"OPENBLAS_CORETYPE": "Haswell"})
    with pytest.raises(ValueError, match="requires"):
        validate_c2_environment({})
    with pytest.raises(ValueError, match="requires"):
        validate_c2_environment({"OPENBLAS_CORETYPE": "SkylakeX"})

    validate_c2_runtime_cores(("Haswell", "Haswell"))
    with pytest.raises(ValueError, match="must not be empty"):
        validate_c2_runtime_cores(())
    with pytest.raises(ValueError, match="non-qualified"):
        validate_c2_runtime_cores(("Haswell", "SkylakeX"))


def test_retained_h1_h2_c1_results_match_c2_contract() -> None:
    config = load_config()
    h1 = json.loads(H1_RESULT.read_text(encoding="utf-8"))
    h2 = json.loads(H2_RESULT.read_text(encoding="utf-8"))
    c1 = json.loads(C1_RESULT.read_text(encoding="utf-8"))

    validate_retained_h1_result(h1, config)
    validate_retained_h2_result(h2, config)
    validate_retained_c1_result(c1, config)


def _synthetic_binding_inputs(config: dict) -> tuple[dict, dict, dict, dict]:
    run_ids = [f"run-{index:03d}" for index in range(750)]
    unresolved = run_ids[:224]

    restriction_runs = []
    checkpoints = []
    replay_rows = []
    for index, run_id in enumerate(run_ids):
        attempts = [0.0] * 199
        restriction_runs.append(
            {
                "run_id": run_id,
                "fit_failure": False,
                "bootstrap_attempt_statistics": attempts,
                "dataset_sha256": f"dataset-{index}",
                "dataset_id": f"dataset-id-{index}",
                "bootstrap_stream_seed": index + 1000,
                "observed_statistic": 1.0,
            }
        )
        from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
            canonical_attempt_sequence_sha256,
        )

        attempt_hash = canonical_attempt_sequence_sha256(attempts)
        checkpoints.append(
            {
                "run_id": run_id,
                "dataset_sha256": f"dataset-{index}",
                "observed_statistic": 1.0,
                "attempt_sequence_sha256": attempt_hash,
                "bootstrap_stream_seed": index + 1000,
            }
        )
        is_unresolved = run_id in unresolved
        replay_rows.append(
            {
                "run_id": run_id,
                "decision": None if is_unresolved else "NOT_REJECT_P_GT_ALPHA",
                "status": (
                    "SEQUENTIAL_UNRESOLVED"
                    if is_unresolved
                    else "SEQUENTIAL_DECISION"
                ),
                "terminal_n": 199 if is_unresolved else 10,
                "terminal_sum": 0,
                "failure_n": None,
                "stopping_n": None if is_unresolved else 10,
                "boundary_hit": None if is_unresolved else "UPPER",
                "dataset_sha256": f"dataset-{index}",
                "bootstrap_stream_seed": index + 1000,
                "observed_statistic": 1.0,
                "attempt_sequence_sha256": attempt_hash,
                "full_prefix_sum_199": 0,
                "terminal_lower": -1 if is_unresolved else 0,
                "terminal_upper": 2 if is_unresolved else 1,
            }
        )

    checkpoints.sort(key=lambda row: row["run_id"])
    unresolved_sorted = sorted(unresolved)
    config = deepcopy(config)
    config["stage_b_lineage"]["unresolved_run_ids_sha256"] = (
        canonical_json_sha256(unresolved_sorted)
    )
    config["stage_b_lineage"]["stream_checkpoints_sha256"] = (
        canonical_json_sha256(checkpoints)
    )

    paired_source = {
        "restriction_run_count": 750,
        "restriction_runs": restriction_runs,
    }
    raw_h2 = {
        "status": "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE",
        "authoritative": False,
        "restriction_run_count": 750,
        "bootstrap_refit_failure_count": 0,
        "replay_rows": replay_rows,
        "stream_checkpoints": checkpoints,
    }
    c1_rows = []
    checkpoint_map = {
        row["run_id"]: row for row in checkpoints
    }
    for run_id in unresolved_sorted:
        c1_rows.append(
            {
                "run_id": run_id,
                "homogeneous_c1_qualification_pass": True,
                "dataset_fingerprint_match": True,
                "observed_statistic_match": True,
                "attempt_sequence_sha256_match": True,
                "bootstrap_refit_failure_free": True,
                "retained_attempt_sequence_sha256": checkpoint_map[
                    run_id
                ]["attempt_sequence_sha256"],
                "regenerated_attempt_sequence_sha256": checkpoint_map[
                    run_id
                ]["attempt_sequence_sha256"],
            }
        )
    c1_combined = {
        "qualification_id": "F1B.R2.HOMOGENEOUS_C1_EXACT_REPLAY.V1",
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_C1_EXACT_REPLAY_RESULT",
        "authoritative": False,
        "gate_pass": True,
        "qualified_run_count": 224,
        "qualification_pass_count": 224,
        "exact_observed_statistic_count": 224,
        "bootstrap_refit_failure_free_count": 224,
        "rows": c1_rows,
    }
    return config, paired_source, raw_h2, c1_combined


def test_c2_binding_targets_exactly_h2_unresolved_c1_passes() -> None:
    config, paired_source, raw_h2, c1_combined = (
        _synthetic_binding_inputs(load_config())
    )
    binding = bind_c2_targets(
        paired_source,
        raw_h2,
        c1_combined,
        config,
    )
    assert len(binding["target_run_ids"]) == 224
    assert len(binding["targets"]) == 224
    assert binding["target_run_ids"][0] == "run-000"
    assert binding["target_run_ids"][-1] == "run-223"


def _synthetic_c2_row(run_id: str, index: int) -> dict:
    return {
        "run_id": run_id,
        "restriction": "ADD_RESTRICTION",
        "role": "TEST_ROLE",
        "axis": None,
        "target_mean_bernoulli_kl": 0.0,
        "sign": None,
        "anchor_id": "TEST_ANCHOR",
        "evaluation_replicate": index % 10,
        "new_attempt_count": 1,
        "new_successful_fit_count": 1,
        "status": "SEQUENTIAL_DECISION",
        "decision": "NOT_REJECT_P_GT_ALPHA",
        "stopping_n": 200,
        "failure_n": None,
    }


def test_c2_combiner_requires_all_16_shards_and_224_unique_targets() -> None:
    config = load_config()
    run_ids = [f"target-{index:03d}" for index in range(224)]
    config["stage_b_lineage"]["unresolved_run_ids_sha256"] = (
        canonical_json_sha256(sorted(run_ids))
    )
    partitions = [
        {
            "continuation_id": config["continuation_id"],
            "status": "NON_AUTHORITATIVE_HOMOGENEOUS_C2_PARTITION",
            "authoritative": False,
            "shard_index": shard,
            "shard_count": 16,
            "target_run_ids_sha256": config["stage_b_lineage"][
                "unresolved_run_ids_sha256"
            ],
            "rows": [],
        }
        for shard in range(16)
    ]
    for index, run_id in enumerate(run_ids):
        partitions[index % 16]["rows"].append(
            _synthetic_c2_row(run_id, index)
        )
    for partition in partitions:
        annotate_partition_runtime_cores(
            partition,
            ("Haswell", "Haswell"),
        )

    combined = combine_c2_partitions(partitions, config)
    assert combined["target_stream_count"] == 224
    assert combined["continued_stream_count"] == 224
    assert combined["global_summary"]["newly_resolved_count"] == 224
    assert combined["reporting_checkpoints"]["199"][
        "cumulative_newly_resolved_count"
    ] == 0
    assert combined["reporting_checkpoints"]["499"][
        "cumulative_newly_resolved_count"
    ] == 224

    broken = deepcopy(partitions)
    broken[1]["shard_index"] = 0
    with pytest.raises(ValueError, match="duplicate"):
        combine_c2_partitions(broken, config)


def test_c2_tests_do_not_authorize_execution_in_contract() -> None:
    config = load_config()
    assert config["stage_c2"]["execution_requires_merged_gate"] is True
    assert config["boundary"]["stage_c2_executed"] is False


def test_c2_binding_rejects_h1_h2_stream_seed_drift() -> None:
    config, paired_source, raw_h2, c1_combined = (
        _synthetic_binding_inputs(load_config())
    )
    target = raw_h2["stream_checkpoints"][0]
    target["bootstrap_stream_seed"] += 1
    config["stage_b_lineage"]["stream_checkpoints_sha256"] = (
        canonical_json_sha256(
            sorted(
                raw_h2["stream_checkpoints"],
                key=lambda row: str(row["run_id"]),
            )
        )
    )
    with pytest.raises(ValueError, match="stream-seed mismatch"):
        bind_c2_targets(
            paired_source,
            raw_h2,
            c1_combined,
            config,
        )


def _single_target_for_continuation() -> dict:
    from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
        canonical_attempt_sequence_sha256,
    )

    attempts = [0.0] * 199
    attempt_hash = canonical_attempt_sequence_sha256(attempts)
    run = {
        "run_id": "run-target",
        "dataset_id": "dataset-id",
        "dataset_sha256": "dataset-sha",
        "bootstrap_stream_seed": 12345,
        "observed_statistic": 1.0,
        "bootstrap_attempt_statistics": attempts,
        "restriction": "ADD_RESTRICTION",
        "identity": "identity",
        "identity_type": "NULL",
        "role": "role",
        "anchor_id": "anchor",
        "axis": None,
        "sign": None,
        "target_mean_bernoulli_kl": 0.0,
        "evaluation_replicate": 0,
    }
    return {
        "run_id": "run-target",
        "source_run": run,
        "checkpoint": {
            "run_id": "run-target",
            "dataset_sha256": "dataset-sha",
            "bootstrap_stream_seed": 12345,
            "observed_statistic": 1.0,
            "attempt_sequence_sha256": attempt_hash,
        },
        "h2_replay_row": {
            "run_id": "run-target",
            "decision": None,
            "status": "SEQUENTIAL_UNRESOLVED",
            "terminal_n": 199,
            "terminal_sum": 0,
            "full_prefix_sum_199": 0,
            "terminal_lower": -1,
            "terminal_upper": 2,
            "failure_n": None,
            "stopping_n": None,
            "boundary_hit": None,
        },
        "c1_row": {
            "retained_attempt_sequence_sha256": attempt_hash,
        },
    }


class _SyntheticBoundaries:
    def row(self, n: int):
        if int(n) == 199:
            return SimpleNamespace(lower=-1, upper=2)
        return SimpleNamespace(lower=0, upper=2)


def test_c2_stream_stops_immediately_on_first_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"fit": 0, "simulate": 0}

    monkeypatch.setattr(
        c2_module,
        "regenerate_dataset_for_run",
        lambda *args, **kwargs: object(),
    )
    monkeypatch.setattr(
        c2_module,
        "dataset_fingerprint",
        lambda dataset: "dataset-sha",
    )
    monkeypatch.setattr(
        c2_module,
        "_scales",
        lambda *args, **kwargs: object(),
    )

    def fake_fit(*args, **kwargs):
        calls["fit"] += 1
        if calls["fit"] == 1:
            return SimpleNamespace(statistic=1.0, restricted=object())
        if calls["fit"] == 2:
            return SimpleNamespace(statistic=0.0, restricted=object())
        raise AssertionError("C2 requested a fit after terminal boundary")

    def fake_simulate(*args, **kwargs):
        calls["simulate"] += 1
        if calls["simulate"] > 1:
            raise AssertionError("C2 generated a draw after terminal boundary")
        return object()

    monkeypatch.setattr(c2_module, "fit_restriction_pair", fake_fit)
    monkeypatch.setattr(
        c2_module,
        "simulate_exact_design_under_restriction",
        fake_simulate,
    )

    result = continue_target_stream(
        _single_target_for_continuation(),
        paired_config={},
        departure_cases={},
        boundaries=_SyntheticBoundaries(),
        config=load_config(),
    )

    assert result["status"] == "SEQUENTIAL_DECISION"
    assert result["decision"] == "REJECT_P_LE_ALPHA"
    assert result["boundary_hit"] == "LOWER"
    assert result["stopping_n"] == 200
    assert result["last_new_draw_index"] == 199
    assert result["new_attempt_count"] == 1
    assert result["new_successful_fit_count"] == 1
    assert calls == {"fit": 2, "simulate": 1}


def test_c2_stream_stops_immediately_on_first_refit_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"fit": 0, "simulate": 0}

    monkeypatch.setattr(
        c2_module,
        "regenerate_dataset_for_run",
        lambda *args, **kwargs: object(),
    )
    monkeypatch.setattr(
        c2_module,
        "dataset_fingerprint",
        lambda dataset: "dataset-sha",
    )
    monkeypatch.setattr(
        c2_module,
        "_scales",
        lambda *args, **kwargs: object(),
    )

    def fake_fit(*args, **kwargs):
        calls["fit"] += 1
        if calls["fit"] == 1:
            return SimpleNamespace(statistic=1.0, restricted=object())
        if calls["fit"] == 2:
            raise RuntimeError("synthetic bootstrap refit failure")
        raise AssertionError("C2 requested a fit after refit failure")

    def fake_simulate(*args, **kwargs):
        calls["simulate"] += 1
        if calls["simulate"] > 1:
            raise AssertionError("C2 generated a draw after refit failure")
        return object()

    monkeypatch.setattr(c2_module, "fit_restriction_pair", fake_fit)
    monkeypatch.setattr(
        c2_module,
        "simulate_exact_design_under_restriction",
        fake_simulate,
    )

    result = continue_target_stream(
        _single_target_for_continuation(),
        paired_config={},
        departure_cases={},
        boundaries=_SyntheticBoundaries(),
        config=load_config(),
    )

    assert result["status"] == "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    assert result["decision"] is None
    assert result["failure_n"] == 200
    assert result["failure_draw_index"] == 199
    assert result["last_new_draw_index"] == 199
    assert result["new_attempt_count"] == 1
    assert result["new_successful_fit_count"] == 0
    assert calls == {"fit": 2, "simulate": 1}
