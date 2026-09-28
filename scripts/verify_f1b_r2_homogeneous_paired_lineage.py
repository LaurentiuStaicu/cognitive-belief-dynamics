from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_paired_lineage import (
    validate_h1_environment,
    validate_h1_runtime_cores,
    validate_homogeneous_paired_config,
)
from cognitive_epistemic_model.calibration.f1b_r2_openblas_lineage import (
    parse_openblas_verbose_cores,
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


def verify_sha256(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != str(expected):
        raise ValueError(
            f"{label} SHA-256 mismatch: {actual} != {expected}"
        )


def runtime_probe() -> dict:
    probe = r"""
import json
import os
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
import scipy.linalg

cpu_model = None
cpuinfo = Path("/proc/cpuinfo")
if cpuinfo.exists():
    for line in cpuinfo.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines():
        if line.lower().startswith("model name"):
            cpu_model = line.partition(":")[2].strip()
            break

a = np.arange(4096, dtype=np.float64).reshape(64, 64) / 4096.0
_ = a @ a.T
_ = scipy.linalg.lu_factor(a + np.eye(64))

print(
    "CBD_HOMOGENEOUS_PAIRED_RUNTIME_IDENTITY="
    + json.dumps(
        {
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_model": cpu_model,
            "OPENBLAS_CORETYPE": os.environ.get("OPENBLAS_CORETYPE"),
            "OPENBLAS_NUM_THREADS": os.environ.get(
                "OPENBLAS_NUM_THREADS"
            ),
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
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
    validate_h1_runtime_cores(cores)

    marker = "CBD_HOMOGENEOUS_PAIRED_RUNTIME_IDENTITY="
    identity_line = next(
        (
            line
            for line in completed.stdout.splitlines()
            if line.startswith(marker)
        ),
        None,
    )
    if identity_line is None:
        raise RuntimeError(
            "homogeneous paired runtime identity marker missing"
        )
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
            "Verify the H0 prospective homogeneous F1b R2 paired-source "
            "execution lineage without running a scientific fit or "
            "generating bootstrap draws."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_homogeneous_paired_source_lineage_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validate_homogeneous_paired_config(config)
    validate_h1_environment()

    verify_git_blob(
        Path(config["frozen_dependency_lock"]["path"]),
        config["frozen_dependency_lock"]["git_blob_sha"],
        "frozen dependency lock",
    )
    for path_text, expected in config[
        "protected_scientific_file_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)
    for path_text, expected in config[
        "protected_execution_file_git_blob_sha"
    ].items():
        verify_git_blob(Path(path_text), expected, path_text)

    input_hashes = {}
    for label, spec in config["frozen_inputs"].items():
        path = Path(spec["path"])
        verify_sha256(path, spec["sha256"], label)
        input_hashes[label] = spec["sha256"]

    probe = runtime_probe()
    result = {
        "lineage_id": config["lineage_id"],
        "status": "NON_AUTHORITATIVE_HOMOGENEOUS_PAIRED_H0_RESULT",
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
            "protected_execution_file_git_blob_sha": config[
                "protected_execution_file_git_blob_sha"
            ],
            "frozen_input_sha256": input_hashes,
            "historical_paired_source": config[
                "historical_paired_source"
            ],
        },
        "boundary": {
            "scientific_fit_executed": False,
            "bootstrap_draw_generated": False,
            "scientific_dataset_identity_changed": False,
            "seed_identity_changed": False,
            "historical_source_rewritten": False,
            "stage_c2_authorized": False,
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
