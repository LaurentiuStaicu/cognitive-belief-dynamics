from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    NOT_REJECT,
    REFIT_FAILURE,
    REJECT,
    UNRESOLVED_AT_CAP,
    evaluate_method,
    validate_m1_combined,
    validate_m2_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_paired_method_m2_sequential_resolution_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


ROLE_COUNTS_PER_MISSINGNESS = {
    "ADD_NULL_FALSE_REJECTION": 20,
    "CBD_NULL_FALSE_REJECTION": 40,
    "ADD_SPECIFICITY_NEGATIVE_CONTROL": 60,
    "ADD_DEPARTURE_DIAGNOSTIC": 120,
    "CBD_DEPARTURE_DETECTION": 180,
}


def make_rows(method: str = "POPULATION") -> list[dict]:
    rows = []
    index = 0
    for missingness in (0.0, 0.15):
        for role, count in ROLE_COUNTS_PER_MISSINGNESS.items():
            for _ in range(count):
                if role in (
                    "ADD_DEPARTURE_DIAGNOSTIC",
                    "CBD_DEPARTURE_DETECTION",
                ):
                    decision = REJECT
                else:
                    decision = NOT_REJECT
                rows.append(
                    {
                        "scientific_run_id": f"run-{index}",
                        "inference_method": method,
                        "role": role,
                        "missingness_rate": missingness,
                        "status": "SEQUENTIAL_RESOLVED",
                        "decision": decision,
                        "terminal_n": 499,
                    }
                )
                index += 1
    assert len(rows) == 840
    return rows


def test_repository_m2_contract_is_frozen() -> None:
    config = load_config()
    validate_m2_config(config)
    assert config["retained_m1"]["eligible_methods"] == [
        "POPULATION",
        "HIERARCHICAL_0.5X",
        "HIERARCHICAL_1X",
        "HIERARCHICAL_2X",
    ]
    assert config["controller"]["prior_total_attempts"] == 199
    assert config["controller"]["maximum_total_attempts"] == 10000
    assert config["eligibility"] == {
        "maximum_overall_refit_failure_proportion": 0.02,
        "maximum_role_missingness_refit_failure_proportion": 0.05,
        "minimum_overall_resolution_proportion": 0.8,
        "minimum_role_missingness_resolution_proportion": 0.6,
        "m1_eligibility_inheritance_required": True,
    }


def test_m2_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        validate_m2_config(config)


def test_fully_resolved_method_is_eligible() -> None:
    result = evaluate_method(
        make_rows(),
        load_config(),
        "POPULATION",
    )
    assert result["decision_state"] == "M2_ELIGIBLE"
    assert result["overall_resolution_rate"] == 1.0
    assert result["overall_refit_failure_rate"] == 0.0
    assert result["checks"] == {
        "m1_eligibility_inherited": True,
        "refit_stability_pass": True,
        "overall_resolution_pass": True,
        "stratum_resolution_pass": True,
    }


def test_overall_resolution_failure_is_not_hidden() -> None:
    rows = make_rows()
    for row in rows[:169]:
        row["status"] = UNRESOLVED_AT_CAP
        row["decision"] = None
        row["terminal_n"] = 10000
    result = evaluate_method(rows, load_config(), "POPULATION")
    assert result["overall_resolution_rate"] < 0.8
    assert result["decision_state"] == (
        "M2_INELIGIBLE_OVERALL_RESOLUTION"
    )


def test_stratum_resolution_failure_is_not_hidden() -> None:
    rows = make_rows()
    target = [
        row
        for row in rows
        if row["role"] == "ADD_NULL_FALSE_REJECTION"
        and row["missingness_rate"] == 0.0
    ]
    assert len(target) == 20
    for row in target[:9]:
        row["status"] = UNRESOLVED_AT_CAP
        row["decision"] = None
        row["terminal_n"] = 10000

    result = evaluate_method(rows, load_config(), "POPULATION")
    assert result["overall_resolution_rate"] > 0.8
    assert result["checks"]["overall_resolution_pass"] is True
    assert result["checks"]["stratum_resolution_pass"] is False
    assert result["decision_state"] == (
        "M2_INELIGIBLE_STRATUM_RESOLUTION"
    )


def test_refit_failure_threshold_has_priority() -> None:
    rows = make_rows()
    for row in rows[:17]:
        row["status"] = REFIT_FAILURE
        row["decision"] = None
        row["terminal_n"] = 250
    result = evaluate_method(rows, load_config(), "POPULATION")
    assert result["overall_refit_failure_rate"] > 0.02
    assert result["decision_state"] == (
        "M2_INELIGIBLE_REFIT_STABILITY"
    )


def test_m2_accepts_actual_retained_m1_artifact_status() -> None:
    artifact = {
        "design_id": "F1B.R2.PAIRED_METHOD_M1_SCREEN.V1",
        "status": "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SCREEN_RESULT",
        "authoritative": False,
        "scientific_run_count": 840,
        "method_execution_count": 3360,
        "eligible_methods": [
            "POPULATION",
            "HIERARCHICAL_0.5X",
            "HIERARCHICAL_1X",
            "HIERARCHICAL_2X",
        ],
        "hierarchical_scale_sensitive": True,
        "rows": [],
    }
    with pytest.raises(ValueError, match="row count changed"):
        validate_m1_combined(artifact, load_config())
