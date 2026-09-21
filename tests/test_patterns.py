from cognitive_epistemic_model.model import accuracy_weight, compute_belief, share_probability
from cognitive_epistemic_model.state import ModelParams
from cognitive_epistemic_model.updates import decay_correction, update_familiarity, update_reliability

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


def test_val_m0_003_learned_source_reliability_weighting():
    initial = 0.5
    learned_unreliable = update_reliability(initial, P.alpha_t, 0.0)
    learned_reliable = update_reliability(initial, P.alpha_t, 1.0)
    assert learned_reliable > initial > learned_unreliable

    low = belief(evidence=0.8, reliability=learned_unreliable)
    high = belief(evidence=0.8, reliability=learned_reliable)
    assert high > low


def test_val_m0_004_accuracy_salience_improves_true_false_sharing_discernment():
    w0 = accuracy_weight(0.25, False, P.beta_accuracy_cue)
    w1 = accuracy_weight(0.25, True, P.beta_accuracy_cue)

    false_without = share_probability(
        belief=0.2, accuracy_weight_value=w0, reward_context=1.0,
        sharing_bias=0.0, params=P,
    )
    true_without = share_probability(
        belief=0.8, accuracy_weight_value=w0, reward_context=1.0,
        sharing_bias=0.0, params=P,
    )
    false_with = share_probability(
        belief=0.2, accuracy_weight_value=w1, reward_context=1.0,
        sharing_bias=0.0, params=P,
    )
    true_with = share_probability(
        belief=0.8, accuracy_weight_value=w1, reward_context=1.0,
        sharing_bias=0.0, params=P,
    )

    discernment_without = true_without - false_without
    discernment_with = true_with - false_with

    assert false_with < false_without
    assert discernment_with > discernment_without


def test_val_m0_n01_belief_not_action():
    b = 0.15
    w = 0.05
    p = share_probability(belief=b, accuracy_weight_value=w, reward_context=3.0, sharing_bias=0.0, params=P)
    assert p > 0.5
