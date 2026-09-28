from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_s4_method_binding import (
    build_s4_bound_execution_manifest,
    validate_protected_files,
    validate_s4_method_binding_config,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/f1b_r2_s4_method_binding_v1.json"),
    )
    parser.add_argument(
        "--m2-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_paired_method_m2_sequential_resolution_2026-09-28.json"
        ),
    )
    parser.add_argument(
        "--s4-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_s4_broad_scientific_matrix_2026-09-28.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_s4_method_binding_config(config)
    validate_protected_files(config, Path("."))

    if git_blob_sha(args.m2_result) != str(
        config["retained_m2"]["result_git_blob_sha"]
    ):
        raise ValueError("retained M2 result Git blob mismatch")
    if git_blob_sha(args.s4_result) != str(
        config["retained_s4_matrix"]["result_git_blob_sha"]
    ):
        raise ValueError("retained S4 matrix result Git blob mismatch")

    m2_result = load(args.m2_result)
    s4_result = load(args.s4_result)
    manifest = build_s4_bound_execution_manifest(
        m2_result,
        s4_result,
        config,
    )
    manifest["provenance"] = {
        "config_sha256": sha256(args.config),
        "m2_result_git_blob_sha": git_blob_sha(args.m2_result),
        "s4_result_git_blob_sha": git_blob_sha(args.s4_result),
        "m2_artifact_id": int(config["retained_m2"]["artifact_id"]),
        "s4_matrix_artifact_id": int(
            config["retained_s4_matrix"]["artifact_id"]
        ),
        "m2_combined_json_sha256": config["retained_m2"][
            "combined_json_sha256"
        ],
        "s4_manifest_json_sha256": config["retained_s4_matrix"][
            "manifest_json_sha256"
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
