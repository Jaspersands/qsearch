from itertools import product

import pytest
from sympy import Matrix, eye, zeros

from product_corners import (
    alternating_form, complete_by_corners, complete_with_known_map, corner_ranks, gaussian_fixture,
    matrix_multiply, matrix_star, mod, odd_maximal_order, rank_mod,
    reference_gram, transport_generators, weak_corner_actions,
)
from kernel_output import action, odd_maximal_split, product_actions


def local_planes(prime):
    lines = [Matrix([1, 0])]+[Matrix([z, 1]) for z in range(prime)]
    for first in lines:
        for second in lines:
            k = zeros(4, 2)
            k[:2, 0], k[2:, 1] = first, second
            yield k, False
    for entries in product(range(prime), repeat=4):
        a = Matrix(2, 2, entries)
        if int(a.det()) % prime == prime-1:
            yield eye(2).col_join(a), True


@pytest.mark.parametrize("prime", [3, 5])
def test_complete_local_classification(prime):
    j, counts = alternating_form(2), {False: 0, True: 0}
    row_map = eye(4)[:, [0, 2]].T*j
    for plane, transverse in local_planes(prime):
        assert rank_mod(plane, prime) == 2
        assert mod(plane.T*j*plane, prime) == zeros(2)
        ranks = corner_ranks(plane*row_map, prime)
        expected = ((4, 4), (4, 4)) if transverse else ((1, 1), (1, 1))
        assert ranks == expected
        counts[transverse] += 1
    assert counts == {False: (prime+1)**2, True: prime*(prime*prime-1)}
    assert sum(counts.values()) == (prime+1)*(prime*prime+1)


@pytest.mark.parametrize("p", [7, 11, 19])
@pytest.mark.parametrize("parameters", [(1, 0, 2), (3, 2, 2), (6, 3, 4)])
def test_integral_transverse_corners_generate_full_order(p, parameters):
    order, phi = gaussian_fixture(p, *parameters)
    ell = sum(x*x for x in parameters)
    unit = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, matrix_star(order, phi), phi) == ell*unit
    assert matrix_multiply(order, phi, matrix_star(order, phi)) == ell*unit
    assert abs(int(Matrix.hstack(*transport_generators(order, phi)).det())) == ell**16
    completed = complete_by_corners(order, phi)
    assert completed == eye(16)
    gram = reference_gram(order)
    assert gram.det() == p**8
    assert (completed.T*gram*completed).det() == p**8


@pytest.mark.parametrize("p", [7, 11, 19])
def test_split_dual_kernel_does_not_get_saturated_by_corners(p):
    order, a = odd_maximal_order(p), Matrix([6, 5, 0, 0])
    phi = Matrix.vstack(a, zeros(4, 1), zeros(4, 1), order.star(a))
    completed = complete_by_corners(order, phi)
    assert abs(int(completed.det())) == 61**16
    assert (completed.T*reference_gram(order)*completed).det() == p**8*61**32


def test_uniform_transport_cannot_simulate_a_path_independent_oneend_oracle():
    alpha = Matrix([[0, -1], [1, 0]])
    for t in (1, 2, 7):
        path = Matrix([[1, t], [0, 1]])
        forward = path*alpha*path.inv()
        returned = path.inv()*forward*path
        assert returned == alpha
    # This is an exact cancellation control, not an isogeny-walk simulation.


@pytest.mark.parametrize("p", [7, 11, 19])
def test_one_known_mixing_involution_completes_the_order(p):
    order, phi = gaussian_fixture(p)
    gamma = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), -order.unit)
    assert complete_with_known_map(order, phi, gamma) == eye(16)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert abs(int(complete_with_known_map(order, phi, identity).det())) == 61**16


@pytest.mark.parametrize("prime", [3, 5, 7, 13])
def test_small_torsion_interface_cancels_common_weak_mask(prime):
    order, phi = gaussian_fixture(11)
    actions = product_actions(odd_maximal_split(11, prime))
    phi_matrix = action(phi, actions)
    actual = transport_generators(order, phi)
    for mask in (1, prime-1):
        images = weak_corner_actions(actions, mask*phi_matrix, 61, prime)
        for index, f in enumerate(actual):
            f_matrix = action(f, actions)
            for row in range(2):
                for col in range(2):
                    expected = zeros(4)
                    expected[2*row:2*row+2, 2*col:2*col+2] = f_matrix[2*row:2*row+2, 2*col:2*col+2]
                    assert images[4*index+2*row+col] == mod(expected, prime)


def test_source_word_algebra_cannot_manufacture_a_mixing_map():
    order, phi = gaussian_fixture(11)
    transported = transport_generators(order, phi)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    gamma = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), -order.unit)
    span = Matrix.hstack(identity, *transported)
    assert rank_mod(span, 61) == 5
    assert rank_mod(span.row_join(gamma), 61) == 6
    for i, j in ((0, 7), (5, 8), (6, 13), (12, 3)):
        source_product = matrix_multiply(order, eye(16)[:, i], eye(16)[:, j])
        expected = Matrix.hstack(*transported)*source_product
        assert matrix_multiply(order, transported[i], transported[j]) == 61*expected


def test_invalid_transport_is_not_promoted():
    with pytest.raises(ValueError, match="rank-two"):
        corner_ranks(eye(4), 3)
    with pytest.raises(ValueError, match="isotropic"):
        corner_ranks(Matrix.diag(1, 1, 0, 0), 3)
    order, phi = gaussian_fixture(11)
    with pytest.raises(ValueError, match="nonintegral"):
        complete_with_known_map(order, phi, eye(16)[:, 0]/2)
