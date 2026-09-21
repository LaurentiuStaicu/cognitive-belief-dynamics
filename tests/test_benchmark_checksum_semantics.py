from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "model" / "benchmarks" / "results"
SEMANTICS = RESULTS / "checksum_semantics.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        digest, target = line.split("  ", 1)
        target = target.split("  #", 1)[0]
        assert len(digest) == 64
        int(digest, 16)
        rows.append((digest, target))
    return rows


def test_checksum_semantics_cover_all_primary_retained_manifests() -> None:
    data = load(SEMANTICS)
    assert data["schema_version"] == 1
    entries = data["entries"]
    assert {entry["phase"] for entry in entries} == {"F", "G", "I", "K", "M"}

    expected = {
        str(path.relative_to(ROOT))
        for path in RESULTS.glob("m1_e4_*authoritative*.sha256")
        if not path.name.endswith(".shards.sha256")
    }
    assert {entry["checksum_file"] for entry in entries} == expected


def test_phase_f_and_g_checksums_are_explicitly_historical_json_digests() -> None:
    entries = {entry["phase"]: entry for entry in load(SEMANTICS)["entries"]}
    expected = {
        "F": (
            "c8aad7d5fcab17ddc114b0a0e1776e576e30056e21f0307fbb0a32722128cea7",
            "m1_e4_candidate_recovery_authoritative.json",
        ),
        "G": (
            "80635b2e44eb0991fe8db446c163a0a2c3ff9dbab8396342098bdba6f72694b4",
            "m1_e4_trial_count_refinement_authoritative.json",
        ),
    }
    for phase, pair in expected.items():
        entry = entries[phase]
        rows = parse_manifest(ROOT / entry["checksum_file"])
        assert rows == [pair]
        assert entry["hashed_target_kind"] == "HISTORICAL_AUTHORITATIVE_AGGREGATE_JSON"
        assert entry["hashed_target_present_in_checkout"] is False
        assert entry["retained_result"].endswith(".csv")


def test_phase_i_checksum_is_a_twelve_shard_historical_manifest() -> None:
    entry = next(item for item in load(SEMANTICS)["entries"] if item["phase"] == "I")
    rows = parse_manifest(ROOT / entry["checksum_file"])
    assert entry["hashed_target_kind"] == "HISTORICAL_SHARD_RESULT_JSON_SET"
    assert entry["hashed_target_present_in_checkout"] is False
    assert entry["expected_target_count"] == len(rows) == 12
    assert len({target for _, target in rows}) == 12
    assert all(target.startswith("screen-") and target.endswith("/result.json") for _, target in rows)


def test_phase_k_checksum_recomputes_from_retained_authoritative_json() -> None:
    entry = next(item for item in load(SEMANTICS)["entries"] if item["phase"] == "K")
    rows = parse_manifest(ROOT / entry["checksum_file"])
    assert len(rows) == 1
    digest, target = rows[0]
    retained = ROOT / entry["retained_result"]
    assert entry["hashed_target_present_in_checkout"] is True
    assert target == entry["hashed_target"] == entry["retained_result"]
    assert sha256(retained) == digest


def test_phase_m_checksum_is_source_aggregate_not_retained_json_hash() -> None:
    entry = next(item for item in load(SEMANTICS)["entries"] if item["phase"] == "M")
    rows = parse_manifest(ROOT / entry["checksum_file"])
    assert len(rows) == 1
    digest, target = rows[0]
    result = load(ROOT / entry["retained_result"])
    provenance = load(RESULTS / "m1_e4_protocol_robustness_authoritative_2026-09-17.provenance.json")

    assert target == entry["hashed_target"] == "phase-m-summary.json"
    assert entry["hashed_target_present_in_checkout"] is False
    assert entry["hashed_target_kind"] == "HISTORICAL_ACTIONS_SOURCE_AGGREGATE_JSON"
    assert result["source_aggregate_sha256"] == digest
    assert provenance["authoritative_source_aggregate_sha256"] == digest
    assert sha256(ROOT / entry["retained_result"]) != digest
