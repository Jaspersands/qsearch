from fractions import Fraction as F
import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.linalg import eigh

import filtered_kms as k


@pytest.mark.parametrize("d", [2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("beta", [0.0, 0.37])
def test_physical_matrices_check_both_metrics_and_both_filters(d, beta):
    row = k.dense_control(d, beta, s=0.29)
    assert max(row["identity_errors"].values()) < 2e-8
    assert len(row["filter_controls"]) == 2
    assert not row["parent_gap_disproved"]


@pytest.mark.parametrize("s", [-3.0, -0.25, 0.0, 0.25, 3.0])
def test_filter_phase_is_retained(s):
    row = k.dense_control(5, 0.6, s)
    assert row["log_same_KMS_filter_commutator_ratio_lower"] is not None
    for control in row["filter_controls"]:
        assert control["measured_same_KMS_commutator_ratio"]+1e-9 >= math.exp(
            row["log_same_KMS_filter_commutator_ratio_lower"])


def test_thermal_derivative_metric_is_not_the_physical_commutator_metric():
    row = k.dense_control(5, 0.6)
    assert not math.isclose(row["same_KMS_gradient"], row["raw_physical_form"], rel_tol=1e-3)
    assert row["identity_errors"]["tagged_metric_equals_physical_form"] < 1e-12


def test_exact_certificate_in_degree_regime_keeps_opposite_controls():
    row = k.rational_certificate(2**20, F(1, 8200))
    assert row["inside_beta_squared_d_plus_one_le_one_over_64"]
    assert row["same_KMS_filter_commutator_ratio_exceeds_99_over_100"]
    assert row["filtered_to_raw_physical_form_ratio_below_1_over_100"]
    assert F(row["same_KMS_filter_commutator_ratio_lower"]) > F(99, 100)
    assert F(row["filtered_to_raw_physical_form_ratio_upper"]) < F(1, 10**15)
    assert row["filtered_parent_gap_lower_from_existing_mass_lemma"] == "25/36"
    assert row["classical_envelope_ratio_upper_from_existing_moment_bound"] == "128/127"
    assert not row["large_matrices_built"] and not row["parent_gap_disproved"]


def test_inconclusive_small_certificate_does_not_manufacture_a_failure():
    row = k.rational_certificate(16, F(1, 40))
    assert not row["same_KMS_filter_commutator_ratio_exceeds_99_over_100"]
    assert not row["filtered_to_raw_physical_form_ratio_below_1_over_100"]
    assert row["same_KMS_filter_commutator_ratio_lower"] == "0"


def test_exact_certificates_tighten_monotonically_and_bound_floating_values():
    d, beta = 2**20, F(1, 8200)
    formula = k.star_formula(d, float(beta))
    previous_lower, previous_upper = F(0), None
    for terms in (0, 4, 8, 12, 24):
        row = k.rational_certificate(d, beta, terms)
        lower = F(row["same_KMS_filter_commutator_ratio_lower"])
        upper = F(row["filtered_to_raw_physical_form_ratio_upper"])
        assert lower >= previous_lower
        assert previous_upper is None or upper <= previous_upper
        assert math.log(float(lower)) <= formula["log_same_KMS_filter_commutator_ratio_lower"]+1e-12
        assert math.log(float(upper)) >= formula["log_filtered_to_raw_physical_form_ratio"]-1e-12
        previous_lower, previous_upper = lower, upper


def test_large_formula_retains_rare_transition_and_stays_finite():
    for d in (2**16, 2**20, 2**24, 2**32, 2**40):
        row = k.star_formula(d, 1/(8*math.sqrt(d+1)))
        assert row["one_minus_sector_axis_overlap"] > 0
        assert math.isfinite(row["log_raw_physical_form_over_sector_weight"])
        assert math.isfinite(row["log_filtered_to_raw_physical_form_ratio"])
        assert row["log_filtered_physical_form_over_sector_weight"] <= row["log_filtered_witness_Rayleigh_upper"]
        assert row["filtered_witness_Rayleigh_lower"] >= 0.8
    assert row["log_filtered_to_raw_physical_form_ratio"] < -100000
    assert abs(row["log_same_KMS_filter_commutator_ratio_lower"]) < 1e-6


def test_beta_zero_is_trace_limit_not_an_obstruction():
    for d in (2, 7, 2**20):
        row = k.star_formula(d, 0)
        expected = d/2+d*d/(d*d+1)
        for name in ("log_same_KMS_gradient_over_sector_weight", "log_raw_physical_form_over_sector_weight",
                     "log_filtered_physical_form_over_sector_weight", "log_integrated_physical_form_over_sector_weight"):
            assert math.isclose(math.exp(row[name]), expected)
        assert row["log_same_KMS_filter_commutator_ratio_lower"] is None
        assert row["log_filtered_to_raw_physical_form_ratio"] == 0


def test_integrated_form_against_independent_physical_quadrature():
    d, beta = 3, 0.61
    model, _, W, S = k.physical_reference(d, beta)
    values, vectors = eigh(model.h)
    omega = beta*(values[:, None]-values[None, :])
    spectral_z = [vectors.T@z@vectors for z in model.z]

    def integrand(s):
        energy = 0.0
        for z in spectral_z:
            B = vectors@(z*np.exp(-omega**2/8+1j*s*omega))@vectors.T
            energy += k.kms_squared(B@W-W@B, S)/4
        return 2/math.cosh(2*math.pi*s)*energy

    actual, error = quad(integrand, -8, 8, epsabs=1e-11, epsrel=1e-11)
    expected = 2.0**(-(d-1))*math.exp(k.star_formula(d, beta)["log_integrated_physical_form_over_sector_weight"])
    assert error < 1e-10
    assert abs(actual-expected) < 1e-10


@pytest.mark.parametrize("d,beta,s", [(1, .1, 0), (True, .1, 0), (4, -1, 0),
                                     (4, math.nan, 0), (4, True, 0), (4, .1, math.inf), (4, .1, True)])
def test_invalid_inputs_rejected(d, beta, s):
    with pytest.raises(ValueError):
        k.star_formula(d, beta, s)


def test_no_silent_dense_large_execution_or_inexact_certificates():
    with pytest.raises(ValueError):
        k.dense_control(8, .1)
    with pytest.raises(ValueError):
        k.dense_control(3, 1.1)
    with pytest.raises(ValueError):
        k.rational_certificate(2**20, 1/8200)
    with pytest.raises(ValueError):
        k.rational_certificate(2**20, F(1, 8200), 129)
