from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_kl_v2_paired_bootstrap_draw_stability_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_paired_bootstrap_result_retains_complete_valid_characterization() -> None:
    result = load()
    assert result["status"] == (
        "NON_AUTHORITATIVE_R2_KL_V2_PAIRED_BOOTSTRAP_CHARACTERIZATION_COMPLETE"
    )
    assert result["authoritative"] is False
    assert result["issue"] == 206

    design = result["design"]
    assert design["draw_grid"] == [49, 99, 199]
    assert design["evaluation_replicates"] == 10
    assert design["unique_datasets"] == 390
    assert design["restriction_runs"] == 750
    assert design["snapshots"] == 2250
    assert design["pair_comparisons"] == 2250

    integrity = result["operational_integrity"]
    assert integrity["fit_failures"] == 0
    assert integrity["calibration_failures"] == 0
    assert integrity["bootstrap_fit_failures"] == 0
    assert integrity["valid_snapshots"] == 2250
    assert integrity["all_snapshots_valid"] is True


def test_paired_bootstrap_exact_artifact_provenance_is_frozen() -> None:
    execution = load()["execution"]
    assert execution["temporary_execution_pr"] == 210
    assert execution["source_run_id"] == "36339370047"
    assert execution["recovery_pr"] == 211
    assert execution["recovery_run_id"] == "36340881516"
    assert execution["recovered_combined_artifact_id"] == 10938668225
    assert execution["recovered_combined_artifact_zip_sha256"] == (
        "008bc62bc5048011cd015fa133111627e7a88b35bb5eb194b8e3dca062d547d7"
    )
    assert execution["exact_combined_json_sha256"] == (
        "b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301"
    )
    assert execution["exact_combined_json_size_bytes"] == 9013672
    assert len(execution["partition_json_sha256"]) == 5


def test_global_pair_stability_values_are_retained_without_selection() -> None:
    result = load()
    rows = {
        (row["left_draws"], row["right_draws"]): row
        for row in result["global_pair_stability"]
    }
    assert rows[(49, 99)]["discordant_decisions"] == 37
    assert rows[(49, 199)]["discordant_decisions"] == 43
    assert rows[(99, 199)]["discordant_decisions"] == 16
    assert rows[(99, 199)]["decision_concordance"] == (
        0.9786666666666667
    )

    interpretation = result["interpretation"]
    assert interpretation["selection_prohibited"] is True
    assert interpretation["authoritative_bootstrap_draws_frozen"] is False
    assert interpretation["authoritative_evaluation_replicates_frozen"] is False
    assert interpretation["power_validated"] is False


def test_null_and_specificity_context_is_not_promoted_to_alpha_validation() -> None:
    result = load()
    roles = result["role_context"]

    assert [row["rejections"] for row in roles["CBD_NULL_FALSE_REJECTION"]] == [
        1,
        0,
        0,
    ]
    assert [row["rejections"] for row in roles["ADD_NULL_FALSE_REJECTION"]] == [
        0,
        0,
        0,
    ]
    assert [
        row["rejections"]
        for row in roles["ADD_SPECIFICITY_NEGATIVE_CONTROL"]
    ] == [2, 4, 6]


def test_99_199_stratified_stability_retains_all_principal_dimensions() -> None:
    pair = load()["pair_99_199"]
    assert {row["role"] for row in pair["by_role"]} == {
        "CBD_NULL_FALSE_REJECTION",
        "ADD_NULL_FALSE_REJECTION",
        "CBD_DEPARTURE_DETECTION",
        "ADD_SPECIFICITY_NEGATIVE_CONTROL",
        "ADD_DEPARTURE_DIAGNOSTIC",
    }
    assert {
        row["axis"] for row in pair["by_axis"]
    } == {
        None,
        "STANDALONE_ACCURACY_MAIN_EFFECT",
        "COMPLEMENT_RELATION_VIOLATION",
        "COMBINED_VIOLATION",
    }
    assert {row["target_mean_bernoulli_kl"] for row in pair["by_target"]} == {
        0.0,
        0.001,
        0.002,
        0.003,
    }

    cbd = next(
        row
        for row in pair["by_role"]
        if row["role"] == "CBD_DEPARTURE_DETECTION"
    )
    assert cbd["comparisons"] == 360
    assert cbd["discordant"] == 7
    assert cbd["concordance"] == 0.9805555555555555


def test_result_boundary_keeps_human_stage_closed() -> None:
    interpretation = load()["interpretation"]
    assert interpretation["authoritative_core_grid_frozen"] is False
    assert interpretation["human_n_frozen"] is False
    assert interpretation["participant_recruitment_authorized"] is False
    assert interpretation["runtime_f1b_authorized"] is False
    assert interpretation["next_gate"] == (
        "PROSPECTIVE_BOOTSTRAP_DRAW_COUNT_DECISION_RULE_OR_FURTHER_CHARACTERIZATION"
    )
