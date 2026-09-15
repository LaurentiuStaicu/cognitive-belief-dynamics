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
    assert counts["subsystems"] == 8
    assert counts["processes"] >= 13
    assert counts["empirical_targets"] >= 1
    assert counts["theory_chapters"] == 16
    assert counts["theory_glossary"] >= 15
    assert counts["theory_tokens"] >= 60


@pytest.mark.parametrize("registry", ["modules", "variables", "links", "subsystems", "processes", "empirical_targets"])
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


def test_evidence_snapshot_schema_is_enforced(tmp_path):
    model = tmp_path / "model"
    shutil.copytree(ROOT / "model", model)
    snapshot = json.loads((model / "evidence_snapshot.json").read_text())
    snapshot["id"] = "EVIDENCE.INVALID"
    (model / "evidence_snapshot.json").write_text(json.dumps(snapshot))
    with pytest.raises(RegistryError, match="evidence snapshot"):
        validate_model_dir(model, ROOT / "schemas")


def test_empirical_target_references_are_enforced(tmp_path):
    model = tmp_path / "model"
    shutil.copytree(ROOT / "model", model)
    targets = json.loads((model / "empirical_targets.json").read_text())
    targets[0]["evidence_ref"] = "REF.MISSING.2099"
    (model / "empirical_targets.json").write_text(json.dumps(targets))
    with pytest.raises(RegistryError, match="unresolved target evidence reference"):
        validate_model_dir(model, ROOT / "schemas")


def test_empirical_target_pattern_references_are_enforced(tmp_path):
    model = tmp_path / "model"
    shutil.copytree(ROOT / "model", model)
    targets = json.loads((model / "empirical_targets.json").read_text())
    targets[0]["pattern_id"] = "VAL.M1.999"
    (model / "empirical_targets.json").write_text(json.dumps(targets))
    with pytest.raises(RegistryError, match="unresolved target pattern reference"):
        validate_model_dir(model, ROOT / "schemas")


def test_empirical_target_auxiliary_references_are_enforced(tmp_path):
    model = tmp_path / "model"
    shutil.copytree(ROOT / "model", model)
    targets = json.loads((model / "empirical_targets.json").read_text())
    m1_e3 = next(item for item in targets if item["id"] == "TARGET.M1.E3.ROBERTSON_2023")
    m1_e3["integrity_refs"] = ["REF.MISSING.2099"]
    (model / "empirical_targets.json").write_text(json.dumps(targets))
    with pytest.raises(RegistryError, match="unresolved target integrity_refs"):
        validate_model_dir(model, ROOT / "schemas")


def test_platform_ab_target_preserves_native_design_fields():
    targets = json.loads((ROOT / "model/empirical_targets.json").read_text())
    target = next(item for item in targets if item["id"] == "TARGET.M1.E3.ROBERTSON_2023")

    assert target["study"]["design_family"] == "PLATFORM_AB_TEST_ARCHIVE"
    assert "n_recruited" not in target["study"]
    assert "n_analyzed" not in target["study"]
    assert target["study"]["n_experiments"] == 12448
    assert target["study"]["n_clicks"] == 2778124

    metrics = {item["metric"] for item in target["effects"]}
    assert {"LOG_ODDS_COEFFICIENT", "RELATIVE_CHANGE_PERCENT"} <= metrics
