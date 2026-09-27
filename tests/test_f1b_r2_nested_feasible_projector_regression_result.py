from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_nested_feasible_projector_regression_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_corrected_projector_regression_passes_without_rewriting_history() -> None:
    result = load()
    assert result["historical_result_immutable"] is True
    assert result["authoritative"] is False
    summary = result["summary"]
    assert summary["gate_pass"] is True
    assert summary["candidate_surface_rows"] == 36
    assert summary["attainment_status_changes"] == 0
    assert summary["closure_boundary_identity_changes"] == 0
    assert summary["scientific_domain_identity_changes"] == 0
    assert summary["historical_unresolved_count"] == 0
    assert summary["corrected_unresolved_count"] == 0


def test_attainment_counts_and_closure_identities_are_preserved() -> None:
    result = load()
    for row in result["attainment_counts"]:
        assert row["finite_interior_historical"] == 7
        assert row["finite_interior_corrected"] == 7
        assert row["closure_limit_historical"] == 5
        assert row["closure_limit_corrected"] == 5

    closure = result["closure_case_identities"]
    assert closure["all_three_candidates_same"] is True
    assert len(closure["cases"]) == 5
    assert {
        row["boundary"] for row in closure["cases"]
    } == {"W0=HIGH", "W1=HIGH"}


def test_numerical_correction_never_worsens_retained_objectives() -> None:
    summary = load()["summary"]
    assert summary["max_positive_closure_objective_delta"] == 0.0
    assert summary["max_positive_finite_logit_objective_delta"] == 0.0
    assert summary["historical_closure_failed_optimizer_starts"] == 0
    assert summary["corrected_closure_failed_optimizer_starts"] == 0
    assert summary["historical_finite_logit_failed_optimizer_starts"] == 0
    assert summary["corrected_finite_logit_failed_optimizer_starts"] == 0


def test_all_36_candidate_surface_rows_are_accounted_for() -> None:
    result = load()
    changed = result["changed_candidate_surface_rows"]
    unchanged = result["unchanged_candidate_surface_rows"]
    assert len(changed) == 2
    assert len(unchanged) == 34
    assert len(changed) + len(unchanged) == 36

    assert max(
        row["closure_surface_probability_rms_old_vs_corrected"]
        for row in changed
    ) == result["summary"][
        "max_closure_surface_probability_rms_old_vs_corrected"
    ]
    assert max(
        row["finite_logit_surface_probability_rms_old_vs_corrected"]
        for row in changed
    ) == result["summary"][
        "max_finite_logit_surface_probability_rms_old_vs_corrected"
    ]


def test_regression_authorizes_only_resuming_deterministic_envelope_gate() -> None:
    result = load()
    boundary = result["boundary"]
    assert "Historical #171 remains immutable" in boundary
    assert "prospective numerical infrastructure only" in boundary
    assert "does not authorize stochastic characterization" in boundary
    assert "paired bootstrap" in boundary
