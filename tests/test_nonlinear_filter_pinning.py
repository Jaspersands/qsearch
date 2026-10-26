from fractions import Fraction as Q
from itertools import combinations, product
from math import comb

import pytest

from theorems import nonlinear_filter_pinning as f


@pytest.mark.parametrize("rho", [Q(1, 2), Q(3, 7), Q(2, 5)])
@pytest.mark.parametrize("degree", [0, 1, 3, 6])
def test_biased_shell_moments_equal_complete_source_enumeration(rho, degree):
    M = 6
    a = tuple(Q((-1)**k, 2*k+1) for k in range(degree+1))
    Z, mean, second = f.exact_moments(a, M, rho)
    masses = [Q(comb(M, s))*rho**s*(1-rho)**(M-s)*f.filter_value(a, M, rho, s)**2
              for s in range(M+1)]
    assert sum(masses) == Z
    assert sum(s*m for s, m in enumerate(masses))/Z == mean
    assert sum(s*s*m for s, m in enumerate(masses))/Z == second


def test_shell_recurrence_is_actual_elementary_symmetric_polynomial():
    M, rho = 5, Q(3, 7)
    for bits in product((0, 1), repeat=M):
        for degree in range(M+1):
            expected = Q(0)
            for subset in combinations(range(M), degree):
                value = Q(1)
                for i in subset:
                    value *= bits[i]-rho
                expected += value
            a = (Q(0),)*degree+(Q(1),)
            assert f.filter_value(a, M, rho, sum(bits)) == expected


@pytest.mark.parametrize("order", [0, 1, 2, 3])
def test_pairwise_transfer_pays_twice_the_test_support(order):
    required = 200+2*order
    assert f.transfer_budget(required, 50, order)["vertex_budget"] == required
    with pytest.raises(ValueError, match="pairwise"):
        f.transfer_budget(required-1, 50, order)


def test_published_parameters_allow_only_two_nontrivial_moments():
    assert f.transfer_budget(205, 50, 2)["moment_order"] == 2
    with pytest.raises(ValueError):
        f.transfer_budget(205, 50, 3)


def test_native_polynomials_agree_only_inside_proved_cutoff():
    control = f.native_control()
    assert control["enumerated_polynomials"] == 2401
    assert control["native_norm"] == control["source_norm"]
    assert control["norm_transfer_valid"] and not control["mean_transfer_valid"]
    assert Q(control["forbidden_mean_transfer_error"]) > 0


def test_triangular_residual_coordinates_really_biject():
    images = set()
    for values in product(range(5), repeat=4):
        coordinates = f.residual_map(values, (1, 3, 2), 5)
        assert f.inverse_residual_map(coordinates, (1, 3, 2), 5) == values
        images.add(coordinates)
    assert len(images) == 5**4


@pytest.mark.parametrize("n", [0, 1, 7, 32])
def test_integer_binomial_tail_and_outward_rounding(n):
    rho = Q(3, 7)
    for threshold in range(n+2):
        exact = sum((Q(comb(n, j))*rho**j*(1-rho)**(n-j) for j in range(threshold, n+1)), Q(0))
        assert f.binomial_tail(n, rho, threshold) == exact
        assert f.enclose(exact, 40) <= exact <= f.enclose(exact, 40, upper=True)


def test_all_pin_patterns_are_dominated_by_all_pass_pins():
    M, rho, threshold, K = 7, Q(3, 7), 5, 3
    cap = f.binomial_tail(M-K, rho, threshold-K)
    for fixed in range(K+1):
        for accepted in range(fixed+1):
            assert f.binomial_tail(M-fixed, rho, threshold-accepted) <= cap


def test_tail_witness_is_valid_without_a_binomial_target_law():
    probabilities = (Q(1, 10), Q(0), Q(1, 5), Q(0), Q(7, 10))
    mean = sum(s*p for s, p in enumerate(probabilities))
    second = sum(s*s*p for s, p in enumerate(probabilities))
    witness = f.tail_witness(4, mean, second, 3)
    assert f.verify_tail_witness(4, witness)
    assert Q(witness["probability_lower_exact"]) <= sum(probabilities[3:])


@pytest.mark.parametrize("field,value", [
    ("probability_lower_dyadic", "1"), ("probability_lower_exact", "1"),
    ("support_points_checked", 999), ("variance", "-1"),
    ("minorant_coefficients", ["1", "0", "0"]),
])
def test_tampered_tail_certificate_rejected(field, value):
    witness = f.tail_witness(5, Q(3), Q(10), 3)
    witness[field] = value
    with pytest.raises((ValueError, ArithmeticError)):
        f.verify_tail_witness(5, witness)


def test_live_rational_candidate_and_method_specific_exponential_gap():
    M, rho, D = 2051, Q(1026, 2053), 50
    a = f.rational_filter(M, rho, D)
    Z, mean, second = f.exact_moments(a, M, rho)
    witness = f.tail_witness(M, mean, second, 1299)
    assert Z > 0
    assert Q(64313, 100000) < mean/M < Q(64314, 100000)
    assert Q(witness["probability_lower_dyadic"]) > Q(475, 1000)
    comparison = f.pinning_comparison(M, rho, 100, witness, Q(1, 100))
    assert Q(comparison["component_tail_upper_dyadic"]) < Q(2, 10**24)
    assert Q(comparison["signed_total_absolute_weight_lower"]) > 10**23
    assert Q(comparison["positive_mixture_mass_above_pin_cap_lower"]) > Q(465, 1000)
    assert "not general classical search" in comparison["scope"]
    assert 1-(1-Q(witness["probability_lower_dyadic"])+Q(1, 100))**5 > Q(95, 100)


def test_actual_benchmark_degree_decoder_never_receives_the_error_support():
    result = f.decoder_control()
    assert result["source_error_sparse"] == result["recovered_error_sparse"]
    assert len(result["source_error_sparse"]) == 100
    assert not result["decoder"]["source_error_or_support_supplied"]
    assert result["decoder"]["full_syndromes_replayed"]
    assert result["basis_control_NOT_coherent_execution"]


def test_unrestricted_residual_pins_do_not_get_a_false_obstruction():
    witness = f.tail_witness(8, Q(7), Q(50), 6)
    row = f.pinning_comparison(8, Q(1, 2), 8, witness)
    assert Q(row["component_tail_upper_dyadic"]) == 1
    assert Q(row["positive_mixture_tail_deficit_lower"]) == 0
    assert Q(row["signed_total_absolute_weight_lower"]) == 1
    assert Q(row["positive_mixture_mass_above_pin_cap_lower"]) == 0


def test_no_useful_tail_bound_means_unknown_not_zero_success():
    witness = f.tail_witness(8, Q(2), Q(5), 6)
    assert Q(witness["probability_lower_exact"]) == 0
    assert f.verify_tail_witness(8, witness)


@pytest.mark.parametrize("operation", [
    lambda: f.exact_moments((Q(0),), 4, Q(1, 2)),
    lambda: f.exact_moments((0.1,), 4, Q(1, 2)),
    lambda: f.shell_norms(4, 0.5, 1),
    lambda: f.filter_value((Q(1),), 4, Q(1, 2), 5),
    lambda: f.binomial_tail(-1, Q(1, 2), 1),
    lambda: f.tail_witness(4, Q(3), Q(1), 2),
])
def test_invalid_proof_inputs_fail_closed(operation):
    with pytest.raises(ValueError):
        operation()
