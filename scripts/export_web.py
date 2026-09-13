"""Export canonical registries and deterministic reference runs for the static viewer."""
from dataclasses import asdict
import json
from pathlib import Path
from cognitive_epistemic_model.events import ExposureEvent, CorrectionEvent, DecisionEvent, SourceFeedbackEvent
from cognitive_epistemic_model.simulation import Simulator
from cognitive_epistemic_model.state import AgentState, ModelParams

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'web/public/model'

def reference_run(kind):
    agent = AgentState(agent_id='A1', prior_belief={'C1': 0.3})
    sim = Simulator({'A1': agent}, seed=7)
    frames = []
    for time in range(13):
        events = []
        if time in (1, 2, 3, 4):
            events.append(ExposureEvent(time, 'A1', 'C1', 'S1'))
        if kind == 'correction' and time == 5:
            events.append(CorrectionEvent(time, 'A1', 'C1'))
        if kind == 'source' and time in (2, 4, 6, 8):
            events.append(SourceFeedbackEvent(time, 'A1', 'S1', False))
        events.append(DecisionEvent(time, 'A1', 'C1', 'S1', evidence_signal=0.6 if kind == 'source' else 0.0, reward_context=0.5, accuracy_cue=kind == 'accuracy' and time >= 5))
        start = len(sim.log)
        sim.run(events)
        frames.append({'time':time, 'familiarity':agent.f('C1'), 'correction':agent.c('C1'), 'reliability':agent.t('S1'), 'events':[asdict(e) for e in sim.log[start:]], **sim.log[-1].observation})
    return {'id':kind, 'seed':7, 'prior':0.3, 'parameters':asdict(ModelParams()), 'frames':frames}

def export():
    DEST.mkdir(parents=True, exist_ok=True)
    for name in ('variables', 'links', 'modules', 'validation_tests', 'references'):
        (DEST / f'{name}.json').write_bytes((ROOT / 'model' / f'{name}.json').read_bytes())
    (DEST / 'runs.json').write_text(json.dumps({'model_version':'0.2.0a0','runs':[reference_run(k) for k in ('repetition','correction','source','accuracy')]}, indent=2)+'\n')

if __name__ == '__main__':
    export()
