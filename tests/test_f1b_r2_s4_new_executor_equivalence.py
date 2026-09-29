from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_broad_executor as executor,
)
from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_new_executor_equivalence as equivalence,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_s4_new_executor_equivalence_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def scientific_row() -> dict:
    return {
        "scientific_run_id": (
            "DATASET|REPLICATE=42|RESTRICTION=ADD_RESTRICTION"
            "|MISSINGNESS=0.00"
        ),
        "dataset_id": "DATASET|REPLICATE=42",
        "identity": "TEST_IDENTITY",
        "identity_type": "DEPARTURE",
        "restriction": "ADD_RESTRICTION",
        "role": "ADD_DEPARTURE_DIAGNOSTIC",
        "anchor_id": "ANCHOR",
        "axis": "AXIS",
        "sign": 1,
        "target_mean_bernoulli_kl": 0.002,
        "evaluation_replicate": 42,
        "missingness": 0.0,
    }


def spec() -> SimpleNamespace:
    return SimpleNamespace(
        identity="TEST_IDENTITY",
        identity_type="DEPARTURE",
        restriction="ADD_RESTRICTION",
        role="ADD_DEPARTURE_DIAGNOSTIC",
        anchor_id="ANCHOR",
        axis="AXIS",
        sign=1,
        target_mean_bernoulli_kl=0.002,
    )


def test_repository_equivalence_contract_is_frozen() -> None:
    config = load_config()
    equivalence.validate_equivalence_config(config)
    assert config["selection"]["expected_row_count"] == 12
    assert config["selection"]["expected_unique_scientific_run_count"] == 7
    assert config["selection"]["selected_row_identity_sha256"] == (
        "41062e2bf501799a41b78d412b33551685045b98b9a67c9d50a9a26131c16b36"
    )
    assert config["numerical_lineage"]["required_value"] == "Haswell"
    assert config["executor_contract"]["prefix_attempts"] == 199
    assert config["executor_contract"]["maximum_total_attempts"] == 10000


def test_equivalence_contract_cannot_close_release_blocker() -> None:
    config = deepcopy(load_config())
    config["release"]["release_blocker_closed"] = True
    with pytest.raises(ValueError, match="v0.2.0 blocker"):
        equivalence.validate_equivalence_config(config)


def test_equivalence_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        equivalence.validate_equivalence_config(config)


def test_new_executor_stops_on_first_prefix_refit_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []

    monkeypatch.setattr(executor, "validate_m1_config", lambda config: None)
    monkeypatch.setattr(executor, "validate_m2_config", lambda config: None)
    monkeypatch.setattr(
        executor,
        "_scientific_identity",
        lambda row, spec, replicate: ("DATASET|REPLICATE=42", row["scientific_run_id"]),
    )
    monkeypatch.setattr(executor, "dataset_fingerprint", lambda dataset: "dataset-sha")
    monkeypatch.setattr(executor, "bootstrap_seed_for", lambda *args, **kwargs: 123)
    monkeypatch.setattr(
        executor,
        "_method_observed_fit",
        lambda *args, **kwargs: (SimpleNamespace(statistic=2.0), None),
    )

    def fake_draw(*args, draw_index: int, **kwargs) -> float:
        calls.append(draw_index)
        if draw_index == 3:
            raise RuntimeError("synthetic refit failure")
        return 3.0

    monkeypatch.setattr(executor, "_new_draw_statistic", fake_draw)

    row = executor.run_new_stream(
        scientific_row(),
        spec=spec(),
        replicate=42,
        dataset=object(),
        method_id="POPULATION",
        paired_config={},
        m1_config={},
        m2_config={},
        boundaries=object(),
    )

    assert calls == [0, 1, 2, 3]
    assert row["status"] == "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    assert row["prefix_attempt_count"] == 4
    assert row["prefix_successful_attempt_count"] == 3
    assert row["prefix_refit_failure_count"] == 1
    assert row["terminal_n"] == 4
    assert row["failure_n"] == 4
    assert row["terminal_sum"] == 3
    assert row["continued_beyond_199"] is False
    assert row["new_attempt_count"] == 0


def test_new_executor_observed_fit_failure_is_unresolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(executor, "validate_m1_config", lambda config: None)
    monkeypatch.setattr(executor, "validate_m2_config", lambda config: None)
    monkeypatch.setattr(
        executor,
        "_scientific_identity",
        lambda row, spec, replicate: ("DATASET|REPLICATE=42", row["scientific_run_id"]),
    )
    monkeypatch.setattr(executor, "dataset_fingerprint", lambda dataset: "dataset-sha")
    monkeypatch.setattr(executor, "bootstrap_seed_for", lambda *args, **kwargs: 123)

    def fail_fit(*args, **kwargs):
        raise ValueError("synthetic observed fit failure")

    monkeypatch.setattr(executor, "_method_observed_fit", fail_fit)

    row = executor.run_new_stream(
        scientific_row(),
        spec=spec(),
        replicate=42,
        dataset=object(),
        method_id="POPULATION",
        paired_config={},
        m1_config={},
        m2_config={},
        boundaries=object(),
    )

    assert row["status"] == "PREFIX_EXECUTION_FAILURE_UNRESOLVED"
    assert row["prefix_attempt_count"] == 0
    assert row["prefix_execution_failure"] is True
    assert row["terminal_n"] == 0
    assert row["decision"] is None
