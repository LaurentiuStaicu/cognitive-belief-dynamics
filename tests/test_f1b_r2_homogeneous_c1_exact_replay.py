from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c1_exact_replay import (
    build_effective_continuation,
    canonical_json_sha256,
    derive_h2_stage_b_binding,
    validate_c1_environment,
    validate_c1_runtime_cores,
    validate_homogeneous_c1_config,
    validate_retained_h1_result,
    validate_retained_h2_result,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_homogeneous_c1_exact_replay_v1.json"
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


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_homogeneous_c1_contract_is_frozen_and_non_authoritative() -> None:
    config = load_config()
    validate_homogeneous_c1_config(config)

    assert config["issue"] == 241
    assert config["candidate_environment"]["value"] == "Haswell"
    assert config["stage_c1"]["regenerate_draw_indices"] == [0, 198]
    assert config["stage_c1"]["regenerate_complete_prefix"] is True
    assert config["stage_c1"]["maximum_draw_index"] == 198
    assert config["stage_c1"]["required_match_count"] == 224
    assert config["stage_c1"]["required_bootstrap_refit_failure_count"] == 0
    assert not any(config["boundary"].values())


def test_homogeneous_c1_draw_and_exact_match_guards_fail_closed() -> None:
    base = load_config()

    mutated = deepcopy(base)
    mutated["stage_c1"]["regenerate_draw_indices"] = [0, 199]
    with pytest.raises(ValueError, match="draw endpoints"):
        validate_homogeneous_c1_config(mutated)

    mutated = deepcopy(base)
    mutated["stage_c1"]["regenerate_complete_prefix"] = False
    with pytest.raises(ValueError, match="complete prefix"):
        validate_homogeneous_c1_config(mutated)

    mutated = deepcopy(base)
    mutated["stage_c1"]["required_dataset_fingerprint_match"] = False
    with pytest.raises(ValueError, match="dataset exact-match"):
        validate_homogeneous_c1_config(mutated)

    mutated = deepcopy(base)
    mutated["stage_c1"]["required_attempt_sequence_sha256_match"] = False
    with pytest.raises(ValueError, match="attempt-hash"):
        validate_homogeneous_c1_config(mutated)


def test_homogeneous_c1_environment_and_runtime_core_fail_closed() -> None:
    validate_c1_environment({"OPENBLAS_CORETYPE": "Haswell"})
    with pytest.raises(ValueError, match="requires"):
        validate_c1_environment({})
    with pytest.raises(ValueError, match="requires"):
        validate_c1_environment({"OPENBLAS_CORETYPE": "SkylakeX"})

    validate_c1_runtime_cores(("Haswell", "Haswell"))
    with pytest.raises(ValueError, match="must not be empty"):
        validate_c1_runtime_cores(())
    with pytest.raises(ValueError, match="non-qualified"):
        validate_c1_runtime_cores(("Haswell", "SkylakeX"))


def test_retained_h1_and_h2_results_match_new_c1_contract() -> None:
    config = load_config()
    h1 = json.loads(H1_RESULT.read_text(encoding="utf-8"))
    h2 = json.loads(H2_RESULT.read_text(encoding="utf-8"))

    validate_retained_h1_result(h1, config)
    validate_retained_h2_result(h2, config)


def test_effective_continuation_preserves_old_qualification_invariants() -> None:
    effective = build_effective_continuation(load_config())
    assert effective["status"] == (
        "NON_AUTHORITATIVE_RESAMPLING_RISK_CONTINUATION_DESIGN"
    )
    assert effective["controller"] == {
        "alpha": 0.05,
        "epsilon": 0.001,
        "halfspend": 1000.0,
        "prior_max_attempts": 199,
        "maximum_total_attempts": 10000,
    }
    assert effective["source"][
        "retained_stage_b_expected_unresolved_count"
    ] == 224
    assert effective["stage_c1"][
        "new_bootstrap_draw_indices_allowed"
    ] is False
    assert effective["stage_c1"]["required_match_count"] == 224
    assert effective["stage_c1"]["shard_count"] == 8


def test_h2_binding_derives_unresolved_ids_and_checkpoint_digest() -> None:
    config = load_config()
    synthetic = {
        "status": "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE",
        "authoritative": False,
        "restriction_run_count": 2,
        "bootstrap_refit_failure_count": 0,
        "replay_rows": [
            {"run_id": "run-b", "decision": None},
            {"run_id": "run-a", "decision": "NOT_REJECT_P_GT_ALPHA"},
        ],
        "stream_checkpoints": [
            {
                "run_id": "run-b",
                "dataset_sha256": "b",
                "observed_statistic": 2.0,
                "attempt_sequence_sha256": "bb",
            },
            {
                "run_id": "run-a",
                "dataset_sha256": "a",
                "observed_statistic": 1.0,
                "attempt_sequence_sha256": "aa",
            },
        ],
    }
    checkpoints = sorted(
        synthetic["stream_checkpoints"],
        key=lambda row: row["run_id"],
    )
    config["stage_b_lineage"]["expected_restriction_runs"] = 2
    config["stage_b_lineage"]["expected_stream_checkpoints"] = 2
    config["stage_b_lineage"]["expected_unresolved_count"] = 1
    config["stage_b_lineage"]["unresolved_run_ids_sha256"] = (
        canonical_json_sha256(["run-b"])
    )
    config["stage_b_lineage"]["stream_checkpoints_sha256"] = (
        canonical_json_sha256(checkpoints)
    )

    binding = derive_h2_stage_b_binding(synthetic, config)
    assert binding["unresolved_run_ids"] == ["run-b"]
    assert [row["run_id"] for row in binding["stream_checkpoints"]] == [
        "run-a",
        "run-b",
    ]


def test_canonical_json_sha256_matches_h2_canonicalization() -> None:
    value = ["a", "b", {"x": 1, "y": 2}]
    expected = hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    assert canonical_json_sha256(value) == expected


def test_frozen_input_sha256_values_match_repository_files() -> None:
    config = load_config()
    for label, spec in config["frozen_inputs"].items():
        path = ROOT / spec["path"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == spec["sha256"], (
            f"{label} SHA-256 changed: {actual} != {spec['sha256']}"
        )


def test_old_qualification_implementation_is_pinned() -> None:
    config = load_config()
    assert config["protected_qualification_file_git_blob_sha"] == {
        "src/cognitive_epistemic_model/calibration/"
        "f1b_r2_resampling_risk_continuation.py": (
            "dda992b4988f2319cddbcf2bdc628ddc645f0ca2"
        )
    }
