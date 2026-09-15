from __future__ import annotations

import math

import pytest

from cognitive_epistemic_model.access import (
    AccessModel,
    AccessParams,
    HeadlinePreview,
    access_outcome,
    access_probability,
    reference_access_experiment,
    reference_headline_pair,
)


def test_reference_headline_pair_holds_registered_invariants_fixed():
    lower, higher = reference_headline_pair()

    assert lower.hneg == 0
    assert higher.hneg == 1

    for attribute in (
        "story_id",
        "source_id",
        "image_id",
        "fact_compatible",
        "preview_impression",
    ):
        assert getattr(lower, attribute) == getattr(higher, attribute)

    assert lower.preview_impression is True
    assert lower.fact_compatible is True


def test_null_model_converges_across_hneg_conditions():
    lower, higher = reference_headline_pair()

    p_lower = access_probability(preview=lower, model=AccessModel.NULL)
    p_higher = access_probability(preview=higher, model=AccessModel.NULL)

    assert p_lower == pytest.approx(p_higher)


def test_selected_hneg_model_has_registered_direction():
    lower, higher = reference_headline_pair()

    p_lower = access_probability(
        preview=lower,
        model=AccessModel.HEADLINE_NEGATIVITY,
    )
    p_higher = access_probability(
        preview=higher,
        model=AccessModel.HEADLINE_NEGATIVITY,
    )

    assert p_higher > p_lower


def test_reference_parameter_is_demonstrative_not_published_beta():
    params = AccessParams()

    assert params.beta_hneg > 0
    assert params.beta_hneg != pytest.approx(0.015)


def test_paccess_requires_registered_preview_impression():
    preview = HeadlinePreview(
        headline_id="H1",
        story_id="S1",
        source_id="SRC1",
        hneg=1,
        preview_impression=False,
    )

    with pytest.raises(ValueError, match="PreviewImpression"):
        access_probability(
            preview=preview,
            model=AccessModel.HEADLINE_NEGATIVITY,
        )


def test_non_click_preserves_preview_impression():
    preview = HeadlinePreview(
        headline_id="H1",
        story_id="S1",
        source_id="SRC1",
        hneg=0,
        preview_impression=True,
    )

    p = access_probability(preview=preview, model=AccessModel.NULL)
    result = access_outcome(probability=p, draw=0.99)

    assert result is False
    assert preview.preview_impression is True


@pytest.mark.parametrize(
    "kwargs",
    [
        {"headline_id": "", "story_id": "S", "source_id": "SRC", "hneg": 0},
        {"headline_id": "H", "story_id": "", "source_id": "SRC", "hneg": 0},
        {"headline_id": "H", "story_id": "S", "source_id": "", "hneg": 0},
        {"headline_id": "H", "story_id": "S", "source_id": "SRC", "hneg": -1},
        {"headline_id": "H", "story_id": "S", "source_id": "SRC", "hneg": 2},
    ],
)
def test_headline_preview_rejects_invalid_reference_inputs(kwargs):
    with pytest.raises(ValueError):
        HeadlinePreview(**kwargs)


@pytest.mark.parametrize(
    ("probability", "draw"),
    [
        (-0.1, 0.5),
        (1.1, 0.5),
        (0.5, -0.1),
        (0.5, 1.1),
        (math.nan, 0.5),
        (0.5, math.nan),
    ],
)
def test_access_outcome_rejects_invalid_probability_or_draw(probability, draw):
    with pytest.raises(ValueError):
        access_outcome(probability=probability, draw=draw)


def test_reference_experiment_discriminates_null_from_hneg_without_downstream_state():
    experiment = reference_access_experiment()

    lower = experiment["conditions"]["lower_negativity"]
    higher = experiment["conditions"]["higher_negativity"]

    null_lower = lower["models"]["null"]["p_access"]
    null_higher = higher["models"]["null"]["p_access"]
    hneg_lower = lower["models"]["headline_negativity"]["p_access"]
    hneg_higher = higher["models"]["headline_negativity"]["p_access"]

    assert null_lower == pytest.approx(null_higher)
    assert hneg_higher > hneg_lower

    assert experiment["selected_cue"] == "Hneg"
    assert experiment["cue_encoding"]["runtime_sentiment_analysis"] is False
    assert experiment["parameters"]["calibrated"] is False

    def all_keys(value):
        if isinstance(value, dict):
            for key, item in value.items():
                yield key
                yield from all_keys(item)
        elif isinstance(value, list):
            for item in value:
                yield from all_keys(item)

    keys = set(all_keys(experiment))
    for forbidden in (
        "belief",
        "Share",
        "Aissue",
        "Pengage",
        "EngageIntent",
    ):
        assert forbidden not in keys


def test_reference_experiment_illustrative_draw_is_not_validation_target():
    experiment = reference_access_experiment()
    assert experiment["purpose"] == "MODEL_DISCRIMINATION_DEMONSTRATION"
    assert "Directional" in experiment["interpretation_boundary"]
