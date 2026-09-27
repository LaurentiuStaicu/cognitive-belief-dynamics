from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_bootstrap_characterization import (
    run_bootstrap_characterization,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def parse_replicate_indices(value: str | None) -> tuple[int, ...] | None:
    if value is None:
        return None
    indices: list[int] = []
    for token in value.split(","):
        token = token.strip()
        if not token:
            raise ValueError("empty replicate-index token")
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if end < start:
                raise ValueError("replicate-index range must be increasing")
            indices.extend(range(start, end + 1))
        else:
            indices.append(int(token))
    normalized = tuple(indices)
    if tuple(sorted(set(normalized))) != normalized:
        raise ValueError(
            "replicate indices must be unique and strictly increasing"
        )
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run non-authoritative F1b R2 bootstrap characterization."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_bootstrap_characterization_design.json"
        ),
    )
    parser.add_argument(
        "--departure-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    parser.add_argument(
        "--replicate-indices",
        default=None,
        help=(
            "Execution-only replicate partition, e.g. 0-4 or 0,2,4. "
            "The scientific evaluation count in the config is unchanged."
        ),
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    departure_config = json.loads(
        args.departure_config.read_text(encoding="utf-8")
    )
    replicate_indices = parse_replicate_indices(args.replicate_indices)
    result = run_bootstrap_characterization(
        config,
        departure_config,
        replicate_indices=replicate_indices,
    )
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "departure_config_path": str(args.departure_config),
        "departure_config_sha256": sha256(args.departure_config),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
