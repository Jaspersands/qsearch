"""Regression against mistaking forced copy symmetries for native escape."""

from itertools import permutations, product

import pytest
from sympy import Matrix, Rational, eye, symbols

from inherited_symmetries import (
    adjoint, category_contains, control, graph_intertwining,
    interpolation_diamond, product_action, quaternion_copy_group, supplied_pullbacks,
)
from interpolation_closure import terminal_generators


def test_quaternion_group_and_universal_commutation():
    a, b, c, d = symbols("a b c d")
    four_square = Matrix([[a, -b, -c, -d], [b, a, d, -c],
                          [c, -d, a, b], [d, c, -b, a]])
    group = quaternion_copy_group()
    keys = {tuple(x) for x in group}
    assert len(keys) == 8
    assert group[2]**2 == group[4]**2 == -eye(4)
    assert group[2]*group[4] == -group[4]*group[2]
    for x in group:
        assert x.T*x == eye(4)
        assert x*four_square == four_square*x
        assert all(tuple(x*y) in keys for y in group)


def test_entire_universal_integral_orthogonal_centralizer_has_eight_elements():
    # Every integral orthogonal matrix is a signed permutation, so this
    # exhausts the four-dimensional universal group, not a geometric group.
    a, b, c = (Matrix([[0, -b, -c, -d], [b, 0, d, -c],
                      [c, -d, 0, b], [d, c, -b, 0]])
               for b, c, d in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    commuting = set()
    for perm in permutations(range(4)):
        for signs in product((-1, 1), repeat=4):
            x = Matrix(4, 4, lambda i, j: signs[i]*int(perm[i] == j))
            if all(x*y == y*x for y in (a, b, c)):
                commuting.add(tuple(x))
    assert commuting == {tuple(x) for x in quaternion_copy_group()}


@pytest.mark.parametrize("q,roots,divisor", [
    (3, (1, 2, 1, 1), 2), (3, (1, 2, 1, 1), 5),
    (5, (1, 2, 1, 1), 4), (17, (1, 2, 1, 1), 6),
    (17, (1, 2, 1, 1), 24), (2**61-1, (1, 0, 0, 0), 2**40),
])
def test_partial_graph_invariance_and_zero_escape(q, roots, divisor):
    graph_intertwining(q, roots)
    for x in supplied_pullbacks(q, roots, divisor):
        assert adjoint(x)*x == divisor**2*eye(16)
        assert category_contains(x, q, 4)
        assert not any(x[:8, 8:]) and not any(x[8:, :8])
    result = control(q, roots, divisor)
    assert result["forced_group_order"] == 8
    assert result["all_supplied_pullbacks_in_known_category"]
    assert not result["native_partial_quotient_computed"]
    assert not result["geometric_automorphism_list_computed"]
    assert not result["useful_native_map_found"]


def test_special_four_square_witness_has_more_than_universal_symmetries():
    # A4=I4 commutes with all signed permutations, not just Q8.
    swap = eye(4)
    swap.row_swap(0, 1)
    assert tuple(swap) not in {tuple(x) for x in quaternion_copy_group()}
    psi, _ = interpolation_diamond(5, (1, 0, 0, 0))
    u = product_action(swap)
    assert u*psi == psi*u
    assert category_contains(u, 5, 4)


def test_terminal_extra_automorphism_still_does_not_escape():
    psi, multiplier = interpolation_diamond(5, (1, 2, 1, 1))
    target_swap = terminal_generators()[-1]
    pulled = adjoint(psi)*target_swap*psi
    assert all(pulled != multiplier*product_action(b) for b in quaternion_copy_group())
    assert category_contains(pulled, 5, 4)


def test_two_torsion_alias_is_not_a_faithful_automorphism_list():
    group = quaternion_copy_group()
    assert group[0] != group[1]
    assert all(int(x) % 2 == 0 for x in group[0]-group[1])


def test_invalid_divisor_and_nonintegral_actions_are_rejected():
    with pytest.raises(ValueError, match="divisor"):
        supplied_pullbacks(5, (1, 2, 1, 1), 5)
    with pytest.raises(ValueError, match="integral"):
        product_action(Rational(1, 2)*eye(4))
