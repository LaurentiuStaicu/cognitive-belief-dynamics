from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

from cognitive_epistemic_model.calibration import (
    f1b_r2_paired_bootstrap_characterization as paired_characterization,
)
from cognitive_epistemic_model.calibration.f1b_r2_c1_numerical_diagnostic import (
    environment_identity,
    select_diagnostic_sentinels,
)
from cognitive_epistemic_model.calibration.f1b_r2_openblas_lineage import (
    validate_candidate_environment,
    validate_qualification_config,
    validate_retained_draw_indices,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization import (
    dataset_fingerprint,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
    regenerate_bootstrap_attempt_statistics,
    regenerate_dataset_for_run,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)


PAIRED_SHA256 = (
    "b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    sentinel = sys.argv[1]
    paired_source_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    replica = int(sys.argv[4])

    validate_candidate_environment()
    lineage_config = json.loads(
        Path(
            "model/benchmarks/f1b_r2_openblas_execution_lineage_v1.json"
        ).read_text(encoding="utf-8")
    )
    validate_qualification_config(lineage_config)
    if sentinel not in lineage_config["q1_sentinels"]["labels"]:
        raise ValueError(f"unsupported Q1 sentinel: {sentinel}")

    if sha256(paired_source_path) != PAIRED_SHA256:
        raise ValueError("paired source SHA-256 mismatch")

    c1_result_path = Path(
        "model/results/f1b_r2_continuation_c1_failed_2026-09-27.json"
    )
    if sha256(c1_result_path) != lineage_config["retained_c1_v1"]["sha256"]:
        raise ValueError("retained C1 V1 SHA-256 mismatch")

    paired_source = json.loads(
        paired_source_path.read_text(encoding="utf-8")
    )
    c1_result = json.loads(c1_result_path.read_text(encoding="utf-8"))
    paired_config = json.loads(
        Path(
            "model/benchmarks/"
            "f1b_r2_kl_v2_paired_bootstrap_draw_stability.json"
        ).read_text(encoding="utf-8")
    )
    v2_config = json.loads(
        Path(
            "model/benchmarks/f1b_r2_kl_controlled_departure_design_v2.json"
        ).read_text(encoding="utf-8")
    )
    review_config = json.loads(
        Path(
            "model/benchmarks/f1b_r2_distance_definition_review.json"
        ).read_text(encoding="utf-8")
    )
    historical_config = json.loads(
        Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ).read_text(encoding="utf-8")
    )

    sentinels = select_diagnostic_sentinels(c1_result)
    run_id = sentinels[sentinel]
    source_runs = {
        str(row["run_id"]): row
        for row in paired_source["restriction_runs"]
    }
    if run_id not in source_runs:
        raise ValueError(f"Q1 sentinel missing from paired source: {run_id}")
    run = source_runs[run_id]

    departure_cases = build_departure_case_map(
        v2_config,
        review_config,
        historical_config,
    )
    dataset = regenerate_dataset_for_run(
        run,
        paired_config=paired_config,
        departure_cases=departure_cases,
    )
    regenerated_dataset_sha256 = dataset_fingerprint(dataset)
    retained_dataset_sha256 = str(run["dataset_sha256"])
    dataset_match = regenerated_dataset_sha256 == retained_dataset_sha256

    draw_indices = validate_retained_draw_indices(range(199))
    scales = paired_characterization._scales(
        paired_config,
        generator=False,
    )
    regenerated_observed, regenerated_attempts = (
        regenerate_bootstrap_attempt_statistics(
            run,
            dataset,
            paired_config=paired_config,
            draw_indices=draw_indices,
        )
    )
    retained_observed = float(run["observed_statistic"])
    observed_exact = float(regenerated_observed) == retained_observed

    retained_attempts = tuple(run["bootstrap_attempt_statistics"])
    if len(retained_attempts) != 199 or len(regenerated_attempts) != 199:
        raise ValueError("Q1 sentinel must contain exactly 199 retained attempts")
    retained_hash = canonical_attempt_sequence_sha256(retained_attempts)
    regenerated_hash = canonical_attempt_sequence_sha256(
        regenerated_attempts
    )
    attempt_hash_match = regenerated_hash == retained_hash
    first_divergent_draw = next(
        (
            index
            for index, (retained, regenerated) in enumerate(
                zip(retained_attempts, regenerated_attempts, strict=True)
            )
            if retained != regenerated
        ),
        None,
    )

    qualification_pass = (
        dataset_match and observed_exact and attempt_hash_match
    )
    result = {
        "qualification_id": lineage_config["qualification_id"],
        "status": "NON_AUTHORITATIVE_OPENBLAS_Q1_SENTINEL_RESULT",
        "authoritative": False,
        "issue": 227,
        "sentinel": sentinel,
        "replica": replica,
        "run_id": run_id,
        "candidate_environment": {
            "OPENBLAS_CORETYPE": os.environ.get("OPENBLAS_CORETYPE"),
            "OPENBLAS_VERBOSE": os.environ.get("OPENBLAS_VERBOSE"),
        },
        "dataset": {
            "retained_sha256": retained_dataset_sha256,
            "regenerated_sha256": regenerated_dataset_sha256,
            "exact_match": dataset_match,
        },
        "observed_statistic": {
            "retained": retained_observed,
            "regenerated": float(regenerated_observed),
            "exact_match": observed_exact,
            "absolute_delta": abs(
                float(regenerated_observed) - retained_observed
            ),
        },
        "attempt_sequence": {
            "draw_count": 199,
            "retained_sha256": retained_hash,
            "regenerated_sha256": regenerated_hash,
            "exact_match": attempt_hash_match,
            "first_divergent_draw_index": first_divergent_draw,
        },
        "environment": environment_identity(),
        "qualification_pass": qualification_pass,
        "boundary": {
            "maximum_draw_index": 198,
            "new_draw_index_ge_199_generated": False,
            "failed_c1_v1_rewritten": False,
            "stage_c2_authorized": False,
            "scientific_fit_settings_changed": False,
        },
    }
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "OPENBLAS_Q1_SENTINEL="
        + json.dumps(
            {
                "sentinel": sentinel,
                "replica": replica,
                "cpu_model": result["environment"]["cpu_model"],
                "dataset_match": dataset_match,
                "observed_exact": observed_exact,
                "observed_delta": result["observed_statistic"][
                    "absolute_delta"
                ],
                "attempt_hash_match": attempt_hash_match,
                "first_divergent_draw": first_divergent_draw,
                "qualification_pass": qualification_pass,
            },
            sort_keys=True,
        )
    )
    if not qualification_pass:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
