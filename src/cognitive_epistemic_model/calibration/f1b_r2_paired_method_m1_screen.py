from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from typing import Any

import numpy as np

from . import f1b_r2_paired_bootstrap_characterization as paired
from .f1b_hierarchical_recovery import RandomEffectScales
from .f1b_prehuman_recovery import R2Dataset, R2Family
from .f1b_r2_population_restriction_recovery import (
    bootstrap_population_restriction_test_prefix_snapshots,
)
from .f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
)
from .f1b_r2_restriction_recovery import (
    R2Restriction,
    bootstrap_restriction_test_prefix_snapshots,
)


DESIGN_ID = "F1B.R2.PAIRED_METHOD_M1_SCREEN.V1"
STATUS = "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SCREEN_DESIGN"
EXPECTED_METHODS = (
    "POPULATION",
    "HIERARCHICAL_0.5X",
    "HIERARCHICAL_1X",
    "HIERARCHICAL_2X",
)
EXPECTED_ROLES = {
    "ADD_NULL_FALSE_REJECTION",
    "CBD_NULL_FALSE_REJECTION",
    "ADD_SPECIFICITY_NEGATIVE_CONTROL",
    "ADD_DEPARTURE_DIAGNOSTIC",
    "CBD_DEPARTURE_DETECTION",
}


@dataclass(frozen=True)
class M1ScientificSpec:
    template_run_id: str
    identity: str
    identity_type: str
    restriction: str
    role: str
    anchor_id: str | None
    axis: str | None
    sign: int | None
    target_mean_bernoulli_kl: float | None
    dataset_id_prefix: str
    replicate_count: int


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_m1_config(config: dict) -> None:
    if config["design_id"] != DESIGN_ID:
        raise ValueError("M1 design identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported M1 design status")
    if int(config["issue"]) != 259:
        raise ValueError("M1 issue changed")

    methods = config["methods"]
    if tuple(str(row["id"]) for row in methods) != EXPECTED_METHODS:
        raise ValueError("M1 method order/set changed")
    expected_scales = {
        "POPULATION": None,
        "HIERARCHICAL_0.5X": 0.5,
        "HIERARCHICAL_1X": 1.0,
        "HIERARCHICAL_2X": 2.0,
    }
    for row in methods:
        actual = row["fit_scale_multiplier"]
        expected = expected_scales[str(row["id"])]
        if expected is None:
            if actual is not None or row["kind"] != "POPULATION":
                raise ValueError("population M1 method definition changed")
        elif float(actual) != expected or row["kind"] != "HIERARCHICAL":
            raise ValueError("hierarchical M1 method definition changed")

    if tuple(float(x) for x in config["missingness_regimes"]) != (0.0, 0.15):
        raise ValueError("M1 missingness regimes changed")

    design = config["scientific_design"]
    if int(design["expected_departure_cell_count"]) != 72:
        raise ValueError("M1 departure cell count changed")
    if int(design["departure_replicates_per_cell"]) != 5:
        raise ValueError("M1 departure replicate count changed")
    if tuple(int(x) for x in design["departure_replicate_indices"]) != tuple(
        range(5)
    ):
        raise ValueError("M1 departure replicate indices changed")
    if int(design["null_replicates_per_identity"]) != 20:
        raise ValueError("M1 null replicate count changed")
    if tuple(int(x) for x in design["null_replicate_indices"]) != tuple(
        range(20)
    ):
        raise ValueError("M1 null replicate indices changed")
    if tuple(str(x) for x in design["null_identities"]) != (
        "ADD_NULL",
        "CBD_NULL_ANCHOR_1",
        "CBD_NULL_ANCHOR_2",
    ):
        raise ValueError("M1 null identities changed")
    if int(design["restriction_runs_per_missingness"]) != 420:
        raise ValueError("M1 restriction runs/missingness changed")
    if int(design["total_scientific_restriction_runs"]) != 840:
        raise ValueError("M1 total scientific restriction runs changed")
    if int(design["total_method_executions"]) != 3360:
        raise ValueError("M1 total method executions changed")

    bootstrap = config["bootstrap"]
    if int(bootstrap["attempted_draws"]) != 199:
        raise ValueError("M1 bootstrap prefix changed")
    if int(bootstrap["minimum_successful_draws"]) != 180:
        raise ValueError("M1 bootstrap success threshold changed")
    if float(bootstrap["alpha"]) != 0.05:
        raise ValueError("M1 alpha changed")
    if bootstrap["continuation_beyond_198_allowed"] is not False:
        raise ValueError("M1 cannot continue beyond draw 198")
    if bootstrap["decision_label"] != "FIXED_199_SCREEN_ONLY":
        raise ValueError("M1 decision semantics changed")

    eligibility = config["eligibility"]
    if float(
        eligibility["operational"]["maximum_overall_failure_proportion"]
    ) != 0.02:
        raise ValueError("M1 operational overall threshold changed")
    if float(
        eligibility["operational"][
            "maximum_role_missingness_failure_proportion"
        ]
    ) != 0.05:
        raise ValueError("M1 operational stratum threshold changed")
    if float(
        eligibility["null_false_rejection"][
            "maximum_pooled_proportion_per_missingness"
        ]
    ) != 0.15:
        raise ValueError("M1 null pooled threshold changed")
    if int(
        eligibility["null_false_rejection"][
            "maximum_count_per_20_rep_identity"
        ]
    ) != 5:
        raise ValueError("M1 null identity threshold changed")
    if float(
        eligibility["add_specificity"][
            "maximum_pooled_false_rejection_proportion_per_missingness"
        ]
    ) != 0.20:
        raise ValueError("M1 specificity pooled threshold changed")
    if float(
        eligibility["add_specificity"][
            "maximum_false_rejection_proportion_per_kl"
        ]
    ) != 0.30:
        raise ValueError("M1 specificity KL threshold changed")
    if float(eligibility["strong_departure_signal"]["kl"]) != 0.003:
        raise ValueError("M1 strong KL changed")
    if float(
        eligibility["strong_departure_signal"][
            "minimum_margin_above_same_regime_pooled_null_false_rejection"
        ]
    ) != 0.10:
        raise ValueError("M1 signal margin changed")
    degradation = eligibility["missingness_degradation"]
    if float(degradation["maximum_null_false_rejection_increase"]) != 0.10:
        raise ValueError("M1 null missingness threshold changed")
    if float(
        degradation["maximum_specificity_false_rejection_increase"]
    ) != 0.10:
        raise ValueError("M1 specificity missingness threshold changed")
    if float(
        degradation["maximum_strong_departure_expected_direction_decrease"]
    ) != 0.20:
        raise ValueError("M1 signal missingness threshold changed")
    if float(
        eligibility["hierarchical_scale_sensitivity"][
            "flag_threshold_max_minus_min_expected_direction_rate"
        ]
    ) != 0.20:
        raise ValueError("M1 scale sensitivity threshold changed")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("M1 scientific boundary was weakened")


def _dataset_prefix(dataset_id: str) -> str:
    marker = "|REPLICATE="
    if marker not in dataset_id:
        raise ValueError("source dataset ID lacks replicate marker")
    return dataset_id.rsplit(marker, 1)[0]


def select_scientific_specs(source: dict, config: dict) -> list[M1ScientificSpec]:
    validate_m1_config(config)
    templates: dict[tuple[str, str], dict] = {}
    for run in source["restriction_runs"]:
        if int(run["evaluation_replicate"]) != 0:
            continue
        key = (str(run["identity"]), str(run["restriction"]))
        if key in templates:
            raise ValueError("duplicate replicate-zero M1 template")
        templates[key] = run

    specs: list[M1ScientificSpec] = []
    departure_cells: set[tuple[Any, ...]] = set()
    null_identities: set[str] = set()
    roles: set[str] = set()

    for run in templates.values():
        role = str(run["role"])
        roles.add(role)
        identity_type = str(run["identity_type"])
        if identity_type == "NULL":
            replicate_count = 20
            null_identities.add(str(run["identity"]))
        elif identity_type == "DEPARTURE":
            replicate_count = 5
            departure_cells.add(
                (
                    role,
                    run["axis"],
                    run["target_mean_bernoulli_kl"],
                    run["sign"],
                    run["anchor_id"],
                )
            )
        else:
            raise ValueError("unsupported M1 identity type")

        specs.append(
            M1ScientificSpec(
                template_run_id=str(run["run_id"]),
                identity=str(run["identity"]),
                identity_type=identity_type,
                restriction=str(run["restriction"]),
                role=role,
                anchor_id=run["anchor_id"],
                axis=run["axis"],
                sign=run["sign"],
                target_mean_bernoulli_kl=run["target_mean_bernoulli_kl"],
                dataset_id_prefix=_dataset_prefix(str(run["dataset_id"])),
                replicate_count=replicate_count,
            )
        )

    if roles != EXPECTED_ROLES:
        raise ValueError("M1 role coverage changed")
    if null_identities != set(
        str(x) for x in config["scientific_design"]["null_identities"]
    ):
        raise ValueError("M1 null identity coverage changed")
    if len(departure_cells) != 72:
        raise ValueError("M1 departure cell coverage changed")
    if len(specs) != 75:
        raise ValueError("M1 scientific restriction-cell count changed")

    expected_runs = sum(spec.replicate_count for spec in specs)
    if expected_runs != 420:
        raise ValueError("M1 planned restriction runs/missingness changed")
    return sorted(
        specs,
        key=lambda spec: (spec.identity, spec.restriction),
    )


def dataset_id_for(spec: M1ScientificSpec, replicate: int) -> str:
    index = int(replicate)
    if not 0 <= index < int(spec.replicate_count):
        raise ValueError("M1 replicate outside frozen spec")
    return f"{spec.dataset_id_prefix}|REPLICATE={index}"


def _generator_definition(
    spec: M1ScientificSpec,
    *,
    paired_config: dict,
    departure_cases: dict[str, dict],
) -> tuple[R2Family, tuple[float, ...]]:
    if spec.identity_type == "NULL":
        nulls = {
            str(row["identity"]): row
            for row in paired._null_specs(paired_config)
        }
        if spec.identity not in nulls:
            raise ValueError("unknown M1 null identity")
        row = nulls[spec.identity]
        return row["family"], tuple(float(x) for x in row["parameters"])
    if spec.identity_type == "DEPARTURE":
        if spec.identity not in departure_cases:
            raise ValueError("unknown M1 departure identity")
        return (
            R2Family.AP_C,
            tuple(
                float(x)
                for x in departure_cases[spec.identity]["general_coefficients"]
            ),
        )
    raise ValueError("unsupported M1 identity type")


def simulate_paired_missingness_datasets(
    spec: M1ScientificSpec,
    replicate: int,
    *,
    paired_config: dict,
    departure_cases: dict[str, dict],
) -> tuple[R2Dataset, R2Dataset]:
    family, parameters = _generator_definition(
        spec,
        paired_config=paired_config,
        departure_cases=departure_cases,
    )
    dataset_id = dataset_id_for(spec, replicate)

    complete_config = deepcopy(paired_config)
    complete_config["design"]["missingness_rate"] = 0.0
    missing_config = deepcopy(paired_config)
    missing_config["design"]["missingness_rate"] = 0.15

    complete = paired._simulate_dataset(
        family=family,
        parameters=parameters,
        config=complete_config,
        dataset_identity=dataset_id,
        evaluation_replicate=int(replicate),
    )
    missing = paired._simulate_dataset(
        family=family,
        parameters=parameters,
        config=missing_config,
        dataset_identity=dataset_id,
        evaluation_replicate=int(replicate),
    )
    assert_missingness_subset(complete, missing)
    return complete, missing


def assert_missingness_subset(
    complete: R2Dataset,
    missing: R2Dataset,
) -> None:
    complete_index = {
        (int(p), int(i)): index
        for index, (p, i) in enumerate(
            zip(complete.participant, complete.item, strict=True)
        )
    }
    if len(complete_index) != complete.share.size:
        raise ValueError("complete M1 participant/item pairs are not unique")
    for j, (participant, item) in enumerate(
        zip(missing.participant, missing.item, strict=True)
    ):
        key = (int(participant), int(item))
        if key not in complete_index:
            raise ValueError("missingness dataset is not subset of complete data")
        i = complete_index[key]
        if int(missing.share[j]) != int(complete.share[i]):
            raise ValueError("missingness changed response value")
        if float(missing.belief[j]) != float(complete.belief[i]):
            raise ValueError("missingness changed belief value")
        if float(missing.accuracy_cue[j]) != float(complete.accuracy_cue[i]):
            raise ValueError("missingness changed accuracy value")
        if float(missing.reward_context[j]) != float(complete.reward_context[i]):
            raise ValueError("missingness changed reward value")


def hierarchical_scales(
    paired_config: dict,
    multiplier: float,
) -> RandomEffectScales:
    base = paired._scales(paired_config, generator=False)
    value = float(multiplier)
    return RandomEffectScales(
        participant_intercept_sd=base.participant_intercept_sd * value,
        item_intercept_sd=base.item_intercept_sd * value,
        participant_slope_sd=base.participant_slope_sd * value,
        item_slope_sd=base.item_slope_sd * value,
    )


def bootstrap_seed_for(
    spec: M1ScientificSpec,
    replicate: int,
    *,
    paired_config: dict,
) -> int:
    return paired._bootstrap_seed(
        paired_config,
        dataset_id=dataset_id_for(spec, replicate),
        restriction=R2Restriction(spec.restriction),
    )


def run_method_prefix(
    dataset: R2Dataset,
    *,
    spec: M1ScientificSpec,
    replicate: int,
    method_id: str,
    paired_config: dict,
    config: dict,
) -> dict:
    validate_m1_config(config)
    if method_id not in EXPECTED_METHODS:
        raise ValueError("unknown M1 inference method")
    restriction = R2Restriction(spec.restriction)
    seed = bootstrap_seed_for(
        spec,
        replicate,
        paired_config=paired_config,
    )
    draws = int(config["bootstrap"]["attempted_draws"])
    minimum = int(config["bootstrap"]["minimum_successful_draws"])
    alpha = float(config["bootstrap"]["alpha"])

    try:
        if method_id == "POPULATION":
            result = bootstrap_population_restriction_test_prefix_snapshots(
                dataset,
                restriction,
                draw_counts=(draws,),
                minimum_successful_draws_by_count={draws: minimum},
                seed=seed,
                alpha=alpha,
            )
        else:
            multiplier = {
                "HIERARCHICAL_0.5X": 0.5,
                "HIERARCHICAL_1X": 1.0,
                "HIERARCHICAL_2X": 2.0,
            }[method_id]
            result = bootstrap_restriction_test_prefix_snapshots(
                dataset,
                restriction,
                scales=hierarchical_scales(paired_config, multiplier),
                draw_counts=(draws,),
                minimum_successful_draws_by_count={draws: minimum},
                seed=seed,
                alpha=alpha,
            )
    except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
        return {
            "fit_failure": True,
            "failure_type": type(exc).__name__,
            "failure_message": str(exc),
            "observed_statistic": None,
            "bootstrap_attempt_statistics": [],
            "bootstrap_draws_successful": 0,
            "bootstrap_fit_failures": 0,
            "bootstrap_calibration_failure": True,
            "p_value": None,
            "rejected": None,
            "held_out_participant_delta": None,
            "held_out_item_delta": None,
        }

    snapshot = result.snapshots[0]
    return {
        "fit_failure": False,
        "failure_type": None,
        "failure_message": None,
        "observed_statistic": float(result.observed_statistic),
        "bootstrap_attempt_statistics": [
            None if value is None else float(value)
            for value in result.bootstrap_attempt_statistics
        ],
        "bootstrap_draws_successful": int(
            snapshot.bootstrap_draws_successful
        ),
        "bootstrap_fit_failures": int(snapshot.bootstrap_fit_failures),
        "bootstrap_calibration_failure": bool(
            snapshot.bootstrap_calibration_failure
        ),
        "p_value": (
            None if snapshot.p_value is None else float(snapshot.p_value)
        ),
        "rejected": (
            None if snapshot.rejected is None else bool(snapshot.rejected)
        ),
        "held_out_participant_delta": float(
            result.held_out_participant_delta
        ),
        "held_out_item_delta": float(result.held_out_item_delta),
    }


def _rate(rows: list[dict], predicate) -> float:
    if not rows:
        raise ValueError("M1 rate denominator is empty")
    return sum(bool(predicate(row)) for row in rows) / len(rows)


def _is_failure(row: dict) -> bool:
    return bool(row["fit_failure"]) or bool(
        row["bootstrap_calibration_failure"]
    )


def _false_reject(row: dict) -> bool:
    return (not _is_failure(row)) and row["rejected"] is True


def _expected_direction(row: dict) -> bool:
    if _is_failure(row):
        return False
    role = str(row["role"])
    if role in (
        "ADD_NULL_FALSE_REJECTION",
        "CBD_NULL_FALSE_REJECTION",
        "ADD_SPECIFICITY_NEGATIVE_CONTROL",
    ):
        return row["rejected"] is False
    if role in (
        "ADD_DEPARTURE_DIAGNOSTIC",
        "CBD_DEPARTURE_DETECTION",
    ):
        return row["rejected"] is True
    raise ValueError("unknown M1 role semantics")


def evaluate_method(rows: list[dict], config: dict, method_id: str) -> dict:
    validate_m1_config(config)
    selected = [row for row in rows if row["inference_method"] == method_id]
    if len(selected) != 840:
        raise ValueError(f"M1 method {method_id} does not have 840 rows")

    failures = [row for row in selected if _is_failure(row)]
    overall_failure_rate = len(failures) / len(selected)

    operational_pass = (
        overall_failure_rate
        <= float(
            config["eligibility"]["operational"][
                "maximum_overall_failure_proportion"
            ]
        )
    )
    role_missingness_failures = []
    for role in sorted(EXPECTED_ROLES):
        for missingness in (0.0, 0.15):
            group = [
                row for row in selected
                if row["role"] == role
                and float(row["missingness_rate"]) == missingness
            ]
            if not group:
                raise ValueError("empty M1 role/missingness stratum")
            rate = _rate(group, _is_failure)
            role_missingness_failures.append(
                {
                    "role": role,
                    "missingness_rate": missingness,
                    "failure_rate": rate,
                }
            )
            operational_pass = operational_pass and rate <= float(
                config["eligibility"]["operational"][
                    "maximum_role_missingness_failure_proportion"
                ]
            )

    null_stats = []
    null_pass = True
    for missingness in (0.0, 0.15):
        pooled = [
            row for row in selected
            if row["identity_type"] == "NULL"
            and float(row["missingness_rate"]) == missingness
        ]
        if len(pooled) != 60:
            raise ValueError("M1 pooled null denominator changed")
        pooled_rate = _rate(pooled, _false_reject)
        null_stats.append(
            {
                "missingness_rate": missingness,
                "pooled_count": len(pooled),
                "false_reject_count": sum(_false_reject(row) for row in pooled),
                "false_reject_rate": pooled_rate,
            }
        )
        null_pass = null_pass and pooled_rate <= float(
            config["eligibility"]["null_false_rejection"][
                "maximum_pooled_proportion_per_missingness"
            ]
        )
        for identity in config["scientific_design"]["null_identities"]:
            identity_rows = [
                row for row in pooled if row["identity"] == identity
            ]
            if len(identity_rows) != 20:
                raise ValueError("M1 null identity denominator changed")
            false_count = sum(_false_reject(row) for row in identity_rows)
            null_pass = null_pass and false_count <= int(
                config["eligibility"]["null_false_rejection"][
                    "maximum_count_per_20_rep_identity"
                ]
            )

    specificity_stats = []
    specificity_pass = True
    for missingness in (0.0, 0.15):
        pooled = [
            row for row in selected
            if row["role"] == "ADD_SPECIFICITY_NEGATIVE_CONTROL"
            and float(row["missingness_rate"]) == missingness
        ]
        if len(pooled) != 60:
            raise ValueError("M1 specificity denominator changed")
        pooled_rate = _rate(pooled, _false_reject)
        specificity_stats.append(
            {
                "missingness_rate": missingness,
                "false_reject_count": sum(_false_reject(row) for row in pooled),
                "false_reject_rate": pooled_rate,
            }
        )
        specificity_pass = specificity_pass and pooled_rate <= float(
            config["eligibility"]["add_specificity"][
                "maximum_pooled_false_rejection_proportion_per_missingness"
            ]
        )
        for kl in (0.001, 0.002, 0.003):
            kl_rows = [
                row for row in pooled
                if float(row["target_mean_bernoulli_kl"]) == kl
            ]
            if len(kl_rows) != 20:
                raise ValueError("M1 specificity KL denominator changed")
            specificity_pass = specificity_pass and _rate(
                kl_rows, _false_reject
            ) <= float(
                config["eligibility"]["add_specificity"][
                    "maximum_false_rejection_proportion_per_kl"
                ]
            )

    signal_stats = []
    signal_pass = True
    for missingness in (0.0, 0.15):
        null_rate = next(
            row["false_reject_rate"]
            for row in null_stats
            if row["missingness_rate"] == missingness
        )
        for role in config["eligibility"]["strong_departure_signal"]["roles"]:
            group = [
                row for row in selected
                if row["role"] == role
                and float(row["missingness_rate"]) == missingness
                and float(row["target_mean_bernoulli_kl"]) == 0.003
            ]
            expected_count = 60 if role == "CBD_DEPARTURE_DETECTION" else 40
            if len(group) != expected_count:
                raise ValueError("M1 strong-departure denominator changed")
            rate = _rate(group, _expected_direction)
            margin = rate - null_rate
            signal_stats.append(
                {
                    "role": role,
                    "missingness_rate": missingness,
                    "expected_direction_rate": rate,
                    "null_false_reject_rate": null_rate,
                    "margin": margin,
                }
            )
            signal_pass = signal_pass and margin >= float(
                config["eligibility"]["strong_departure_signal"][
                    "minimum_margin_above_same_regime_pooled_null_false_rejection"
                ]
            )

    degradation = config["eligibility"]["missingness_degradation"]
    null0 = next(x["false_reject_rate"] for x in null_stats if x["missingness_rate"] == 0.0)
    null15 = next(x["false_reject_rate"] for x in null_stats if x["missingness_rate"] == 0.15)
    spec0 = next(x["false_reject_rate"] for x in specificity_stats if x["missingness_rate"] == 0.0)
    spec15 = next(x["false_reject_rate"] for x in specificity_stats if x["missingness_rate"] == 0.15)
    missingness_pass = (
        null15 - null0
        <= float(degradation["maximum_null_false_rejection_increase"])
        and spec15 - spec0
        <= float(
            degradation["maximum_specificity_false_rejection_increase"]
        )
    )
    signal_degradation = []
    for role in config["eligibility"]["strong_departure_signal"]["roles"]:
        rate0 = next(
            x["expected_direction_rate"]
            for x in signal_stats
            if x["role"] == role and x["missingness_rate"] == 0.0
        )
        rate15 = next(
            x["expected_direction_rate"]
            for x in signal_stats
            if x["role"] == role and x["missingness_rate"] == 0.15
        )
        drop = rate0 - rate15
        signal_degradation.append({"role": role, "drop": drop})
        missingness_pass = missingness_pass and drop <= float(
            degradation[
                "maximum_strong_departure_expected_direction_decrease"
            ]
        )

    if not operational_pass:
        state = "M1_INELIGIBLE_OPERATIONAL"
    elif not (null_pass and specificity_pass):
        state = "M1_INELIGIBLE_NULL_OR_SPECIFICITY"
    elif not signal_pass:
        state = "M1_INELIGIBLE_SIGNAL_SEPARATION"
    elif not missingness_pass:
        state = "M1_INELIGIBLE_MISSINGNESS"
    else:
        state = "M1_ELIGIBLE"

    return {
        "inference_method": method_id,
        "decision_state": state,
        "overall_failure_rate": overall_failure_rate,
        "role_missingness_failure_rates": role_missingness_failures,
        "null": null_stats,
        "specificity": specificity_stats,
        "strong_departure": signal_stats,
        "missingness_signal_degradation": signal_degradation,
        "checks": {
            "operational_pass": operational_pass,
            "null_pass": null_pass,
            "specificity_pass": specificity_pass,
            "signal_pass": signal_pass,
            "missingness_pass": missingness_pass,
        },
    }


def evaluate_all_methods(rows: list[dict], config: dict) -> dict:
    validate_m1_config(config)
    if len(rows) != 3360:
        raise ValueError("M1 combined row count changed")
    method_results = [
        evaluate_method(rows, config, method)
        for method in EXPECTED_METHODS
    ]

    scale_threshold = float(
        config["eligibility"]["hierarchical_scale_sensitivity"][
            "flag_threshold_max_minus_min_expected_direction_rate"
        ]
    )
    scale_details = []
    scale_sensitive = False
    for missingness in (0.0, 0.15):
        strata = (
            ("ADD_SPECIFICITY_NEGATIVE_CONTROL", None),
            ("CBD_DEPARTURE_DETECTION", 0.003),
            ("ADD_DEPARTURE_DIAGNOSTIC", 0.003),
        )
        for role, kl in strata:
            rates = {}
            for method in (
                "HIERARCHICAL_0.5X",
                "HIERARCHICAL_1X",
                "HIERARCHICAL_2X",
            ):
                group = [
                    row for row in rows
                    if row["inference_method"] == method
                    and row["role"] == role
                    and float(row["missingness_rate"]) == missingness
                    and (
                        kl is None
                        or float(row["target_mean_bernoulli_kl"]) == kl
                    )
                ]
                if not group:
                    raise ValueError("empty M1 scale-sensitivity stratum")
                rates[method] = _rate(group, _expected_direction)
            spread = max(rates.values()) - min(rates.values())
            scale_details.append(
                {
                    "role": role,
                    "target_mean_bernoulli_kl": kl,
                    "missingness_rate": missingness,
                    "rates": rates,
                    "max_minus_min": spread,
                }
            )
            scale_sensitive = scale_sensitive or spread > scale_threshold

    eligible = [
        row["inference_method"]
        for row in method_results
        if row["decision_state"] == "M1_ELIGIBLE"
    ]
    if eligible:
        overall = "M1_HAS_ELIGIBLE_METHODS"
    else:
        overall = "M1_NO_ELIGIBLE_METHOD_INFERENCE_REDESIGN_REQUIRED"

    return {
        "design_id": config["design_id"],
        "status": "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SCREEN_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "method_results": method_results,
        "eligible_methods": eligible,
        "hierarchical_scale_sensitive": scale_sensitive,
        "hierarchical_scale_sensitivity": scale_details,
        "overall_decision": overall,
        "boundary": dict(config["boundary"]),
    }
