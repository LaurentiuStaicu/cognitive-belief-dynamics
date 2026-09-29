from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import hashlib
import json
import os
from pathlib import Path
import statistics
import time

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    simulate_paired_missingness_datasets,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    build_m2_boundaries,
    validate_m2_environment,
)
from cognitive_epistemic_model.calibration.f1b_r2_resampling_risk_continuation import (
    build_departure_case_map,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_executor import (
    run_new_stream,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_scientific_matrix import (
    select_s4_scientific_specs,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_fresh_replicate_preflight import (
    EXPECTED_METHODS,
    EXPECTED_METHOD_DIGEST,
    EXPECTED_RUN_DIGEST,
    EXPECTED_TERMINAL_STATES,
    canonical_json_sha256,
    method_row_id,
    validate_preflight_config,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-source", type=Path, required=True)
    parser.add_argument("--s4-manifest", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument(
        "--preflight-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_s4_fresh_replicate_preflight_v1.json"
        ),
    )
    parser.add_argument(
        "--equivalence-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_s4_new_executor_equivalence_v1.json"
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
        "--m2-config",
        type=Path,
        default=Path(
            "model/benchmarks/"
            "f1b_r2_paired_method_m2_sequential_resolution_v1.json"
        ),
    )
    parser.add_argument(
        "--s4-config",
        type=Path,
        default=Path(
            "model/benchmarks/f1b_r2_s4_broad_scientific_matrix_v1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    preflight_config = load(args.preflight_config)
    validate_preflight_config(preflight_config)
    validate_m2_environment(os.environ)

    equivalence_config = load(args.equivalence_config)
    expected_h1 = str(
        equivalence_config["retained_sources"]["h1"]["json_sha256"]
    )
    if sha256(args.h1_source) != expected_h1:
        raise ValueError("S4 fresh preflight H1 source SHA-256 mismatch")

    expected_s4 = str(
        preflight_config["retained_sources"]["s4_matrix"][
            "manifest_json_sha256"
        ]
    )
    if sha256(args.s4_manifest) != expected_s4:
        raise ValueError("S4 fresh preflight manifest SHA-256 mismatch")

    selection = load(args.selection)
    if selection["status"] != (
        "NON_AUTHORITATIVE_S4_FRESH_REPLICATE_PREFLIGHT_SELECTION_COMPLETE"
    ):
        raise ValueError("S4 fresh preflight selection status changed")
    if selection["execution_authorized"] is not True:
        raise ValueError("S4 fresh preflight selection not authorized")
    if selection["executor_equivalence_retained_and_verified"] is not True:
        raise ValueError("S4 fresh preflight equivalence not verified")
    if int(selection["scientific_run_count"]) != 18:
        raise ValueError("S4 fresh preflight selection run count changed")
    if int(selection["method_row_count"]) != 72:
        raise ValueError("S4 fresh preflight selection method count changed")
    if selection["scientific_run_ids_sha256"] != EXPECTED_RUN_DIGEST:
        raise ValueError("S4 fresh preflight selection run digest changed")
    if selection["method_row_ids_sha256"] != EXPECTED_METHOD_DIGEST:
        raise ValueError("S4 fresh preflight selection method digest changed")
    if tuple(selection["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("S4 fresh preflight selected method set changed")

    h1_source = load(args.h1_source)
    s4_manifest = load(args.s4_manifest)
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("S4 fresh preflight manifest run count changed")
    s4_rows = {
        str(row["scientific_run_id"]): row
        for row in s4_manifest["rows"]
    }
    if len(s4_rows) != 15000:
        raise ValueError("S4 fresh preflight manifest identities changed")

    selected_rows = list(selection["rows"])
    selected_ids = [str(row["scientific_run_id"]) for row in selected_rows]
    if canonical_json_sha256(selected_ids) != EXPECTED_RUN_DIGEST:
        raise ValueError("S4 fresh preflight selected row order changed")
    for row in selected_rows:
        run_id = str(row["scientific_run_id"])
        if run_id not in s4_rows:
            raise ValueError("S4 fresh preflight selected run missing")
        if row != s4_rows[run_id]:
            raise ValueError("S4 fresh preflight selected row content changed")

    m1_config = load(args.m1_config)
    m2_config = load(args.m2_config)
    s4_config = load(args.s4_config)
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

    specs = select_s4_scientific_specs(
        h1_source,
        m1_config,
        s4_config,
    )
    spec_map = {
        (str(spec.identity), str(spec.restriction)): spec
        for spec in specs
    }
    if len(spec_map) != 75:
        raise ValueError("S4 fresh preflight scientific specs not unique")

    dataset_cache = {}
    spec_cache = {}
    for scientific_row in selected_rows:
        run_id = str(scientific_row["scientific_run_id"])
        key = (
            str(scientific_row["identity"]),
            str(scientific_row["restriction"]),
        )
        if key not in spec_map:
            raise ValueError("S4 fresh preflight scientific spec missing")
        spec = spec_map[key]
        replicate = int(scientific_row["evaluation_replicate"])
        datasets = simulate_paired_missingness_datasets(
            spec,
            replicate,
            paired_config=paired_config,
            departure_cases=departure_cases,
        )
        missingness = float(scientific_row["missingness"])
        if missingness == 0.0:
            dataset = datasets[0]
        elif missingness == 0.15:
            dataset = datasets[1]
        else:
            raise ValueError("S4 fresh preflight missingness changed")
        dataset_cache[run_id] = dataset
        spec_cache[run_id] = spec

    boundaries = build_m2_boundaries(m2_config)
    rows = []
    elapsed_by_method = Counter()
    started = time.perf_counter()
    for scientific_row in selected_rows:
        run_id = str(scientific_row["scientific_run_id"])
        for method_id in EXPECTED_METHODS:
            method_started = time.perf_counter()
            row = run_new_stream(
                scientific_row,
                spec=spec_cache[run_id],
                replicate=int(scientific_row["evaluation_replicate"]),
                dataset=dataset_cache[run_id],
                method_id=method_id,
                paired_config=paired_config,
                m1_config=m1_config,
                m2_config=m2_config,
                boundaries=boundaries,
            )
            row["elapsed_seconds"] = time.perf_counter() - method_started
            elapsed_by_method[method_id] += row["elapsed_seconds"]
            rows.append(row)
    elapsed = time.perf_counter() - started

    if len(rows) != 72:
        raise ValueError("S4 fresh preflight did not execute 72 method rows")

    row_ids = [
        method_row_id(
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        )
        for row in rows
    ]
    if len(set(row_ids)) != 72:
        raise ValueError("S4 fresh preflight method row IDs not unique")
    if canonical_json_sha256(row_ids) != EXPECTED_METHOD_DIGEST:
        raise ValueError("S4 fresh preflight executed method digest changed")

    grouped = defaultdict(list)
    for row in rows:
        grouped[str(row["scientific_run_id"])].append(row)
    if set(grouped) != set(selected_ids):
        raise ValueError("S4 fresh preflight executed run coverage changed")

    for run_id, group in grouped.items():
        if {str(row["inference_method"]) for row in group} != set(
            EXPECTED_METHODS
        ):
            raise ValueError(
                f"S4 fresh preflight method coverage changed: {run_id}"
            )
        if len({str(row["dataset_sha256"]) for row in group}) != 1:
            raise ValueError(
                f"S4 fresh preflight dataset pairing changed: {run_id}"
            )
        if len({int(row["bootstrap_base_seed"]) for row in group}) != 1:
            raise ValueError(
                f"S4 fresh preflight base seed pairing changed: {run_id}"
            )

    status_counts = Counter(str(row["status"]) for row in rows)
    if not set(status_counts).issubset(set(EXPECTED_TERMINAL_STATES)):
        raise ValueError("S4 fresh preflight terminal state changed")

    terminal_ns = [int(row["terminal_n"]) for row in rows]
    if any(value < 0 or value > 10000 for value in terminal_ns):
        raise ValueError("S4 fresh preflight terminal n outside contract")

    decision_counts = Counter(
        "NONE" if row["decision"] is None else str(row["decision"])
        for row in rows
    )
    method_summaries = {}
    for method_id in EXPECTED_METHODS:
        subset = [row for row in rows if row["inference_method"] == method_id]
        method_summaries[method_id] = {
            "row_count": len(subset),
            "elapsed_seconds": float(elapsed_by_method[method_id]),
            "status_counts": dict(
                Counter(str(row["status"]) for row in subset)
            ),
            "decision_counts": dict(
                Counter(
                    "NONE" if row["decision"] is None else str(row["decision"])
                    for row in subset
                )
            ),
        }

    result = {
        "preflight_id": preflight_config["preflight_id"],
        "status": "NON_AUTHORITATIVE_S4_FRESH_REPLICATE_PREFLIGHT_COMPLETE",
        "authoritative": False,
        "issue": int(preflight_config["issue"]),
        "scientific_run_count": 18,
        "method_row_count": 72,
        "scientific_run_ids_sha256": EXPECTED_RUN_DIGEST,
        "method_row_ids_sha256": EXPECTED_METHOD_DIGEST,
        "eligible_methods": list(EXPECTED_METHODS),
        "elapsed_seconds": elapsed,
        "status_counts": dict(status_counts),
        "decision_counts": dict(decision_counts),
        "terminal_n_summary": {
            "minimum": min(terminal_ns),
            "median": statistics.median(terminal_ns),
            "maximum": max(terminal_ns),
        },
        "method_summaries": method_summaries,
        "rows": rows,
        "structural_preflight_pass": True,
        "scientific_outcome_is_not_acceptance_criterion": True,
        "w0_authorized_after_retention": True,
        "broad_execution_started": False,
        "scientific_interpretation_authorized": False,
        "release_0_2_0_blocker_closed": False,
        "provenance": {
            "preflight_config_sha256": sha256(args.preflight_config),
            "equivalence_config_sha256": sha256(args.equivalence_config),
            "h1_source_sha256": sha256(args.h1_source),
            "s4_manifest_sha256": sha256(args.s4_manifest),
            "selection_sha256": sha256(args.selection),
        },
        "boundary": {
            "broad_execution_started": False,
            "scientific_interpretation_authorized": False,
            "method_selected": False,
            "scale_selected": False,
            "power_validated": False,
            "human_n_frozen": False,
            "participant_recruitment_allowed": False,
            "runtime_f1b_change_allowed": False,
            "version_bumped": False,
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
