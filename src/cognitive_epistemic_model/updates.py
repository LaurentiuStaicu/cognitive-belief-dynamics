from __future__ import annotations

import math

from .mathutils import clamp01


def update_familiarity(current: float, alpha_f: float) -> float:
    """Bounded saturating exposure update."""
    return clamp01(current + alpha_f * (1.0 - current))


def encode_correction(current: float, alpha_c: float) -> float:
    return clamp01(current + alpha_c * (1.0 - current))


def decay_correction(current: float, lambda_c: float, delta_t: float) -> float:
    if delta_t < 0:
        raise ValueError("delta_t must be non-negative")
    return clamp01(current * math.exp(-lambda_c * delta_t))


def update_reliability(current: float, alpha_t: float, outcome: float) -> float:
    if outcome not in (0.0, 1.0):
        raise ValueError("outcome must be 0 or 1")
    return clamp01(current + alpha_t * (outcome - current))


def source_weight(reliability_estimate: float) -> float:
    """Reference bounded source weighting: [0,1] -> [-1,1]."""
    return 2.0 * clamp01(reliability_estimate) - 1.0
