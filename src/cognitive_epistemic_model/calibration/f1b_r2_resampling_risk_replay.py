from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from statistics import median

from .f1b_r2_resampling_risk import (
    generate_resampling_risk_boundaries,
    replay_exceedance_stream,
)


def canonical_attempt_sequence_sha256(
    attempts: list[float | None] | tuple[float | None, ...],
) -> str:
    payload = json.dumps(
        list(attempts),
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _fixed_snapshot(run: dict, draws: int) -> dict:
    matches = [
        row
        for row in run["snapshots"]
        if int(row["bootstrap_draws"]) == int(draws)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"run {run['run_id']} does not contain exactly one "
            f"{draws}-draw snapshot"
        )
    return matches[0]


def _stratum_key(value) -> str:
    return "NULL" if value is None else str(value)


def _stopping_distribution(rows: list[dict]) -> dict:
    stopping = [
        int(row["stopping_n"])
        for row in rows
        if row["stopping_n"] is not None
    ]
    if not stopping:
        return {
            "resolved_count": 0,
            "minimum": None,
            "median": None,
            "maximum": None,
            "histogram": {},
        }
    counts = Counter(stopping)
    return {
        "resolved_count": len(stopping),
        "minimum": min(stopping),
        "median": float(median(stopping)),
        "maximum": max(stopping),
        "histogram": {
            str(key): int(value)
            for key, value in sorted(counts.items())
        },
    }


def _summary(rows: list[dict]) -> dict:
    total = len(rows)
    resolved = [row for row in rows if row["decision"] is not None]
    unresolved = [
        row for row in rows if row["decision"] is None
    ]
    rejected = sum(
        row["decision"] == "REJECT_P_LE_ALPHA"
        for row in resolved
    )
    not_rejected = sum(
        row["decision"] == "NOT_REJECT_P_GT_ALPHA"
        for row in resolved
    )
    disagreements = sum(
        bool(row["sequential_vs_fixed_199_disagreement"])
        for row in resolved
    )
    return {
        "run_count": total,
        "resolved_by_49_count": sum(
            row["resolved_by_49"] for row in rows
        ),
        "resolved_by_99_count": sum(
            row["resolved_by_99"] for row in rows
        ),
        "resolved_by_199_count": len(resolved),
        "unresolved_at_199_count": len(unresolved),
        "resolved_by_49_rate": (
            sum(row["resolved_by_49"] for row in rows) / total
            if total
            else None
        ),
        "resolved_by_99_rate": (
            sum(row["resolved_by_99"] for row in rows) / total
            if total
            else None
        ),
        "resolved_by_199_rate": (
            len(resolved) / total if total else None
        ),
        "sequential_reject_count": rejected,
        "sequential_not_reject_count": not_rejected,
        "sequential_vs_fixed_199_disagreement_count": disagreements,
        "stopping_distribution": _stopping_distribution(rows),
    }


def _aggregate_by(rows: list[dict], field: str) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[_stratum_key(row.get(field))].append(row)
    return [
        {
            field: key,
            **_summary(values),
        }
        for key, values in sorted(groups.items())
    ]


def replay_retained_paired_bootstrap(
    retained: dict,
    config: dict,
) -> dict:
    if config["status"] != (
        "NON_AUTHORITATIVE_RESAMPLING_RISK_CONTROLLER_PROTOTYPE"
    ):
        raise ValueError("unsupported resampling-risk controller config")
    if retained["authoritative"] is not False:
        raise ValueError("retained paired source must be non-authoritative")
    expected_runs = int(
        config["replay_source"]["expected_restriction_runs"]
    )
    expected_attempts = int(
        config["replay_source"]["expected_attempts_per_run"]
    )
    if int(retained["restriction_run_count"]) != expected_runs:
        raise ValueError("retained restriction-run count mismatch")
    if len(retained["restriction_runs"]) != expected_runs:
        raise ValueError("retained restriction-run payload is incomplete")

    boundaries = generate_resampling_risk_boundaries(
        alpha=float(config["alpha"]),
        epsilon=float(config["epsilon"]),
        halfspend=float(config["halfspend"]),
        max_n=int(config["replay_max_attempts"]),
        probability_tolerance=float(
            config["probability_tolerance"]
        ),
    )
    alpha = float(config["alpha"])
    rows: list[dict] = []
    checkpoints: list[dict] = []
    observed_refit_failures = 0

    for run in retained["restriction_runs"]:
        attempts = list(run["bootstrap_attempt_statistics"])
        if len(attempts) != expected_attempts:
            raise ValueError(
                f"run {run['run_id']} does not contain "
                f"{expected_attempts} bootstrap attempts"
            )
        if bool(run["fit_failure"]):
            raise ValueError(
                f"retained run {run['run_id']} has observed-fit failure"
            )

        attempt_hash = canonical_attempt_sequence_sha256(attempts)
        checkpoints.append(
            {
                "run_id": str(run["run_id"]),
                "dataset_sha256": str(run["dataset_sha256"]),
                "bootstrap_stream_seed": int(
                    run["bootstrap_stream_seed"]
                ),
                "observed_statistic": float(
                    run["observed_statistic"]
                ),
                "attempt_sequence_sha256": attempt_hash,
            }
        )

        exceedances: list[int | None] = []
        for value in attempts:
            if value is None:
                observed_refit_failures += 1
                exceedances.append(None)
            else:
                exceedances.append(
                    int(float(value) >= float(run["observed_statistic"]))
                )

        replay = replay_exceedance_stream(
            exceedances,
            boundaries=boundaries,
        )
        valid_exceedances = [
            int(value)
            for value in exceedances
            if value is not None
        ]
        if len(valid_exceedances) != expected_attempts:
            fixed_plus_one = None
            fixed_rejected = None
        else:
            exceedance_count = int(sum(valid_exceedances))
            fixed_plus_one = float(
                (1 + exceedance_count)
                / (1 + expected_attempts)
            )
            fixed_rejected = bool(fixed_plus_one <= alpha)

        retained_199 = _fixed_snapshot(run, expected_attempts)
        if bool(retained_199["bootstrap_calibration_failure"]):
            raise ValueError(
                f"retained run {run['run_id']} has 199-draw "
                "calibration failure"
            )
        if int(retained_199["bootstrap_fit_failures"]) != (
            expected_attempts - len(valid_exceedances)
        ):
            raise ValueError(
                f"retained run {run['run_id']} bootstrap-failure count "
                "does not match attempt sequence"
            )
        if fixed_plus_one is not None:
            retained_p = float(retained_199["p_value"])
            if abs(retained_p - fixed_plus_one) > 1e-15:
                raise ValueError(
                    f"retained 199-draw p-value mismatch for "
                    f"{run['run_id']}"
                )
            if bool(retained_199["rejected"]) != fixed_rejected:
                raise ValueError(
                    f"retained 199-draw decision mismatch for "
                    f"{run['run_id']}"
                )

        sequential_rejected = (
            None
            if replay.decision is None
            else replay.decision == "REJECT_P_LE_ALPHA"
        )
        disagreement = (
            None
            if sequential_rejected is None or fixed_rejected is None
            else bool(sequential_rejected) != bool(fixed_rejected)
        )

        rows.append(
            {
                "run_id": str(run["run_id"]),
                "dataset_id": str(run["dataset_id"]),
                "dataset_sha256": str(run["dataset_sha256"]),
                "bootstrap_stream_seed": int(
                    run["bootstrap_stream_seed"]
                ),
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
                "observed_statistic": float(
                    run["observed_statistic"]
                ),
                "attempt_sequence_sha256": attempt_hash,
                "status": replay.status,
                "decision": replay.decision,
                "stopping_n": replay.stopping_n,
                "stopping_sum": replay.stopping_sum,
                "boundary_hit": replay.boundary_hit,
                "failure_n": replay.failure_n,
                "terminal_n": replay.terminal_n,
                "terminal_sum": replay.terminal_sum,
                "terminal_lower": replay.terminal_lower,
                "terminal_upper": replay.terminal_upper,
                "full_prefix_sum_199": (
                    None
                    if len(valid_exceedances) != expected_attempts
                    else int(sum(valid_exceedances))
                ),
                "resolved_by_49": bool(
                    replay.stopping_n is not None
                    and replay.stopping_n <= 49
                ),
                "resolved_by_99": bool(
                    replay.stopping_n is not None
                    and replay.stopping_n <= 99
                ),
                "resolved_by_199": bool(
                    replay.stopping_n is not None
                ),
                "fixed_199_plus_one_p_value": fixed_plus_one,
                "fixed_199_rejected": fixed_rejected,
                "retained_fixed_199_p_value": retained_199["p_value"],
                "retained_fixed_199_rejected": retained_199["rejected"],
                "sequential_vs_fixed_199_disagreement": disagreement,
            }
        )

    expected_failures = int(
        config["replay_source"]["expected_bootstrap_fit_failures"]
    )
    if observed_refit_failures != expected_failures:
        raise ValueError(
            "retained bootstrap-refit failure count does not match "
            "frozen replay source"
        )

    rows.sort(key=lambda row: row["run_id"])
    checkpoints.sort(key=lambda row: row["run_id"])
    return {
        "replay_id": "F1B.R2.RESAMPLING_RISK_REPLAY.V1",
        "status": "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE",
        "authoritative": False,
        "controller_id": config["controller_id"],
        "alpha": float(config["alpha"]),
        "epsilon": float(config["epsilon"]),
        "halfspend": float(config["halfspend"]),
        "max_attempts": int(config["replay_max_attempts"]),
        "restriction_run_count": len(rows),
        "bootstrap_refit_failure_count": observed_refit_failures,
        "global_summary": _summary(rows),
        "by_restriction": _aggregate_by(rows, "restriction"),
        "by_role": _aggregate_by(rows, "role"),
        "by_axis": _aggregate_by(rows, "axis"),
        "by_target": _aggregate_by(
            rows,
            "target_mean_bernoulli_kl",
        ),
        "by_sign": _aggregate_by(rows, "sign"),
        "by_anchor": _aggregate_by(rows, "anchor_id"),
        "replay_rows": rows,
        "stream_checkpoints": checkpoints,
        "boundary_table": boundaries.to_dict(),
        "interpretation_boundary": (
            "Replay of the exact retained first-199 bootstrap attempts only. "
            "The sequential decisions control Monte Carlo resampling risk "
            "conditional on the retained bootstrap mechanism. Unresolved "
            "runs remain unresolved. This result does not select a bootstrap "
            "draw count, validate scientific Type-I error or power, freeze "
            "a core grid or human N, authorize recruitment, or change "
            "runtime F1b."
        ),
    }
