"""Algebraic scope tests; no curve models or geometric factor computation."""

import pytest
from sympy import Matrix, Rational, eye, zeros

from nonfree_factor_bound import (
    automorphism_certificate, factor_certificate, scalar_value, shear_product_control,
)
from kernel_output import matrix_multiply, matrix_star, odd_maximal_order
from polarization_probe import gram_matrix, norm_table, unit_projectors


@pytest.fixture(scope="module")
def data():
    order = odd_maximal_order(11)
    i, h = eye(4)[:, 1], eye(4)[:, 2]
    return order, i, h


@pytest.mark.parametrize("reverse", [False, True])
def test_positive_controls_extract_short_noncommuting_map(data, reverse):
    order, i, h = data
    x, y = (i, h) if reverse else (h, i)
    a, beta, d, projector = shear_product_control(order, x, y, reverse)
    result = factor_certificate(order, beta, a, beta, d, projector)
    assert result["factor_leaves_known_quadratic_algebra"]
    assert result["witness_does_not_commute"]
    assert result["witness_degree"] == result["degree_bound"]
    assert not result["factor_assumed_isomorphic_to_original_curve"]
    assert not result["native_decomposition_or_enumeration_executed"]
    if reverse:
        assert (a, result["first_factor_degree"], result["witness_degree"]) == (7, 4, 12)
    else:
        assert (a, result["first_factor_degree"], result["witness_degree"]) == (2, 1, 1)


def test_enormous_second_diagonal_does_not_inflate_small_a_bound(data):
    order, i, h = data
    a, beta, d, projector = shear_product_control(order, 10**30*h, i)
    result = factor_certificate(order, beta, a, beta, d, projector)
    assert d > 10**60
    assert result["a"] == 2
    assert result["witness_degree"] == result["degree_bound"] == 1


def test_complement_and_coordinate_swap_keep_the_same_obstruction(data):
    order, i, h = data
    a, beta, d, projector = shear_product_control(order, i, h, True)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    first = factor_certificate(order, beta, a, beta, d, projector)
    other = factor_certificate(order, beta, a, beta, d, identity-projector)
    assert other["first_factor_degree"] == a-first["first_factor_degree"]
    assert Matrix(other["witness_coefficients"]) == -Matrix(first["witness_coefficients"])
    swap = Matrix.vstack(zeros(4, 1), order.unit, order.unit, zeros(4, 1))
    swapped = matrix_multiply(order, matrix_multiply(order, swap, projector), swap)
    flipped = factor_certificate(order, beta, d, order.star(beta), a, swapped)
    assert flipped["witness_does_not_commute"]
    assert flipped["witness_degree"] <= d*d//4


def test_known_quadratic_factor_is_not_a_positive_signal(data):
    order, i, _ = data
    a, beta, d, projector = shear_product_control(order, i, i)
    result = factor_certificate(order, i, a, beta, d, projector)
    assert not result["witness_does_not_commute"]
    assert not result["factor_leaves_known_quadratic_algebra"]


def test_zero_first_component_is_handled_without_dividing_by_m(data):
    order, i, _ = data
    projector = Matrix.vstack(zeros(4, 1), zeros(4, 1), zeros(4, 1), order.unit)
    result = factor_certificate(order, i, 1, zeros(4, 1), 1, projector)
    assert result["first_factor_degree"] == result["witness_degree"] == 0
    assert not result["factor_leaves_known_quadratic_algebra"]


def test_projector_from_previous_free_factor_code_obeys_general_identity(data):
    order, i, h = data
    a, beta, d, _ = shear_product_control(order, h, i)
    table, _ = norm_table(order, a)
    witnesses = list(unit_projectors(order, a, beta, d, table))
    assert witnesses
    results = [factor_certificate(order, beta, a, beta, d, projector)
               for _, projector in witnesses]
    assert any(result["witness_does_not_commute"] for result in results)
    assert all(result["witness_degree"] <= a*a//4 for result in results)


def test_rational_idempotent_is_not_promoted_to_an_integral_factor(data):
    order, i, _ = data
    projector = Rational(1, 2)*Matrix.vstack(order.unit, i, -i, order.unit)
    assert matrix_multiply(order, projector, projector) == projector
    assert matrix_star(order, projector) == projector
    with pytest.raises(ValueError, match="integral binary"):
        factor_certificate(order, i, 1, zeros(4, 1), 1, projector)


def test_bad_input_promises_are_rejected(data):
    order, i, h = data
    a, beta, d, projector = shear_product_control(order, h, i)
    with pytest.raises(ValueError, match="quadratic"):
        factor_certificate(order, i, a, beta, d, projector)
    with pytest.raises(ValueError, match="nonscalar"):
        factor_certificate(order, order.unit, a, beta, d, projector)
    with pytest.raises(ValueError, match="idempotent"):
        factor_certificate(order, beta, a, beta, d, 2*projector)
    with pytest.raises(ValueError, match="unimodular"):
        factor_certificate(order, beta, a, beta, d+1, projector)


def test_idempotence_without_orthogonality_is_insufficient(data):
    order, i, _ = data
    projector = Matrix.vstack(order.unit, i, zeros(4, 1), zeros(4, 1))
    assert matrix_multiply(order, projector, projector) == projector
    with pytest.raises(ValueError, match="orthogonal"):
        factor_certificate(order, i, 1, zeros(4, 1), 1, projector)


def test_huge_diagonals_from_known_basis_change_do_not_remove_classical_gate(data):
    order, i, h = data
    a, beta, d, projector = shear_product_control(order, h, i)
    original = gram_matrix(order, a, beta, d)
    n, one = 10**12, order.unit
    change = Matrix.vstack(n*one, (n+1)*one, (n-1)*one, n*one)
    inverse = Matrix.vstack(n*one, -(n+1)*one, -(n-1)*one, n*one)
    moved_h = matrix_multiply(order, matrix_multiply(order, matrix_star(order, change), original), change)
    moved_p = matrix_multiply(order, matrix_multiply(order, inverse, projector), change)
    moved_a = scalar_value(order, moved_h[:4, :])
    moved_d = scalar_value(order, moved_h[12:, :])
    assert min(moved_a, moved_d) > 10**24
    assert factor_certificate(order, beta, moved_a, moved_h[4:8, :], moved_d, moved_p)[
        "witness_does_not_commute"]
    restored_h = matrix_multiply(order, matrix_multiply(order, matrix_star(order, inverse), moved_h), inverse)
    restored_p = matrix_multiply(order, matrix_multiply(order, change, moved_p), inverse)
    assert restored_h == original and restored_p == projector
    assert factor_certificate(order, beta, a, beta, d, restored_p)["degree_bound"] == 1


def test_binary_automorphism_escape_has_small_first_column_witness(data):
    order, i, h = data
    a, beta, d, projector = shear_product_control(order, 10**20*h, i)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    result = automorphism_certificate(order, beta, a, beta, d, identity-2*projector)
    assert result["branch"] == "first_column_y"
    assert result["witness_degree"] == result["degree_bound"] == 4
    assert not result["native_automorphism_computation_executed"]


def test_known_first_column_can_hide_an_elliptic_unit_phase(data):
    order, i, h = data
    # H is the shear Gram matrix over Q(h), whereas eta=i is an already
    # available noncommuting elliptic unit. No hard positive signal remains.
    beta, eta = h, i
    b = order.multiply(beta, order.unit-eta)
    automorphism = Matrix.vstack(order.unit, b, zeros(4, 1), eta)
    result = automorphism_certificate(order, h, 1, beta, 4, automorphism)
    assert result["branch"] == "elliptic_unit_phase"
    assert result["witness_degree"] == 1


def test_completed_square_branch_catches_noncommuting_top_entry(data):
    order, i, h = data
    automorphism = Matrix.vstack(i, zeros(4, 1), zeros(4, 1), order.unit)
    result = automorphism_certificate(order, h, 1, zeros(4, 1), 1, automorphism)
    assert result["branch"] == "first_column_completed_square"
    assert result["witness_degree"] == 1


def test_quadratic_automorphism_and_nonunitary_input_are_not_escapes(data):
    order, i, _ = data
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    result = automorphism_certificate(order, i, 1, zeros(4, 1), 1, identity)
    assert result["branch"] == "known_quadratic_automorphism"
    assert result["witness_coefficients"] is None
    with pytest.raises(ValueError, match="H-unitary"):
        automorphism_certificate(order, i, 1, zeros(4, 1), 1, 2*identity)


def test_receipt_separates_deductive_scope_from_supplied_controls():
    from replay_nonfree_bound import receipt
    result = receipt()
    assert result["scope"]["nonfree_factor_case_is_deductive_not_geometric_test"]
    assert not result["scope"]["native_nonfree_factor_constructed"]
    assert not result["scope"]["native_low_degree_enumeration_executed"]
    assert not result["scope"]["independent_review"]
    assert not result["scope"]["quantum_advantage_established"]
    assert [x["witness_degree"] for x in result["automorphism_controls"]] == [4, 1]
