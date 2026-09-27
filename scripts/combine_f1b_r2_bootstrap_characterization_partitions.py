from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_bootstrap_characterization import (
    combine_bootstrap_characterization_partitions,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Combine replicate-partitioned non-authoritative F1b R2 "
            "bootstrap characterization results."
        )
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

    loaded = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.partitions
    ]
    provenance = [part.get("provenance") for part in loaded]
    if any(item is None for item in provenance):
        raise ValueError("every partition must retain provenance")

    invariant_provenance = (
        "source_commit",
        "config_sha256",
        "departure_config_sha256",
    )
    first = provenance[0]
    for item in provenance[1:]:
        for key in invariant_provenance:
            if item[key] != first[key]:
                raise ValueError(f"partition provenance mismatch for {key}")

    result = combine_bootstrap_characterization_partitions(loaded)
    result["provenance"] = {
        "source_commit": first["source_commit"],
        "config_path": first["config_path"],
        "config_sha256": first["config_sha256"],
        "departure_config_path": first["departure_config_path"],
        "departure_config_sha256": first["departure_config_sha256"],
        "combined_from_replicate_partitions": True,
        "partition_files": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "execution_replicate_indices": part[
                    "execution_replicate_indices"
                ],
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
