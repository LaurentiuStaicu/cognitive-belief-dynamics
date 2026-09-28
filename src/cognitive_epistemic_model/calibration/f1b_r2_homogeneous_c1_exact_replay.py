from __future__ import annotations

import hashlib
import json
from typing import Mapping

from .f1b_r2_openblas_lineage import (
    EXPECTED_OPENBLAS_CORE,
    MAX_RETAINED_DRAW_INDEX,
    validate_candidate_environment,
    validate_runtime_cores,
)
from .f1b_r2_resampling_risk_continuation import (
    combine_continuation_qualification_partitions,
)


HOMOGENEOUS_C1_ID = "F1B.R2.HOMOGENEOUS_C1_EXACT_REPLAY.V1"
HOMOGENEOUS_C1_STATUS = (
    "NON_AUTHORITATIVE_HOMOGENEOUS_C1_EXACT_REPLAY_DESIGN"
)
EXPECTED_UNRESOLVED_COUNT = 224
EXPECTED_STAGE_B_STREAM_COUNT = 750
EXPECTED_H1_RESTRICTION_RUNS = 750
EXPECTED_CHECKPOINT_COUNT = 750
EXPECTED_SHARD_COUNT = 8


def canonical_json_sha256(value) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_homogeneous_c1_config(config: dict) -> None:
    if config["qualification_id"] != HOMOGENEOUS_C1_ID:
        raise ValueError("homogeneous C1 identity changed")
    if config["status"] != HOMOGENEOUS_C1_STATUS:
        raise ValueError("unsupported homogeneous C1 status")
    if int(config["issue"]) != 241:
        raise ValueError("homogeneous C1 issue changed")

    candidate = config["candidate_environment"]
    if candidate["variable"] != "OPENBLAS_CORETYPE":
        raise ValueError("homogeneous C1 environment variable changed")
    if candidate["value"] != EXPECTED_OPENBLAS_CORE:
        raise ValueError("homogeneous C1 OpenBLAS core changed")
    if candidate["must_be_set_before_python_start"] is not True:
        raise ValueError("OpenBLAS core must be set before Python startup")
    if candidate["runtime_core_confirmation_required"] is not True:
        raise ValueError("homogeneous C1 runtime core confirmation is required")

    source = config["source_lineage"]
    if source["lineage_id"] != (
        "F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1"
    ):
        raise ValueError("homogeneous C1 H1 lineage changed")
    if int(source["expected_restriction_runs"]) != EXPECTED_H1_RESTRICTION_RUNS:
        raise ValueError("homogeneous C1 H1 run count changed")
    if int(source["expected_attempts_per_run"]) != 199:
        raise ValueError("homogeneous C1 H1 attempt horizon changed")
    if int(source["expected_bootstrap_fit_failures"]) != 0:
        raise ValueError("homogeneous C1 H1 fit-failure expectation changed")

    stage_b = config["stage_b_lineage"]
    if int(stage_b["expected_restriction_runs"]) != EXPECTED_STAGE_B_STREAM_COUNT:
        raise ValueError("homogeneous C1 H2 run count changed")
    if int(stage_b["expected_stream_checkpoints"]) != EXPECTED_CHECKPOINT_COUNT:
        raise ValueError("homogeneous C1 H2 checkpoint count changed")
    if int(stage_b["expected_unresolved_count"]) != EXPECTED_UNRESOLVED_COUNT:
        raise ValueError("homogeneous C1 unresolved count changed")

    controller = config["controller"]
    if float(controller["alpha"]) != 0.05:
        raise ValueError("homogeneous C1 alpha changed")
    if float(controller["epsilon"]) != 0.001:
        raise ValueError("homogeneous C1 epsilon changed")
    if float(controller["halfspend"]) != 1000.0:
        raise ValueError("homogeneous C1 halfspend changed")
    if int(controller["prior_max_attempts"]) != 199:
        raise ValueError("homogeneous C1 prior horizon changed")
    if int(controller["maximum_total_attempts"]) != 10000:
        raise ValueError("homogeneous C1 prospective cap changed")
    if controller["controller_changed"] is not False:
        raise ValueError("homogeneous C1 controller must remain unchanged")

    c1 = config["stage_c1"]
    if c1["new_bootstrap_draw_indices_allowed"] is not False:
        raise ValueError("homogeneous C1 cannot authorize new bootstrap draws")
    if int(c1["maximum_draw_index"]) != MAX_RETAINED_DRAW_INDEX:
        raise ValueError("homogeneous C1 maximum draw index changed")
    if float(c1["observed_statistic_absolute_tolerance"]) != 1e-10:
        raise ValueError("homogeneous C1 observed-statistic tolerance changed")
    if int(c1["required_bootstrap_refit_failure_count"]) != 0:
        raise ValueError("homogeneous C1 refit-failure requirement changed")
    if int(c1["required_match_count"]) != EXPECTED_UNRESOLVED_COUNT:
        raise ValueError("homogeneous C1 match count changed")
    if int(c1["shard_count"]) != EXPECTED_SHARD_COUNT:
        raise ValueError("homogeneous C1 shard count changed")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("homogeneous C1 interpretation boundary weakened")


def validate_c1_environment(
    environment: Mapping[str, str | None] | None = None,
) -> None:
    validate_candidate_environment(
        environment,
        expected_core=EXPECTED_OPENBLAS_CORE,
    )


def validate_c1_runtime_cores(cores: tuple[str, ...]) -> None:
    validate_runtime_cores(
        cores,
        expected_core=EXPECTED_OPENBLAS_CORE,
    )


def validate_retained_h1_result(h1_result: dict, config: dict) -> None:
    source = config["source_lineage"]
    if h1_result["lineage_id"] != source["lineage_id"]:
        raise ValueError("homogeneous C1 retained H1 lineage mismatch")
    if h1_result["status"] != (
        "NON_AUTHORITATIVE_H1_HOMOGENEOUS_PAIRED_SOURCE_QUALIFIED_RETAINED"
    ):
        raise ValueError("homogeneous C1 requires retained qualified H1 source")
    if h1_result["authoritative"] is not False:
        raise ValueError("homogeneous C1 H1 source became authoritative")

    decision = h1_result["decision"]
    if decision["h1_full_homogeneous_source_generation_pass"] is not True:
        raise ValueError("homogeneous C1 H1 generation did not pass")
    if decision["h1_independent_replay_qualification_pass"] is not True:
        raise ValueError("homogeneous C1 H1 replay did not pass")

    combined = h1_result["combined_source"]
    if int(combined["artifact_id"]) != int(source["artifact_id"]):
        raise ValueError("homogeneous C1 H1 artifact mismatch")
    if str(combined["combined_json_sha256"]) != str(
        source["combined_json_sha256"]
    ):
        raise ValueError("homogeneous C1 H1 source SHA-256 mismatch")
    if int(combined["combined_json_size_bytes"]) != int(
        source["combined_json_size_bytes"]
    ):
        raise ValueError("homogeneous C1 H1 source size mismatch")


def validate_retained_h2_result(h2_result: dict, config: dict) -> None:
    stage_b = config["stage_b_lineage"]
    if h2_result["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_STAGE_B_REBUILD_COMPLETE_RETAINED"
    ):
        raise ValueError("homogeneous C1 requires retained H2 result")
    if h2_result["authoritative"] is not False:
        raise ValueError("homogeneous C1 H2 result became authoritative")
    if h2_result["decision"]["h2_stage_b_rebuild_pass"] is not True:
        raise ValueError("homogeneous C1 H2 rebuild did not pass")
    if h2_result["decision"]["historical_stage_b_inherited"] is not False:
        raise ValueError("homogeneous C1 cannot inherit historical Stage-B")

    execution = h2_result["execution"]
    if int(execution["result_artifact_id"]) != int(stage_b["artifact_id"]):
        raise ValueError("homogeneous C1 H2 artifact mismatch")
    if str(execution["raw_replay_json_sha256"]) != str(
        stage_b["raw_json_sha256"]
    ):
        raise ValueError("homogeneous C1 H2 raw JSON SHA-256 mismatch")
    if int(execution["raw_replay_json_size_bytes"]) != int(
        stage_b["raw_json_size_bytes"]
    ):
        raise ValueError("homogeneous C1 H2 raw JSON size mismatch")

    integrity = h2_result["integrity"]
    if int(integrity["restriction_run_count"]) != int(
        stage_b["expected_restriction_runs"]
    ):
        raise ValueError("homogeneous C1 H2 restriction count mismatch")
    if int(integrity["stream_checkpoint_count"]) != int(
        stage_b["expected_stream_checkpoints"]
    ):
        raise ValueError("homogeneous C1 H2 checkpoint count mismatch")
    if int(integrity["unresolved_run_count"]) != int(
        stage_b["expected_unresolved_count"]
    ):
        raise ValueError("homogeneous C1 H2 unresolved count mismatch")
    if str(integrity["unresolved_run_ids_sha256"]) != str(
        stage_b["unresolved_run_ids_sha256"]
    ):
        raise ValueError("homogeneous C1 H2 unresolved digest mismatch")
    if str(integrity["homogeneous_stream_checkpoints_sha256"]) != str(
        stage_b["stream_checkpoints_sha256"]
    ):
        raise ValueError("homogeneous C1 H2 checkpoint digest mismatch")


def derive_h2_stage_b_binding(raw_h2: dict, config: dict) -> dict:
    stage_b = config["stage_b_lineage"]
    if raw_h2["status"] != "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE":
        raise ValueError("homogeneous C1 raw H2 status changed")
    if raw_h2["authoritative"] is not False:
        raise ValueError("homogeneous C1 raw H2 became authoritative")
    if int(raw_h2["restriction_run_count"]) != int(
        stage_b["expected_restriction_runs"]
    ):
        raise ValueError("homogeneous C1 raw H2 restriction count changed")
    if int(raw_h2["bootstrap_refit_failure_count"]) != 0:
        raise ValueError("homogeneous C1 raw H2 contains refit failures")

    rows = list(raw_h2["replay_rows"])
    checkpoints = sorted(
        list(raw_h2["stream_checkpoints"]),
        key=lambda row: str(row["run_id"]),
    )
    if len(rows) != int(stage_b["expected_restriction_runs"]):
        raise ValueError("homogeneous C1 raw H2 replay-row count changed")
    if len(checkpoints) != int(stage_b["expected_stream_checkpoints"]):
        raise ValueError("homogeneous C1 raw H2 checkpoint count changed")

    checkpoint_ids = [str(row["run_id"]) for row in checkpoints]
    if len(checkpoint_ids) != len(set(checkpoint_ids)):
        raise ValueError("homogeneous C1 raw H2 checkpoint IDs are not unique")

    checkpoint_hash = canonical_json_sha256(checkpoints)
    if checkpoint_hash != str(stage_b["stream_checkpoints_sha256"]):
        raise ValueError("homogeneous C1 raw H2 checkpoint digest mismatch")

    unresolved = sorted(
        str(row["run_id"])
        for row in rows
        if row["decision"] is None
    )
    if len(unresolved) != int(stage_b["expected_unresolved_count"]):
        raise ValueError("homogeneous C1 raw H2 unresolved count changed")
    if len(unresolved) != len(set(unresolved)):
        raise ValueError("homogeneous C1 raw H2 unresolved IDs are not unique")

    unresolved_hash = canonical_json_sha256(unresolved)
    if unresolved_hash != str(stage_b["unresolved_run_ids_sha256"]):
        raise ValueError("homogeneous C1 raw H2 unresolved digest mismatch")

    return {
        "unresolved_run_ids": unresolved,
        "stream_checkpoints": checkpoints,
        "integrity": {
            "stream_checkpoint_count": len(checkpoints),
            "unresolved_run_count": len(unresolved),
            "unresolved_run_ids_sha256": unresolved_hash,
            "stream_checkpoints_sha256": checkpoint_hash,
        },
    }


def build_effective_continuation(config: dict) -> dict:
    validate_homogeneous_c1_config(config)
    c1 = config["stage_c1"]
    controller = config["controller"]
    return {
        "continuation_id": config["qualification_id"],
        "status": "NON_AUTHORITATIVE_RESAMPLING_RISK_CONTINUATION_DESIGN",
        "issue": int(config["issue"]),
        "controller": {
            "alpha": float(controller["alpha"]),
            "epsilon": float(controller["epsilon"]),
            "halfspend": float(controller["halfspend"]),
            "prior_max_attempts": int(controller["prior_max_attempts"]),
            "maximum_total_attempts": int(
                controller["maximum_total_attempts"]
            ),
        },
        "source": {
            "retained_stage_b_expected_unresolved_count": int(
                config["stage_b_lineage"]["expected_unresolved_count"]
            ),
        },
        "stage_c1": {
            "new_bootstrap_draw_indices_allowed": False,
            "observed_statistic_absolute_tolerance": float(
                c1["observed_statistic_absolute_tolerance"]
            ),
            "required_match_count": int(c1["required_match_count"]),
            "shard_count": int(c1["shard_count"]),
        },
        "interpretation_boundary": {
            "fixed_bootstrap_draw_count_selected": False,
            "statistical_power_validated": False,
            "authoritative_core_grid_frozen": False,
            "human_n_frozen": False,
            "participant_recruitment_allowed": False,
            "runtime_f1b_change_allowed": False,
        },
    }


def annotate_partition_with_homogeneous_requirements(
    partition: dict,
    paired_source: dict,
) -> dict:
    source_runs = {
        str(run["run_id"]): run
        for run in paired_source["restriction_runs"]
    }
    for row in partition["rows"]:
        run = source_runs[str(row["run_id"])]
        retained_attempts = tuple(run["bootstrap_attempt_statistics"])
        source_failure_count = sum(
            attempt is None for attempt in retained_attempts
        )
        row["observed_statistic_exact_match"] = (
            float(row["observed_statistic_absolute_delta"]) == 0.0
        )
        row["retained_source_bootstrap_refit_failure_count"] = (
            source_failure_count
        )
        row["bootstrap_refit_failure_free"] = (
            source_failure_count == 0
            and bool(row["attempt_sequence_sha256_match"])
        )
        row["homogeneous_c1_qualification_pass"] = (
            bool(row["qualification_pass"])
            and bool(row["bootstrap_refit_failure_free"])
        )

    partition["homogeneous_c1_pass_count"] = sum(
        bool(row["homogeneous_c1_qualification_pass"])
        for row in partition["rows"]
    )
    partition["exact_observed_statistic_count"] = sum(
        bool(row["observed_statistic_exact_match"])
        for row in partition["rows"]
    )
    partition["bootstrap_refit_failure_free_count"] = sum(
        bool(row["bootstrap_refit_failure_free"])
        for row in partition["rows"]
    )
    partition["status"] = (
        "NON_AUTHORITATIVE_HOMOGENEOUS_C1_EXACT_REPLAY_PARTITION"
    )
    return partition


def combine_homogeneous_c1_partitions(
    partitions: list[dict],
    config: dict,
) -> dict:
    effective = build_effective_continuation(config)

    base_partitions = []
    for partition in partitions:
        copy = dict(partition)
        copy["status"] = (
            "NON_AUTHORITATIVE_STAGE_C1_REGENERATION_QUALIFICATION"
        )
        base_partitions.append(copy)

    combined = combine_continuation_qualification_partitions(
        base_partitions,
        effective,
    )
    rows = combined["rows"]
    required = int(config["stage_c1"]["required_match_count"])

    homogeneous_pass_count = sum(
        bool(row["homogeneous_c1_qualification_pass"])
        for row in rows
    )
    exact_observed_count = sum(
        bool(row["observed_statistic_exact_match"])
        for row in rows
    )
    nonzero_observed_deltas = [
        float(row["observed_statistic_absolute_delta"])
        for row in rows
        if float(row["observed_statistic_absolute_delta"]) != 0.0
    ]
    refit_free_count = sum(
        bool(row["bootstrap_refit_failure_free"])
        for row in rows
    )

    gate_pass = (
        combined["gate_pass"]
        and homogeneous_pass_count == required
        and refit_free_count == required
    )

    return {
        "qualification_id": config["qualification_id"],
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_C1_EXACT_REPLAY_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "stage": "C1",
        "eligible_unresolved_run_count": required,
        "qualified_run_count": len(rows),
        "qualification_pass_count": homogeneous_pass_count,
        "qualification_failure_count": len(rows) - homogeneous_pass_count,
        "exact_observed_statistic_count": exact_observed_count,
        "nonzero_observed_statistic_delta_count": len(
            nonzero_observed_deltas
        ),
        "maximum_observed_statistic_absolute_delta": max(
            nonzero_observed_deltas,
            default=0.0,
        ),
        "bootstrap_refit_failure_free_count": refit_free_count,
        "gate_pass": gate_pass,
        "rows": rows,
        "next_gate": (
            config["decision"]["c1_pass_next_gate"]
            if gate_pass
            else config["decision"]["c1_fail_next_gate"]
        ),
        "boundary": {
            "new_bootstrap_attempt_generated": False,
            "new_draw_index_ge_199_generated": False,
            "stage_c2_authorized": False,
            "power_validated": False,
            "authoritative_core_grid_frozen": False,
            "human_n_frozen": False,
            "participant_recruitment_allowed": False,
            "runtime_f1b_change_allowed": False,
        },
    }
