from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1a_transmission_recovery import (
    run_recovery_benchmark,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the prospective synthetic F1a transmission-recovery benchmark."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/f1a_transmission_recovery_core.json"),
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("model/experiments/f1a_transmission_recovery_contract.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--replicates",
        type=int,
        default=None,
        help=(
            "Optional smoke/debug override. Any override makes the result "
            "non-authoritative; the prospective config value is authoritative."
        ),
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    authoritative = args.replicates is None
    if args.replicates is not None:
        if args.replicates <= 0:
            raise SystemExit("--replicates must be positive")
        config = {**config, "replicates_per_grid_cell": args.replicates}

    result = run_recovery_benchmark(config, authoritative=authoritative)
    result["provenance"] = {
        "source_commit": git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "contract_path": str(args.contract),
        "contract_sha256": sha256(args.contract),
        "replicate_override": args.replicates,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
