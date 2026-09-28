from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json


INTERPRETATION_ID = "F1B.R2.POST_C2_SCIENTIFIC_INTERPRETATION.V1"
INTERPRETATION_STATUS = "NON_AUTHORITATIVE_POST_C2_CHARACTERIZATION_DESIGN"

REJECT = "REJECT_P_LE_ALPHA"
NOT_REJECT = "NOT_REJECT_P_GT_ALPHA"
UNRESOLVED = "SEQUENTIAL_UNRESOLVED_AT_CAP"


def canonical_json_sha256(value) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_interpretation_config(config: dict) -> None:
    if config["interpretation_id"] != INTERPRETATION_ID:
        raise ValueError("post-C2 interpretation identity changed")
    if config["status"] != INTERPRETATION_STATUS:
        raise ValueError("unsupported post-C2 interpretation status")
    if int(config["issue"]) != 249:
        raise ValueError("post-C2 interpretation issue changed")

    h2 = config["retained_h2"]
    if int(h2["expected_run_count"]) != 750:
        raise ValueError("H2 run count changed")
    if int(h2["expected_unresolved_at_199_count"]) != 224:
        raise ValueError("H2 unresolved count changed")

    c2 = config["retained_c2"]
    if int(c2["expected_target_count"]) != 224:
        raise ValueError("C2 target count changed")
    if int(c2["expected_resolved_count"]) != 201:
        raise ValueError("C2 resolved count changed")
    if int(c2["expected_unresolved_at_cap_count"]) != 23:
        raise ValueError("C2 unresolved-at-cap count changed")
    if int(c2["maximum_total_attempts"]) != 10000:
        raise ValueError("C2 cap changed")

    final = config["final_state"]
    if int(final["expected_total_run_count"]) != 750:
        raise ValueError("final run count changed")
    if int(final["expected_reject_count"]) != 246:
        raise ValueError("final reject count changed")
    if int(final["expected_not_reject_count"]) != 481:
        raise ValueError("final not-reject count changed")
    if int(final["expected_unresolved_at_cap_count"]) != 23:
        raise ValueError("final unresolved count changed")
    if set(final["allowed_terminal_states"]) != {
        REJECT,
        NOT_REJECT,
        UNRESOLVED,
    }:
        raise ValueError("final terminal states changed")

    estimands = config["estimands"]
    if estimands["unconditional_three_outcome_required"] is not True:
        raise ValueError("three-outcome estimand is required")
    if estimands["conditional_decided_only_secondary"] is not True:
        raise ValueError("decided-only quantities must remain secondary")
    if estimands["drop_unresolved_from_primary_denominator"] is not False:
        raise ValueError("unresolved streams cannot be dropped")
    if estimands["unresolved_bounds_required"] is not True:
        raise ValueError("unresolved bounds are required")
    if estimands["inferential_power_claim_authorized"] is not False:
        raise ValueError("power claims are not yet authorized")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("post-C2 interpretation boundary was weakened")


def validate_retained_results(
    h2_result: dict,
    c2_result: dict,
    config: dict,
) -> None:
    validate_interpretation_config(config)

    if h2_result["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_STAGE_B_REBUILD_COMPLETE_RETAINED"
    ):
        raise ValueError("retained H2 status changed")
    if h2_result["authoritative"] is not False:
        raise ValueError("retained H2 became authoritative")
    h2_spec = config["retained_h2"]
    if int(h2_result["integrity"]["restriction_run_count"]) != int(
        h2_spec["expected_run_count"]
    ):
        raise ValueError("retained H2 run count mismatch")
    if int(h2_result["integrity"]["unresolved_run_count"]) != int(
        h2_spec["expected_unresolved_at_199_count"]
    ):
        raise ValueError("retained H2 unresolved count mismatch")
    if str(h2_result["integrity"]["unresolved_run_ids_sha256"]) != str(
        h2_spec["unresolved_run_ids_sha256"]
    ):
        raise ValueError("retained H2 unresolved digest mismatch")

    if c2_result["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_C2_CONTINUATION_COMPLETE_RETAINED"
    ):
        raise ValueError("retained C2 status changed")
    if c2_result["authoritative"] is not False:
        raise ValueError("retained C2 became authoritative")
    c2_spec = config["retained_c2"]
    if int(c2_result["target_set"]["target_stream_count"]) != int(
        c2_spec["expected_target_count"]
    ):
        raise ValueError("retained C2 target count mismatch")
    if str(c2_result["target_set"]["target_run_ids_sha256"]) != str(
        h2_spec["unresolved_run_ids_sha256"]
    ):
        raise ValueError("retained C2 target digest mismatch")
    if int(c2_result["result"]["newly_resolved_count"]) != int(
        c2_spec["expected_resolved_count"]
    ):
        raise ValueError("retained C2 resolved count mismatch")
    if int(c2_result["result"]["unresolved_at_cap_count"]) != int(
        c2_spec["expected_unresolved_at_cap_count"]
    ):
        raise ValueError("retained C2 unresolved count mismatch")
    if str(c2_result["result"]["unresolved_at_cap_run_ids_sha256"]) != str(
        c2_spec["unresolved_at_cap_run_ids_sha256"]
    ):
        raise ValueError("retained C2 unresolved digest mismatch")
    if c2_result["decision"]["unresolved_at_cap_retained_as_unresolved"] is not True:
        raise ValueError("retained C2 unresolved semantics changed")
    if c2_result["decision"]["power_validated"] is not False:
        raise ValueError("retained C2 unexpectedly validates power")


def _unique_map(rows: list[dict], label: str) -> dict[str, dict]:
    result = {str(row["run_id"]): row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"{label} run IDs are not unique")
    return result


def _final_state_from_c2(row: dict) -> str:
    decision = row.get("decision")
    if decision is not None:
        if decision not in (REJECT, NOT_REJECT):
            raise ValueError("unsupported C2 decision")
        return str(decision)
    if row.get("status") != UNRESOLVED:
        raise ValueError("nonterminal C2 row is not unresolved-at-cap")
    return UNRESOLVED


def derive_final_rows(
    raw_h2: dict,
    raw_c2: dict,
    config: dict,
) -> list[dict]:
    validate_interpretation_config(config)

    h2_rows = list(raw_h2["replay_rows"])
    c2_rows = list(raw_c2["rows"])
    if len(h2_rows) != int(config["retained_h2"]["expected_run_count"]):
        raise ValueError("raw H2 row count changed")
    if len(c2_rows) != int(config["retained_c2"]["expected_target_count"]):
        raise ValueError("raw C2 row count changed")

    h2_map = _unique_map(h2_rows, "H2")
    c2_map = _unique_map(c2_rows, "C2")

    h2_unresolved = sorted(
        run_id
        for run_id, row in h2_map.items()
        if row.get("decision") is None
    )
    if len(h2_unresolved) != int(
        config["retained_h2"]["expected_unresolved_at_199_count"]
    ):
        raise ValueError("raw H2 unresolved count changed")
    if canonical_json_sha256(h2_unresolved) != str(
        config["retained_h2"]["unresolved_run_ids_sha256"]
    ):
        raise ValueError("raw H2 unresolved digest mismatch")
    if set(c2_map) != set(h2_unresolved):
        raise ValueError("C2 target set differs from H2 unresolved set")

    if str(raw_c2["target_run_ids_sha256"]) != str(
        config["retained_h2"]["unresolved_run_ids_sha256"]
    ):
        raise ValueError("raw C2 target digest mismatch")

    final_rows: list[dict] = []
    for run_id in sorted(h2_map):
        h2 = h2_map[run_id]
        base = {
            "run_id": run_id,
            "identity": str(h2["identity"]),
            "identity_type": str(h2["identity_type"]),
            "restriction": str(h2["restriction"]),
            "role": str(h2["role"]),
            "anchor_id": h2["anchor_id"],
            "axis": h2["axis"],
            "sign": h2["sign"],
            "target_mean_bernoulli_kl": h2["target_mean_bernoulli_kl"],
            "evaluation_replicate": int(h2["evaluation_replicate"]),
            "dataset_sha256": str(h2["dataset_sha256"]),
            "bootstrap_stream_seed": int(h2["bootstrap_stream_seed"]),
        }
        if h2.get("decision") is not None:
            if run_id in c2_map:
                raise ValueError("H2-resolved stream was extended by C2")
            final_state = str(h2["decision"])
            if final_state not in (REJECT, NOT_REJECT):
                raise ValueError("unsupported H2 terminal decision")
            base.update(
                {
                    "source_stage": "H2",
                    "final_state": final_state,
                    "final_stopping_n": int(h2["stopping_n"]),
                }
            )
        else:
            c2 = c2_map[run_id]
            if str(c2["dataset_sha256"]) != str(h2["dataset_sha256"]):
                raise ValueError("H2/C2 dataset identity mismatch")
            if int(c2["bootstrap_stream_seed"]) != int(
                h2["bootstrap_stream_seed"]
            ):
                raise ValueError("H2/C2 bootstrap seed mismatch")
            if int(c2["prior_total_attempts"]) != 199:
                raise ValueError("C2 prior attempt count changed")
            if int(c2["first_new_draw_index"]) != 199:
                raise ValueError("C2 first new draw index changed")
            base.update(
                {
                    "source_stage": "C2",
                    "final_state": _final_state_from_c2(c2),
                    "final_stopping_n": c2["stopping_n"],
                }
            )
        final_rows.append(base)

    states = Counter(row["final_state"] for row in final_rows)
    expected = config["final_state"]
    if len(final_rows) != int(expected["expected_total_run_count"]):
        raise ValueError("final row count mismatch")
    if states[REJECT] != int(expected["expected_reject_count"]):
        raise ValueError("final reject count mismatch")
    if states[NOT_REJECT] != int(expected["expected_not_reject_count"]):
        raise ValueError("final not-reject count mismatch")
    if states[UNRESOLVED] != int(expected["expected_unresolved_at_cap_count"]):
        raise ValueError("final unresolved count mismatch")

    unresolved = sorted(
        row["run_id"]
        for row in final_rows
        if row["final_state"] == UNRESOLVED
    )
    if canonical_json_sha256(unresolved) != str(
        config["retained_c2"]["unresolved_at_cap_run_ids_sha256"]
    ):
        raise ValueError("final unresolved-at-cap digest mismatch")

    return final_rows


def summarize_three_outcome(rows: list[dict]) -> dict:
    total = len(rows)
    counts = Counter(row["final_state"] for row in rows)
    reject = int(counts[REJECT])
    not_reject = int(counts[NOT_REJECT])
    unresolved = int(counts[UNRESOLVED])
    decided = reject + not_reject
    if total == 0:
        return {
            "run_count": 0,
            "reject_count": 0,
            "not_reject_count": 0,
            "unresolved_count": 0,
            "reject_proportion": None,
            "not_reject_proportion": None,
            "unresolved_proportion": None,
            "reject_proportion_bounds_with_unresolved": [None, None],
            "conditional_reject_proportion_among_decided": None,
        }
    return {
        "run_count": total,
        "reject_count": reject,
        "not_reject_count": not_reject,
        "unresolved_count": unresolved,
        "reject_proportion": reject / total,
        "not_reject_proportion": not_reject / total,
        "unresolved_proportion": unresolved / total,
        "reject_proportion_bounds_with_unresolved": [
            reject / total,
            (reject + unresolved) / total,
        ],
        "conditional_reject_proportion_among_decided": (
            reject / decided if decided else None
        ),
    }


def _aggregate_by(rows: list[dict], field: str) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        key = "NULL" if row.get(field) is None else str(row.get(field))
        groups[key].append(row)
    return [
        {field: key, **summarize_three_outcome(group)}
        for key, group in sorted(groups.items())
    ]


def _role_semantic_summary(rows: list[dict], config: dict) -> list[dict]:
    semantics = config["role_semantics"]
    detection = set(semantics["detection_roles"])
    controls = set(semantics["negative_control_roles"])
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[str(row["role"])].append(row)

    output = []
    for role, group in sorted(groups.items()):
        summary = summarize_three_outcome(group)
        if role in detection:
            semantic_kind = "DETECTION_ROLE"
            success = summary["reject_count"]
            failure = summary["not_reject_count"]
            primary_name = "detection_proportion"
        elif role in controls:
            semantic_kind = "NEGATIVE_CONTROL_ROLE"
            success = summary["not_reject_count"]
            failure = summary["reject_count"]
            primary_name = "specificity_pass_proportion"
        else:
            raise ValueError(f"role lacks declared semantics: {role}")

        total = summary["run_count"]
        unresolved = summary["unresolved_count"]
        semantic = {
            "role": role,
            "semantic_kind": semantic_kind,
            **summary,
            primary_name: success / total if total else None,
            f"{primary_name}_bounds_with_unresolved": (
                [success / total, (success + unresolved) / total]
                if total
                else [None, None]
            ),
            "semantic_failure_count": failure,
            "indeterminate_count": unresolved,
        }
        output.append(semantic)
    return output


def build_post_c2_characterization(
    raw_h2: dict,
    raw_c2: dict,
    config: dict,
) -> dict:
    rows = derive_final_rows(raw_h2, raw_c2, config)
    dimensions = list(config["aggregation_dimensions"])
    by_dimension = {
        field: _aggregate_by(rows, field)
        for field in dimensions
    }

    unresolved_rows = [
        row for row in rows if row["final_state"] == UNRESOLVED
    ]
    return {
        "interpretation_id": config["interpretation_id"],
        "status": "NON_AUTHORITATIVE_POST_C2_CHARACTERIZATION_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "global_summary": summarize_three_outcome(rows),
        "role_semantic_summary": _role_semantic_summary(rows, config),
        "by_dimension": by_dimension,
        "unresolved_at_cap": {
            "count": len(unresolved_rows),
            "run_ids_sha256": canonical_json_sha256(
                sorted(row["run_id"] for row in unresolved_rows)
            ),
            "rows": unresolved_rows,
        },
        "rows": rows,
        "interpretation_boundary": {
            "c2_rerun_performed": False,
            "c2_cap_extended": False,
            "c2_outcome_reclassified": False,
            "unresolved_dropped_from_primary_denominator": False,
            "inferential_power_claim_made": False,
            "authoritative_core_grid_frozen": False,
            "human_n_frozen": False,
            "participant_recruitment_authorized": False,
            "runtime_f1b_authorized": False,
        },
    }
