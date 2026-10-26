"""Exact controls for application reductions, not classical complexity proofs."""

from collections import deque
from fractions import Fraction

from flint import fmpz_mod_ctx, fmpz_mod_mat
import numpy as np
import pytest
from sympy.combinatorics.named_groups import DihedralGroup

from self_dual_rowspace_hsp_reduction import (
    canonical_rowspace,
    compose_permutations,
    inverse_permutation,
    rowspace_hiding_value,
)


def _large_hull_code():
    matrix = np.zeros((3, 8), dtype=np.uint8)
    for i in range(3):
        matrix[i, i] = matrix[i, i + 4] = 1
    return matrix


def _dihedral_elements():
    return [
        tuple(element.array_form)
        for element in DihedralGroup(8).generate_schreier_sims()
    ]


def _left_orbit_label(matrix, permutation):
    return rowspace_hiding_value(matrix, inverse_permutation(permutation))


def test_ambient_group_really_has_nilpotency_class_three():
    group = DihedralGroup(8)
    assert group.is_solvable
    assert [subgroup.order() for subgroup in group.lower_central_series()] == [
        16, 4, 2, 1
    ]


def test_nontrivial_hull_orbit_fibres_are_exactly_stabilizer_cosets():
    matrix = _large_hull_code()
    assert canonical_rowspace(matrix).shape[0] == 3
    assert not np.any((matrix @ matrix.T) & 1)  # C is its own hull.
    elements = _dihedral_elements()
    identity = tuple(range(8))
    base = _left_orbit_label(matrix, identity)
    labels = {g: _left_orbit_label(matrix, g) for g in elements}
    stabilizer = {g for g in elements if labels[g] == base}
    assert len(stabilizer) == 4
    assert len(set(labels.values())) == 4

    for g in elements:
        for other in elements:
            difference = compose_permutations(inverse_permutation(other), g)
            assert (labels[g] == labels[other]) == (difference in stabilizer)
        for h in stabilizer:
            assert labels[compose_permutations(g, h)] == labels[g]


def test_permutation_matrix_subspace_stabilizer_and_row_gauge_agree():
    matrix = _large_hull_code()
    row_change = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]], dtype=np.uint8)
    changed = (row_change @ matrix) & 1
    base = canonical_rowspace(matrix)
    for g in _dihedral_elements():
        permutation_matrix = np.eye(8, dtype=np.uint8)[:, g]
        matrix_stabilizes = np.array_equal(
            canonical_rowspace(matrix @ permutation_matrix), base
        )
        left_stabilizes = _left_orbit_label(matrix, g) == _left_orbit_label(
            matrix, tuple(range(8))
        )
        assert matrix_stabilizes == left_stabilizes
        assert _left_orbit_label(changed, g) == _left_orbit_label(matrix, g)


def _wreath_product(x, y, p):
    a, b, swap = x
    c, d, other_swap = y
    if swap:
        c, d = d, c
    return ((a + c) % p, (b + d) % p, swap ^ other_swap)


def _wreath_inverse(x, p):
    a, b, swap = x
    if swap:
        a, b = b, a
    return (-a % p, -b % p, swap)


def _commutator(x, y, p):
    value = _wreath_product(_wreath_inverse(x, p), _wreath_inverse(y, p), p)
    return _wreath_product(_wreath_product(value, x, p), y, p)


@pytest.mark.parametrize("p", [3, 5, 7, 11])
def test_odd_prime_swap_wreath_leaves_nilpotent_ambient(p):
    r, t, identity = (1, p - 1, 0), (0, 0, 1), (0, 0, 0)
    assert _wreath_product(_wreath_product(t, r, p), t, p) == _wreath_inverse(r, p)
    value = r
    for depth in range(1, 9):
        value = _commutator(value, t, p)
        exponent = pow(-2, depth, p)
        assert value == (exponent, -exponent % p, 0)
        assert value != identity
    # This finite identity is a control; the universal nonvanishing proof
    # uses that -2 is invertible modulo every odd prime.


def test_binary_swap_wreath_is_a_class_two_exception():
    p = 2
    elements = [(a, b, s) for a in range(p) for b in range(p) for s in range(2)]
    commutators = {_commutator(x, y, p) for x in elements for y in elements}
    assert commutators == {(0, 0, 0), (1, 1, 0)}
    assert all(
        _commutator(c, g, p) == (0, 0, 0)
        for c in commutators
        for g in elements
    )


def _cyclic_shift(v, amount):
    return tuple(v[(i-amount) % len(v)] for i in range(len(v)))


def _p_wreath_product(x, y, p):
    v, a = x
    w, b = y
    return (tuple((r+s) % p for r, s in zip(v, _cyclic_shift(w, a))), (a+b) % p)


def _p_wreath_power(x, exponent, p):
    value = ((0,)*p, 0)
    for _ in range(exponent):
        value = _p_wreath_product(value, x, p)
    return value


@pytest.mark.parametrize("p", [2, 3, 5, 7, 11])
def test_regular_characteristic_p_wreath_has_class_p_and_exponent_p_squared(p):
    basis = [tuple(int(i == j) for j in range(p)) for i in range(p)]
    rows, ranks = basis, []
    for _ in range(p):
        # J=P-I generates the commutator ideal. Subsequent commutators
        # multiply by J (up to an invertible shift and sign).
        rows = [tuple((a-b) % p for a, b in zip(_cyclic_shift(v, 1), v)) for v in rows]
        ranks.append(fmpz_mod_mat(rows, fmpz_mod_ctx(p)).rref()[1])
        if len(ranks) == p-1:
            assert rows[0] == (1,)*p
    assert ranks == list(range(p-1, -1, -1))
    assert rows == [(0,)*p]*p
    element = (basis[0], 1)
    assert _p_wreath_power(element, p, p) == ((1,)*p, 0)
    assert _p_wreath_power(element, p*p, p) == ((0,)*p, 0)
    # A group commutator agrees with (P^-1-I)v for the chosen convention.
    v, t = (basis[0], 0), ((0,)*p, 1)
    comm = _p_wreath_product(_p_wreath_power(v, p-1, p),
                             _p_wreath_power(t, p-1, p), p)
    comm = _p_wreath_product(_p_wreath_product(comm, v, p), t, p)
    assert comm == (tuple((a-b) % p for a, b in zip(_cyclic_shift(basis[0], -1), basis[0])), 0)


def test_target_transporter_preparation_is_paid_and_not_a_subgroup_source():
    matrix = _large_hull_code()
    elements = _dihedral_elements()
    identity = tuple(range(8))
    labels = {g: _left_orbit_label(matrix, g) for g in elements}
    orbit = set(labels.values())
    base = labels[identity]
    target = next(label for label in labels.values() if label != base)
    stabilizer = {g for g in elements if labels[g] == base}
    transporter = {g for g in elements if labels[g] == target}
    t = next(iter(transporter))
    assert transporter == {compose_permutations(t, h) for h in stabilizer}
    assert identity not in transporter
    assert Fraction(len(transporter), len(elements)) == Fraction(1, len(orbit)) == Fraction(1, 4)

    # This is the explicit polynomial-orbit alternative, using only the
    # supplied generators/action and storing one witness per seen label.
    generators = [tuple(g.array_form) for g in DihedralGroup(8).generators]
    witnesses, queue, calls = {base: identity}, deque([identity]), 0
    while queue:
        word = queue.popleft()
        for generator in generators:
            other = compose_permutations(generator, word)
            label = _left_orbit_label(matrix, other)
            calls += 1
            if label not in witnesses:
                witnesses[label] = other
                queue.append(other)
    assert set(witnesses) == orbit
    assert witnesses[target] in transporter
    assert calls == len(orbit)*len(generators)
