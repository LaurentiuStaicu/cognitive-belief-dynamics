from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_terminal_partition import (
    aggregate_terminal_partition,
    compose_terminal_partition,
    validate_terminal_partition_config,
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


def verify_git_blob(path: Path, expected: str, label: str) -> None:
    actual = git_blob_sha(path)
    if actual != str(expected):
        raise ValueError(f"{label} Git blob mismatch: {actual} != {expected}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compose the non-authoritative homogeneous F1b R2 terminal "
            "resampling-risk partition from retained H2 and C2 artifacts."
        )
    )
    parser.add_argument("--h2-raw", type=Path, required=True)
    parser.add_argument("--c2-raw", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_homogeneous_terminal_partition_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_terminal_partition_config(config)

    h2_spec = config["h2_stage_b"]
    c2_spec = config["c2_continuation"]

    verify_git_blob(
        Path(h2_spec["retained_result_path"]),
        h2_spec["retained_result_git_blob_sha"],
        "retained H2 result",
    )
    verify_git_blob(
        Path(c2_spec["retained_result_path"]),
        c2_spec["retained_result_git_blob_sha"],
        "retained C2 result",
    )
    for path_text, expected in config[
        "protected_role_definition_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)
    for path_text, expected in config[
        "protected_controller_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)

    verify_sha256(args.h2_raw, h2_spec["raw_json_sha256"], "H2 raw replay")
    if args.h2_raw.stat().st_size != int(h2_spec["raw_json_size_bytes"]):
        raise ValueError("H2 raw replay byte size changed")

    verify_sha256(args.c2_raw, c2_spec["raw_json_sha256"], "C2 combined result")
    if args.c2_raw.stat().st_size != int(c2_spec["raw_json_size_bytes"]):
        raise ValueError("C2 combined result byte size changed")

    h2_raw = json.loads(args.h2_raw.read_text(encoding="utf-8"))
    c2_raw = json.loads(args.c2_raw.read_text(encoding="utf-8"))

    terminal = compose_terminal_partition(h2_raw, c2_raw, config)
    terminal["characterization"] = aggregate_terminal_partition(
        terminal,
        config,
    )
    terminal["provenance"] = {
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "h2_raw_artifact_id": int(h2_spec["artifact_id"]),
        "h2_raw_sha256": sha256(args.h2_raw),
        "c2_raw_artifact_id": int(c2_spec["artifact_id"]),
        "c2_raw_sha256": sha256(args.c2_raw),
        "retained_h2_result_git_blob_sha": h2_spec[
            "retained_result_git_blob_sha"
        ],
        "retained_c2_result_git_blob_sha": c2_spec[
            "retained_result_git_blob_sha"
        ],
        "protected_role_definition_git_blob_sha": config[
            "protected_role_definition_git_blob_sha"
        ],
        "protected_controller_git_blob_sha": config[
            "protected_controller_git_blob_sha"
        ],
        "execution_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
        ).strip(),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(terminal, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
