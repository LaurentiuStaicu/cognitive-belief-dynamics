from cognitive_epistemic_model.presentation import (
    EngagementParams,
    PresentationFrame,
    PresentationModel,
    active_engagement_probability,
    prior_attitude_congruence,
    reference_presentation_experiment,
    semantic_equivalent_pair,
)


def test_val_m1_002_semantic_equivalent_confirmation_exceeds_refutation_in_frame_only():
    confirmation, refutation = semantic_equivalent_pair()
    assert confirmation.semantic_signature == refutation.semantic_signature
    assert confirmation.proposition.fact_compatible
    assert refutation.proposition.fact_compatible

    p_confirm = active_engagement_probability(
        frame=PresentationFrame.CONFIRMATION,
        congruence=1.0,
        model=PresentationModel.FRAME_ONLY,
    )
    p_refute = active_engagement_probability(
        frame=PresentationFrame.REFUTATION,
        congruence=1.0,
        model=PresentationModel.FRAME_ONLY,
    )
    assert p_confirm > p_refute


def test_val_m1_003_confirmation_advantage_is_larger_when_congruent():
    congruent = prior_attitude_congruence(prior_stance=1.0, message_stance=1.0)
    counter = prior_attitude_congruence(prior_stance=-1.0, message_stance=1.0)

    c_confirm = active_engagement_probability(
        frame=PresentationFrame.CONFIRMATION,
        congruence=congruent,
        model=PresentationModel.FRAME_CONGRUENCE,
    )
    c_refute = active_engagement_probability(
        frame=PresentationFrame.REFUTATION,
        congruence=congruent,
        model=PresentationModel.FRAME_CONGRUENCE,
    )
    x_confirm = active_engagement_probability(
        frame=PresentationFrame.CONFIRMATION,
        congruence=counter,
        model=PresentationModel.FRAME_CONGRUENCE,
    )
    x_refute = active_engagement_probability(
        frame=PresentationFrame.REFUTATION,
        congruence=counter,
        model=PresentationModel.FRAME_CONGRUENCE,
    )

    assert (c_confirm - c_refute) > (x_confirm - x_refute)
    assert abs(x_confirm - x_refute) < 1e-12


def test_val_m1_n02_normalized_frame_null_eliminates_difference():
    params = EngagementParams()
    for congruence in (-1.0, 1.0):
        confirmation = active_engagement_probability(
            frame=PresentationFrame.CONFIRMATION,
            congruence=congruence,
            model=PresentationModel.NULL,
            params=params,
        )
        refutation = active_engagement_probability(
            frame=PresentationFrame.REFUTATION,
            congruence=congruence,
            model=PresentationModel.NULL,
            params=params,
        )
        assert confirmation == refutation


def test_val_m1_n03_engagement_intent_model_is_separate_from_m0_share():
    experiment = reference_presentation_experiment()
    assert experiment["purpose"] == "MODEL_DISCRIMINATION_DEMONSTRATION"
    assert "share" not in experiment
    assert "Share" not in experiment
    assert experiment["conditions"]["congruent"]["models"]["frame_congruence"]["contrast"] > 0
    assert (
        experiment["conditions"]["counter_attitudinal"]["models"]["frame_congruence"]["contrast"]
        == 0
    )
