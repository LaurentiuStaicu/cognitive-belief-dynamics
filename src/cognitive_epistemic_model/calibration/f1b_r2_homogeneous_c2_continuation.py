from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict
import hashlib
import json
from statistics import median
from typing import Iterable, Mapping

import numpy as np

from .f1b_r2_homogeneous_c1_exact_replay import (
    canonical_json_sha256,
    derive_h2_stage_b_binding,
)
from .f1b_r2_openblas_lineage import (
    EXPECTED_OPENBLAS_CORE,
    validate_candidate_environment,
    validate_runtime_cores,
)
from .f1b_r2_paired_bootstrap_characterization import (
    _scales,
    dataset_fingerprint,
)
from .f1b_r2_resampling_risk import (
    ResamplingRiskBoundaryTable,
    generate_resampling_risk_boundaries,
)
from .f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
    regenerate_dataset_for_run,
    stable_shard_index,
)
from .f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)
from .f1b_r2_restriction_recovery import (
    R2Restriction,
    fit_restriction_pair,
    simulate_exact_design_under_restriction,
)


HOMOGENEOUS_C2_ID = "F1B.R2.HOMOGENEOUS_C2_CONTINUATION.V1"
HOMOGENEOUS_C2_STATUS = (
    "NON_AUTHORITATIVE_HOMOGENEOUS_C2_CONTINUATION_DESIGN"
)
EXPECTED_TARGET_STREAMS = 224
EXPECTED_H1_RUNS = 750
EXPECTED_H2_CHECKPOINTS = 750
EXPECTED_PRIOR_ATTEMPTS = 199
FIRST_NEW_DRAW_INDEX = 199
MAXIMUM_NEW_DRAW_INDEX = 9999
MAXIMUM_TOTAL_ATTEMPTS = 10000
EXPECTED_SHARD_COUNT = 16
REPORTING_CHECKPOINTS = (199, 499, 999, 1999, 4999, 10000)


def validate_homogeneous_c2_config(config: dict) -> None:
    if config["continuation_id"] != HOMOGENEOUS_C2_ID:
        raise ValueError("homogeneous C2 identity changed")
    if config["status"] != HOMOGENEOUS_C2_STATUS:
        raise ValueError("unsupported homogeneous C2 status")
    if int(config["issue"]) != 245:
        raise ValueError("homogeneous C2 issue changed")

    candidate = config["candidate_environment"]
    if candidate["variable"] != "OPENBLAS_CORETYPE":
        raise ValueError("homogeneous C2 environment variable changed")
    if candidate["value"] != EXPECTED_OPENBLAS_CORE:
        raise ValueError("homogeneous C2 OpenBLAS core changed")
    if candidate["must_be_set_before_python_start"] is not True:
        raise ValueError("OpenBLAS core must be set before Python startup")
    if candidate["runtime_core_confirmation_required"] is not True:
        raise ValueError("homogeneous C2 runtime core confirmation is required")
    if candidate["environment_fallback_allowed"] is not False:
        raise ValueError("homogeneous C2 environment fallback is forbidden")

    frozen_controller = config["frozen_controller_config"]
    if frozen_controller["path"] != (
        "model/benchmarks/f1b_r2_resampling_risk_controller_v1.json"
    ):
        raise ValueError("homogeneous C2 controller config path changed")
    if frozen_controller["git_blob_sha"] != (
        "3e0878209990d14741d1522d8733feec25e3459f"
    ):
        raise ValueError("homogeneous C2 controller config blob changed")

    source = config["source_lineage"]
    if source["lineage_id"] != (
        "F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1"
    ):
        raise ValueError("homogeneous C2 H1 lineage changed")
    if int(source["expected_restriction_runs"]) != EXPECTED_H1_RUNS:
        raise ValueError("homogeneous C2 H1 run count changed")
    if int(source["expected_attempts_per_run"]) != EXPECTED_PRIOR_ATTEMPTS:
        raise ValueError("homogeneous C2 H1 attempt horizon changed")
    if int(source["expected_bootstrap_fit_failures"]) != 0:
        raise ValueError("homogeneous C2 H1 fit-failure expectation changed")

    stage_b = config["stage_b_lineage"]
    if int(stage_b["expected_restriction_runs"]) != EXPECTED_H1_RUNS:
        raise ValueError("homogeneous C2 H2 run count changed")
    if int(stage_b["expected_stream_checkpoints"]) != EXPECTED_H2_CHECKPOINTS:
        raise ValueError("homogeneous C2 H2 checkpoint count changed")
    if int(stage_b["expected_unresolved_count"]) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 target count changed")

    c1 = config["c1_lineage"]
    if int(c1["required_stream_count"]) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 C1 target count changed")
    if int(c1["qualification_pass_count"]) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 C1 pass count changed")
    if int(c1["exact_observed_statistic_count"]) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 exact-observed count changed")
    if int(c1["bootstrap_refit_failure_free_count"]) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 C1 refit-free count changed")
    if c1["gate_pass"] is not True:
        raise ValueError("homogeneous C2 requires passed C1 gate")

    controller = config["controller"]
    if controller["controller_id"] != "F1B.R2.RESAMPLING_RISK_CONTROLLER.V1":
        raise ValueError("homogeneous C2 controller identity changed")
    if float(controller["alpha"]) != 0.05:
        raise ValueError("homogeneous C2 alpha changed")
    if float(controller["epsilon"]) != 0.001:
        raise ValueError("homogeneous C2 epsilon changed")
    if float(controller["halfspend"]) != 1000.0:
        raise ValueError("homogeneous C2 halfspend changed")
    if str(controller["spending_sequence"]) != (
        "epsilon_n = epsilon * n / (halfspend + n)"
    ):
        raise ValueError("homogeneous C2 spending sequence changed")
    if float(controller["probability_tolerance"]) != 1e-12:
        raise ValueError("homogeneous C2 probability tolerance changed")
    if int(controller["prior_total_attempts"]) != EXPECTED_PRIOR_ATTEMPTS:
        raise ValueError("homogeneous C2 prior attempt count changed")
    if int(controller["maximum_total_attempts"]) != MAXIMUM_TOTAL_ATTEMPTS:
        raise ValueError("homogeneous C2 total-attempt cap changed")
    if controller["controller_changed"] is not False:
        raise ValueError("homogeneous C2 controller must remain unchanged")

    c2 = config["stage_c2"]
    if int(c2["target_stream_count"]) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 stream target changed")
    if int(c2["first_new_draw_index"]) != FIRST_NEW_DRAW_INDEX:
        raise ValueError("homogeneous C2 first new draw index changed")
    if int(c2["maximum_new_draw_index"]) != MAXIMUM_NEW_DRAW_INDEX:
        raise ValueError("homogeneous C2 maximum new draw index changed")
    if int(c2["maximum_total_attempts"]) != MAXIMUM_TOTAL_ATTEMPTS:
        raise ValueError("homogeneous C2 maximum total attempts changed")
    if c2["draw_indices_strictly_increasing"] is not True:
        raise ValueError("homogeneous C2 draw order was weakened")
    if c2["resolved_h2_streams_eligible"] is not False:
        raise ValueError("resolved H2 streams cannot enter homogeneous C2")
    if c2["extend_terminal_stream_allowed"] is not False:
        raise ValueError("terminal streams cannot be extended")
    if c2["stop_on_boundary"] is not True:
        raise ValueError("homogeneous C2 must stop on a decision boundary")
    if c2["stop_on_bootstrap_refit_failure"] is not True:
        raise ValueError("homogeneous C2 must stop on bootstrap refit failure")
    if c2["bootstrap_refit_failure_status"] != (
        "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    ):
        raise ValueError("homogeneous C2 refit-failure status changed")
    if c2["unresolved_at_cap_status"] != "SEQUENTIAL_UNRESOLVED_AT_CAP":
        raise ValueError("homogeneous C2 cap status changed")
    if tuple(int(x) for x in c2["reporting_checkpoints_total_n"]) != (
        REPORTING_CHECKPOINTS
    ):
        raise ValueError("homogeneous C2 reporting checkpoints changed")
    if int(c2["shard_count"]) != EXPECTED_SHARD_COUNT:
        raise ValueError("homogeneous C2 shard count changed")
    if c2["shard_assignment"] != "SHA256_RUN_ID_MODULO_SHARD_COUNT":
        raise ValueError("homogeneous C2 shard assignment changed")
    if c2["historical_c2_inheritance_allowed"] is not False:
        raise ValueError("historical C2 provenance cannot be inherited")
    if c2["execution_requires_merged_gate"] is not True:
        raise ValueError("homogeneous C2 execution must require merged gate")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("homogeneous C2 interpretation boundary weakened")


def validate_c2_environment(
    environment: Mapping[str, str | None] | None = None,
) -> None:
    validate_candidate_environment(
        environment,
        expected_core=EXPECTED_OPENBLAS_CORE,
    )


def validate_c2_runtime_cores(cores: tuple[str, ...]) -> None:
    validate_runtime_cores(
        cores,
        expected_core=EXPECTED_OPENBLAS_CORE,
    )


def validate_new_draw_indices(
    draw_indices: Iterable[int],
) -> tuple[int, ...]:
    values = tuple(int(value) for value in draw_indices)
    if not values:
        raise ValueError("homogeneous C2 new draw set must not be empty")
    if values[0] != FIRST_NEW_DRAW_INDEX:
        raise ValueError("homogeneous C2 must start at draw index 199")
    if values[-1] > MAXIMUM_NEW_DRAW_INDEX:
        raise ValueError("homogeneous C2 draw index exceeds 9999")
    expected = tuple(range(FIRST_NEW_DRAW_INDEX, values[-1] + 1))
    if values != expected:
        raise ValueError(
            "homogeneous C2 new draw indices must be contiguous and increasing"
        )
    return values


def validate_retained_h1_result(h1_result: dict, config: dict) -> None:
    source = config["source_lineage"]
    if h1_result["lineage_id"] != source["lineage_id"]:
        raise ValueError("homogeneous C2 retained H1 lineage mismatch")
    if h1_result["status"] != (
        "NON_AUTHORITATIVE_H1_HOMOGENEOUS_PAIRED_SOURCE_QUALIFIED_RETAINED"
    ):
        raise ValueError("homogeneous C2 requires retained qualified H1 source")
    if h1_result["authoritative"] is not False:
        raise ValueError("homogeneous C2 H1 source became authoritative")
    if h1_result["decision"][
        "h1_full_homogeneous_source_generation_pass"
    ] is not True:
        raise ValueError("homogeneous C2 H1 generation did not pass")
    if h1_result["decision"][
        "h1_independent_replay_qualification_pass"
    ] is not True:
        raise ValueError("homogeneous C2 H1 replay did not pass")
    combined = h1_result["combined_source"]
    if int(combined["artifact_id"]) != int(source["artifact_id"]):
        raise ValueError("homogeneous C2 H1 artifact mismatch")
    if str(combined["combined_json_sha256"]) != str(
        source["combined_json_sha256"]
    ):
        raise ValueError("homogeneous C2 H1 source SHA-256 mismatch")


def validate_retained_h2_result(h2_result: dict, config: dict) -> None:
    stage_b = config["stage_b_lineage"]
    if h2_result["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_STAGE_B_REBUILD_COMPLETE_RETAINED"
    ):
        raise ValueError("homogeneous C2 requires retained H2 result")
    if h2_result["authoritative"] is not False:
        raise ValueError("homogeneous C2 H2 result became authoritative")
    decision = h2_result["decision"]
    if decision["h2_stage_b_rebuild_pass"] is not True:
        raise ValueError("homogeneous C2 H2 rebuild did not pass")
    if decision["historical_stage_b_inherited"] is not False:
        raise ValueError("homogeneous C2 cannot inherit historical Stage-B")
    execution = h2_result["execution"]
    if int(execution["result_artifact_id"]) != int(stage_b["artifact_id"]):
        raise ValueError("homogeneous C2 H2 artifact mismatch")
    if str(execution["raw_replay_json_sha256"]) != str(
        stage_b["raw_json_sha256"]
    ):
        raise ValueError("homogeneous C2 H2 raw SHA-256 mismatch")
    integrity = h2_result["integrity"]
    if str(integrity["unresolved_run_ids_sha256"]) != str(
        stage_b["unresolved_run_ids_sha256"]
    ):
        raise ValueError("homogeneous C2 H2 unresolved digest mismatch")
    if str(integrity["homogeneous_stream_checkpoints_sha256"]) != str(
        stage_b["stream_checkpoints_sha256"]
    ):
        raise ValueError("homogeneous C2 H2 checkpoint digest mismatch")


def validate_retained_c1_result(c1_result: dict, config: dict) -> None:
    expected = config["c1_lineage"]
    if c1_result["qualification_id"] != (
        "F1B.R2.HOMOGENEOUS_C1_EXACT_REPLAY.V1"
    ):
        raise ValueError("homogeneous C2 retained C1 identity changed")
    if c1_result["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_C1_EXACT_REPLAY_PASS_RETAINED"
    ):
        raise ValueError("homogeneous C2 requires retained passed C1 result")
    if c1_result["authoritative"] is not False:
        raise ValueError("homogeneous C2 retained C1 became authoritative")
    result = c1_result["result"]
    if int(result["eligible_unresolved_run_count"]) != int(
        expected["required_stream_count"]
    ):
        raise ValueError("homogeneous C2 retained C1 target count mismatch")
    if int(result["qualification_pass_count"]) != int(
        expected["qualification_pass_count"]
    ):
        raise ValueError("homogeneous C2 retained C1 pass count mismatch")
    if int(result["exact_observed_statistic_count"]) != int(
        expected["exact_observed_statistic_count"]
    ):
        raise ValueError("homogeneous C2 retained C1 exact-observed count mismatch")
    if int(result["bootstrap_refit_failure_free_count"]) != int(
        expected["bootstrap_refit_failure_free_count"]
    ):
        raise ValueError("homogeneous C2 retained C1 refit-free count mismatch")
    if result["gate_pass"] is not True:
        raise ValueError("homogeneous C2 retained C1 gate did not pass")
    if c1_result["decision"]["stage_c2_authorized_by_this_result"] is not False:
        raise ValueError("retained C1 unexpectedly self-authorized C2")
    combined = c1_result["execution"]["combined_artifact"]
    if int(combined["artifact_id"]) != int(expected["artifact_id"]):
        raise ValueError("homogeneous C2 retained C1 artifact mismatch")
    if str(combined["combined_json_sha256"]) != str(
        expected["combined_json_sha256"]
    ):
        raise ValueError("homogeneous C2 retained C1 combined SHA-256 mismatch")
    if int(combined["combined_json_size_bytes"]) != int(
        expected["combined_json_size_bytes"]
    ):
        raise ValueError("homogeneous C2 retained C1 combined size mismatch")


def _source_run_map(paired_source: dict) -> dict[str, dict]:
    runs = {
        str(row["run_id"]): row
        for row in paired_source["restriction_runs"]
    }
    if len(runs) != EXPECTED_H1_RUNS:
        raise ValueError("homogeneous C2 H1 source run IDs are not unique")
    return runs


def _checkpoint_map(raw_h2: dict) -> dict[str, dict]:
    checkpoints = {
        str(row["run_id"]): row
        for row in raw_h2["stream_checkpoints"]
    }
    if len(checkpoints) != EXPECTED_H2_CHECKPOINTS:
        raise ValueError("homogeneous C2 H2 checkpoint IDs are not unique")
    return checkpoints


def _replay_row_map(raw_h2: dict) -> dict[str, dict]:
    rows = {
        str(row["run_id"]): row
        for row in raw_h2["replay_rows"]
    }
    if len(rows) != EXPECTED_H1_RUNS:
        raise ValueError("homogeneous C2 H2 replay IDs are not unique")
    return rows


def bind_c2_targets(
    paired_source: dict,
    raw_h2: dict,
    c1_combined: dict,
    config: dict,
) -> dict:
    validate_homogeneous_c2_config(config)

    source = config["source_lineage"]
    if int(paired_source["restriction_run_count"]) != int(
        source["expected_restriction_runs"]
    ):
        raise ValueError("homogeneous C2 H1 source run count changed")
    if any(bool(run["fit_failure"]) for run in paired_source["restriction_runs"]):
        raise ValueError("homogeneous C2 H1 source contains observed fit failure")
    if any(
        len(run["bootstrap_attempt_statistics"]) != EXPECTED_PRIOR_ATTEMPTS
        for run in paired_source["restriction_runs"]
    ):
        raise ValueError("homogeneous C2 H1 prefix length changed")
    if any(
        any(value is None for value in run["bootstrap_attempt_statistics"])
        for run in paired_source["restriction_runs"]
    ):
        raise ValueError("homogeneous C2 H1 source contains bootstrap refit failure")

    h2_binding = derive_h2_stage_b_binding(raw_h2, config)
    unresolved = tuple(h2_binding["unresolved_run_ids"])
    unresolved_set = set(unresolved)
    if len(unresolved) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 target set is not 224 streams")

    expected_c1 = config["c1_lineage"]
    if c1_combined["qualification_id"] != (
        "F1B.R2.HOMOGENEOUS_C1_EXACT_REPLAY.V1"
    ):
        raise ValueError("homogeneous C2 C1 artifact identity changed")
    if c1_combined["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_C1_EXACT_REPLAY_RESULT"
    ):
        raise ValueError("homogeneous C2 C1 artifact status changed")
    if c1_combined["authoritative"] is not False:
        raise ValueError("homogeneous C2 C1 artifact became authoritative")
    if c1_combined["gate_pass"] is not True:
        raise ValueError("homogeneous C2 C1 artifact gate did not pass")
    if int(c1_combined["qualified_run_count"]) != int(
        expected_c1["required_stream_count"]
    ):
        raise ValueError("homogeneous C2 C1 artifact count changed")
    if int(c1_combined["qualification_pass_count"]) != int(
        expected_c1["qualification_pass_count"]
    ):
        raise ValueError("homogeneous C2 C1 artifact pass count changed")
    if int(c1_combined["exact_observed_statistic_count"]) != int(
        expected_c1["exact_observed_statistic_count"]
    ):
        raise ValueError("homogeneous C2 C1 exact-observed artifact count changed")
    if int(c1_combined["bootstrap_refit_failure_free_count"]) != int(
        expected_c1["bootstrap_refit_failure_free_count"]
    ):
        raise ValueError("homogeneous C2 C1 refit-free artifact count changed")

    c1_rows = {
        str(row["run_id"]): row
        for row in c1_combined["rows"]
    }
    if len(c1_rows) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 C1 row IDs are not unique")
    if set(c1_rows) != unresolved_set:
        raise ValueError("homogeneous C2 H2/C1 target sets differ")

    source_runs = _source_run_map(paired_source)
    checkpoints = _checkpoint_map(raw_h2)
    replay_rows = _replay_row_map(raw_h2)
    targets: list[dict] = []

    for run_id in unresolved:
        if run_id not in source_runs:
            raise ValueError(f"homogeneous C2 target missing from H1: {run_id}")
        if run_id not in checkpoints or run_id not in replay_rows:
            raise ValueError(f"homogeneous C2 target missing from H2: {run_id}")
        c1_row = c1_rows[run_id]
        if c1_row["homogeneous_c1_qualification_pass"] is not True:
            raise ValueError(f"homogeneous C2 target did not pass C1: {run_id}")
        if c1_row["dataset_fingerprint_match"] is not True:
            raise ValueError(f"homogeneous C2 target C1 dataset mismatch: {run_id}")
        if c1_row["observed_statistic_match"] is not True:
            raise ValueError(f"homogeneous C2 target C1 observed mismatch: {run_id}")
        if c1_row["attempt_sequence_sha256_match"] is not True:
            raise ValueError(f"homogeneous C2 target C1 attempt mismatch: {run_id}")
        if c1_row["bootstrap_refit_failure_free"] is not True:
            raise ValueError(f"homogeneous C2 target C1 refit failure: {run_id}")

        run = source_runs[run_id]
        checkpoint = checkpoints[run_id]
        replay = replay_rows[run_id]
        attempts = tuple(run["bootstrap_attempt_statistics"])
        attempt_hash = canonical_attempt_sequence_sha256(attempts)
        if attempt_hash != str(checkpoint["attempt_sequence_sha256"]):
            raise ValueError(f"homogeneous C2 H1/H2 prefix mismatch: {run_id}")
        if attempt_hash != str(c1_row["retained_attempt_sequence_sha256"]):
            raise ValueError(f"homogeneous C2 H1/C1 prefix mismatch: {run_id}")
        if str(run["dataset_sha256"]) != str(checkpoint["dataset_sha256"]):
            raise ValueError(f"homogeneous C2 H1/H2 dataset mismatch: {run_id}")
        if int(run["bootstrap_stream_seed"]) != int(
            checkpoint["bootstrap_stream_seed"]
        ):
            raise ValueError(f"homogeneous C2 H1/H2 stream-seed mismatch: {run_id}")
        if float(run["observed_statistic"]) != float(
            checkpoint["observed_statistic"]
        ):
            raise ValueError(
                f"homogeneous C2 H1/H2 observed-statistic mismatch: {run_id}"
            )
        if str(c1_row["regenerated_attempt_sequence_sha256"]) != attempt_hash:
            raise ValueError(
                f"homogeneous C2 C1 regenerated-prefix mismatch: {run_id}"
            )
        if str(replay["dataset_sha256"]) != str(run["dataset_sha256"]):
            raise ValueError(f"homogeneous C2 H1/H2 replay dataset mismatch: {run_id}")
        if int(replay["bootstrap_stream_seed"]) != int(
            run["bootstrap_stream_seed"]
        ):
            raise ValueError(f"homogeneous C2 H1/H2 replay seed mismatch: {run_id}")
        if float(replay["observed_statistic"]) != float(
            run["observed_statistic"]
        ):
            raise ValueError(
                f"homogeneous C2 H1/H2 replay observed mismatch: {run_id}"
            )
        if str(replay["attempt_sequence_sha256"]) != attempt_hash:
            raise ValueError(f"homogeneous C2 H1/H2 replay prefix mismatch: {run_id}")
        if replay["decision"] is not None:
            raise ValueError(f"homogeneous C2 target already resolved in H2: {run_id}")
        if replay["status"] != "SEQUENTIAL_UNRESOLVED":
            raise ValueError(f"homogeneous C2 target H2 status changed: {run_id}")
        if int(replay["terminal_n"]) != EXPECTED_PRIOR_ATTEMPTS:
            raise ValueError(f"homogeneous C2 target H2 terminal n changed: {run_id}")
        if replay["failure_n"] is not None:
            raise ValueError(f"homogeneous C2 target has prior refit failure: {run_id}")

        targets.append(
            {
                "run_id": run_id,
                "source_run": run,
                "checkpoint": checkpoint,
                "h2_replay_row": replay,
                "c1_row": c1_row,
            }
        )

    target_hash = canonical_json_sha256(sorted(unresolved))
    if target_hash != str(config["stage_b_lineage"]["unresolved_run_ids_sha256"]):
        raise ValueError("homogeneous C2 target digest changed")

    return {
        "target_run_ids": sorted(unresolved),
        "target_run_ids_sha256": target_hash,
        "targets": targets,
        "h2_binding": h2_binding,
    }


def build_c2_boundaries(config: dict) -> ResamplingRiskBoundaryTable:
    validate_homogeneous_c2_config(config)
    controller = config["controller"]
    return generate_resampling_risk_boundaries(
        alpha=float(controller["alpha"]),
        epsilon=float(controller["epsilon"]),
        halfspend=float(controller["halfspend"]),
        max_n=int(controller["maximum_total_attempts"]),
        probability_tolerance=float(controller["probability_tolerance"]),
    )


def _restriction_index(restriction: R2Restriction) -> int:
    return 1 if restriction is R2Restriction.ADD else 2


def _prefix_exceedance_sum(run: dict) -> int:
    observed = float(run["observed_statistic"])
    attempts = tuple(run["bootstrap_attempt_statistics"])
    if len(attempts) != EXPECTED_PRIOR_ATTEMPTS:
        raise ValueError("homogeneous C2 retained prefix length changed")
    if any(value is None for value in attempts):
        raise ValueError("homogeneous C2 retained prefix contains refit failure")
    return sum(int(float(value) >= observed) for value in attempts)


def _prepare_scientific_stream(
    target: dict,
    *,
    paired_config: dict,
    departure_cases: dict[str, dict],
    observed_tolerance: float,
) -> dict:
    run = target["source_run"]
    dataset = regenerate_dataset_for_run(
        run,
        paired_config=paired_config,
        departure_cases=departure_cases,
    )
    regenerated_dataset_sha = dataset_fingerprint(dataset)
    retained_dataset_sha = str(run["dataset_sha256"])
    if regenerated_dataset_sha != retained_dataset_sha:
        raise ValueError(
            f"homogeneous C2 regenerated dataset mismatch: {run['run_id']}"
        )
    if retained_dataset_sha != str(target["checkpoint"]["dataset_sha256"]):
        raise ValueError(
            f"homogeneous C2 checkpoint dataset mismatch: {run['run_id']}"
        )

    restriction = R2Restriction(str(run["restriction"]))
    scales = _scales(paired_config, generator=False)
    observed_pair = fit_restriction_pair(
        dataset,
        restriction,
        scales=scales,
    )
    regenerated_observed = float(observed_pair.statistic)
    retained_observed = float(run["observed_statistic"])
    observed_delta = abs(regenerated_observed - retained_observed)
    if observed_delta > float(observed_tolerance):
        raise ValueError(
            f"homogeneous C2 observed statistic mismatch: {run['run_id']}"
        )

    prefix_sum = _prefix_exceedance_sum(run)
    h2_row = target["h2_replay_row"]
    if int(h2_row["terminal_sum"]) != int(prefix_sum):
        raise ValueError(
            f"homogeneous C2 H2 prefix sum mismatch: {run['run_id']}"
        )
    if int(h2_row["full_prefix_sum_199"]) != int(prefix_sum):
        raise ValueError(
            f"homogeneous C2 H2 full-prefix sum mismatch: {run['run_id']}"
        )
    if h2_row["stopping_n"] is not None or h2_row["boundary_hit"] is not None:
        raise ValueError(
            f"homogeneous C2 H2 target became terminal: {run['run_id']}"
        )

    return {
        "dataset": dataset,
        "restriction": restriction,
        "scales": scales,
        "observed_pair": observed_pair,
        "regenerated_observed_statistic": regenerated_observed,
        "retained_observed_statistic": retained_observed,
        "observed_statistic_absolute_delta": observed_delta,
        "observed_statistic_exact_match": (
            regenerated_observed == retained_observed
        ),
        "prefix_sum_199": int(prefix_sum),
    }


def _continuation_state_at_checkpoint(
    *,
    checkpoint_n: int,
    status: str,
    stopping_n: int | None,
    failure_n: int | None,
    terminal_n: int,
) -> str:
    checkpoint_n = int(checkpoint_n)
    if checkpoint_n == EXPECTED_PRIOR_ATTEMPTS:
        return "UNRESOLVED_ACTIVE"
    if stopping_n is not None and int(stopping_n) <= checkpoint_n:
        return "RESOLVED"
    if failure_n is not None and int(failure_n) <= checkpoint_n:
        return "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    if status == "SEQUENTIAL_UNRESOLVED_AT_CAP" and terminal_n <= checkpoint_n:
        return "SEQUENTIAL_UNRESOLVED_AT_CAP"
    if terminal_n >= checkpoint_n:
        return "UNRESOLVED_ACTIVE"
    return "TERMINATED_BEFORE_CHECKPOINT"


def continue_target_stream(
    target: dict,
    *,
    paired_config: dict,
    departure_cases: dict[str, dict],
    boundaries: ResamplingRiskBoundaryTable,
    config: dict,
) -> dict:
    validate_homogeneous_c2_config(config)
    run = target["source_run"]
    prepared = _prepare_scientific_stream(
        target,
        paired_config=paired_config,
        departure_cases=departure_cases,
        observed_tolerance=1e-10,
    )
    restriction = prepared["restriction"]
    observed_pair = prepared["observed_pair"]
    retained_observed = prepared["retained_observed_statistic"]
    partial_sum = int(prepared["prefix_sum_199"])
    prior_boundary = boundaries.row(EXPECTED_PRIOR_ATTEMPTS)
    h2_row = target["h2_replay_row"]
    if int(h2_row["terminal_lower"]) != int(prior_boundary.lower):
        raise ValueError(
            f"homogeneous C2 H2 lower-boundary mismatch: {run['run_id']}"
        )
    if int(h2_row["terminal_upper"]) != int(prior_boundary.upper):
        raise ValueError(
            f"homogeneous C2 H2 upper-boundary mismatch: {run['run_id']}"
        )
    if partial_sum <= int(prior_boundary.lower) or partial_sum >= int(
        prior_boundary.upper
    ):
        raise ValueError(
            f"homogeneous C2 target is terminal at retained n=199: {run['run_id']}"
        )
    seed = int(run["bootstrap_stream_seed"])

    retained_attempts = tuple(run["bootstrap_attempt_statistics"])
    retained_hash = canonical_attempt_sequence_sha256(retained_attempts)
    new_attempts: list[float | None] = []
    new_exceedances: list[int | None] = []

    status = "SEQUENTIAL_UNRESOLVED_AT_CAP"
    decision: str | None = None
    stopping_n: int | None = None
    stopping_sum: int | None = None
    boundary_hit: str | None = None
    failure_n: int | None = None
    failure_draw_index: int | None = None

    for draw_index in range(
        FIRST_NEW_DRAW_INDEX,
        MAXIMUM_NEW_DRAW_INDEX + 1,
    ):
        total_n = draw_index + 1
        rng = np.random.default_rng(
            np.random.SeedSequence(
                [
                    seed,
                    _restriction_index(restriction),
                    draw_index,
                ]
            )
        )
        bootstrap_dataset = simulate_exact_design_under_restriction(
            prepared["dataset"],
            observed_pair.restricted,
            scales=prepared["scales"],
            rng=rng,
        )
        try:
            pair = fit_restriction_pair(
                bootstrap_dataset,
                restriction,
                scales=prepared["scales"],
            )
        except (RuntimeError, ValueError, np.linalg.LinAlgError):
            new_attempts.append(None)
            new_exceedances.append(None)
            status = config["stage_c2"]["bootstrap_refit_failure_status"]
            failure_n = total_n
            failure_draw_index = draw_index
            break

        statistic = float(pair.statistic)
        exceedance = int(statistic >= retained_observed)
        new_attempts.append(statistic)
        new_exceedances.append(exceedance)
        partial_sum += exceedance

        boundary = boundaries.row(total_n)
        if partial_sum <= int(boundary.lower):
            status = "SEQUENTIAL_DECISION"
            decision = "REJECT_P_LE_ALPHA"
            stopping_n = total_n
            stopping_sum = partial_sum
            boundary_hit = "LOWER"
            break
        if partial_sum >= int(boundary.upper):
            status = "SEQUENTIAL_DECISION"
            decision = "NOT_REJECT_P_GT_ALPHA"
            stopping_n = total_n
            stopping_sum = partial_sum
            boundary_hit = "UPPER"
            break

    if not new_attempts:
        raise RuntimeError("homogeneous C2 generated no continuation attempt")

    generated_indices = tuple(
        range(
            FIRST_NEW_DRAW_INDEX,
            FIRST_NEW_DRAW_INDEX + len(new_attempts),
        )
    )
    validate_new_draw_indices(generated_indices)

    terminal_n = EXPECTED_PRIOR_ATTEMPTS + len(new_attempts)
    if terminal_n > MAXIMUM_TOTAL_ATTEMPTS:
        raise RuntimeError("homogeneous C2 terminal n exceeds cap")
    if status == "SEQUENTIAL_UNRESOLVED_AT_CAP":
        if terminal_n != MAXIMUM_TOTAL_ATTEMPTS:
            raise RuntimeError("homogeneous C2 unresolved stream stopped before cap")
        terminal_boundary = boundaries.row(terminal_n)
    elif failure_n is not None:
        terminal_boundary = boundaries.row(failure_n)
    else:
        if stopping_n is None:
            raise RuntimeError("homogeneous C2 decision missing stopping n")
        terminal_boundary = boundaries.row(stopping_n)

    full_attempts = retained_attempts + tuple(new_attempts)
    new_attempt_hash = canonical_attempt_sequence_sha256(new_attempts)
    full_attempt_hash = canonical_attempt_sequence_sha256(full_attempts)

    reporting_states = {
        str(checkpoint): _continuation_state_at_checkpoint(
            checkpoint_n=checkpoint,
            status=status,
            stopping_n=stopping_n,
            failure_n=failure_n,
            terminal_n=terminal_n,
        )
        for checkpoint in REPORTING_CHECKPOINTS
    }

    return {
        "run_id": str(run["run_id"]),
        "dataset_id": str(run["dataset_id"]),
        "dataset_sha256": str(run["dataset_sha256"]),
        "bootstrap_stream_seed": seed,
        "identity": str(run["identity"]),
        "identity_type": str(run["identity_type"]),
        "restriction": str(run["restriction"]),
        "role": str(run["role"]),
        "anchor_id": run["anchor_id"],
        "axis": run["axis"],
        "sign": run["sign"],
        "target_mean_bernoulli_kl": run["target_mean_bernoulli_kl"],
        "evaluation_replicate": int(run["evaluation_replicate"]),
        "retained_observed_statistic": retained_observed,
        "regenerated_observed_statistic": prepared[
            "regenerated_observed_statistic"
        ],
        "observed_statistic_absolute_delta": prepared[
            "observed_statistic_absolute_delta"
        ],
        "observed_statistic_exact_match": prepared[
            "observed_statistic_exact_match"
        ],
        "prior_total_attempts": EXPECTED_PRIOR_ATTEMPTS,
        "prior_exceedance_sum": int(prepared["prefix_sum_199"]),
        "prior_lower_boundary": int(prior_boundary.lower),
        "prior_upper_boundary": int(prior_boundary.upper),
        "retained_prefix_sha256": retained_hash,
        "c1_retained_prefix_sha256": str(
            target["c1_row"]["retained_attempt_sequence_sha256"]
        ),
        "first_new_draw_index": FIRST_NEW_DRAW_INDEX,
        "last_new_draw_index": generated_indices[-1],
        "new_attempt_count": len(new_attempts),
        "new_successful_fit_count": sum(
            value is not None for value in new_attempts
        ),
        "new_attempt_sequence_sha256": new_attempt_hash,
        "full_attempt_sequence_sha256": full_attempt_hash,
        "status": status,
        "decision": decision,
        "stopping_n": stopping_n,
        "stopping_sum": stopping_sum,
        "boundary_hit": boundary_hit,
        "failure_n": failure_n,
        "failure_draw_index": failure_draw_index,
        "terminal_n": terminal_n,
        "terminal_sum": partial_sum,
        "terminal_lower": int(terminal_boundary.lower),
        "terminal_upper": int(terminal_boundary.upper),
        "reporting_states": reporting_states,
        "boundary": {
            "new_draw_indices_contiguous": True,
            "terminal_stream_extended": False,
            "historical_c2_inherited": False,
        },
    }


def continue_c2_partition(
    binding: dict,
    paired_config: dict,
    v2_config: dict,
    review_config: dict,
    historical_departure_config: dict,
    config: dict,
    *,
    shard_index: int,
) -> dict:
    validate_homogeneous_c2_config(config)
    shard_count = int(config["stage_c2"]["shard_count"])
    shard_index = int(shard_index)
    if not 0 <= shard_index < shard_count:
        raise ValueError("homogeneous C2 shard index out of range")

    target_map = {
        str(target["run_id"]): target
        for target in binding["targets"]
    }
    if len(target_map) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 binding target count changed")

    selected_ids = sorted(
        run_id
        for run_id in target_map
        if stable_shard_index(run_id, shard_count) == shard_index
    )

    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_departure_config,
    )
    boundaries = build_c2_boundaries(config)
    rows = [
        continue_target_stream(
            target_map[run_id],
            paired_config=paired_config,
            departure_cases=departure_cases,
            boundaries=boundaries,
            config=config,
        )
        for run_id in selected_ids
    ]

    return {
        "continuation_id": config["continuation_id"],
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_C2_PARTITION",
        "authoritative": False,
        "issue": int(config["issue"]),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "eligible_target_count": EXPECTED_TARGET_STREAMS,
        "target_run_ids_sha256": binding["target_run_ids_sha256"],
        "continued_run_count": len(rows),
        "rows": rows,
        "boundary": {
            "only_c1_qualified_targets": True,
            "resolved_h2_streams_extended": False,
            "historical_c2_inherited": False,
        },
    }


def _stratum_key(value) -> str:
    return "NULL" if value is None else str(value)


def _stopping_distribution(rows: list[dict]) -> dict:
    values = [
        int(row["stopping_n"])
        for row in rows
        if row["stopping_n"] is not None
    ]
    if not values:
        return {
            "resolved_count": 0,
            "minimum": None,
            "median": None,
            "maximum": None,
            "histogram": {},
        }
    counts = Counter(values)
    return {
        "resolved_count": len(values),
        "minimum": min(values),
        "median": float(median(values)),
        "maximum": max(values),
        "histogram": {
            str(key): int(value)
            for key, value in sorted(counts.items())
        },
    }


def _checkpoint_summary(rows: list[dict]) -> dict:
    result: dict[str, dict] = {}
    previous_resolved = 0
    for checkpoint in REPORTING_CHECKPOINTS:
        if checkpoint == EXPECTED_PRIOR_ATTEMPTS:
            resolved = 0
            failures = 0
            active = len(rows)
        else:
            resolved = sum(
                row["stopping_n"] is not None
                and int(row["stopping_n"]) <= checkpoint
                for row in rows
            )
            failures = sum(
                row["failure_n"] is not None
                and int(row["failure_n"]) <= checkpoint
                for row in rows
            )
            active = len(rows) - resolved - failures
            if checkpoint == MAXIMUM_TOTAL_ATTEMPTS:
                active = sum(
                    row["status"] == "SEQUENTIAL_UNRESOLVED_AT_CAP"
                    for row in rows
                )
        result[str(checkpoint)] = {
            "cumulative_newly_resolved_count": int(resolved),
            "newly_resolved_since_previous_checkpoint": int(
                resolved - previous_resolved
            ),
            "cumulative_bootstrap_refit_failure_count": int(failures),
            "active_or_unresolved_count": int(active),
        }
        previous_resolved = resolved
    return result


def _row_summary(rows: list[dict]) -> dict:
    resolved = [row for row in rows if row["decision"] is not None]
    reject = sum(
        row["decision"] == "REJECT_P_LE_ALPHA"
        for row in resolved
    )
    not_reject = sum(
        row["decision"] == "NOT_REJECT_P_GT_ALPHA"
        for row in resolved
    )
    failures = sum(
        row["status"] == "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
        for row in rows
    )
    unresolved_cap = sum(
        row["status"] == "SEQUENTIAL_UNRESOLVED_AT_CAP"
        for row in rows
    )
    return {
        "run_count": len(rows),
        "newly_resolved_count": len(resolved),
        "newly_reject_count": int(reject),
        "newly_not_reject_count": int(not_reject),
        "bootstrap_refit_failure_unresolved_count": int(failures),
        "unresolved_at_cap_count": int(unresolved_cap),
        "new_attempt_count": sum(int(row["new_attempt_count"]) for row in rows),
        "new_successful_fit_count": sum(
            int(row["new_successful_fit_count"])
            for row in rows
        ),
        "stopping_distribution": _stopping_distribution(rows),
    }


def _aggregate_by(rows: list[dict], field: str) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[_stratum_key(row.get(field))].append(row)
    return [
        {
            field: key,
            **_row_summary(values),
        }
        for key, values in sorted(groups.items())
    ]


def annotate_partition_runtime_cores(
    partition: dict,
    cores: tuple[str, ...],
) -> dict:
    validate_c2_runtime_cores(cores)
    normalized = list(cores)
    partition["runtime_openblas_cores"] = normalized
    for row in partition["rows"]:
        row["runtime_openblas_cores"] = normalized
    return partition


def combine_c2_partitions(
    partitions: list[dict],
    config: dict,
) -> dict:
    validate_homogeneous_c2_config(config)
    shard_count = int(config["stage_c2"]["shard_count"])
    if len(partitions) != shard_count:
        raise ValueError("homogeneous C2 partition count mismatch")

    seen_shards: set[int] = set()
    rows: list[dict] = []
    target_hashes: set[str] = set()

    for partition in partitions:
        if partition["continuation_id"] != config["continuation_id"]:
            raise ValueError("homogeneous C2 partition identity mismatch")
        if partition["status"] != "NON_AUTHORITATIVE_HOMOGENEOUS_C2_PARTITION":
            raise ValueError("homogeneous C2 partition status mismatch")
        if partition["authoritative"] is not False:
            raise ValueError("homogeneous C2 partition became authoritative")
        if int(partition["shard_count"]) != shard_count:
            raise ValueError("homogeneous C2 partition shard count mismatch")
        shard = int(partition["shard_index"])
        if shard in seen_shards:
            raise ValueError("duplicate homogeneous C2 shard")
        seen_shards.add(shard)
        target_hashes.add(str(partition["target_run_ids_sha256"]))
        cores = tuple(partition.get("runtime_openblas_cores", ()))
        validate_c2_runtime_cores(cores)
        for row in partition["rows"]:
            if row.get("runtime_openblas_cores") != list(cores):
                raise ValueError(
                    "homogeneous C2 row runtime core evidence mismatch"
                )
        rows.extend(partition["rows"])

    if seen_shards != set(range(shard_count)):
        raise ValueError("homogeneous C2 shard coverage incomplete")
    if len(target_hashes) != 1:
        raise ValueError("homogeneous C2 target digest differs across shards")

    run_ids = [str(row["run_id"]) for row in rows]
    if len(run_ids) != EXPECTED_TARGET_STREAMS:
        raise ValueError("homogeneous C2 combined target count mismatch")
    if len(set(run_ids)) != EXPECTED_TARGET_STREAMS:
        raise ValueError("duplicate homogeneous C2 run ID")
    if canonical_json_sha256(sorted(run_ids)) != str(
        config["stage_b_lineage"]["unresolved_run_ids_sha256"]
    ):
        raise ValueError("homogeneous C2 combined target digest mismatch")

    rows.sort(key=lambda row: str(row["run_id"]))
    summary = _row_summary(rows)
    checkpoint_summary = _checkpoint_summary(rows)

    return {
        "continuation_id": config["continuation_id"],
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_C2_CONTINUATION_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "target_stream_count": EXPECTED_TARGET_STREAMS,
        "continued_stream_count": len(rows),
        "target_run_ids_sha256": str(
            config["stage_b_lineage"]["unresolved_run_ids_sha256"]
        ),
        "global_summary": summary,
        "reporting_checkpoints": checkpoint_summary,
        "by_restriction": _aggregate_by(rows, "restriction"),
        "by_role": _aggregate_by(rows, "role"),
        "by_axis": _aggregate_by(rows, "axis"),
        "by_target": _aggregate_by(rows, "target_mean_bernoulli_kl"),
        "by_sign": _aggregate_by(rows, "sign"),
        "by_anchor": _aggregate_by(rows, "anchor_id"),
        "by_evaluation_replicate": _aggregate_by(
            rows,
            "evaluation_replicate",
        ),
        "rows": rows,
        "boundary": {
            "fixed_bootstrap_draw_count_selected": False,
            "power_validated": False,
            "authoritative_core_grid_frozen": False,
            "human_n_frozen": False,
            "participant_recruitment_allowed": False,
            "runtime_f1b_change_allowed": False,
        },
    }
