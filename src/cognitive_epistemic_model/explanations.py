"""Read-only decomposition of reference logs, checked against simulator outputs.

These terms explain latent equation scores. They are not causal attributions,
probability-point effects or intervention rankings.
"""
from .mathutils import logit
from .state import AgentState
from .updates import source_weight


def explain_reference_run(run: dict) -> dict:
    agent = AgentState(agent_id='A1', prior_belief={'C1': run['prior']})
    p = run['parameters']
    direction = 0.0
    previous = None
    frames = []
    for f in run['frames']:
        for event in f['events']:
            if event['event_type'] == 'CorrectionEvent':
                direction = event['payload']['direction']
        decision = f['events'][-1]['payload']
        belief_terms = {
            'prior': logit(run['prior']),
            'familiarity': p['beta_f'] * f['familiarity'],
            'evidence': p['beta_source_evidence'] * decision['evidence_signal'] * source_weight(f['reliability']),
            'correction': p['beta_correction'] * f['correction'] * direction,
        }
        share_terms = {
            'bias': agent.sharing_bias,
            'belief': f['accuracy_weight'] * (2.0 * f['belief'] - 1.0),
            'reward': p['beta_reward'] * (1.0 - f['accuracy_weight']) * decision['reward_context'],
        }
        frames.append({
            'time': f['time'], 'belief_terms': belief_terms,
            'belief_logit': f['latent_log_odds'], 'sharing_terms': share_terms,
            'sharing_logit': sum(share_terms.values()),
            'inputs': {'evidence_signal': decision['evidence_signal'],
                       'correction_direction': direction,
                       'accuracy_cue': decision['accuracy_cue'],
                       'accuracy_baseline': agent.accuracy_baseline,
                       'reward_context': decision['reward_context']},
            'changes': None if previous is None else {
                key: f[key] - previous[key] for key in
                ('familiarity', 'correction', 'reliability', 'belief', 'accuracy_weight', 'share_probability')
            },
        })
        previous = f
    return {'id': run['id'], 'frames': frames}
