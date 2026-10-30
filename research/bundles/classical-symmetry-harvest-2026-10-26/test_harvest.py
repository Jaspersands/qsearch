"""Supplied arithmetic controls for the native attack's exact identities."""

from math import gcd
from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye, zeros
from sympy.matrices.normalforms import hermite_normal_form

from harvest import (
    adjoin_and_close, coprime_scalar_shift, entries, outside_lattice,
    pell_product_factor, pullback_certificate, trace_coordinates,
)
from additive_source import adjoint, construct, multiply, quaternion_matrix, scalar_matrix
from kernel_output import odd_maximal_order, odd_maximal_split

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "polarization-completion-probe-2026-10-25"))
from polarization_probe import norm_table


def easy_unit_fixture(denominator=2):
    order = odd_maximal_order(11)
    zero, one, delta, unit = zeros(4, 1), order.unit, eye(4)[:, 2], eye(4)[:, 1]
    u = quaternion_matrix([[one, delta], [zero, one]])
    inverse = quaternion_matrix([[one, -delta], [zero, one]])
    v = quaternion_matrix([[unit, zero], [zero, one]])
    z = multiply(order, adjoint(order, u), u)
    w = multiply(order, multiply(order, inverse, v), u)
    return order, z, u.scale(denominator), inverse.scale(denominator), w


@pytest.mark.parametrize("denominator", [2, 5, 7])
def test_pullback_of_a_missing_native_unit_enlarges_order(denominator):
    order, z, c, f, w = easy_unit_fixture(denominator)
    basis = Matrix.diag(1, 3, 1, 3)
    assert outside_lattice(w, basis)
    assert not outside_lattice(c, basis) and not outside_lattice(f, basis)
    pulled, report = pullback_certificate(order, z, c, f, w, denominator**2, 9)
    assert report["coprime_index_transport"] is True
    assert report["native_pullback_executed"] is False
    assert outside_lattice(pulled, basis)
    recovered, chain = adjoin_and_close(order, basis, entries(pulled))
    assert recovered == eye(4)
    assert chain == [9, 3, 1]


def test_bad_auxiliary_prime_can_hide_every_missing_corner():
    order, z, c, f, w = easy_unit_fixture(3)
    basis = Matrix.diag(1, 3, 1, 3)
    pulled, report = pullback_certificate(order, z, c, f, w, 9, 9)
    assert outside_lattice(w, basis)
    assert not outside_lattice(pulled, basis)
    assert report["coprime_index_transport"] is False
    recovered, chain = adjoin_and_close(order, basis, entries(pulled))
    assert recovered == basis and chain == [9]


def test_wrong_polarization_or_symmetry_rejected():
    order, z, c, f, w = easy_unit_fixture()
    with pytest.raises(ValueError, match="converter"):
        pullback_certificate(order, scalar_matrix(order, eye(2)), c, f, w, 4, 9)
    with pytest.raises(ValueError, match="symmetry"):
        pullback_certificate(order, z, c, f, w.scale(2), 4, 9)
    with pytest.raises(ValueError, match="integral"):
        pullback_certificate(order, z, c, f, w.scale(Matrix([[1]])[0]/2), 4, 9)


@pytest.mark.parametrize("n,k", [(3, 2), (17, 12), (99, 70), (577, 408)])
def test_pell_zero_query_is_always_an_integral_product(n, k):
    order = odd_maximal_order(11)
    p, inverse = pell_product_factor(n, k)
    z = construct(order, zeros(4, 1), n, (2*k*k, 2*k, 0, 0))["polarization"]
    assert scalar_matrix(order, p.T*p) == z
    assert p*inverse == eye(16)
    assert all(x.is_Integer for x in inverse)


def unit_closed_index_seventeen_order(order):
    modulus = 17
    line = Matrix([4, 1])
    row = Matrix([[Matrix.hstack(line, a*line).det() % modulus
                   for a in odd_maximal_split(11, modulus)]])
    pivot = next(i for i in range(4) if row[i] % modulus)
    inverse = pow(int(row[pivot]), -1, modulus)
    columns = [modulus*eye(4)[:, pivot]]
    for i in range(4):
        if i != pivot:
            columns.append(eye(4)[:, i]-(int(row[i])*inverse % modulus)*eye(4)[:, pivot])
    basis = hermite_normal_form(Matrix.hstack(*columns))
    assert basis.det() == 17
    closed, chain = adjoin_and_close(order, basis, [])
    assert closed == basis and chain == [17]
    return basis


def test_complete_zero_query_automorphism_group_adds_no_information():
    order = odd_maximal_order(11)
    basis = unit_closed_index_seventeen_order(order)
    table, _ = norm_table(order, 1)
    units = table[1]
    i = eye(4)[:, 1]
    assert {tuple(x) for x in units} == {tuple(x) for x in (order.unit, -order.unit, i, -i)}
    assert all(all(x.is_Integer for x in basis.inv()*unit) for unit in units)
    p, inverse = pell_product_factor(17, 12)
    p, inverse = scalar_matrix(order, p), scalar_matrix(order, inverse)
    z = construct(order, zeros(4, 1), 17, (288, 24, 0, 0))["polarization"]
    # These generate the ENTIRE monomial group, not a random symmetry sample:
    # one coordinate unit and adjacent swaps generate (O^*)^16 semidirect S16.
    generators = []
    coefficients = [a.copy() for a in scalar_matrix(order, eye(16)).coefficients]
    for k in range(4):
        coefficients[k][0, 0] = i[k]
    from additive_source import QMatrix
    generators.append(QMatrix(tuple(coefficients)))
    for j in range(15):
        permutation = eye(16)
        permutation.row_swap(j, j+1)
        generators.append(scalar_matrix(order, permutation))
    for value in generators:
        w = multiply(order, multiply(order, inverse, value), p)
        assert multiply(order, multiply(order, adjoint(order, w), z), w) == z
        assert not outside_lattice(w, basis)
    assert basis.det() > 1


@pytest.mark.parametrize("p", [5, 7, 11, 101])
def test_scalar_shift_avoids_characteristic_degree_without_factoring(p):
    for trace in range(-5, 6):
        for degree in range(max(1, (trace*trace+3)//4), max(1, (trace*trace+3)//4)+12):
            shift, new_degree = coprime_scalar_shift(p, trace, degree)
            assert shift in (0, 1, 2)
            assert new_degree == degree+trace*shift+shift*shift
            assert gcd(new_degree, p) == 1
    assert coprime_scalar_shift(p, 0, p) == (1, p+1)


def test_trace_pairings_detect_nonintegral_relative_coordinates():
    order = odd_maximal_order(11)
    basis = Matrix.diag(1, 3, 1, 3)
    gram = Matrix(4, 4, lambda i, j:
                  (order.traces*order.multiply(basis[:, i], order.star(basis[:, j])))[0])
    x = eye(4)[:, 1]
    mixed = Matrix([(order.traces*order.multiply(x, order.star(basis[:, j])))[0]
                    for j in range(4)])
    assert trace_coordinates(gram, mixed) == basis.inv()*x
    assert trace_coordinates(gram, mixed)[1].q == 3


def test_even_index_must_be_saturated_before_coprime_even_converter():
    assert all(gcd(2*k, 18) != 1 for k in range(1, 30))
    assert gcd(2, 9) == 1


@pytest.mark.parametrize("n,k", [(2, 1), (1, 0), (17, 13)])
def test_non_pell_factor_rejected(n, k):
    with pytest.raises(ValueError, match="Pell"):
        pell_product_factor(n, k)


def test_fractional_additions_are_not_truncated_to_integer_lattice():
    from sympy import Rational
    with pytest.raises(ValueError, match="integral"):
        adjoin_and_close(odd_maximal_order(11), eye(4), [Matrix([Rational(1, 2), 0, 0, 0])])


def test_receipt_does_not_promote_controls_to_dequantization():
    from replay_harvest import receipt
    result = receipt()
    assert result["execution_scope"]["exact_matrix_and_order_closure_controls"] is True
    assert result["execution_scope"]["independent_review"] is True
    assert all(value is False for key, value in result["execution_scope"].items()
               if key not in {"exact_matrix_and_order_closure_controls", "independent_review"})
    assert result["review_followup"]["corrected_statement_independently_re_reviewed"] is False


def test_uniform_sampler_is_an_obligation_not_an_implemented_solver():
    from replay_harvest import receipt
    result = receipt()
    assert result["uniform_hitting_obligation"] == {
        "single_uniform_sampler_required": True,
        "single_polynomial_required": True,
        "original_paid_input_length_required": True,
        "all_adaptively_reached_orders_required": True,
        "polynomial_query_and_frame_lengths_required": True,
        "native_data_only_required": True,
        "sampler_implemented": False,
        "hitting_bound_proved": False,
    }
    assert "additive-source-independent-review-2026-10-26/REVIEW.md" in result["hashes"]
