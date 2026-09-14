"""Illustrative intervention bundles evaluated with M0, not calibrated policy effects."""
from . import __version__
from dataclasses import asdict, replace
from statistics import mean
from .events import CorrectionEvent, DecisionEvent, ExposureEvent, SourceFeedbackEvent
from .simulation import Simulator
from .state import AgentState, ModelParams

LEVERS = [
    {'id':'repetition','bit':1,'label':{'ro':'Reducerea repetiției','en':'Reduce repetition'},'factor':'Nexp → F → B → P(share)',
     'action':{'ro':'După activare, elimină expunerile suplimentare la pașii 2–4, pentru ambele tipuri de afirmații.','en':'After activation, remove additional exposures at steps 2–4, for both claim types.'}},
    {'id':'correction','bit':2,'label':{'ro':'Context corectiv verificat','en':'Verified corrective context'},'factor':'C → B → P(share)',
     'action':{'ro':'La activare, adaugă context fact-check corect: negativ pentru afirmația falsă, pozitiv pentru cea adevărată.','en':'At activation, add correct fact-check context: negative for the false claim, positive for the true claim.'}},
    {'id':'accuracy','bit':4,'label':{'ro':'Indiciu de acuratețe','en':'Accuracy cue'},'factor':'W → P(share)',
     'action':{'ro':'De la activare, crește ponderea acurateții în decizie, fără schimbarea directă a convingerii.','en':'From activation, increase accuracy weight in decisions without directly changing belief.'}},
    {'id':'source','bit':8,'label':{'ro':'Feedback verificabil despre sursă','en':'Verifiable source feedback'},'factor':'T × evidence → B → P(share)',
     'action':{'ro':'Patru confirmări corecte la interval de doi pași ajută agentul să recunoască sursa informativă.','en':'Four correct confirmations two steps apart help the agent recognize the informative source.'}},
]

def evaluate_bundle(mask: int, start: int, params: ModelParams) -> dict:
    if mask not in range(16) or start not in (2,5):
        raise ValueError('mask must be 0..15 and start must be 2 or 5')
    outcomes = {}
    for claim_type, direction in [('false', -1.0), ('true', 1.0)]:
        # The evaluator defines a synthetic world. The agent receives evidence and
        # fact-check events, never a ground_truth argument to its belief function.
        agent = AgentState(agent_id='A', prior_belief={'C':0.5})
        sim = Simulator({'A':agent}, params=params, seed=7)
        shares=[]
        beliefs=[]
        for time in range(13):
            if time in (1,2,3,4) and not (mask & 1 and time >= start and time > 1):
                sim.step(ExposureEvent(time,'A','C','S'))
            if mask & 2 and time == start:
                sim.step(CorrectionEvent(time,'A','C',direction))
            if mask & 8 and time in (start,start+2,start+4,start+6):
                sim.step(SourceFeedbackEvent(time,'A','S',True))
            result=sim.step(DecisionEvent(time,'A','C','S',direction*0.6,reward_context=0.5,accuracy_cue=bool(mask & 4 and time>=start)))
            shares.append(result.share_probability)
            beliefs.append(result.belief)
        outcomes[claim_type+'_share']=mean(shares)
        outcomes[claim_type+'_belief']=mean(beliefs)
        outcomes[claim_type+'_share_path']=shares
    return {'mask':mask,'start':start,**outcomes}

def export_interventions() -> dict:
    profiles=[]
    for name, scale in [('low',0.7),('reference',1.0),('high',1.3)]:
        p=ModelParams()
        p=replace(p,beta_f=p.beta_f*scale,beta_correction=p.beta_correction*scale,beta_accuracy_cue=p.beta_accuracy_cue*scale)
        profiles.append({'id':name,'scale':scale,'parameters':asdict(p),'bundles':[evaluate_bundle(mask,start,p) for start in (2,5) for mask in range(16)]})
    return {'model_version':__version__,'purpose':'ILLUSTRATIVE_DECISION_SUPPORT','horizon':[0,12],
            'evaluation':'Expected sharing probabilities averaged over all 13 steps, separately for one false and one true synthetic claim; no population extrapolation.',
            'levers':LEVERS,'profiles':profiles}
