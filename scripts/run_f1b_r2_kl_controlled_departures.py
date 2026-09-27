from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_kl_controlled_departures import (
    generate_kl_controlled_departure_design,
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
        description=(
            "Generate deterministic F1b R2 KL-controlled departure design v1."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_kl_controlled_departure_design_v1.json"
        ),
    )
    parser.add_argument(
        "--review-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_distance_definition_review.json"
        ),
    )
    parser.add_argument(
        "--historical-departure-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    review_config = json.loads(
        args.review_config.read_text(encoding="utf-8")
    )
    historical_config = json.loads(
        args.historical_departure_config.read_text(encoding="utf-8")
    )
    result = generate_kl_controlled_departure_design(
        config,
        review_config,
        historical_config,
    )
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "review_config_path": str(args.review_config),
        "review_config_sha256": sha256(args.review_config),
        "historical_departure_config_path": str(
            args.historical_departure_config
        ),
        "historical_departure_config_sha256": sha256(
            args.historical_departure_config
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
