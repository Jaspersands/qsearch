"""Exact arithmetic controls; not native geometry, sampling or an HSP run."""

from pathlib import Path
import sys

import pytest
from sympy import Matrix, Rational, eye, kronecker_product, zeros

from small_multiplier import (
    LOW_HIGH, commutator_obstruction, noncommuting_entries,
    pullback_certificate, reorder, small_multiplier, source_obstruction,
)
from additive_source import (
    QMatrix, adjoint, blocks, construct, four_square_matrix,
    multiply, scalar_matrix, shear,
)
from kernel_output import odd_maximal_order
from pair_order import norm, trace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "active-coset-density-2026-10-26"))
from coset_controls import conjugate, pell_unit_i_generators
from harvest import adjoin_and_close, outside_lattice


@pytest.mark.parametrize("n,roots", [(2, (3, 2, 1, 1)),
                                    (3, (8, 4, 0, 0)),
                                    (5, (24, 4, 4, 4))])
@pytest.mark.parametrize("beta", [(0, 0, 0, 0), (4, 0, 0, 0), (2, -3, 1, 4)])
def test_block_isogeny_and_principal_inverse(n, roots, beta):
    order = odd_maximal_order(103)
    beta = Matrix(beta)
    source = small_multiplier(order, beta, n, roots)
    identity = scalar_matrix(order, eye(16))
    cross = QMatrix(tuple(x[:8, 8:] for x in source["h"].coefficients))
    diagonal = QMatrix(tuple(n*x*eye(4) for x in beta))
    negative_dual = QMatrix(tuple(-n*x*eye(4) for x in order.star(beta)))
    t = scalar_matrix(order, four_square_matrix(roots))
    assert cross == blocks(diagonal, t, adjoint(order, t), negative_dual)
    assert multiply(order, source["h"], source["inverse_h"]) == identity
    assert multiply(order, source["c"], source["cbar"]) == identity.scale(n*n)
    assert multiply(order, source["cbar"], source["c"]) == identity.scale(n*n)
    assert multiply(order, multiply(order, adjoint(order, source["c"]),
                                   source["h"]), source["c"]) == identity.scale(n*n)
    assert source["corner_degree_bound"] == n**4
    assert source["supplied_order_control"] is True
    assert source["native_model_constructed"] is False


def test_reorder_round_trip_handles_nonsymmetric_matrices_and_multiple_copies():
    order = odd_maximal_order(11)
    matrix = scalar_matrix(order, Matrix(32, 32, lambda i, j: 100*i+j))
    permuted = reorder(matrix)
    assert permuted.coefficients[0][0, 8] == LOW_HIGH[8]
    assert reorder(permuted, inverse=True) == matrix
    with pytest.raises(ValueError, match="divisible by 16"):
        reorder(scalar_matrix(order, eye(8)))


@pytest.fixture(scope="module")
def pell_data():
    order = odd_maximal_order(11)
    basis = Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                    [0, 0, 17, 4], [0, 0, 0, 1]])
    delta = eye(4)[:, 2]
    return order, basis, delta, pell_unit_i_generators(order, 17, 12)


def test_small_multiplier_erases_the_complete_integral_coset_control(pell_data):
    order, basis, delta, generators = pell_data
    assert adjoin_and_close(order, basis, [])[0] == basis
    assert outside_lattice(scalar_matrix(order, eye(16)), basis) == ()
    assert any(x.is_Integer is not True for x in basis.inv()*delta)
    roots = (288, 24, 0, 0)
    base = small_multiplier(order, zeros(4, 1), 17, roots)
    useful = []
    for multiplier in (1, 8, 16):
        moved_delta = multiplier*delta
        moved = small_multiplier(order, 17*moved_delta, 17, roots)
        # The entire-group proof uses this identity, not sampling its elements.
        s = reorder(shear(order, moved_delta))
        assert multiply(order, s, moved["c"]) == base["c"]
        for w0 in generators:
            w = conjugate(order, w0, moved_delta)
            assert not outside_lattice(w0, basis)
            pulled = multiply(order, multiply(order, moved["cbar"], reorder(w)), moved["c"])
            expected = multiply(order, multiply(order, base["cbar"], reorder(w0)), base["c"])
            assert pulled == expected
            assert not outside_lattice(pulled, basis)
            useful.append(bool(outside_lattice(w, basis)))
    assert any(useful)


def test_transverse_pullback_can_already_be_in_R(pell_data):
    order, basis, delta, generators = pell_data
    source = small_multiplier(order, 17*delta, 17, (288, 24, 0, 0))
    w = conjugate(order, generators[0], delta)
    pulled, report = pullback_certificate(order, source, w, alpha=delta)
    assert outside_lattice(w, basis)
    assert not outside_lattice(pulled, basis)
    assert report["outside_quadratic_field"] is True
    assert report["noncommuting_entries"]
    assert report["outside_order_preservation_claimed"] is False
    assert report["native_extraction_executed"] is False
    assert report["corner_degree_bound"] == 17**4
    for col in range(16):
        assert sum(report["degrees"][:, col]) == 17**4
    recovered = multiply(order, multiply(order, source["c"], pulled), source["cbar"])
    assert reorder(recovered.scale(Rational(1, 17**4)), inverse=True) == w


def test_stabilization_with_copy_mixing_keeps_the_same_bound(pell_data):
    order, _, delta, generators = pell_data
    source = small_multiplier(order, 17*delta, 17, (288, 24, 0, 0), copies=8)
    exchange = eye(8)
    exchange.row_swap(0, 7)
    shuffle = scalar_matrix(order, kronecker_product(exchange, eye(16)))
    w = multiply(order, shuffle, conjugate(order, generators[5], delta).repeat(8))
    pulled, report = pullback_certificate(order, source, w)
    assert pulled.shape == (128, 128)
    assert report["dimension"] == 128
    assert report["corner_degree_bound"] == 17**4
    assert max(report["degrees"]) <= 17**4
    assert report["outside_quadratic_field"] is None


def test_large_query_coefficients_do_not_increase_the_transverse_bound():
    order = odd_maximal_order(103)
    alpha = eye(4)[:, 1]
    for beta in (alpha, alpha+10**40*order.unit, 10**40*alpha):
        source = small_multiplier(order, beta, 2, (3, 2, 1, 1))
        result = source_obstruction(order, alpha, beta, 2, 103)
        assert source["corner_degree_bound"] == 16
        assert result["discriminant"] == -4
        assert result["commutator_norm_upper_bound"] == 64
        assert result["all_bounded_maps_commute_conditional"] is True
        assert result["native_orientation_authenticated"] is False
        assert result["no_order_growth_requires_quadratic_saturation"] is True
    result = source_obstruction(order, alpha, alpha, 3, 103)
    assert result["all_bounded_maps_commute_conditional"] is False
    assert result["conclusion_if_inequality_fails"] == "no_conclusion"


@pytest.mark.parametrize("p,alpha,x", [
    (7, (0, 0, 1, 0), (0, 1, 0, 0)),
    (11, (0, 1, 0, 0), (0, 0, 1, 0)),
    (103, (2, 3, -1, 4), (1, -2, 3, -1)),
    (103, (0, 1, 0, 0), (5, 0, 0, 0)),
    (103, (0, 1, 0, 0), (0, 0, 0, 0)),
])
def test_commutator_discriminant_bound_and_ramified_divisibility(p, alpha, x):
    order = odd_maximal_order(p)
    alpha, x = Matrix(alpha), Matrix(x)
    commutator = order.multiply(alpha, x)-order.multiply(x, alpha)
    d_alpha = trace(order, alpha)**2-4*norm(order, alpha)
    d_x = trace(order, x)**2-4*norm(order, x)
    mixed = 2*trace(order, order.multiply(alpha, x))-trace(order, alpha)*trace(order, x)
    degree = norm(order, commutator)
    assert degree == (d_alpha*d_x-mixed*mixed)/4
    assert degree <= abs(d_alpha)*norm(order, x)
    assert degree % p == 0
    if commutator != zeros(4, 1):
        assert degree >= p


def test_strict_inequality_is_essential_and_equality_has_a_real_counterexample():
    order = odd_maximal_order(7)
    alpha, x = eye(4)[:, 2], eye(4)[:, 1]
    assert trace(order, alpha)**2-4*norm(order, alpha) == -7
    assert norm(order, x) == 1
    assert norm(order, order.multiply(alpha, x)-order.multiply(x, alpha)) == 7
    assert commutator_obstruction(7, -7, 1)["all_bounded_maps_commute_conditional"] is False


def test_rational_unitary_is_not_a_native_integral_symmetry():
    order = odd_maximal_order(103)
    source = small_multiplier(order, [0, 1, 0, 0], 2, (3, 2, 1, 1))
    u = eye(16)
    u[:2, :2] = Matrix([[Rational(3, 5), Rational(-4, 5)],
                        [Rational(4, 5), Rational(3, 5)]])
    w = multiply(order, multiply(order, source["c"], scalar_matrix(order, u)),
                 source["cbar"]).scale(Rational(1, source["a"]))
    assert multiply(order, multiply(order, adjoint(order, w), source["h"]), w) == source["h"]
    assert not w.integral
    with pytest.raises(ValueError, match="integral symmetry"):
        pullback_certificate(order, source, reorder(w, inverse=True))


def test_invalid_symmetry_and_tampered_multiplier_are_rejected():
    order = odd_maximal_order(103)
    source = small_multiplier(order, [0, 1, 0, 0], 2, (3, 2, 1, 1))
    identity = scalar_matrix(order, eye(16))
    with pytest.raises(ValueError, match="H-unitary"):
        pullback_certificate(order, source, identity.scale(2))
    tampered = dict(source, cbar=source["cbar"].scale(2))
    with pytest.raises(ValueError, match="invalid small-multiplier"):
        pullback_certificate(order, tampered, identity)


@pytest.mark.parametrize("p,disc,bound", [(15, -4, 16), (True, -4, 16),
                                         (103, -2, 16), (103, 0, 16),
                                         (103, -4, -1), (103, -4, True)])
def test_invalid_numeric_obstructions_are_rejected(p, disc, bound):
    with pytest.raises(ValueError):
        commutator_obstruction(p, disc, bound)


def test_scalar_wrong_field_fractional_and_wrong_shape_inputs_are_rejected():
    order = odd_maximal_order(103)
    alpha, beta = eye(4)[:, 1], eye(4)[:, 2]
    with pytest.raises(ValueError, match="commute"):
        source_obstruction(order, alpha, beta, 2, 103)
    with pytest.raises(ValueError, match="scalar query"):
        source_obstruction(order, alpha, order.unit, 2, 103)
    with pytest.raises(ValueError, match="nonscalar orientation"):
        source_obstruction(order, order.unit, beta, 2, 103)
    with pytest.raises(ValueError, match="integral"):
        source_obstruction(order, alpha/2, alpha, 2, 103)
    with pytest.raises(ValueError, match="coordinates"):
        source_obstruction(order, alpha[:2, :], alpha, 2, 103)
    with pytest.raises(ValueError, match="denominator"):
        source_obstruction(order, alpha, alpha, True, 103)
    with pytest.raises(ValueError, match="copy count"):
        small_multiplier(order, alpha, 2, (3, 2, 1, 1), copies=False)
    with pytest.raises(ValueError, match="four-square norm"):
        small_multiplier(order, alpha, 2, (1, 2, 3, 4))
    with pytest.raises(ValueError, match="nonscalar"):
        noncommuting_entries(order, scalar_matrix(order, eye(16)), order.unit)
