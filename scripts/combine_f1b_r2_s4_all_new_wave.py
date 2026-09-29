from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_s4_all_new_wave import (
    combine_wave_shards,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--wave-plan", type=Path, required=True)
    parser.add_argument("--wave-id", required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/f1b_r2_s4_all_new_wave_execution_v1.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    wave_id = str(args.wave_id)
    files = sorted(args.shard_root.glob("*/f1b-r2-s4-all-new-shard-*.json"))
    if len(files) != 250:
        raise ValueError(
            f"expected 250 S4 all-new shard JSON files, got {len(files)}"
        )

    result = combine_wave_shards(
        [load(path) for path in files],
        plan=load(args.wave_plan),
        config=load(args.config),
        wave_id=wave_id,
    )
    result["source_shard_file_count"] = len(files)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
