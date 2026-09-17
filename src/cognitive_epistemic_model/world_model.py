from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log2


class WorldModelInputError(ValueError):
    """Raised when a normative world-model update would require invented evidence."""


@dataclass(frozen=True)
class PropositionState:
    """Narrow normative proposition state for MOD.14.

    This is deliberately not the descriptive CEM belief state B. It is a
    proposition-level reference computation whose inputs must come from an
    explicit domain-specific measurement model.
    """

    probability: float
    uncertainty: float
    cumulative_log2_likelihood_ratio: float = 0.0
    update_count: int = 0


def _probability(value: float) -> float:
    value = float(value)
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise WorldModelInputError("probability must be finite and within [0, 1]")
    return value


def _likelihood_ratio(value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise WorldModelInputError("likelihood ratio must be finite and > 0")
    return value


def binary_uncertainty(probability: float) -> float:
    """Return normalized binary Shannon entropy in [0, 1]."""

    p = _probability(probability)
    if p in (0.0, 1.0):
        return 0.0
    return -(p * log2(p) + (1.0 - p) * log2(1.0 - p))


def bayes_update(prior_probability: float, likelihood_ratio: float) -> float:
    """Apply the declared MOD.14 odds-form Bayesian reference update.

    ``likelihood_ratio`` is never inferred from familiarity, source trust,
    agreement, attention or any other psychological cue. Consumers must supply
    a defensible diagnostic LR from the relevant measurement model.
    """

    p0 = _probability(prior_probability)
    lr = _likelihood_ratio(likelihood_ratio)
    if p0 == 0.0:
        return 0.0
    if p0 == 1.0:
        return 1.0
    numerator = p0 * lr
    return numerator / (numerator + (1.0 - p0))


def initial_state(prior_probability: float) -> PropositionState:
    p = _probability(prior_probability)
    return PropositionState(probability=p, uncertainty=binary_uncertainty(p))


def update_state(state: PropositionState, likelihood_ratio: float) -> PropositionState:
    lr = _likelihood_ratio(likelihood_ratio)
    posterior = bayes_update(state.probability, lr)
    return PropositionState(
        probability=posterior,
        uncertainty=binary_uncertainty(posterior),
        cumulative_log2_likelihood_ratio=(
            state.cumulative_log2_likelihood_ratio + log2(lr)
        ),
        update_count=state.update_count + 1,
    )
