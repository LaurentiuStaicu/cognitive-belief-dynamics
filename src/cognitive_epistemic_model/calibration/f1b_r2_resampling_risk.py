from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class ResamplingRiskBoundary:
    n: int
    lower: int
    upper: int
    spending_allowance: float
    cumulative_lower_probability: float
    cumulative_upper_probability: float
    survivor_probability: float


@dataclass(frozen=True)
class ResamplingRiskBoundaryTable:
    alpha: float
    epsilon: float
    halfspend: float
    max_n: int
    probability_tolerance: float
    rows: tuple[ResamplingRiskBoundary, ...]

    def row(self, n: int) -> ResamplingRiskBoundary:
        if not 1 <= int(n) <= self.max_n:
            raise ValueError("n lies outside the generated boundary table")
        return self.rows[int(n) - 1]

    def to_dict(self) -> dict:
        return {
            "alpha": self.alpha,
            "epsilon": self.epsilon,
            "halfspend": self.halfspend,
            "max_n": self.max_n,
            "probability_tolerance": self.probability_tolerance,
            "rows": [asdict(row) for row in self.rows],
        }


@dataclass(frozen=True)
class ResamplingRiskReplayResult:
    status: str
    decision: str | None
    stopping_n: int | None
    stopping_sum: int | None
    boundary_hit: str | None
    terminal_n: int
    terminal_sum: int
    terminal_lower: int
    terminal_upper: int
    failure_n: int | None


def _validate_parameters(
    *,
    alpha: float,
    epsilon: float,
    halfspend: float,
    max_n: int,
    probability_tolerance: float,
) -> None:
    if not 0.0 < float(alpha) < 1.0:
        raise ValueError("alpha must lie strictly inside (0,1)")
    if not 0.0 < float(epsilon) <= 0.25:
        raise ValueError("epsilon must lie inside (0,0.25]")
    if float(halfspend) <= 0.0:
        raise ValueError("halfspend must be positive")
    if int(max_n) < 1:
        raise ValueError("max_n must be positive")
    if not 0.0 < float(probability_tolerance) < 1e-6:
        raise ValueError(
            "probability_tolerance must be positive and below 1e-6"
        )


def spending_allowance(
    n: int,
    *,
    epsilon: float,
    halfspend: float,
) -> float:
    if int(n) < 1:
        raise ValueError("n must be positive")
    if not 0.0 < float(epsilon) <= 0.25:
        raise ValueError("epsilon must lie inside (0,0.25]")
    if float(halfspend) <= 0.0:
        raise ValueError("halfspend must be positive")
    return float(epsilon) * int(n) / (float(halfspend) + int(n))


def generate_resampling_risk_boundaries(
    *,
    alpha: float,
    epsilon: float,
    halfspend: float,
    max_n: int,
    probability_tolerance: float = 1e-12,
) -> ResamplingRiskBoundaryTable:
    """Generate Gandy-style sequential boundaries by exact recursion.

    The state vector contains the unconditional probability, under p=alpha,
    of every Bernoulli partial sum that has not crossed either boundary yet.
    At each step the upper and lower boundaries spend no more than the
    prospectively declared epsilon_n allowance.
    """
    _validate_parameters(
        alpha=alpha,
        epsilon=epsilon,
        halfspend=halfspend,
        max_n=max_n,
        probability_tolerance=probability_tolerance,
    )

    alpha = float(alpha)
    epsilon = float(epsilon)
    halfspend = float(halfspend)
    max_n = int(max_n)
    tolerance = float(probability_tolerance)

    upper_error = 0.0
    lower_error = 0.0
    survivor_offset = 0
    survivor = np.asarray([1.0 - alpha, alpha], dtype=float)

    rows: list[ResamplingRiskBoundary] = [
        ResamplingRiskBoundary(
            n=1,
            lower=-1,
            upper=2,
            spending_allowance=spending_allowance(
                1,
                epsilon=epsilon,
                halfspend=halfspend,
            ),
            cumulative_lower_probability=0.0,
            cumulative_upper_probability=0.0,
            survivor_probability=1.0,
        )
    ]

    for n in range(2, max_n + 1):
        raw = np.zeros(survivor.size + 1, dtype=float)
        raw[:-1] += survivor * (1.0 - alpha)
        raw[1:] += survivor * alpha

        raw_offset = survivor_offset
        raw_maximum = raw_offset + raw.size - 1
        sums = np.arange(raw_offset, raw_maximum + 1, dtype=int)
        allowance = spending_allowance(
            n,
            epsilon=epsilon,
            halfspend=halfspend,
        )

        raw_total = float(np.sum(raw))

        if upper_error + raw_total <= allowance:
            upper = 1
        else:
            upper_tail = np.cumsum(raw[::-1])[::-1]
            candidates = np.flatnonzero(
                upper_error + upper_tail <= allowance
            )
            upper = (
                raw_offset + int(candidates[0])
                if candidates.size
                else raw_maximum + 1
            )

        if lower_error + raw_total <= allowance:
            lower = n
        else:
            lower_cdf = np.cumsum(raw)
            candidates = np.flatnonzero(
                lower_error + lower_cdf <= allowance
            )
            lower = (
                raw_offset + int(candidates[-1])
                if candidates.size
                else raw_offset - 1
            )

        if lower >= upper:
            raise RuntimeError(
                "resampling-risk boundaries overlap; "
                "declared parameters are numerically invalid"
            )

        upper_hit = float(np.sum(raw[sums >= upper]))
        lower_hit = float(np.sum(raw[sums <= lower]))
        upper_error += upper_hit
        lower_error += lower_hit

        survivor_mask = (sums > lower) & (sums < upper)
        survivor_indices = np.flatnonzero(survivor_mask)
        if survivor_indices.size == 0:
            survivor = np.asarray([], dtype=float)
            survivor_offset = 0
        else:
            start = int(survivor_indices[0])
            stop = int(survivor_indices[-1]) + 1
            survivor = raw[start:stop].copy()
            survivor_offset = raw_offset + start

        survivor_probability = float(np.sum(survivor))
        total_probability = (
            survivor_probability + upper_error + lower_error
        )
        if abs(total_probability - 1.0) > tolerance:
            raise RuntimeError(
                "resampling-risk probability mass was not conserved"
            )
        if upper_error > allowance + tolerance:
            raise RuntimeError(
                "upper-boundary error probability exceeded spending allowance"
            )
        if lower_error > allowance + tolerance:
            raise RuntimeError(
                "lower-boundary error probability exceeded spending allowance"
            )

        rows.append(
            ResamplingRiskBoundary(
                n=n,
                lower=int(lower),
                upper=int(upper),
                spending_allowance=float(allowance),
                cumulative_lower_probability=float(lower_error),
                cumulative_upper_probability=float(upper_error),
                survivor_probability=survivor_probability,
            )
        )

    return ResamplingRiskBoundaryTable(
        alpha=alpha,
        epsilon=epsilon,
        halfspend=halfspend,
        max_n=max_n,
        probability_tolerance=tolerance,
        rows=tuple(rows),
    )


def replay_exceedance_stream(
    stream: Iterable[int | bool | None],
    *,
    boundaries: ResamplingRiskBoundaryTable,
) -> ResamplingRiskReplayResult:
    """Replay a finite exceedance stream against frozen sequential bounds."""
    values = tuple(stream)
    if not values:
        raise ValueError("stream must contain at least one attempt")
    if len(values) > boundaries.max_n:
        raise ValueError("stream exceeds generated boundary table")

    partial_sum = 0
    for index, value in enumerate(values, start=1):
        if value is None:
            row = boundaries.row(index)
            return ResamplingRiskReplayResult(
                status="BOOTSTRAP_REFIT_FAILURE_UNRESOLVED",
                decision=None,
                stopping_n=None,
                stopping_sum=None,
                boundary_hit=None,
                terminal_n=index,
                terminal_sum=partial_sum,
                terminal_lower=row.lower,
                terminal_upper=row.upper,
                failure_n=index,
            )
        if isinstance(value, (bool, np.bool_)):
            integer = int(value)
        elif isinstance(value, (int, np.integer)) and int(value) in (0, 1):
            integer = int(value)
        else:
            raise ValueError("stream values must be 0, 1, bool, or None")

        partial_sum += integer
        row = boundaries.row(index)

        if partial_sum <= row.lower:
            return ResamplingRiskReplayResult(
                status="SEQUENTIAL_DECISION",
                decision="REJECT_P_LE_ALPHA",
                stopping_n=index,
                stopping_sum=partial_sum,
                boundary_hit="LOWER",
                terminal_n=index,
                terminal_sum=partial_sum,
                terminal_lower=row.lower,
                terminal_upper=row.upper,
                failure_n=None,
            )
        if partial_sum >= row.upper:
            return ResamplingRiskReplayResult(
                status="SEQUENTIAL_DECISION",
                decision="NOT_REJECT_P_GT_ALPHA",
                stopping_n=index,
                stopping_sum=partial_sum,
                boundary_hit="UPPER",
                terminal_n=index,
                terminal_sum=partial_sum,
                terminal_lower=row.lower,
                terminal_upper=row.upper,
                failure_n=None,
            )

    row = boundaries.row(len(values))
    return ResamplingRiskReplayResult(
        status="SEQUENTIAL_UNRESOLVED",
        decision=None,
        stopping_n=None,
        stopping_sum=None,
        boundary_hit=None,
        terminal_n=len(values),
        terminal_sum=partial_sum,
        terminal_lower=row.lower,
        terminal_upper=row.upper,
        failure_n=None,
    )
