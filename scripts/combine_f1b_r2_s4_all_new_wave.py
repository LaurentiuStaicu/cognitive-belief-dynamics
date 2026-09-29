from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_s4_all_new_wave_combine import (
    combine_all_new_wave_shards,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--wave-plan", type=Path, required=True)
    parser.add_argument(
        "--wave-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_s4_w1_execution_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.wave_config)
    plan = load(args.wave_plan)
    wave_id = str(config["wave"]["wave_id"]).lower()
    files = sorted(
        args.shard_root.glob(f"*/f1b-r2-s4-{wave_id}-shard-*.json")
    )
    if len(files) != 250:
        raise ValueError(
            f"expected 250 S4 all-new-wave shard JSON files, got {len(files)}"
        )

    result = combine_all_new_wave_shards(
        [load(path) for path in files],
        plan=plan,
        config=config,
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
