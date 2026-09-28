from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    EXPECTED_METHODS,
    canonical_json_sha256,
    evaluate_all_methods,
    validate_m1_config,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", type=Path, action="append", required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_paired_method_m1_screen_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_m1_config(config)

    parts = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.partition
    ]
    if not parts:
        raise ValueError("M1 combine requires partitions")
    shard_counts = {int(part["shard_count"]) for part in parts}
    if len(shard_counts) != 1:
        raise ValueError("M1 shard-count mismatch")
    shard_count = shard_counts.pop()
    indices = sorted(int(part["shard_index"]) for part in parts)
    if indices != list(range(shard_count)):
        raise ValueError("M1 partitions are incomplete or duplicated")
    if any(
        part["status"] != "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SHARD_RESULT"
        for part in parts
    ):
        raise ValueError("M1 partition status changed")
    if any(bool(value) for part in parts for value in part["boundary"].values()):
        raise ValueError("M1 partition boundary weakened")

    rows = [
        row
        for part in parts
        for row in part["rows"]
    ]
    if len(rows) != int(
        config["scientific_design"]["total_method_executions"]
    ):
        raise ValueError("M1 combined method row count changed")

    keys = [
        (str(row["scientific_run_id"]), str(row["inference_method"]))
        for row in rows
    ]
    if len(set(keys)) != len(keys):
        raise ValueError("M1 combined method rows are not unique")

    scientific_runs = {str(row["scientific_run_id"]) for row in rows}
    if len(scientific_runs) != int(
        config["scientific_design"]["total_scientific_restriction_runs"]
    ):
        raise ValueError("M1 combined scientific run count changed")

    methods = {str(row["inference_method"]) for row in rows}
    if methods != set(EXPECTED_METHODS):
        raise ValueError("M1 combined method coverage changed")
    for scientific_run in scientific_runs:
        run_methods = {
            str(row["inference_method"])
            for row in rows
            if row["scientific_run_id"] == scientific_run
        }
        if run_methods != set(EXPECTED_METHODS):
            raise ValueError("M1 scientific run is not fully paired")

    evaluation = evaluate_all_methods(rows, config)
    result = {
        **evaluation,
        "scientific_run_count": len(scientific_runs),
        "method_execution_count": len(rows),
        "combined_row_identity_sha256": canonical_json_sha256(
            sorted([list(key) for key in keys])
        ),
        "partition_count": len(parts),
        "partition_elapsed_seconds": sum(
            float(part["elapsed_seconds"]) for part in parts
        ),
        "rows": sorted(
            rows,
            key=lambda row: (
                row["scientific_run_id"],
                row["inference_method"],
            ),
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
