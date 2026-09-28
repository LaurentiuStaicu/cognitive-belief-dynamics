from __future__ import annotations

from collections.abc import Iterable
from typing import Mapping

from .f1b_r2_openblas_lineage import (
    EXPECTED_OPENBLAS_CORE,
    MAX_RETAINED_DRAW_INDEX,
    validate_candidate_environment,
    validate_retained_draw_indices,
    validate_runtime_cores,
)


HOMOGENEOUS_PAIRED_LINEAGE_ID = (
    "F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1"
)
HOMOGENEOUS_PAIRED_STATUS = (
    "NON_AUTHORITATIVE_HOMOGENEOUS_PAIRED_SOURCE_REGENERATION_DESIGN"
)
EXPECTED_EVALUATION_REPLICATES = tuple(range(10))
EXPECTED_UNIQUE_DATASETS = 390
EXPECTED_RESTRICTION_RUNS = 750
EXPECTED_SNAPSHOTS = 2250
EXPECTED_PAIR_COMPARISONS = 2250


def validate_homogeneous_paired_config(config: dict) -> None:
    if config["lineage_id"] != HOMOGENEOUS_PAIRED_LINEAGE_ID:
        raise ValueError("homogeneous paired lineage identity changed")
    if config["status"] != HOMOGENEOUS_PAIRED_STATUS:
        raise ValueError("unsupported homogeneous paired lineage status")
    if int(config["issue"]) != 234:
        raise ValueError("homogeneous paired lineage issue changed")

    candidate = config["candidate_environment"]
    if candidate["variable"] != "OPENBLAS_CORETYPE":
        raise ValueError("candidate OpenBLAS environment variable changed")
    if candidate["value"] != EXPECTED_OPENBLAS_CORE:
        raise ValueError("candidate OpenBLAS core changed")
    if candidate["must_be_set_before_python_start"] is not True:
        raise ValueError("OpenBLAS core must be frozen before Python starts")
    if candidate["runtime_core_confirmation_required"] is not True:
        raise ValueError("runtime OpenBLAS core confirmation is required")

    h1 = config["h1_full_source_regeneration"]
    if tuple(int(x) for x in h1["evaluation_replicates"]) != (
        EXPECTED_EVALUATION_REPLICATES
    ):
        raise ValueError("H1 evaluation-replicate grid changed")
    if int(h1["expected_unique_dataset_count"]) != EXPECTED_UNIQUE_DATASETS:
        raise ValueError("H1 unique-dataset count changed")
    if int(h1["expected_restriction_run_count"]) != EXPECTED_RESTRICTION_RUNS:
        raise ValueError("H1 restriction-run count changed")
    if int(h1["expected_snapshot_count"]) != EXPECTED_SNAPSHOTS:
        raise ValueError("H1 snapshot count changed")
    if int(h1["expected_pair_comparison_count"]) != EXPECTED_PAIR_COMPARISONS:
        raise ValueError("H1 pair-comparison count changed")
    if tuple(int(x) for x in h1["draw_grid"]) != (49, 99, 199):
        raise ValueError("H1 draw grid changed")
    if int(h1["maximum_draw_index"]) != MAX_RETAINED_DRAW_INDEX:
        raise ValueError("H1 maximum draw index changed")
    if h1["new_draw_index_ge_199_authorized"] is not False:
        raise ValueError("H1 must not authorize draw index >=199")
    if h1["scientific_dataset_identity_changed"] is not False:
        raise ValueError("H1 must preserve scientific dataset identity")
    if h1["seed_derivation_changed"] is not False:
        raise ValueError("H1 must preserve seed derivation")

    h2 = config["h2_stage_b_rebuild"]
    if h2["historical_stage_b_checkpoint_inheritance_allowed"] is not False:
        raise ValueError("historical Stage-B checkpoints cannot be inherited")
    if h2["controller_changed"] is not False:
        raise ValueError("H2 controller must remain unchanged")
    if float(h2["alpha"]) != 0.05:
        raise ValueError("H2 alpha changed")
    if float(h2["epsilon"]) != 0.001:
        raise ValueError("H2 epsilon changed")
    if float(h2["halfspend"]) != 1000.0:
        raise ValueError("H2 halfspend changed")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("homogeneous paired interpretation boundary weakened")


def validate_h1_environment(
    environment: Mapping[str, str | None] | None = None,
) -> None:
    validate_candidate_environment(
        environment,
        expected_core=EXPECTED_OPENBLAS_CORE,
    )


def validate_h1_runtime_cores(cores: tuple[str, ...]) -> None:
    validate_runtime_cores(
        cores,
        expected_core=EXPECTED_OPENBLAS_CORE,
    )


def validate_h1_draw_indices(draw_indices: Iterable[int]) -> tuple[int, ...]:
    return validate_retained_draw_indices(tuple(draw_indices))


def validate_h1_replicates(
    replicate_indices: Iterable[int],
) -> tuple[int, ...]:
    values = tuple(int(value) for value in replicate_indices)
    if not values:
        raise ValueError("H1 replicate set must not be empty")
    if tuple(sorted(set(values))) != values:
        raise ValueError("H1 replicate indices must be unique and increasing")
    if values[0] < 0 or values[-1] > 9:
        raise ValueError("H1 replicate indices must lie in 0..9")
    return values
