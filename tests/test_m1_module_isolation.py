from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "cognitive_epistemic_model"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            imports.add(prefix + (node.module or ""))
    return imports


def test_m1_presentation_candidate_does_not_depend_on_m0_state_or_simulator() -> None:
    imports = imported_modules(PACKAGE / "presentation.py")
    forbidden = {
        ".state",
        ".simulation",
        ".model",
        "cognitive_epistemic_model.state",
        "cognitive_epistemic_model.simulation",
        "cognitive_epistemic_model.model",
    }
    assert imports.isdisjoint(forbidden)


def test_m1_access_candidate_does_not_depend_on_m0_state_or_simulator() -> None:
    imports = imported_modules(PACKAGE / "access.py")
    forbidden = {
        ".state",
        ".simulation",
        ".model",
        "cognitive_epistemic_model.state",
        "cognitive_epistemic_model.simulation",
        "cognitive_epistemic_model.model",
    }
    assert imports.isdisjoint(forbidden)


def test_m1_editorial_candidate_does_not_depend_on_m0_state_or_simulator() -> None:
    imports = imported_modules(PACKAGE / "editorial.py")
    forbidden = {
        ".state",
        ".simulation",
        ".model",
        "cognitive_epistemic_model.state",
        "cognitive_epistemic_model.simulation",
        "cognitive_epistemic_model.model",
    }
    assert imports.isdisjoint(forbidden)
