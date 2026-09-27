from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_kl_controlled_departures import (
    generate_kl_controlled_departure_design,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_bootstrap_characterization import (
    run_paired_bootstrap_characterization,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def parse_replicate_indices(value: str | None) -> tuple[int, ...] | None:
    if value is None:
        return None
    indices: list[int] = []
    for token in value.split(","):
        token = token.strip()
        if not token:
            raise ValueError("empty replicate-index token")
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if end < start:
                raise ValueError("replicate range must be increasing")
            indices.extend(range(start, end + 1))
        else:
            indices.append(int(token))
    normalized = tuple(indices)
    if tuple(sorted(set(normalized))) != normalized:
        raise ValueError(
            "replicate indices must be unique and strictly increasing"
        )
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run non-authoritative paired same-dataset bootstrap draw "
            "stability characterization for F1b R2 KL v2."
        )
    )
    parser.add_argument(
        "--config",
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
        "--v2-qualification-result",
        type=Path,
        default=Path(
            "model/results/"
            "f1b_r2_kl_controlled_departure_v2_qualification_2026-09-27.json"
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
        "--historical-departure-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_controlled_departure_design.json"
        ),
    )
    parser.add_argument("--replicate-indices", default=None)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default=None)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    v2_config = json.loads(args.v2_config.read_text(encoding="utf-8"))
    qualification = json.loads(
        args.v2_qualification_result.read_text(encoding="utf-8")
    )
    review_config = json.loads(
        args.review_config.read_text(encoding="utf-8")
    )
    historical_config = json.loads(
        args.historical_departure_config.read_text(encoding="utf-8")
    )

    v2_config_sha256 = sha256(args.v2_config)
    if qualification["status"] != (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_QUALIFIED"
    ):
        raise ValueError("paired characterization requires retained V2 qualification")
    if qualification["authoritative"] is not False:
        raise ValueError("V2 qualification boundary changed")
    if not bool(qualification["qualification"]["gate_pass"]):
        raise ValueError("paired characterization requires V2 qualification PASS")
    if qualification["design"]["design_id"] != "F1B.R2.KL_CONTROLLED_DEPARTURE.V2":
        raise ValueError("V2 qualification design identity mismatch")
    if int(qualification["design"]["case_count"]) != 36:
        raise ValueError("V2 qualification must retain all 36 cases")
    if qualification["design"]["target_mean_bernoulli_kl"] != [0.001, 0.002, 0.003]:
        raise ValueError("V2 qualification target grid mismatch")
    if qualification["execution"]["config_sha256"] != v2_config_sha256:
        raise ValueError(
            "current V2 config hash does not match retained qualification"
        )

    generated = generate_kl_controlled_departure_design(
        v2_config,
        review_config,
        historical_config,
    )
    if generated["design_id"] != "F1B.R2.KL_CONTROLLED_DEPARTURE.V2":
        raise ValueError("paired characterization requires KL v2 design")
    if generated["case_count"] != 36:
        raise ValueError("paired characterization requires all 36 V2 cases")

    result = run_paired_bootstrap_characterization(
        config,
        generated["cases"],
        replicate_indices=parse_replicate_indices(args.replicate_indices),
    )
    result["provenance"] = {
        "source_commit": args.source_commit or git_head(),
        "config_path": str(args.config),
        "config_sha256": sha256(args.config),
        "v2_config_path": str(args.v2_config),
        "v2_config_sha256": v2_config_sha256,
        "v2_qualification_result_path": str(args.v2_qualification_result),
        "v2_qualification_result_sha256": sha256(
            args.v2_qualification_result
        ),
        "review_config_path": str(args.review_config),
        "review_config_sha256": sha256(args.review_config),
        "historical_departure_config_path": str(
            args.historical_departure_config
        ),
        "historical_departure_config_sha256": sha256(
            args.historical_departure_config
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
