from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    replay_retained_paired_bootstrap,
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
            "Replay exact retained F1b R2 KL v2 paired bootstrap streams "
            "through the frozen resampling-risk controller."
        )
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_resampling_risk_controller_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    input_sha256 = sha256(args.input)
    expected_sha256 = str(
        config["replay_source"]["exact_json_sha256"]
    )
    if input_sha256 != expected_sha256:
        raise ValueError(
            "retained replay input SHA-256 mismatch: "
            f"{input_sha256} != {expected_sha256}"
        )

    retained = json.loads(args.input.read_text(encoding="utf-8"))
    result = replay_retained_paired_bootstrap(retained, config)
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "input_path": str(args.input),
        "input_sha256": input_sha256,
        "controller_config_path": str(args.config),
        "controller_config_sha256": sha256(args.config),
        "retained_artifact_id": int(
            config["replay_source"]["exact_artifact_id"]
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
