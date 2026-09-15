from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import exp, isfinite


class PresentationFrame(str, Enum):
    CONFIRMATION = "confirmation"
    REFUTATION = "refutation"


class PresentationModel(str, Enum):
    NULL = "null"
    FRAME_ONLY = "frame_only"
    FRAME_CONGRUENCE = "frame_congruence"


@dataclass(frozen=True)
class SemanticProposition:
    proposition_id: str
    semantic_stance: float
    fact_compatible: bool = True

    def __post_init__(self) -> None:
        if not self.proposition_id:
            raise ValueError("proposition_id must be non-empty")
        if not isfinite(self.semantic_stance) or not -1.0 <= self.semantic_stance <= 1.0:
            raise ValueError("semantic_stance must be finite and in [-1, 1]")


@dataclass(frozen=True)
class PresentedMessage:
    proposition: SemanticProposition
    frame: PresentationFrame
    semantic_signature: str

    def __post_init__(self) -> None:
        if not self.semantic_signature:
            raise ValueError("semantic_signature must be non-empty")


@dataclass(frozen=True)
class EngagementParams:
    intercept: float = -0.40
    beta_frame: float = 0.15
    beta_congruence: float = 0.35
    beta_interaction: float = 0.15

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")


def logistic(value: float) -> float:
    return 1.0 / (1.0 + exp(-value))


def frame_code(frame: PresentationFrame) -> float:
    return 1.0 if frame is PresentationFrame.CONFIRMATION else -1.0


def prior_attitude_congruence(
    *,
    prior_stance: float,
    message_stance: float,
) -> float:
    """Task-specific prior-attitude congruence in [-1, 1].

    This relational quantity is not ideology, party identity, personality, or a
    global confirmation-bias score.
    """
    for name, value in (("prior_stance", prior_stance), ("message_stance", message_stance)):
        if not isfinite(value) or not -1.0 <= value <= 1.0:
            raise ValueError(f"{name} must be finite and in [-1, 1]")
    return prior_stance * message_stance


def active_engagement_probability(
    *,
    frame: PresentationFrame,
    congruence: float,
    model: PresentationModel,
    params: EngagementParams | None = None,
) -> float:
    """Reference M1.E2 active-engagement propensity.

    Published experiments anchor the qualitative framing and moderation patterns.
    These coefficients are demonstrative and are not fitted to published effect sizes.
    """
    params = params or EngagementParams()
    if not isfinite(congruence) or not -1.0 <= congruence <= 1.0:
        raise ValueError("congruence must be finite and in [-1, 1]")

    if model is PresentationModel.NULL:
        score = params.intercept
    elif model is PresentationModel.FRAME_ONLY:
        score = params.intercept + params.beta_frame * frame_code(frame)
    elif model is PresentationModel.FRAME_CONGRUENCE:
        f = frame_code(frame)
        score = (
            params.intercept
            + params.beta_frame * f
            + params.beta_congruence * congruence
            + params.beta_interaction * f * congruence
        )
    else:
        raise ValueError(f"unsupported model: {model}")

    return logistic(score)


def semantic_equivalent_pair(
    proposition_id: str = "P1",
    semantic_stance: float = 1.0,
) -> tuple[PresentedMessage, PresentedMessage]:
    """Return confirmation/refutation forms with an identical semantic signature."""
    proposition = SemanticProposition(
        proposition_id=proposition_id,
        semantic_stance=semantic_stance,
        fact_compatible=True,
    )
    signature = f"{proposition_id}:semantic-equivalent"
    return (
        PresentedMessage(proposition, PresentationFrame.CONFIRMATION, signature),
        PresentedMessage(proposition, PresentationFrame.REFUTATION, signature),
    )


def reference_presentation_experiment() -> dict:
    confirmation, refutation = semantic_equivalent_pair()
    params = EngagementParams()
    conditions = {}

    for audience, prior_stance in (("congruent", 1.0), ("counter_attitudinal", -1.0)):
        congruence = prior_attitude_congruence(
            prior_stance=prior_stance,
            message_stance=confirmation.proposition.semantic_stance,
        )
        models = {}
        for model in PresentationModel:
            models[model.value] = {
                "confirmation": active_engagement_probability(
                    frame=PresentationFrame.CONFIRMATION,
                    congruence=congruence,
                    model=model,
                    params=params,
                ),
                "refutation": active_engagement_probability(
                    frame=PresentationFrame.REFUTATION,
                    congruence=congruence,
                    model=model,
                    params=params,
                ),
            }
            models[model.value]["contrast"] = (
                models[model.value]["confirmation"] - models[model.value]["refutation"]
            )

        conditions[audience] = {
            "prior_stance": prior_stance,
            "message_stance": confirmation.proposition.semantic_stance,
            "congruence": congruence,
            "models": models,
        }

    return {
        "id": "M1.E2",
        "purpose": "MODEL_DISCRIMINATION_DEMONSTRATION",
        "semantic_proposition_id": confirmation.proposition.proposition_id,
        "semantic_signature": confirmation.semantic_signature,
        "fact_compatible": confirmation.proposition.fact_compatible,
        "frames": [confirmation.frame.value, refutation.frame.value],
        "parameters": {
            "intercept": params.intercept,
            "beta_frame": params.beta_frame,
            "beta_congruence": params.beta_congruence,
            "beta_interaction": params.beta_interaction,
        },
        "conditions": conditions,
        "empirical_target_ids": [
            "TARGET.M1.E2.ARUGUETE_2024",
            "TARGET.M1.E2.ALVARADO_2026",
        ],
        "interpretation_boundary": (
            "Reference model comparison only. The studies support a confirmation/refutation "
            "engagement pattern and a congruence interaction, but do not identify these "
            "specific coefficients or this logistic functional form."
        ),
    }
