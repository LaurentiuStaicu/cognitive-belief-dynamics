from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    simulate_paired_missingness_datasets,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    build_m2_boundaries,
    stable_shard,
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
from cognitive_epistemic_model.calibration.f1b_r2_s4_w0_execution import (
    validate_w0_config,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_w0_shard import (
    build_shard_result,
    is_imported_prefix_row,
    normalize_imported_m2_row,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-source", type=Path, required=True)
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument("--m2-combined", type=Path, required=True)
    parser.add_argument("--w0-plan", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument(
        "--w0-config",
        type=Path,
        default=Path("model/benchmarks/f1b_r2_s4_w0_execution_v1.json"),
    )
    parser.add_argument(
        "--m1-config",
        type=Path,
        default=Path("model/benchmarks/f1b_r2_paired_method_m1_screen_v1.json"),
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

    config = load(args.w0_config)
    validate_w0_config(config)
    validate_m2_environment(os.environ)

    raw = config["retained_sources"]["raw_sources"]
    if sha256(args.h1_source) != str(raw["h1_json_sha256"]):
        raise ValueError("S4 W0 H1 source SHA-256 mismatch")
    if sha256(args.s4_manifest) != str(raw["s4_manifest_json_sha256"]):
        raise ValueError("S4 W0 S4 manifest SHA-256 mismatch")
    if sha256(args.m2_combined) != str(raw["m2_json_sha256"]):
        raise ValueError("S4 W0 M2 combined SHA-256 mismatch")

    plan = load(args.w0_plan)
    if plan["status"] != "NON_AUTHORITATIVE_S4_W0_EXECUTION_PLAN_COMPLETE":
        raise ValueError("S4 W0 plan status changed")
    if plan["execution_authorized"] is not True:
        raise ValueError("S4 W0 plan is not authorized")
    if int(plan["shard_count"]) != 250:
        raise ValueError("S4 W0 plan shard count changed")
    if str(plan["shard_plan_sha256"]) != str(
        config["shards"]["shard_plan_sha256"]
    ):
        raise ValueError("S4 W0 plan digest changed")

    shard_index = int(args.shard_index)
    if not 0 <= shard_index < 250:
        raise ValueError("S4 W0 shard index outside 0..249")
    shard_plan = {
        int(row["shard_index"]): row for row in plan["shard_plan"]
    }
    if set(shard_plan) != set(range(250)):
        raise ValueError("S4 W0 shard-plan index coverage changed")
    expected = shard_plan[shard_index]

    h1_source = load(args.h1_source)
    s4_manifest = load(args.s4_manifest)
    m2_combined = load(args.m2_combined)
    m1_config = load(args.m1_config)
    m2_config = load(args.m2_config)
    s4_config = load(args.s4_config)

    scientific_rows = [
        row
        for row in s4_manifest["rows"]
        if 0 <= int(row["evaluation_replicate"]) <= 24
        and stable_shard(str(row["scientific_run_id"]), 250) == shard_index
    ]
    scientific_rows.sort(key=lambda row: str(row["scientific_run_id"]))
    if len(scientific_rows) != int(expected["scientific_run_count"]):
        raise ValueError("S4 W0 shard scientific-run count changed")

    expected_imported = int(expected["imported_scientific_run_count"])
    expected_new = int(expected["new_scientific_run_count"])
    if sum(is_imported_prefix_row(row) for row in scientific_rows) != expected_imported:
        raise ValueError("S4 W0 shard imported count changed")
    if sum(not is_imported_prefix_row(row) for row in scientific_rows) != expected_new:
        raise ValueError("S4 W0 shard new count changed")

    specs = select_s4_scientific_specs(
        h1_source,
        m1_config,
        s4_config,
    )
    spec_map = {
        (str(spec.identity), str(spec.restriction)): spec for spec in specs
    }
    if len(spec_map) != 75:
        raise ValueError("S4 W0 scientific spec coverage changed")

    m2_map = {
        (str(row["scientific_run_id"]), str(row["inference_method"])): row
        for row in m2_combined["rows"]
    }
    if len(m2_map) != 3360:
        raise ValueError("S4 W0 M2 row coverage changed")

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
    boundaries = build_m2_boundaries(m2_config)

    method_rows = []
    for scientific_row in scientific_rows:
        run_id = str(scientific_row["scientific_run_id"])
        key = (
            str(scientific_row["identity"]),
            str(scientific_row["restriction"]),
        )
        if key not in spec_map:
            raise ValueError("S4 W0 scientific spec missing")
        spec = spec_map[key]
        replicate = int(scientific_row["evaluation_replicate"])

        if is_imported_prefix_row(scientific_row):
            for method_id in EXPECTED_METHODS_M2:
                retained_key = (run_id, method_id)
                if retained_key not in m2_map:
                    raise ValueError("S4 W0 imported M2 row missing")
                method_rows.append(
                    normalize_imported_m2_row(m2_map[retained_key])
                )
            continue

        datasets = simulate_paired_missingness_datasets(
            spec,
            replicate,
            paired_config=paired_config,
            departure_cases=departure_cases,
        )
        missingness = float(scientific_row["missingness"])
        if missingness == 0.0:
            dataset = datasets[0]
        elif missingness == 0.15:
            dataset = datasets[1]
        else:
            raise ValueError("S4 W0 missingness regime changed")

        for method_id in EXPECTED_METHODS_M2:
            method_rows.append(
                run_new_stream(
                    scientific_row,
                    spec=spec,
                    replicate=replicate,
                    dataset=dataset,
                    method_id=method_id,
                    paired_config=paired_config,
                    m1_config=m1_config,
                    m2_config=m2_config,
                    boundaries=boundaries,
                )
            )

    result = build_shard_result(
        scientific_rows,
        method_rows,
        shard_index=shard_index,
        expected_imported_scientific_run_count=expected_imported,
        expected_new_scientific_run_count=expected_new,
    )
    result["provenance"] = {
        "h1_source_sha256": sha256(args.h1_source),
        "s4_manifest_sha256": sha256(args.s4_manifest),
        "m2_combined_sha256": sha256(args.m2_combined),
        "w0_plan_sha256": sha256(args.w0_plan),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
