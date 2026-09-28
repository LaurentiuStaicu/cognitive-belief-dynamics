from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_c2_continuation import (
    combine_c2_partitions,
    validate_homogeneous_c2_config,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Combine homogeneous F1b R2 Stage-C2 continuation partitions."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_homogeneous_c2_continuation_v1.json"
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

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_homogeneous_c2_config(config)

    partitions = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.partitions
    ]
    result = combine_c2_partitions(partitions, config)
    result["provenance"] = {
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "partition_files": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "shard_index": int(partition["shard_index"]),
                "continued_run_count": int(
                    partition["continued_run_count"]
                ),
            }
            for path, partition in zip(
                args.partitions,
                partitions,
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
