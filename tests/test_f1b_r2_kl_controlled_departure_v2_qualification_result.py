from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_kl_controlled_departure_v2_qualification_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_v2_deterministic_qualification_passes_complete_grid() -> None:
    result = load()
    assert result["status"] == (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_QUALIFIED"
    )
    assert result["authoritative"] is False
    assert result["issue"] == 202

    design = result["design"]
    assert design["design_id"] == "F1B.R2.KL_CONTROLLED_DEPARTURE.V2"
    assert design["target_mean_bernoulli_kl"] == [0.001, 0.002, 0.003]
    assert design["case_count"] == 36
    assert design["execution_partition_count"] == 6

    qualification = result["qualification"]
    assert qualification["gate_pass"] is True
    assert qualification["all_36_cases_generated"] is True
    assert qualification["scientific_domain_unresolved_count"] == 0
    assert qualification["finite_interior_count"] == 33
    assert qualification["closure_limit_count"] == 3
    assert qualification["max_target_error"] <= 1e-7
    assert qualification["all_standalone_add_compatible"] is True
    assert qualification["standalone_max_add_rms"] <= 1e-10


def test_v2_closure_limit_cases_are_explicit_and_only_complement_minus() -> None:
    result = load()
    rows = result["closure_limit_cases"]
    assert len(rows) == 3
    assert {
        (
            row["anchor_id"],
            row["sign"],
            row["target_mean_kl"],
            tuple(row["closure_boundary_components"]),
        )
        for row in rows
    } == {
        ("CBD_ANCHOR_1", -1, 0.003, ("W1=HIGH",)),
        ("CBD_ANCHOR_2", -1, 0.002, ("W1=HIGH",)),
        ("CBD_ANCHOR_2", -1, 0.003, ("W1=HIGH",)),
    }
    assert all(
        row["axis"] == "COMPLEMENT_RELATION_VIOLATION"
        for row in rows
    )


def test_v2_upper_complement_plus_saturation_is_retained_not_hidden() -> None:
    rows = load()["saturation_context"]
    assert len(rows) == 2

    a2 = next(
        row
        for row in rows
        if row["anchor_id"] == "CBD_ANCHOR_2"
    )
    assert a2["axis"] == "COMPLEMENT_RELATION_VIOLATION"
    assert a2["sign"] == 1
    assert a2["target_mean_kl"] == 0.003
    assert a2["generator_outside_005_095_count"] == 6
    assert a2["generator_outside_010_090_count"] == 6
    assert a2["min_probability_general"] < 0.01
    assert a2["max_probability_general"] > 0.99


def test_cross_version_0_001_check_preserves_available_v1_cases() -> None:
    check = load()["cross_version_0_001"]
    assert check["exact_v1_case_count_available"] == 8
    assert check["attainment_status_changes"] == 0
    assert check["closure_identity_changes"] == 0
    assert check["complement_v1_exact_partition_available"] is False
    assert check["max_abs_scalar_delta"] < 1e-10
    assert check["max_general_coefficient_abs_delta"] < 1e-10
    assert check["max_cbd_surface_coordinate_abs_delta"] < 1e-6


def test_v2_result_retains_exact_execution_hashes() -> None:
    execution = load()["execution"]
    assert execution["scientific_source_commit"] == (
        "63c1784332eb2de22da5d4d1bf47af5f8f2133f8"
    )
    assert execution["temporary_pr"] == 204
    assert execution["github_run_id"] == "36336694463"
    assert execution["combined_artifact_id"] == 10937835482
    assert execution["combined_artifact_zip_sha256"] == (
        "87c56a14a045e798d2964471f64d8c59b9ca45b905df484427995a118ef76da8"
    )
    assert execution["exact_combined_json_sha256"] == (
        "cc0b95f4bba63dc721a864b4dbe53be9c0c8a07071991575ea2a438d410d4ef7"
    )
    assert execution["exact_combined_json_size_bytes"] == 33934395


def test_v2_qualification_authorizes_only_next_design_search_gate() -> None:
    result = load()
    assert result["next_gate"] == (
        "PAIRED_SAME_DATASET_BOOTSTRAP_CHARACTERIZATION_DESIGN"
    )
    boundary = result["interpretation_boundary"]
    assert "does not validate detection power" in boundary
    assert "human N" in boundary
    assert "authorize recruitment" in boundary
    assert "runtime F1b" in boundary
