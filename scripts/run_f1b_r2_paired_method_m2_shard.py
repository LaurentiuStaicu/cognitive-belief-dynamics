from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization import (
    dataset_fingerprint,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    dataset_id_for,
    select_scientific_specs,
    simulate_paired_missingness_datasets,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    build_m2_boundaries,
    canonical_json_sha256,
    characterize_stream,
    stable_shard,
    validate_m1_combined,
    validate_m2_config,
    validate_m2_environment,
    validate_retained_m1_result,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def verify_blob(path: Path, expected: str, label: str) -> None:
    actual = git_blob_sha(path)
    if actual != str(expected):
        raise ValueError(f"{label} Git blob mismatch: {actual} != {expected}")


def verify_repository_contract(config: dict) -> None:
    lock = config["frozen_dependency_lock"]
    verify_blob(
        Path(lock["path"]),
        lock["git_blob_sha"],
        "M2 dependency lock",
    )
    controller = config["controller"]
    verify_blob(
        Path(controller["config_path"]),
        controller["config_git_blob_sha"],
        "M2 controller config",
    )
    retained = config["retained_m1"]
    verify_blob(
        Path(retained["result_path"]),
        retained["result_git_blob_sha"],
        "M2 retained M1 result",
    )
    for raw_path, expected in config["protected_file_git_blob_sha"].items():
        verify_blob(
            Path(raw_path),
            expected,
            f"M2 protected file {raw_path}",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-source", type=Path, required=True)
    parser.add_argument("--m1-source", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_paired_method_m2_sequential_resolution_v1.json"
        ),
    )
    parser.add_argument(
        "--m1-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_paired_method_m1_screen_v1.json"
        ),
    )
    parser.add_argument(
        "--m1-result",
        type=Path,
        default=Path(
            "model/results/f1b_r2_paired_method_m1_screen_2026-09-28.json"
        ),
    )
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_m2_config(config)
    validate_m2_environment(os.environ)
    verify_repository_contract(config)

    expected_shards = int(config["execution"]["shard_count"])
    if args.shard_count != expected_shards:
        raise ValueError("M2 runtime shard count differs from frozen design")
    if not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid M2 shard index")

    retained_m1_result = load(args.m1_result)
    validate_retained_m1_result(retained_m1_result, config)

    h1_expected = str(config["h1_source"]["combined_json_sha256"])
    h1_actual = sha256(args.h1_source)
    if h1_actual != h1_expected:
        raise ValueError("M2 H1 source SHA-256 mismatch")

    m1_expected = str(config["retained_m1"]["combined_json_sha256"])
    m1_actual = sha256(args.m1_source)
    if m1_actual != m1_expected:
        raise ValueError("M2 M1 source SHA-256 mismatch")
    if args.m1_source.stat().st_size != int(
        config["retained_m1"]["combined_json_size_bytes"]
    ):
        raise ValueError("M2 M1 source size mismatch")

    h1_source = load(args.h1_source)
    m1_source = load(args.m1_source)
    validate_m1_combined(m1_source, config)
    m1_config = load(args.m1_config)

    paired_config = load(
        Path(
            "model/benchmarks/"
            "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
        )
    )
    v2_config = load(
        Path("model/benchmarks/f1b_r2_kl_controlled_departure_design_v2.json")
    )
    review_config = load(
        Path("model/benchmarks/f1b_r2_distance_definition_review.json")
    )
    historical_config = load(
        Path("model/benchmarks/f1b_r2_controlled_departure_design.json")
    )
    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_config,
    )
    specs = select_scientific_specs(h1_source, m1_config)
    boundaries = build_m2_boundaries(config)

    retained_rows = {
        (
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        ): row
        for row in m1_source["rows"]
    }
    if len(retained_rows) != 3360:
        raise ValueError("M2 retained M1 row keys are not unique")

    rows: list[dict] = []
    selected_scientific_runs = 0
    started = time.perf_counter()

    for spec in specs:
        for replicate in range(spec.replicate_count):
            dataset_id = dataset_id_for(spec, replicate)
            datasets = simulate_paired_missingness_datasets(
                spec,
                replicate,
                paired_config=paired_config,
                departure_cases=departure_cases,
            )
            for missingness, dataset in zip(
                (0.0, 0.15),
                datasets,
                strict=True,
            ):
                scientific_run_id = (
                    f"{dataset_id}|RESTRICTION={spec.restriction}"
                    f"|MISSINGNESS={missingness:.2f}"
                )
                if stable_shard(
                    scientific_run_id,
                    args.shard_count,
                ) != args.shard_index:
                    continue

                selected_scientific_runs += 1
                fingerprint = dataset_fingerprint(dataset)
                method_rows = []
                for method_id in EXPECTED_METHODS_M2:
                    key = (scientific_run_id, method_id)
                    if key not in retained_rows:
                        raise ValueError(
                            f"M2 retained M1 row missing: {key}"
                        )
                    retained = retained_rows[key]
                    if fingerprint != str(retained["dataset_sha256"]):
                        raise ValueError(
                            "M2 regenerated dataset fingerprint mismatch"
                        )
                    result = characterize_stream(
                        retained,
                        spec=spec,
                        replicate=replicate,
                        dataset=dataset,
                        method_id=method_id,
                        paired_config=paired_config,
                        m1_config=m1_config,
                        m2_config=config,
                        boundaries=boundaries,
                    )
                    method_rows.append(result)

                if len(method_rows) != len(EXPECTED_METHODS_M2):
                    raise ValueError("M2 scientific run lacks paired methods")
                if len(
                    {row["dataset_sha256"] for row in method_rows}
                ) != 1:
                    raise ValueError("M2 paired methods saw different datasets")
                rows.extend(method_rows)

    if len(rows) != 4 * selected_scientific_runs:
        raise ValueError("M2 shard pairing count changed")

    result = {
        "design_id": config["design_id"],
        "status": "NON_AUTHORITATIVE_PAIRED_METHOD_M2_SHARD_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "h1_source_sha256": h1_actual,
        "m1_source_sha256": m1_actual,
        "shard_index": int(args.shard_index),
        "shard_count": int(args.shard_count),
        "selected_scientific_run_count": selected_scientific_runs,
        "method_row_count": len(rows),
        "row_identity_sha256": canonical_json_sha256(
            [
                [
                    row["scientific_run_id"],
                    row["inference_method"],
                ]
                for row in sorted(
                    rows,
                    key=lambda row: (
                        row["scientific_run_id"],
                        row["inference_method"],
                    ),
                )
            ]
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
        "boundary": dict(config["boundary"]),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
