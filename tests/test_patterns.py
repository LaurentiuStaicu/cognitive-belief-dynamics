from cognitive_epistemic_model.model import accuracy_weight, compute_belief, share_probability
from cognitive_epistemic_model.state import ModelParams
from cognitive_epistemic_model.updates import decay_correction, update_familiarity

P = ModelParams()


def belief(*, familiarity=0.0, correction=0.0, direction=0.0, evidence=0.0, reliability=0.5):
    return compute_belief(
        prior_belief=0.5,
        familiarity=familiarity,
        correction_access=correction,
        correction_direction=direction,
        evidence_signal=evidence,
        reliability_estimate=reliability,
        params=P,
    )[0]


def test_val_m0_001_illusory_truth_pattern():
    f0 = 0.0
    f1 = update_familiarity(f0, P.alpha_f)
    f2 = update_familiarity(f1, P.alpha_f)
    assert belief(familiarity=f2) > belief(familiarity=f1) > belief(familiarity=f0)


def test_val_m0_002_correction_and_regression():
    f = update_familiarity(update_familiarity(0.0, P.alpha_f), P.alpha_f)
    before = belief(familiarity=f)
    immediately = belief(familiarity=f, correction=0.8, direction=-1.0)
    later_c = decay_correction(0.8, P.lambda_c, 20.0)
    later = belief(familiarity=f, correction=later_c, direction=-1.0)
    assert immediately < before
    assert later > immediately


def test_val_m0_003_source_reliability_weighting():
    low = belief(evidence=0.8, reliability=0.55)
    high = belief(evidence=0.8, reliability=0.90)
    assert high > low


def test_val_m0_004_accuracy_salience_reduces_false_sharing_when_reward_competes():
    b = 0.2
    w0 = accuracy_weight(0.25, False, P.beta_accuracy_cue)
    w1 = accuracy_weight(0.25, True, P.beta_accuracy_cue)
    p0 = share_probability(belief=b, accuracy_weight_value=w0, reward_context=1.0, sharing_bias=0.0, params=P)
    p1 = share_probability(belief=b, accuracy_weight_value=w1, reward_context=1.0, sharing_bias=0.0, params=P)
    assert p1 < p0


def test_val_m0_n01_belief_not_action():
    b = 0.15
    w = 0.05
    p = share_probability(belief=b, accuracy_weight_value=w, reward_context=3.0, sharing_bias=0.0, params=P)
    assert p > 0.5
