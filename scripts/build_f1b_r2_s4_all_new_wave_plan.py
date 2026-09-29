from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_s4_all_new_wave import (
    build_all_new_wave_plan,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument(
        "--wave-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_s4_w1_execution_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build_all_new_wave_plan(
        load(args.s4_manifest),
        load(args.wave_config),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
