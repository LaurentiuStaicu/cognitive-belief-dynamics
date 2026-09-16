from __future__ import annotations

from math import fsum, isclose


class ProbabilityUnavailableError(ValueError):
    """Raised when a consumer asks for probabilities that the registry does not provide."""


class InvalidProbabilityVectorError(ValueError):
    """Raised when explicit finite-scenario probabilities are malformed."""


def require_finite_scenario_probabilities(item: dict) -> tuple[float, ...]:
    """Return only explicit, valid finite-scenario probabilities.

    The function deliberately refuses to infer equal weights or derive weights
    from scenario spacing. It is the OA-6A fail-closed boundary for later
    decision-analysis consumers.
    """

    if item.get("quantification_status") != "FINITE_SCENARIOS":
        raise InvalidProbabilityVectorError("item is not a FINITE_SCENARIOS uncertainty")

    if item.get("probability_status") == "NOT_AVAILABLE":
        raise ProbabilityUnavailableError("finite scenarios have no registered probabilities")

    scenarios = item.get("finite_scenarios")
    probabilities = item.get("scenario_probabilities")
    if not isinstance(scenarios, list) or len(scenarios) < 2:
        raise InvalidProbabilityVectorError("finite_scenarios must contain at least two scenarios")
    if not isinstance(probabilities, list) or len(probabilities) != len(scenarios):
        raise InvalidProbabilityVectorError("scenario probability count must match scenario count")

    values = tuple(float(value) for value in probabilities)
    if any(value < 0.0 or value > 1.0 for value in values):
        raise InvalidProbabilityVectorError("scenario probabilities must be within [0, 1]")
    if not isclose(fsum(values), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise InvalidProbabilityVectorError("scenario probabilities must sum to 1")

    return values
