from __future__ import annotations

import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_openblas_lineage import (
    parse_openblas_verbose_cores,
    validate_candidate_environment,
    validate_qualification_config,
    validate_retained_draw_indices,
    validate_runtime_cores,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_openblas_execution_lineage_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_openblas_verbose_parser_requires_runtime_core() -> None:
    assert parse_openblas_verbose_cores(
        "Core: Haswell\nCore: Haswell\n"
    ) == ("Haswell", "Haswell")
    with pytest.raises(ValueError, match="did not report"):
        parse_openblas_verbose_cores("no runtime core here")


def test_runtime_core_gate_requires_all_haswell() -> None:
    validate_runtime_cores(("Haswell", "Haswell"))
    with pytest.raises(ValueError, match="non-qualified"):
        validate_runtime_cores(("Haswell", "SkylakeX"))


def test_candidate_environment_requires_explicit_haswell() -> None:
    validate_candidate_environment({"OPENBLAS_CORETYPE": "Haswell"})
    with pytest.raises(ValueError, match="requires"):
        validate_candidate_environment({})
    with pytest.raises(ValueError, match="requires"):
        validate_candidate_environment({"OPENBLAS_CORETYPE": "SkylakeX"})


def test_qualification_draw_guard_forbids_new_indices() -> None:
    assert validate_retained_draw_indices((0, 17, 198)) == (0, 17, 198)
    with pytest.raises(ValueError, match="0..198"):
        validate_retained_draw_indices((199,))
    with pytest.raises(ValueError, match="unique and increasing"):
        validate_retained_draw_indices((2, 1))


def test_frozen_openblas_lineage_contract() -> None:
    config = load_config()
    validate_qualification_config(config)

    assert config["candidate_environment"] == {
        "variable": "OPENBLAS_CORETYPE",
        "value": "Haswell",
        "must_be_set_before_python_start": True,
        "runtime_core_confirmation_required": True,
        "runtime_probe": "OPENBLAS_VERBOSE=2_OR_EQUIVALENT_OPENBLAS_API",
    }
    assert config["q2_full_replay"]["required_stream_count"] == 224
    assert config["q2_full_replay"]["maximum_draw_index"] == 198
    assert (
        config["q2_full_replay"][
            "observed_statistic_absolute_tolerance"
        ]
        == 1e-10
    )
    assert not any(config["boundary"].values())


def test_boundary_weakening_fails_closed() -> None:
    config = load_config()
    config["boundary"]["stage_c2_authorized"] = True
    with pytest.raises(ValueError, match="boundary weakened"):
        validate_qualification_config(config)
