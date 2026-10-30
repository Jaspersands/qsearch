from fractions import Fraction as F
import math

import numpy as np
import pytest
from scipy.linalg import eigh, expm

import thermal_flow as t


@pytest.mark.parametrize("d", [2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("beta", [0.0, 0.17])
def test_independent_physical_operators_match_sector_formulas(d, beta):
    result = t.dense_control(d, beta)
    assert max(result["identity_errors"].values()) < 1e-9
    assert not result["parent_gap_disproved"]


@pytest.mark.parametrize("s", [-3.0, -0.25, 0.0, 0.25, 3.0])
def test_actual_gaussian_filter_is_not_conflated_with_real_time_failure(s):
    result = t.dense_control(5, 0.6, s=s)
    assert result["filtered_image_gradient_squared_ratio"] <= math.exp(
        result["log_gaussian_image_gradient_squared_ratio_upper"])+1e-9


def test_rational_certificate_falsifies_both_shortcuts_inside_degree_regime():
    result = t.rational_countercertificate(65536, F(1, 2056))
    assert result["inside_beta_squared_d_plus_one_le_one_over_64"]
    assert result["flow_bound_strictly_falsified"]
    assert result["defect_bound_strictly_falsified"]
    assert F(result["flow_squared_ratio_lower"]) > F(result["incorrect_flow_squared_bound_upper"])
    assert F(result["defect_squared_ratio_lower"]) > result["incorrect_defect_squared_bound"]
    assert not result["large_matrices_built"] and not result["parent_gap_disproved"]
    assert result["filtered_parent_gap_lower_from_existing_mass_lemma"] == "25/36"
    assert result["classical_envelope_ratio_upper_from_existing_moment_bound"] == "128/127"


def test_rational_certificate_may_be_inconclusive_without_changing_claim():
    result = t.rational_countercertificate(16, F(1, 40))
    assert not result["flow_bound_strictly_falsified"]
    assert not result["defect_bound_strictly_falsified"]
    assert not result["parent_gap_disproved"]


def test_taylor_certificate_monotone_and_below_exact_floating_value():
    previous = F(0)
    row = t.star_formula(65536, 1/2056)
    for terms in (0, 4, 8, 12, 16, 24):
        cert = t.rational_countercertificate(65536, F(1, 2056), terms)
        lower = F(cert["flow_squared_ratio_lower"])
        assert lower >= previous
        assert math.log(float(lower)) <= row["log_flow_squared_amplification"]+1e-12
        previous = lower


def test_asymptotic_ledger_exhibits_growth_and_gaussian_suppression():
    rows = [t.star_formula(d, 1/(8*math.sqrt(d+1))) for d in (2**16, 2**20, 2**24)]
    assert all(row["log_flow_squared_amplification"] > row["log_incorrect_thermal_flow_squared_bound"]
               for row in rows)
    assert rows[-1]["log_flow_squared_amplification"] > 450
    assert rows[-1]["log_gaussian_image_gradient_squared_ratio_upper"] < -250000
    assert rows[-1]["log_phase_forgotten_Gaussian_gradient_squared_ratio_at_s_zero"] > 450
    assert all(not row["parent_gap_disproved"] for row in rows)


def test_zero_temperature_parameter_recovers_trace_control():
    for d in (2, 7, 128, 65536):
        row = t.star_formula(d, 0)
        assert math.isclose(math.exp(row["log_defect_squared_ratio"]), 8*(d+1)/(d+2))
        assert row["log_defect_squared_ratio"] <= row["log_trace_metric_defect_bound"]
        assert row["log_flow_squared_amplification"] <= 1e-14


@pytest.mark.parametrize("d,beta", [(1, 0.1), (True, 0.1), (4, -0.1), (4, math.nan), (4, True)])
def test_invalid_numeric_inputs_rejected(d, beta):
    with pytest.raises(ValueError):
        t.star_formula(d, beta)


def test_no_silent_exponential_execution_or_inexact_certificate():
    with pytest.raises(ValueError):
        t.dense_control(8, 0.1)
    with pytest.raises(ValueError):
        t.rational_countercertificate(65536, 1/2056)
    with pytest.raises(ValueError):
        t.rational_countercertificate(17, F(1, 40))
    with pytest.raises(ValueError):
        t.rational_countercertificate(16, F(1, 40), 129)


def test_phase_forgotten_gaussian_average_against_physical_evolution():
    d, beta = 3, 0.4
    model = t.build_model(d+1, [(0, j) for j in range(1, d+1)])
    dim = len(model.h)
    P = np.eye(dim)
    for j in range(2, d+1):
        P = P@(np.eye(dim)+model.operators[1]@model.operators[j])/2
    X = 1j*P@model.operators[0]@model.operators[1]
    S = expm(-beta*model.h/2)
    def energy(x):
        result = 0.0
        for z in model.z:
            derivative = (x-z@x@z)/2
            result += np.trace(S@derivative.conj().T@S@derivative).real/dim
        return result
    eigenvalues, vectors = eigh(model.h)
    nodes, weights = np.polynomial.hermite.hermgauss(32)
    average = 0.0
    for node, weight in zip(nodes, weights):
        time = beta*node/math.sqrt(2)  # V has variance1/4.
        U = (vectors*np.exp(1j*time*eigenvalues))@vectors.T
        average += weight*energy(U@X@U.conj().T)/math.sqrt(math.pi)
    formula = t.star_formula(d, beta)
    expected = math.exp(formula["log_phase_forgotten_Gaussian_gradient_squared_ratio_at_s_zero"])
    assert abs(average/energy(X)-expected) < 1e-11
