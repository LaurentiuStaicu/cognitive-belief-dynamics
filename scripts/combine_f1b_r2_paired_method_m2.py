from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    canonical_json_sha256,
    evaluate_all_methods,
    validate_m2_config,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--partition",
        action="append",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_paired_method_m2_sequential_resolution_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_m2_config(config)
    expected_partitions = int(config["execution"]["shard_count"])
    if len(args.partition) != expected_partitions:
        raise ValueError(
            f"M2 requires exactly {expected_partitions} partitions"
        )

    parts = [load(path) for path in args.partition]
    indices = sorted(int(part["shard_index"]) for part in parts)
    if indices != list(range(expected_partitions)):
        raise ValueError("M2 partition index coverage changed")
    if any(int(part["shard_count"]) != expected_partitions for part in parts):
        raise ValueError("M2 partition shard-count mismatch")
    if any(part["design_id"] != config["design_id"] for part in parts):
        raise ValueError("M2 partition design identity mismatch")
    if any(
        part["status"] != "NON_AUTHORITATIVE_PAIRED_METHOD_M2_SHARD_RESULT"
        for part in parts
    ):
        raise ValueError("M2 partition status mismatch")
    if any(part["authoritative"] is not False for part in parts):
        raise ValueError("M2 partition became authoritative")
    if any(any(bool(v) for v in part["boundary"].values()) for part in parts):
        raise ValueError("M2 partition weakened scientific boundary")

    h1_hashes = {str(part["h1_source_sha256"]) for part in parts}
    m1_hashes = {str(part["m1_source_sha256"]) for part in parts}
    if h1_hashes != {str(config["h1_source"]["combined_json_sha256"])}:
        raise ValueError("M2 H1 provenance differs across partitions")
    if m1_hashes != {
        str(config["retained_m1"]["combined_json_sha256"])
    }:
        raise ValueError("M2 M1 provenance differs across partitions")

    rows = [
        row
        for part in parts
        for row in part["rows"]
    ]
    scientific_count = sum(
        int(part["selected_scientific_run_count"])
        for part in parts
    )
    if scientific_count != 840:
        raise ValueError("M2 scientific-run count changed")
    if len(rows) != 3360:
        raise ValueError("M2 method-execution count changed")

    identities = [
        [str(row["scientific_run_id"]), str(row["inference_method"])]
        for row in sorted(
            rows,
            key=lambda row: (
                row["scientific_run_id"],
                row["inference_method"],
            ),
        )
    ]
    if len({tuple(value) for value in identities}) != 3360:
        raise ValueError("M2 combined row identities are not unique")
    for scientific_run_id in {
        str(row["scientific_run_id"]) for row in rows
    }:
        methods = {
            str(row["inference_method"])
            for row in rows
            if str(row["scientific_run_id"]) == scientific_run_id
        }
        if methods != set(EXPECTED_METHODS_M2):
            raise ValueError("M2 combined scientific run lacks paired methods")

    evaluation = evaluate_all_methods(rows, config)
    result = {
        "design_id": config["design_id"],
        "status": "NON_AUTHORITATIVE_PAIRED_METHOD_M2_COMBINED_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "partition_count": expected_partitions,
        "scientific_run_count": scientific_count,
        "method_execution_count": len(rows),
        "combined_row_identity_sha256": canonical_json_sha256(identities),
        "partition_elapsed_seconds": {
            str(int(part["shard_index"])): float(part["elapsed_seconds"])
            for part in sorted(
                parts,
                key=lambda part: int(part["shard_index"]),
            )
        },
        **evaluation,
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
