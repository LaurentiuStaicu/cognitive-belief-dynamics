from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_homogeneous_paired_lineage import (
    EXPECTED_EVALUATION_REPLICATES,
    validate_h1_draw_indices,
    validate_h1_environment,
    validate_h1_replicates,
    validate_h1_runtime_cores,
    validate_homogeneous_paired_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_homogeneous_paired_source_lineage_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_homogeneous_paired_contract_is_frozen_and_non_authoritative() -> None:
    config = load_config()
    validate_homogeneous_paired_config(config)

    assert config["issue"] == 234
    assert config["candidate_environment"] == {
        "variable": "OPENBLAS_CORETYPE",
        "value": "Haswell",
        "must_be_set_before_python_start": True,
        "runtime_core_confirmation_required": True,
        "runtime_probe": "OPENBLAS_VERBOSE=2_OR_EQUIVALENT_OPENBLAS_API",
    }
    h1 = config["h1_full_source_regeneration"]
    assert tuple(h1["evaluation_replicates"]) == EXPECTED_EVALUATION_REPLICATES
    assert h1["draw_grid"] == [49, 99, 199]
    assert h1["maximum_draw_index"] == 198
    assert h1["expected_unique_dataset_count"] == 390
    assert h1["expected_restriction_run_count"] == 750
    assert h1["expected_snapshot_count"] == 2250
    assert h1["expected_pair_comparison_count"] == 2250
    assert h1["scientific_dataset_identity_changed"] is False
    assert h1["seed_derivation_changed"] is False

    identity = config["new_source_identity"]
    assert identity["wrapper_metadata_required"] is True
    assert identity["scientific_characterization_id_changed"] is False
    assert identity["scientific_dataset_id_changed"] is False
    assert identity["seed_identity_changed"] is False

    h2 = config["h2_stage_b_rebuild"]
    assert h2["historical_stage_b_checkpoint_inheritance_allowed"] is False
    assert h2["controller_changed"] is False
    assert h2["alpha"] == 0.05
    assert h2["epsilon"] == 0.001
    assert h2["halfspend"] == 1000
    assert not any(config["boundary"].values())


def test_h1_environment_fails_closed() -> None:
    validate_h1_environment({"OPENBLAS_CORETYPE": "Haswell"})
    with pytest.raises(ValueError, match="requires"):
        validate_h1_environment({})
    with pytest.raises(ValueError, match="requires"):
        validate_h1_environment({"OPENBLAS_CORETYPE": "SkylakeX"})


def test_h1_runtime_core_confirmation_fails_closed() -> None:
    validate_h1_runtime_cores(("Haswell", "Haswell"))
    with pytest.raises(ValueError, match="must not be empty"):
        validate_h1_runtime_cores(())
    with pytest.raises(ValueError, match="non-qualified"):
        validate_h1_runtime_cores(("Haswell", "SkylakeX"))


def test_h1_draws_cannot_cross_retained_prefix() -> None:
    assert validate_h1_draw_indices((0, 49, 99, 198)) == (0, 49, 99, 198)
    with pytest.raises(ValueError, match="0..198"):
        validate_h1_draw_indices((199,))
    with pytest.raises(ValueError, match="unique and increasing"):
        validate_h1_draw_indices((1, 1))


def test_h1_replicates_are_bounded_and_ordered() -> None:
    assert validate_h1_replicates(range(10)) == tuple(range(10))
    assert validate_h1_replicates((0, 7, 8, 9)) == (0, 7, 8, 9)
    with pytest.raises(ValueError, match="0..9"):
        validate_h1_replicates((10,))
    with pytest.raises(ValueError, match="unique and increasing"):
        validate_h1_replicates((1, 1))


def test_config_protects_existing_scientific_and_execution_paths() -> None:
    config = load_config()
    assert set(config["protected_scientific_file_git_blob_sha"]) == {
        "src/cognitive_epistemic_model/calibration/f1b_r2_paired_bootstrap_characterization.py",
        "src/cognitive_epistemic_model/calibration/f1b_r2_restriction_recovery.py",
        "src/cognitive_epistemic_model/calibration/f1b_prehuman_recovery.py",
        "src/cognitive_epistemic_model/calibration/f1b_hierarchical_recovery.py",
        "src/cognitive_epistemic_model/calibration/f1b_r2_kl_controlled_departures.py",
    }
    assert set(config["protected_execution_file_git_blob_sha"]) == {
        "scripts/run_f1b_r2_kl_v2_paired_bootstrap.py",
        "scripts/combine_f1b_r2_kl_v2_paired_bootstrap_partitions.py",
    }
    assert config["historical_paired_source"]["inherit_as_future_source"] is False


def test_frozen_input_sha256_values_match_repository_files() -> None:
    config = load_config()
    for label, spec in config["frozen_inputs"].items():
        path = ROOT / spec["path"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == spec["sha256"], (
            f"{label} SHA-256 changed: {actual} != {spec['sha256']}"
        )
