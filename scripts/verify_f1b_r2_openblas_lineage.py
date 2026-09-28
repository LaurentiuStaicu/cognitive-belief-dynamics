from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from cognitive_epistemic_model.calibration.f1b_r2_openblas_lineage import (
    parse_openblas_verbose_cores,
    validate_candidate_environment,
    validate_qualification_config,
    validate_runtime_cores,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def verify_git_blob(path: Path, expected: str, label: str) -> None:
    actual = git_blob_sha(path)
    if actual != str(expected):
        raise ValueError(
            f"{label} Git blob mismatch: {actual} != {expected}"
        )


def runtime_probe() -> dict:
    probe = r"""
import json
import platform
import sys

import numpy as np
import scipy
import scipy.linalg

a = np.arange(4096, dtype=np.float64).reshape(64, 64) / 4096.0
_ = a @ a.T
_ = scipy.linalg.lu_factor(a + np.eye(64))

print(
    "CBD_OPENBLAS_RUNTIME_IDENTITY="
    + json.dumps(
        {
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        sort_keys=True,
    )
)
"""
    environment = os.environ.copy()
    environment["OPENBLAS_VERBOSE"] = "2"
    completed = subprocess.run(
        [sys.executable, "-c", probe],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    combined = completed.stdout + "\n" + completed.stderr
    cores = parse_openblas_verbose_cores(combined)
    validate_runtime_cores(cores)

    marker = "CBD_OPENBLAS_RUNTIME_IDENTITY="
    identity_line = next(
        (
            line
            for line in completed.stdout.splitlines()
            if line.startswith(marker)
        ),
        None,
    )
    if identity_line is None:
        raise RuntimeError("runtime identity marker missing from OpenBLAS probe")
    identity = json.loads(identity_line[len(marker) :])
    return {
        "reported_cores": list(cores),
        "identity": identity,
        "probe_stdout": completed.stdout,
        "probe_stderr": completed.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the prospective F1b R2 OpenBLAS execution lineage "
            "without running a scientific fit or generating bootstrap draws."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_openblas_execution_lineage_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_qualification_config(config)
    validate_candidate_environment()

    verify_git_blob(
        Path(config["frozen_dependency_lock"]["path"]),
        config["frozen_dependency_lock"]["git_blob_sha"],
        "frozen dependency lock",
    )
    for path_text, expected in config[
        "protected_scientific_file_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)

    retained = config["retained_c1_v1"]
    retained_path = Path(retained["path"])
    actual_retained_sha = sha256(retained_path)
    if actual_retained_sha != retained["sha256"]:
        raise ValueError(
            "retained C1 V1 result SHA-256 mismatch: "
            f"{actual_retained_sha} != {retained['sha256']}"
        )

    probe = runtime_probe()
    result = {
        "qualification_id": config["qualification_id"],
        "status": "NON_AUTHORITATIVE_OPENBLAS_Q0_ENVIRONMENT_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "candidate_environment": {
            "OPENBLAS_CORETYPE": os.environ.get("OPENBLAS_CORETYPE"),
            "OPENBLAS_VERBOSE_for_probe": "2",
        },
        "runtime_probe": probe,
        "provenance": {
            "config_sha256": sha256(args.config),
            "dependency_lock_git_blob_sha": config[
                "frozen_dependency_lock"
            ]["git_blob_sha"],
            "protected_scientific_file_git_blob_sha": config[
                "protected_scientific_file_git_blob_sha"
            ],
            "retained_c1_v1_sha256": actual_retained_sha,
        },
        "boundary": {
            "scientific_fit_executed": False,
            "bootstrap_draw_generated": False,
            "stage_c2_authorized": False,
            "failed_c1_v1_rewritten": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
