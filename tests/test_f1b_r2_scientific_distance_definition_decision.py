from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_scientific_distance_definition_decision.json"
)


def load() -> dict:
    return json.loads(DECISION.read_text(encoding="utf-8"))


def test_future_scientific_departure_definition_is_directed_bernoulli_kl() -> None:
    decision = load()
    selected = decision["selected_candidate"]
    assert decision["authoritative_for_future_distance_definition"] is True
    assert selected["candidate_id"] == "BERNOULLI_KL_GENERAL_TO_CBD"
    assert selected["direction"] == "GENERAL_TO_CBD"
    assert selected["primary_quantity"] == "MEAN_BERNOULLI_KL"
    assert selected["sqrt_2_mean_kl_status"] == "SCALE_DIAGNOSTIC_ONLY"
    assert selected["scientific_restricted_set"] == (
        "CLOSURE_OF_CBD_RESPONSE_FAMILY_ON_THE_EXPLICIT_DESIGN_MEASURE"
    )


def test_metric_decision_does_not_rewrite_historical_characterization() -> None:
    historical = load()["historical_results_rule"]
    assert historical["rewrite_historical_158"] is False
    assert historical["reinterpret_historical_158_under_new_distance"] is False
    assert historical["historical_utility_rms_definition_preserved"] is True
    assert historical["new_distance_requires_new_versioned_departure_design"] is True


def test_closure_attainment_remains_explicit() -> None:
    decision = load()
    closure = decision["closure_review"]
    assert closure["candidates_each_finite_interior_attained"] == 7
    assert closure["candidates_each_closure_limit"] == 5
    assert closure["candidates_each_scientific_domain_unresolved"] == 0
    assert closure["same_closure_cases_across_all_candidates"] is True
    assert (
        closure["maximum_probability_rms_closure_vs_finite_less_than"]
        == 0.0001
    )
    assert decision["selected_candidate"][
        "finite_parameter_attainment_must_be_reported"
    ] is True


def test_d1_d2_remain_diagnostics_not_invalidated() -> None:
    statuses = {
        row["candidate_id"]: row["status"]
        for row in load()["nonselected_primary_candidates"]
    }
    assert statuses == {
        "STABILIZED_UTILITY_RMS": (
            "RETAINED_DIAGNOSTIC_NOT_PRIMARY_FUTURE_DEPARTURE_STRENGTH"
        ),
        "PROBABILITY_RMS": (
            "RETAINED_DIAGNOSTIC_NOT_PRIMARY_FUTURE_DEPARTURE_STRENGTH"
        ),
    }


def test_decision_authorizes_only_next_deterministic_design_gate() -> None:
    decision = load()
    next_gate = decision["next_gate"]
    assert next_gate["name"] == "VERSIONED_KL_CONTROLLED_DEPARTURE_DESIGN"
    assert next_gate["deterministic_first"] is True
    assert next_gate["must_freeze_target_strength_grid_before_stochastic_results"] is True
    assert next_gate["preserve_both_signs"] is True
    assert next_gate["preserve_multiple_anchors"] is True
    assert next_gate["paired_bootstrap_authorized"] is False

    boundary = decision["execution_boundary"]
    assert boundary == {
        "operational_fitter_bounds_changed": False,
        "paired_bootstrap_authorized": False,
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_power_validated": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }
