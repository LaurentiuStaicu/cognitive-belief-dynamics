from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m1_screen import (
    M1ScientificSpec,
    dataset_id_for,
)
from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_broad_scientific_matrix as s4,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_s4_broad_scientific_matrix_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def make_spec(
    index: int,
    *,
    identity_type: str,
    role: str,
    identity: str | None = None,
) -> M1ScientificSpec:
    value = identity or f"DEPARTURE_{index:02d}"
    return M1ScientificSpec(
        template_run_id=f"TEMPLATE_{index:02d}",
        identity=value,
        identity_type=identity_type,
        restriction=(
            "ADD_RESTRICTION"
            if role.startswith("ADD_")
            else "CBD_COMPLEMENT_RESTRICTION"
        ),
        role=role,
        anchor_id=(
            None
            if role == "ADD_NULL_FALSE_REJECTION"
            else f"ANCHOR_{index:02d}"
        ),
        axis=None if identity_type == "NULL" else f"AXIS_{index:02d}",
        sign=None if identity_type == "NULL" else (1 if index % 2 else -1),
        target_mean_bernoulli_kl=(
            None if identity_type == "NULL" else 0.002
        ),
        dataset_id_prefix=f"DATASET_{index:02d}",
        replicate_count=5 if identity_type == "DEPARTURE" else 20,
    )


def synthetic_m1_specs() -> list[M1ScientificSpec]:
    departure_roles = (
        ["ADD_SPECIFICITY_NEGATIVE_CONTROL"] * 12
        + ["ADD_DEPARTURE_DIAGNOSTIC"] * 24
        + ["CBD_DEPARTURE_DETECTION"] * 36
    )
    specs = [
        make_spec(index, identity_type="DEPARTURE", role=role)
        for index, role in enumerate(departure_roles)
    ]
    specs.extend(
        [
            make_spec(
                72,
                identity_type="NULL",
                role="ADD_NULL_FALSE_REJECTION",
                identity="ADD_NULL",
            ),
            make_spec(
                73,
                identity_type="NULL",
                role="CBD_NULL_FALSE_REJECTION",
                identity="CBD_NULL_ANCHOR_1",
            ),
            make_spec(
                74,
                identity_type="NULL",
                role="CBD_NULL_FALSE_REJECTION",
                identity="CBD_NULL_ANCHOR_2",
            ),
        ]
    )
    return specs


def test_repository_s4_matrix_contract_is_frozen() -> None:
    config = load_config()
    s4.validate_s4_matrix_config(config)
    design = config["scientific_design"]
    assert design["expected_departure_cell_count"] == 72
    assert design["expected_null_identity_count"] == 3
    assert design["expected_restriction_cell_count"] == 75
    assert design["evaluation_replicate_indices"] == list(range(100))
    assert design["restriction_runs_per_missingness"] == 7500
    assert design["departure_runs_total"] == 14400
    assert design["null_runs_total"] == 600
    assert design["total_scientific_runs"] == 15000
    assert config["precision"]["maximum_worst_case_component_mcse"] == 0.05
    assert config["method_binding"]["eligible_methods_known_at_this_gate"] is False


def test_m1_prefix_dataset_ids_are_unchanged_when_spec_expands() -> None:
    departure = make_spec(
        0,
        identity_type="DEPARTURE",
        role="ADD_DEPARTURE_DIAGNOSTIC",
    )
    broad_departure = s4.replace(departure, replicate_count=100)
    for replicate in range(5):
        assert dataset_id_for(departure, replicate) == dataset_id_for(
            broad_departure,
            replicate,
        )

    null = make_spec(
        72,
        identity_type="NULL",
        role="ADD_NULL_FALSE_REJECTION",
        identity="ADD_NULL",
    )
    broad_null = s4.replace(null, replicate_count=100)
    for replicate in range(20):
        assert dataset_id_for(null, replicate) == dataset_id_for(
            broad_null,
            replicate,
        )


def test_scientific_run_id_freezes_replicate_restriction_and_missingness() -> None:
    spec = s4.replace(
        make_spec(
            0,
            identity_type="DEPARTURE",
            role="ADD_DEPARTURE_DIAGNOSTIC",
        ),
        replicate_count=100,
    )
    assert s4.scientific_run_id(spec, 99, 0.15) == (
        "DATASET_00|REPLICATE=99"
        "|RESTRICTION=ADD_RESTRICTION|MISSINGNESS=0.15"
    )


def test_manifest_is_exactly_15000_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    config = load_config()
    specs = synthetic_m1_specs()
    monkeypatch.setattr(
        s4,
        "select_scientific_specs",
        lambda source, m1_config: specs,
    )
    manifest = s4.build_s4_scientific_manifest({}, {}, config)
    assert manifest["restriction_cell_count"] == 75
    assert manifest["scientific_cell_missingness_count"] == 150
    assert manifest["scientific_run_count"] == 15000
    assert manifest["departure_run_count"] == 14400
    assert manifest["null_run_count"] == 600
    assert manifest["missingness_run_counts"] == {
        "0.00": 7500,
        "0.15": 7500,
    }
    assert len(manifest["rows"]) == 15000
    assert len(
        {row["scientific_run_id"] for row in manifest["rows"]}
    ) == 15000
    assert manifest["boundary"] == config["boundary"]


def test_matrix_gate_cannot_preselect_methods() -> None:
    config = deepcopy(load_config())
    config["method_binding"]["eligible_methods_known_at_this_gate"] = True
    with pytest.raises(ValueError, match="preselect"):
        s4.validate_s4_matrix_config(config)


def test_matrix_gate_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["inference_methods_executed"] = True
    with pytest.raises(ValueError, match="boundary"):
        s4.validate_s4_matrix_config(config)
