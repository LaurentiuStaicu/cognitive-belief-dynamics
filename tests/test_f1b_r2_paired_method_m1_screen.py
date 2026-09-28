from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import numpy as np
import pytest

from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R2Dataset,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    EXPECTED_METHODS,
    assert_missingness_subset,
    evaluate_all_methods,
    validate_m1_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_paired_method_m1_screen_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def test_repository_m1_contract_is_frozen() -> None:
    config = load_config()
    validate_m1_config(config)
    assert config["scientific_design"]["expected_departure_cell_count"] == 72
    assert config["scientific_design"]["total_scientific_restriction_runs"] == 840
    assert config["scientific_design"]["total_method_executions"] == 3360
    assert config["bootstrap"]["attempted_draws"] == 199
    assert config["bootstrap"]["minimum_successful_draws"] == 180
    assert tuple(row["id"] for row in config["methods"]) == EXPECTED_METHODS


def test_m1_contract_rejects_boundary_weakening() -> None:
    config = deepcopy(load_config())
    config["boundary"]["method_selected"] = True
    with pytest.raises(ValueError, match="boundary"):
        validate_m1_config(config)


def _dataset(indices: list[int]) -> R2Dataset:
    values = np.asarray(indices, dtype=int)
    return R2Dataset(
        share=(values % 2).astype(int),
        belief=(0.1 + values * 0.01).astype(float),
        accuracy_cue=(values % 2).astype(float),
        reward_context=((values % 3) - 1).astype(float),
        participant=(values // 4).astype(int),
        item=(values % 4).astype(int),
    )


def test_missingness_must_be_exact_subset() -> None:
    complete = _dataset(list(range(12)))
    missing = R2Dataset(
        share=complete.share[[0, 2, 7, 9]],
        belief=complete.belief[[0, 2, 7, 9]],
        accuracy_cue=complete.accuracy_cue[[0, 2, 7, 9]],
        reward_context=complete.reward_context[[0, 2, 7, 9]],
        participant=complete.participant[[0, 2, 7, 9]],
        item=complete.item[[0, 2, 7, 9]],
    )
    assert_missingness_subset(complete, missing)

    corrupted = R2Dataset(
        share=missing.share.copy(),
        belief=missing.belief.copy(),
        accuracy_cue=missing.accuracy_cue.copy(),
        reward_context=missing.reward_context.copy(),
        participant=missing.participant.copy(),
        item=missing.item.copy(),
    )
    corrupted.share[0] = 1 - corrupted.share[0]
    with pytest.raises(ValueError, match="response"):
        assert_missingness_subset(complete, corrupted)


def _row(
    *,
    method: str,
    missingness: float,
    role: str,
    identity: str,
    kl: float | None,
    rejected: bool,
    failure: bool = False,
) -> dict:
    return {
        "inference_method": method,
        "missingness_rate": missingness,
        "role": role,
        "identity": identity,
        "identity_type": "NULL" if "NULL" in role else "DEPARTURE",
        "target_mean_bernoulli_kl": kl,
        "fit_failure": failure,
        "bootstrap_calibration_failure": failure,
        "rejected": None if failure else rejected,
    }


def synthetic_pass_rows() -> list[dict]:
    rows: list[dict] = []
    for method in EXPECTED_METHODS:
        for missingness in (0.0, 0.15):
            for identity, role in (
                ("ADD_NULL", "ADD_NULL_FALSE_REJECTION"),
                ("CBD_NULL_ANCHOR_1", "CBD_NULL_FALSE_REJECTION"),
                ("CBD_NULL_ANCHOR_2", "CBD_NULL_FALSE_REJECTION"),
            ):
                rows.extend(
                    _row(
                        method=method,
                        missingness=missingness,
                        role=role,
                        identity=identity,
                        kl=None,
                        rejected=False,
                    )
                    for _ in range(20)
                )

            for kl in (0.001, 0.002, 0.003):
                rows.extend(
                    _row(
                        method=method,
                        missingness=missingness,
                        role="ADD_SPECIFICITY_NEGATIVE_CONTROL",
                        identity=f"SPEC_{kl}",
                        kl=kl,
                        rejected=False,
                    )
                    for _ in range(20)
                )
                rows.extend(
                    _row(
                        method=method,
                        missingness=missingness,
                        role="CBD_DEPARTURE_DETECTION",
                        identity=f"CBD_{kl}",
                        kl=kl,
                        rejected=(kl == 0.003),
                    )
                    for _ in range(60)
                )
                rows.extend(
                    _row(
                        method=method,
                        missingness=missingness,
                        role="ADD_DEPARTURE_DIAGNOSTIC",
                        identity=f"ADD_{kl}",
                        kl=kl,
                        rejected=(kl == 0.003),
                    )
                    for _ in range(40)
                )
    assert len(rows) == 3360
    return rows


def test_m1_synthetic_all_methods_can_remain_eligible() -> None:
    result = evaluate_all_methods(synthetic_pass_rows(), load_config())
    assert result["eligible_methods"] == list(EXPECTED_METHODS)
    assert result["overall_decision"] == "M1_HAS_ELIGIBLE_METHODS"
    assert result["hierarchical_scale_sensitive"] is False
    assert {
        row["decision_state"] for row in result["method_results"]
    } == {"M1_ELIGIBLE"}


def test_m1_null_pathology_makes_only_affected_method_ineligible() -> None:
    rows = synthetic_pass_rows()
    target = [
        row
        for row in rows
        if row["inference_method"] == "POPULATION"
        and row["missingness_rate"] == 0.0
        and row["identity"] == "ADD_NULL"
    ]
    for row in target[:6]:
        row["rejected"] = True

    result = evaluate_all_methods(rows, load_config())
    decisions = {
        row["inference_method"]: row["decision_state"]
        for row in result["method_results"]
    }
    assert decisions["POPULATION"] == "M1_INELIGIBLE_NULL_OR_SPECIFICITY"
    assert decisions["HIERARCHICAL_1X"] == "M1_ELIGIBLE"


def test_m1_operational_failures_are_not_dropped_from_denominator() -> None:
    rows = synthetic_pass_rows()
    population = [
        row for row in rows if row["inference_method"] == "POPULATION"
    ]
    for row in population[:18]:
        row["fit_failure"] = True
        row["bootstrap_calibration_failure"] = True
        row["rejected"] = None

    result = evaluate_all_methods(rows, load_config())
    population_result = next(
        row for row in result["method_results"]
        if row["inference_method"] == "POPULATION"
    )
    assert population_result["overall_failure_rate"] == pytest.approx(18 / 840)
    assert population_result["decision_state"] == "M1_INELIGIBLE_OPERATIONAL"
