from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization import (
    dataset_fingerprint,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    bootstrap_seed_for,
    dataset_id_for,
    select_scientific_specs,
    simulate_paired_missingness_datasets,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_m2_prefix_bridge import (
    build_prefix_bridge_manifest,
    validate_prefix_bridge_config,
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


def verify_source(path: Path, spec: dict, label: str) -> None:
    actual_sha = sha256(path)
    if actual_sha != str(spec["json_sha256"]):
        raise ValueError(
            f"{label} SHA-256 mismatch: {actual_sha} != {spec['json_sha256']}"
        )
    if "json_size_bytes" in spec:
        actual_size = path.stat().st_size
        if actual_size != int(spec["json_size_bytes"]):
            raise ValueError(
                f"{label} size mismatch: {actual_size} != "
                f"{spec['json_size_bytes']}"
            )


def verify_protected_files(config: dict) -> None:
    for raw_path, expected in config[
        "protected_file_git_blob_sha"
    ].items():
        path = Path(raw_path)
        actual = git_blob_sha(path)
        if actual != str(expected):
            raise ValueError(
                f"protected prefix-bridge file changed: "
                f"{raw_path}: {actual} != {expected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-source", type=Path, required=True)
    parser.add_argument("--m1-source", type=Path, required=True)
    parser.add_argument("--m2-source", type=Path, required=True)
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_s4_m2_prefix_bridge_v1.json"
        ),
    )
    parser.add_argument(
        "--m1-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_paired_method_m1_screen_v1.json"
        ),
    )
    parser.add_argument(
        "--paired-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
        ),
    )
    parser.add_argument(
        "--v2-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_kl_controlled_departure_design_v2.json"
        ),
    )
    parser.add_argument(
        "--review-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_distance_definition_review.json"
        ),
    )
    parser.add_argument(
        "--historical-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load(args.config)
    validate_prefix_bridge_config(config)
    verify_protected_files(config)

    verify_source(args.h1_source, config["h1_source"], "H1 source")
    verify_source(args.m1_source, config["m1_source"], "M1 source")
    verify_source(args.m2_source, config["m2_source"], "M2 source")
    verify_source(
        args.s4_manifest,
        config["s4_matrix_source"],
        "S4 manifest",
    )

    h1_source = load(args.h1_source)
    m1_source = load(args.m1_source)
    m2_source = load(args.m2_source)
    s4_manifest = load(args.s4_manifest)
    m1_config = load(args.m1_config)
    paired_config = load(args.paired_config)
    v2_config = load(args.v2_config)
    review_config = load(args.review_config)
    historical_config = load(args.historical_config)

    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_config,
    )
    specs = select_scientific_specs(h1_source, m1_config)

    regenerated_dataset_sha256: dict[str, str] = {}
    expected_bootstrap_seed: dict[str, int] = {}

    for spec in specs:
        for replicate in range(spec.replicate_count):
            dataset_id = dataset_id_for(spec, replicate)
            datasets = simulate_paired_missingness_datasets(
                spec,
                replicate,
                paired_config=paired_config,
                departure_cases=departure_cases,
            )
            seed = bootstrap_seed_for(
                spec,
                replicate,
                paired_config=paired_config,
            )
            for missingness, dataset in zip(
                (0.0, 0.15),
                datasets,
                strict=True,
            ):
                scientific_run_id = (
                    f"{dataset_id}|RESTRICTION={spec.restriction}"
                    f"|MISSINGNESS={missingness:.2f}"
                )
                if scientific_run_id in regenerated_dataset_sha256:
                    raise ValueError(
                        "duplicate deterministic prefix scientific run"
                    )
                regenerated_dataset_sha256[scientific_run_id] = (
                    dataset_fingerprint(dataset)
                )
                expected_bootstrap_seed[scientific_run_id] = int(seed)

    if len(regenerated_dataset_sha256) != 840:
        raise ValueError(
            "deterministic prefix regeneration did not produce 840 runs"
        )

    result = build_prefix_bridge_manifest(
        m1_source=m1_source,
        m2_source=m2_source,
        s4_manifest=s4_manifest,
        config=config,
        regenerated_dataset_sha256=regenerated_dataset_sha256,
        expected_bootstrap_seed=expected_bootstrap_seed,
    )
    result["provenance"] = {
        "config_sha256": sha256(args.config),
        "h1_source_sha256": sha256(args.h1_source),
        "m1_source_sha256": sha256(args.m1_source),
        "m2_source_sha256": sha256(args.m2_source),
        "s4_manifest_sha256": sha256(args.s4_manifest),
        "h1_artifact_id": int(config["h1_source"]["artifact_id"]),
        "m1_artifact_id": int(config["m1_source"]["artifact_id"]),
        "m2_artifact_id": int(config["m2_source"]["artifact_id"]),
        "s4_matrix_artifact_id": int(
            config["s4_matrix_source"]["artifact_id"]
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
