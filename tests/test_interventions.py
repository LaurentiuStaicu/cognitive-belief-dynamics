import pytest
from cognitive_epistemic_model.interventions import evaluate_bundle, export_interventions
from cognitive_epistemic_model.state import ModelParams


def test_grid_probabilities_and_reproducibility():
    data = export_interventions()
    assert data == export_interventions()
    assert len(data['profiles']) == 3
    for profile in data['profiles']:
        assert {(b['mask'], b['start']) for b in profile['bundles']} == {(m, t) for m in range(16) for t in (2, 5)}
        for b in profile['bundles']:
            for kind in ('false', 'true'):
                path = b[kind + '_share_path']
                assert len(path) == 13
                assert all(0 <= p <= 1 for p in path)
                assert b[kind + '_share'] == pytest.approx(sum(path) / 13)


def test_timing_cannot_change_past_exposures():
    p = ModelParams()
    baseline = evaluate_bundle(0, 5, p)
    late = evaluate_bundle(1, 5, p)
    early = evaluate_bundle(1, 2, p)
    for kind in ('false', 'true'):
        key = kind + '_share_path'
        assert late[key] == baseline[key]
        assert early[key][:2] == baseline[key][:2]
        assert early[key][2:] != baseline[key][2:]
        assert evaluate_bundle(0, 2, p)[key] == baseline[key]


def test_correction_and_accuracy_have_distinct_paths():
    p = ModelParams()
    base = evaluate_bundle(0, 2, p)
    correction = evaluate_bundle(2, 2, p)
    cue = evaluate_bundle(4, 2, p)
    assert correction['false_belief'] < base['false_belief']
    assert correction['true_belief'] > base['true_belief']
    for kind in ('false', 'true'):
        assert cue[kind + '_belief'] == base[kind + '_belief']
        assert correction[kind + '_share_path'][:2] == base[kind + '_share_path'][:2]


def test_invalid_bundle():
    with pytest.raises(ValueError):
        evaluate_bundle(16, 2, ModelParams())
    with pytest.raises(ValueError):
        evaluate_bundle(0, 3, ModelParams())
