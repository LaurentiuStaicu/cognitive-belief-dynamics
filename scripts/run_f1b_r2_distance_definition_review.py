from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_distance_definition_review import (
    run_distance_definition_review,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def load_cases(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    parsed: list[dict] = []
    for row in rows:
        parsed.append(
            {
                **row,
                "sign": int(row["sign"]),
                "requested_cbd_rms_distance": float(
                    row["requested_cbd_rms_distance"]
                ),
                "achieved_cbd_rms_distance": float(
                    row["achieved_cbd_rms_distance"]
                ),
                "general_coefficients": json.loads(
                    row["general_coefficients"]
                ),
                "nearest_cbd_parameters": json.loads(
                    row["nearest_cbd_parameters"]
                ),
            }
        )
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run deterministic F1b R2 scientific nearest-CBD "
            "distance-definition review."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_distance_definition_review.json"
        ),
    )
    parser.add_argument(
        "--departure-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ),
    )
    parser.add_argument(
        "--bound-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_projection_bound_sensitivity.json"
        ),
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_complement_sign_geometry_case_summary_2026-09-27.tsv"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    departure_config = json.loads(
        args.departure_config.read_text(encoding="utf-8")
    )
    bound_config = json.loads(
        args.bound_config.read_text(encoding="utf-8")
    )
    retained_cases = load_cases(args.cases)

    result = run_distance_definition_review(
        config,
        departure_config,
        bound_config,
        retained_cases,
    )
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "departure_config_path": str(args.departure_config),
        "departure_config_sha256": sha256(args.departure_config),
        "bound_config_path": str(args.bound_config),
        "bound_config_sha256": sha256(args.bound_config),
        "retained_cases_path": str(args.cases),
        "retained_cases_sha256": sha256(args.cases),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
