from __future__ import annotations

import hashlib
import json
from math import comb
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_transmission_recovery_contract.json"
SCHEMA = ROOT / "schemas" / "f1a_transmission_recovery_contract.schema.json"
CONFIG = ROOT / "model" / "benchmarks" / "f1a_transmission_recovery_core.json"
RESULT = ROOT / "model" / "benchmarks" / "results" / "f1a_transmission_recovery_authoritative_2026-09-21.json"
PROMOTION = ROOT / "model" / "experiments" / "f1a_recovery_promotion_2026-09-21.json"
PROMOTION_SCHEMA = ROOT / "schemas" / "f1a_recovery_promotion.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def exact_recovery_probability(n: int, q: float, tolerance: float) -> float:
    return sum(
        comb(n, k) * q**k * (1.0 - q) ** (n - k)
        for k in range(n + 1)
        if abs(k / n - q) <= tolerance + 1e-12
    )


def test_f1a_recovery_contract_matches_strict_schema() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_f1a_recovery_design_is_prospective_and_non_empirical() -> None:
    contract = load(CONTRACT)
    config = load(CONFIG)

    assert contract["status"] == "PROSPECTIVE_SYNTHETIC_RECOVERY_DESIGN"
    assert contract["baseline"]["current_f1a_stage"] == "SYNTHETIC_EXECUTABLE"
    assert contract["estimand"]["empirical_interpretation_allowed"] is False
    assert contract["estimand"]["jointly_estimates_share_propensity"] is False
    assert contract["promotion_gate"]["automatic_promotion_allowed"] is False
    assert contract["promotion_gate"]["candidate_stage_after_authoritative_pass"] == "RECOVERY_TESTED"

    assert config["status"] == "PROSPECTIVE_SYNTHETIC_RECOVERY_DESIGN"
    assert config["generator"]["empirical_parameter"] is False
    assert config["recovery_gate"]["stress_cells_are_gating"] is False


def test_exact_binomial_pre_run_coverage_matches_frozen_design() -> None:
    config = load(CONFIG)
    q_grid = config["generator"]["grid"]
    tolerance = config["estimator"]["absolute_error_tolerance"]
    frozen = config["prospective_exact_binomial_coverage"]["minimum_over_q_grid"]

    for n_text, expected in frozen.items():
        n = int(n_text)
        minimum = min(
            exact_recovery_probability(n, float(q), tolerance)
            for q in q_grid
        )
        assert minimum == pytest.approx(float(expected), abs=5e-7)


def test_core_counts_are_feasible_but_stress_count_is_deliberately_non_gating() -> None:
    config = load(CONFIG)
    q_grid = config["generator"]["grid"]
    tolerance = config["estimator"]["absolute_error_tolerance"]
    gate = config["recovery_gate"]["minimum_recovery_probability_each_core_cell"]

    for n in config["observation_design"]["core_opportunity_counts"]:
        assert min(
            exact_recovery_probability(int(n), float(q), tolerance)
            for q in q_grid
        ) > gate

    assert min(
        exact_recovery_probability(25, float(q), tolerance)
        for q in q_grid
    ) < gate


def test_recovery_design_preserves_observability_and_delay_boundaries() -> None:
    contract = load(CONTRACT)
    text = " ".join(contract["observability_boundary"]).lower()
    interpretation = " ".join(contract["interpretation_boundary"]).lower()

    assert "share-edge opportunities" in text
    assert "may not be identifiable" in text
    assert "population" in interpretation
    assert "platform" in interpretation
    assert "formal system dynamics" in interpretation


def test_recovery_document_matches_frozen_boundary() -> None:
    text = (ROOT / "docs" / "F1A_RECOVERY_DESIGN.md").read_text(encoding="utf-8")
    for token in (
        "PROSPECTIVE_SYNTHETIC_RECOVERY_DESIGN",
        "q_hat = realised endogenous exposures / realised Share-edge opportunities",
        "N=25",
        "stress only",
        "RECOVERY_TESTED",
        "EMPIRICALLY_CONSTRAINED",
    ):
        assert token in text


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_authoritative_f1a_recovery_result_preserves_frozen_provenance() -> None:
    result = load(RESULT)
    assert result["status"] == "AUTHORITATIVE_SYNTHETIC_RECOVERY_RESULT"
    assert result["authoritative"] is True
    assert result["replicates_per_grid_cell"] == 200
    assert result["provenance"]["replicate_override"] is None
    assert result["provenance"]["config_sha256"] == sha256(CONFIG)
    assert result["provenance"]["contract_sha256"] == sha256(CONTRACT)
    assert result["provenance"]["source_commit"] == "8cea4e0b51b5413f2f3c76cafacde7f05fc842f9"


def test_authoritative_f1a_recovery_result_meets_only_declared_core_gate() -> None:
    result = load(RESULT)
    assert result["minimum_core_grid_recovery_probability"] == pytest.approx(0.885)
    assert result["all_core_grid_cells_pass"] is True
    assert result["controls"]["all_controls_pass"] is True
    assert result["structural_checks"]["all_structural_checks_pass"] is True
    assert result["sensitivity_checks"]["all_monotonic"] is True
    assert result["promotion_candidate"] is True

    core = result["core_grid_results"]
    stress = result["stress_grid_results"]
    assert len(core) == 20
    assert len(stress) == 10
    assert all(row["passes_recovery_gate"] is True for row in core)
    assert all(row["passes_recovery_gate"] is None for row in stress)
    assert any(row["recovery_probability"] < 0.80 for row in stress)


def test_authoritative_f1a_recovery_result_reports_expected_limitations() -> None:
    result = load(RESULT)
    boundary = result["interpretation_boundary"].lower()
    assert "best-case synthetic recovery benchmark only" in boundary
    assert "does not establish an empirical transmission mechanism" in boundary
    assert "active status" in boundary

    for row in result["core_grid_results"] + result["stress_grid_results"]:
        assert row["maximum_delay_realization_error"] == 0.0
        assert row["maximum_familiarity_consistency_error"] == 0.0


def test_f1a_recovery_promotion_record_matches_strict_schema_and_result() -> None:
    promotion = load(PROMOTION)
    schema = load(PROMOTION_SCHEMA)
    result = load(RESULT)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(promotion)

    assert promotion["decision"] == "PROMOTE_TO_RECOVERY_TESTED"
    assert promotion["new_stage"] == "RECOVERY_TESTED"
    assert promotion["authoritative_result"]["minimum_core_recovery_probability"] == result["minimum_core_grid_recovery_probability"]
    assert promotion["authoritative_result"]["all_core_cells_pass"] is result["all_core_grid_cells_pass"]
    assert promotion["authoritative_result"]["promotion_candidate"] is result["promotion_candidate"]
    assert promotion["ci_evidence"]["result_reproduced_exactly"] is True
    assert promotion["next_gate"] == {
        "candidate_stage": "EMPIRICALLY_CONSTRAINED",
        "automatic_promotion_allowed": False,
        "empirical_evidence_bridge_required": True,
        "measurement_observability_contract_required": True,
        "active_runtime_registration_allowed": False,
    }
