from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
BENCHMARKS = ROOT / "model/benchmarks/README.md"
RESULT = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_protocol_robustness_authoritative_2026-09-17.json"
)


def normalized(path: Path) -> str:
    return path.read_text(encoding="utf-8").lower()


def test_status_preserves_canonical_event_driven_paradigm_boundary() -> None:
    status = normalized(STATUS)
    assert (
        "event-driven cognitive state-transition and agent-level stochastic "
        "dynamical model informed by systems thinking"
    ) in status
    assert "not currently a formal system dynamics model" in status
    assert "share do not automatically generate future exposure" in status
    assert "event schedules remain externally supplied" in status


def test_status_reports_confirmation_pass_and_protocol_robustness_fail_together() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "PROTOCOL_ROBUSTNESS_FAIL"
    assert result["minimum_recovery_probability"] == 0.56
    assert set(result["formal_failed_cells"]) == {
        "COMBINED_ADVERSE__EVSD",
        "ITEM_HIGH__EVSD",
        "ITEM_MODERATE__EVSD",
    }

    for path in (STATUS, BENCHMARKS):
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        assert "all 18 primary p64_x10 cells meet the declared 0.80 recovery gate" in lower
        assert "0.92" in text
        assert "PROTOCOL_ROBUSTNESS_FAIL" in text
        assert "3 of 18" in text
        assert "0.56" in text
        for cell_id in result["formal_failed_cells"]:
            assert cell_id in text


def test_status_does_not_convert_synthetic_results_into_human_validation() -> None:
    status = normalized(STATUS)
    benchmarks = normalized(BENCHMARKS)

    assert "synthetic identifiability/discrimination results only" in status
    assert "human-participant validation of m1.e4" in status
    assert "identification or estimation of pencode" in status
    assert "authorization of participant recruitment" in status

    assert "synthetic model-recovery finding" in benchmarks
    assert "does not select evsd or 2ht as human truth" in benchmarks
    assert "must be reported together" in benchmarks
