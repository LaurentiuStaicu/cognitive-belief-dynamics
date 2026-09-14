import importlib.util
from pathlib import Path
import pytest
from cognitive_epistemic_model.explanations import explain_reference_run
from cognitive_epistemic_model.mathutils import logistic

spec = importlib.util.spec_from_file_location('export_web', Path(__file__).resolve().parents[1] / 'scripts/export_web.py')
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


@pytest.mark.parametrize('kind', ['repetition', 'correction', 'source', 'accuracy'])
def test_terms_reconstruct_actual_reference_outputs(kind):
    run = exporter.reference_run(kind)
    explained = explain_reference_run(run)
    assert len(explained['frames']) == len(run['frames']) == 13
    for original, explanation in zip(run['frames'], explained['frames']):
        assert sum(explanation['belief_terms'].values()) == pytest.approx(original['latent_log_odds'], abs=1e-14)
        assert logistic(sum(explanation['belief_terms'].values())) == pytest.approx(original['belief'], abs=1e-14)
        assert logistic(sum(explanation['sharing_terms'].values())) == pytest.approx(original['share_probability'], abs=1e-14)
        if original['time'] == 0:
            assert explanation['changes'] is None
        else:
            for key, delta in explanation['changes'].items():
                assert run['frames'][original['time'] - 1][key] + delta == pytest.approx(original[key])


def test_context_and_cue_are_not_conflated_with_belief():
    correction = explain_reference_run(exporter.reference_run('correction'))['frames']
    assert correction[4]['belief_terms']['correction'] == 0
    assert correction[5]['belief_terms']['correction'] < 0
    source = explain_reference_run(exporter.reference_run('source'))['frames']
    assert source[0]['belief_terms']['evidence'] == 0
    assert source[2]['belief_terms']['evidence'] < 0
    cue = explain_reference_run(exporter.reference_run('accuracy'))['frames']
    assert cue[4]['belief_terms'] == cue[5]['belief_terms']
    assert cue[4]['sharing_terms'] != cue[5]['sharing_terms']
    assert cue[5]['inputs']['accuracy_cue'] is True
