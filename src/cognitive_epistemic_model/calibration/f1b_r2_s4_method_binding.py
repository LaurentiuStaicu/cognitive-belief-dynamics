from __future__ import annotations

import json
import subprocess
from pathlib import Path


BINDING_ID = "F1B.R2.S4.METHOD_BINDING.V1"
STATUS = "NON_AUTHORITATIVE_S4_METHOD_BINDING_DESIGN"
EXPECTED_METHODS = (
    "POPULATION",
    "HIERARCHICAL_0.5X",
    "HIERARCHICAL_1X",
    "HIERARCHICAL_2X",
)


def validate_s4_method_binding_config(config: dict) -> None:
    if config["binding_id"] != BINDING_ID:
        raise ValueError("S4 method-binding identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 method-binding status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 method-binding issue changed")

    m2 = config["retained_m2"]
    if tuple(str(x) for x in m2["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("retained M2 eligible-method order/set changed")
    if m2["all_methods_m2_eligible"] is not True:
        raise ValueError("S4 binding requires all retained M2 methods eligible")
    if m2["hierarchical_scale_sensitivity_retained"] is not True:
        raise ValueError("M2 hierarchical scale sensitivity was dropped")
    if int(m2["scientific_run_count"]) != 840:
        raise ValueError("retained M2 scientific-run count changed")
    if int(m2["method_execution_count"]) != 3360:
        raise ValueError("retained M2 method-execution count changed")

    matrix = config["retained_s4_matrix"]
    if int(matrix["restriction_cell_count"]) != 75:
        raise ValueError("retained S4 restriction-cell count changed")
    if int(matrix["scientific_cell_missingness_count"]) != 150:
        raise ValueError("retained S4 stratum count changed")
    if int(matrix["scientific_run_count"]) != 15000:
        raise ValueError("retained S4 scientific-run count changed")
    if int(matrix["departure_run_count"]) != 14400:
        raise ValueError("retained S4 departure-run count changed")
    if int(matrix["null_run_count"]) != 600:
        raise ValueError("retained S4 null-run count changed")
    if matrix["missingness_run_counts"] != {"0.00": 7500, "0.15": 7500}:
        raise ValueError("retained S4 missingness counts changed")
    if tuple(int(x) for x in matrix["evaluation_replicate_indices"]) != tuple(
        range(100)
    ):
        raise ValueError("retained S4 evaluation-replicate identity changed")
    if int(matrix["replicates_per_stratum"]) != 100:
        raise ValueError("retained S4 replicate count changed")
    if float(matrix["maximum_worst_case_component_mcse"]) != 0.05:
        raise ValueError("retained S4 MCSE target changed")

    bound = config["bound_execution"]
    if tuple(str(x) for x in bound["method_order"]) != EXPECTED_METHODS:
        raise ValueError("bound S4 method order/set changed")
    if int(bound["method_count"]) != 4:
        raise ValueError("bound S4 method count changed")
    if int(bound["scientific_run_count"]) != 15000:
        raise ValueError("bound S4 scientific-run count changed")
    if int(bound["method_execution_count"]) != 60000:
        raise ValueError("bound S4 method-execution count changed")
    required_true = (
        "every_scientific_run_requires_every_method",
        "common_scientific_dataset_across_methods",
        "common_missingness_mask_across_methods",
        "hierarchical_common_random_numbers_across_scales",
        "population_method_namespace_distinct",
    )
    for key in required_true:
        if bound[key] is not True:
            raise ValueError(f"S4 binding invariant weakened: {key}")
    if bound["failed_method_run_pairs_replaced"] is not False:
        raise ValueError("failed S4 method/run pairs cannot be replaced")

    interpretation = config["interpretation"]
    if interpretation["method_selection_authorized"] is not False:
        raise ValueError("S4 binding cannot select a method")
    if interpretation["broad_characterization_authorized_after_binding_execution"] is not True:
        raise ValueError("S4 binding execution must authorize only broad characterization")
    if interpretation["power_validated"] is not False:
        raise ValueError("S4 binding cannot validate power")
    if interpretation["human_n_frozen"] is not False:
        raise ValueError("S4 binding cannot freeze human N")
    if interpretation["release_0_2_0_blocker_closed"] is not False:
        raise ValueError("S4 binding alone cannot close v0.2.0 blocker")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 method-binding boundary was weakened")


def _git_blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)],
        text=True,
    ).strip()


def validate_protected_files(config: dict, root: Path) -> None:
    for raw_path, expected in config["protected_file_git_blob_sha"].items():
        path = root / raw_path
        actual = _git_blob_sha(path)
        if actual != str(expected):
            raise ValueError(
                f"S4 protected file changed: {raw_path}: {actual} != {expected}"
            )


def validate_retained_results(
    m2_result: dict,
    s4_result: dict,
    config: dict,
) -> None:
    validate_s4_method_binding_config(config)

    if m2_result["status"] != (
        "NON_AUTHORITATIVE_PAIRED_METHOD_M2_COMPLETE_RETAINED"
    ):
        raise ValueError("retained M2 status changed")
    if m2_result["authoritative"] is not False:
        raise ValueError("retained M2 became authoritative")
    if m2_result["overall_decision"] != "M2_HAS_ELIGIBLE_METHODS":
        raise ValueError("retained M2 overall decision changed")
    if tuple(str(x) for x in m2_result["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("retained M2 eligible methods changed")
    if m2_result["interpretation"]["all_four_methods_m2_eligible"] is not True:
        raise ValueError("retained M2 all-method eligibility changed")
    if m2_result["interpretation"]["no_method_selected"] is not True:
        raise ValueError("retained M2 unexpectedly selected a method")
    if (
        m2_result["interpretation"]["hierarchical_scale_sensitivity_retained"]
        is not True
    ):
        raise ValueError("retained M2 scale sensitivity was dropped")
    if int(m2_result["matrix"]["scientific_run_count"]) != 840:
        raise ValueError("retained M2 scientific-run count mismatch")
    if int(m2_result["matrix"]["method_execution_count"]) != 3360:
        raise ValueError("retained M2 execution count mismatch")
    if any(int(row["refit_failure_count"]) != 0 for row in m2_result["method_results"]):
        raise ValueError("retained M2 unexpectedly contains refit failures")
    if any(row["decision_state"] != "M2_ELIGIBLE" for row in m2_result["method_results"]):
        raise ValueError("retained M2 method eligibility changed")

    matrix = config["retained_s4_matrix"]
    if s4_result["status"] != (
        "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_COMPLETE_RETAINED"
    ):
        raise ValueError("retained S4 matrix status changed")
    if s4_result["authoritative"] is not False:
        raise ValueError("retained S4 matrix became authoritative")
    actual = s4_result["matrix"]
    if int(actual["restriction_cell_count"]) != int(matrix["restriction_cell_count"]):
        raise ValueError("retained S4 restriction-cell mismatch")
    if int(actual["scientific_cell_missingness_count"]) != int(
        matrix["scientific_cell_missingness_count"]
    ):
        raise ValueError("retained S4 stratum mismatch")
    if int(actual["scientific_run_count"]) != int(matrix["scientific_run_count"]):
        raise ValueError("retained S4 scientific-run mismatch")
    if int(actual["departure_run_count"]) != int(matrix["departure_run_count"]):
        raise ValueError("retained S4 departure-run mismatch")
    if int(actual["null_run_count"]) != int(matrix["null_run_count"]):
        raise ValueError("retained S4 null-run mismatch")
    if actual["missingness_run_counts"] != matrix["missingness_run_counts"]:
        raise ValueError("retained S4 missingness mismatch")
    if str(actual["scientific_run_ids_sha256"]) != str(
        matrix["scientific_run_ids_sha256"]
    ):
        raise ValueError("retained S4 run-ID digest mismatch")
    if tuple(int(x) for x in actual["evaluation_replicate_indices"]) != tuple(
        range(100)
    ):
        raise ValueError("retained S4 evaluation-replicate mismatch")

    if s4_result["method_binding"]["m2_eligible_methods_bound"] is not False:
        raise ValueError("retained S4 matrix was already method-bound")
    if s4_result["method_binding"]["method_execution_started"] is not False:
        raise ValueError("retained S4 matrix unexpectedly started method execution")


def build_s4_bound_execution_manifest(
    m2_result: dict,
    s4_result: dict,
    config: dict,
) -> dict:
    validate_retained_results(m2_result, s4_result, config)
    methods = list(config["bound_execution"]["method_order"])
    scientific_run_count = int(
        config["bound_execution"]["scientific_run_count"]
    )
    method_execution_count = scientific_run_count * len(methods)
    if method_execution_count != 60000:
        raise ValueError("S4 bound execution count is not 60,000")

    return {
        "binding_id": config["binding_id"],
        "status": "NON_AUTHORITATIVE_S4_METHOD_BINDING_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "eligible_methods": methods,
        "method_count": len(methods),
        "scientific_run_count": scientific_run_count,
        "method_execution_count": method_execution_count,
        "scientific_run_ids_sha256": config["retained_s4_matrix"][
            "scientific_run_ids_sha256"
        ],
        "m2_combined_row_identity_sha256": config["retained_m2"][
            "combined_row_identity_sha256"
        ],
        "maximum_worst_case_component_mcse": float(
            config["retained_s4_matrix"][
                "maximum_worst_case_component_mcse"
            ]
        ),
        "hierarchical_scale_sensitivity_retained": True,
        "method_selected": False,
        "broad_characterization_authorized": True,
        "power_validated": False,
        "release_0_2_0_blocker_closed": False,
        "boundary": dict(config["boundary"]),
    }
