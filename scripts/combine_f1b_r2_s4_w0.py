from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_s4_w0_combine import (
    combine_w0_shards,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--w0-plan", type=Path, required=True)
    parser.add_argument(
        "--w0-config",
        type=Path,
        default=Path("model/benchmarks/f1b_r2_s4_w0_execution_v1.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.w0_config)
    plan = load(args.w0_plan)
    files = sorted(
        args.shard_root.glob("*/f1b-r2-s4-w0-shard-*.json")
    )
    if len(files) != 250:
        raise ValueError(
            f"expected 250 W0 shard JSON files, got {len(files)}"
        )

    result = combine_w0_shards(
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
