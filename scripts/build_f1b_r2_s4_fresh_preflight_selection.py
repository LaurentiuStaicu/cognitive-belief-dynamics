from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_s4_fresh_replicate_preflight import (
    build_preflight_selection_manifest,
    validate_preflight_config,
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


def verify_protected_files(config: dict) -> None:
    for raw_path, expected in config[
        "protected_file_git_blob_sha"
    ].items():
        path = Path(raw_path)
        actual = git_blob_sha(path)
        if actual != str(expected):
            raise ValueError(
                f"S4 fresh-preflight protected file changed: "
                f"{raw_path}: {actual} != {expected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_s4_fresh_replicate_preflight_v1.json"
        ),
    )
    parser.add_argument(
        "--equivalence-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_s4_new_executor_equivalence_2026-09-29.json"
        ),
    )
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_preflight_config(config)
    verify_protected_files(config)

    eq_source = config["retained_sources"]["executor_equivalence"]
    if git_blob_sha(args.equivalence_result) != str(
        eq_source["result_git_blob_sha"]
    ):
        raise ValueError("S4 fresh-preflight equivalence-result Git blob mismatch")

    source = config["retained_sources"]["s4_matrix"]
    if sha256(args.s4_manifest) != str(source["manifest_json_sha256"]):
        raise ValueError("S4 fresh-preflight manifest SHA-256 mismatch")

    equivalence_result = load(args.equivalence_result)
    manifest = load(args.s4_manifest)
    result = build_preflight_selection_manifest(
        manifest,
        equivalence_result,
        config,
    )
    result["provenance"] = {
        "config_sha256": sha256(args.config),
        "equivalence_result_git_blob_sha": git_blob_sha(
            args.equivalence_result
        ),
        "equivalence_raw_result_json_sha256": eq_source[
            "raw_result_json_sha256"
        ],
        "s4_manifest_sha256": sha256(args.s4_manifest),
        "s4_matrix_artifact_id": int(source["artifact_id"]),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
