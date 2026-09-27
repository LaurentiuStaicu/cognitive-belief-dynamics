from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_controlled_departures import (
    generate_controlled_departure_design,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_broad_departure_characterization_49x20.json"
)
DEPARTURES = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_broad_characterization_freezes_only_non_authoritative_stage() -> None:
    config = load(CONFIG)
    assert config["seed"] == 2026092702
    assert config["bootstrap"]["draw_grid"] == [49]
    assert config["evaluation_replicate_grid"] == [20]
    assert config["expected_departure_case_count"] == 36
    assert config["expected_restriction_tests"] == 1500
    assert config["departure_case_filter"] is None

    boundary = config["execution_boundary"]
    assert boundary == {
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_run_allowed": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_broad_characterization_covers_complete_declared_departure_grid() -> None:
    generated = generate_controlled_departure_design(load(DEPARTURES))
    cases = generated["cases"]
    assert len(cases) == 36

    counts = Counter(case["axis"] for case in cases)
    assert counts == {
        "STANDALONE_ACCURACY_MAIN_EFFECT": 12,
        "COMPLEMENT_RELATION_VIOLATION": 12,
        "COMBINED_VIOLATION": 12,
    }

    standalone = [
        case
        for case in cases
        if case["axis"] == "STANDALONE_ACCURACY_MAIN_EFFECT"
    ]
    assert all(case["add_compatibility_expected"] for case in standalone)

    expected_distances = {0.1, 0.25, 0.5}
    for axis in counts:
        axis_cases = [case for case in cases if case["axis"] == axis]
        assert {case["sign"] for case in axis_cases} == {-1, 1}
        assert {
            case["requested_cbd_rms_distance"] for case in axis_cases
        } == expected_distances


def test_replicate_partition_plan_is_complete_and_non_overlapping() -> None:
    config = load(CONFIG)
    plan = config["execution_partition_plan"]
    assert plan["partition_axis"] == "evaluation_replicate"
    assert plan["scientific_total_evaluation_replicates"] == 20
    assert plan["forbid_departure_filter_sharding"] is True

    seen: set[int] = set()
    for shard in plan["shards"]:
        indices = shard["replicate_indices"]
        assert indices == sorted(set(indices))
        assert not seen.intersection(indices)
        seen.update(indices)

    assert seen == set(range(20))


def test_declared_workload_matches_full_grid() -> None:
    config = load(CONFIG)
    departures = config["expected_departure_case_count"]
    replicates = config["evaluation_replicate_grid"][0]
    restriction_identities_per_replicate = 3 + 2 * departures
    assert restriction_identities_per_replicate == 75
    assert restriction_identities_per_replicate * replicates == 1500
