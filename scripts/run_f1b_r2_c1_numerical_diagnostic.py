from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration import (
    f1b_r2_paired_bootstrap_characterization as paired_characterization,
)
from cognitive_epistemic_model.calibration.f1b_r2_c1_numerical_diagnostic import (
    diagnose_run_prefix,
    environment_identity,
    select_diagnostic_sentinels,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
    regenerate_dataset_for_run,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def verify_path_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != str(expected):
        raise ValueError(
            f"{label} SHA-256 mismatch: {actual} != {expected}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Trace retained F1b R2 Stage-C1 sentinels without changing "
            "the scientific fitter or generating any draw index >=199."
        )
    )
    parser.add_argument("--paired-source", type=Path, required=True)
    parser.add_argument(
        "--c1-result",
        type=Path,
        default=Path(
            "model/results/f1b_r2_continuation_c1_failed_2026-09-27.json"
        ),
    )
    parser.add_argument(
        "--continuation-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_resampling_risk_continuation_v1.json"
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
    parser.add_argument(
        "--sentinel",
        choices=(
            "EXACT_PASS_CONTROL",
            "EXACT_OBSERVED_HASH_FAILURE",
            "WITHIN_TOLERANCE_HASH_FAILURE",
            "OUTSIDE_TOLERANCE_HASH_FAILURE",
        ),
        required=True,
    )
    parser.add_argument(
        "--same-process-repeats",
        type=int,
        default=2,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    args = parser.parse_args()

    if int(args.same_process_repeats) != 2:
        raise ValueError(
            "initial diagnostic freezes exactly two same-process repeats"
        )

    continuation = json.loads(
        args.continuation_config.read_text(encoding="utf-8")
    )
    source = continuation["source"]
    verify_path_hash(
        args.paired_source,
        source["paired_exact_json_sha256"],
        "paired source",
    )
    verify_path_hash(
        args.paired_config,
        source["paired_config_sha256"],
        "paired config",
    )
    verify_path_hash(
        args.v2_config,
        source["v2_config_sha256"],
        "V2 config",
    )
    verify_path_hash(
        args.review_config,
        source["review_config_sha256"],
        "distance review config",
    )
    verify_path_hash(
        args.historical_departure_config,
        source["historical_departure_config_sha256"],
        "historical departure config",
    )
    for path_text, expected_blob in source[
        "scientific_file_git_blob_sha"
    ].items():
        actual_blob = git_blob_sha(Path(path_text))
        if actual_blob != str(expected_blob):
            raise ValueError(
                "scientific lineage mismatch for "
                f"{path_text}: {actual_blob} != {expected_blob}"
            )

    c1_result = json.loads(args.c1_result.read_text(encoding="utf-8"))
    sentinels = select_diagnostic_sentinels(c1_result)
    run_id = sentinels[str(args.sentinel)]

    paired_source = json.loads(
        args.paired_source.read_text(encoding="utf-8")
    )
    source_runs = {
        str(row["run_id"]): row
        for row in paired_source["restriction_runs"]
    }
    if run_id not in source_runs:
        raise ValueError(f"sentinel run missing from paired source: {run_id}")
    run = source_runs[run_id]

    paired_config = json.loads(
        args.paired_config.read_text(encoding="utf-8")
    )
    v2_config = json.loads(
        args.v2_config.read_text(encoding="utf-8")
    )
    review_config = json.loads(
        args.review_config.read_text(encoding="utf-8")
    )
    historical_config = json.loads(
        args.historical_departure_config.read_text(encoding="utf-8")
    )
    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_config,
    )
    dataset = regenerate_dataset_for_run(
        run,
        paired_config=paired_config,
        departure_cases=departure_cases,
    )
    scales = paired_characterization._scales(
        paired_config,
        generator=False,
    )

    environment = environment_identity()
    repeats = [
        diagnose_run_prefix(
            run,
            dataset,
            scales=scales,
            draw_indices=range(199),
            stop_after_first_divergence=True,
        )
        for _ in range(2)
    ]
    result = {
        "diagnostic_id": "F1B.R2.STAGE_C1.NUMERICAL_DIAGNOSTIC.V1",
        "status": "NON_AUTHORITATIVE_STAGE_C1_NUMERICAL_DIAGNOSTIC",
        "authoritative": False,
        "issue": 223,
        "sentinel": str(args.sentinel),
        "sentinel_run_id": run_id,
        "sentinel_map": sentinels,
        "same_process_repeat_count": 2,
        "same_process_repeats_exactly_equal": repeats[0] == repeats[1],
        "environment": environment,
        "repeats": repeats,
        "provenance": {
            "source_commit": args.source_commit or git_head(),
            "paired_source_sha256": sha256(args.paired_source),
            "c1_result_sha256": sha256(args.c1_result),
            "continuation_config_sha256": sha256(
                args.continuation_config
            ),
            "paired_config_sha256": sha256(args.paired_config),
            "v2_config_sha256": sha256(args.v2_config),
            "review_config_sha256": sha256(args.review_config),
            "historical_departure_config_sha256": sha256(
                args.historical_departure_config
            ),
            "scientific_file_git_blob_sha": source[
                "scientific_file_git_blob_sha"
            ],
        },
        "boundary": {
            "stage_c1_gate_changed": False,
            "stage_c2_authorized": False,
            "new_draw_index_ge_199_generated": False,
            "scientific_fit_settings_changed": False,
            "human_n_frozen": False,
            "participant_recruitment_authorized": False,
            "runtime_f1b_authorized": False,
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
