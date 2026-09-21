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
