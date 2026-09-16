from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.m1_e4_participant_recovery import (
    run_participant_recovery_benchmark,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run participant-aware hierarchical M1.E4 model recovery."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/m1_e4_participant_aware_screening.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--replicates",
        type=int,
        default=None,
        help="Optional smoke/debug override. Confirmation runs require frozen config.",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    if args.replicates is not None:
        if args.replicates <= 0:
            raise SystemExit("--replicates must be positive")
        config = {**config, "replicates": args.replicates}

    result = run_participant_recovery_benchmark(config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
