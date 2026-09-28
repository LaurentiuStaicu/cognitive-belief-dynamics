from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from cognitive_epistemic_model.calibration import (
    f1b_r2_paired_bootstrap_characterization as paired_characterization,
)
from cognitive_epistemic_model.calibration.f1b_r2_c1_numerical_diagnostic import (
    environment_identity,
    select_diagnostic_sentinels,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
    regenerate_bootstrap_attempt_statistics,
    regenerate_dataset_for_run,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)


PAIRED_SHA256 = "b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    sentinel = sys.argv[1]
    paired_source_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    replica = int(sys.argv[4])

    if sha256(paired_source_path) != PAIRED_SHA256:
        raise ValueError("paired source SHA-256 mismatch")

    paired_source = json.loads(
        paired_source_path.read_text(encoding="utf-8")
    )
    c1_result = json.loads(
        Path(
            "model/results/f1b_r2_continuation_c1_failed_2026-09-27.json"
        ).read_text(encoding="utf-8")
    )
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
    scales = paired_characterization._scales(
        paired_config,
        generator=False,
    )
    regenerated_observed, regenerated_attempts = (
        regenerate_bootstrap_attempt_statistics(
            run,
            dataset,
            paired_config=paired_config,
            draw_indices=range(199),
        )
    )
    retained_attempts = tuple(run["bootstrap_attempt_statistics"])
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
    retained_hash = canonical_attempt_sequence_sha256(retained_attempts)
    regenerated_hash = canonical_attempt_sequence_sha256(
        regenerated_attempts
    )
    retained_observed = float(run["observed_statistic"])
    result = {
        "diagnostic_id": "F1B.R2.C1.CROSS_RUNNER_SENTINEL.V1",
        "authoritative": False,
        "sentinel": sentinel,
        "replica": replica,
        "run_id": run_id,
        "execution_path": "UNINSTRUMENTED_STAGE_C1_REGENERATION_FUNCTION",
        "retained_observed_statistic": retained_observed,
        "regenerated_observed_statistic": float(regenerated_observed),
        "observed_statistic_absolute_delta": abs(
            float(regenerated_observed) - retained_observed
        ),
        "observed_statistic_exact_match": (
            float(regenerated_observed) == retained_observed
        ),
        "retained_attempt_sequence_sha256": retained_hash,
        "regenerated_attempt_sequence_sha256": regenerated_hash,
        "attempt_sequence_sha256_match": (
            regenerated_hash == retained_hash
        ),
        "first_divergent_draw_index": first_divergent_draw,
        "environment": environment_identity(),
        "boundary": {
            "stage_c1_gate_changed": False,
            "stage_c2_authorized": False,
            "new_draw_index_ge_199_generated": False,
            "scientific_fit_settings_changed": False,
        },
    }
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "CROSS_RUNNER_SENTINEL="
        + json.dumps(
            {
                "sentinel": sentinel,
                "replica": replica,
                "cpu_model": result["environment"]["cpu_model"],
                "observed_exact": result[
                    "observed_statistic_exact_match"
                ],
                "observed_delta": result[
                    "observed_statistic_absolute_delta"
                ],
                "attempt_hash_match": result[
                    "attempt_sequence_sha256_match"
                ],
                "first_divergent_draw": first_divergent_draw,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
