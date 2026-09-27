from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_projection_bound_sensitivity_summary_non_authoritative_2026-09-27.json"
)


def load() -> dict:
    return json.loads(SUMMARY.read_text(encoding="utf-8"))


def test_retained_bound_sensitivity_result_is_complete_and_non_authoritative() -> None:
    result = load()
    assert result["authoritative"] is False
    assert result["execution"]["case_count"] == 12
    assert result["execution"]["bound_set_count"] == 4
    assert result["execution"]["case_bound_projection_count"] == 48
    assert result["execution"]["optimizer_start_count"] == 384
    assert result["execution"]["optimizer_start_success_count"] == 384
    assert result["execution"]["optimizer_start_failure_count"] == 0


def test_bound_activity_resolves_by_wide_8x() -> None:
    result = load()
    assert result["bound_activity"] == {
        "CURRENT_1X": 9,
        "WIDE_2X": 9,
        "WIDE_4X": 1,
        "WIDE_8X": 0,
    }
    assert result["stability"]["wide_8x_boundary_active_case_count"] == 0
    assert (
        result["stability"]["wide_4x_to_8x_max_abs_rms_change"]
        < 2e-6
    )


def test_current_bounded_distance_is_materially_bound_dependent() -> None:
    result = load()
    dependence = result["bound_dependence"]
    assert dependence["materially_present"] is True
    assert (
        dependence["max_current_1x_to_wide_8x_relative_reduction"]
        > 0.66
    )
    affected = next(
        row
        for row in dependence["case_distances"]
        if row["anchor"] == "CBD_ANCHOR_2"
        and row["sign"] == 1
        and row["nominal"] == 0.5
    )
    assert affected["current_1x"] > 0.49
    assert affected["wide_8x"] < 0.17


def test_sign_asymmetry_remains_after_bound_expansion() -> None:
    result = load()
    assert result["sign_geometry"][
        "asymmetry_remains_after_bound_expansion"
    ] is True

    medium_large = [
        row
        for row in result["sign_geometry"]["wide_8x_comparisons"]
        if row["distance"] in {0.25, 0.5}
    ]
    assert len(medium_large) == 4
    for row in medium_large:
        assert row["probability_rms_plus_over_minus"] < 0.70
        assert row["mean_kl_plus_over_minus"] < 0.50
        assert row["information_plus_over_minus"] < 0.71


def test_result_routes_to_distance_definition_review_not_paired_bootstrap() -> None:
    result = load()
    interpretation = result["interpretation"]
    assert interpretation[
        "projection_bounds_materially_affect_current_distance_definition"
    ] is True
    assert interpretation[
        "intrinsic_logistic_manifold_sign_asymmetry_also_remains"
    ] is True
    assert interpretation["paired_bootstrap_allowed_next"] is False
    assert interpretation["next_gate"] == (
        "SCIENTIFIC_NEAREST_CBD_DISTANCE_DEFINITION_REVIEW_BEFORE_PAIRED_BOOTSTRAP"
    )

    boundary = result["interpretation_boundary"]
    assert "do not change the operational fitter" in boundary
    assert "do not authorize paired bootstrap" in boundary
    assert "human N" in boundary
    assert "recruitment" in boundary
    assert "runtime F1b" in boundary


def test_execution_provenance_is_cryptographically_retained() -> None:
    result = load()
    execution = result["execution"]
    assert execution["github_run_id"] == "36321330611"
    assert execution["artifact_id"] == 10932059775
    assert execution["artifact_zip_sha256"] == (
        "63f1c4f1c170ed85a90e48e8ead56a4ec24079a4219d8c3faa3004ef3a7c47f0"
    )
    assert execution["exact_json_sha256"] == (
        "ea8584a1edb3a80ed8751aa1dd6ea504817204cd4d11ebc34a9f42f6d327b55a"
    )
