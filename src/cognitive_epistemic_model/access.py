from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from .mathutils import logistic


class AccessModel(str, Enum):
    NULL = "null"
    HEADLINE_NEGATIVITY = "headline_negativity"


@dataclass(frozen=True)
class HeadlinePreview:
    """One rendered headline preview in the M1.E3 reference task.

    hneg is the precomputed controlled cue frozen in Phase A:
    0 = lower-negativity/control condition, 1 = higher-negativity condition.

    It is deliberately not a runtime sentiment score and not the continuous
    LIWC negative-word proportion used by the empirical source.
    """

    headline_id: str
    story_id: str
    source_id: str
    hneg: int
    preview_impression: bool = True
    fact_compatible: bool = True
    image_id: str | None = None

    def __post_init__(self) -> None:
        if not self.headline_id or not self.story_id or not self.source_id:
            raise ValueError("headline_id, story_id and source_id must be non-empty")
        if self.hneg not in (0, 1):
            raise ValueError("hneg must be the controlled binary cue 0 or 1")
        if not isinstance(self.preview_impression, bool):
            raise ValueError("preview_impression must be boolean")
        if not isinstance(self.fact_compatible, bool):
            raise ValueError("fact_compatible must be boolean")
        if self.image_id is not None and not self.image_id:
            raise ValueError("image_id must be non-empty when provided")


@dataclass(frozen=True)
class AccessParams:
    """Demonstrative M1.E3 reference parameters.

    These values are not fitted to Robertson et al. (2023), and beta_hneg is
    not a translation of the published standardized coefficient or the reported
    approximate 2.3% CTR change.
    """

    intercept: float = -2.0
    beta_hneg: float = 0.20

    def __post_init__(self) -> None:
        if not isfinite(self.intercept):
            raise ValueError("intercept must be finite")
        if not isfinite(self.beta_hneg) or self.beta_hneg < 0.0:
            raise ValueError("beta_hneg must be finite and non-negative")


def access_probability(
    *,
    preview: HeadlinePreview,
    model: AccessModel,
    params: AccessParams | None = None,
) -> float:
    """Return Paccess conditional on a registered preview impression.

    The NULL model ignores headline negativity. The candidate model adds only
    the controlled Hneg cue. No downstream cognition or action state is read or
    mutated by this function.
    """
    if not preview.preview_impression:
        raise ValueError("Paccess is conditional on PreviewImpression = true")

    params = params or AccessParams()

    if model is AccessModel.NULL:
        score = params.intercept
    elif model is AccessModel.HEADLINE_NEGATIVITY:
        score = params.intercept + params.beta_hneg * preview.hneg
    else:
        raise ValueError(f"unsupported access model: {model}")

    return logistic(score)


def access_outcome(*, probability: float, draw: float) -> bool:
    """Reference open/click outcome for an illustrative Bernoulli draw."""
    for name, value in (("probability", probability), ("draw", draw)):
        if not isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be finite and in [0, 1]")
    return draw < probability


def reference_headline_pair() -> tuple[HeadlinePreview, HeadlinePreview]:
    """Controlled M1.E3 pair differing only in the registered Hneg cue."""
    common = {
        "story_id": "STORY.M1.E3.REFERENCE",
        "source_id": "SOURCE.M1.E3.REFERENCE",
        "preview_impression": True,
        "fact_compatible": True,
        "image_id": "IMAGE.M1.E3.FIXED",
    }
    return (
        HeadlinePreview(
            headline_id="HEADLINE.M1.E3.LOWER_NEGATIVITY",
            hneg=0,
            **common,
        ),
        HeadlinePreview(
            headline_id="HEADLINE.M1.E3.HIGHER_NEGATIVITY",
            hneg=1,
            **common,
        ),
    )


def reference_access_experiment() -> dict:
    """Deterministic NULL-vs-Hneg model-discrimination experiment."""
    lower, higher = reference_headline_pair()
    params = AccessParams()
    illustrative_draw = 0.13

    def condition(preview: HeadlinePreview) -> dict:
        null_p = access_probability(
            preview=preview,
            model=AccessModel.NULL,
            params=params,
        )
        hneg_p = access_probability(
            preview=preview,
            model=AccessModel.HEADLINE_NEGATIVITY,
            params=params,
        )
        return {
            "headline_id": preview.headline_id,
            "story_id": preview.story_id,
            "source_id": preview.source_id,
            "image_id": preview.image_id,
            "fact_compatible": preview.fact_compatible,
            "preview_impression": preview.preview_impression,
            "hneg": preview.hneg,
            "models": {
                AccessModel.NULL.value: {
                    "p_access": null_p,
                    "access": access_outcome(
                        probability=null_p,
                        draw=illustrative_draw,
                    ),
                },
                AccessModel.HEADLINE_NEGATIVITY.value: {
                    "p_access": hneg_p,
                    "access": access_outcome(
                        probability=hneg_p,
                        draw=illustrative_draw,
                    ),
                },
            },
        }

    conditions = {
        "lower_negativity": condition(lower),
        "higher_negativity": condition(higher),
    }

    return {
        "id": "M1.E3",
        "purpose": "MODEL_DISCRIMINATION_DEMONSTRATION",
        "selected_cue": "Hneg",
        "cue_encoding": {
            "type": "PRECOMPUTED_CONTROLLED_CUE",
            "control": 0,
            "treatment": 1,
            "runtime_sentiment_analysis": False,
        },
        "parameters": {
            "intercept": params.intercept,
            "beta_hneg": params.beta_hneg,
            "calibrated": False,
        },
        "illustrative_access_draw": illustrative_draw,
        "conditions": conditions,
        "empirical_target_id": "TARGET.M1.E3.ROBERTSON_2023",
        "validation_pattern_ids": [
            "VAL.M1.004",
            "VAL.M1.N04",
            "VAL.M1.N05",
            "VAL.M1.N06",
        ],
        "interpretation_boundary": (
            "Directional model-discrimination demonstration only. Hneg is a binary "
            "precomputed condition, not the source study's continuous LIWC score. "
            "The reference intercept and beta_hneg are demonstrative and are not "
            "fitted to the published coefficient or CTR magnitude. Access is not "
            "attention, reading completion, belief, engagement intent, or sharing."
        ),
    }
