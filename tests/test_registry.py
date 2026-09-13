from pathlib import Path
import json
import shutil
import pytest

from cognitive_epistemic_model.registry import RegistryError, validate_model_dir

ROOT = Path(__file__).resolve().parents[1]


def test_registry_schema_and_semantic_validation():
    counts = validate_model_dir(ROOT / "model", ROOT / "schemas")
    assert counts["modules"] == 20
    assert counts["variables"] >= 7
    assert counts["links"] >= 3


@pytest.mark.parametrize("registry", ["modules", "variables", "links"])
def test_duplicate_ids_are_rejected(tmp_path, registry):
    model = tmp_path / "model"
    shutil.copytree(ROOT / "model", model)
    path = model / f"{registry}.json"
    items = json.loads(path.read_text())
    items.append(dict(items[0]))
    path.write_text(json.dumps(items))
    with pytest.raises(RegistryError, match=f"duplicate {registry} IDs"):
        validate_model_dir(model, ROOT / "schemas")
