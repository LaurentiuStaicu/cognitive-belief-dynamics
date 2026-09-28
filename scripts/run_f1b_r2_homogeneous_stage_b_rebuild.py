from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_stage_b_rebuild import (
    build_h2_effective_controller,
    validate_h2_rebuild_config,
    validate_retained_h1_result,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    replay_retained_paired_bootstrap,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def verify_git_blob(path: Path, expected: str, label: str) -> None:
    actual = git_blob_sha(path)
    if actual != str(expected):
        raise ValueError(
            f"{label} Git blob mismatch: {actual} != {expected}"
        )


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild non-authoritative F1b R2 Stage-B resampling-risk "
            "provenance from the retained homogeneous H1 paired source "
            "without generating any new bootstrap attempts."
        )
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--rebuild-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_homogeneous_stage_b_rebuild_v1.json"
        ),
    )
    parser.add_argument(
        "--controller-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_resampling_risk_controller_v1.json"
        ),
    )
    parser.add_argument(
        "--h1-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_homogeneous_paired_h1_qualification_2026-09-28.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rebuild = json.loads(
        args.rebuild_config.read_text(encoding="utf-8")
    )
    validate_h2_rebuild_config(rebuild)

    source_spec = rebuild["source_lineage"]
    verify_git_blob(
        args.h1_result,
        source_spec["retained_h1_result_git_blob_sha"],
        "retained H1 result",
    )
    h1_result = json.loads(args.h1_result.read_text(encoding="utf-8"))
    validate_retained_h1_result(h1_result, rebuild)

    frozen = rebuild["frozen_controller"]
    verify_git_blob(
        args.controller_config,
        frozen["config_git_blob_sha"],
        "frozen controller config",
    )
    for path_text, expected in rebuild[
        "protected_controller_file_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)

    base_controller = json.loads(
        args.controller_config.read_text(encoding="utf-8")
    )
    effective_controller = build_h2_effective_controller(
        base_controller,
        rebuild,
    )

    input_sha = sha256(args.input)
    if input_sha != str(source_spec["combined_json_sha256"]):
        raise ValueError(
            "homogeneous H1 source SHA-256 mismatch: "
            f"{input_sha} != {source_spec['combined_json_sha256']}"
        )
    if args.input.stat().st_size != int(
        source_spec["combined_json_size_bytes"]
    ):
        raise ValueError("homogeneous H1 source size mismatch")

    retained = json.loads(args.input.read_text(encoding="utf-8"))
    replay = replay_retained_paired_bootstrap(
        retained,
        effective_controller,
    )
    replay["homogeneous_rebuild"] = {
        "rebuild_id": rebuild["rebuild_id"],
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_STAGE_B_REBUILD_COMPLETE",
        "issue": int(rebuild["issue"]),
        "source_lineage_id": source_spec["lineage_id"],
        "historical_stage_b_inherited": False,
        "new_bootstrap_attempts_generated": False,
        "maximum_source_attempts": 199,
    }
    replay["provenance"] = {
        "execution_commit": git_head(),
        "input_path": str(args.input),
        "input_artifact_id": int(source_spec["artifact_id"]),
        "input_artifact_name": str(source_spec["artifact_name"]),
        "input_sha256": input_sha,
        "input_size_bytes": args.input.stat().st_size,
        "h1_result_path": str(args.h1_result),
        "h1_result_git_blob_sha": str(
            source_spec["retained_h1_result_git_blob_sha"]
        ),
        "rebuild_config_path": str(args.rebuild_config),
        "rebuild_config_sha256": sha256(args.rebuild_config),
        "controller_config_path": str(args.controller_config),
        "controller_config_git_blob_sha": str(
            frozen["config_git_blob_sha"]
        ),
        "controller_config_sha256": sha256(args.controller_config),
        "protected_controller_file_git_blob_sha": rebuild[
            "protected_controller_file_git_blob_sha"
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(replay, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
