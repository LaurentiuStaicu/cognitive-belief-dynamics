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

@pytest.mark.parametrize('case', ['unknown_reference', 'doi_mismatch', 'missing_translation', 'duplicate_reference'])
def test_evidence_integrity(tmp_path, case):
    model = tmp_path / 'model'
    shutil.copytree(ROOT / 'model', model)
    links = json.loads((model / 'links.json').read_text())
    references = json.loads((model / 'references.json').read_text())
    if case == 'unknown_reference':
        links[0]['evidence_refs'] = ['REF.MISSING.2026']
        message = 'unresolved evidence references'
    elif case == 'doi_mismatch':
        references[0]['url'] = 'https://doi.org/10.1234/wrong'
        message = 'DOI URL mismatch'
    elif case == 'missing_translation':
        del links[0]['evidence_limitations']['ro']
        message = 'required property'
    else:
        references.append(dict(references[0]))
        message = 'duplicate references IDs'
    (model / 'links.json').write_text(json.dumps(links))
    (model / 'references.json').write_text(json.dumps(references))
    with pytest.raises(RegistryError, match=message):
        validate_model_dir(model, ROOT / 'schemas')
