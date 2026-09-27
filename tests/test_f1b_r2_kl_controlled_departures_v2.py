from __future__ import annotations

import json
from pathlib import Path

import pytest

import cognitive_epistemic_model.calibration.f1b_r2_kl_controlled_departures as klgen
from cognitive_epistemic_model.calibration.f1b_r2_controlled_departures import (
    DepartureAxis,
)

ROOT = Path(__file__).resolve().parents[1]
V1 = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_kl_controlled_departure_design_v1.json"
)
V2 = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_kl_controlled_departure_design_v2.json"
)
REVIEW = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_distance_definition_review.json"
)
HISTORICAL = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)
ENVELOPE = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_kl_complement_envelope_result_2026-09-27.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fake_case_from_solver_arguments(**kwargs) -> dict:
    axis = kwargs["axis"]
    anchor_id = str(kwargs["anchor_id"])
    sign = int(kwargs["sign"])
    target = float(kwargs["target_mean_kl"])
    config = kwargs["config"]
    add_expected = (
        axis is DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT
    )
    return {
        "case_id": (
            f"{config['design_id']}__{anchor_id}__{axis.value}__"
            f"{sign}__KL_{target:.3f}"
        ),
        "design_version": str(config["design_id"]),
        "anchor_id": anchor_id,
        "anchor_family": (
            "CBD_ADD_INTERSECTION" if add_expected else "CBD"
        ),
        "axis": axis.value,
        "sign": sign,
        "requested_mean_bernoulli_kl": target,
        "achieved_mean_bernoulli_kl": target,
        "mean_kl_error": 0.0,
        "cbd_attainment_status": "FINITE_INTERIOR_ATTAINED",
        "add_compatibility_expected": add_expected,
        "add_compatibility_pass": True,
    }


def test_v2_contract_is_frozen_from_corrected_deterministic_geometry() -> None:
    config = load(V2)
    envelope = load(ENVELOPE)

    assert config["design_id"] == "F1B.R2.KL_CONTROLLED_DEPARTURE.V2"
    assert config["status"] == (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_DESIGN"
    )
    assert config["issue"] == 202
    assert config["target_mean_bernoulli_kl"] == [0.001, 0.002, 0.003]
    assert config["expected_case_count"] == 36

    rationale = config["target_grid_rationale"]
    binding = envelope["diagnostic_conclusion"][
        "minimum_plus_ray_envelope_maximum"
    ]
    assert binding == 0.0032538188153675754
    assert rationale["binding_complement_plus_envelope_maximum"] == binding
    assert rationale["upper_target"] == 0.003
    assert rationale["upper_target"] < binding
    assert rationale["upper_target_below_binding_envelope"] is True
    assert rationale["stochastic_or_power_input_used"] is False
    assert rationale["psychological_effect_size_labels_used"] is False


def test_v2_boundary_remains_deterministic_only() -> None:
    boundary = load(V2)["execution_boundary"]
    assert boundary == {
        "stochastic_simulation_allowed": False,
        "bootstrap_allowed": False,
        "operational_fitter_bounds_change_allowed": False,
        "historical_departure_rewrite_allowed": False,
        "paired_bootstrap_authorized": False,
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_power_validated": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_versioned_generator_preserves_v1_and_emits_v2_statuses(
    monkeypatch,
) -> None:
    review = load(REVIEW)
    historical = load(HISTORICAL)
    monkeypatch.setattr(
        klgen,
        "solve_kl_controlled_departure_case",
        lambda **kwargs: _fake_case_from_solver_arguments(**kwargs),
    )

    v1 = klgen.generate_kl_controlled_departure_design(
        load(V1),
        review,
        historical,
    )
    assert v1["design_id"] == "F1B.R2.KL_CONTROLLED_DEPARTURE.V1"
    assert v1["status"] == (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V1_RESULT"
    )
    assert v1["target_mean_bernoulli_kl"] == [0.001, 0.005, 0.01]
    assert v1["case_count"] == 36

    v2 = klgen.generate_kl_controlled_departure_design(
        load(V2),
        review,
        historical,
    )
    assert v2["design_id"] == "F1B.R2.KL_CONTROLLED_DEPARTURE.V2"
    assert v2["status"] == (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_RESULT"
    )
    assert v2["target_mean_bernoulli_kl"] == [0.001, 0.002, 0.003]
    assert v2["case_count"] == 36
    assert len({case["case_id"] for case in v2["cases"]}) == 36


def test_v2_partition_status_and_complete_grid_are_versioned(
    monkeypatch,
) -> None:
    config = load(V2)
    review = load(REVIEW)
    historical = load(HISTORICAL)
    monkeypatch.setattr(
        klgen,
        "solve_kl_controlled_departure_case",
        lambda **kwargs: _fake_case_from_solver_arguments(**kwargs),
    )

    partition = klgen.generate_kl_controlled_departure_partition(
        config,
        review,
        historical,
        axis_name="COMPLEMENT_RELATION_VIOLATION",
        anchor_id="CBD_ANCHOR_2",
    )
    assert partition["status"] == (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_PARTITION"
    )
    assert partition["target_mean_bernoulli_kl"] == [0.001, 0.002, 0.003]
    assert partition["case_count"] == 6
    assert {case["sign"] for case in partition["cases"]} == {-1, 1}
    assert {
        case["requested_mean_bernoulli_kl"]
        for case in partition["cases"]
    } == {0.001, 0.002, 0.003}


def test_frozen_version_contract_rejects_target_grid_mutation() -> None:
    config = load(V2)
    config["target_mean_bernoulli_kl"] = [0.001, 0.002, 0.0025]

    with pytest.raises(
        ValueError,
        match="target grid does not match the frozen design contract",
    ):
        klgen.generate_kl_controlled_departure_design(
            config,
            load(REVIEW),
            load(HISTORICAL),
        )


def test_frozen_version_contract_rejects_status_or_unknown_design() -> None:
    status_mismatch = load(V2)
    status_mismatch["status"] = (
        "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V1_DESIGN"
    )
    with pytest.raises(ValueError, match="status does not match design_id"):
        klgen.generate_kl_controlled_departure_design(
            status_mismatch,
            load(REVIEW),
            load(HISTORICAL),
        )

    unknown = load(V2)
    unknown["design_id"] = "F1B.R2.KL_CONTROLLED_DEPARTURE.V3"
    with pytest.raises(ValueError, match="unsupported KL controlled-departure"):
        klgen.generate_kl_controlled_departure_design(
            unknown,
            load(REVIEW),
            load(HISTORICAL),
        )
