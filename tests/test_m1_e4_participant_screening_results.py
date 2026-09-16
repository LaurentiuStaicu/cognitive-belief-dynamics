from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_screening_authoritative_2026-09-16.csv"
)
CHECKSUMS = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_screening_authoritative_2026-09-16.sha256"
)


def load_rows() -> list[dict[str, str]]:
    with RESULTS.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_authoritative_participant_screening_has_complete_frozen_grid():
    rows = load_rows()

    assert len(rows) == 72
    assert {row["allocation"] for row in rows} == {
        "P40_X16",
        "P64_X10",
        "P80_X8",
        "P128_X5",
    }
    assert {row["heterogeneity"] for row in rows} == {
        "low",
        "moderate",
        "high",
    }
    assert {row["generator"] for row in rows} == {"EVSD", "2HT"}
    assert {row["regime"] for row in rows} == {"weak", "medium", "strong"}

    keys = {
        (
            row["allocation"],
            row["heterogeneity"],
            row["generator"],
            row["regime"],
        )
        for row in rows
    }
    assert len(keys) == 72

    for row in rows:
        assert int(row["replicates"]) == 50
        assert (
            float(row["recovery_probability"])
            + float(row["wrong_probability"])
            + float(row["inconclusive_probability"])
        ) == 1.0
        assert row["passes_0_80"] == "True"


def test_screening_decision_surface_matches_phase_i_audit():
    rows = load_rows()

    assert min(float(row["recovery_probability"]) for row in rows) == 0.88
    assert max(float(row["wrong_probability"]) for row in rows) == 0.0

    expected_minimum = {
        "P40_X16": 0.94,
        "P64_X10": 0.96,
        "P80_X8": 0.90,
        "P128_X5": 0.88,
    }
    for allocation, expected in expected_minimum.items():
        actual = min(
            float(row["recovery_probability"])
            for row in rows
            if row["allocation"] == allocation
        )
        assert actual == expected

    limiting = [
        row
        for row in rows
        if float(row["recovery_probability"]) == 0.88
    ]
    assert len(limiting) == 1
    assert limiting[0]["allocation"] == "P128_X5"
    assert limiting[0]["heterogeneity"] == "low"
    assert limiting[0]["generator"] == "EVSD"
    assert limiting[0]["regime"] == "weak"


def test_screening_shard_checksum_manifest_is_complete():
    lines = [
        line.strip()
        for line in CHECKSUMS.read_text().splitlines()
        if line.strip()
    ]

    assert len(lines) == 12
    paths = set()
    for line in lines:
        digest, path = line.split("  ", 1)
        assert len(digest) == 64
        int(digest, 16)
        assert path.endswith("/result.json")
        paths.add(path)

    assert len(paths) == 12
