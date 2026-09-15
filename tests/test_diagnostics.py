import math

from cognitive_epistemic_model.calibration.diagnostics import (
    PARAMETER_NAMES,
    local_identifiability_report,
    local_sensitivity_matrix,
    m0_observable_vector,
    prediction_robustness_report,
)
from cognitive_epistemic_model.state import ModelParams


def test_m0_diagnostic_vector_is_finite_and_nontrivial():
    values = m0_observable_vector(ModelParams())
    assert len(values) > len(PARAMETER_NAMES)
    assert all(math.isfinite(float(x)) for x in values)


def test_local_sensitivity_report_separates_rank_from_prediction_robustness():
    matrix, names = local_sensitivity_matrix(ModelParams())
    assert matrix.shape[1] == len(PARAMETER_NAMES)
    assert tuple(names) == PARAMETER_NAMES

    ident = local_identifiability_report(ModelParams())
    robust = prediction_robustness_report(ModelParams())

    assert ident["scope"] == "LOCAL_PRACTICAL_IDENTIFIABILITY_DIAGNOSTIC"
    assert ident["parameter_count"] == len(PARAMETER_NAMES)
    assert 0 <= ident["normalised_sensitivity_rank"] <= len(PARAMETER_NAMES)
    assert len(ident["highest_tradeoff_pairs"]) > 0
    assert robust["scope"] == "LOCAL_PREDICTION_ROBUSTNESS"
    assert robust["relative_parameter_perturbation"] == 0.10
    assert robust["max_absolute_output_change"] >= 0.0
