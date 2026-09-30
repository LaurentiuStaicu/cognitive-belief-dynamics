from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_all_new_wave as wave


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r2_s4_w1_execution_v1.json"
W2_CONFIG = (
    ROOT / "model" / "benchmarks" / "f1b_r2_s4_w2_execution_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def load_w2_config() -> dict:
    return json.loads(W2_CONFIG.read_text(encoding="utf-8"))


def test_repository_w1_contract_is_frozen() -> None:
    config = load_config()
    wave.validate_all_new_wave_config(config)
    assert config["wave"]["wave_id"] == "W1"
    assert config["wave"]["replicate_start"] == 25
    assert config["wave"]["replicate_end"] == 49
    assert config["wave"]["scientific_run_count"] == 3750
    assert config["wave"]["method_row_count"] == 15000
    assert config["wave"]["imported_method_row_count"] == 0
    assert config["wave"]["new_method_execution_count"] == 15000
    assert config["wave"]["shard_plan_sha256"] == (
        "36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175"
    )
    assert config["preflight"]["shard_index"] == 11
    assert config["authorization"]["preflight_retained"] is True
    assert config["authorization"]["full_wave_execution_authorized"] is True
    assert config["retained_sources"]["preflight_result"]["git_blob_sha"] == (
        "4dc28d64ef81c2070467dc197064e9b4f37173e7"
    )


def test_w1_rejects_w0_membership() -> None:
    config = deepcopy(load_config())
    config["wave"]["wave_id"] = "W0"
    with pytest.raises(ValueError, match="unsupported"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_premature_w2_relabel() -> None:
    config = deepcopy(load_config())
    config["wave"].update(
        {
            "wave_id": "W2",
            "predecessor_wave_id": "W1",
            "replicate_start": 50,
            "replicate_end": 74,
            "scientific_run_ids_sha256": (
                "a24dea39afdb03b91784248755d9ddad94466bbab8391044308eeeb8c9eff617"
            ),
            "method_row_ids_sha256": (
                "a338bd644ee62a474cf417aa0396a0ff2df4a310618e63ffb644c8f5f3cc8ba2"
            ),
            "shard_plan_sha256": (
                "399b4feecc51731f4691ca7168eb61625834cc1dc74e2fb66d3f6fe23ffe2475"
            ),
        }
    )
    config["shards"]["minimum_scientific_runs_per_shard"] = 6
    config["retained_sources"]["predecessor_result"]["wave_id"] = "W1"
    with pytest.raises(ValueError, match="predecessor status"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_imported_rows() -> None:
    config = deepcopy(load_config())
    config["wave"]["imported_method_row_count"] = 4
    with pytest.raises(ValueError, match="cannot import"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_method_change() -> None:
    config = deepcopy(load_config())
    config["methods"].pop()
    with pytest.raises(ValueError, match="method order/set"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_parallelism_change() -> None:
    config = deepcopy(load_config())
    config["shards"]["max_parallel"] = 21
    with pytest.raises(ValueError, match="max-parallel"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_early_interpretation() -> None:
    config = deepcopy(load_config())
    config["execution"]["scientific_interpretation_after_wave"] = True
    with pytest.raises(ValueError, match="interpretation"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_lost_preflight_retention() -> None:
    config = deepcopy(load_config())
    config["authorization"]["preflight_retained"] = False
    with pytest.raises(ValueError, match="authorization must match"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_full_wave_deauthorization_mismatch() -> None:
    config = deepcopy(load_config())
    config["authorization"]["full_wave_execution_authorized"] = False
    with pytest.raises(ValueError, match="authorization must match"):
        wave.validate_all_new_wave_config(config)


def test_w1_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        wave.validate_all_new_wave_config(config)


def test_repository_w2_contract_is_frozen() -> None:
    config = load_w2_config()
    wave.validate_all_new_wave_config(config)
    assert config["wave"]["wave_id"] == "W2"
    assert config["wave"]["predecessor_wave_id"] == "W1"
    assert config["wave"]["replicate_start"] == 50
    assert config["wave"]["replicate_end"] == 74
    assert config["wave"]["scientific_run_count"] == 3750
    assert config["wave"]["method_row_count"] == 15000
    assert config["wave"]["imported_method_row_count"] == 0
    assert config["wave"]["scientific_run_ids_sha256"] == (
        "a24dea39afdb03b91784248755d9ddad94466bbab8391044308eeeb8c9eff617"
    )
    assert config["wave"]["method_row_ids_sha256"] == (
        "a338bd644ee62a474cf417aa0396a0ff2df4a310618e63ffb644c8f5f3cc8ba2"
    )
    assert config["wave"]["shard_plan_sha256"] == (
        "399b4feecc51731f4691ca7168eb61625834cc1dc74e2fb66d3f6fe23ffe2475"
    )
    assert config["shards"]["minimum_scientific_runs_per_shard"] == 6
    assert config["shards"]["maximum_scientific_runs_per_shard"] == 27
    predecessor = config["retained_sources"]["predecessor_result"]
    assert predecessor["path"] == (
        "model/results/f1b_r2_s4_w1_combined_2026-09-30.json"
    )
    assert predecessor["git_blob_sha"] == (
        "7302806c2630b8d24a84f20885a543274badcd33"
    )
    assert predecessor["required_status"] == (
        "NON_AUTHORITATIVE_S4_W1_COMBINED_COMPLETE_RETAINED"
    )
    retained_path = ROOT / predecessor["path"]
    retained_bytes = retained_path.read_bytes()
    git_blob = hashlib.sha1(
        f"blob {len(retained_bytes)}\\0".encode("ascii") + retained_bytes
    ).hexdigest()
    assert git_blob == predecessor["git_blob_sha"]
    assert "preflight" not in config
    assert "preflight_result" not in config["retained_sources"]
    assert config["authorization"]["full_wave_requires_preflight_retention"] is False
    assert config["authorization"]["preflight_retained"] is False
    assert config["authorization"]["full_wave_execution_authorized"] is True
    assert config["authorization"]["w2_authorized"] is True
    assert config["authorization"]["w3_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "path",
            "model/results/wrong.json",
            "predecessor path",
        ),
        (
            "git_blob_sha",
            "0" * 40,
            "predecessor blob",
        ),
        (
            "required_status",
            "WRONG_STATUS",
            "predecessor status",
        ),
    ],
)
def test_w2_rejects_wrong_retained_predecessor(
    field: str,
    value: str,
    message: str,
) -> None:
    config = deepcopy(load_w2_config())
    config["retained_sources"]["predecessor_result"][field] = value
    with pytest.raises(ValueError, match=message):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_missing_retained_predecessor() -> None:
    config = deepcopy(load_w2_config())
    del config["retained_sources"]["predecessor_result"]
    with pytest.raises(ValueError, match="predecessor is missing"):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_w1_style_preflight_dependency() -> None:
    config = deepcopy(load_w2_config())
    config["preflight"] = {"shard_index": 11}
    with pytest.raises(ValueError, match="must not depend"):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_imported_rows() -> None:
    config = deepcopy(load_w2_config())
    config["wave"]["imported_method_row_count"] = 4
    with pytest.raises(ValueError, match="cannot import"):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_replicate_or_identity_change() -> None:
    config = deepcopy(load_w2_config())
    config["wave"]["replicate_start"] = 49
    with pytest.raises(ValueError, match="replicate_start"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["wave"]["scientific_run_ids_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="scientific identity"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["wave"]["method_row_ids_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="method identity"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["wave"]["shard_plan_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="shard-plan identity"):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_shard_or_method_change() -> None:
    config = deepcopy(load_w2_config())
    config["shards"]["minimum_scientific_runs_per_shard"] = 5
    with pytest.raises(ValueError, match="shard range"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["methods"].reverse()
    with pytest.raises(ValueError, match="method order/set"):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_executor_or_numerical_lineage_change() -> None:
    config = deepcopy(load_w2_config())
    config["execution"]["shared_broad_executor_git_blob_sha"] = "0" * 40
    with pytest.raises(ValueError, match="executor blob"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["execution"]["numerical_lineage"] = "Generic"
    with pytest.raises(ValueError, match="numerical lineage"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["execution"]["sequential_prefix_attempts"] = 200
    with pytest.raises(ValueError, match="prefix length"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["execution"]["sequential_max_total_attempts"] = 9999
    with pytest.raises(ValueError, match="sequential cap"):
        wave.validate_all_new_wave_config(config)


def test_w2_rejects_early_w3_or_scientific_gate() -> None:
    config = deepcopy(load_w2_config())
    config["authorization"]["w3_authorized"] = True
    with pytest.raises(ValueError, match="cannot authorize W3"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        wave.validate_all_new_wave_config(config)

    config = deepcopy(load_w2_config())
    config["execution"]["scientific_interpretation_after_wave"] = True
    with pytest.raises(ValueError, match="interpretation"):
        wave.validate_all_new_wave_config(config)


def test_w2_plan_builder_has_no_w1_preflight_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = deepcopy(load_w2_config())
    rows = [
        {
            "scientific_run_id": (
                f"S4-W2-SYNTHETIC-R{replicate:02d}-CELL={cell:03d}"
            ),
            "evaluation_replicate": replicate,
        }
        for replicate in range(100)
        for cell in range(150)
    ]
    run_ids = sorted(
        str(row["scientific_run_id"])
        for row in rows
        if 50 <= int(row["evaluation_replicate"]) <= 74
    )
    method_ids = sorted(
        wave.method_row_id(run_id, method)
        for run_id in run_ids
        for method in wave.EXPECTED_METHODS_M2
    )
    shard_plan = []
    for shard_index in range(250):
        local = sorted(
            run_id
            for run_id in run_ids
            if wave.stable_shard(run_id, 250) == shard_index
        )
        assert local
        shard_plan.append(
            {
                "shard_index": shard_index,
                "scientific_run_count": len(local),
                "imported_scientific_run_count": 0,
                "new_scientific_run_count": len(local),
                "imported_method_row_count": 0,
                "new_method_execution_count": len(local) * 4,
            }
        )

    run_digest = wave.canonical_json_sha256(run_ids)
    method_digest = wave.canonical_json_sha256(method_ids)
    shard_digest = wave.canonical_json_sha256(shard_plan)
    counts = [row["scientific_run_count"] for row in shard_plan]

    expected = deepcopy(wave.EXPECTED_WAVES["W2"])
    expected["scientific_run_ids_sha256"] = run_digest
    expected["method_row_ids_sha256"] = method_digest
    expected["shard_plan_sha256"] = shard_digest
    expected["shard_range"] = (min(counts), max(counts))
    monkeypatch.setitem(wave.EXPECTED_WAVES, "W2", expected)

    config["wave"]["scientific_run_ids_sha256"] = run_digest
    config["wave"]["method_row_ids_sha256"] = method_digest
    config["wave"]["shard_plan_sha256"] = shard_digest
    config["shards"]["minimum_scientific_runs_per_shard"] = min(counts)
    config["shards"]["maximum_scientific_runs_per_shard"] = max(counts)

    manifest = {
        "status": "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST",
        "scientific_run_count": 15000,
        "rows": rows,
    }
    plan = wave.build_all_new_wave_plan(manifest, config)
    assert plan["wave_id"] == "W2"
    assert plan["scientific_run_count"] == 3750
    assert plan["method_row_count"] == 15000
    assert plan["shard_count"] == 250
    assert len(plan["shard_plan"]) == 250
    assert "preflight_shard_index" not in plan
    assert "preflight_retained" not in plan
    assert plan["full_wave_execution_authorized"] is True
