from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_post_c2_scientific_interpretation import (
    NOT_REJECT,
    REJECT,
    UNRESOLVED,
    _final_state_from_c2,
    _role_semantic_summary,
    _unique_map,
    canonical_json_sha256,
    summarize_three_outcome,
    validate_interpretation_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_post_c2_scientific_interpretation_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def test_repository_contract_is_frozen() -> None:
    config = load_config()
    validate_interpretation_config(config)
    assert config["retained_h2"]["expected_run_count"] == 750
    assert config["retained_h2"]["expected_unresolved_at_199_count"] == 224
    assert config["retained_c2"]["expected_resolved_count"] == 201
    assert config["retained_c2"]["expected_unresolved_at_cap_count"] == 23
    assert config["retained_c2"]["maximum_total_attempts"] == 10000
    assert config["final_state"] == {
        "expected_total_run_count": 750,
        "expected_reject_count": 246,
        "expected_not_reject_count": 481,
        "expected_unresolved_at_cap_count": 23,
        "allowed_terminal_states": [
            REJECT,
            NOT_REJECT,
            UNRESOLVED,
        ],
    }


def test_three_outcome_summary_keeps_unresolved_in_primary_denominator() -> None:
    rows = [
        {"final_state": REJECT},
        {"final_state": REJECT},
        {"final_state": NOT_REJECT},
        {"final_state": UNRESOLVED},
    ]
    summary = summarize_three_outcome(rows)
    assert summary["run_count"] == 4
    assert summary["reject_count"] == 2
    assert summary["not_reject_count"] == 1
    assert summary["unresolved_count"] == 1
    assert summary["reject_proportion"] == 0.5
    assert summary["not_reject_proportion"] == 0.25
    assert summary["unresolved_proportion"] == 0.25
    assert summary["reject_proportion_bounds_with_unresolved"] == [
        0.5,
        0.75,
    ]
    assert summary["conditional_reject_proportion_among_decided"] == (
        pytest.approx(2 / 3)
    )


def test_unresolved_c2_row_cannot_be_silently_reclassified() -> None:
    assert _final_state_from_c2(
        {"decision": None, "status": UNRESOLVED}
    ) == UNRESOLVED
    with pytest.raises(ValueError, match="unresolved-at-cap"):
        _final_state_from_c2(
            {"decision": None, "status": "SEQUENTIAL_UNRESOLVED"}
        )


def test_duplicate_run_ids_fail_closed() -> None:
    rows = [{"run_id": "a"}, {"run_id": "a"}]
    with pytest.raises(ValueError, match="not unique"):
        _unique_map(rows, "synthetic")


def test_interpretation_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["c2_cap_extension_allowed"] = True
    with pytest.raises(ValueError, match="boundary"):
        validate_interpretation_config(config)


def test_role_semantics_separate_detection_from_negative_control() -> None:
    config = load_config()
    rows = [
        {
            "role": "CBD_DEPARTURE_DETECTION",
            "final_state": REJECT,
        },
        {
            "role": "CBD_DEPARTURE_DETECTION",
            "final_state": NOT_REJECT,
        },
        {
            "role": "CBD_DEPARTURE_DETECTION",
            "final_state": UNRESOLVED,
        },
        {
            "role": "ADD_SPECIFICITY_NEGATIVE_CONTROL",
            "final_state": NOT_REJECT,
        },
        {
            "role": "ADD_SPECIFICITY_NEGATIVE_CONTROL",
            "final_state": REJECT,
        },
        {
            "role": "ADD_SPECIFICITY_NEGATIVE_CONTROL",
            "final_state": UNRESOLVED,
        },
    ]
    result = {
        row["role"]: row
        for row in _role_semantic_summary(rows, config)
    }

    detection = result["CBD_DEPARTURE_DETECTION"]
    assert detection["semantic_kind"] == "DETECTION_ROLE"
    assert detection["detection_proportion"] == pytest.approx(1 / 3)
    assert detection["detection_proportion_bounds_with_unresolved"] == [
        pytest.approx(1 / 3),
        pytest.approx(2 / 3),
    ]

    control = result["ADD_SPECIFICITY_NEGATIVE_CONTROL"]
    assert control["semantic_kind"] == "NEGATIVE_CONTROL_ROLE"
    assert control["specificity_pass_proportion"] == pytest.approx(1 / 3)
    assert control["specificity_pass_proportion_bounds_with_unresolved"] == [
        pytest.approx(1 / 3),
        pytest.approx(2 / 3),
    ]


def test_canonical_hash_is_order_sensitive_for_run_id_list() -> None:
    assert canonical_json_sha256(["a", "b"]) != canonical_json_sha256(
        ["b", "a"]
    )
