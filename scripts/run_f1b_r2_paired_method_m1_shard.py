from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from cognitive_epistemic_model.calibration import (
    f1b_r2_paired_bootstrap_characterization as paired,
)
from cognitive_epistemic_model.calibration.f1b_r2_kl_controlled_departures import (
    generate_kl_controlled_departure_design,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization import (
    dataset_fingerprint,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    EXPECTED_METHODS,
    bootstrap_seed_for,
    canonical_json_sha256,
    dataset_id_for,
    run_method_prefix,
    select_scientific_specs,
    simulate_paired_missingness_datasets,
    validate_m1_config,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)


def stable_shard(value: str, count: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % int(count)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_paired_method_m1_screen_v1.json"
        ),
    )
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid M1 shard index")

    config = load(args.config)
    validate_m1_config(config)
    expected_sha = str(config["source"]["json_sha256"])
    actual_sha = hashlib.sha256(args.source.read_bytes()).hexdigest()
    if actual_sha != expected_sha:
        raise ValueError("M1 H1 source SHA-256 mismatch")

    source = load(args.source)
    paired_config = load(
        Path(
            "model/benchmarks/"
            "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
        )
    )
    v2_config = load(
        Path("model/benchmarks/f1b_r2_kl_controlled_departure_design_v2.json")
    )
    review_config = load(
        Path("model/benchmarks/f1b_r2_distance_definition_review.json")
    )
    historical_config = load(
        Path("model/benchmarks/f1b_r2_controlled_departure_design.json")
    )
    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_config,
    )
    specs = select_scientific_specs(source, config)

    source_runs = {
        (
            str(row["identity"]),
            str(row["restriction"]),
            int(row["evaluation_replicate"]),
        ): row
        for row in source["restriction_runs"]
    }
    if len(source_runs) != 750:
        raise ValueError("M1 H1 source run keys are not unique")

    rows: list[dict] = []
    selected_scientific_runs = 0
    started_all = time.perf_counter()

    for spec in specs:
        for replicate in range(spec.replicate_count):
            dataset_id = dataset_id_for(spec, replicate)
            for missingness, dataset in zip(
                (0.0, 0.15),
                simulate_paired_missingness_datasets(
                    spec,
                    replicate,
                    paired_config=paired_config,
                    departure_cases=departure_cases,
                ),
                strict=True,
            ):
                scientific_run_id = (
                    f"{dataset_id}|RESTRICTION={spec.restriction}"
                    f"|MISSINGNESS={missingness:.2f}"
                )
                if stable_shard(
                    scientific_run_id,
                    args.shard_count,
                ) != args.shard_index:
                    continue

                selected_scientific_runs += 1
                fingerprint = dataset_fingerprint(dataset)
                source_key = (spec.identity, spec.restriction, replicate)
                retained_source = source_runs.get(source_key)
                h1_dataset_exact = None
                if missingness == 0.0 and retained_source is not None:
                    h1_dataset_exact = (
                        fingerprint == str(retained_source["dataset_sha256"])
                    )
                    if not h1_dataset_exact:
                        raise ValueError(
                            f"M1 retained H1 dataset mismatch: {scientific_run_id}"
                        )

                base_seed = bootstrap_seed_for(
                    spec,
                    replicate,
                    paired_config=paired_config,
                )
                if retained_source is not None and base_seed != int(
                    retained_source["bootstrap_stream_seed"]
                ):
                    raise ValueError("M1 H1 bootstrap base seed changed")

                for method_id in EXPECTED_METHODS:
                    started = time.perf_counter()
                    result = run_method_prefix(
                        dataset,
                        spec=spec,
                        replicate=replicate,
                        method_id=method_id,
                        paired_config=paired_config,
                        config=config,
                    )
                    elapsed = time.perf_counter() - started
                    attempt_sha = (
                        None
                        if not result["bootstrap_attempt_statistics"]
                        else canonical_attempt_sequence_sha256(
                            result["bootstrap_attempt_statistics"]
                        )
                    )
                    h1_prefix_exact = None
                    if (
                        method_id == "HIERARCHICAL_1X"
                        and missingness == 0.0
                        and retained_source is not None
                    ):
                        retained_attempts = tuple(
                            retained_source["bootstrap_attempt_statistics"][:199]
                        )
                        if len(retained_attempts) != 199:
                            raise ValueError("M1 retained H1 prefix changed")
                        retained_sha = canonical_attempt_sequence_sha256(
                            retained_attempts
                        )
                        h1_prefix_exact = attempt_sha == retained_sha
                        if not h1_prefix_exact:
                            raise ValueError(
                                "M1 HIERARCHICAL_1X retained H1 prefix mismatch"
                            )

                    rows.append(
                        {
                            "scientific_run_id": scientific_run_id,
                            "dataset_id": dataset_id,
                            "dataset_sha256": fingerprint,
                            "identity": spec.identity,
                            "identity_type": spec.identity_type,
                            "restriction": spec.restriction,
                            "role": spec.role,
                            "anchor_id": spec.anchor_id,
                            "axis": spec.axis,
                            "sign": spec.sign,
                            "target_mean_bernoulli_kl": (
                                spec.target_mean_bernoulli_kl
                            ),
                            "evaluation_replicate": int(replicate),
                            "missingness_rate": float(missingness),
                            "inference_method": method_id,
                            "bootstrap_base_seed": int(base_seed),
                            "h1_dataset_exact": h1_dataset_exact,
                            "h1_prefix_exact": h1_prefix_exact,
                            "bootstrap_attempt_sequence_sha256": attempt_sha,
                            "elapsed_seconds": elapsed,
                            **{
                                key: value
                                for key, value in result.items()
                                if key != "bootstrap_attempt_statistics"
                            },
                        }
                    )

    result = {
        "design_id": config["design_id"],
        "status": "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SHARD_RESULT",
        "authoritative": False,
        "issue": int(config["issue"]),
        "source_json_sha256": actual_sha,
        "shard_index": int(args.shard_index),
        "shard_count": int(args.shard_count),
        "selected_scientific_run_count": selected_scientific_runs,
        "method_row_count": len(rows),
        "row_identity_sha256": canonical_json_sha256(
            [
                [
                    row["scientific_run_id"],
                    row["inference_method"],
                ]
                for row in sorted(
                    rows,
                    key=lambda row: (
                        row["scientific_run_id"],
                        row["inference_method"],
                    ),
                )
            ]
        ),
        "elapsed_seconds": time.perf_counter() - started_all,
        "rows": rows,
        "boundary": dict(config["boundary"]),
    }
    if len(rows) != 4 * selected_scientific_runs:
        raise ValueError("M1 shard pairing count changed")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
