from __future__ import annotations

from contextlib import contextmanager, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sys
from typing import Iterator

import numpy as np
import scipy
from scipy.special import expit

from . import f1b_hierarchical_recovery as hierarchical
from . import f1b_r2_restriction_recovery as restrictions
from .f1b_hierarchical_recovery import (
    R2HierarchicalFit,
    RandomEffectScales,
)
from .f1b_prehuman_recovery import R2Dataset, R2Family
from .f1b_r2_paired_bootstrap_characterization import dataset_fingerprint
from .f1b_r2_restriction_recovery import (
    R2Restriction,
    RestrictionPairFit,
)


MAX_RETAINED_DRAW_INDEX = 198
OBSERVED_STATISTIC_TOLERANCE = 1e-10


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _array_sha256(values: np.ndarray) -> str:
    array = np.asarray(values)
    header = json.dumps(
        {
            "dtype": array.dtype.str,
            "shape": list(array.shape),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _sha256_bytes(header + b"\0" + np.ascontiguousarray(array).tobytes())


def _fit_vector(fit: R2HierarchicalFit) -> np.ndarray:
    return np.concatenate(
        (
            np.asarray(fit.fixed_parameters, dtype=float),
            np.asarray(fit.participant_intercepts, dtype=float),
            np.asarray(fit.item_intercepts, dtype=float),
            np.asarray(fit.participant_reward_slopes, dtype=float),
            np.asarray(fit.item_reward_slopes, dtype=float),
        )
    )


def _fit_summary(fit: R2HierarchicalFit) -> dict:
    vector = _fit_vector(fit)
    fixed = np.asarray(fit.fixed_parameters, dtype=float)
    return {
        "family": fit.family.value,
        "fixed_parameters": [float(value) for value in fixed],
        "fixed_parameters_sha256": _array_sha256(fixed),
        "full_parameter_vector_sha256": _array_sha256(vector),
        "full_parameter_vector_size": int(vector.size),
        "penalized_objective": float(fit.penalized_objective),
        "log_likelihood": float(fit.log_likelihood),
        "parameter_count": int(fit.parameter_count),
        "converged": bool(fit.converged),
    }


def _fixed_parameter_count(family: R2Family) -> int:
    if family in (R2Family.AP_A, R2Family.AP_B):
        return 4
    if family is R2Family.AP_C:
        return 6
    raise ValueError(f"unsupported R2 family: {family}")


@contextmanager
def _optimizer_trace() -> Iterator[dict]:
    """Intercept optimizer metadata without changing the scientific fitter.

    This diagnostic helper is intentionally process-local and single-threaded.
    It restores both patched module symbols even if fitting raises.
    """

    original_fit = restrictions.fit_r2_hierarchical_candidate
    original_minimize = hierarchical.minimize
    state: dict = {
        "current_family": None,
        "current_fit_serial": None,
        "optimizer_calls": [],
        "fit_calls": [],
    }

    def traced_minimize(fun, x0, *args, **kwargs):
        family = state["current_family"]
        fit_serial = state["current_fit_serial"]
        if family is None or fit_serial is None:
            raise RuntimeError(
                "diagnostic optimizer interception escaped an R2 fit context"
            )

        x0_array = np.asarray(x0, dtype=float)
        fixed_count = _fixed_parameter_count(family)
        call_index = sum(
            int(row["fit_serial"]) == int(fit_serial)
            for row in state["optimizer_calls"]
        )

        result = original_minimize(fun, x0, *args, **kwargs)
        result_x = np.asarray(result.x, dtype=float)
        jac = getattr(result, "jac", None)
        jac_array = (
            np.asarray(jac, dtype=float).reshape(-1)
            if jac is not None
            else np.asarray([], dtype=float)
        )
        options = dict(kwargs.get("options") or {})
        state["optimizer_calls"].append(
            {
                "fit_serial": int(fit_serial),
                "family": family.value,
                "optimizer_call_index": int(call_index),
                "retry_call": bool(call_index > 0),
                "method": str(kwargs.get("method")),
                "options": {
                    str(key): options[key]
                    for key in sorted(options)
                },
                "x0_sha256": _array_sha256(x0_array),
                "x0_size": int(x0_array.size),
                "population_fixed_parameters": [
                    float(value)
                    for value in x0_array[:fixed_count]
                ],
                "population_fixed_parameters_sha256": _array_sha256(
                    x0_array[:fixed_count]
                ),
                "success": bool(result.success),
                "status": (
                    int(result.status)
                    if getattr(result, "status", None) is not None
                    else None
                ),
                "message": str(getattr(result, "message", "")),
                "nit": (
                    int(result.nit)
                    if getattr(result, "nit", None) is not None
                    else None
                ),
                "nfev": (
                    int(result.nfev)
                    if getattr(result, "nfev", None) is not None
                    else None
                ),
                "njev": (
                    int(result.njev)
                    if getattr(result, "njev", None) is not None
                    else None
                ),
                "objective": float(result.fun),
                "jacobian_infinity_norm": (
                    float(np.max(np.abs(jac_array)))
                    if jac_array.size
                    else None
                ),
                "result_vector_sha256": _array_sha256(result_x),
                "result_fixed_parameters": [
                    float(value)
                    for value in result_x[:fixed_count]
                ],
                "result_fixed_parameters_sha256": _array_sha256(
                    result_x[:fixed_count]
                ),
            }
        )
        return result

    def traced_fit(family, *args, **kwargs):
        fit_serial = len(state["fit_calls"])
        previous_family = state["current_family"]
        previous_serial = state["current_fit_serial"]
        state["current_family"] = family
        state["current_fit_serial"] = fit_serial
        try:
            fit = original_fit(family, *args, **kwargs)
        except Exception as exc:
            state["fit_calls"].append(
                {
                    "fit_serial": int(fit_serial),
                    "family": family.value,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "fit": None,
                }
            )
            raise
        else:
            state["fit_calls"].append(
                {
                    "fit_serial": int(fit_serial),
                    "family": family.value,
                    "error_type": None,
                    "error_message": None,
                    "fit": _fit_summary(fit),
                }
            )
            return fit
        finally:
            state["current_family"] = previous_family
            state["current_fit_serial"] = previous_serial

    restrictions.fit_r2_hierarchical_candidate = traced_fit
    hierarchical.minimize = traced_minimize
    try:
        yield state
    finally:
        restrictions.fit_r2_hierarchical_candidate = original_fit
        hierarchical.minimize = original_minimize


def trace_restriction_pair(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    scales: RandomEffectScales,
) -> tuple[RestrictionPairFit, dict]:
    with _optimizer_trace() as trace:
        pair = restrictions.fit_restriction_pair(
            dataset,
            restriction,
            scales=scales,
        )
    return pair, {
        "restriction": restriction.value,
        "statistic": float(pair.statistic),
        "restricted_fit": _fit_summary(pair.restricted),
        "general_fit": _fit_summary(pair.general),
        "fit_calls": trace["fit_calls"],
        "optimizer_calls": trace["optimizer_calls"],
    }


def _datasets_exactly_equal(left: R2Dataset, right: R2Dataset) -> bool:
    return all(
        np.array_equal(getattr(left, field), getattr(right, field))
        for field in (
            "share",
            "belief",
            "accuracy_cue",
            "reward_context",
            "participant",
            "item",
        )
    )


def diagnostic_bootstrap_simulation(
    template: R2Dataset,
    fit: R2HierarchicalFit,
    *,
    scales: RandomEffectScales,
    bootstrap_stream_seed: int,
    restriction_index: int,
    draw_index: int,
) -> tuple[R2Dataset, dict]:
    if not 0 <= int(draw_index) <= MAX_RETAINED_DRAW_INDEX:
        raise ValueError(
            "diagnostic draw index must remain inside retained 0..198"
        )

    seed_words = (
        int(bootstrap_stream_seed),
        int(restriction_index),
        int(draw_index),
    )
    scientific_rng = np.random.default_rng(np.random.SeedSequence(seed_words))
    scientific_dataset = restrictions.simulate_exact_design_under_restriction(
        template,
        fit,
        scales=scales,
        rng=scientific_rng,
    )

    diagnostic_rng = np.random.default_rng(np.random.SeedSequence(seed_words))
    participant_count = int(np.max(template.participant)) + 1
    item_count = int(np.max(template.item)) + 1
    eta = restrictions._fixed_eta(
        fit.family,
        fit.fixed_parameters,
        template.belief,
        template.accuracy_cue,
        template.reward_context,
    )
    participant_intercept = diagnostic_rng.normal(
        0.0,
        scales.participant_intercept_sd,
        participant_count,
    )
    item_intercept = diagnostic_rng.normal(
        0.0,
        scales.item_intercept_sd,
        item_count,
    )
    participant_slope = diagnostic_rng.normal(
        0.0,
        scales.participant_slope_sd,
        participant_count,
    )
    item_slope = diagnostic_rng.normal(
        0.0,
        scales.item_slope_sd,
        item_count,
    )
    eta = (
        eta
        + participant_intercept[template.participant]
        + item_intercept[template.item]
        + participant_slope[template.participant] * template.reward_context
        + item_slope[template.item] * template.reward_context
    )
    probability = expit(eta)
    share = diagnostic_rng.binomial(1, probability).astype(int)
    diagnostic_dataset = R2Dataset(
        share=share,
        belief=template.belief.copy(),
        accuracy_cue=template.accuracy_cue.copy(),
        reward_context=template.reward_context.copy(),
        participant=template.participant.copy(),
        item=template.item.copy(),
    )

    if not _datasets_exactly_equal(scientific_dataset, diagnostic_dataset):
        raise RuntimeError(
            "diagnostic bootstrap simulation diverged from scientific simulator"
        )
    scientific_sha = dataset_fingerprint(scientific_dataset)
    diagnostic_sha = dataset_fingerprint(diagnostic_dataset)
    if scientific_sha != diagnostic_sha:
        raise RuntimeError(
            "diagnostic bootstrap dataset fingerprint mismatch"
        )

    random_effect_hashes = {
        "participant_intercept_sha256": _array_sha256(
            participant_intercept
        ),
        "item_intercept_sha256": _array_sha256(item_intercept),
        "participant_reward_slope_sha256": _array_sha256(
            participant_slope
        ),
        "item_reward_slope_sha256": _array_sha256(item_slope),
    }
    return scientific_dataset, {
        "seed_words": list(seed_words),
        "probability_sha256": _array_sha256(probability),
        "share_sha256": _array_sha256(share),
        "dataset_sha256": scientific_sha,
        "random_effect_hashes": random_effect_hashes,
        "scientific_simulator_exact_match": True,
    }


def _attempts_exactly_equal(
    retained: float | None,
    regenerated: float | None,
) -> bool:
    if retained is None or regenerated is None:
        return retained is None and regenerated is None
    return float(retained) == float(regenerated)


def _validated_draw_indices(draw_indices) -> tuple[int, ...]:
    values = tuple(int(value) for value in draw_indices)
    if not values:
        raise ValueError("diagnostic draw index sequence must not be empty")
    if len(values) != len(set(values)):
        raise ValueError("diagnostic draw indices must be unique")
    if tuple(sorted(values)) != values:
        raise ValueError("diagnostic draw indices must be increasing")
    if values[0] < 0 or values[-1] > MAX_RETAINED_DRAW_INDEX:
        raise ValueError(
            "diagnostic draws are restricted to retained indices 0..198"
        )
    return values


def diagnose_run_prefix(
    run: dict,
    dataset: R2Dataset,
    *,
    scales: RandomEffectScales,
    draw_indices=range(199),
    stop_after_first_divergence: bool = True,
) -> dict:
    indices = _validated_draw_indices(draw_indices)
    retained_attempts = tuple(run["bootstrap_attempt_statistics"])
    if len(retained_attempts) != 199:
        raise ValueError("diagnostic source run must retain exactly 199 attempts")

    restriction = R2Restriction(str(run["restriction"]))
    restriction_index = (
        1 if restriction is R2Restriction.ADD else 2
    )
    observed_pair, observed_trace = trace_restriction_pair(
        dataset,
        restriction,
        scales=scales,
    )
    retained_observed = float(run["observed_statistic"])
    observed_delta = abs(
        float(observed_pair.statistic) - retained_observed
    )

    draw_rows: list[dict] = []
    first_divergent_draw = None
    for draw_index in indices:
        bootstrap_dataset, simulation_trace = diagnostic_bootstrap_simulation(
            dataset,
            observed_pair.restricted,
            scales=scales,
            bootstrap_stream_seed=int(run["bootstrap_stream_seed"]),
            restriction_index=restriction_index,
            draw_index=draw_index,
        )
        error_type = None
        error_message = None
        pair_trace = None
        regenerated_statistic: float | None
        try:
            bootstrap_pair, pair_trace = trace_restriction_pair(
                bootstrap_dataset,
                restriction,
                scales=scales,
            )
            regenerated_statistic = float(bootstrap_pair.statistic)
        except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
            regenerated_statistic = None
            error_type = type(exc).__name__
            error_message = str(exc)

        retained_statistic = retained_attempts[draw_index]
        exact_equal = _attempts_exactly_equal(
            retained_statistic,
            regenerated_statistic,
        )
        if not exact_equal and first_divergent_draw is None:
            first_divergent_draw = int(draw_index)

        retained_numeric = (
            float(retained_statistic)
            if retained_statistic is not None
            else None
        )
        absolute_delta = (
            abs(regenerated_statistic - retained_numeric)
            if regenerated_statistic is not None
            and retained_numeric is not None
            else None
        )
        retained_exceedance = (
            bool(retained_numeric >= retained_observed)
            if retained_numeric is not None
            else None
        )
        regenerated_exceedance = (
            bool(regenerated_statistic >= observed_pair.statistic)
            if regenerated_statistic is not None
            else None
        )
        draw_rows.append(
            {
                "draw_index": int(draw_index),
                "simulation": simulation_trace,
                "retained_statistic": retained_numeric,
                "regenerated_statistic": regenerated_statistic,
                "exact_statistic_match": bool(exact_equal),
                "absolute_statistic_delta": absolute_delta,
                "retained_exceedance": retained_exceedance,
                "regenerated_exceedance": regenerated_exceedance,
                "exceedance_match": (
                    retained_exceedance == regenerated_exceedance
                ),
                "bootstrap_fit_error_type": error_type,
                "bootstrap_fit_error_message": error_message,
                "bootstrap_pair_trace": pair_trace,
            }
        )
        if (
            stop_after_first_divergence
            and first_divergent_draw is not None
        ):
            break

    return {
        "run_id": str(run["run_id"]),
        "restriction": restriction.value,
        "dataset_sha256": dataset_fingerprint(dataset),
        "retained_dataset_sha256": str(run["dataset_sha256"]),
        "dataset_fingerprint_match": (
            dataset_fingerprint(dataset) == str(run["dataset_sha256"])
        ),
        "retained_observed_statistic": retained_observed,
        "regenerated_observed_statistic": float(observed_pair.statistic),
        "observed_statistic_absolute_delta": float(observed_delta),
        "observed_statistic_match_1e_10": bool(
            observed_delta <= OBSERVED_STATISTIC_TOLERANCE
        ),
        "observed_pair_trace": observed_trace,
        "draws_executed": int(len(draw_rows)),
        "first_divergent_draw_index": first_divergent_draw,
        "full_requested_prefix_exact": (
            first_divergent_draw is None
            and len(draw_rows) == len(indices)
        ),
        "draws": draw_rows,
        "interpretation_boundary": (
            "Diagnostic replay of retained draw indices only. No bootstrap "
            "draw index >=199 is generated and this result cannot authorize "
            "Stage C2 or change the frozen Stage-C1 gate."
        ),
    }


def select_diagnostic_sentinels(
    c1_result: dict,
    *,
    tolerance: float = OBSERVED_STATISTIC_TOLERANCE,
) -> dict[str, str]:
    rows = list(c1_result["rows"])
    if len(rows) != 224:
        raise ValueError("retained C1 result must contain exactly 224 rows")

    def ordered(predicate) -> list[dict]:
        return sorted(
            (row for row in rows if predicate(row)),
            key=lambda row: str(row["run_id"]),
        )

    pass_control = ordered(
        lambda row: bool(row["qualification_pass"])
    )
    exact_hash_failure = ordered(
        lambda row: (
            not bool(row["attempt_sequence_sha256_match"])
            and float(row["observed_statistic_absolute_delta"]) == 0.0
        )
    )
    within_tolerance_failure = ordered(
        lambda row: (
            not bool(row["attempt_sequence_sha256_match"])
            and 0.0
            < float(row["observed_statistic_absolute_delta"])
            <= float(tolerance)
        )
    )
    outside_tolerance_failure = ordered(
        lambda row: (
            not bool(row["attempt_sequence_sha256_match"])
            and float(row["observed_statistic_absolute_delta"])
            > float(tolerance)
        )
    )

    if not pass_control:
        raise ValueError("retained C1 result has no exact-pass control")
    if len(exact_hash_failure) != 1:
        raise ValueError(
            "retained C1 result must contain exactly one exact-stat/hash failure"
        )
    if not within_tolerance_failure:
        raise ValueError(
            "retained C1 result has no nonzero within-tolerance hash failure"
        )
    if not outside_tolerance_failure:
        raise ValueError(
            "retained C1 result has no outside-tolerance hash failure"
        )

    return {
        "EXACT_PASS_CONTROL": str(pass_control[0]["run_id"]),
        "EXACT_OBSERVED_HASH_FAILURE": str(
            exact_hash_failure[0]["run_id"]
        ),
        "WITHIN_TOLERANCE_HASH_FAILURE": str(
            within_tolerance_failure[0]["run_id"]
        ),
        "OUTSIDE_TOLERANCE_HASH_FAILURE": str(
            outside_tolerance_failure[0]["run_id"]
        ),
    }


def environment_identity() -> dict:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        np.show_config()

    threadpool_info = None
    threadpool_error = None
    try:
        from threadpoolctl import threadpool_info as get_threadpool_info

        threadpool_info = get_threadpool_info()
    except Exception as exc:  # pragma: no cover - environment dependent
        threadpool_error = f"{type(exc).__name__}: {exc}"

    cpu_model = None
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines():
            if line.lower().startswith("model name"):
                _, _, value = line.partition(":")
                cpu_model = value.strip()
                break

    thread_environment = {
        key: os.environ.get(key)
        for key in (
            "OMP_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "MKL_NUM_THREADS",
            "BLIS_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
            "NUMEXPR_NUM_THREADS",
        )
    }
    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_model": cpu_model,
        "numpy_show_config": buffer.getvalue(),
        "thread_environment": thread_environment,
        "threadpoolctl": threadpool_info,
        "threadpoolctl_error": threadpool_error,
    }
