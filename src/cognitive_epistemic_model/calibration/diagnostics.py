from __future__ import annotations

from dataclasses import asdict, replace
from math import exp
from typing import Iterable

import numpy as np

from ..model import accuracy_weight, compute_belief, share_probability
from ..state import ModelParams
from ..updates import encode_correction, update_familiarity, update_reliability

PARAMETER_NAMES = (
    "alpha_f",
    "alpha_c",
    "lambda_c",
    "alpha_t",
    "beta_f",
    "beta_source_evidence",
    "beta_correction",
    "beta_accuracy_cue",
    "beta_reward",
)


def m0_observable_vector(params: ModelParams) -> np.ndarray:
    """Deterministic M0 summaries used only for local diagnostics.

    The vector spans the four reference mechanism families. It is not empirical
    calibration data and it is not used by the simulator to produce reference runs.
    """
    outputs: list[float] = []

    familiarity = 0.0
    familiarity_path = []
    for _ in range(4):
        familiarity = update_familiarity(familiarity, params.alpha_f)
        familiarity_path.append(familiarity)
        outputs.append(familiarity)

    for f in familiarity_path:
        b, _ = compute_belief(
            prior_belief=0.3,
            familiarity=f,
            correction_access=0.0,
            correction_direction=0.0,
            evidence_signal=0.0,
            reliability_estimate=0.5,
            params=params,
        )
        outputs.append(b)

    c0 = encode_correction(0.0, params.alpha_c)
    for dt in (0.0, 2.0, 6.0, 12.0):
        c = c0 * exp(-params.lambda_c * dt)
        outputs.append(c)
        b, _ = compute_belief(
            prior_belief=0.3,
            familiarity=familiarity,
            correction_access=c,
            correction_direction=-1.0,
            evidence_signal=0.0,
            reliability_estimate=0.5,
            params=params,
        )
        outputs.append(b)

    reliability = 0.5
    for confirmed in (0.0, 1.0, 1.0, 1.0):
        reliability = update_reliability(reliability, params.alpha_t, confirmed)
        outputs.append(reliability)
        b, _ = compute_belief(
            prior_belief=0.3,
            familiarity=familiarity,
            correction_access=0.0,
            correction_direction=0.0,
            evidence_signal=0.6,
            reliability_estimate=reliability,
            params=params,
        )
        outputs.append(b)

    for belief in (0.2, 0.8):
        for cue in (False, True):
            w = accuracy_weight(0.25, cue, params.beta_accuracy_cue)
            outputs.append(w)
            outputs.append(
                share_probability(
                    belief=belief,
                    accuracy_weight_value=w,
                    reward_context=1.0,
                    sharing_bias=0.0,
                    params=params,
                )
            )

    return np.asarray(outputs, dtype=float)


def local_sensitivity_matrix(
    params: ModelParams | None = None,
    parameter_names: Iterable[str] = PARAMETER_NAMES,
    relative_step: float = 1e-4,
) -> tuple[np.ndarray, tuple[str, ...]]:
    """Return local relative-parameter sensitivities around the reference M0 point.

    Columns are dy / d(log(theta)) approximated by centred finite differences.
    This is a practical/local diagnostic only; it does not establish structural
    identifiability.
    """
    params = params or ModelParams()
    names = tuple(parameter_names)
    base = asdict(params)
    matrix = np.empty((m0_observable_vector(params).size, len(names)), dtype=float)

    for j, name in enumerate(names):
        value = float(base[name])
        if value <= 0:
            raise ValueError(f"{name} must be positive for relative sensitivity")
        lo = value * (1.0 - relative_step)
        hi = value * (1.0 + relative_step)
        y_lo = m0_observable_vector(replace(params, **{name: lo}))
        y_hi = m0_observable_vector(replace(params, **{name: hi}))
        matrix[:, j] = (y_hi - y_lo) / (2.0 * relative_step)

    return matrix, names


def local_identifiability_report(params: ModelParams | None = None) -> dict:
    """Summarise sensitivity rank and parameter trade-offs at the M0 reference point."""
    matrix, names = local_sensitivity_matrix(params)
    norms = np.linalg.norm(matrix, axis=0)
    normalised = np.zeros_like(matrix)
    active = norms > 1e-12
    normalised[:, active] = matrix[:, active] / norms[active]
    singular_values = np.linalg.svd(normalised[:, active], compute_uv=False) if np.any(active) else np.array([])
    tol = (singular_values[0] * 1e-8) if singular_values.size else 0.0
    rank = int(np.sum(singular_values > tol))
    condition = (
        float(singular_values[0] / singular_values[-1])
        if singular_values.size and singular_values[-1] > 1e-12
        else None
    )
    correlation = normalised.T @ normalised

    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pairs.append(
                {
                    "parameters": [names[i], names[j]],
                    "absolute_cosine_similarity": float(abs(correlation[i, j])),
                }
            )
    pairs.sort(key=lambda x: x["absolute_cosine_similarity"], reverse=True)

    return {
        "scope": "LOCAL_PRACTICAL_IDENTIFIABILITY_DIAGNOSTIC",
        "model_specification": "M0",
        "parameter_names": list(names),
        "observable_count": int(matrix.shape[0]),
        "parameter_count": int(matrix.shape[1]),
        "active_parameter_count": int(np.sum(active)),
        "normalised_sensitivity_rank": rank,
        "condition_number": condition,
        "singular_values": [float(x) for x in singular_values],
        "column_norms": {name: float(norm) for name, norm in zip(names, norms)},
        "highest_tradeoff_pairs": pairs[:10],
        "interpretation_boundary": (
            "Local finite-difference sensitivity around the demonstrative M0 reference point. "
            "It is not structural-identifiability proof, empirical calibration, or parameter uncertainty."
        ),
    }


def prediction_robustness_report(
    params: ModelParams | None = None,
    relative_perturbation: float = 0.10,
) -> dict:
    """Keep output robustness conceptually separate from parameter identifiability."""
    params = params or ModelParams()
    base = m0_observable_vector(params)
    changes = []
    for name in PARAMETER_NAMES:
        value = float(getattr(params, name))
        for direction in (-1.0, 1.0):
            perturbed = replace(
                params,
                **{name: value * (1.0 + direction * relative_perturbation)},
            )
            y = m0_observable_vector(perturbed)
            changes.append(float(np.max(np.abs(y - base))))

    return {
        "scope": "LOCAL_PREDICTION_ROBUSTNESS",
        "model_specification": "M0",
        "relative_parameter_perturbation": relative_perturbation,
        "max_absolute_output_change": max(changes),
        "median_max_absolute_output_change": float(np.median(changes)),
        "interpretation_boundary": (
            "Deterministic local perturbation diagnostic. Small output change does not imply "
            "parameter identifiability; large change does not imply empirical validity."
        ),
    }
