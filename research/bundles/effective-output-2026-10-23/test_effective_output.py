import pytest
from sympy import Matrix, eye, zeros

from effective_output import (column_star, left_hermitian_gram, left_order_actions,
                              pullback_matrix, scalar_base_change, source_inclusion)
from kernel_output import matrix_multiply, odd_maximal_order, odd_maximal_split, reconstruct
from twist_control import twist_control


@pytest.mark.parametrize("p,ell", [(7, 3), (11, 5), (19, 7)])
def test_contravariant_multiplication_and_full_left_action(p, ell):
    order = odd_maximal_order(p)
    k = Matrix([[1, 0], [1, 2], [0, 1], [2, 3]])
    output = reconstruct(order, odd_maximal_split(p, ell), k, ell)
    basis = output.order_basis
    actions = left_order_actions(order, output)
    maps = [pullback_matrix(order, output, basis[:, i]) for i in range(basis.cols)]
    assert all(t*a == a*t for t in maps for a in actions)
    witnessed_noncommutativity = False
    for i, j in [(0, 1), (1, 2), (3, 7), (4, 12), (5, 10)]:
        product = matrix_multiply(order, basis[:, i], basis[:, j])
        assert pullback_matrix(order, output, product) == maps[j]*maps[i]
        witnessed_noncommutativity |= maps[j]*maps[i] != maps[i]*maps[j]
    assert witnessed_noncommutativity
    for i in range(4):
        for j in range(4):
            product = order.multiply(eye(4)[:, i], eye(4)[:, j])
            expected = sum((product[k]*actions[k] for k in range(4)), zeros(8))
            assert actions[i]*actions[j] == expected


@pytest.mark.parametrize("p,ell", [(7, 3), (11, 5), (19, 7)])
def test_inclusion_and_polarization_multiplier(p, ell):
    order = odd_maximal_order(p)
    output = reconstruct(order, odd_maximal_split(p, ell), Matrix([[1, 0], [0, 0], [0, 1], [0, 0]]), ell)
    inclusion = source_inclusion(order, output)
    gram = left_hermitian_gram(order, output)
    assert abs(int(inclusion.det())) == ell**4
    for i in range(8):
        for j in range(8):
            value = zeros(4, 1)
            for k in range(2):
                value += order.multiply(inclusion[4*k:4*k+4, i], order.star(inclusion[4*k:4*k+4, j]))
            assert value == ell*gram[i][j]
            assert all(v.q == 1 for v in gram[i][j])


@pytest.mark.parametrize("p", [7, 11, 19])
def test_actual_twists_need_quadratic_extension(p):
    assert all(twist_control(p)["checks"].values())


@pytest.mark.parametrize("p,f", [(5, 2), (7, 4), (11, 6), (19, 8)])
@pytest.mark.parametrize("sign", [-1, 1])
def test_same_paid_quadratic_extension_normalizes_both_signs(p, f, sign):
    result = scalar_base_change(p, f, sign*p**(f//2))
    assert result["relative_extension_degree"] == 2
    assert result["normalized_frobenius"] == result["reference_frobenius_after_base_change"]
    assert not result["geometric_field_promise_verified"]


@pytest.mark.parametrize("p,f,c", [(3, 2, -3), (7, 1, 7), (7, 2, 6), (9, 2, 9)])
def test_field_contract_rejects_invalid_consequences(p, f, c):
    with pytest.raises(ValueError):
        scalar_base_change(p, f, c)


def test_nonintegral_target_map_is_not_promoted():
    order = odd_maximal_order(11)
    output = reconstruct(order, odd_maximal_split(11, 3), Matrix([[1, 0], [0, 0], [0, 1], [0, 0]]), 3)
    with pytest.raises(ValueError, match="target-order"):
        pullback_matrix(order, output, output.order_basis[:, 0]/2)
