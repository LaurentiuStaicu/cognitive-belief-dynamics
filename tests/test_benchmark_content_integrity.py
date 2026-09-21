from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "model" / "benchmarks" / "results"
BENCH = ROOT / "model" / "benchmarks"


def read_csv(name: str) -> list[dict[str, str]]:
    with (RESULTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def probability_close(value: float, expected: float, tol: float = 1e-12) -> bool:
    return math.isclose(value, expected, rel_tol=0.0, abs_tol=tol)


def test_core_and_refinement_csvs_are_numerically_self_consistent() -> None:
    cases = [
        ("m1_e4_candidate_recovery_authoritative_2026-09-16.csv", 24, {40, 80, 160, 320}),
        ("m1_e4_trial_count_refinement_authoritative_2026-09-16.csv", 18, {480, 640, 960}),
    ]
    for name, expected_rows, expected_trials in cases:
        rows = read_csv(name)
        assert len(rows) == expected_rows
        assert {int(row["n_target"]) for row in rows} == expected_trials
        assert {int(row["n_foil"]) for row in rows} == expected_trials
        assert {int(row["replicates"]) for row in rows} == {200}
        for row in rows:
            recovery = float(row["recovery_probability"])
            wrong = float(row["wrong_probability"])
            inconclusive = float(row["inconclusive_probability"])
            assert probability_close(recovery + wrong + inconclusive, 1.0)
            assert (row["passes_0_80"].lower() == "true") is (recovery >= 0.8)


def test_trial_count_refinement_changes_only_the_registered_axis() -> None:
    core = json.loads((BENCH / "m1_e4_candidate_recovery_core.json").read_text())
    refine = json.loads((BENCH / "m1_e4_candidate_recovery_trial_count_refinement.json").read_text())
    for key in refine["controlled_change"]["unchanged_axes"]:
        assert refine[key] == core[key]
    assert refine["controlled_change"]["changed_axis_only"] == "trial_counts_per_operating_point"
    assert refine["trial_counts_per_operating_point"] == [480, 640, 960]
    assert core["trial_counts_per_operating_point"] == [40, 80, 160, 320]


def test_screening_surface_is_complete_and_self_consistent() -> None:
    rows = read_csv("m1_e4_participant_screening_authoritative_2026-09-16.csv")
    assert len(rows) == 72
    assert {row["allocation"] for row in rows} == {"P40_X16", "P64_X10", "P80_X8", "P128_X5"}
    assert {row["heterogeneity"] for row in rows} == {"low", "moderate", "high"}
    assert {row["generator"] for row in rows} == {"EVSD", "2HT"}
    assert {row["regime"] for row in rows} == {"weak", "medium", "strong"}
    assert {int(row["replicates"]) for row in rows} == {50}
    for row in rows:
        recovery = float(row["recovery_probability"])
        wrong = float(row["wrong_probability"])
        inconclusive = float(row["inconclusive_probability"])
        assert probability_close(recovery + wrong + inconclusive, 1.0)
        assert (row["passes_0_80"].lower() == "true") is (recovery >= 0.8)


def test_confirmation_selection_is_exactly_derived_from_screening_surface() -> None:
    rows = read_csv("m1_e4_participant_screening_authoritative_2026-09-16.csv")
    screening = {
        f'{row["allocation"]}__{row["heterogeneity"]}__{row["generator"]}__{row["regime"]}':
        float(row["recovery_probability"])
        for row in rows
    }
    config = json.loads((BENCH / "m1_e4_participant_confirmation_200.json").read_text())
    assert len(config["selected_cells"]) == config["selection_policy"]["selected_cells_total"] == 29
    assert sum(cell["role"] == "PRIMARY_P64_FULL_GRID" for cell in config["selected_cells"]) == 18
    for cell in config["selected_cells"]:
        assert cell["cell_id"] in screening
        assert probability_close(cell["screening_recovery"], screening[cell["cell_id"]])


def test_confirmation_authoritative_result_recomputes_from_cell_counts() -> None:
    result = json.loads(
        (RESULTS / "m1_e4_participant_confirmation_authoritative_2026-09-16.json").read_text()
    )
    rows = result["results"]
    assert len(rows) == result["selected_cells_total"] == 29
    assert sum(row["replicates"] for row in rows) == 5800
    wrong_total = 0
    primary = []
    for row in rows:
        assert sum(row["selected"].values()) == row["replicates"]
        correct = row["selected"][row["generator"]]
        wrong = sum(
            value for key, value in row["selected"].items()
            if key not in {row["generator"], "INCONCLUSIVE"}
        )
        inconclusive = row["selected"]["INCONCLUSIVE"]
        assert probability_close(correct / row["replicates"], row["recovery_probability"])
        assert probability_close(wrong / row["replicates"], row["wrong_probability"])
        assert probability_close(inconclusive / row["replicates"], row["inconclusive_probability"])
        assert probability_close(
            row["recovery_probability"] + row["wrong_probability"] + row["inconclusive_probability"],
            1.0,
        )
        wrong_total += wrong
        if row["role"] == "PRIMARY_P64_FULL_GRID":
            primary.append(row)
    assert len(primary) == 18
    assert min(row["recovery_probability"] for row in primary) == 0.92
    assert all(row["passes_formal_recovery_gate"] for row in primary)
    assert wrong_total == result["wrong_family_selections_total"] == 3


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    p = successes / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = z * math.sqrt((p * (1.0 - p) / n) + z * z / (4.0 * n * n)) / denom
    return center - half, center + half


def test_phase_m_authoritative_result_recomputes_from_cell_counts() -> None:
    result = json.loads(
        (RESULTS / "m1_e4_protocol_robustness_authoritative_2026-09-17.json").read_text()
    )
    rows = result["results"]
    reps = result["replicates_per_cell"]
    assert len(rows) == result["selected_cells_total"] == 18
    assert reps == 200

    correct_total = wrong_total = inconclusive_total = 0
    failed = []
    lower_bounds = []
    for row in rows:
        assert sum(row["selected"].values()) == reps
        correct = row["selected"][row["generator"]]
        wrong = sum(
            value for key, value in row["selected"].items()
            if key not in {row["generator"], "INCONCLUSIVE"}
        )
        inconclusive = row["selected"]["INCONCLUSIVE"]
        assert probability_close(correct / reps, row["recovery_probability"])
        assert probability_close(wrong / reps, row["wrong_probability"])
        assert probability_close(inconclusive / reps, row["inconclusive_probability"])
        assert probability_close(
            row["recovery_probability"] + row["wrong_probability"] + row["inconclusive_probability"],
            1.0,
        )

        lower, upper = wilson(correct, reps)
        assert probability_close(lower, row["wilson_95"]["lower"])
        assert probability_close(upper, row["wilson_95"]["upper"])
        lower_bounds.append(lower)

        passes = row["recovery_probability"] >= result["formal_gate"]
        assert row["passes_formal_gate"] is passes
        if not passes:
            failed.append(row["cell_id"])

        correct_total += correct
        wrong_total += wrong
        inconclusive_total += inconclusive

    assert result["total_replicates"] == reps * len(rows) == 3600
    assert result["correct_family_selections_total"] == correct_total == 3169
    assert result["wrong_family_selections_total"] == wrong_total == 25
    assert result["inconclusive_total"] == inconclusive_total == 406
    assert result["minimum_recovery_probability"] == min(row["recovery_probability"] for row in rows) == 0.56
    assert probability_close(result["minimum_wilson_lower"], min(lower_bounds))
    assert sorted(result["formal_failed_cells"]) == sorted(failed) == [
        "COMBINED_ADVERSE__EVSD",
        "ITEM_HIGH__EVSD",
        "ITEM_MODERATE__EVSD",
    ]
    assert result["status"] == "PROTOCOL_ROBUSTNESS_FAIL"


def test_declared_benchmark_source_paths_exist() -> None:
    configs = [
        json.loads((BENCH / "m1_e4_participant_confirmation_200.json").read_text()),
        json.loads((BENCH / "m1_e4_protocol_robustness_200.json").read_text()),
    ]
    checked = []
    for config in configs:
        for key, value in config.items():
            if key.startswith("source_") and isinstance(value, str):
                checked.append((key, value))
                assert (ROOT / value).is_file(), f"{key} -> {value}"
    assert {key for key, _ in checked} == {
        "source_screening_config",
        "source_screening_results",
        "source_phase_i_document",
        "source_phase_l_document",
        "source_phase_m_document",
    }


def test_participant_screening_design_arithmetic_is_self_consistent() -> None:
    config = json.loads((BENCH / "m1_e4_participant_aware_screening.json").read_text())
    assert config["design_structure"]["operating_points"] == 5
    assert config["confirmation_replicates"] == 200
    assert config["screening_gate"]["confirmation_replicates"] == 200
    assert config["screening_gate"]["confirmation_required"] is True
    assert config["screening_gate"]["screening_replicates_are_authoritative_for_human_protocol"] is False

    for allocation in config["participant_allocations"]:
        assert (
            allocation["participants"]
            * allocation["target_trials_per_participant_per_cell"]
            == config["aggregate_target_per_cell"]
            == 640
        )
        assert (
            allocation["participants"]
            * allocation["foil_trials_per_participant_per_cell"]
            == config["aggregate_foil_per_cell"]
            == 640
        )
        expected_total = (
            (allocation["target_trials_per_participant_per_cell"]
             + allocation["foil_trials_per_participant_per_cell"])
            * config["design_structure"]["operating_points"]
            * 2
        )
        assert allocation["total_responses_per_participant"] == expected_total


def test_confirmation_selection_policy_is_exactly_reconstructed_from_screening() -> None:
    rows = read_csv("m1_e4_participant_screening_authoritative_2026-09-16.csv")
    config = json.loads((BENCH / "m1_e4_participant_confirmation_200.json").read_text())

    expected_primary = {
        f'{row["allocation"]}__{row["heterogeneity"]}__{row["generator"]}__{row["regime"]}'
        for row in rows
        if row["allocation"] == "P64_X10"
    }

    expected_boundary: set[str] = set()
    for allocation in ("P40_X16", "P80_X8", "P128_X5"):
        for generator in ("EVSD", "2HT"):
            group = [
                row for row in rows
                if row["allocation"] == allocation and row["generator"] == generator
            ]
            minimum = min(float(row["recovery_probability"]) for row in group)
            expected_boundary |= {
                f'{row["allocation"]}__{row["heterogeneity"]}__{row["generator"]}__{row["regime"]}'
                for row in group
                if float(row["recovery_probability"]) == minimum
            }

    selected_primary = {
        row["cell_id"] for row in config["selected_cells"]
        if row["role"] == "PRIMARY_P64_FULL_GRID"
    }
    selected_boundary = {
        row["cell_id"] for row in config["selected_cells"]
        if row["role"] == "BOUNDARY_MINIMUM_WITH_TIES"
    }

    assert selected_primary == expected_primary
    assert selected_boundary == expected_boundary
    assert len(expected_primary) == config["selection_policy"]["primary_cells"] == 18
    assert len(expected_boundary) == config["selection_policy"]["boundary_cells"] == 11
    assert len(expected_primary | expected_boundary) == config["selection_policy"]["selected_cells_total"] == 29


def test_confirmation_gate_and_precision_metadata_match_executable_values() -> None:
    config = json.loads((BENCH / "m1_e4_participant_confirmation_200.json").read_text())
    screening = json.loads((BENCH / "m1_e4_participant_aware_screening.json").read_text())
    assert config["replicates_per_cell"] == screening["confirmation_replicates"] == 200
    assert config["formal_gate"]["primary_all_cells_recovery_at_least"] == config["recovery_threshold"] == 0.8
    assert config["robustness_sensitivity"]["wilson_interval_level"] == 0.95
    assert config["robustness_sensitivity"]["replaces_formal_gate"] is False


def test_phase_m_design_counts_gate_and_mcse_metadata_recompute() -> None:
    config = json.loads((BENCH / "m1_e4_protocol_robustness_200.json").read_text())
    assert len(config["profiles"]) == 9
    assert len(config["generators"]) == 2
    assert config["selected_cells_total"] == len(config["profiles"]) * len(config["generators"]) == 18
    assert config["formal_gate"]["all_18_cells_recovery_at_least"] == config["recovery_threshold"] == 0.8
    assert config["formal_gate"]["point_estimate_gate_is_authoritative"] is True
    assert config["precision_sensitivity"]["replaces_formal_gate"] is False

    n = config["replicates_per_cell"]
    expected_max = math.sqrt(0.25 / n)
    expected_at_gate = math.sqrt(
        config["recovery_threshold"] * (1.0 - config["recovery_threshold"]) / n
    )
    assert probability_close(config["precision_sensitivity"]["mcse_max_at_200"], expected_max)
    assert probability_close(
        config["precision_sensitivity"]["mcse_at_recovery_0_8"], expected_at_gate
    )


def test_phase_m_allocation_response_arithmetic_is_self_consistent() -> None:
    config = json.loads((BENCH / "m1_e4_protocol_robustness_200.json").read_text())
    allocation = config["allocation"]
    per_participant = (
        (allocation["target_trials_per_participant_per_cell"]
         + allocation["foil_trials_per_participant_per_cell"])
        * allocation["bias_operating_points"]
        * allocation["hsimp_conditions"]
    )
    assert allocation["label"] == "P64_X10"
    assert allocation["generated_participants"] == 64
    assert per_participant == 200
