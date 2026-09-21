from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_confirmation_authoritative_2026-09-16.json"
)
PROVENANCE = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_confirmation_authoritative_2026-09-16.provenance.json"
)
CHECKSUM = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_confirmation_authoritative_2026-09-16.sha256"
)
SHARD_CHECKSUMS = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_confirmation_authoritative_2026-09-16.shards.sha256"
)


def load_result() -> dict:
    return json.loads(RESULTS.read_text())


def test_authoritative_confirmation_has_complete_frozen_surface():
    result = load_result()
    rows = result["results"]

    assert result["selected_cells_total"] == 29
    assert result["primary_cells"] == 18
    assert result["boundary_cells"] == 11
    assert result["replicates_per_cell"] == 200
    assert len(rows) == 29
    assert len({row["cell_id"] for row in rows}) == 29

    primary = [row for row in rows if row["role"] == "PRIMARY_P64_FULL_GRID"]
    boundary = [
        row for row in rows
        if row["role"] == "BOUNDARY_MINIMUM_WITH_TIES"
    ]
    assert len(primary) == 18
    assert len(boundary) == 11
    assert {row["allocation"] for row in primary} == {"P64_X10"}

    for row in rows:
        assert row["replicates"] == 200
        assert sum(row["selected"].values()) == 200
        assert np.isclose(
            row["recovery_probability"]
            + row["wrong_probability"]
            + row["inconclusive_probability"],
            1.0,
        )


def test_authoritative_primary_gate_and_wilson_sensitivity_pass():
    result = load_result()
    primary = [
        row for row in result["results"]
        if row["role"] == "PRIMARY_P64_FULL_GRID"
    ]

    assert result["primary_all_formal_gate_pass"] is True
    assert result["primary_all_secondary_wilson_margin_pass"] is True
    assert result["primary_minimum_recovery"] == 0.92
    assert min(row["wilson_lower"] for row in primary) == 0.874010511732856

    limiting = [
        row
        for row in primary
        if row["recovery_probability"] == 0.92
    ]
    assert len(limiting) == 1
    row = limiting[0]
    assert row["cell_id"] == "P64_X10__low__EVSD__weak"
    assert row["selected"] == {"2HT": 1, "EVSD": 184, "INCONCLUSIVE": 15}


def test_authoritative_boundary_and_confusion_summary_matches_audit():
    result = load_result()
    rows = result["results"]

    assert result["boundary_minimum_recovery"] == 0.885
    assert result["wrong_family_selections_total"] == 3
    assert result["inconclusive_total"] == 135

    wrong_cells = {
        row["cell_id"]
        for row in rows
        if row["wrong_probability"] > 0
    }
    assert wrong_cells == {
        "P40_X16__low__EVSD__weak",
        "P64_X10__low__EVSD__weak",
        "P128_X5__low__EVSD__weak",
    }


def test_authoritative_confirmation_provenance_and_hash_manifests():
    provenance = json.loads(PROVENANCE.read_text())
    assert provenance["github_run_id"] == "35081097627"
    assert (
        provenance["source_phase_j_main_sha"]
        == "76aca60beb49a4e2ce5d96abaa564a67282ba811"
    )
    assert (
        provenance["workflow_source_sha"]
        == "faa8b4223960bb60dfa10654a7107d4158021f7f"
    )

    checksum_line = CHECKSUM.read_text().strip()
    digest, path = checksum_line.split("  ", 1)
    assert digest == "88c16c2143e7131a4ec8915dbb726ece7e859a797162df173b89743837335f89"
    assert path.endswith(
        "m1_e4_participant_confirmation_authoritative_2026-09-16.json"
    )

    shard_lines = [
        line.strip()
        for line in SHARD_CHECKSUMS.read_text().splitlines()
        if line.strip()
    ]
    assert len(shard_lines) == 29
    for line in shard_lines:
        shard_digest, shard_path = line.split("  ", 1)
        assert len(shard_digest) == 64
        int(shard_digest, 16)
        assert shard_path.endswith("/result.json")


def test_confirmation_result_preserves_scientific_boundary():
    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    active_variables = (ROOT / "model/variables.json").read_text().lower()

    assert snapshot["model_specification"] == "M1"
    release_manifest = json.loads((ROOT / "releases/v0.1.1.manifest.json").read_text())
    evidence_revision = release_manifest["evidence_metadata_revision"]
    assert evidence_revision["prior_snapshot"] == "EVIDENCE.M1.2026-09-16.r1"
    assert evidence_revision["release_snapshot"] == snapshot["id"]
    assert evidence_revision["evidence_set_changed"] is False
    assert evidence_revision["metadata_corrected_or_qualified"] is True
    assert '"pencode"' not in active_variables
    assert not (ROOT / "web").exists()
