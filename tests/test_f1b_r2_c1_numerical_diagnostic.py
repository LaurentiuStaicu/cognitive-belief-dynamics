from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest

import cognitive_epistemic_model.calibration.f1b_hierarchical_recovery as hierarchical
import cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery as restrictions
from cognitive_epistemic_model.calibration.f1b_hierarchical_recovery import (
    R2HierarchicalFit,
    RandomEffectScales,
)
from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R2Dataset,
    R2Family,
)
from cognitive_epistemic_model.calibration.f1b_r2_c1_numerical_diagnostic import (
    _optimizer_trace,
    _validated_draw_indices,
    diagnostic_bootstrap_simulation,
    select_diagnostic_sentinels,
)


def _dataset() -> R2Dataset:
    return R2Dataset(
        share=np.asarray([0, 1, 1, 0], dtype=int),
        belief=np.asarray([0.2, 0.4, 0.6, 0.8], dtype=float),
        accuracy_cue=np.asarray([0.0, 1.0, 0.0, 1.0], dtype=float),
        reward_context=np.asarray([-1.0, -1.0, 1.0, 1.0], dtype=float),
        participant=np.asarray([0, 1, 0, 1], dtype=int),
        item=np.asarray([0, 0, 1, 1], dtype=int),
    )


def _scales() -> RandomEffectScales:
    return RandomEffectScales(
        participant_intercept_sd=0.2,
        item_intercept_sd=0.3,
        participant_slope_sd=0.15,
        item_slope_sd=0.1,
    )


def _fit(family: R2Family = R2Family.AP_B) -> R2HierarchicalFit:
    return R2HierarchicalFit(
        family=family,
        fixed_parameters=(0.1, 0.2, -0.3, 0.4),
        participant_intercepts=np.zeros(2),
        item_intercepts=np.zeros(2),
        participant_reward_slopes=np.zeros(2),
        item_reward_slopes=np.zeros(2),
        log_likelihood=-2.0,
        parameter_count=12,
        penalized_objective=3.0,
        converged=True,
    )


def test_diagnostic_bootstrap_matches_scientific_simulator_exactly() -> None:
    dataset, trace = diagnostic_bootstrap_simulation(
        _dataset(),
        _fit(),
        scales=_scales(),
        bootstrap_stream_seed=123456,
        restriction_index=1,
        draw_index=17,
    )
    assert dataset.share.shape == (4,)
    assert trace["scientific_simulator_exact_match"] is True
    assert len(trace["dataset_sha256"]) == 64
    assert len(trace["probability_sha256"]) == 64
    assert trace["seed_words"] == [123456, 1, 17]


def test_diagnostic_draw_indices_fail_closed_outside_retained_prefix() -> None:
    assert _validated_draw_indices((0, 17, 198)) == (0, 17, 198)
    with pytest.raises(ValueError, match="0..198"):
        _validated_draw_indices((0, 199))
    with pytest.raises(ValueError, match="0..198"):
        _validated_draw_indices((-1, 0))
    with pytest.raises(ValueError, match="unique"):
        _validated_draw_indices((0, 0))
    with pytest.raises(ValueError, match="increasing"):
        _validated_draw_indices((1, 0))


def test_sentinel_selection_is_deterministic_and_stratified() -> None:
    rows = []
    for index in range(224):
        rows.append(
            {
                "run_id": f"RUN_{index:03d}",
                "qualification_pass": True,
                "attempt_sequence_sha256_match": True,
                "observed_statistic_absolute_delta": 0.0,
            }
        )

    rows[5].update(
        {
            "qualification_pass": False,
            "attempt_sequence_sha256_match": False,
            "observed_statistic_absolute_delta": 0.0,
        }
    )
    rows[6].update(
        {
            "qualification_pass": False,
            "attempt_sequence_sha256_match": False,
            "observed_statistic_absolute_delta": 1e-12,
        }
    )
    rows[7].update(
        {
            "qualification_pass": False,
            "attempt_sequence_sha256_match": False,
            "observed_statistic_absolute_delta": 1e-6,
        }
    )

    result = select_diagnostic_sentinels({"rows": rows})
    assert result == {
        "EXACT_PASS_CONTROL": "RUN_000",
        "EXACT_OBSERVED_HASH_FAILURE": "RUN_005",
        "WITHIN_TOLERANCE_HASH_FAILURE": "RUN_006",
        "OUTSIDE_TOLERANCE_HASH_FAILURE": "RUN_007",
    }


def test_optimizer_interception_restores_scientific_symbols(
    monkeypatch,
) -> None:
    original_minimize = hierarchical.minimize
    original_fit = restrictions.fit_r2_hierarchical_candidate

    def fake_minimize(fun, x0, *args, **kwargs):
        x = np.asarray(x0, dtype=float) + 0.25
        return SimpleNamespace(
            x=x,
            success=True,
            status=0,
            message="fake success",
            nit=3,
            nfev=5,
            njev=5,
            fun=1.5,
            jac=np.zeros_like(x),
        )

    def fake_fit(family, dataset, mask, *, scales):
        fixed_count = 4 if family is not R2Family.AP_C else 6
        x0 = np.zeros(fixed_count + 8, dtype=float)
        result = hierarchical.minimize(
            lambda vector: 0.0,
            x0,
            method="L-BFGS-B",
            jac=True,
            options={"maxiter": 400, "ftol": 1e-10, "maxls": 50},
        )
        fixed = tuple(float(value) for value in result.x[:fixed_count])
        return R2HierarchicalFit(
            family=family,
            fixed_parameters=fixed,
            participant_intercepts=np.zeros(2),
            item_intercepts=np.zeros(2),
            participant_reward_slopes=np.zeros(2),
            item_reward_slopes=np.zeros(2),
            log_likelihood=-1.0,
            parameter_count=fixed_count + 8,
            penalized_objective=float(result.fun),
            converged=True,
        )

    monkeypatch.setattr(hierarchical, "minimize", fake_minimize)
    monkeypatch.setattr(
        restrictions,
        "fit_r2_hierarchical_candidate",
        fake_fit,
    )
    patched_minimize = hierarchical.minimize
    patched_fit = restrictions.fit_r2_hierarchical_candidate

    with _optimizer_trace() as trace:
        fit = restrictions.fit_r2_hierarchical_candidate(
            R2Family.AP_B,
            _dataset(),
            np.ones(4, dtype=bool),
            scales=_scales(),
        )
        assert fit.family is R2Family.AP_B
        assert len(trace["optimizer_calls"]) == 1
        call = trace["optimizer_calls"][0]
        assert call["family"] == R2Family.AP_B.value
        assert call["retry_call"] is False
        assert call["message"] == "fake success"
        assert call["nit"] == 3
        assert call["jacobian_infinity_norm"] == 0.0

    assert hierarchical.minimize is patched_minimize
    assert restrictions.fit_r2_hierarchical_candidate is patched_fit
    assert hierarchical.minimize is not original_minimize
    assert restrictions.fit_r2_hierarchical_candidate is not original_fit
