from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_scientific_matrix import (
    build_s4_scientific_manifest,
    validate_s4_matrix_config,
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


def verify_repository_contract(config: dict) -> None:
    for raw_path, expected in config[
        "protected_file_git_blob_sha"
    ].items():
        path = Path(raw_path)
        actual = git_blob_sha(path)
        if actual != str(expected):
            raise ValueError(
                f"S4 protected file changed: {raw_path}: "
                f"{actual} != {expected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-source", type=Path, required=True)
    parser.add_argument(
        "--m1-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_paired_method_m1_screen_v1.json"
        ),
    )
    parser.add_argument(
        "--s4-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_s4_broad_scientific_matrix_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    s4_config = load(args.s4_config)
    validate_s4_matrix_config(s4_config)
    verify_repository_contract(s4_config)

    expected_source_sha = str(
        s4_config["source"]["h1_json_sha256"]
    )
    actual_source_sha = sha256(args.h1_source)
    if actual_source_sha != expected_source_sha:
        raise ValueError("S4 H1 source SHA-256 mismatch")

    h1_source = load(args.h1_source)
    m1_config = load(args.m1_config)
    manifest = build_s4_scientific_manifest(
        h1_source,
        m1_config,
        s4_config,
    )
    manifest["provenance"] = {
        "h1_source_sha256": actual_source_sha,
        "h1_artifact_id": int(
            s4_config["source"]["h1_artifact_id"]
        ),
        "m1_config_git_blob_sha": s4_config[
            "protected_file_git_blob_sha"
        ][
            "model/benchmarks/"
            "f1b_r2_paired_method_m1_screen_v1.json"
        ],
        "s4_config_sha256": sha256(args.s4_config),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
