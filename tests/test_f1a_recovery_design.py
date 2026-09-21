from __future__ import annotations

import json
from math import comb
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_transmission_recovery_contract.json"
SCHEMA = ROOT / "schemas" / "f1a_transmission_recovery_contract.schema.json"
CONFIG = ROOT / "model" / "benchmarks" / "f1a_transmission_recovery_core.json"


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
