from __future__ import annotations

import json
from math import isclose
from pathlib import Path
from statistics import NormalDist

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "model/contracts/m1_e4_generative_candidate_contract.json"
SCHEMA_PATH = ROOT / "schemas/m1_e4_generative_candidate_contract.schema.json"
NORM = NormalDist()


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def evsd_inverse(hit_rate: float, false_alarm_rate: float) -> tuple[float, float]:
    z_hit = NORM.inv_cdf(hit_rate)
    z_fa = NORM.inv_cdf(false_alarm_rate)
    d = z_hit - z_fa
    c = -0.5 * (z_hit + z_fa)
    return d, c


def evsd_forward(d: float, c: float) -> tuple[float, float]:
    hit_rate = NORM.cdf(d / 2 - c)
    false_alarm_rate = NORM.cdf(-d / 2 - c)
    return hit_rate, false_alarm_rate


def two_ht_inverse(hit_rate: float, false_alarm_rate: float) -> tuple[float, float | None]:
    ddet = hit_rate - false_alarm_rate
    if isclose(ddet, 1.0):
        return ddet, None
    g = false_alarm_rate / (1 - ddet)
    return ddet, g


def two_ht_forward(ddet: float, g: float) -> tuple[float, float]:
    hit_rate = ddet + (1 - ddet) * g
    false_alarm_rate = (1 - ddet) * g
    return hit_rate, false_alarm_rate


def test_m1_e4_generative_contract_validates_against_schema():
    contract = load_contract()
    schema = json.loads(SCHEMA_PATH.read_text())
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_m1_e4_has_exactly_two_primary_candidate_families():
    candidates = load_contract()["primary_candidates"]
    assert len(candidates) == 2
    assert {candidate["id"] for candidate in candidates} == {
        "CANDIDATE.M1.E4.C1.EVSD",
        "CANDIDATE.M1.E4.C2.2HT",
    }
    assert {candidate["family"] for candidate in candidates} == {
        "CONTINUOUS_EVIDENCE_STRENGTH",
        "DISCRETE_DETECTION_PLUS_GUESSING",
    }


def test_m1_e4_evsd_inverse_forward_consistency():
    hit_rate, false_alarm_rate = 0.72, 0.21
    d, c = evsd_inverse(hit_rate, false_alarm_rate)
    reconstructed_h, reconstructed_f = evsd_forward(d, c)
    assert isclose(reconstructed_h, hit_rate, abs_tol=1e-12)
    assert isclose(reconstructed_f, false_alarm_rate, abs_tol=1e-12)


def test_m1_e4_symmetric_2ht_inverse_forward_consistency():
    hit_rate, false_alarm_rate = 0.72, 0.21
    ddet, g = two_ht_inverse(hit_rate, false_alarm_rate)
    assert g is not None
    reconstructed_h, reconstructed_f = two_ht_forward(ddet, g)
    assert isclose(reconstructed_h, hit_rate, abs_tol=1e-12)
    assert isclose(reconstructed_f, false_alarm_rate, abs_tol=1e-12)


def test_m1_e4_one_point_equifinality_is_demonstrated():
    hit_rate, false_alarm_rate = 0.72, 0.21

    d, c = evsd_inverse(hit_rate, false_alarm_rate)
    evsd_h, evsd_f = evsd_forward(d, c)

    ddet, g = two_ht_inverse(hit_rate, false_alarm_rate)
    assert g is not None
    threshold_h, threshold_f = two_ht_forward(ddet, g)

    assert isclose(evsd_h, threshold_h, abs_tol=1e-12)
    assert isclose(evsd_f, threshold_f, abs_tol=1e-12)

    ident = load_contract()["one_point_identifiability"]
    assert ident["single_operating_point_selects_candidate_family"] is False
    assert ident["published_mean_dprime_selects_candidate_family"] is False


def test_m1_e4_pure_bias_manipulation_preserves_evsd_memory_parameter():
    fixed_d = 1.1
    criteria = [-0.7, 0.0, 0.8]
    recovered_d = []
    points = []
    for criterion in criteria:
        hit_rate, false_alarm_rate = evsd_forward(fixed_d, criterion)
        d, _ = evsd_inverse(hit_rate, false_alarm_rate)
        recovered_d.append(d)
        points.append((hit_rate, false_alarm_rate))

    assert all(isclose(value, fixed_d, abs_tol=1e-12) for value in recovered_d)
    probability_differences = [h - f for h, f in points]
    assert max(probability_differences) - min(probability_differences) > 1e-3


def test_m1_e4_pure_bias_manipulation_preserves_2ht_detection_parameter():
    fixed_ddet = 0.42
    guesses = [0.15, 0.45, 0.8]
    recovered_ddet = []
    points = []
    for guess in guesses:
        hit_rate, false_alarm_rate = two_ht_forward(fixed_ddet, guess)
        ddet, recovered_g = two_ht_inverse(hit_rate, false_alarm_rate)
        assert recovered_g is not None
        assert isclose(recovered_g, guess, abs_tol=1e-12)
        recovered_ddet.append(ddet)
        points.append((hit_rate, false_alarm_rate))

    assert all(isclose(value, fixed_ddet, abs_tol=1e-12) for value in recovered_ddet)
    assert all(isclose(h - f, fixed_ddet, abs_tol=1e-12) for h, f in points)


def test_m1_e4_asymmetric_2ht_is_explicitly_underidentified():
    boundary = load_contract()["asymmetric_2ht_boundary"]
    assert boundary["status"] == "DEFERRED_UNDERIDENTIFIED"
    assert boundary["underidentified"] is True
    assert set(boundary["parameters"]) == {"Do", "Dn", "g"}
    assert set(boundary["observed_probabilities_from_one_operating_point"]) == {"H", "F"}


def test_m1_e4_future_fit_is_raw_response_and_parameter_count_aware():
    contract = load_contract()
    surface = contract["future_fitting_surface"]
    fairness = contract["comparison_fairness"]

    assert surface["primary_level"] == "RAW_BINOMIAL_RESPONSES"
    assert surface["summary_only_fit_allowed"] is False
    assert {"Nhit", "Nmiss", "Nfa", "Ncr"}.issubset(surface["required_retained_quantities"])
    assert fairness["parameter_count_aware"] is True
    assert "AIC" in fairness["required_diagnostics"]
    assert fairness["aic_is_causal_proof"] is False


def test_m1_e4_pencode_is_not_equated_with_candidate_memory_parameters():
    contract = load_contract()
    forbidden = set(contract["pencode_boundary"]["forbidden_equivalences"])
    assert contract["pencode_boundary"]["status"] == "NOT_IDENTIFIED_AND_NOT_ACTIVE"
    assert "Pencode = d" in forbidden
    assert "Pencode = Ddet" in forbidden

    candidates = {candidate["id"]: candidate for candidate in contract["primary_candidates"]}
    assert "not Pencode" in candidates["CANDIDATE.M1.E4.C1.EVSD"]["what_memory_parameter_is_not"]
    assert "not automatically an item-level Pencode" in candidates["CANDIDATE.M1.E4.C2.2HT"]["what_memory_parameter_is_not"]


def test_m1_e4_generative_validation_patterns_are_not_active():
    contract = load_contract()
    active = json.loads((ROOT / "model/validation_tests.json").read_text())
    active_ids = {item["id"] for item in active}
    planned_ids = {
        item["id"]
        for item in contract["validation_contract"]["planned_patterns"]
    }
    assert planned_ids.isdisjoint(active_ids)


def test_m1_e4_phase_c_forbids_runtime_ui_registry_and_release_changes():
    contract = load_contract()
    gate = contract["promotion_gate"]

    assert gate["active_registry_mutation_allowed"] is False
    assert gate["runtime_model_selection_allowed"] is False
    assert gate["executable_cognitive_equation_allowed"] is False
    assert gate["ui_allowed"] is False

    assert not (ROOT / "src/cognitive_epistemic_model/recognition.py").exists()
    assert not (ROOT / "src/cognitive_epistemic_model/encoding.py").exists()
    assert not (ROOT / "web/src/recognition-stage.ts").exists()

    active_variables = json.loads((ROOT / "model/variables.json").read_text())
    active_names = {item["short_name"] for item in active_variables}
    assert "Pencode" not in active_names
    assert "Ddet" not in active_names

    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    assert snapshot["id"] == "EVIDENCE.M1.2026-09-16.r1"
