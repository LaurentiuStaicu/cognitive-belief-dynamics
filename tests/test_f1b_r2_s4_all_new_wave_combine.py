from __future__ import annotations

import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_all_new_wave as wave,
)
from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_all_new_wave_combine as combine,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r2_s4_w1_execution_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_combine_requires_exactly_250_shards() -> None:
    with pytest.raises(ValueError, match="exactly 250"):
        combine.combine_all_new_wave_shards(
            [],
            plan={"shard_plan": [], "wave_id": "W1"},
            config=load_config(),
        )


def test_combine_rejects_duplicate_shard_indices() -> None:
    shards = [{"shard_index": 0} for _ in range(250)]
    with pytest.raises(ValueError, match="shard-index coverage"):
        combine.combine_all_new_wave_shards(
            shards,
            plan={"shard_plan": [], "wave_id": "W1"},
            config=load_config(),
        )


def test_w1_status_constants_are_frozen() -> None:
    assert wave.plan_status("W1") == (
        "NON_AUTHORITATIVE_S4_W1_EXECUTION_PLAN_COMPLETE"
    )
    assert wave.shard_status("W1") == (
        "NON_AUTHORITATIVE_S4_W1_SHARD_COMPLETE"
    )
    assert wave.combined_status("W1") == (
        "NON_AUTHORITATIVE_S4_W1_COMBINED_COMPLETE"
    )
