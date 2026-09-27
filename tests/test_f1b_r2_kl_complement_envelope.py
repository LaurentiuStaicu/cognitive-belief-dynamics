from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import cognitive_epistemic_model.calibration.f1b_r2_kl_complement_envelope as env

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_kl_complement_envelope_diagnostic.json"
)
KL_CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_kl_controlled_departure_design_v1.json"
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


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fake_projection(mean_kl: float, *, closure: bool = False) -> dict:
    status = (
        "NON_ATTAINED_OR_CLOSURE_LIMIT"
        if closure
        else "FINITE_INTERIOR_ATTAINED"
    )
    components = ["W1=HIGH"] if closure else []
    return {
        "attainment_status": status,
        "closure_boundary_components": components,
        "scientific_domain_components": [],
        "selected_widest_domain": {
            "primary_distance": float(mean_kl),
            "selected_surface_coordinates": [-0.2, 0.4, 0.6, 0.8],
            "surface_metrics": {
                "utility_rms_distance": 0.2,
                "probability_rms_distance": 0.05,
                "information_weighted_logit_distance": 0.1,
                "min_probability_general": 0.2,
                "max_probability_general": 0.8,
                "min_probability_cbd": 0.25,
                "max_probability_cbd": 0.75,
            },
        },
    }


def test_envelope_contract_is_the_frozen_v1_failure_diagnostic() -> None:
    config = load(CONFIG)
    assert config["issue"] == 182
    assert config["selected_axis"] == "COMPLEMENT_RELATION_VIOLATION"
    assert config["anchors"] == ["CBD_ANCHOR_1", "CBD_ANCHOR_2"]
    assert config["signs"] == [-1, 1]
    assert config["frozen_targets"] == [0.001, 0.005, 0.01]
    assert config["scalar_grid"] == {
        "start": 0.0,
        "step": 0.025,
        "maximum": 20.0,
        "expected_point_count": 801,
    }
    assert config["execution_boundary"] == {
        "v1_target_revision_allowed": False,
        "scalar_range_revision_allowed": False,
        "ray_revision_allowed": False,
        "stochastic_simulation_allowed": False,
        "bootstrap_allowed": False,
        "paired_bootstrap_authorized": False,
        "authoritative_power_validated": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_envelope_classifies_crossings_and_above_envelope(monkeypatch) -> None:
    call_index = {"value": 0}

    def fake_project(*args, **kwargs):
        index = call_index["value"]
        call_index["value"] += 1
        if index <= 300:
            mean_kl = 0.00002 * index
        else:
            mean_kl = 0.006 - 0.000008 * (index - 300)
        return _fake_projection(
            max(0.0, mean_kl),
            closure=index >= 200,
        )

    monkeypatch.setattr(env, "_project_kl_closure", fake_project)

    result = env.scan_complement_kl_ray(
        load(CONFIG),
        load(KL_CONFIG),
        load(REVIEW),
        load(HISTORICAL),
        anchor_id="CBD_ANCHOR_1",
        sign=1,
    )

    assert result["point_count"] == 801
    assert result["scalar_start"] == 0.0
    assert result["scalar_end"] == 20.0
    assert result["maximum_mean_bernoulli_kl"] == pytest.approx(0.006)
    assert result["scalar_at_maximum"] == pytest.approx(7.5)
    assert result["monotone_non_decreasing"] is False
    assert result["direction_reversal_count"] == 1
    assert result["first_closure_scalar"] == pytest.approx(5.0)

    by_target = {
        row["target"]: row for row in result["target_results"]
    }
    assert by_target[0.001]["classification"] == (
        "TARGET_ATTAINABLE_WITHIN_V1_RANGE"
    )
    assert by_target[0.001]["first_crossing_bracket"] == pytest.approx(
        [1.225, 1.25]
    )
    assert by_target[0.005]["classification"] == (
        "TARGET_ATTAINABLE_WITHIN_V1_RANGE"
    )
    assert by_target[0.005]["first_crossing_bracket"] == pytest.approx(
        [6.225, 6.25]
    )
    assert by_target[0.01]["classification"] == (
        "TARGET_ABOVE_RAY_ENVELOPE_WITHIN_V1_RANGE"
    )
    assert by_target[0.01]["maximum_observed_mean_kl"] == pytest.approx(
        0.006
    )
    assert by_target[0.01]["non_monotone_after_maximum"] is True


def test_envelope_fails_closed_on_scientific_domain_activity(monkeypatch) -> None:
    call_index = {"value": 0}

    def fake_project(*args, **kwargs):
        index = call_index["value"]
        call_index["value"] += 1
        projection = _fake_projection(0.00001 * index)
        if index == 3:
            projection["scientific_domain_components"] = [
                "beta_reward=HIGH"
            ]
        return projection

    monkeypatch.setattr(env, "_project_kl_closure", fake_project)
    with pytest.raises(env.ComplementKLEnvelopeError, match="UNRESOLVED"):
        env.scan_complement_kl_ray(
            load(CONFIG),
            load(KL_CONFIG),
            load(REVIEW),
            load(HISTORICAL),
            anchor_id="CBD_ANCHOR_1",
            sign=-1,
        )


def _ray(anchor: str, sign: int) -> dict:
    return {
        "diagnostic_id": (
            "F1B.R2.KL_COMPLEMENT_ATTAINABLE_ENVELOPE.2026-09-27"
        ),
        "status": "NON_AUTHORITATIVE_KL_COMPLEMENT_ENVELOPE_RAY_RESULT",
        "authoritative": False,
        "anchor_id": anchor,
        "sign": sign,
        "point_count": 801,
        "profile": [],
    }


def test_envelope_combiner_requires_exact_four_rays() -> None:
    config = load(CONFIG)
    rays = [
        _ray("CBD_ANCHOR_1", -1),
        _ray("CBD_ANCHOR_1", 1),
        _ray("CBD_ANCHOR_2", -1),
        _ray("CBD_ANCHOR_2", 1),
    ]
    combined = env.combine_complement_kl_envelope_rays(
        list(reversed(rays)),
        config,
    )
    assert combined["ray_count"] == 4
    assert combined["point_count"] == 3204
    assert [
        (row["anchor_id"], row["sign"]) for row in combined["rays"]
    ] == [
        ("CBD_ANCHOR_1", -1),
        ("CBD_ANCHOR_1", 1),
        ("CBD_ANCHOR_2", -1),
        ("CBD_ANCHOR_2", 1),
    ]

    with pytest.raises(ValueError, match="duplicate"):
        env.combine_complement_kl_envelope_rays(
            [rays[0], rays[0]],
            config,
        )
    with pytest.raises(ValueError, match="coverage is incomplete"):
        env.combine_complement_kl_envelope_rays(
            rays[:3],
            config,
        )


def test_envelope_does_not_allow_posthoc_grid_change() -> None:
    config = load(CONFIG)
    changed = copy.deepcopy(config)
    changed["scalar_grid"]["maximum"] = 21.0
    with pytest.raises(ValueError, match="scalar grid"):
        env._validate_config(
            changed,
            load(KL_CONFIG),
            load(REVIEW),
        )

    changed = copy.deepcopy(config)
    changed["frozen_targets"] = [0.001, 0.004, 0.008]
    with pytest.raises(ValueError, match="target grid"):
        env._validate_config(
            changed,
            load(KL_CONFIG),
            load(REVIEW),
        )
