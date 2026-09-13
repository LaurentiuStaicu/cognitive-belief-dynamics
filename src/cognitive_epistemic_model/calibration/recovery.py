from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from ..updates import update_familiarity


def familiarity_trajectory(alpha_f: float, exposures: int, initial: float = 0.0) -> np.ndarray:
    out = [float(initial)]
    f = float(initial)
    for _ in range(exposures):
        f = update_familiarity(f, alpha_f)
        out.append(f)
    return np.asarray(out)


def recover_alpha_f(observed: np.ndarray, initial: float = 0.0) -> float:
    observed = np.asarray(observed, dtype=float)
    exposures = len(observed) - 1

    def residual(x: np.ndarray) -> np.ndarray:
        predicted = familiarity_trajectory(float(x[0]), exposures, initial=initial)
        return predicted - observed

    result = least_squares(residual, x0=np.array([0.3]), bounds=(0.0, 1.0))
    return float(result.x[0])
