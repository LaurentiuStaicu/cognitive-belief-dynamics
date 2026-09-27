from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_bootstrap_calibration_pilot_non_authoritative_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def by_role(result: dict) -> dict[str, dict]:
    return {row["role"]: row for row in result["aggregate"]}


def test_retained_pilot_has_exact_provenance_and_non_authoritative_status() -> None:
    result = load()
    assert result["status"] == "NON_AUTHORITATIVE_R2_BOOTSTRAP_CHARACTERIZATION_RESULT"
    assert result["authoritative"] is False
    assert result["draw_grid"] == [49]
    assert result["evaluation_replicate_grid"] == [5]
    assert result["trial_count"] == 25
    assert result["departure_case_count"] == 1
    assert result["provenance"]["source_commit"] == (
        "41646ae89e000423c01f9d4d3221f9adefa7b19a"
    )
    assert result["provenance"]["config_sha256"] == (
        "35c84547c8de98b969f1d206a29de43bf925a771af995ebdfbc3534feaa9245c"
    )
    assert result["provenance"]["departure_config_sha256"] == (
        "e5603e0115d98abbb2df549671592fda14818abb5e990a0b5afad8641e5a2a1e"
    )
    assert result["execution_context"]["github_run_id"] == "36299032582"
    assert result["execution_context"]["temporary_workflow_not_for_merge"] is True


def test_pilot_has_no_fit_or_calibration_failures() -> None:
    result = load()
    assert all(row["fit_failure_count"] == 0 for row in result["aggregate"])
    assert all(
        row["bootstrap_calibration_failure_count"] == 0
        for row in result["aggregate"]
    )
    assert all(row["bootstrap_fit_failures"] == 0 for row in result["trials"])
    assert all(row["bootstrap_draws_successful"] == 49 for row in result["trials"])


def test_pilot_retains_prefrozen_null_and_departure_outcomes() -> None:
    result = load()
    roles = by_role(result)

    cbd_nulls = sorted(
        (
            row
            for row in result["aggregate"]
            if row["role"] == "CBD_NULL_FALSE_REJECTION"
        ),
        key=lambda row: row["anchor_id"],
    )
    assert [(row["anchor_id"], row["rejections"]) for row in cbd_nulls] == [
        ("CBD_ANCHOR_1", 1),
        ("CBD_ANCHOR_2", 0),
    ]
    assert roles["ADD_NULL_FALSE_REJECTION"]["rejections"] == 0
    assert roles["CBD_DEPARTURE_DETECTION"]["rejections"] == 5
    assert roles["ADD_SPECIFICITY_NEGATIVE_CONTROL"]["rejections"] == 1


def test_pilot_cannot_freeze_calibration_or_power() -> None:
    result = load()
    assert "Draw counts and evaluation replicates remain design-search values" in (
        result["interpretation_boundary"]
    )
    assert result["aggregate"][0]["evaluation_replicates"] == 5
