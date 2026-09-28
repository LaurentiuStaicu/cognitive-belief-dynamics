from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c2_continuation import (
    bind_c2_targets,
    continue_c2_partition,
    validate_c2_environment,
    validate_homogeneous_c2_config,
    validate_retained_c1_result,
    validate_retained_h1_result,
    validate_retained_h2_result,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def verify_git_blob(path: Path, expected: str, label: str) -> None:
    actual = git_blob_sha(path)
    if actual != str(expected):
        raise ValueError(
            f"{label} Git blob mismatch: {actual} != {expected}"
        )


def verify_sha256(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != str(expected):
        raise ValueError(
            f"{label} SHA-256 mismatch: {actual} != {expected}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Continue exactly the 224 qualified homogeneous F1b R2 "
            "resampling-risk streams from retained n=199 to the "
            "prospective n=10000 cap."
        )
    )
    parser.add_argument("--paired-source", type=Path, required=True)
    parser.add_argument("--stage-b-raw", type=Path, required=True)
    parser.add_argument("--c1-combined", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_homogeneous_c2_continuation_v1.json"
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
    parser.add_argument(
        "--h2-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_homogeneous_stage_b_rebuild_2026-09-28.json"
        ),
    )
    parser.add_argument(
        "--c1-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_homogeneous_c1_exact_replay_2026-09-28.json"
        ),
    )
    parser.add_argument(
        "--paired-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
        ),
    )
    parser.add_argument(
        "--v2-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_kl_controlled_departure_design_v2.json"
        ),
    )
    parser.add_argument(
        "--review-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_distance_definition_review.json"
        ),
    )
    parser.add_argument(
        "--historical-departure-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ),
    )
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_homogeneous_c2_config(config)
    validate_c2_environment()

    verify_git_blob(
        Path(config["frozen_dependency_lock"]["path"]),
        config["frozen_dependency_lock"]["git_blob_sha"],
        "frozen dependency lock",
    )
    for key in (
        "protected_scientific_file_git_blob_sha",
        "protected_controller_file_git_blob_sha",
        "protected_lineage_file_git_blob_sha",
    ):
        for path_text, expected in config[key].items():
            verify_git_blob(Path(path_text), expected, path_text)

    source = config["source_lineage"]
    stage_b = config["stage_b_lineage"]
    c1 = config["c1_lineage"]

    verify_git_blob(
        args.h1_result,
        source["retained_h1_result_git_blob_sha"],
        "retained H1 result",
    )
    verify_git_blob(
        args.h2_result,
        stage_b["retained_h2_result_git_blob_sha"],
        "retained H2 result",
    )
    verify_git_blob(
        args.c1_result,
        c1["retained_result_git_blob_sha"],
        "retained C1 result",
    )

    h1_result = json.loads(args.h1_result.read_text(encoding="utf-8"))
    h2_result = json.loads(args.h2_result.read_text(encoding="utf-8"))
    c1_result = json.loads(args.c1_result.read_text(encoding="utf-8"))
    validate_retained_h1_result(h1_result, config)
    validate_retained_h2_result(h2_result, config)
    validate_retained_c1_result(c1_result, config)

    verify_sha256(
        args.paired_source,
        source["combined_json_sha256"],
        "homogeneous H1 source",
    )
    if args.paired_source.stat().st_size != int(
        source["combined_json_size_bytes"]
    ):
        raise ValueError("homogeneous H1 source size mismatch")

    verify_sha256(
        args.stage_b_raw,
        stage_b["raw_json_sha256"],
        "homogeneous H2 raw replay",
    )
    if args.stage_b_raw.stat().st_size != int(
        stage_b["raw_json_size_bytes"]
    ):
        raise ValueError("homogeneous H2 raw replay size mismatch")

    verify_sha256(
        args.c1_combined,
        c1["combined_json_sha256"],
        "homogeneous C1 combined result",
    )
    if args.c1_combined.stat().st_size != int(
        c1["combined_json_size_bytes"]
    ):
        raise ValueError("homogeneous C1 combined result size mismatch")

    frozen_inputs = {
        "paired_config": args.paired_config,
        "v2_config": args.v2_config,
        "review_config": args.review_config,
        "historical_departure_config": args.historical_departure_config,
    }
    for label, path in frozen_inputs.items():
        verify_sha256(
            path,
            config["frozen_inputs"][label]["sha256"],
            label,
        )

    paired_source = json.loads(
        args.paired_source.read_text(encoding="utf-8")
    )
    raw_h2 = json.loads(args.stage_b_raw.read_text(encoding="utf-8"))
    c1_combined = json.loads(
        args.c1_combined.read_text(encoding="utf-8")
    )

    binding = bind_c2_targets(
        paired_source,
        raw_h2,
        c1_combined,
        config,
    )

    paired_config = json.loads(
        args.paired_config.read_text(encoding="utf-8")
    )
    v2_config = json.loads(args.v2_config.read_text(encoding="utf-8"))
    review_config = json.loads(
        args.review_config.read_text(encoding="utf-8")
    )
    historical_config = json.loads(
        args.historical_departure_config.read_text(encoding="utf-8")
    )

    result = continue_c2_partition(
        binding,
        paired_config,
        v2_config,
        review_config,
        historical_config,
        config,
        shard_index=int(args.shard_index),
    )
    result["provenance"] = {
        "execution_commit": git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "h1_result_path": str(args.h1_result),
        "h1_result_git_blob_sha": source[
            "retained_h1_result_git_blob_sha"
        ],
        "h1_source_artifact_id": int(source["artifact_id"]),
        "h1_source_sha256": sha256(args.paired_source),
        "h2_result_path": str(args.h2_result),
        "h2_result_git_blob_sha": stage_b[
            "retained_h2_result_git_blob_sha"
        ],
        "h2_raw_artifact_id": int(stage_b["artifact_id"]),
        "h2_raw_sha256": sha256(args.stage_b_raw),
        "h2_unresolved_run_ids_sha256": binding[
            "h2_binding"
        ]["integrity"]["unresolved_run_ids_sha256"],
        "h2_stream_checkpoints_sha256": binding[
            "h2_binding"
        ]["integrity"]["stream_checkpoints_sha256"],
        "c1_result_path": str(args.c1_result),
        "c1_result_git_blob_sha": c1["retained_result_git_blob_sha"],
        "c1_artifact_id": int(c1["artifact_id"]),
        "c1_combined_sha256": sha256(args.c1_combined),
        "target_run_ids_sha256": binding["target_run_ids_sha256"],
        "frozen_input_sha256": {
            label: sha256(path)
            for label, path in frozen_inputs.items()
        },
        "protected_scientific_file_git_blob_sha": config[
            "protected_scientific_file_git_blob_sha"
        ],
        "protected_controller_file_git_blob_sha": config[
            "protected_controller_file_git_blob_sha"
        ],
        "protected_lineage_file_git_blob_sha": config[
            "protected_lineage_file_git_blob_sha"
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
