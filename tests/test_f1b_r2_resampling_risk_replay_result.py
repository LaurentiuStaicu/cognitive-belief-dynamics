from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_resampling_risk_replay_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_stage_b_replay_retention_counts_are_frozen() -> None:
    result = load()
    assert result["status"] == (
        "NON_AUTHORITATIVE_RESAMPLING_RISK_REPLAY_COMPLETE"
    )
    assert result["authoritative"] is False
    assert result["issue"] == 213

    summary = result["global_summary"]
    assert summary["run_count"] == 750
    assert summary["resolved_by_49_count"] == 326
    assert summary["resolved_by_99_count"] == 372
    assert summary["resolved_by_199_count"] == 526
    assert summary["unresolved_at_199_count"] == 224
    assert summary["sequential_reject_count"] == 119
    assert summary["sequential_not_reject_count"] == 407
    assert summary[
        "sequential_vs_fixed_199_disagreement_count"
    ] == 0


def test_controller_landmarks_match_validated_stage_a() -> None:
    controller = load()["controller"]
    assert controller["alpha"] == 0.05
    assert controller["epsilon"] == 0.001
    assert controller["halfspend"] == 1000.0
    assert controller["max_attempts"] == 199

    landmarks = controller["boundary_landmarks"]
    assert (landmarks["1"]["lower"], landmarks["1"]["upper"]) == (-1, 2)
    assert (landmarks["49"]["lower"], landmarks["49"]["upper"]) == (-1, 12)
    assert (landmarks["99"]["lower"], landmarks["99"]["upper"]) == (-1, 17)
    assert (landmarks["173"]["lower"], landmarks["173"]["upper"]) == (0, 23)
    assert (landmarks["199"]["lower"], landmarks["199"]["upper"]) == (0, 25)


def test_all_stream_checkpoints_are_retained_and_unique() -> None:
    result = load()
    checkpoints = result["stream_checkpoints"]
    integrity = result["integrity"]

    assert len(checkpoints) == 750
    assert integrity["stream_checkpoint_count"] == 750
    assert len(integrity["stream_checkpoints_sha256"]) == 64

    run_ids = [row["run_id"] for row in checkpoints]
    assert len(run_ids) == len(set(run_ids)) == 750
    assert all(len(row["dataset_sha256"]) == 64 for row in checkpoints)
    assert all(
        len(row["attempt_sequence_sha256"]) == 64
        for row in checkpoints
    )

    unresolved = result["unresolved_run_ids"]
    assert len(unresolved) == len(set(unresolved)) == 224
    assert set(unresolved).issubset(set(run_ids))


def test_unresolved_runs_are_not_reclassified_by_fixed_199() -> None:
    context = load()["unresolved_fixed_199_context_descriptive_only"]
    assert context["sequential_unresolved_count"] == 224
    assert context["fixed_199_reject_count"] == 140
    assert context["fixed_199_not_reject_count"] == 84
    assert context["fixed_199_plus_one_p_value_min"] == 0.01
    assert context["fixed_199_plus_one_p_value_median"] == 0.04
    assert context["fixed_199_plus_one_p_value_max"] == 0.125
    assert "remain unresolved" in context["warning"]


def test_all_sequential_rejects_share_conservative_lower_boundary_stop() -> None:
    structure = load()["sequential_reject_structure"]
    assert structure == {
        "reject_count": 119,
        "all_rejects_stopping_n_173": True,
        "all_rejects_stopping_sum_0": True,
    }


def test_role_context_preserves_unresolved_burden() -> None:
    rows = {row["role"]: row for row in load()["by_role"]}
    assert rows["CBD_DEPARTURE_DETECTION"]["unresolved_at_199_count"] == 131
    assert rows["ADD_DEPARTURE_DIAGNOSTIC"]["unresolved_at_199_count"] == 74
    assert rows["ADD_SPECIFICITY_NEGATIVE_CONTROL"][
        "unresolved_at_199_count"
    ] == 17
    assert rows["CBD_NULL_FALSE_REJECTION"]["unresolved_at_199_count"] == 2
    assert rows["ADD_NULL_FALSE_REJECTION"]["unresolved_at_199_count"] == 0


def test_exact_replay_provenance_is_retained() -> None:
    execution = load()["execution"]
    assert execution["temporary_replay_pr"] == 216
    assert execution["github_run_id"] == "36343709630"
    assert execution["replay_artifact_id"] == 10938984164
    assert execution["replay_artifact_zip_sha256"] == (
        "0a7f6308aa0bd21866a4559d4dec38210b2225fa3f23f3e45da4abcbba76574b"
    )
    assert execution["exact_replay_json_sha256"] == (
        "47d9321432208f56ad5ecc3077547601122196373d54c40a4c02bde91218635b"
    )
    assert execution["exact_replay_json_size_bytes"] == 1803618
    assert execution["retained_input_artifact_id"] == 10938668225
    assert execution["retained_input_json_sha256"] == (
        "b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301"
    )


def test_stage_b_boundary_authorizes_only_a_prospective_extension_gate() -> None:
    result = load()
    assert result["next_gate"] == (
        "PROSPECTIVE_EXTENSION_BEYOND_199_WITH_EXPLICIT_CAP_"
        "OR_SEPARATELY_JUSTIFIED_CONTROLLER_CHANGE"
    )
    interpretation = result["interpretation"]
    assert interpretation["stage_b_replay_complete"] is True
    assert interpretation["draw_count_selected"] is False
    assert interpretation["new_bootstrap_attempts_generated"] is False
    assert interpretation["statistical_power_validated"] is False
    assert interpretation["authoritative_core_grid_frozen"] is False
    assert interpretation["human_n_frozen"] is False
    assert interpretation["participant_recruitment_authorized"] is False
    assert interpretation["runtime_f1b_authorized"] is False
