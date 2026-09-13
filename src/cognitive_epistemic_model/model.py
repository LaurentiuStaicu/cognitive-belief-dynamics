from __future__ import annotations

from dataclasses import dataclass

from .mathutils import logit, logistic
from .state import ModelParams
from .updates import source_weight


@dataclass(frozen=True)
class Judgment:
    belief: float
    latent_log_odds: float
    accuracy_weight: float
    share_probability: float


def accuracy_weight(baseline: float, accuracy_cue: bool, beta_accuracy_cue: float) -> float:
    shift = beta_accuracy_cue if accuracy_cue else 0.0
    return logistic(logit(baseline) + shift)


def compute_belief(
    *,
    prior_belief: float,
    familiarity: float,
    correction_access: float,
    correction_direction: float,
    evidence_signal: float,
    reliability_estimate: float,
    params: ModelParams,
) -> tuple[float, float]:
    """Compute belief without access to ground truth.

    correction_direction is in [-1, 1], evidence_signal in [-1, 1].
    """
    if not -1.0 <= correction_direction <= 1.0:
        raise ValueError("correction_direction must be in [-1, 1]")
    if not -1.0 <= evidence_signal <= 1.0:
        raise ValueError("evidence_signal must be in [-1, 1]")

    z = (
        logit(prior_belief)
        + params.beta_f * familiarity
        + params.beta_source_evidence * evidence_signal * source_weight(reliability_estimate)
        + params.beta_correction * correction_access * correction_direction
    )
    return logistic(z), z


def share_probability(
    *,
    belief: float,
    accuracy_weight_value: float,
    reward_context: float,
    sharing_bias: float,
    params: ModelParams,
) -> float:
    u = (
        sharing_bias
        + accuracy_weight_value * (2.0 * belief - 1.0)
        + params.beta_reward * (1.0 - accuracy_weight_value) * reward_context
    )
    return logistic(u)


def judge(
    *,
    prior_belief: float,
    familiarity: float,
    correction_access: float,
    correction_direction: float,
    evidence_signal: float,
    reliability_estimate: float,
    accuracy_baseline: float,
    accuracy_cue: bool,
    reward_context: float,
    sharing_bias: float,
    params: ModelParams,
) -> Judgment:
    belief, z = compute_belief(
        prior_belief=prior_belief,
        familiarity=familiarity,
        correction_access=correction_access,
        correction_direction=correction_direction,
        evidence_signal=evidence_signal,
        reliability_estimate=reliability_estimate,
        params=params,
    )
    w = accuracy_weight(accuracy_baseline, accuracy_cue, params.beta_accuracy_cue)
    p_share = share_probability(
        belief=belief,
        accuracy_weight_value=w,
        reward_context=reward_context,
        sharing_bias=sharing_bias,
        params=params,
    )
    return Judgment(belief=belief, latent_log_odds=z, accuracy_weight=w, share_probability=p_share)
