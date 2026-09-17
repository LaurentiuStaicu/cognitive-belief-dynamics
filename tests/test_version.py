import json
from pathlib import Path
import tomllib
from cognitive_epistemic_model import __version__

ROOT = Path(__file__).resolve().parents[1]


def test_release_versions_are_consistent():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    assert 'version' in project['project']['dynamic']
    assert project['tool']['hatch']['version']['path'] == 'src/cognitive_epistemic_model/__init__.py'
    npm = __version__.replace('a', '-alpha.')
    assert json.loads((ROOT / 'web/package.json').read_text())['version'] == npm
    lock = json.loads((ROOT / 'web/package-lock.json').read_text())
    assert lock['version'] == lock['packages']['']['version'] == npm
    version = json.loads((ROOT / 'web/public/model/version.json').read_text())
    assert version['version'] == version['software_version'] == __version__
    assert version['model'] == version['model_specification'] == 'M1'
    assert version['baseline_model_specification'] == 'M0'
    assert version['evidence_snapshot'].startswith('EVIDENCE.M1.')
    assert '.r' in version['evidence_snapshot']
    assert version['release_tag'] == 'v' + __version__
    runs = json.loads((ROOT / 'web/public/model/runs.json').read_text())
    assert runs['model_version'] == __version__
    assert runs['model_specification'] == 'M0'
    assert runs['purpose'] == 'MECHANISM_TEST_DEMONSTRATION'
    assert all(run['purpose'] == 'MECHANISM_TEST_DEMONSTRATION' for run in runs['runs'])
    interventions = json.loads((ROOT / 'web/public/model/interventions.json').read_text())
    assert interventions['model_version'] == __version__
    assert interventions['purpose'] == 'ILLUSTRATIVE_DECISION_SUPPORT'
    explanations = json.loads((ROOT / 'web/public/model/explanations.json').read_text())
    assert explanations['model_version'] == __version__
    assert explanations['model_specification'] == 'M0'
    assert explanations['purpose'] == 'EXPLANATION_OF_REFERENCE_RUNS'
    diagnostics = json.loads((ROOT / 'web/public/model/diagnostics.json').read_text())
    assert diagnostics['software_version'] == __version__
    assert diagnostics['model_specification'] == 'M0'
    m1 = json.loads((ROOT / 'web/public/model/m1_editorial.json').read_text())
    assert m1['model_version'] == __version__
    assert m1['model_specification'] == 'M1'
    assert m1['baseline_model_specification'] == 'M0'
    assert m1['experiment']['id'] == 'M1.E1'
    assert m1['experiment']['purpose'] == 'MECHANISM_TEST_DEMONSTRATION'
    assert m1['experiment']['conditions']['negative']['observed_balance'] < m1['experiment']['conditions']['neutral']['observed_balance']
    assert m1['experiment']['nested_null']['observed_balance'] == 0.0
    m1e2 = json.loads((ROOT / 'web/public/model/m1_presentation.json').read_text())
    assert m1e2['model_version'] == __version__
    assert m1e2['model_specification'] == 'M1'
    assert m1e2['baseline_model_specification'] == 'M0'
    assert m1e2['experiment']['id'] == 'M1.E2'
    assert m1e2['experiment']['purpose'] == 'MODEL_DISCRIMINATION_DEMONSTRATION'
    assert m1e2['experiment']['semantic_signature']
    congruent = m1e2['experiment']['conditions']['congruent']['models']['frame_congruence']
    counter = m1e2['experiment']['conditions']['counter_attitudinal']['models']['frame_congruence']
    assert congruent['contrast'] > counter['contrast']
    assert abs(counter['contrast']) < 1e-12
    m1e3 = json.loads((ROOT / 'web/public/model/m1_access.json').read_text())
    assert m1e3['model_version'] == __version__
    assert m1e3['model_specification'] == 'M1'
    assert m1e3['baseline_model_specification'] == 'M0'
    assert m1e3['experiment']['id'] == 'M1.E3'
    assert m1e3['experiment']['purpose'] == 'MODEL_DISCRIMINATION_DEMONSTRATION'
    lower = m1e3['experiment']['conditions']['lower_negativity']
    higher = m1e3['experiment']['conditions']['higher_negativity']
    assert lower['models']['null']['p_access'] == higher['models']['null']['p_access']
    assert higher['models']['headline_negativity']['p_access'] > lower['models']['headline_negativity']['p_access']
    assert m1e3['experiment']['parameters']['calibrated'] is False
    assert 'belief' in m1e3['experiment']['interpretation_boundary'].lower()
    snapshot = json.loads((ROOT / 'model/evidence_snapshot.json').read_text())
    assert snapshot['id'] == version['evidence_snapshot']
    assert f'Alpha {__version__}' in (ROOT / 'README.md').read_text()
    assert (ROOT / f'releases/v{__version__}.md').is_file()
    assert (ROOT / 'CITATION.cff').is_file()
    assert (ROOT / 'docs/ODD_MAIN.md').is_file()
    assert (ROOT / 'docs/ODD_M1.md').is_file()
    assert (ROOT / 'docs/ODD_M1_E2.md').is_file()
    assert (ROOT / 'docs/ODD_M1_E3.md').is_file()
    assert (ROOT / 'docs/ALPHA_0.4.2a0_PLAN.md').is_file()
    assert (ROOT / 'docs/ALPHA_0.4.3a0_OA_VP_CLOSURE_AUDIT.md').is_file()
    assert (ROOT / 'LICENSE').is_file()
    assert (ROOT / 'LICENSES/CC-BY-4.0.txt').is_file()
