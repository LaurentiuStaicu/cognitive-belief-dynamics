from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSES = ROOT / "model/processes.json"


def test_all_canonical_process_code_refs_resolve_inside_scientific_core():
    processes = json.loads(PROCESSES.read_text(encoding="utf-8"))
    refs = [item["code_ref"] for item in processes if item.get("code_ref")]

    assert refs
    missing = [ref for ref in refs if not (ROOT / ref).is_file()]
    assert missing == []
    assert all(not ref.startswith("web/") for ref in refs)


def test_scientific_core_does_not_restore_product_layer():
    assert not (ROOT / "web").exists()


def test_canonical_status_reports_both_retained_m1_e4_outcomes():
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    benchmarks = (ROOT / "model/benchmarks/README.md").read_text(encoding="utf-8")

    for text in (status, benchmarks):
        normalized = text.lower()
        assert "all 18 primary p64_x10 cells meet the declared 0.80 recovery gate" in normalized
        assert "minimum observed recovery of 0.92" in normalized
        assert "protocol_robustness_fail" in normalized
        assert "item_moderate__evsd" in normalized
        assert "item_high__evsd" in normalized
        assert "combined_adverse__evsd" in normalized
        assert "minimum recovery probability" in normalized
        assert r"\n\n" not in text
