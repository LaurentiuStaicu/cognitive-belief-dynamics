from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_fresh_replicate_preflight as preflight,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_s4_fresh_replicate_preflight_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_repository_fresh_preflight_contract_is_frozen() -> None:
    config = load_config()
    preflight.validate_preflight_config(config)
    assert config["selection"]["expected_scientific_run_count"] == 18
    assert config["selection"]["expected_method_row_count"] == 72
    assert (
        config["selection"]["expected_scientific_run_ids_sha256"]
        == preflight.EXPECTED_RUN_DIGEST
    )
    assert (
        config["selection"]["expected_method_row_ids_sha256"]
        == preflight.EXPECTED_METHOD_DIGEST
    )


def test_preflight_rejects_equivalence_shortcut() -> None:
    config = deepcopy(load_config())
    config["prerequisite"][
        "preflight_execution_before_equivalence_retention"
    ] = True
    with pytest.raises(ValueError, match="cannot run before equivalence"):
        preflight.validate_preflight_config(config)


def test_preflight_rejects_run_digest_change() -> None:
    config = deepcopy(load_config())
    config["selection"]["expected_scientific_run_ids_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="run digest"):
        preflight.validate_preflight_config(config)


def test_preflight_rejects_terminal_state_change() -> None:
    config = deepcopy(load_config())
    config["execution_contract"]["allowed_terminal_states"].pop()
    with pytest.raises(ValueError, match="terminal-state"):
        preflight.validate_preflight_config(config)


def test_preflight_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["broad_execution_started"] = True
    with pytest.raises(ValueError, match="boundary"):
        preflight.validate_preflight_config(config)


def test_method_row_id_is_canonical() -> None:
    assert preflight.method_row_id("RUN", "POPULATION") == (
        "RUN|METHOD=POPULATION"
    )


def _synthetic_manifest() -> dict:
    rows: list[dict] = []

    for identity, restriction, role in (
        ("ADD_NULL", "ADD_RESTRICTION", "ADD_NULL_FALSE_REJECTION"),
        (
            "CBD_NULL_ANCHOR_1",
            "CBD_COMPLEMENT_RESTRICTION",
            "CBD_NULL_FALSE_REJECTION",
        ),
        (
            "CBD_NULL_ANCHOR_2",
            "CBD_COMPLEMENT_RESTRICTION",
            "CBD_NULL_FALSE_REJECTION",
        ),
    ):
        for missingness in (0.0, 0.15):
            rows.append(
                {
                    "scientific_run_id": (
                        f"NULL|{identity}|REPLICATE=20|"
                        f"RESTRICTION={restriction}|"
                        f"MISSINGNESS={missingness:.2f}"
                    ),
                    "identity": identity,
                    "identity_type": "NULL",
                    "restriction": restriction,
                    "role": role,
                    "sign": None,
                    "evaluation_replicate": 20,
                    "missingness": missingness,
                }
            )

    for role, restriction in (
        ("ADD_SPECIFICITY_NEGATIVE_CONTROL", "ADD_RESTRICTION"),
        ("ADD_DEPARTURE_DIAGNOSTIC", "ADD_RESTRICTION"),
        ("CBD_DEPARTURE_DETECTION", "CBD_COMPLEMENT_RESTRICTION"),
    ):
        for sign in (-1, 1):
            for missingness in (0.0, 0.15):
                rows.append(
                    {
                        "scientific_run_id": (
                            f"DEP|{role}|SIGN={sign}|REPLICATE=5|"
                            f"RESTRICTION={restriction}|"
                            f"MISSINGNESS={missingness:.2f}"
                        ),
                        "identity": f"{role}_{sign}",
                        "identity_type": "DEPARTURE",
                        "restriction": restriction,
                        "role": role,
                        "sign": sign,
                        "evaluation_replicate": 5,
                        "missingness": missingness,
                    }
                )

    return {
        "status": "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST",
        "scientific_run_count": 15000,
        "rows": rows,
    }


def test_selector_enforces_all_18_fresh_runs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = _synthetic_manifest()
    config = deepcopy(load_config())

    expected_rows = manifest["rows"]
    run_ids = [row["scientific_run_id"] for row in expected_rows]
    method_ids = [
        preflight.method_row_id(run_id, method)
        for run_id in run_ids
        for method in preflight.EXPECTED_METHODS
    ]
    run_digest = preflight.canonical_json_sha256(run_ids)
    method_digest = preflight.canonical_json_sha256(method_ids)

    monkeypatch.setattr(preflight, "EXPECTED_RUN_DIGEST", run_digest)
    monkeypatch.setattr(preflight, "EXPECTED_METHOD_DIGEST", method_digest)
    config["selection"]["expected_scientific_run_ids_sha256"] = run_digest
    config["selection"]["expected_method_row_ids_sha256"] = method_digest

    selected = preflight.select_fresh_preflight_rows(manifest, config)
    assert len(selected) == 18
    assert {row["role"] for row in selected} == set(
        preflight.EXPECTED_ROLES
    )
    assert {
        row["identity"]
        for row in selected
        if row["identity_type"] == "NULL"
    } == set(preflight.EXPECTED_NULL_IDENTITIES)
