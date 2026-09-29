from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    simulate_paired_missingness_datasets,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    build_m2_boundaries,
    validate_m2_environment,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_executor import (
    run_new_stream,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_scientific_matrix import (
    select_s4_scientific_specs,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_new_executor_equivalence import (
    build_equivalence_result,
    select_equivalence_rows,
    validate_equivalence_config,
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


def verify_repository_contract(config: dict) -> None:
    for raw_path, expected in config[
        "protected_file_git_blob_sha"
    ].items():
        actual = git_blob_sha(Path(raw_path))
        if actual != str(expected):
            raise ValueError(
                f"S4 equivalence protected file changed: "
                f"{raw_path}: {actual} != {expected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-source", type=Path, required=True)
    parser.add_argument("--m2-source", type=Path, required=True)
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_s4_new_executor_equivalence_v1.json"
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
        "--m2-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_paired_method_m2_sequential_resolution_v1.json"
        ),
    )
    parser.add_argument(
        "--s4-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_s4_broad_scientific_matrix_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_equivalence_config(config)
    validate_m2_environment(os.environ)
    verify_repository_contract(config)

    expected_h1 = str(
        config["retained_sources"]["h1"]["json_sha256"]
    )
    if sha256(args.h1_source) != expected_h1:
        raise ValueError("S4 equivalence H1 source SHA-256 mismatch")

    expected_m2 = str(
        config["retained_sources"]["m2"]["json_sha256"]
    )
    if sha256(args.m2_source) != expected_m2:
        raise ValueError("S4 equivalence M2 source SHA-256 mismatch")

    expected_s4 = str(
        config["retained_sources"]["s4_matrix"][
            "manifest_json_sha256"
        ]
    )
    if sha256(args.s4_manifest) != expected_s4:
        raise ValueError("S4 equivalence S4 manifest SHA-256 mismatch")

    h1_source = load(args.h1_source)
    m2_source = load(args.m2_source)
    s4_manifest = load(args.s4_manifest)
    selected = select_equivalence_rows(m2_source, config)

    m1_config = load(args.m1_config)
    m2_config = load(args.m2_config)
    s4_config = load(args.s4_config)

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

    specs = select_s4_scientific_specs(
        h1_source,
        m1_config,
        s4_config,
    )
    spec_map = {
        (str(spec.identity), str(spec.restriction)): spec
        for spec in specs
    }
    if len(spec_map) != 75:
        raise ValueError("S4 equivalence scientific specs not unique")

    s4_rows = {
        str(row["scientific_run_id"]): row
        for row in s4_manifest["rows"]
    }
    if len(s4_rows) != 15000:
        raise ValueError("S4 equivalence S4 row identities changed")

    required_run_ids = {
        str(row["scientific_run_id"]) for row in selected
    }
    if len(required_run_ids) != 7:
        raise ValueError("S4 equivalence selected run count changed")

    dataset_cache: dict[str, object] = {}
    spec_cache: dict[str, object] = {}
    for retained in selected:
        scientific_run_id = str(retained["scientific_run_id"])
        if scientific_run_id in dataset_cache:
            continue
        if scientific_run_id not in s4_rows:
            raise ValueError("S4 equivalence selected run absent from S4")

        key = (
            str(retained["identity"]),
            str(retained["restriction"]),
        )
        if key not in spec_map:
            raise ValueError("S4 equivalence scientific spec missing")
        spec = spec_map[key]
        replicate = int(retained["evaluation_replicate"])
        datasets = simulate_paired_missingness_datasets(
            spec,
            replicate,
            paired_config=paired_config,
            departure_cases=departure_cases,
        )
        missingness = float(retained["missingness_rate"])
        if missingness == 0.0:
            dataset = datasets[0]
        elif missingness == 0.15:
            dataset = datasets[1]
        else:
            raise ValueError("S4 equivalence missingness changed")

        dataset_cache[scientific_run_id] = dataset
        spec_cache[scientific_run_id] = spec

    boundaries = build_m2_boundaries(m2_config)
    reproduced = []
    started = time.perf_counter()
    for retained in selected:
        scientific_run_id = str(retained["scientific_run_id"])
        scientific_row = s4_rows[scientific_run_id]
        spec = spec_cache[scientific_run_id]
        reproduced.append(
            run_new_stream(
                scientific_row,
                spec=spec,
                replicate=int(retained["evaluation_replicate"]),
                dataset=dataset_cache[scientific_run_id],
                method_id=str(retained["inference_method"]),
                paired_config=paired_config,
                m1_config=m1_config,
                m2_config=m2_config,
                boundaries=boundaries,
            )
        )

    result = build_equivalence_result(
        selected_retained_rows=selected,
        reproduced_rows=reproduced,
        config=config,
    )
    result["elapsed_seconds"] = time.perf_counter() - started
    result["provenance"] = {
        "config_sha256": sha256(args.config),
        "h1_source_sha256": sha256(args.h1_source),
        "m2_source_sha256": sha256(args.m2_source),
        "s4_manifest_sha256": sha256(args.s4_manifest),
        "executor_git_blob_sha": git_blob_sha(
            Path(
                "src/cognitive_epistemic_model/calibration/"
                "f1b_r2_s4_broad_executor.py"
            )
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
