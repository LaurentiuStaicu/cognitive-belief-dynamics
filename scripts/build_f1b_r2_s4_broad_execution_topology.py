from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_execution_topology import (
    build_topology_manifest,
    validate_topology_config,
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
                f"S4 topology protected file changed: "
                f"{raw_path}: {actual} != {expected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_s4_broad_execution_topology_v1.json"
        ),
    )
    parser.add_argument(
        "--prefix-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_s4_m2_prefix_bridge_2026-09-29.json"
        ),
    )
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_topology_config(config)
    verify_protected_files(config)

    prefix_spec = config["retained_sources"]["prefix_bridge_result"]
    if git_blob_sha(args.prefix_result) != str(prefix_spec["git_blob_sha"]):
        raise ValueError("S4 topology prefix-result Git blob mismatch")

    s4_spec = config["retained_sources"]["s4_matrix_result"]
    if sha256(args.s4_manifest) != str(s4_spec["manifest_json_sha256"]):
        raise ValueError("S4 topology raw manifest SHA-256 mismatch")

    prefix_result = load(args.prefix_result)
    if prefix_result["status"] != (
        "NON_AUTHORITATIVE_S4_M2_PREFIX_BRIDGE_COMPLETE_RETAINED"
    ):
        raise ValueError("S4 topology retained prefix status changed")
    if prefix_result["import_identity"]["prefix_import_authorized"] is not True:
        raise ValueError("S4 topology prefix import is not authorized")

    s4_manifest = load(args.s4_manifest)
    result = build_topology_manifest(
        s4_manifest,
        prefix_result,
        config,
    )
    result["provenance"] = {
        "config_sha256": sha256(args.config),
        "prefix_result_git_blob_sha": git_blob_sha(args.prefix_result),
        "s4_manifest_sha256": sha256(args.s4_manifest),
        "s4_matrix_artifact_id": int(s4_spec["artifact_id"]),
        "prefix_bridge_artifact_id": int(prefix_spec["artifact_id"]),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
