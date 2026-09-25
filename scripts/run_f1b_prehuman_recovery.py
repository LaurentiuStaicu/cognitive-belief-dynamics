from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    run_smoke_benchmark,
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
        description="Run the non-authoritative F1b pre-human synthetic recovery smoke benchmark."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/f1b_prehuman_model_recovery_smoke.json"),
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("model/experiments/f1b_prehuman_model_recovery_contract.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--source-commit",
        default=None,
        help="Exact source commit for provenance; defaults to git rev-parse HEAD.",
    )
    parser.add_argument(
        "--replicates",
        type=int,
        default=None,
        help="Optional smoke override; all F1b engine runs remain non-authoritative.",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.replicates is not None:
        if args.replicates <= 0:
            raise SystemExit("--replicates must be positive")
        config = {**config, "replicates": args.replicates}

    result = run_smoke_benchmark(config)
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
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
