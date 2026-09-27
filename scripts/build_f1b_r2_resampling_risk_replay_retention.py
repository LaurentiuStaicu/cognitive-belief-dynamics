from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from statistics import median


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _boundary_landmarks(replay: dict) -> dict:
    rows = {
        int(row["n"]): row
        for row in replay["boundary_table"]["rows"]
    }
    required = (1, 49, 99, 173, 199)
    missing = [n for n in required if n not in rows]
    if missing:
        raise ValueError(
            f"replay boundary table missing landmarks: {missing}"
        )
    fields = (
        "lower",
        "upper",
        "spending_allowance",
        "cumulative_lower_probability",
        "cumulative_upper_probability",
        "survivor_probability",
    )
    return {
        str(n): {field: rows[n][field] for field in fields}
        for n in required
    }


def build_retained_result(
    replay: dict,
    *,
    replay_artifact_id: int,
    replay_artifact_zip_sha256: str,
    replay_json_sha256: str,
    replay_json_size_bytes: int,
) -> dict:
    if replay["status"] != (
        "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE"
    ):
        raise ValueError("unexpected replay status")
    if replay["authoritative"] is not False:
        raise ValueError("replay must remain non-authoritative")
    if int(replay["restriction_run_count"]) != 750:
        raise ValueError("retained replay must contain 750 restriction runs")
    if int(replay["bootstrap_refit_failure_count"]) != 0:
        raise ValueError("retained replay unexpectedly contains refit failures")
    if len(replay["stream_checkpoints"]) != 750:
        raise ValueError("retained replay checkpoint count mismatch")
    if len(replay["replay_rows"]) != 750:
        raise ValueError("retained replay row count mismatch")

    rows = list(replay["replay_rows"])
    unresolved = [row for row in rows if row["decision"] is None]
    resolved = [row for row in rows if row["decision"] is not None]

    fixed_p = [
        float(row["fixed_199_plus_one_p_value"])
        for row in unresolved
        if row["fixed_199_plus_one_p_value"] is not None
    ]
    if len(fixed_p) != len(unresolved):
        raise ValueError(
            "all frozen unresolved runs must have retained fixed-199 context"
        )

    role_context = {}
    for role in sorted({str(row["role"]) for row in rows}):
        group = [row for row in unresolved if str(row["role"]) == role]
        role_context[role] = {
            "unresolved_count": len(group),
            "fixed_199_reject_count_descriptive_only": sum(
                bool(row["fixed_199_rejected"]) for row in group
            ),
            "fixed_199_not_reject_count_descriptive_only": sum(
                not bool(row["fixed_199_rejected"]) for row in group
            ),
        }

    checkpoints = sorted(
        replay["stream_checkpoints"],
        key=lambda row: str(row["run_id"]),
    )
    checkpoint_bytes = json.dumps(
        checkpoints,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    sequential_reject = [
        row
        for row in resolved
        if row["decision"] == "REJECT_P_LE_ALPHA"
    ]
    return {
        "result_id": (
            "F1B.R2.RESAMPLING_RISK_REPLAY.RESULT.2026-09-27"
        ),
        "status": (
            "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE"
        ),
        "authoritative": False,
        "issue": 213,
        "scientific_source_commit": replay["provenance"][
            "source_commit"
        ],
        "execution": {
            "temporary_replay_pr": 216,
            "github_run_id": "36343709630",
            "replay_artifact_id": int(replay_artifact_id),
            "replay_artifact_zip_sha256": str(
                replay_artifact_zip_sha256
            ),
            "exact_replay_json_sha256": str(replay_json_sha256),
            "exact_replay_json_size_bytes": int(
                replay_json_size_bytes
            ),
            "retained_input_artifact_id": int(
                replay["provenance"]["retained_artifact_id"]
            ),
            "retained_input_json_sha256": replay["provenance"][
                "input_sha256"
            ],
            "controller_config_sha256": replay["provenance"][
                "controller_config_sha256"
            ],
        },
        "controller": {
            "controller_id": replay["controller_id"],
            "alpha": replay["alpha"],
            "epsilon": replay["epsilon"],
            "halfspend": replay["halfspend"],
            "max_attempts": replay["max_attempts"],
            "boundary_landmarks": _boundary_landmarks(replay),
        },
        "integrity": {
            "restriction_run_count": replay[
                "restriction_run_count"
            ],
            "bootstrap_refit_failure_count": replay[
                "bootstrap_refit_failure_count"
            ],
            "stream_checkpoint_count": len(checkpoints),
            "stream_checkpoints_sha256": sha256_bytes(
                checkpoint_bytes
            ),
            "sequential_vs_fixed_199_disagreement_count_among_resolved": (
                replay["global_summary"][
                    "sequential_vs_fixed_199_disagreement_count"
                ]
            ),
        },
        "global_summary": replay["global_summary"],
        "by_restriction": replay["by_restriction"],
        "by_role": replay["by_role"],
        "by_axis": replay["by_axis"],
        "by_target": replay["by_target"],
        "by_sign": replay["by_sign"],
        "by_anchor": replay["by_anchor"],
        "unresolved_fixed_199_context_descriptive_only": {
            "sequential_unresolved_count": len(unresolved),
            "fixed_199_reject_count": sum(
                bool(row["fixed_199_rejected"])
                for row in unresolved
            ),
            "fixed_199_not_reject_count": sum(
                not bool(row["fixed_199_rejected"])
                for row in unresolved
            ),
            "fixed_199_plus_one_p_value_min": min(fixed_p),
            "fixed_199_plus_one_p_value_median": float(
                median(fixed_p)
            ),
            "fixed_199_plus_one_p_value_max": max(fixed_p),
            "by_role": role_context,
            "warning": (
                "These fixed-199 states are descriptive only. "
                "Sequentially unresolved runs remain unresolved and "
                "are not classified by the fixed-199 decision."
            ),
        },
        "sequential_reject_structure": {
            "reject_count": len(sequential_reject),
            "all_rejects_stopping_n_173": all(
                row["stopping_n"] == 173
                for row in sequential_reject
            ),
            "all_rejects_stopping_sum_0": all(
                row["stopping_sum"] == 0
                for row in sequential_reject
            ),
        },
        "unresolved_run_ids": sorted(
            str(row["run_id"]) for row in unresolved
        ),
        "stream_checkpoints": checkpoints,
        "next_gate": (
            "PROSPECTIVE_EXTENSION_BEYOND_199_WITH_EXPLICIT_CAP_"
            "OR_SEPARATELY_JUSTIFIED_CONTROLLER_CHANGE"
        ),
        "interpretation": {
            "stage_b_replay_complete": True,
            "draw_count_selected": False,
            "new_bootstrap_attempts_generated": False,
            "statistical_power_validated": False,
            "authoritative_core_grid_frozen": False,
            "human_n_frozen": False,
            "participant_recruitment_authorized": False,
            "runtime_f1b_authorized": False,
            "boundary": (
                "The epsilon=0.001 controller resolves 526/750 "
                "retained streams by n=199 and leaves 224 unresolved. "
                "Unresolved runs remain unresolved. The resampling-risk "
                "guarantee concerns Monte Carlo implementation error "
                "conditional on the retained bootstrap mechanism only."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build compact repository retention for the exact F1b R2 "
            "resampling-risk replay artifact."
        )
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifact-id", type=int, required=True)
    parser.add_argument("--artifact-zip-sha256", required=True)
    args = parser.parse_args()

    raw = args.input.read_bytes()
    replay = json.loads(raw)
    retained = build_retained_result(
        replay,
        replay_artifact_id=args.artifact_id,
        replay_artifact_zip_sha256=args.artifact_zip_sha256,
        replay_json_sha256=sha256_bytes(raw),
        replay_json_size_bytes=len(raw),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(retained, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
