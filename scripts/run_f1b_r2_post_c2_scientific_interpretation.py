from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_post_c2_scientific_interpretation import (
    build_post_c2_characterization,
    validate_interpretation_config,
    validate_retained_results,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def verify_sha256(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != str(expected):
        raise ValueError(f"{label} SHA-256 mismatch: {actual} != {expected}")


def verify_blob(path: Path, expected: str, label: str) -> None:
    actual = git_blob_sha(path)
    if actual != str(expected):
        raise ValueError(f"{label} Git blob mismatch: {actual} != {expected}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct and characterize the final homogeneous F1b R2 "
            "three-outcome state from retained H2 and C2 artifacts without "
            "new simulation."
        )
    )
    parser.add_argument("--h2-raw", type=Path, required=True)
    parser.add_argument("--c2-raw", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_post_c2_scientific_interpretation_v1.json"
        ),
    )
    parser.add_argument(
        "--h2-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_homogeneous_stage_b_rebuild_2026-09-28.json"
        ),
    )
    parser.add_argument(
        "--c2-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_homogeneous_c2_continuation_2026-09-28.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_interpretation_config(config)

    h2_spec = config["retained_h2"]
    c2_spec = config["retained_c2"]

    verify_blob(
        args.h2_result,
        h2_spec["result_git_blob_sha"],
        "retained H2 result",
    )
    verify_blob(
        args.c2_result,
        c2_spec["result_git_blob_sha"],
        "retained C2 result",
    )
    verify_sha256(
        args.h2_raw,
        h2_spec["raw_json_sha256"],
        "raw H2 replay",
    )
    verify_sha256(
        args.c2_raw,
        c2_spec["combined_json_sha256"],
        "raw C2 combined result",
    )
    if args.h2_raw.stat().st_size != int(h2_spec["raw_json_size_bytes"]):
        raise ValueError("raw H2 replay size mismatch")
    if args.c2_raw.stat().st_size != int(c2_spec["combined_json_size_bytes"]):
        raise ValueError("raw C2 combined size mismatch")

    h2_result = json.loads(args.h2_result.read_text(encoding="utf-8"))
    c2_result = json.loads(args.c2_result.read_text(encoding="utf-8"))
    validate_retained_results(h2_result, c2_result, config)

    raw_h2 = json.loads(args.h2_raw.read_text(encoding="utf-8"))
    raw_c2 = json.loads(args.c2_raw.read_text(encoding="utf-8"))
    result = build_post_c2_characterization(raw_h2, raw_c2, config)
    result["provenance"] = {
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "h2_result_path": str(args.h2_result),
        "h2_result_git_blob_sha": h2_spec["result_git_blob_sha"],
        "h2_artifact_id": int(h2_spec["artifact_id"]),
        "h2_raw_sha256": sha256(args.h2_raw),
        "c2_result_path": str(args.c2_result),
        "c2_result_git_blob_sha": c2_spec["result_git_blob_sha"],
        "c2_artifact_id": int(c2_spec["artifact_id"]),
        "c2_raw_sha256": sha256(args.c2_raw),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
