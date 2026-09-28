from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from typing import Any


INTERPRETATION_ID = "F1B.R2.HOMOGENEOUS_TERMINAL_PARTITION.V1"
INTERPRETATION_STATUS = (
    "NON_AUTHORITATIVE_TERMINAL_PARTITION_INTERPRETATION_DESIGN"
)
EXPECTED_TOTAL = 750
EXPECTED_TERMINAL_DECISIONS = 727
EXPECTED_H2_RESOLVED = 526
EXPECTED_C2_TARGETS = 224
EXPECTED_C2_RESOLVED = 201
EXPECTED_TERMINAL_DECISIONS = EXPECTED_H2_RESOLVED + EXPECTED_C2_RESOLVED
EXPECTED_UNRESOLVED_AT_CAP = 23

EXPECTED_ROLES = {
    "CBD_NULL_FALSE_REJECTION",
    "ADD_NULL_FALSE_REJECTION",
    "CBD_DEPARTURE_DETECTION",
    "ADD_SPECIFICITY_NEGATIVE_CONTROL",
    "ADD_DEPARTURE_DIAGNOSTIC",
}


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_terminal_partition_config(config: dict) -> None:
    if config["interpretation_id"] != INTERPRETATION_ID:
        raise ValueError("terminal-partition identity changed")
    if config["status"] != INTERPRETATION_STATUS:
        raise ValueError("terminal-partition status changed")
    if int(config["issue"]) != 250:
        raise ValueError("terminal-partition issue changed")

    terminal = config["terminal_partition"]
    if int(terminal["expected_total_run_count"]) != EXPECTED_TOTAL:
        raise ValueError("terminal total-run count changed")
    if int(terminal["expected_terminal_decision_count"]) != (
        EXPECTED_TERMINAL_DECISIONS
    ):
        raise ValueError("terminal decision count changed")
    if int(terminal["expected_unresolved_at_cap_count"]) != (
        EXPECTED_UNRESOLVED_AT_CAP
    ):
        raise ValueError("terminal unresolved-at-cap count changed")
    if int(terminal["expected_bootstrap_refit_failure_count"]) != 0:
        raise ValueError("terminal refit-failure expectation changed")
    if int(terminal["h2_resolved_source_count"]) != EXPECTED_H2_RESOLVED:
        raise ValueError("H2 resolved source count changed")
    if int(terminal["c2_resolved_source_count"]) != EXPECTED_C2_RESOLVED:
        raise ValueError("C2 resolved source count changed")
    if int(terminal["c2_unresolved_source_count"]) != (
        EXPECTED_UNRESOLVED_AT_CAP
    ):
        raise ValueError("C2 unresolved source count changed")

    roles = config["semantic_roles"]
    if set(roles) != EXPECTED_ROLES:
        raise ValueError("terminal semantic-role set changed")

    expected = {
        "CBD_NULL_FALSE_REJECTION": (
            "CBD_COMPLEMENT_RESTRICTION",
            "NOT_REJECT_P_GT_ALPHA",
        ),
        "ADD_NULL_FALSE_REJECTION": (
            "ADD_RESTRICTION",
            "NOT_REJECT_P_GT_ALPHA",
        ),
        "CBD_DEPARTURE_DETECTION": (
            "CBD_COMPLEMENT_RESTRICTION",
            "REJECT_P_LE_ALPHA",
        ),
        "ADD_SPECIFICITY_NEGATIVE_CONTROL": (
            "ADD_RESTRICTION",
            "NOT_REJECT_P_GT_ALPHA",
        ),
        "ADD_DEPARTURE_DIAGNOSTIC": (
            "ADD_RESTRICTION",
            "REJECT_P_LE_ALPHA",
        ),
    }
    for role, (restriction, decision) in expected.items():
        if roles[role]["restriction"] != restriction:
            raise ValueError(f"semantic restriction changed for {role}")
        if roles[role]["expected_decision"] != decision:
            raise ValueError(f"semantic expected decision changed for {role}")

    characterization = config["characterization"]
    if characterization["impute_unresolved"] is not False:
        raise ValueError("unresolved terminal decisions cannot be imputed")
    required_groups = (
        "restriction",
        "role",
        "axis",
        "target_mean_bernoulli_kl",
        "sign",
        "anchor_id",
        "evaluation_replicate",
    )
    if tuple(characterization["group_fields"]) != required_groups:
        raise ValueError("terminal characterization grouping changed")

    if any(bool(value) for value in config["execution_boundary"].values()):
        raise ValueError("terminal interpretation boundary weakened")


def _validate_h2_raw(h2: dict, config: dict) -> dict[str, dict]:
    spec = config["h2_stage_b"]
    if h2["status"] != "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE":
        raise ValueError("H2 raw replay status changed")
    if h2["authoritative"] is not False:
        raise ValueError("H2 raw replay became authoritative")
    if int(h2["restriction_run_count"]) != int(spec["expected_run_count"]):
        raise ValueError("H2 raw replay run count changed")
    if int(h2["bootstrap_refit_failure_count"]) != 0:
        raise ValueError("H2 raw replay contains bootstrap refit failures")

    rows = {str(row["run_id"]): row for row in h2["replay_rows"]}
    if len(rows) != int(spec["expected_run_count"]):
        raise ValueError("H2 raw replay run IDs are not unique")

    resolved = [row for row in rows.values() if row["decision"] is not None]
    unresolved = sorted(
        run_id for run_id, row in rows.items() if row["decision"] is None
    )
    if len(resolved) != int(spec["expected_resolved_count"]):
        raise ValueError("H2 resolved count changed")
    if len(unresolved) != int(spec["expected_unresolved_count"]):
        raise ValueError("H2 unresolved count changed")
    if canonical_json_sha256(unresolved) != str(
        spec["unresolved_run_ids_sha256"]
    ):
        raise ValueError("H2 unresolved run-ID digest mismatch")
    return rows


def _validate_c2_raw(
    c2: dict,
    config: dict,
    *,
    h2_unresolved: set[str],
) -> dict[str, dict]:
    spec = config["c2_continuation"]
    if c2["status"] != "NON_AUTHORITATIVE_HOMOGENEOUS_C2_CONTINUATION_RESULT":
        raise ValueError("C2 result status changed")
    if c2["authoritative"] is not False:
        raise ValueError("C2 result became authoritative")
    if int(c2["target_stream_count"]) != int(spec["expected_target_count"]):
        raise ValueError("C2 target count changed")
    if int(c2["continued_stream_count"]) != int(spec["expected_target_count"]):
        raise ValueError("C2 continued count changed")

    rows = {str(row["run_id"]): row for row in c2["rows"]}
    if len(rows) != int(spec["expected_target_count"]):
        raise ValueError("C2 target run IDs are not unique")
    if set(rows) != h2_unresolved:
        raise ValueError("C2 target set differs from H2 unresolved set")
    if canonical_json_sha256(sorted(rows)) != str(
        config["h2_stage_b"]["unresolved_run_ids_sha256"]
    ):
        raise ValueError("C2 target-set digest mismatch")

    resolved = [
        row for row in rows.values()
        if row["status"] == "SEQUENTIAL_DECISION"
    ]
    unresolved = sorted(
        run_id
        for run_id, row in rows.items()
        if row["status"] == "SEQUENTIAL_UNRESOLVED_AT_CAP"
    )
    failures = [
        row for row in rows.values()
        if row["status"] == "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
        or row.get("failure_draw_index") is not None
    ]
    if len(resolved) != int(spec["expected_newly_resolved_count"]):
        raise ValueError("C2 newly resolved count changed")
    if len(unresolved) != int(spec["expected_unresolved_at_cap_count"]):
        raise ValueError("C2 unresolved-at-cap count changed")
    if failures:
        raise ValueError("C2 contains bootstrap refit failures")
    if canonical_json_sha256(unresolved) != str(
        spec["unresolved_at_cap_run_ids_sha256"]
    ):
        raise ValueError("C2 unresolved-at-cap digest mismatch")
    return rows


def _same_identity(h2: dict, c2: dict) -> None:
    fields = (
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
    for field in fields:
        if h2[field] != c2[field]:
            raise ValueError(
                f"H2/C2 scientific identity mismatch for {field}: "
                f"{h2['run_id']}"
            )
    if float(h2["observed_statistic"]) != float(
        c2["retained_observed_statistic"]
    ):
        raise ValueError(
            f"H2/C2 observed-statistic binding mismatch: {h2['run_id']}"
        )
    if str(h2["attempt_sequence_sha256"]) != str(
        c2["retained_prefix_sha256"]
    ):
        raise ValueError(
            f"H2/C2 retained-prefix binding mismatch: {h2['run_id']}"
        )


def _semantic_annotation(row: dict, config: dict) -> dict:
    role = str(row["role"])
    spec = config["semantic_roles"].get(role)
    if spec is None:
        raise ValueError(f"unknown terminal scientific role: {role}")
    if str(row["restriction"]) != str(spec["restriction"]):
        raise ValueError(f"role/restriction mismatch for {row['run_id']}")

    decision = row["decision"]
    if decision is None:
        direction = "UNRESOLVED_AT_CAP"
    elif decision == spec["expected_decision"]:
        direction = "EXPECTED_DIRECTION"
    else:
        direction = "OPPOSITE_DIRECTION"
    return {
        "scientific_role": spec["scientific_role"],
        "expected_decision": spec["expected_decision"],
        "role_direction_status": direction,
        "reject_semantics": spec["reject_semantics"],
    }


def compose_terminal_partition(
    h2_raw: dict,
    c2_raw: dict,
    config: dict,
) -> dict:
    validate_terminal_partition_config(config)
    h2_rows = _validate_h2_raw(h2_raw, config)
    h2_unresolved = {
        run_id for run_id, row in h2_rows.items() if row["decision"] is None
    }
    c2_rows = _validate_c2_raw(
        c2_raw,
        config,
        h2_unresolved=h2_unresolved,
    )

    terminal_rows: list[dict] = []
    for run_id in sorted(h2_rows):
        h2 = h2_rows[run_id]
        if h2["decision"] is not None:
            terminal = {
                **{
                    key: h2[key]
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
                "terminal_source_stage": "H2_STAGE_B",
                "status": "SEQUENTIAL_DECISION",
                "decision": h2["decision"],
                "stopping_n": int(h2["stopping_n"]),
                "stopping_sum": int(h2["stopping_sum"]),
                "boundary_hit": h2["boundary_hit"],
                "terminal_n": int(h2["terminal_n"]),
                "terminal_sum": int(h2["terminal_sum"]),
                "terminal_lower": int(h2["terminal_lower"]),
                "terminal_upper": int(h2["terminal_upper"]),
                "bootstrap_refit_failure": False,
            }
        else:
            c2 = c2_rows[run_id]
            _same_identity(h2, c2)
            terminal = {
                **{
                    key: c2[key]
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
                "terminal_source_stage": "C2_CONTINUATION",
                "status": c2["status"],
                "decision": c2["decision"],
                "stopping_n": c2["stopping_n"],
                "stopping_sum": c2["stopping_sum"],
                "boundary_hit": c2["boundary_hit"],
                "terminal_n": int(c2["terminal_n"]),
                "terminal_sum": int(c2["terminal_sum"]),
                "terminal_lower": int(c2["terminal_lower"]),
                "terminal_upper": int(c2["terminal_upper"]),
                "bootstrap_refit_failure": (
                    c2.get("failure_draw_index") is not None
                ),
            }
            if c2["status"] == "SEQUENTIAL_UNRESOLVED_AT_CAP":
                if int(c2["terminal_n"]) != 10000:
                    raise ValueError("cap-unresolved stream did not stop at n=10000")

        terminal.update(_semantic_annotation(terminal, config))
        terminal_rows.append(terminal)

    decisions = [row for row in terminal_rows if row["decision"] is not None]
    unresolved = [
        row for row in terminal_rows
        if row["status"] == "SEQUENTIAL_UNRESOLVED_AT_CAP"
    ]
    failures = [
        row for row in terminal_rows if row["bootstrap_refit_failure"]
    ]
    if len(terminal_rows) != EXPECTED_TOTAL:
        raise ValueError("terminal partition count mismatch")
    if len(decisions) != EXPECTED_TERMINAL_DECISIONS:
        raise ValueError("terminal decision count mismatch")
    if len(unresolved) != EXPECTED_UNRESOLVED_AT_CAP:
        raise ValueError("terminal unresolved-at-cap count mismatch")
    if failures:
        raise ValueError("terminal partition contains refit failures")

    role_counts = defaultdict(int)
    role_resolved = defaultdict(int)
    for row in terminal_rows:
        role = str(row["role"])
        role_counts[role] += 1
        role_resolved[role] += int(row["decision"] is not None)
    if set(role_counts) != EXPECTED_ROLES:
        raise ValueError("terminal partition role coverage changed")
    if any(role_resolved[role] == 0 for role in EXPECTED_ROLES):
        decision = "CHARACTERIZATION_REFINEMENT_REQUIRED"
    else:
        decision = "READY_FOR_NEXT_RECOVERY_POWER_CHARACTERIZATION"

    return {
        "interpretation_id": config["interpretation_id"],
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_TERMINAL_PARTITION_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "terminal_run_count": len(terminal_rows),
        "terminal_decision_count": len(decisions),
        "unresolved_at_cap_count": len(unresolved),
        "bootstrap_refit_failure_count": len(failures),
        "role_coverage": {
            role: {
                "run_count": role_counts[role],
                "resolved_count": role_resolved[role],
            }
            for role in sorted(EXPECTED_ROLES)
        },
        "rows": terminal_rows,
        "interpretation_decision": decision,
        "boundary": dict(config["execution_boundary"]),
    }


def _key(value: Any) -> str:
    return "NULL" if value is None else str(value)


def summarize_rows(rows: list[dict]) -> dict:
    total = len(rows)
    resolved = [row for row in rows if row["decision"] is not None]
    unresolved = total - len(resolved)
    reject = sum(row["decision"] == "REJECT_P_LE_ALPHA" for row in rows)
    not_reject = sum(
        row["decision"] == "NOT_REJECT_P_GT_ALPHA" for row in rows
    )
    expected = sum(
        row["role_direction_status"] == "EXPECTED_DIRECTION"
        for row in rows
    )
    opposite = sum(
        row["role_direction_status"] == "OPPOSITE_DIRECTION"
        for row in rows
    )

    def fraction(numerator: int, denominator: int) -> float | None:
        return numerator / denominator if denominator else None

    return {
        "run_count": total,
        "resolved_count": len(resolved),
        "unresolved_at_cap_count": unresolved,
        "reject_count": reject,
        "not_reject_count": not_reject,
        "expected_direction_count": expected,
        "opposite_direction_count": opposite,
        "reject_resolved_only_proportion": fraction(reject, len(resolved)),
        "reject_total_denominator_lower_bound": fraction(reject, total),
        "reject_total_denominator_upper_bound": fraction(
            reject + unresolved,
            total,
        ),
        "expected_direction_resolved_only_proportion": fraction(
            expected,
            len(resolved),
        ),
        "expected_direction_total_denominator_lower_bound": fraction(
            expected,
            total,
        ),
        "expected_direction_total_denominator_upper_bound": fraction(
            expected + unresolved,
            total,
        ),
    }


def aggregate_terminal_partition(result: dict, config: dict) -> dict:
    validate_terminal_partition_config(config)
    if result["status"] != (
        "NON_AUTHORITATIVE_HOMOGENEOUS_TERMINAL_PARTITION_RESULT"
    ):
        raise ValueError("terminal result status changed")
    rows = list(result["rows"])
    if len(rows) != EXPECTED_TOTAL:
        raise ValueError("terminal result run count changed")

    aggregates: dict[str, list[dict]] = {}
    for field in config["characterization"]["group_fields"]:
        groups: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            groups[_key(row.get(field))].append(row)
        aggregates[field] = [
            {field: key, **summarize_rows(values)}
            for key, values in sorted(groups.items())
        ]

    unresolved = [
        dict(row)
        for row in rows
        if row["status"] == "SEQUENTIAL_UNRESOLVED_AT_CAP"
    ]
    for row in unresolved:
        row["distance_above_lower_boundary"] = (
            int(row["terminal_sum"]) - int(row["terminal_lower"])
        )
        row["distance_below_upper_boundary"] = (
            int(row["terminal_upper"]) - int(row["terminal_sum"])
        )

    unresolved_aggregates: dict[str, list[dict]] = {}
    for field in config["characterization"]["group_fields"]:
        groups: dict[str, list[dict]] = defaultdict(list)
        for row in unresolved:
            groups[_key(row.get(field))].append(row)
        unresolved_aggregates[field] = [
            {field: key, "count": len(values)}
            for key, values in sorted(groups.items())
        ]

    return {
        "global_summary": summarize_rows(rows),
        "by_dimension": aggregates,
        "unresolved_at_cap": {
            "count": len(unresolved),
            "run_ids_sha256": canonical_json_sha256(
                sorted(str(row["run_id"]) for row in unresolved)
            ),
            "by_dimension": unresolved_aggregates,
            "rows": unresolved,
        },
        "interpretation_decision": result["interpretation_decision"],
    }
