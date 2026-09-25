from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r1_high_replicate import (
    run_r1_high_replicate_characterization,
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
        description="Run the non-authoritative F1b R1 high-replicate characterization."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/f1b_r1_high_replicate_characterization.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    parser.add_argument(
        "--replicates",
        type=int,
        default=None,
        help="Optional non-authoritative debug override.",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.replicates is not None:
        if args.replicates <= 0:
            raise SystemExit("--replicates must be positive")
        config = {**config, "replicates_per_cell": args.replicates}

    result = run_r1_high_replicate_characterization(config)
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
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
