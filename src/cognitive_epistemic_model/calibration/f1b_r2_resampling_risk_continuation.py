from __future__ import annotations

from collections.abc import Iterable
import hashlib

import numpy as np

from .f1b_prehuman_recovery import R2Dataset, R2Family
from .f1b_r2_kl_controlled_departures import (
    generate_kl_controlled_departure_design,
)
from .f1b_r2_paired_bootstrap_characterization import (
    _null_specs,
    _scales,
    _simulate_dataset,
    dataset_fingerprint,
)
from .f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)
from .f1b_r2_restriction_recovery import (
    R2Restriction,
    fit_restriction_pair,
    simulate_exact_design_under_restriction,
)


def stable_shard_index(run_id: str, shard_count: int) -> int:
    if int(shard_count) <= 0:
        raise ValueError("shard_count must be positive")
    digest = hashlib.sha256(str(run_id).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % int(shard_count)


def _validate_continuation_config(config: dict) -> None:
    if config["status"] != (
        "NON_AUTHORITATIVE_RESAMPLING_RISK_CONTINUATION_DESIGN"
    ):
        raise ValueError("unsupported continuation design status")
    controller = config["controller"]
    if float(controller["alpha"]) != 0.05:
        raise ValueError("continuation alpha changed")
    if float(controller["epsilon"]) != 0.001:
        raise ValueError("continuation epsilon changed")
    if float(controller["halfspend"]) != 1000.0:
        raise ValueError("continuation halfspend changed")
    if int(controller["prior_max_attempts"]) != 199:
        raise ValueError("continuation prior horizon changed")
    if int(controller["maximum_total_attempts"]) != 10000:
        raise ValueError("continuation cap changed")
    c1 = config["stage_c1"]
    if bool(c1["new_bootstrap_draw_indices_allowed"]):
        raise ValueError("Stage C1 must not authorize new bootstrap indices")
    if int(c1["required_match_count"]) != 224:
        raise ValueError("Stage C1 required-match count changed")
    if int(c1["shard_count"]) != 8:
        raise ValueError("Stage C1 shard count changed")
    boundary = config["interpretation_boundary"]
    if any(bool(value) for value in boundary.values()):
        raise ValueError("continuation interpretation boundary was weakened")


def build_departure_case_map(
    v2_config: dict,
    review_config: dict,
    historical_departure_config: dict,
) -> dict[str, dict]:
    generated = generate_kl_controlled_departure_design(
        v2_config,
        review_config,
        historical_departure_config,
    )
    if generated["design_id"] != "F1B.R2.KL_CONTROLLED_DEPARTURE.V2":
        raise ValueError("continuation requires KL-controlled departure V2")
    if int(generated["case_count"]) != 36:
        raise ValueError("continuation requires all 36 V2 departure cases")
    cases = {
        str(case["case_id"]): case
        for case in generated["cases"]
    }
    if len(cases) != 36:
        raise ValueError("duplicate V2 departure case ID")
    return cases


def regenerate_dataset_for_run(
    run: dict,
    *,
    paired_config: dict,
    departure_cases: dict[str, dict],
) -> R2Dataset:
    identity_type = str(run["identity_type"])
    identity = str(run["identity"])
    if identity_type == "NULL":
        specs = {
            str(spec["identity"]): spec
            for spec in _null_specs(paired_config)
        }
        if identity not in specs:
            raise ValueError(f"unknown null identity: {identity}")
        spec = specs[identity]
        family = spec["family"]
        parameters = tuple(float(x) for x in spec["parameters"])
    elif identity_type == "DEPARTURE":
        if identity not in departure_cases:
            raise ValueError(f"unknown V2 departure identity: {identity}")
        case = departure_cases[identity]
        family = R2Family.AP_C
        parameters = tuple(
            float(value) for value in case["general_coefficients"]
        )
    else:
        raise ValueError(f"unsupported identity_type: {identity_type}")

    return _simulate_dataset(
        family=family,
        parameters=parameters,
        config=paired_config,
        dataset_identity=str(run["dataset_id"]),
        evaluation_replicate=int(run["evaluation_replicate"]),
    )


def regenerate_bootstrap_attempt_statistics(
    run: dict,
    dataset: R2Dataset,
    *,
    paired_config: dict,
    draw_indices: Iterable[int],
) -> tuple[float, tuple[float | None, ...]]:
    restriction = R2Restriction(str(run["restriction"]))
    scales = _scales(paired_config, generator=False)
    observed = fit_restriction_pair(
        dataset,
        restriction,
        scales=scales,
    )
    restriction_index = (
        1 if restriction is R2Restriction.ADD else 2
    )
    seed = int(run["bootstrap_stream_seed"])

    attempts: list[float | None] = []
    for draw in draw_indices:
        index = int(draw)
        if index < 0:
            raise ValueError("bootstrap draw index must be non-negative")
        rng = np.random.default_rng(
            np.random.SeedSequence(
                [seed, int(restriction_index), index]
            )
        )
        bootstrap_dataset = simulate_exact_design_under_restriction(
            dataset,
            observed.restricted,
            scales=scales,
            rng=rng,
        )
        try:
            pair = fit_restriction_pair(
                bootstrap_dataset,
                restriction,
                scales=scales,
            )
        except (RuntimeError, ValueError, np.linalg.LinAlgError):
            attempts.append(None)
            continue
        attempts.append(float(pair.statistic))

    return float(observed.statistic), tuple(attempts)


def _checkpoint_map(stage_b_result: dict) -> dict[str, dict]:
    checkpoints = {
        str(row["run_id"]): row
        for row in stage_b_result["stream_checkpoints"]
    }
    if len(checkpoints) != int(
        stage_b_result["integrity"]["stream_checkpoint_count"]
    ):
        raise ValueError("Stage-B stream checkpoint IDs are not unique")
    return checkpoints


def _source_run_map(paired_source: dict) -> dict[str, dict]:
    runs = {
        str(row["run_id"]): row
        for row in paired_source["restriction_runs"]
    }
    if len(runs) != int(paired_source["restriction_run_count"]):
        raise ValueError("paired-source run IDs are not unique")
    return runs


def qualify_continuation_partition(
    paired_source: dict,
    stage_b_result: dict,
    continuation_config: dict,
    paired_config: dict,
    v2_config: dict,
    review_config: dict,
    historical_departure_config: dict,
    *,
    shard_index: int,
) -> dict:
    _validate_continuation_config(continuation_config)
    c1 = continuation_config["stage_c1"]
    shard_count = int(c1["shard_count"])
    shard_index = int(shard_index)
    if not 0 <= shard_index < shard_count:
        raise ValueError("Stage C1 shard index out of range")

    unresolved = tuple(
        str(run_id)
        for run_id in stage_b_result["unresolved_run_ids"]
    )
    if len(unresolved) != int(
        continuation_config["source"][
            "retained_stage_b_expected_unresolved_count"
        ]
    ):
        raise ValueError("Stage-B unresolved-run count changed")
    if len(unresolved) != len(set(unresolved)):
        raise ValueError("Stage-B unresolved run IDs are not unique")

    source_runs = _source_run_map(paired_source)
    checkpoints = _checkpoint_map(stage_b_result)
    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_departure_config,
    )

    selected = [
        run_id
        for run_id in unresolved
        if stable_shard_index(run_id, shard_count) == shard_index
    ]
    rows: list[dict] = []
    tolerance = float(c1["observed_statistic_absolute_tolerance"])

    for run_id in sorted(selected):
        if run_id not in source_runs:
            raise ValueError(f"unresolved run missing from paired source: {run_id}")
        if run_id not in checkpoints:
            raise ValueError(f"unresolved run missing Stage-B checkpoint: {run_id}")

        run = source_runs[run_id]
        checkpoint = checkpoints[run_id]
        retained_attempts = list(run["bootstrap_attempt_statistics"])
        if len(retained_attempts) != 199:
            raise ValueError(
                f"retained unresolved run does not have 199 attempts: {run_id}"
            )

        retained_source_hash = canonical_attempt_sequence_sha256(
            retained_attempts
        )
        if retained_source_hash != str(
            checkpoint["attempt_sequence_sha256"]
        ):
            raise ValueError(
                f"paired source/checkpoint attempt hash mismatch: {run_id}"
            )

        dataset = regenerate_dataset_for_run(
            run,
            paired_config=paired_config,
            departure_cases=departure_cases,
        )
        regenerated_dataset_sha256 = dataset_fingerprint(dataset)
        retained_dataset_sha256 = str(run["dataset_sha256"])
        dataset_match = (
            regenerated_dataset_sha256 == retained_dataset_sha256
            == str(checkpoint["dataset_sha256"])
        )

        regenerated_observed, regenerated_attempts = (
            regenerate_bootstrap_attempt_statistics(
                run,
                dataset,
                paired_config=paired_config,
                draw_indices=range(199),
            )
        )
        observed_delta = abs(
            float(regenerated_observed) - float(run["observed_statistic"])
        )
        observed_match = observed_delta <= tolerance

        regenerated_attempt_hash = canonical_attempt_sequence_sha256(
            regenerated_attempts
        )
        attempt_match = (
            regenerated_attempt_hash
            == retained_source_hash
            == str(checkpoint["attempt_sequence_sha256"])
        )

        rows.append(
            {
                "run_id": run_id,
                "identity": str(run["identity"]),
                "identity_type": str(run["identity_type"]),
                "restriction": str(run["restriction"]),
                "role": str(run["role"]),
                "anchor_id": run["anchor_id"],
                "axis": run["axis"],
                "sign": run["sign"],
                "target_mean_bernoulli_kl": run[
                    "target_mean_bernoulli_kl"
                ],
                "evaluation_replicate": int(
                    run["evaluation_replicate"]
                ),
                "retained_dataset_sha256": retained_dataset_sha256,
                "regenerated_dataset_sha256": regenerated_dataset_sha256,
                "dataset_fingerprint_match": dataset_match,
                "retained_observed_statistic": float(
                    run["observed_statistic"]
                ),
                "regenerated_observed_statistic": float(
                    regenerated_observed
                ),
                "observed_statistic_absolute_delta": observed_delta,
                "observed_statistic_match": observed_match,
                "retained_attempt_sequence_sha256": retained_source_hash,
                "regenerated_attempt_sequence_sha256": (
                    regenerated_attempt_hash
                ),
                "attempt_sequence_sha256_match": attempt_match,
                "qualification_pass": (
                    dataset_match and observed_match and attempt_match
                ),
            }
        )

    return {
        "continuation_id": continuation_config["continuation_id"],
        "status": "NON_AUTHORITATIVE_STAGE_C1_REGENERATION_QUALIFICATION",
        "authoritative": False,
        "stage": "C1",
        "shard_index": shard_index,
        "shard_count": shard_count,
        "eligible_unresolved_run_count": len(unresolved),
        "qualified_run_count": len(rows),
        "qualification_pass_count": sum(
            bool(row["qualification_pass"]) for row in rows
        ),
        "all_selected_runs_pass": all(
            bool(row["qualification_pass"]) for row in rows
        ),
        "rows": rows,
        "interpretation_boundary": (
            "Stage C1 reproduces only already-retained draw indices 0..198. "
            "No new bootstrap draw index is generated and Stage C2 remains "
            "closed until all 224 unresolved streams reproduce exactly."
        ),
    }


def combine_continuation_qualification_partitions(
    partitions: list[dict],
    continuation_config: dict,
) -> dict:
    _validate_continuation_config(continuation_config)
    c1 = continuation_config["stage_c1"]
    shard_count = int(c1["shard_count"])
    if len(partitions) != shard_count:
        raise ValueError("Stage C1 partition count mismatch")

    seen_shards: set[int] = set()
    rows: list[dict] = []
    for partition in partitions:
        if partition["continuation_id"] != continuation_config[
            "continuation_id"
        ]:
            raise ValueError("Stage C1 continuation ID mismatch")
        if partition["status"] != (
            "NON_AUTHORITATIVE_STAGE_C1_REGENERATION_QUALIFICATION"
        ):
            raise ValueError("Stage C1 partition status mismatch")
        if partition["authoritative"] is not False:
            raise ValueError("Stage C1 partition became authoritative")
        if int(partition["shard_count"]) != shard_count:
            raise ValueError("Stage C1 shard-count mismatch")
        shard = int(partition["shard_index"])
        if shard in seen_shards:
            raise ValueError("duplicate Stage C1 shard")
        seen_shards.add(shard)
        rows.extend(partition["rows"])

    if seen_shards != set(range(shard_count)):
        raise ValueError("Stage C1 shard coverage incomplete")

    run_ids = [str(row["run_id"]) for row in rows]
    required = int(c1["required_match_count"])
    if len(run_ids) != required:
        raise ValueError("Stage C1 combined run count mismatch")
    if len(set(run_ids)) != required:
        raise ValueError("duplicate Stage C1 run ID")

    pass_count = sum(bool(row["qualification_pass"]) for row in rows)
    return {
        "continuation_id": continuation_config["continuation_id"],
        "status": "NON_AUTHORITATIVE_STAGE_C1_REGENERATION_QUALIFICATION_RESULT",
        "authoritative": False,
        "stage": "C1",
        "eligible_unresolved_run_count": required,
        "qualified_run_count": len(rows),
        "qualification_pass_count": pass_count,
        "qualification_failure_count": len(rows) - pass_count,
        "gate_pass": pass_count == required,
        "rows": sorted(rows, key=lambda row: str(row["run_id"])),
        "next_gate": (
            "STAGE_C2_EXACT_CONTINUATION_TO_PROSPECTIVE_CAP_10000"
            if pass_count == required
            else "BLOCKED_BY_STAGE_C1_REPRODUCTION_FAILURE"
        ),
        "interpretation_boundary": (
            "Stage C1 is reproducibility qualification only. Stage C2 may "
            "start only after 224/224 exact attempt-sequence hash matches."
        ),
    }
