from __future__ import annotations

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_w0_combine as combine


def test_combine_requires_exactly_250_shards() -> None:
    with pytest.raises(ValueError, match="exactly 250"):
        combine.combine_w0_shards([], plan={"shard_plan": []}, config={})


def test_combine_rejects_duplicate_shard_indices() -> None:
    shards = [
        {"shard_index": 0}
        for _ in range(250)
    ]
    with pytest.raises(ValueError, match="shard-index coverage"):
        combine.combine_w0_shards(
            shards,
            plan={"shard_plan": []},
            config={},
        )


def test_combined_status_constant_is_frozen() -> None:
    assert combine.COMBINED_STATUS == (
        "NON_AUTHORITATIVE_S4_W0_COMBINED_COMPLETE"
    )
