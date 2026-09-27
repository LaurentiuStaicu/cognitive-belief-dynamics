from __future__ import annotations

import json
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r2_bootstrap_characterization import (
    run_bootstrap_characterization,
    wilson_interval,
)

ROOT = Path(__file__).resolve().parents[1]
FULL = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_bootstrap_characterization_design.json"
)
SMOKE = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_bootstrap_characterization_smoke.json"
)
DEPARTURES = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_full_design_keeps_bootstrap_and_evaluation_counts_non_authoritative() -> None:
    config = load(FULL)
    assert config["bootstrap"]["draw_grid"] == [49, 99, 199]
    assert config["evaluation_replicate_grid"] == [5, 10, 20]
    assert config["bootstrap"]["draw_grid_status"] == "DESIGN_SEARCH_NOT_AUTHORITATIVE"
    assert (
        config["evaluation_replicate_grid_status"]
        == "STAGED_DESIGN_SEARCH_NOT_AUTHORITATIVE"
    )
    assert config["execution_boundary"] == {
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_run_allowed": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_wilson_interval_is_bounded_and_orders_limits() -> None:
    low, high = wilson_interval(5, 10)
    assert 0.0 <= low <= 0.5 <= high <= 1.0
    assert wilson_interval(0, 0) == (0.0, 1.0)


def test_smoke_characterization_is_deterministic_and_keeps_failures_explicit() -> None:
    config = load(SMOKE)
    departures = load(DEPARTURES)
    first = run_bootstrap_characterization(config, departures)
    second = run_bootstrap_characterization(config, departures)
    assert first == second
    assert first["status"] == "SMOKE_NON_AUTHORITATIVE_R2_BOOTSTRAP_RESULT"
    assert first["authoritative"] is False
    assert first["departure_case_count"] == 1

    # 3 null tests + 1 departure tested against 2 restrictions
    assert first["trial_count"] == 5
    assert len(first["aggregate"]) == 5

    for row in first["aggregate"]:
        assert "fit_failure_count" in row
        assert "bootstrap_calibration_failure_count" in row


def test_standalone_accuracy_smoke_case_is_add_specificity_negative_control() -> None:
    result = run_bootstrap_characterization(load(SMOKE), load(DEPARTURES))
    rows = [
        row
        for row in result["trials"]
        if row["role"] == "ADD_SPECIFICITY_NEGATIVE_CONTROL"
    ]
    assert len(rows) == 1
    row = rows[0]
    assert row["axis"] == "STANDALONE_ACCURACY_MAIN_EFFECT"
    assert row["requested_cbd_rms_distance"] == 0.1
    # With only two bootstrap draws, plus-one p cannot be <= 0.05.
    if not row["fit_failure"] and not row["bootstrap_calibration_failure"]:
        assert row["rejected"] is False
