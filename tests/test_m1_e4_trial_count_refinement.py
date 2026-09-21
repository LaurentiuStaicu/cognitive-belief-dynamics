from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "model/benchmarks/m1_e4_candidate_recovery_core.json"
REFINEMENT = ROOT / "model/benchmarks/m1_e4_candidate_recovery_trial_count_refinement.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def test_trial_count_refinement_changes_only_declared_design_axis():
    core = load(CORE)
    refinement = load(REFINEMENT)

    assert refinement["trial_counts_per_operating_point"] == [480, 640, 960]
    assert core["trial_counts_per_operating_point"] == [40, 80, 160, 320]

    for key in (
        "seed",
        "replicates",
        "recovery_threshold",
        "bias_grids",
        "memory_grids",
        "selection_rule",
    ):
        assert refinement[key] == core[key], key

    control = refinement["controlled_change"]
    assert control["changed_axis_only"] == "trial_counts_per_operating_point"
    assert set(control["unchanged_axes"]) == {
        "seed",
        "replicates",
        "recovery_threshold",
        "bias_grids",
        "memory_grids",
        "selection_rule",
    }


def test_refinement_keeps_five_operating_points_and_full_memory_grid():
    refinement = load(REFINEMENT)

    assert len(refinement["bias_grids"]["EVSD"]) == 5
    assert len(refinement["bias_grids"]["2HT"]) == 5
    assert {row["label"] for row in refinement["memory_grids"]["EVSD"]} == {
        "weak",
        "medium",
        "strong",
    }
    assert {row["label"] for row in refinement["memory_grids"]["2HT"]} == {
        "weak",
        "medium",
        "strong",
    }


def test_refinement_remains_non_empirical_and_non_runtime():
    refinement = load(REFINEMENT)

    assert refinement["status"] == "TARGETED_TRIAL_COUNT_REFINEMENT"
    assert refinement["replicates"] == 200
    assert refinement["recovery_threshold"] == 0.8
    assert "does not calibrate M1.E4" in refinement["interpretation_boundary"]
    assert "identify Pencode" in refinement["interpretation_boundary"]
