from __future__ import annotations

from copy import deepcopy


H2_REBUILD_ID = "F1B.R2.HOMOGENEOUS_STAGE_B_REBUILD.V1"
H2_STATUS = "NON_AUTHORITATIVE_HOMOGENEOUS_STAGE_B_REBUILD_DESIGN"


def validate_h2_rebuild_config(config: dict) -> None:
    if config["rebuild_id"] != H2_REBUILD_ID:
        raise ValueError("H2 rebuild identity changed")
    if config["status"] != H2_STATUS:
        raise ValueError("unsupported H2 rebuild status")
    if int(config["issue"]) != 234:
        raise ValueError("H2 issue changed")

    source = config["source_lineage"]
    if source["lineage_id"] != (
        "F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1"
    ):
        raise ValueError("H2 source lineage changed")
    if str(source["combined_json_sha256"]) != (
        "618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e"
    ):
        raise ValueError("H2 source JSON SHA-256 changed")
    if int(source["expected_restriction_runs"]) != 750:
        raise ValueError("H2 source restriction-run count changed")
    if int(source["expected_attempts_per_run"]) != 199:
        raise ValueError("H2 retained-attempt horizon changed")
    if int(source["expected_bootstrap_fit_failures"]) != 0:
        raise ValueError("H2 source fit-failure expectation changed")

    controller = config["frozen_controller"]
    if controller["controller_id"] != "F1B.R2.RESAMPLING_RISK_CONTROLLER.V1":
        raise ValueError("H2 controller identity changed")
    if controller["status"] != (
        "NON_AUTHORITATIVE_RESAMPLING_RISK_CONTROLLER_PROTOTYPE"
    ):
        raise ValueError("H2 controller status changed")
    if float(controller["alpha"]) != 0.05:
        raise ValueError("H2 alpha changed")
    if float(controller["epsilon"]) != 0.001:
        raise ValueError("H2 epsilon changed")
    if float(controller["halfspend"]) != 1000.0:
        raise ValueError("H2 halfspend changed")
    if str(controller["spending_sequence"]) != (
        "epsilon_n = epsilon * n / (halfspend + n)"
    ):
        raise ValueError("H2 spending sequence changed")
    if int(controller["replay_max_attempts"]) != 199:
        raise ValueError("H2 replay horizon changed")
    if float(controller["probability_tolerance"]) != 1e-12:
        raise ValueError("H2 probability tolerance changed")
    if controller["bootstrap_refit_failure_policy"] != (
        "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    ):
        raise ValueError("H2 refit-failure policy changed")
    if controller["boundary_initialization"] != {
        "n": 1,
        "upper": 2,
        "lower": -1,
    }:
        raise ValueError("H2 boundary initialization changed")
    if controller["decision_semantics"] != {
        "lower_boundary": "REJECT_P_LE_ALPHA",
        "upper_boundary": "NOT_REJECT_P_GT_ALPHA",
        "no_boundary": "SEQUENTIAL_UNRESOLVED",
    }:
        raise ValueError("H2 decision semantics changed")

    execution = config["h2_execution"]
    if execution["new_bootstrap_attempts_allowed"] is not False:
        raise ValueError("H2 cannot authorize new bootstrap attempts")
    if execution["source_attempts_reused_only"] is not True:
        raise ValueError("H2 must reuse retained source attempts only")
    if int(execution["maximum_attempts"]) != 199:
        raise ValueError("H2 maximum attempt count changed")
    if execution[
        "historical_stage_b_checkpoint_inheritance_allowed"
    ] is not False:
        raise ValueError("H2 cannot inherit historical Stage-B checkpoints")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("H2 interpretation boundary was weakened")


def validate_retained_h1_result(h1_result: dict, config: dict) -> None:
    if h1_result["lineage_id"] != config["source_lineage"]["lineage_id"]:
        raise ValueError("retained H1 lineage identity mismatch")
    if h1_result["status"] != (
        "NON_AUTHORITATIVE_H1_HOMOGENEOUS_PAIRED_SOURCE_QUALIFIED_RETAINED"
    ):
        raise ValueError("H2 requires retained qualified H1 source")
    if h1_result["authoritative"] is not False:
        raise ValueError("H1 result must remain non-authoritative")
    decision = h1_result["decision"]
    if decision["h1_full_homogeneous_source_generation_pass"] is not True:
        raise ValueError("H1 source generation did not pass")
    if decision["h1_independent_replay_qualification_pass"] is not True:
        raise ValueError("H1 replay qualification did not pass")
    if decision["homogeneous_source_accepted_for_h2_input"] is not True:
        raise ValueError("H1 source is not accepted for H2")
    if decision["historical_stage_b_may_be_inherited"] is not False:
        raise ValueError("H1 unexpectedly authorizes historical Stage-B inheritance")

    source = h1_result["combined_source"]
    expected = config["source_lineage"]
    if int(source["artifact_id"]) != int(expected["artifact_id"]):
        raise ValueError("H1 source artifact ID mismatch")
    if str(source["combined_json_sha256"]) != str(
        expected["combined_json_sha256"]
    ):
        raise ValueError("H1 source SHA-256 mismatch")
    if int(source["combined_json_size_bytes"]) != int(
        expected["combined_json_size_bytes"]
    ):
        raise ValueError("H1 source size mismatch")


def validate_frozen_controller(base: dict, config: dict) -> None:
    frozen = config["frozen_controller"]
    checks = {
        "controller_id": frozen["controller_id"],
        "status": frozen["status"],
        "alpha": frozen["alpha"],
        "epsilon": frozen["epsilon"],
        "halfspend": frozen["halfspend"],
        "spending_sequence": frozen["spending_sequence"],
        "replay_max_attempts": frozen["replay_max_attempts"],
        "probability_tolerance": frozen["probability_tolerance"],
        "bootstrap_refit_failure_policy": frozen[
            "bootstrap_refit_failure_policy"
        ],
        "boundary_initialization": frozen["boundary_initialization"],
        "decision_semantics": frozen["decision_semantics"],
    }
    for key, expected in checks.items():
        if base[key] != expected:
            raise ValueError(f"frozen controller field changed: {key}")

    boundary = base["execution_boundary"]
    if any(bool(value) for value in boundary.values()):
        raise ValueError("historical controller execution boundary changed")


def build_h2_effective_controller(base: dict, config: dict) -> dict:
    validate_frozen_controller(base, config)
    source = config["source_lineage"]
    effective = deepcopy(base)
    effective["replay_source"] = {
        "result_path": "ACTIONS_ARTIFACT:"
        + str(source["artifact_name"])
        + "/"
        + str(source["combined_json_name"]),
        "exact_artifact_id": int(source["artifact_id"]),
        "exact_json_sha256": str(source["combined_json_sha256"]),
        "exact_json_size_bytes": int(source["combined_json_size_bytes"]),
        "expected_restriction_runs": int(
            source["expected_restriction_runs"]
        ),
        "expected_attempts_per_run": int(
            source["expected_attempts_per_run"]
        ),
        "expected_bootstrap_fit_failures": int(
            source["expected_bootstrap_fit_failures"]
        ),
    }
    return effective
