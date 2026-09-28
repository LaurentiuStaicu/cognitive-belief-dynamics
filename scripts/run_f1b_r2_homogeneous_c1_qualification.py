from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c1_exact_replay import (
    annotate_partition_with_homogeneous_requirements,
    build_effective_continuation,
    derive_h2_stage_b_binding,
    validate_c1_environment,
    validate_homogeneous_c1_config,
    validate_retained_h1_result,
    validate_retained_h2_result,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    qualify_continuation_partition,
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
            "Qualify exact regeneration of the homogeneous F1b R2 "
            "Stage-C1 first-199 prefixes before any new bootstrap draw."
        )
    )
    parser.add_argument("--paired-source", type=Path, required=True)
    parser.add_argument("--stage-b-raw", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_homogeneous_c1_exact_replay_v1.json"
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
    validate_homogeneous_c1_config(config)
    validate_c1_environment()

    verify_git_blob(
        Path(config["frozen_dependency_lock"]["path"]),
        config["frozen_dependency_lock"]["git_blob_sha"],
        "frozen dependency lock",
    )
    for path_text, expected in config[
        "protected_scientific_file_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)
    for path_text, expected in config[
        "protected_qualification_file_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)

    source = config["source_lineage"]
    stage_b = config["stage_b_lineage"]
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

    h1_result = json.loads(args.h1_result.read_text(encoding="utf-8"))
    h2_result = json.loads(args.h2_result.read_text(encoding="utf-8"))
    validate_retained_h1_result(h1_result, config)
    validate_retained_h2_result(h2_result, config)

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
    if int(paired_source["restriction_run_count"]) != int(
        source["expected_restriction_runs"]
    ):
        raise ValueError("homogeneous H1 restriction-run count changed")
    if len(paired_source["restriction_runs"]) != int(
        source["expected_restriction_runs"]
    ):
        raise ValueError("homogeneous H1 restriction-run rows changed")
    if any(
        bool(run["fit_failure"])
        for run in paired_source["restriction_runs"]
    ):
        raise ValueError("homogeneous H1 contains observed fit failures")
    if any(
        len(run["bootstrap_attempt_statistics"])
        != int(source["expected_attempts_per_run"])
        for run in paired_source["restriction_runs"]
    ):
        raise ValueError("homogeneous H1 retained attempt horizon changed")
    if any(
        any(
            attempt is None
            for attempt in run["bootstrap_attempt_statistics"]
        )
        for run in paired_source["restriction_runs"]
    ):
        raise ValueError("homogeneous H1 contains bootstrap refit failures")

    raw_h2 = json.loads(args.stage_b_raw.read_text(encoding="utf-8"))
    if raw_h2["provenance"]["input_sha256"] != str(
        source["combined_json_sha256"]
    ):
        raise ValueError("H2 raw replay is not bound to the H1 source")
    if raw_h2["homogeneous_rebuild"]["source_lineage_id"] != str(
        source["lineage_id"]
    ):
        raise ValueError("H2 raw replay source lineage changed")

    effective_stage_b = derive_h2_stage_b_binding(raw_h2, config)
    effective_continuation = build_effective_continuation(config)

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

    result = qualify_continuation_partition(
        paired_source,
        effective_stage_b,
        effective_continuation,
        paired_config,
        v2_config,
        review_config,
        historical_config,
        shard_index=int(args.shard_index),
    )
    annotate_partition_with_homogeneous_requirements(
        result,
        paired_source,
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
        "h2_unresolved_run_ids_sha256": effective_stage_b[
            "integrity"
        ]["unresolved_run_ids_sha256"],
        "h2_stream_checkpoints_sha256": effective_stage_b[
            "integrity"
        ]["stream_checkpoints_sha256"],
        "frozen_input_sha256": {
            label: sha256(path)
            for label, path in frozen_inputs.items()
        },
        "protected_scientific_file_git_blob_sha": config[
            "protected_scientific_file_git_blob_sha"
        ],
        "protected_qualification_file_git_blob_sha": config[
            "protected_qualification_file_git_blob_sha"
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
