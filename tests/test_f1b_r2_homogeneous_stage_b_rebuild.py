from __future__ import annotations

import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_stage_b_rebuild import (
    build_h2_effective_controller,
    validate_frozen_controller,
    validate_h2_rebuild_config,
    validate_retained_h1_result,
)


ROOT = Path(__file__).resolve().parents[1]
REBUILD_CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_homogeneous_stage_b_rebuild_v1.json"
)
CONTROLLER_CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_resampling_risk_controller_v1.json"
)
H1_RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_homogeneous_paired_h1_qualification_2026-09-28.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_h2_rebuild_contract_is_frozen_and_non_authoritative() -> None:
    config = load(REBUILD_CONFIG)
    validate_h2_rebuild_config(config)

    assert config["issue"] == 234
    assert config["source_lineage"]["combined_json_sha256"] == (
        "618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e"
    )
    assert config["source_lineage"]["expected_restriction_runs"] == 750
    assert config["source_lineage"]["expected_attempts_per_run"] == 199

    execution = config["h2_execution"]
    assert execution["new_bootstrap_attempts_allowed"] is False
    assert execution["source_attempts_reused_only"] is True
    assert execution["maximum_attempts"] == 199
    assert (
        execution["historical_stage_b_checkpoint_inheritance_allowed"]
        is False
    )
    assert not any(config["boundary"].values())


def test_retained_h1_result_is_explicitly_accepted_for_h2() -> None:
    config = load(REBUILD_CONFIG)
    h1 = load(H1_RESULT)
    validate_retained_h1_result(h1, config)

    assert h1["decision"]["homogeneous_source_accepted_for_h2_input"] is True
    assert h1["decision"]["historical_stage_b_may_be_inherited"] is False


def test_effective_controller_changes_only_replay_source_provenance() -> None:
    rebuild = load(REBUILD_CONFIG)
    base = load(CONTROLLER_CONFIG)
    validate_frozen_controller(base, rebuild)
    effective = build_h2_effective_controller(base, rebuild)

    for key, value in base.items():
        if key == "replay_source":
            continue
        assert effective[key] == value

    source = effective["replay_source"]
    assert source["exact_artifact_id"] == 10961527329
    assert source["exact_json_sha256"] == (
        "618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e"
    )
    assert source["expected_restriction_runs"] == 750
    assert source["expected_attempts_per_run"] == 199
    assert source["expected_bootstrap_fit_failures"] == 0


def test_controller_parameter_change_fails_closed() -> None:
    rebuild = load(REBUILD_CONFIG)
    base = load(CONTROLLER_CONFIG)
    base["epsilon"] = 0.002
    with pytest.raises(ValueError, match="epsilon"):
        validate_frozen_controller(base, rebuild)


def test_historical_stage_b_inheritance_cannot_be_enabled() -> None:
    config = load(REBUILD_CONFIG)
    config["h2_execution"][
        "historical_stage_b_checkpoint_inheritance_allowed"
    ] = True
    with pytest.raises(ValueError, match="inherit"):
        validate_h2_rebuild_config(config)


def test_new_attempt_generation_cannot_be_enabled() -> None:
    config = load(REBUILD_CONFIG)
    config["h2_execution"]["new_bootstrap_attempts_allowed"] = True
    with pytest.raises(ValueError, match="new bootstrap attempts"):
        validate_h2_rebuild_config(config)


def test_source_hash_change_fails_closed() -> None:
    config = load(REBUILD_CONFIG)
    config["source_lineage"]["combined_json_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="SHA-256"):
        validate_h2_rebuild_config(config)
