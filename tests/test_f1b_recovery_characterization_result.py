from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "model" / "results" / "f1b_recovery_characterization_result_2026-09-27.json.gz"
SUMMARY = ROOT / "model" / "results" / "f1b_recovery_characterization_summary_2026-09-27.json"


def test_f1b_retained_characterization_result_integrity() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    raw = gzip.decompress(RESULT.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == summary["full_result_sha256"]

    result = json.loads(raw.decode("utf-8"))
    assert result["status"] == "NON_AUTHORITATIVE_CHARACTERIZATION_RESULT"
    assert result["authoritative"] is False
    assert result["source_commit"] == "938f72789e883ff5e98c4edc58ffbf3ced84fc93"
    assert len(result["grid_results"]) == 144
    assert len(result["comparisons"]) == 108


def test_f1b_retained_characterization_keeps_all_gates_closed() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    decision = summary["decision"]
    assert decision["authoritative_core_grid_frozen"] is False
    assert decision["human_n_frozen"] is False
    assert decision["participant_recruitment_authorized"] is False
    assert decision["runtime_f1b_authorized"] is False
    assert decision["penalized_hierarchical_prototype_sufficient_for_authoritative_use"] is False


def test_f1b_retained_characterization_is_negative_not_solver_failure() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    for problem in ("R1", "R2"):
        for row in summary["aggregate"][problem].values():
            assert row["cells_fit_failure_gt_0"] == 0
            assert row["mean_fit_failure"] == 0.0
