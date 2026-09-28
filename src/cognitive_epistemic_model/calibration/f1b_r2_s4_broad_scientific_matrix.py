from __future__ import annotations

from collections import Counter
from dataclasses import replace
import hashlib
import json
from typing import Any

from .f1b_r2_paired_method_m1_screen import (
    EXPECTED_ROLES,
    M1ScientificSpec,
    dataset_id_for,
    select_scientific_specs,
)


DESIGN_ID = "F1B.R2.S4.BROAD_SCIENTIFIC_MATRIX.V1"
STATUS = "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_DESIGN"


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_s4_matrix_config(config: dict) -> None:
    if config["design_id"] != DESIGN_ID:
        raise ValueError("S4 matrix design identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 matrix status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 matrix issue changed")

    design = config["scientific_design"]
    if tuple(design["departure_cell_fields"]) != (
        "role",
        "axis",
        "target_mean_bernoulli_kl",
        "sign",
        "anchor_id",
    ):
        raise ValueError("S4 departure-cell identity changed")
    if int(design["expected_departure_cell_count"]) != 72:
        raise ValueError("S4 departure-cell count changed")
    if tuple(str(x) for x in design["null_identities"]) != (
        "ADD_NULL",
        "CBD_NULL_ANCHOR_1",
        "CBD_NULL_ANCHOR_2",
    ):
        raise ValueError("S4 null identities changed")
    if int(design["expected_null_identity_count"]) != 3:
        raise ValueError("S4 null identity count changed")
    if int(design["expected_restriction_cell_count"]) != 75:
        raise ValueError("S4 restriction-cell count changed")
    if tuple(float(x) for x in design["missingness_regimes"]) != (
        0.0,
        0.15,
    ):
        raise ValueError("S4 missingness regimes changed")
    if tuple(int(x) for x in design["evaluation_replicate_indices"]) != (
        tuple(range(100))
    ):
        raise ValueError("S4 evaluation replicate identity changed")
    if int(design["replicates_per_cell_per_missingness"]) != 100:
        raise ValueError("S4 replicate count changed")
    if int(design["restriction_runs_per_missingness"]) != 7500:
        raise ValueError("S4 restriction runs/missingness changed")
    if int(design["departure_runs_total"]) != 14400:
        raise ValueError("S4 departure-run count changed")
    if int(design["null_runs_total"]) != 600:
        raise ValueError("S4 null-run count changed")
    if int(design["total_scientific_runs"]) != 15000:
        raise ValueError("S4 total scientific-run count changed")
    if tuple(int(x) for x in design["m1_departure_prefix_indices"]) != tuple(
        range(5)
    ):
        raise ValueError("S4 M1 departure prefix changed")
    if tuple(int(x) for x in design["m1_null_prefix_indices"]) != tuple(
        range(20)
    ):
        raise ValueError("S4 M1 null prefix changed")

    precision = config["precision"]
    if float(precision["maximum_worst_case_component_mcse"]) != 0.05:
        raise ValueError("S4 MCSE threshold changed")
    if float(precision["worst_case_component_variance"]) != 0.25:
        raise ValueError("S4 worst-case component variance changed")
    if int(precision["minimum_replicates_from_worst_case_mcse"]) != 100:
        raise ValueError("S4 precision-derived replicate count changed")
    if float(precision["worst_case_p"]) != 0.5:
        raise ValueError("S4 worst-case p changed")
    if (
        precision["interpretation"]
        != "MONTE_CARLO_PRECISION_THRESHOLD_NOT_POWER_TARGET"
    ):
        raise ValueError("S4 precision interpretation changed")

    method_binding = config["method_binding"]
    if (
        method_binding["source_stage"]
        != "M2_SEQUENTIAL_RESOLUTION_CHARACTERIZATION"
    ):
        raise ValueError("S4 method-binding stage changed")
    if method_binding["eligible_methods_known_at_this_gate"] is not False:
        raise ValueError("S4 matrix gate cannot preselect methods")
    if (
        method_binding["broad_methods_must_equal_retained_m2_eligible_methods"]
        is not True
    ):
        raise ValueError("S4 method binding was weakened")
    if method_binding["method_selection_by_this_gate"] is not False:
        raise ValueError("S4 matrix gate cannot select a method")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 scientific boundary was weakened")


def select_s4_scientific_specs(
    h1_source: dict,
    m1_config: dict,
    s4_config: dict,
) -> list[M1ScientificSpec]:
    validate_s4_matrix_config(s4_config)
    m1_specs = select_scientific_specs(h1_source, m1_config)
    if len(m1_specs) != 75:
        raise ValueError("S4 source does not contain 75 M1 scientific cells")

    broad_specs = [
        replace(spec, replicate_count=100)
        for spec in m1_specs
    ]
    departure = [spec for spec in broad_specs if spec.identity_type == "DEPARTURE"]
    nulls = [spec for spec in broad_specs if spec.identity_type == "NULL"]
    if len(departure) != 72:
        raise ValueError("S4 source departure-cell count changed")
    if len(nulls) != 3:
        raise ValueError("S4 source null-cell count changed")
    if {spec.role for spec in broad_specs} != EXPECTED_ROLES:
        raise ValueError("S4 source role coverage changed")
    if {spec.identity for spec in nulls} != set(
        str(x) for x in s4_config["scientific_design"]["null_identities"]
    ):
        raise ValueError("S4 source null identity coverage changed")
    return broad_specs


def scientific_run_id(
    spec: M1ScientificSpec,
    replicate: int,
    missingness: float,
) -> str:
    dataset_id = dataset_id_for(spec, replicate)
    return (
        f"{dataset_id}|RESTRICTION={spec.restriction}"
        f"|MISSINGNESS={float(missingness):.2f}"
    )


def build_s4_scientific_manifest(
    h1_source: dict,
    m1_config: dict,
    s4_config: dict,
) -> dict:
    specs = select_s4_scientific_specs(
        h1_source,
        m1_config,
        s4_config,
    )
    missingness_regimes = tuple(
        float(x)
        for x in s4_config["scientific_design"]["missingness_regimes"]
    )

    rows: list[dict] = []
    for spec in specs:
        for replicate in range(100):
            dataset_id = dataset_id_for(spec, replicate)
            for missingness in missingness_regimes:
                rows.append(
                    {
                        "scientific_run_id": scientific_run_id(
                            spec,
                            replicate,
                            missingness,
                        ),
                        "dataset_id": dataset_id,
                        "template_run_id": spec.template_run_id,
                        "identity": spec.identity,
                        "identity_type": spec.identity_type,
                        "restriction": spec.restriction,
                        "role": spec.role,
                        "anchor_id": spec.anchor_id,
                        "axis": spec.axis,
                        "sign": spec.sign,
                        "target_mean_bernoulli_kl": (
                            spec.target_mean_bernoulli_kl
                        ),
                        "evaluation_replicate": replicate,
                        "missingness": missingness,
                    }
                )

    ids = [str(row["scientific_run_id"]) for row in rows]
    if len(ids) != 15000 or len(set(ids)) != 15000:
        raise ValueError("S4 scientific-run identities are not exactly unique")

    identity_counts = Counter(row["identity_type"] for row in rows)
    if identity_counts != Counter({"DEPARTURE": 14400, "NULL": 600}):
        raise ValueError("S4 departure/null run counts changed")

    missingness_counts = Counter(float(row["missingness"]) for row in rows)
    if missingness_counts != Counter({0.0: 7500, 0.15: 7500}):
        raise ValueError("S4 missingness run counts changed")

    cell_counts: Counter[tuple[Any, ...]] = Counter()
    for row in rows:
        if row["identity_type"] == "NULL":
            cell = (
                "NULL",
                row["identity"],
                row["restriction"],
                float(row["missingness"]),
            )
        else:
            cell = (
                "DEPARTURE",
                row["role"],
                row["axis"],
                row["target_mean_bernoulli_kl"],
                row["sign"],
                row["anchor_id"],
                row["restriction"],
                float(row["missingness"]),
            )
        cell_counts[cell] += 1

    if len(cell_counts) != 150:
        raise ValueError("S4 scientific cell × missingness count changed")
    if set(cell_counts.values()) != {100}:
        raise ValueError("S4 cell replication is not exactly 100")

    return {
        "design_id": s4_config["design_id"],
        "status": "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST",
        "authoritative": False,
        "issue": int(s4_config["issue"]),
        "restriction_cell_count": len(specs),
        "scientific_cell_missingness_count": len(cell_counts),
        "scientific_run_count": len(rows),
        "departure_run_count": identity_counts["DEPARTURE"],
        "null_run_count": identity_counts["NULL"],
        "missingness_run_counts": {
            f"{key:.2f}": value
            for key, value in sorted(missingness_counts.items())
        },
        "scientific_run_ids_sha256": canonical_json_sha256(sorted(ids)),
        "rows": rows,
        "boundary": dict(s4_config["boundary"]),
    }
