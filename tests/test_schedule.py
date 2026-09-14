import json
from pathlib import Path

from cognitive_epistemic_model import interventions as module
from cognitive_epistemic_model.state import ModelParams


def test_early_and_late_schedules():
    early = module.bundle_schedule(15, 2)['frames']
    late = module.bundle_schedule(15, 5)['frames']
    def times(frames, key):
        return [f['time'] for f in frames if f[key]]
    assert times(early, 'exposure') == [1]
    assert times(early, 'exposure_prevented') == [2, 3, 4]
    assert times(early, 'correction') == [2]
    assert times(early, 'source_feedback') == [2, 4, 6, 8]
    assert times(early, 'accuracy_cue') == list(range(2, 13))
    assert times(late, 'exposure') == [1, 2, 3, 4]
    assert times(late, 'exposure_prevented') == []
    assert times(late, 'correction') == [5]
    assert times(late, 'source_feedback') == [5, 7, 9, 11]
    assert times(late, 'accuracy_cue') == list(range(5, 13))


def test_unselected_measures_do_not_schedule_actions():
    for start in (2, 5):
        frames = module.bundle_schedule(0, start)['frames']
        assert [f['time'] for f in frames if f['exposure']] == [1, 2, 3, 4]
        assert not any(f[k] for f in frames for k in
                       ('exposure_prevented', 'correction', 'source_feedback', 'accuracy_cue'))


def test_evaluator_executes_scheduled_events_in_order(monkeypatch):
    recorded = []
    original = module.Simulator.step
    def capture(self, event):
        recorded.append(event)
        return original(self, event)
    monkeypatch.setattr(module.Simulator, 'step', capture)
    module.evaluate_bundle(15, 5, ModelParams())
    # Two claims; each has 4 exposures, 1 correction, 4 feedbacks and 13 decisions.
    assert len(recorded) == 44
    for events, direction in ((recorded[:22], -1.0), (recorded[22:], 1.0)):
        assert [type(e).__name__ for e in events if e.time == 5] == [
            'CorrectionEvent', 'SourceFeedbackEvent', 'DecisionEvent']
        assert [e.direction for e in events if isinstance(e, module.CorrectionEvent)] == [direction]
        assert [e.time for e in events if isinstance(e, module.ExposureEvent)] == [1, 2, 3, 4]
        assert [e.time for e in events if isinstance(e, module.DecisionEvent) and e.accuracy_cue] == list(range(5, 13))


def test_export_schedule_and_numerical_reference_are_reproduced():
    path = Path(__file__).resolve().parents[1] / 'web/public/model/interventions.json'
    published = json.loads(path.read_text())
    generated = module.export_interventions()
    assert len(generated['schedules']) == 32
    assert generated['schedules'] == published['schedules']
    # Existing 96 bundle outcomes are preserved exactly by the scheduling refactor.
    assert generated['profiles'] == published['profiles']
