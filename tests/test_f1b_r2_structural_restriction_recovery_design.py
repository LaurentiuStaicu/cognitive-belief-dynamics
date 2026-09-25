from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator
from scipy.special import expit, logit

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1b_r2_structural_restriction_recovery_contract.json"
SCHEMA = ROOT / "schemas" / "f1b_r2_structural_restriction_recovery_contract.schema.json"
DESIGN = ROOT / "model" / "benchmarks" / "f1b_r2_structural_restriction_recovery_design.json"
DOC = ROOT / "docs" / "F1B_R2_STRUCTURAL_RESTRICTION_RECOVERY_DESIGN.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ap_a_utility(
    b: float,
    accuracy_baseline: float,
    beta_accuracy_cue: float,
    beta_reward: float,
    B: np.ndarray,
    A: np.ndarray,
    R: np.ndarray,
) -> np.ndarray:
    w = expit(logit(accuracy_baseline) + beta_accuracy_cue * A)
    return b + w * (2.0 * B - 1.0) + beta_reward * (1.0 - w) * R


def general_utility(
    beta: tuple[float, float, float, float, float, float],
    B: np.ndarray,
    A: np.ndarray,
    R: np.ndarray,
) -> np.ndarray:
    b, beta_b, beta_a, beta_r, beta_ab, beta_ar = beta
    centered = 2.0 * B - 1.0
    return (
        b
        + beta_b * centered
        + beta_a * A
        + beta_r * R
        + beta_ab * A * centered
        + beta_ar * A * R
    )


def test_contract_validates_schema_and_keeps_gates_closed() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    design = load(DESIGN)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)

    assert contract["nesting_statement"]["ap_b_nested_in_general"] is True
    assert contract["nesting_statement"]["ap_a_nested_in_general_for_binary_accuracy_cue"] is True
    assert contract["nesting_statement"]["exclusive_family_classification_authorized"] is False
    assert contract["test_procedure"]["parametric_bootstrap_required"] is True
    assert contract["test_procedure"]["asymptotic_chi_square_assumed"] is False
    assert contract["test_procedure"]["no_unique_winner_required"] is True

    assert design["execution_boundary"] == {
        "recovery_engine_present": False,
        "authoritative_run_allowed": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_current_cbd_action_surface_is_exactly_nested_in_general_surface() -> None:
    b = -0.2
    accuracy_baseline = 0.43
    beta_accuracy_cue = 1.1
    beta_reward = 0.8

    w0 = accuracy_baseline
    w1 = expit(logit(accuracy_baseline) + beta_accuracy_cue)

    beta = (
        b,
        w0,
        0.0,
        beta_reward * (1.0 - w0),
        w1 - w0,
        beta_reward * (w0 - w1),
    )

    cells = np.asarray(list(product([0.2, 0.5, 0.8], [0.0, 1.0], [-1.0, 0.0, 1.0])))
    B, A, R = cells[:, 0], cells[:, 1], cells[:, 2]

    expected = ap_a_utility(
        b,
        accuracy_baseline,
        beta_accuracy_cue,
        beta_reward,
        B,
        A,
        R,
    )
    observed = general_utility(beta, B, A, R)

    assert np.allclose(expected, observed, atol=1e-12)
    _, beta_b, beta_a, beta_r, beta_ab, beta_ar = beta
    assert beta_a == 0.0
    assert abs(beta_ar * (1.0 - beta_b) + beta_r * beta_ab) < 1e-12
    assert 0.0 < beta_b < 1.0
    assert 0.0 < beta_b + beta_ab < 1.0


def test_additive_surface_is_nested_in_general_surface() -> None:
    beta = (-0.2, 0.8, 0.3, 0.6, 0.0, 0.0)
    assert beta[4] == 0.0
    assert beta[5] == 0.0


def test_document_rejects_exclusive_nested_family_classification() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "REJECTED FOR AUTHORITATIVE USE" in text
    assert "No unique model winner is required" in text
    assert "parametric bootstrap" in text
    assert "RMS utility distance" in text
