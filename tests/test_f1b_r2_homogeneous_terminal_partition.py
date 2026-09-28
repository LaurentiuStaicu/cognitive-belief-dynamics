from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_terminal_partition import (
    EXPECTED_ROLES,
    aggregate_terminal_partition,
    canonical_json_sha256,
    compose_terminal_partition,
    validate_terminal_partition_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    ROOT / "model/benchmarks/f1b_r2_homogeneous_terminal_partition_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def test_terminal_partition_config_is_frozen() -> None:
    config = load_config()
    validate_terminal_partition_config(config)
    assert set(config["semantic_roles"]) == EXPECTED_ROLES
    assert config["execution_boundary"] == {
        "new_bootstrap_draws_allowed": False,
        "cap_extension_allowed": False,
        "controller_retuning_allowed": False,
        "unresolved_imputation_allowed": False,
        "scientific_model_change_allowed": False,
        "power_claim_allowed": False,
        "authoritative_core_grid_freeze_allowed": False,
        "human_n_freeze_allowed": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_all_five_role_semantics_are_explicit() -> None:
    config = load_config()
    roles = config["semantic_roles"]
    assert roles["CBD_NULL_FALSE_REJECTION"]["expected_decision"] == (
        "NOT_REJECT_P_GT_ALPHA"
    )
    assert roles["ADD_NULL_FALSE_REJECTION"]["expected_decision"] == (
        "NOT_REJECT_P_GT_ALPHA"
    )
    assert roles["CBD_DEPARTURE_DETECTION"]["expected_decision"] == (
        "REJECT_P_LE_ALPHA"
    )
    assert roles["ADD_SPECIFICITY_NEGATIVE_CONTROL"]["expected_decision"] == (
        "NOT_REJECT_P_GT_ALPHA"
    )
    assert roles["ADD_DEPARTURE_DIAGNOSTIC"]["expected_decision"] == (
        "REJECT_P_LE_ALPHA"
    )


def test_canonical_json_sha256_is_compact_and_sorted() -> None:
    value = ["b", {"y": 2, "x": 1}]
    expected = hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    assert canonical_json_sha256(value) == expected


def test_config_rejects_missing_add_null_role() -> None:
    config = load_config()
    del config["semantic_roles"]["ADD_NULL_FALSE_REJECTION"]
    with pytest.raises(ValueError, match="semantic-role set"):
        validate_terminal_partition_config(config)


def test_config_rejects_cap_extension() -> None:
    config = load_config()
    config["execution_boundary"]["cap_extension_allowed"] = True
    with pytest.raises(ValueError, match="boundary weakened"):
        validate_terminal_partition_config(config)


def _identity(run_id: str, role: str, restriction: str) -> dict:
    return {
        "run_id": run_id,
        "dataset_id": "dataset-" + run_id,
        "dataset_sha256": "d" * 64,
        "bootstrap_stream_seed": 100,
        "identity": "identity-" + run_id,
        "identity_type": "NULL" if "NULL" in role else "DEPARTURE",
        "restriction": restriction,
        "role": role,
        "anchor_id": "anchor",
        "axis": None if "NULL" in role else "axis",
        "sign": None if "NULL" in role else 1,
        "target_mean_bernoulli_kl": 0.0 if "NULL" in role else 0.001,
        "evaluation_replicate": 0,
    }


def test_semantic_direction_annotations_cover_null_and_departure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import cognitive_epistemic_model.calibration.f1b_r2_homogeneous_terminal_partition as module

    config = load_config()
    monkeypatch.setattr(module, "EXPECTED_TOTAL", 5)
    monkeypatch.setattr(module, "EXPECTED_H2_RESOLVED", 3)
    monkeypatch.setattr(module, "EXPECTED_C2_TARGETS", 2)
    monkeypatch.setattr(module, "EXPECTED_C2_RESOLVED", 1)
    monkeypatch.setattr(module, "EXPECTED_UNRESOLVED_AT_CAP", 1)

    config["h2_stage_b"]["expected_run_count"] = 5
    config["h2_stage_b"]["expected_resolved_count"] = 3
    config["h2_stage_b"]["expected_unresolved_count"] = 2
    config["c2_continuation"]["expected_target_count"] = 2
    config["c2_continuation"]["expected_newly_resolved_count"] = 1
    config["c2_continuation"]["expected_unresolved_at_cap_count"] = 1
    config["terminal_partition"]["expected_total_run_count"] = 5
    config["terminal_partition"]["expected_terminal_decision_count"] = 4
    config["terminal_partition"]["expected_unresolved_at_cap_count"] = 1
    config["terminal_partition"]["h2_resolved_source_count"] = 3
    config["terminal_partition"]["c2_resolved_source_count"] = 1
    config["terminal_partition"]["c2_unresolved_source_count"] = 1

    specs = [
        ("a", "CBD_NULL_FALSE_REJECTION", "CBD_COMPLEMENT_RESTRICTION"),
        ("b", "ADD_NULL_FALSE_REJECTION", "ADD_RESTRICTION"),
        ("c", "CBD_DEPARTURE_DETECTION", "CBD_COMPLEMENT_RESTRICTION"),
        ("d", "ADD_SPECIFICITY_NEGATIVE_CONTROL", "ADD_RESTRICTION"),
        ("e", "ADD_DEPARTURE_DIAGNOSTIC", "ADD_RESTRICTION"),
    ]
    h2_rows = []
    checkpoints = []
    for index, spec in enumerate(specs):
        row = _identity(*spec)
        decision = (
            "NOT_REJECT_P_GT_ALPHA"
            if index in (0, 1)
            else "REJECT_P_LE_ALPHA"
            if index == 2
            else None
        )
        h2_rows.append(
            {
                **row,
                "attempt_sequence_sha256": str(index) * 64,
                "observed_statistic": 1.0,
                "decision": decision,
                "status": (
                    "SEQUENTIAL_DECISION"
                    if decision is not None
                    else "SEQUENTIAL_UNRESOLVED"
                ),
                "stopping_n": 100 if decision is not None else None,
                "stopping_sum": 10 if decision is not None else None,
                "boundary_hit": "UPPER" if decision is not None else None,
                "failure_n": None,
                "terminal_n": 100 if decision is not None else 199,
                "terminal_sum": 10,
                "terminal_lower": 1,
                "terminal_upper": 20,
            }
        )
        checkpoints.append({"run_id": spec[0]})

    unresolved_ids = ["d", "e"]
    config["h2_stage_b"]["unresolved_run_ids_sha256"] = (
        canonical_json_sha256(unresolved_ids)
    )

    h2 = {
        "status": "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE",
        "authoritative": False,
        "restriction_run_count": 5,
        "bootstrap_refit_failure_count": 0,
        "replay_rows": h2_rows,
        "stream_checkpoints": checkpoints,
    }

    c2_rows = []
    for run_id, decision, status in (
        ("d", "NOT_REJECT_P_GT_ALPHA", "SEQUENTIAL_DECISION"),
        ("e", None, "SEQUENTIAL_UNRESOLVED_AT_CAP"),
    ):
        source = next(row for row in h2_rows if row["run_id"] == run_id)
        c2_rows.append(
            {
                **{
                    key: source[key]
                    for key in (
                        "run_id",
                        "dataset_id",
                        "dataset_sha256",
                        "bootstrap_stream_seed",
                        "identity",
                        "identity_type",
                        "restriction",
                        "role",
                        "anchor_id",
                        "axis",
                        "sign",
                        "target_mean_bernoulli_kl",
                        "evaluation_replicate",
                    )
                },
                "retained_observed_statistic": 1.0,
                "retained_prefix_sha256": source[
                    "attempt_sequence_sha256"
                ],
                "status": status,
                "decision": decision,
                "stopping_n": 500 if decision is not None else None,
                "stopping_sum": 20 if decision is not None else None,
                "boundary_hit": "UPPER" if decision is not None else None,
                "terminal_n": 500 if decision is not None else 10000,
                "terminal_sum": 20,
                "terminal_lower": 10,
                "terminal_upper": 30,
                "failure_draw_index": None,
            }
        )

    config["c2_continuation"]["unresolved_at_cap_run_ids_sha256"] = (
        canonical_json_sha256(["e"])
    )
    c2 = {
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_C2_CONTINUATION_RESULT",
        "authoritative": False,
        "target_stream_count": 2,
        "continued_stream_count": 2,
        "rows": c2_rows,
    }

    result = compose_terminal_partition(h2, c2, config)
    rows = {row["run_id"]: row for row in result["rows"]}
    assert rows["a"]["role_direction_status"] == "EXPECTED_DIRECTION"
    assert rows["b"]["role_direction_status"] == "EXPECTED_DIRECTION"
    assert rows["c"]["role_direction_status"] == "EXPECTED_DIRECTION"
    assert rows["d"]["role_direction_status"] == "EXPECTED_DIRECTION"
    assert rows["e"]["role_direction_status"] == "UNRESOLVED_AT_CAP"

    aggregate = aggregate_terminal_partition(result, config)
    assert aggregate["global_summary"]["run_count"] == 5
    assert aggregate["global_summary"]["unresolved_at_cap_count"] == 1
    assert aggregate["unresolved_at_cap"]["run_ids_sha256"] == (
        canonical_json_sha256(["e"])
    )
