from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_protocol_robustness_authoritative_2026-09-17.json"
)
PROVENANCE = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_protocol_robustness_authoritative_2026-09-17.provenance.json"
)
CHECKSUM = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_protocol_robustness_authoritative_2026-09-17.sha256"
)
SHARDS = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_protocol_robustness_authoritative_2026-09-17.shards.sha256"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_authoritative_phase_m_result_preserves_frozen_failure_surface() -> None:
    result = load(RESULT)
    rows = result["results"]

    assert result["benchmark_id"] == "BENCH.M1.E4.PROTOCOL_ROBUSTNESS.2026-09-17"
    assert result["phase"] == "M"
    assert result["status"] == "PROTOCOL_ROBUSTNESS_FAIL"
    assert result["formal_gate"] == 0.8
    assert result["replicates_per_cell"] == 200
    assert result["selected_cells_total"] == 18
    assert result["total_replicates"] == 3600
    assert len(rows) == 18
    assert len({row["cell_id"] for row in rows}) == 18
    assert len({row["seed"] for row in rows}) == 18

    for row in rows:
        assert sum(row["selected"].values()) == 200
        assert abs(
            row["recovery_probability"]
            + row["wrong_probability"]
            + row["inconclusive_probability"]
            - 1.0
        ) < 1e-12

    assert result["minimum_recovery_probability"] == 0.56
    assert set(result["formal_failed_cells"]) == {
        "COMBINED_ADVERSE__EVSD",
        "ITEM_HIGH__EVSD",
        "ITEM_MODERATE__EVSD",
    }
    assert set(result["secondary_wilson_failed_cells"]) == set(
        result["formal_failed_cells"]
    )

    by_id = {row["cell_id"]: row for row in rows}
    assert by_id["COMBINED_ADVERSE__EVSD"]["recovery_probability"] == 0.585
    assert by_id["ITEM_HIGH__EVSD"]["recovery_probability"] == 0.56
    assert by_id["ITEM_MODERATE__EVSD"]["recovery_probability"] == 0.78


def test_authoritative_phase_m_provenance_is_cross_artifact_consistent() -> None:
    result = load(RESULT)
    provenance = load(PROVENANCE)
    run = result["run_provenance"]

    assert provenance["authoritative_status"] == result["status"]
    assert provenance["benchmark_id"] == result["benchmark_id"]
    assert provenance["phase"] == result["phase"]
    assert provenance["replicates_per_cell"] == result["replicates_per_cell"]
    assert provenance["selected_cells_total"] == result["selected_cells_total"]
    assert provenance["total_replicates"] == result["total_replicates"]

    assert provenance["run_id"] == run["run_id"] == "35229760477"
    assert provenance["run_attempt"] == run["run_attempt"] == "1"
    assert provenance["event_name"] == run["event_name"] == "push"
    assert provenance["workflow"] == run["workflow"]
    assert provenance["contract_tooling_commit_sha"] == run["contract_tooling_commit_sha"]
    assert provenance["executed_commit_sha"] == run["executed_commit_sha"]
    assert provenance["repository"] == run["repository"]

    digest_line = CHECKSUM.read_text(encoding="utf-8").strip()
    digest, source = digest_line.split("  ", 1)
    source = source.split("  #", 1)[0]
    assert len(digest) == 64
    int(digest, 16)
    assert source == "phase-m-summary.json"
    assert result["source_aggregate_sha256"] == digest
    assert provenance["authoritative_source_aggregate_sha256"] == digest


def test_authoritative_phase_m_shard_manifest_is_complete_and_unique() -> None:
    result = load(RESULT)
    lines = [
        line.strip()
        for line in SHARDS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(lines) == 18

    paths = set()
    for line in lines:
        digest, path = line.split("  ", 1)
        assert len(digest) == 64
        int(digest, 16)
        assert path.startswith("collected/")
        assert path.endswith(".json")
        paths.add(path)

    assert len(paths) == 18
    expected_paths = {
        "collected/" + row["cell_id"].replace("__", "-") + ".json"
        for row in result["results"]
    }
    assert paths == expected_paths


def test_authoritative_phase_m_interpretation_boundary_remains_pre_human() -> None:
    result = load(RESULT)
    boundary = result["interpretation_boundary"].lower()
    active_variables = (ROOT / "model/variables.json").read_text(
        encoding="utf-8"
    ).lower()

    assert "synthetic stress gate" in boundary
    assert "does not select a human model" in boundary
    assert "authorize recruitment" in boundary
    assert '"pencode"' not in active_variables
    assert not (ROOT / "web").exists()
