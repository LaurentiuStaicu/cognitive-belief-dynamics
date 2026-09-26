from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery import (
    run_smoke_restriction_engine,
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
        description="Run the non-authoritative F1b R2 restriction-recovery smoke engine."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_structural_restriction_recovery_smoke.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    parser.add_argument(
        "--bootstrap-draws",
        type=int,
        default=None,
        help="Optional smoke override; remains non-authoritative.",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.bootstrap_draws is not None:
        if args.bootstrap_draws <= 0:
            raise SystemExit("--bootstrap-draws must be positive")
        bootstrap = {
            **config["bootstrap"],
            "draws": args.bootstrap_draws,
            "minimum_successful_draws": args.bootstrap_draws,
        }
        config = {**config, "bootstrap": bootstrap}

    result = run_smoke_restriction_engine(config)
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "bootstrap_draw_override": args.bootstrap_draws,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
