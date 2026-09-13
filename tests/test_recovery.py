import math

from cognitive_epistemic_model.calibration.recovery import familiarity_trajectory, recover_alpha_f


def test_recovery_0_alpha_f():
    true = 0.37
    observed = familiarity_trajectory(true, exposures=8)
    estimated = recover_alpha_f(observed)
    assert math.isclose(estimated, true, rel_tol=1e-5, abs_tol=1e-5)
