from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_distance_definition_closure_review_non_authoritative_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_retained_distance_closure_result_is_non_authoritative() -> None:
    result = load()
    assert result["authoritative"] is False
    assert result["status"] == (
        "NON_AUTHORITATIVE_R2_DISTANCE_DEFINITION_CLOSURE_REVIEW_RESULT"
    )
    assert result["decision_boundary"] == {
        "metric_selected": False,
        "paired_bootstrap_authorized": False,
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_all_three_candidates_have_same_attainment_structure() -> None:
    counts = {
        (row["candidate_id"], row["status"]): row["count"]
        for row in load()["candidate_attainment_counts"]
    }
    candidates = {
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    }
    for candidate in candidates:
        assert counts[(candidate, "FINITE_INTERIOR_ATTAINED")] == 7
        assert counts[(candidate, "NON_ATTAINED_OR_CLOSURE_LIMIT")] == 5
        assert (
            counts.get((candidate, "SCIENTIFIC_DOMAIN_UNRESOLVED"), 0)
            == 0
        )


def test_same_five_surfaces_hit_closure_for_every_candidate() -> None:
    rows = load()["closure_cases"]
    assert len(rows) == 15
    by_candidate: dict[str, set[str]] = {}
    for row in rows:
        assert row["status"] == "NON_ATTAINED_OR_CLOSURE_LIMIT"
        assert row["closure_boundary_components"]
        assert row["scientific_domain_components"] == []
        by_candidate.setdefault(row["candidate_id"], set()).add(
            row["case_id"]
        )

    expected = {
        "CBD_ANCHOR_1__COMPLEMENT_RELATION_VIOLATION__MINUS__RMS_0.25",
        "CBD_ANCHOR_1__COMPLEMENT_RELATION_VIOLATION__MINUS__RMS_0.50",
        "CBD_ANCHOR_2__COMPLEMENT_RELATION_VIOLATION__MINUS__RMS_0.10",
        "CBD_ANCHOR_2__COMPLEMENT_RELATION_VIOLATION__MINUS__RMS_0.25",
        "CBD_ANCHOR_2__COMPLEMENT_RELATION_VIOLATION__MINUS__RMS_0.50",
    }
    assert len(by_candidate) == 3
    for cases in by_candidate.values():
        assert cases == expected


def test_closure_and_finite_logit_selected_surfaces_are_numerically_close() -> None:
    comparison = load()["numerical_comparison"]
    assert comparison["closure_failed_starts"] == {
        "BERNOULLI_KL_GENERAL_TO_CBD": 0,
        "PROBABILITY_RMS": 0,
        "STABILIZED_UTILITY_RMS": 0,
    }
    for value in comparison[
        "max_probability_rms_closure_vs_finite"
    ].values():
        assert value < 1e-4


def test_execution_provenance_is_exact() -> None:
    result = load()
    execution = result["execution"]
    assert result["scientific_source_commit"] == (
        "97a4ac6119709de8089032a21b97877a522dd04d"
    )
    assert execution["temporary_pr"] == 175
    assert execution["github_run_id"] == "36325580317"
    assert execution["artifact_id"] == 10933539813
    assert execution["artifact_zip_sha256"] == (
        "7c947134279e816357bcc8b6d7966c44fc29e49bb536d974827628068e769f48"
    )
    assert execution["exact_json_sha256"] == (
        "55597e0f240b439531b872e99dfec9bafee73323e3c39d18943529069907537e"
    )
