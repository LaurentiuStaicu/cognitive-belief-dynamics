from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class InformationUnit:
    """One event-relevant unit available to an editorial selector.

    compatible_with_facts means the unit is permitted by the reference factual
    pool. It is deliberately separate from valence: negative information is not
    treated as false information.
    """

    unit_id: str
    event_id: str
    valence: float
    compatible_with_facts: bool = True

    def __post_init__(self) -> None:
        if not self.unit_id or not self.event_id:
            raise ValueError("unit_id and event_id must be non-empty")
        if not isfinite(self.valence) or not -1.0 <= self.valence <= 1.0:
            raise ValueError("valence must be finite and in [-1, 1]")


@dataclass(frozen=True)
class EditorialPolicy:
    """Reference editorial emphasis policy.

    emphasis=-1 favours negative-valence units, 0 favours neutral units and
    +1 favours positive-valence units. This is a transparent M1 reference
    policy, not an empirical estimate of newsroom behaviour.
    """

    emphasis: float = 0.0
    budget: int = 3

    def __post_init__(self) -> None:
        if not isfinite(self.emphasis) or not -1.0 <= self.emphasis <= 1.0:
            raise ValueError("emphasis must be finite and in [-1, 1]")
        if self.budget <= 0:
            raise ValueError("budget must be positive")


@dataclass(frozen=True)
class ObservedInformation:
    event_id: str
    units: tuple[InformationUnit, ...]
    balance: float


def _selection_score(unit: InformationUnit, emphasis: float) -> tuple[float, float, str]:
    if emphasis == 0.0:
        # Neutral reference: prefer information closest to neutral valence.
        return (-abs(unit.valence), -abs(unit.valence), unit.unit_id)
    # Signed emphasis: negative emphasis rewards negative units; positive
    # emphasis rewards positive units.
    return (emphasis * unit.valence, -abs(unit.valence), unit.unit_id)


def editorial_select(
    units: Iterable[InformationUnit],
    policy: EditorialPolicy,
    *,
    enabled: bool = True,
) -> ObservedInformation:
    """Return the factual information sample exposed by an editorial policy.

    When enabled=False the function is the nested null model: every available
    unit is observed, independent of editorial emphasis.
    """
    pool = tuple(units)
    if not pool:
        raise ValueError("information pool must not be empty")
    event_ids = {unit.event_id for unit in pool}
    if len(event_ids) != 1:
        raise ValueError("all units in a reference pool must describe one event")
    if not all(unit.compatible_with_facts for unit in pool):
        raise ValueError("M1.E1 reference pool requires fact-compatible units")

    if enabled:
        selected = tuple(
            sorted(
                pool,
                key=lambda unit: _selection_score(unit, policy.emphasis),
                reverse=True,
            )[: min(policy.budget, len(pool))]
        )
    else:
        selected = pool

    balance = sum(unit.valence for unit in selected) / len(selected)
    return ObservedInformation(
        event_id=next(iter(event_ids)),
        units=selected,
        balance=balance,
    )


def update_issue_appraisal(
    *,
    prior_appraisal: float,
    observed_balance: float,
    gain: float = 0.25,
) -> float:
    """Reference M1 mapping from observed sample balance to issue appraisal.

    This bounded linear update is deliberately simple and uncalibrated. The
    framing experiment supports a downstream treatment effect but does not
    uniquely identify this functional form or gain.
    """
    for name, value in (
        ("prior_appraisal", prior_appraisal),
        ("observed_balance", observed_balance),
    ):
        if not isfinite(value) or not -1.0 <= value <= 1.0:
            raise ValueError(f"{name} must be finite and in [-1, 1]")
    if not isfinite(gain) or gain < 0.0:
        raise ValueError("gain must be finite and non-negative")

    return max(-1.0, min(1.0, prior_appraisal + gain * observed_balance))


def reference_information_pool(event_id: str = "E1") -> tuple[InformationUnit, ...]:
    """Symmetric factual pool for the registered M1.E1 pattern test."""
    return tuple(
        InformationUnit(f"{event_id}.{i}", event_id, valence)
        for i, valence in enumerate((-1.0, -0.6, -0.2, 0.0, 0.2, 0.6, 1.0), start=1)
    )
