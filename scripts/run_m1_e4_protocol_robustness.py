from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.m1_e4_protocol_robustness import (
    run_protocol_robustness_cell,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "model/benchmarks/m1_e4_protocol_robustness_200.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one frozen M1.E4 Phase-M protocol-robustness cell."
    )
    parser.add_argument("--profile", required=True)
    parser.add_argument("--generator", required=True, choices=("EVSD", "2HT"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--replicates",
        type=int,
        default=None,
        help="Diagnostic override only. Authoritative Phase-M execution must omit this option.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = json.loads(args.config.read_text())
    result = run_protocol_robustness_cell(
        config,
        profile_id=args.profile,
        generator=args.generator,
        replicate_override=args.replicates,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
