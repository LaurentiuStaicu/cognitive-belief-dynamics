from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_every_registered_process_code_ref_exists() -> None:
    processes = json.loads((ROOT / "model" / "processes.json").read_text(encoding="utf-8"))
    missing = []
    for process in processes:
        ref = ROOT / process["code_ref"]
        if not ref.is_file():
            missing.append((process["id"], process["code_ref"]))
    assert missing == []


def test_process_code_refs_use_scientific_core_or_test_surfaces() -> None:
    processes = json.loads((ROOT / "model" / "processes.json").read_text(encoding="utf-8"))
    for process in processes:
        ref = process["code_ref"]
        assert ref.startswith(("src/cognitive_epistemic_model/", "tests/"))
        assert ref.endswith(".py")


def test_process_status_and_code_ref_are_not_future_placeholders() -> None:
    processes = json.loads((ROOT / "model" / "processes.json").read_text(encoding="utf-8"))
    # Current registry has executable/reference code for implemented_m0 and candidate
    # processes; a future process must not be made to look implemented by a stale code_ref.
    for process in processes:
        if process["status"] in {"implemented_m0", "candidate"}:
            assert (ROOT / process["code_ref"]).is_file()
        elif process["status"] == "future":
            raise AssertionError(
                f'{process["id"]} is future but processes.json requires code_ref; '
                "define future-process semantics explicitly before adding one"
            )
