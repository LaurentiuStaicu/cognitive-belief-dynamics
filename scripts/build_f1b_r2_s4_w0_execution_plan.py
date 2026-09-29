from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_s4_w0_execution import (
    build_w0_plan,
    validate_w0_config,
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
    for raw_path, expected in config["protected_file_git_blob_sha"].items():
        path = Path(raw_path)
        actual = git_blob_sha(path)
        if actual != str(expected):
            raise ValueError(
                f"S4 W0 protected file changed: {raw_path}: "
                f"{actual} != {expected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/f1b_r2_s4_w0_execution_v1.json"),
    )
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument("--m2-combined", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_w0_config(config)
    verify_protected_files(config)

    raw = config["retained_sources"]["raw_sources"]
    if sha256(args.s4_manifest) != str(raw["s4_manifest_json_sha256"]):
        raise ValueError("S4 W0 manifest SHA-256 mismatch")
    if sha256(args.m2_combined) != str(raw["m2_json_sha256"]):
        raise ValueError("S4 W0 M2 combined SHA-256 mismatch")

    s4_manifest = load(args.s4_manifest)
    m2_combined = load(args.m2_combined)
    plan = build_w0_plan(s4_manifest, m2_combined, config)
    plan["provenance"] = {
        "config_sha256": sha256(args.config),
        "s4_manifest_sha256": sha256(args.s4_manifest),
        "m2_combined_sha256": sha256(args.m2_combined),
        "s4_matrix_artifact_id": int(raw["s4_matrix_artifact_id"]),
        "m2_artifact_id": int(raw["m2_artifact_id"]),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
