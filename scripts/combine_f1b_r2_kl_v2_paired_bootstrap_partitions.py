from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization import (
    combine_paired_bootstrap_partitions,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Combine paired same-dataset F1b R2 KL v2 bootstrap "
            "characterization partitions."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
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
    loaded = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.partitions
    ]
    provenance = [part.get("provenance") for part in loaded]
    if any(item is None for item in provenance):
        raise ValueError("every paired partition must retain provenance")

    invariant_keys = (
        "source_commit",
        "config_sha256",
        "v2_config_sha256",
        "v2_qualification_result_sha256",
        "review_config_sha256",
        "historical_departure_config_sha256",
    )
    first = provenance[0]
    for item in provenance[1:]:
        for key in invariant_keys:
            if item[key] != first[key]:
                raise ValueError(
                    f"paired partition provenance mismatch for {key}"
                )

    result = combine_paired_bootstrap_partitions(loaded, config)
    result["provenance"] = {
        "source_commit": first["source_commit"],
        "config_path": first["config_path"],
        "config_sha256": first["config_sha256"],
        "v2_config_path": first["v2_config_path"],
        "v2_config_sha256": first["v2_config_sha256"],
        "v2_qualification_result_path": first[
            "v2_qualification_result_path"
        ],
        "v2_qualification_result_sha256": first[
            "v2_qualification_result_sha256"
        ],
        "review_config_path": first["review_config_path"],
        "review_config_sha256": first["review_config_sha256"],
        "historical_departure_config_path": first[
            "historical_departure_config_path"
        ],
        "historical_departure_config_sha256": first[
            "historical_departure_config_sha256"
        ],
        "combined_from_replicate_partitions": True,
        "partition_files": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "replicate_indices": part[
                    "execution_replicate_indices"
                ],
                "restriction_run_count": int(
                    part["restriction_run_count"]
                ),
            }
            for path, part in zip(args.partitions, loaded, strict=True)
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
