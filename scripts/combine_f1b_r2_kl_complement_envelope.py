from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_kl_complement_envelope import (
    combine_complement_kl_envelope_rays,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Combine deterministic F1b R2 complement KL envelope rays."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_kl_complement_envelope_diagnostic.json"
        ),
    )
    parser.add_argument(
        "--ray",
        type=Path,
        action="append",
        required=True,
        dest="rays",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    loaded = [json.loads(path.read_text(encoding="utf-8")) for path in args.rays]
    provenance = [row.get("provenance") for row in loaded]
    if any(item is None for item in provenance):
        raise ValueError("every envelope ray must retain provenance")

    invariant_keys = (
        "source_commit",
        "config_sha256",
        "kl_config_sha256",
        "review_config_sha256",
        "historical_departure_config_sha256",
    )
    first = provenance[0]
    for item in provenance[1:]:
        for key in invariant_keys:
            if item[key] != first[key]:
                raise ValueError(f"envelope ray provenance mismatch for {key}")

    result = combine_complement_kl_envelope_rays(loaded, config)
    result["provenance"] = {
        "source_commit": first["source_commit"],
        "config_path": first["config_path"],
        "config_sha256": first["config_sha256"],
        "kl_config_path": first["kl_config_path"],
        "kl_config_sha256": first["kl_config_sha256"],
        "review_config_path": first["review_config_path"],
        "review_config_sha256": first["review_config_sha256"],
        "historical_departure_config_path": first[
            "historical_departure_config_path"
        ],
        "historical_departure_config_sha256": first[
            "historical_departure_config_sha256"
        ],
        "combined_from_ray_partitions": True,
        "ray_files": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "anchor_id": row["anchor_id"],
                "sign": row["sign"],
                "point_count": row["point_count"],
            }
            for path, row in zip(args.rays, loaded, strict=True)
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
