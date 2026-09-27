from __future__ import annotations

from collections import defaultdict
import hashlib
from math import sqrt

import numpy as np

from .f1b_hierarchical_recovery import RandomEffectScales
from .f1b_prehuman_recovery import R2Dataset, R2Family, simulate_r2_dataset
from .f1b_r2_restriction_recovery import (
    R2Restriction,
    bootstrap_restriction_test_prefix_snapshots,
)


def _stable_identity_words(identity: str) -> tuple[int, ...]:
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    return tuple(
        int.from_bytes(digest[offset : offset + 4], "big")
        for offset in range(0, 16, 4)
    )


def _stable_seed(identity: str) -> int:
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def dataset_fingerprint(dataset: R2Dataset) -> str:
    digest = hashlib.sha256()
    fields = (
        ("share", dataset.share, "<i8"),
        ("belief", dataset.belief, "<f8"),
        ("accuracy_cue", dataset.accuracy_cue, "<f8"),
        ("reward_context", dataset.reward_context, "<f8"),
        ("participant", dataset.participant, "<i8"),
        ("item", dataset.item, "<i8"),
    )
    for name, values, dtype in fields:
        array = np.ascontiguousarray(np.asarray(values, dtype=dtype))
        digest.update(name.encode("utf-8"))
        digest.update(np.asarray(array.shape, dtype="<i8").tobytes())
        digest.update(array.tobytes())
    return digest.hexdigest()


def _scales(config: dict, *, generator: bool) -> RandomEffectScales:
    random_effects = config["random_effects"]
    multiplier = 1.0 if generator else float(config["fit_scale_multiplier"])
    if multiplier <= 0.0:
        raise ValueError("fit_scale_multiplier must be positive")
    return RandomEffectScales(
        participant_intercept_sd=float(
            random_effects["participant_intercept_sd"]
        )
        * multiplier,
        item_intercept_sd=float(random_effects["item_intercept_sd"])
        * multiplier,
        participant_slope_sd=float(
            random_effects["participant_reward_slope_sd"]
        )
        * multiplier,
        item_slope_sd=float(
            random_effects["item_reward_slope_sd"]
        )
        * multiplier,
    )


def _simulate_dataset(
    *,
    family: R2Family,
    parameters: tuple[float, ...],
    config: dict,
    dataset_identity: str,
    evaluation_replicate: int,
) -> R2Dataset:
    design = config["design"]
    words = _stable_identity_words(dataset_identity)
    rng = np.random.default_rng(
        np.random.SeedSequence(
            [
                int(config["seed"]),
                101,
                *words,
                int(evaluation_replicate),
            ]
        )
    )
    scales = _scales(config, generator=True)
    return simulate_r2_dataset(
        family=family,
        participants=int(design["participants"]),
        items=int(design["items"]),
        belief_levels=tuple(float(x) for x in design["belief_B"]),
        accuracy_levels=tuple(float(x) for x in design["accuracy_cue_A"]),
        reward_levels=tuple(float(x) for x in design["reward_context_R"]),
        parameters=parameters,
        participant_intercept_sd=scales.participant_intercept_sd,
        item_intercept_sd=scales.item_intercept_sd,
        participant_reward_slope_sd=scales.participant_slope_sd,
        item_reward_slope_sd=scales.item_slope_sd,
        rng=rng,
        missingness_rate=float(design["missingness_rate"]),
    )


def _null_specs(config: dict) -> list[dict]:
    return [
        {
            "identity": "CBD_NULL_ANCHOR_1",
            "family": R2Family.AP_A,
            "parameters": tuple(
                float(x)
                for x in config["null_generators"]["CBD_ANCHOR_1"]
            ),
            "restriction": R2Restriction.CBD_COMPLEMENT,
            "role": "CBD_NULL_FALSE_REJECTION",
            "anchor_id": "CBD_ANCHOR_1",
        },
        {
            "identity": "CBD_NULL_ANCHOR_2",
            "family": R2Family.AP_A,
            "parameters": tuple(
                float(x)
                for x in config["null_generators"]["CBD_ANCHOR_2"]
            ),
            "restriction": R2Restriction.CBD_COMPLEMENT,
            "role": "CBD_NULL_FALSE_REJECTION",
            "anchor_id": "CBD_ANCHOR_2",
        },
        {
            "identity": "ADD_NULL",
            "family": R2Family.AP_B,
            "parameters": tuple(
                float(x) for x in config["null_generators"]["ADD_ANCHOR"]
            ),
            "restriction": R2Restriction.ADD,
            "role": "ADD_NULL_FALSE_REJECTION",
            "anchor_id": "ADD_ANCHOR",
        },
    ]


def _resolve_replicates(
    total: int,
    replicate_indices: tuple[int, ...] | None,
) -> tuple[int, ...]:
    if total <= 0:
        raise ValueError("evaluation_replicates must be positive")
    if replicate_indices is None:
        return tuple(range(total))
    if not replicate_indices:
        raise ValueError("replicate_indices must not be empty")
    values = tuple(int(value) for value in replicate_indices)
    if tuple(sorted(set(values))) != values:
        raise ValueError(
            "replicate_indices must be unique and strictly increasing"
        )
    if values[0] < 0 or values[-1] >= total:
        raise ValueError("replicate_indices lie outside the frozen design")
    return values


def _validate_config(config: dict) -> tuple[int, ...]:
    if (
        config["status"]
        != "NON_AUTHORITATIVE_R2_KL_V2_PAIRED_BOOTSTRAP_DESIGN"
    ):
        raise ValueError("unsupported paired KL v2 bootstrap design status")
    draw_grid = tuple(int(x) for x in config["bootstrap"]["draw_grid"])
    if draw_grid != (49, 99, 199):
        raise ValueError("paired draw grid must remain 49/99/199")
    if int(config["evaluation_replicates"]) != 10:
        raise ValueError("paired evaluation replicate count changed")
    pairing = config["pairing_contract"]
    required_true = (
        "dataset_seed_excludes_bootstrap_draw_count",
        "dataset_seed_excludes_total_evaluation_count",
        "dataset_seed_uses_stable_sha256_identity",
        "departure_restrictions_share_dataset",
        "bootstrap_seed_excludes_draw_count",
        "bootstrap_prefixes_nested",
        "python_hash_forbidden",
        "dataset_fingerprint_required",
    )
    if not all(bool(pairing[key]) for key in required_true):
        raise ValueError("paired bootstrap contract was weakened")
    forbidden = (
        "authoritative_bootstrap_draws_frozen",
        "authoritative_evaluation_replicates_frozen",
        "authoritative_power_validated",
        "authoritative_core_grid_frozen",
        "human_n_frozen",
        "participant_recruitment_allowed",
        "runtime_f1b_change_allowed",
    )
    if any(bool(config["execution_boundary"][key]) for key in forbidden):
        raise ValueError("paired bootstrap execution boundary violated")
    return draw_grid


def _bootstrap_seed(
    config: dict,
    *,
    dataset_id: str,
    restriction: R2Restriction,
) -> int:
    return _stable_seed(
        f"{int(config['seed'])}|BOOTSTRAP|{dataset_id}|{restriction.value}"
    )


def _snapshot_dicts(
    result,
    *,
    fit_failure: bool,
) -> list[dict]:
    if fit_failure:
        raise ValueError("fit failures are constructed separately")
    return [
        {
            "bootstrap_draws": int(snapshot.bootstrap_draws_requested),
            "bootstrap_draws_successful": int(
                snapshot.bootstrap_draws_successful
            ),
            "bootstrap_fit_failures": int(
                snapshot.bootstrap_fit_failures
            ),
            "critical_value": (
                None
                if snapshot.critical_value is None
                else float(snapshot.critical_value)
            ),
            "p_value": (
                None if snapshot.p_value is None else float(snapshot.p_value)
            ),
            "rejected": (
                None if snapshot.rejected is None else bool(snapshot.rejected)
            ),
            "bootstrap_calibration_failure": bool(
                snapshot.bootstrap_calibration_failure
            ),
        }
        for snapshot in result.snapshots
    ]


def _failed_snapshots(draw_grid: tuple[int, ...]) -> list[dict]:
    return [
        {
            "bootstrap_draws": int(draws),
            "bootstrap_draws_successful": 0,
            "bootstrap_fit_failures": 0,
            "critical_value": None,
            "p_value": None,
            "rejected": None,
            "bootstrap_calibration_failure": False,
        }
        for draws in draw_grid
    ]


def _run_restriction(
    *,
    dataset: R2Dataset,
    dataset_id: str,
    dataset_sha256: str,
    restriction: R2Restriction,
    role: str,
    identity: str,
    identity_type: str,
    anchor_id: str | None,
    axis: str | None,
    sign: int | None,
    target_mean_kl: float | None,
    achieved_mean_kl: float | None,
    nearest_add_rms: float | None,
    evaluation_replicate: int,
    config: dict,
    draw_grid: tuple[int, ...],
) -> dict:
    seed = _bootstrap_seed(
        config,
        dataset_id=dataset_id,
        restriction=restriction,
    )
    thresholds = {
        int(key): int(value)
        for key, value in config["bootstrap"][
            "minimum_successful_draws_by_draw_count"
        ].items()
    }
    try:
        result = bootstrap_restriction_test_prefix_snapshots(
            dataset,
            restriction,
            scales=_scales(config, generator=False),
            draw_counts=draw_grid,
            minimum_successful_draws_by_count=thresholds,
            seed=seed,
            alpha=float(config["bootstrap"]["alpha"]),
        )
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return {
            "run_id": (
                f"{dataset_id}|RESTRICTION={restriction.value}"
            ),
            "dataset_id": dataset_id,
            "dataset_sha256": dataset_sha256,
            "identity": identity,
            "identity_type": identity_type,
            "role": role,
            "restriction": restriction.value,
            "anchor_id": anchor_id,
            "axis": axis,
            "sign": sign,
            "target_mean_bernoulli_kl": target_mean_kl,
            "achieved_mean_bernoulli_kl": achieved_mean_kl,
            "nearest_add_rms_distance": nearest_add_rms,
            "evaluation_replicate": int(evaluation_replicate),
            "bootstrap_stream_seed": int(seed),
            "fit_failure": True,
            "observed_statistic": None,
            "held_out_participant_delta": None,
            "held_out_item_delta": None,
            "bootstrap_attempt_statistics": [],
            "snapshots": _failed_snapshots(draw_grid),
        }

    return {
        "run_id": f"{dataset_id}|RESTRICTION={restriction.value}",
        "dataset_id": dataset_id,
        "dataset_sha256": dataset_sha256,
        "identity": identity,
        "identity_type": identity_type,
        "role": role,
        "restriction": restriction.value,
        "anchor_id": anchor_id,
        "axis": axis,
        "sign": sign,
        "target_mean_bernoulli_kl": target_mean_kl,
        "achieved_mean_bernoulli_kl": achieved_mean_kl,
        "nearest_add_rms_distance": nearest_add_rms,
        "evaluation_replicate": int(evaluation_replicate),
        "bootstrap_stream_seed": int(seed),
        "fit_failure": False,
        "observed_statistic": float(result.observed_statistic),
        "held_out_participant_delta": float(
            result.held_out_participant_delta
        ),
        "held_out_item_delta": float(result.held_out_item_delta),
        "bootstrap_attempt_statistics": [
            None if value is None else float(value)
            for value in result.bootstrap_attempt_statistics
        ],
        "snapshots": _snapshot_dicts(result, fit_failure=False),
    }


def _wilson(successes: int, total: int) -> list[float]:
    if total <= 0:
        return [0.0, 1.0]
    z = 1.959963984540054
    n = float(total)
    p = float(successes) / n
    z2 = z * z
    denominator = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denominator
    half = (
        z
        * sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n)
        / denominator
    )
    return [
        max(0.0, center - half),
        min(1.0, center + half),
    ]


def _snapshot_aggregate(runs: list[dict]) -> list[dict]:
    groups: dict[tuple, list[tuple[dict, dict]]] = defaultdict(list)
    for run in runs:
        for snapshot in run["snapshots"]:
            key = (
                int(snapshot["bootstrap_draws"]),
                run["restriction"],
                run["role"],
                run["axis"],
                run["target_mean_bernoulli_kl"],
            )
            groups[key].append((run, snapshot))

    rows: list[dict] = []
    for key, values in sorted(groups.items(), key=lambda item: str(item[0])):
        total = len(values)
        fit_failures = sum(run["fit_failure"] for run, _ in values)
        calibration_failures = sum(
            snapshot["bootstrap_calibration_failure"]
            for _, snapshot in values
        )
        valid = [
            snapshot
            for run, snapshot in values
            if not run["fit_failure"]
            and not snapshot["bootstrap_calibration_failure"]
            and snapshot["rejected"] is not None
        ]
        rejected = sum(bool(snapshot["rejected"]) for snapshot in valid)
        rows.append(
            {
                "bootstrap_draws": key[0],
                "restriction": key[1],
                "role": key[2],
                "axis": key[3],
                "target_mean_bernoulli_kl": key[4],
                "snapshot_count": total,
                "valid_snapshot_count": len(valid),
                "rejections": rejected,
                "rejection_probability_all_snapshots": (
                    rejected / total if total else 0.0
                ),
                "rejection_wilson_95_all_snapshots": _wilson(
                    rejected,
                    total,
                ),
                "fit_failure_count": fit_failures,
                "bootstrap_calibration_failure_count": calibration_failures,
                "mean_bootstrap_fit_failures": (
                    float(
                        np.mean(
                            [
                                snapshot["bootstrap_fit_failures"]
                                for snapshot in valid
                            ]
                        )
                    )
                    if valid
                    else None
                ),
            }
        )
    return rows


def _comparison_rows(
    runs: list[dict],
    comparison_pairs: tuple[tuple[int, int], ...],
) -> list[dict]:
    rows: list[dict] = []
    for run in runs:
        snapshots = {
            int(row["bootstrap_draws"]): row
            for row in run["snapshots"]
        }
        for left, right in comparison_pairs:
            a = snapshots[left]
            b = snapshots[right]
            decision_valid = (
                not run["fit_failure"]
                and not a["bootstrap_calibration_failure"]
                and not b["bootstrap_calibration_failure"]
                and a["rejected"] is not None
                and b["rejected"] is not None
            )
            rows.append(
                {
                    "run_id": run["run_id"],
                    "dataset_id": run["dataset_id"],
                    "dataset_sha256": run["dataset_sha256"],
                    "restriction": run["restriction"],
                    "role": run["role"],
                    "anchor_id": run["anchor_id"],
                    "axis": run["axis"],
                    "sign": run["sign"],
                    "target_mean_bernoulli_kl": run[
                        "target_mean_bernoulli_kl"
                    ],
                    "evaluation_replicate": run[
                        "evaluation_replicate"
                    ],
                    "left_draws": left,
                    "right_draws": right,
                    "fit_failure_shared": bool(run["fit_failure"]),
                    "left_calibration_failure": bool(
                        a["bootstrap_calibration_failure"]
                    ),
                    "right_calibration_failure": bool(
                        b["bootstrap_calibration_failure"]
                    ),
                    "calibration_failure_transition": (
                        bool(a["bootstrap_calibration_failure"])
                        != bool(b["bootstrap_calibration_failure"])
                    ),
                    "decision_pair_valid": decision_valid,
                    "left_rejected": a["rejected"],
                    "right_rejected": b["rejected"],
                    "decision_concordant": (
                        None
                        if not decision_valid
                        else bool(a["rejected"]) == bool(b["rejected"])
                    ),
                    "rejection_transition": (
                        None
                        if not decision_valid
                        else (
                            "CONCORDANT"
                            if bool(a["rejected"]) == bool(b["rejected"])
                            else (
                                "REJECT_TO_NOT_REJECT"
                                if bool(a["rejected"])
                                else "NOT_REJECT_TO_REJECT"
                            )
                        )
                    ),
                    "absolute_p_value_difference": (
                        None
                        if a["p_value"] is None or b["p_value"] is None
                        else abs(float(a["p_value"]) - float(b["p_value"]))
                    ),
                    "absolute_critical_value_difference": (
                        None
                        if a["critical_value"] is None
                        or b["critical_value"] is None
                        else abs(
                            float(a["critical_value"])
                            - float(b["critical_value"])
                        )
                    ),
                    "bootstrap_fit_failure_difference": int(
                        b["bootstrap_fit_failures"]
                    )
                    - int(a["bootstrap_fit_failures"]),
                    "successful_draw_difference": int(
                        b["bootstrap_draws_successful"]
                    )
                    - int(a["bootstrap_draws_successful"]),
                }
            )
    return rows


def _paired_aggregate(comparisons: list[dict]) -> list[dict]:
    dimensions = (
        ("GLOBAL", lambda row: "ALL"),
        ("RESTRICTION", lambda row: str(row["restriction"])),
        ("ROLE", lambda row: str(row["role"])),
        ("AXIS", lambda row: str(row["axis"])),
        ("TARGET", lambda row: str(row["target_mean_bernoulli_kl"])),
        ("SIGN", lambda row: str(row["sign"])),
        ("ANCHOR", lambda row: str(row["anchor_id"])),
    )
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in comparisons:
        pair = (int(row["left_draws"]), int(row["right_draws"]))
        for dimension, value_fn in dimensions:
            groups[(pair, dimension, value_fn(row))].append(row)

    out: list[dict] = []
    for (pair, dimension, value), rows in sorted(
        groups.items(),
        key=lambda item: str(item[0]),
    ):
        valid = [row for row in rows if row["decision_pair_valid"]]
        discordant = sum(
            not bool(row["decision_concordant"]) for row in valid
        )
        p_deltas = [
            float(row["absolute_p_value_difference"])
            for row in rows
            if row["absolute_p_value_difference"] is not None
        ]
        critical_deltas = [
            float(row["absolute_critical_value_difference"])
            for row in rows
            if row["absolute_critical_value_difference"] is not None
        ]
        out.append(
            {
                "left_draws": pair[0],
                "right_draws": pair[1],
                "dimension": dimension,
                "value": value,
                "comparison_count": len(rows),
                "valid_decision_pair_count": len(valid),
                "discordant_decision_count": discordant,
                "decision_concordance_probability": (
                    (len(valid) - discordant) / len(valid)
                    if valid
                    else None
                ),
                "calibration_failure_transition_count": sum(
                    row["calibration_failure_transition"] for row in rows
                ),
                "shared_fit_failure_count": sum(
                    row["fit_failure_shared"] for row in rows
                ),
                "mean_absolute_p_value_difference": (
                    float(np.mean(p_deltas)) if p_deltas else None
                ),
                "max_absolute_p_value_difference": (
                    max(p_deltas) if p_deltas else None
                ),
                "mean_absolute_critical_value_difference": (
                    float(np.mean(critical_deltas))
                    if critical_deltas
                    else None
                ),
                "max_absolute_critical_value_difference": (
                    max(critical_deltas) if critical_deltas else None
                ),
            }
        )
    return out


def _run_sort_key(run: dict) -> tuple:
    return (
        int(run["evaluation_replicate"]),
        str(run["identity_type"]),
        str(run["identity"]),
        str(run["restriction"]),
    )


def run_paired_bootstrap_characterization(
    config: dict,
    departure_cases: list[dict],
    *,
    replicate_indices: tuple[int, ...] | None = None,
) -> dict:
    draw_grid = _validate_config(config)
    if len(departure_cases) != int(config["expected_departure_case_count"]):
        raise ValueError("unexpected qualified V2 departure case count")
    case_ids = [str(case["case_id"]) for case in departure_cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate qualified V2 case ID")

    total_replicates = int(config["evaluation_replicates"])
    active_replicates = _resolve_replicates(
        total_replicates,
        replicate_indices,
    )
    ordered_cases = sorted(departure_cases, key=lambda case: str(case["case_id"]))
    runs: list[dict] = []

    for replicate in active_replicates:
        for null in _null_specs(config):
            dataset_identity = (
                f"NULL|{null['identity']}|REPLICATE={int(replicate)}"
            )
            dataset = _simulate_dataset(
                family=null["family"],
                parameters=null["parameters"],
                config=config,
                dataset_identity=dataset_identity,
                evaluation_replicate=replicate,
            )
            fingerprint = dataset_fingerprint(dataset)
            runs.append(
                _run_restriction(
                    dataset=dataset,
                    dataset_id=dataset_identity,
                    dataset_sha256=fingerprint,
                    restriction=null["restriction"],
                    role=null["role"],
                    identity=null["identity"],
                    identity_type="NULL",
                    anchor_id=null["anchor_id"],
                    axis=None,
                    sign=None,
                    target_mean_kl=0.0,
                    achieved_mean_kl=0.0,
                    nearest_add_rms=None,
                    evaluation_replicate=replicate,
                    config=config,
                    draw_grid=draw_grid,
                )
            )

        for case in ordered_cases:
            dataset_identity = (
                f"V2|{case['case_id']}|REPLICATE={int(replicate)}"
            )
            dataset = _simulate_dataset(
                family=R2Family.AP_C,
                parameters=tuple(
                    float(value) for value in case["general_coefficients"]
                ),
                config=config,
                dataset_identity=dataset_identity,
                evaluation_replicate=replicate,
            )
            fingerprint = dataset_fingerprint(dataset)
            for restriction in (
                R2Restriction.CBD_COMPLEMENT,
                R2Restriction.ADD,
            ):
                if restriction is R2Restriction.CBD_COMPLEMENT:
                    role = "CBD_DEPARTURE_DETECTION"
                elif bool(case["add_compatibility_expected"]):
                    role = "ADD_SPECIFICITY_NEGATIVE_CONTROL"
                else:
                    role = "ADD_DEPARTURE_DIAGNOSTIC"
                runs.append(
                    _run_restriction(
                        dataset=dataset,
                        dataset_id=dataset_identity,
                        dataset_sha256=fingerprint,
                        restriction=restriction,
                        role=role,
                        identity=str(case["case_id"]),
                        identity_type="DEPARTURE",
                        anchor_id=str(case["anchor_id"]),
                        axis=str(case["axis"]),
                        sign=int(case["sign"]),
                        target_mean_kl=float(
                            case["requested_mean_bernoulli_kl"]
                        ),
                        achieved_mean_kl=float(
                            case["achieved_mean_bernoulli_kl"]
                        ),
                        nearest_add_rms=float(
                            case["nearest_add_rms_distance"]
                        ),
                        evaluation_replicate=replicate,
                        config=config,
                        draw_grid=draw_grid,
                    )
                )

    runs.sort(key=_run_sort_key)
    comparisons = _comparison_rows(
        runs,
        tuple(
            (int(pair[0]), int(pair[1]))
            for pair in config["comparison_pairs"]
        ),
    )
    unique_datasets = len({run["dataset_id"] for run in runs})
    return {
        "characterization_id": config["characterization_id"],
        "status": "NON_AUTHORITATIVE_R2_KL_V2_PAIRED_BOOTSTRAP_RESULT",
        "authoritative": False,
        "draw_grid": list(draw_grid),
        "evaluation_replicates": total_replicates,
        "execution_replicate_indices": list(active_replicates),
        "departure_case_count": len(ordered_cases),
        "unique_dataset_count": unique_datasets,
        "restriction_run_count": len(runs),
        "snapshot_count": len(runs) * len(draw_grid),
        "pair_comparison_count": len(comparisons),
        "restriction_runs": runs,
        "snapshot_aggregate": _snapshot_aggregate(runs),
        "pair_comparisons": comparisons,
        "pair_aggregate": _paired_aggregate(comparisons),
        "interpretation_boundary": (
            "Paired same-dataset bootstrap draw-stability characterization "
            "only. Draw counts and evaluation replicates remain "
            "non-authoritative design-search values. This result does not "
            "validate statistical power, freeze a core grid or human N, "
            "authorize recruitment, or change runtime F1b."
        ),
    }


def combine_paired_bootstrap_partitions(
    partitions: list[dict],
    config: dict,
) -> dict:
    if not partitions:
        raise ValueError("at least one paired partition is required")
    _validate_config(config)
    total_replicates = int(config["evaluation_replicates"])
    draw_grid = [int(x) for x in config["bootstrap"]["draw_grid"]]

    invariant_keys = (
        "characterization_id",
        "status",
        "authoritative",
        "draw_grid",
        "evaluation_replicates",
        "departure_case_count",
        "interpretation_boundary",
    )
    first = partitions[0]
    seen: set[int] = set()
    runs: list[dict] = []
    for partition in partitions:
        for key in invariant_keys:
            if partition[key] != first[key]:
                raise ValueError(f"paired partition mismatch for {key}")
        indices = tuple(
            int(value)
            for value in partition["execution_replicate_indices"]
        )
        resolved = _resolve_replicates(total_replicates, indices)
        overlap = seen.intersection(resolved)
        if overlap:
            raise ValueError(
                f"replicate overlap across paired partitions: {sorted(overlap)}"
            )
        seen.update(resolved)
        runs.extend(partition["restriction_runs"])

    expected = set(range(total_replicates))
    if seen != expected:
        raise ValueError(
            f"paired partition coverage incomplete: missing={sorted(expected-seen)}"
        )

    run_ids = [str(run["run_id"]) for run in runs]
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("duplicate paired restriction run")

    expected_runs = int(config["expected_restriction_runs"])
    if len(runs) != expected_runs:
        raise ValueError(
            f"unexpected paired restriction-run count: {len(runs)}"
        )
    unique_datasets = len({run["dataset_id"] for run in runs})
    if unique_datasets != int(config["expected_unique_datasets"]):
        raise ValueError("unexpected paired unique-dataset count")

    for run in runs:
        if len(run["snapshots"]) != len(draw_grid):
            raise ValueError("paired run has incomplete draw snapshots")
        if [int(x["bootstrap_draws"]) for x in run["snapshots"]] != draw_grid:
            raise ValueError("paired run draw snapshot grid mismatch")

    runs.sort(key=_run_sort_key)
    comparisons = _comparison_rows(
        runs,
        tuple(
            (int(pair[0]), int(pair[1]))
            for pair in config["comparison_pairs"]
        ),
    )
    if len(comparisons) != int(config["expected_pair_comparison_count"]):
        raise ValueError("unexpected paired comparison count")

    return {
        "characterization_id": first["characterization_id"],
        "status": first["status"],
        "authoritative": False,
        "draw_grid": draw_grid,
        "evaluation_replicates": total_replicates,
        "execution_replicate_indices": list(range(total_replicates)),
        "departure_case_count": first["departure_case_count"],
        "unique_dataset_count": unique_datasets,
        "restriction_run_count": len(runs),
        "snapshot_count": len(runs) * len(draw_grid),
        "pair_comparison_count": len(comparisons),
        "restriction_runs": runs,
        "snapshot_aggregate": _snapshot_aggregate(runs),
        "pair_comparisons": comparisons,
        "pair_aggregate": _paired_aggregate(comparisons),
        "interpretation_boundary": first["interpretation_boundary"],
    }
