from __future__ import annotations

import math

_EPS = 1e-12


def clamp01(x: float) -> float:
    return min(1.0, max(0.0, float(x)))


def logit(p: float) -> float:
    p = min(1.0 - _EPS, max(_EPS, float(p)))
    return math.log(p / (1.0 - p))


def logistic(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)
