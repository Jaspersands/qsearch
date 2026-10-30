"""Exact, bounded controls for a false finite-difference log linearization."""
from math import comb

import pytest

from theorems import finite_difference_log_filter as fd


@pytest.fixture(scope="module", params=fd.CONTROL_PRIMES)
def checked_control(request):
    return fd.control(request.param)


def test_actual_finite_stabilizer_and_wrong_linear_kernel(checked_control):
    p = checked_control["p"]
    assert checked_control["stabilizer"] == [[a, a, a] for a in range(p)]
    assert checked_control["linear_log_kernel"] == [[0, 0, 0]]
    assert checked_control["finite_actions_checked"] == p**3
    assert checked_control["direction_logs_checked"] == p**3
    assert checked_control["individual_log_kernels_checked"] == p**3


def test_diagonal_is_falsely_rejected_by_sum_of_exact_logs(checked_control):
    p = checked_control["p"]
    poly = fd.family_polynomial(p)
    assert fd.finite_action(poly, (1, 1, 1), p) == poly
    assert fd.finite_log(poly, (1, 1, 1), p) == {}
    assert checked_control["diagonal_linear_log"] == [
        {"powers": [0, 0, 0, p], "coefficient": 1}]


def test_module_length_has_nonzero_witness_and_full_upper_check(checked_control):
    p = checked_control["p"]
    module = checked_control["module_length"]
    assert module["action_length"] == p + 1
    assert module["I_power_p_nonzero"] is True
    assert module["I_power_p_plus_1_zero"] is True
    assert module["nonzero_mixed_products_by_order"][p] > 0
    assert module["nonzero_mixed_products_by_order"][p + 1] == 0
    assert module["order_p_plus_1_products_checked"] == comb(p + 3, 2)
    assert module["order_p_witness"] == [
        {"powers": [0, 0, 0, p], "coefficient": 1}]


def test_report_keeps_the_family_easy_and_non_algorithmic(checked_control):
    assert checked_control["status"] == "EXACT_REGRESSION_PASS"
    assert checked_control["family_status"] == "EASY_FACTORIZATION_FAMILY"
    assert checked_control["group_class"] == 1
    assert checked_control["matrix_dimension"] == 4


@pytest.mark.parametrize("p", fd.CONTROL_PRIMES)
def test_nonlinear_directional_carry_is_not_linear_in_parameters(p):
    poly = fd.family_polynomial(p)
    # (a-b)^(p-1)(b-c)=0 here, although the linearized carry b is 1.
    direction = (1, 1, 0)
    actual = fd.finite_log(poly, direction, p)
    assert actual == fd.displayed_direction_log(p, direction)
    assert actual.get((0, 0, 0, p), 0) == 0
    assert actual
    basis_logs = [fd.finite_log(poly, e, p) for e in fd.BASIS_DIRECTIONS]
    assert sum(value.get((0, 0, 0, p), 0) for value in basis_logs[:2]) % p == 1


@pytest.mark.parametrize("p", fd.CONTROL_PRIMES)
def test_action_is_literal_monomial_substitution_and_composes(p):
    poly = {(1, 1, 0, 0): 1}
    expected = {(1, 1, 0, 0): 1, (1, 0, 0, 1): 2,
                (0, 1, 0, 1): 1, (0, 0, 0, 2): 2}
    assert fd.finite_action(poly, (1, 2, 3), p) == expected
    family = fd.family_polynomial(p)
    moved = fd.finite_action(family, (1, 2, 3), p)
    assert fd.finite_action(moved, (p - 1, p - 2, p - 3), p) == family
    for _ in range(p):
        family = fd.finite_difference(family, (1, 2, 3), p)
    assert family == {}


@pytest.mark.parametrize("p", fd.CONTROL_PRIMES)
def test_finite_log_handles_nonfamily_polynomials_and_hasse_carry(p):
    assert fd.finite_log({(0, p, 0, 0): 1}, (0, 1, 0), p) == {(0, 0, 0, p): 1}
    assert fd.finite_log({(0, 2, 0, 0): 1}, (0, 1, 0), p) == {(0, 1, 0, 1): 2}
    assert fd.finite_log({(0, 0, 0, p): 1}, (1, 2, 3), p) == {}
    assert fd.finite_log({}, (1, 1, 1), p) == {}


def test_log_actually_iterates_powers_of_T_minus_I(monkeypatch):
    original = fd._action
    inputs = []

    def recording_action(poly, direction, p):
        inputs.append(poly.copy())
        return original(poly, direction, p)

    monkeypatch.setattr(fd, "_action", recording_action)
    p = 5
    poly = {(0, 2, 0, 0): 1}
    assert fd.finite_log(poly, (0, 1, 0), p) == {(0, 1, 0, 1): 2}
    assert inputs == [poly, {(0, 1, 0, 1): 2, (0, 0, 0, 2): 1},
                      {(0, 0, 0, 2): 2}, {}]


def test_formula_corruption_is_detected_independently(monkeypatch):
    monkeypatch.setattr(fd, "displayed_direction_log", lambda p, direction: {})
    with pytest.raises(ArithmeticError, match="directional log formula disagrees"):
        fd.control(5)


def test_report_metadata_does_not_promote_controls(monkeypatch):
    monkeypatch.setattr(fd, "control", lambda p: {"p": p})
    result = fd.report()
    assert result["controls"] == [{"p": p} for p in (5, 7, 11)]
    for key in ("candidate", "hardness_evidence", "new_algorithm_claim",
                "general_stabilizer_solver", "uses_randomness"):
        assert result[key] is False
    assert result["max_control_prime"] == 11


@pytest.mark.parametrize("p", [True, 5.0, "5", 2, 3, 9, 13, 2**127 - 1])
def test_small_prime_guard_precedes_computation(p):
    for operation in (fd.family_polynomial, fd.displayed_basis_logs,
                      fd.module_length_control, fd.control):
        with pytest.raises(ValueError, match="bounded regression"):
            operation(p)
    for operation in (fd.finite_action, fd.finite_difference, fd.finite_log):
        with pytest.raises(ValueError, match="bounded regression"):
            operation({}, (0, 0, 0), p)
    with pytest.raises(ValueError, match="bounded regression"):
        fd.displayed_direction_log(p, (0, 0, 0))


@pytest.mark.parametrize("direction", [(1, 2), (1, 2, 3, 4), (-1, 0, 0),
                                       (5, 0, 0), (True, 0, 0), (1.0, 0, 0)])
def test_direction_guard(direction):
    with pytest.raises(ValueError, match="canonical"):
        fd.finite_log({}, direction, 5)


@pytest.mark.parametrize("poly", [{(0, 0, 0, 6): 1}, {(0, 0, 0, -1): 1},
                                  {(0, 0, 0): 1}, {(0, 0, 0, True): 1},
                                  {(0, 0, 0, 1): 1.5}])
def test_polynomial_degree_and_integer_guards(poly):
    with pytest.raises(ValueError, match="exponents"):
        fd.finite_action(poly, (1, 0, 0), 5)


def test_coefficients_are_normalized_without_mutating_input():
    poly = {(1, 0, 0, 0): -1, (0, 0, 0, 0): 10}
    original = poly.copy()
    assert fd.finite_action(poly, (0, 0, 0), 5) == {(1, 0, 0, 0): 4}
    assert poly == original
