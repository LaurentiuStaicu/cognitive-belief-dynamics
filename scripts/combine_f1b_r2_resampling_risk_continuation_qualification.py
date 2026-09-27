from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    combine_continuation_qualification_partitions,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Combine Stage C1 F1b R2 resampling-risk continuation "
            "qualification partitions."
        )
    )
    parser.add_argument(
        "--continuation-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_resampling_risk_continuation_v1.json"
        ),
    )
    parser.add_argument(
        "--partition",
        type=Path,
        action="append",
        required=True,
        dest="partitions",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    continuation = json.loads(
        args.continuation_config.read_text(encoding="utf-8")
    )
    parts = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.partitions
    ]
    provenance = [part.get("provenance") for part in parts]
    if any(row is None for row in provenance):
        raise ValueError("every Stage C1 partition must retain provenance")

    invariant_keys = (
        "source_commit",
        "paired_source_sha256",
        "stage_b_result_sha256",
        "continuation_config_sha256",
        "paired_config_sha256",
        "v2_config_sha256",
        "review_config_sha256",
        "historical_departure_config_sha256",
        "scientific_file_git_blob_sha",
    )
    first = provenance[0]
    for row in provenance[1:]:
        for key in invariant_keys:
            if row[key] != first[key]:
                raise ValueError(
                    f"Stage C1 provenance mismatch for {key}"
                )

    result = combine_continuation_qualification_partitions(
        parts,
        continuation,
    )
    result["provenance"] = {
        "source_commit": first["source_commit"],
        "paired_source_sha256": first["paired_source_sha256"],
        "stage_b_result_sha256": first["stage_b_result_sha256"],
        "continuation_config_sha256": first[
            "continuation_config_sha256"
        ],
        "paired_config_sha256": first["paired_config_sha256"],
        "v2_config_sha256": first["v2_config_sha256"],
        "review_config_sha256": first["review_config_sha256"],
        "historical_departure_config_sha256": first[
            "historical_departure_config_sha256"
        ],
        "scientific_file_git_blob_sha": first[
            "scientific_file_git_blob_sha"
        ],
        "partition_files": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "shard_index": int(part["shard_index"]),
                "qualified_run_count": int(
                    part["qualified_run_count"]
                ),
                "qualification_pass_count": int(
                    part["qualification_pass_count"]
                ),
            }
            for path, part in zip(
                args.partitions,
                parts,
                strict=True,
            )
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
