from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_kl_complement_envelope_result_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_corrected_complement_envelope_has_complete_coverage() -> None:
    result = load()
    assert result["status"] == "NON_AUTHORITATIVE_KL_COMPLEMENT_ENVELOPE_RESULT"
    assert result["authoritative"] is False
    assert result["issue"] == 182
    assert result["design"]["ray_count"] == 4
    assert result["design"]["points_per_ray"] == 801
    assert result["design"]["total_points"] == 3204
    assert result["design"]["unresolved_point_count"] == 0
    assert len(result["rays"]) == 4


def test_both_minus_rays_reach_all_frozen_v1_targets() -> None:
    result = load()
    minus = [row for row in result["rays"] if row["sign"] == -1]
    assert len(minus) == 2

    for ray in minus:
        assert {
            row["target"]: row["classification"]
            for row in ray["target_results"]
        } == {
            0.001: "TARGET_ATTAINABLE_WITHIN_V1_RANGE",
            0.005: "TARGET_ATTAINABLE_WITHIN_V1_RANGE",
            0.01: "TARGET_ATTAINABLE_WITHIN_V1_RANGE",
        }
        assert ray["first_closure_scalar"] is not None

    assert result["diagnostic_conclusion"][
        "minus_initial_v1_failure_was_numerical"
    ] is True
    assert result["diagnostic_conclusion"][
        "both_minus_rays_reach_all_frozen_v1_targets"
    ] is True


def test_both_plus_rays_reach_only_the_low_frozen_target() -> None:
    result = load()
    plus = [row for row in result["rays"] if row["sign"] == 1]
    assert len(plus) == 2

    for ray in plus:
        statuses = {
            row["target"]: row["classification"]
            for row in ray["target_results"]
        }
        assert statuses[0.001] == "TARGET_ATTAINABLE_WITHIN_V1_RANGE"
        assert statuses[0.005] == "TARGET_ABOVE_RAY_ENVELOPE_WITHIN_V1_RANGE"
        assert statuses[0.01] == "TARGET_ABOVE_RAY_ENVELOPE_WITHIN_V1_RANGE"
        assert ray["first_closure_scalar"] is None
        assert ray["attainment_counts"] == {"FINITE_INTERIOR_ATTAINED": 801}

    conclusion = result["diagnostic_conclusion"]
    assert conclusion["both_plus_rays_reach_0_001"] is True
    assert conclusion["both_plus_rays_reach_0_005"] is False
    assert conclusion["both_plus_rays_reach_0_010"] is False
    assert conclusion["common_frozen_targets_attainable_on_all_four_rays"] == [
        0.001
    ]


def test_binding_plus_envelope_is_below_0_005() -> None:
    result = load()
    plus_maxima = [
        row["maximum_mean_kl"]
        for row in result["rays"]
        if row["sign"] == 1
    ]
    minimum = min(plus_maxima)
    assert minimum == result["diagnostic_conclusion"][
        "minimum_plus_ray_envelope_maximum"
    ]
    assert minimum == 0.0032538188153675754
    assert minimum < 0.005


def test_v1_grid_is_not_revised_by_envelope_result() -> None:
    result = load()
    conclusion = result["diagnostic_conclusion"]
    assert conclusion[
        "v1_common_target_grid_attainable_on_all_preserved_complement_rays"
    ] is False
    assert conclusion["target_grid_revision_authorized_here"] is False
    assert conclusion["next_gate"] == (
        "PROSPECTIVE_COMMON_KL_TARGET_GRID_REDESIGN_FROM_DETERMINISTIC_GEOMETRY_ONLY"
    )
    boundary = result["interpretation_boundary"]
    assert "target grid" in boundary
    assert "not revised" in boundary
    assert "No stochastic characterization" in boundary


def test_envelope_retains_exact_execution_provenance() -> None:
    result = load()
    execution = result["execution"]
    assert execution["scientific_source_commit"] == (
        "54b6e6d0307ee91960dd80fec0d3f008a3a3d806"
    )
    assert execution["github_run_id"] == "36335130114"
    assert execution["combined_artifact_id"] == 10936214205
    assert execution["combined_artifact_zip_sha256"] == (
        "407fb0e37f302eec97076737243097882cfad92c8dc290054e2119d93bda17ec"
    )
    assert execution["exact_combined_json_sha256"] == (
        "6885f32de25bc6838380d6acc9d7c7f2cda02736104dca4717fe8da7b1c733c6"
    )
    assert execution["exact_combined_json_size_bytes"] == 3267049

    ray_hashes = result["provenance"]["ray_json_sha256"]
    assert set(ray_hashes) == {
        "CBD_ANCHOR_1|-1",
        "CBD_ANCHOR_1|1",
        "CBD_ANCHOR_2|-1",
        "CBD_ANCHOR_2|1",
    }
