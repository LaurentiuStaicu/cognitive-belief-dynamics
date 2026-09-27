from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_nested_feasible_projection_regression_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_nested_feasible_projection_regression_passes_without_rewriting_history() -> None:
    result = load()
    assert result["status"] == "NUMERICAL_INTEGRITY_REGRESSION_PASS"
    assert result["authoritative"] is False
    assert result["issue"] == 190
    assert result["acceptance"]["pass"] is True
    assert result["acceptance"]["historical_result_rewritten"] is False
    assert result["acceptance"]["corrected_projector_prospective_use_allowed"] is True
    assert result["acceptance"]["next_gate"] == (
        "RESUME_ISSUE_182_COMPLEMENT_KL_ENVELOPE"
    )


def test_regression_preserves_all_attainment_and_closure_identities() -> None:
    result = load()
    classification = result["classification_regression"]
    assert classification["case_count"] == 12
    assert classification["candidate_count"] == 3
    assert classification["case_candidate_count"] == 36
    assert classification["attainment_status_changes"] == 0
    assert classification["closure_boundary_identity_changes"] == 0
    assert classification["scientific_domain_identity_changes"] == 0
    assert classification["historical_closure_case_count"] == 15
    assert classification["corrected_closure_case_count"] == 15
    assert classification["unresolved_case_count_historical"] == 0
    assert classification["unresolved_case_count_corrected"] == 0

    counts = {
        (row["candidate_id"], row["status"]): row["count"]
        for row in classification["attainment_counts"]
    }
    for candidate in (
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    ):
        assert counts[(candidate, "FINITE_INTERIOR_ATTAINED")] == 7
        assert counts[(candidate, "NON_ATTAINED_OR_CLOSURE_LIMIT")] == 5


def test_corrected_domain_objectives_never_worsen_historical_selection() -> None:
    result = load()
    domain = result["domain_level_regression"]
    assert domain["finite_domain_comparisons"] == 108
    assert domain["closure_domain_comparisons"] == 108
    assert domain["changed_domain_selections"] == 3

    for projection in ("finite", "closure"):
        block = domain[projection]
        assert block["objective_worsening_count"] == 0
        assert block["max_new_minus_old_objective"] <= 0.0
        assert block["historical_failed_optimizer_start_count"] == 0
        assert block["corrected_failed_optimizer_start_count"] == 0
        assert block["continuation_enabled_domain_count"] == 72
        assert block["exact_carry_forward_selected_count"] == 1
        assert block["max_corrected_raw_apparent_nested_increase"] <= 0.0


def test_response_changes_remain_inside_retained_historical_numerical_scale() -> None:
    scale = load()["retained_response_scale_check"]
    assert (
        scale["max_corrected_vs_historical_finite_probability_rms"]
        < scale["historical_same_candidate_max_closure_vs_finite_probability_rms"]
    )
    assert (
        scale["max_corrected_vs_historical_closure_probability_rms"]
        < scale["historical_same_candidate_max_closure_vs_finite_probability_rms"]
    )
    assert scale["finite_change_fraction_of_retained_same_candidate_scale"] < 1.0
    assert scale["closure_change_fraction_of_retained_same_candidate_scale"] < 1.0


def test_regression_retains_exact_historical_and_corrected_artifact_hashes() -> None:
    result = load()
    historical = result["historical_baseline"]
    corrected = result["corrected_execution"]

    assert historical["scientific_source_commit"] == (
        "97a4ac6119709de8089032a21b97877a522dd04d"
    )
    assert historical["github_run_id"] == "36325580317"
    assert historical["artifact_id"] == 10933539813
    assert historical["exact_json_sha256"] == (
        "55597e0f240b439531b872e99dfec9bafee73323e3c39d18943529069907537e"
    )

    assert corrected["scientific_source_commit"] == (
        "d25909a22f3adde313f59d372b58c139ce15ad1f"
    )
    assert corrected["github_run_id"] == "36333833072"
    assert corrected["artifact_id"] == 10937041228
    assert corrected["exact_json_sha256"] == (
        "039e06da85a137f92d72b01defceb863605ed371597ed9f04a5240aebcfd2939"
    )

    assert result["input_identity"]["all_non_source_input_hashes_match_historical"] is True
