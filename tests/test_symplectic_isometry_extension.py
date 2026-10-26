"""Exact deterministic-extension controls, not an HSP or novelty certificate."""
from itertools import product

import pytest

from theorems.ut5_matrix_phase_alignment import (
    _identity, _product, _rank, _transpose, extend_symplectic_isometry,
    symplectic_pair,
)


def action(matrix, vector, p):
    return [sum(a*b for a, b in zip(row, vector)) % p for row in matrix]


def check_extension(p, source, target):
    S, count = extend_symplectic_isometry(p, source, target)
    n = len(S)
    omega = [[symplectic_pair(a, b, p) for b in _identity(n)] for a in _identity(n)]
    assert _product(_product(_transpose(S), omega, p), S, p) == omega
    assert [action(S, v, p) for v in source] == [list(v) for v in target]
    assert count <= 2*len(source)
    return S, count


def test_every_pair_of_nonzero_vectors_over_f3_has_a_checked_extension():
    vectors = [v for v in product(range(3), repeat=2) if any(v)]
    counts = set()
    for source in vectors:
        for target in vectors:
            _, count = check_extension(3, [source], [target])
            counts.add(count)
    assert counts == {0, 1, 2}


@pytest.mark.parametrize("p", [3, 5])
def test_all_two_dimensional_symplectic_bases_are_recovered_exactly(p):
    found = 0
    for a, b, c, d in product(range(p), repeat=4):
        if (a*d-b*c) % p != 1:
            continue
        target = [[a, c], [b, d]]
        S, _ = check_extension(p, _identity(2), target)
        assert S == ((a, b), (c, d))
        found += 1
    assert found == p*(p*p-1)


@pytest.mark.parametrize("p", [3, 7, 2**127-1])
def test_degenerate_subspace_gram_and_full_basis_need_no_random_completion(p):
    R = 4
    symmetric = [[(i+1)*(j+1) % p for j in range(R)] for i in range(R)]
    shear = [row+[0]*R for row in _identity(R)]
    shear += [row+unit for row, unit in zip(symmetric, _identity(R))]
    fourier = [[0]*R+[-x % p for x in row] for row in _identity(R)]
    fourier += [row+[0]*R for row in _identity(R)]
    reference = _product(fourier, shear, p)
    source = [_identity(2*R)[j] for j in (0, R, 1, 2)]
    gram = [[symplectic_pair(a, b, p) for b in source] for a in source]
    assert _rank(gram, p) == 2  # A nondegenerate pair plus a two-dimensional radical.
    target = [action(reference, v, p) for v in source]
    result = check_extension(p, source, target)
    assert result == extend_symplectic_isometry(p, source, target)
    full_source = _identity(2*R)
    full, _ = check_extension(p, full_source, [action(reference, v, p) for v in full_source])
    assert full == tuple(map(tuple, reference))


@pytest.mark.parametrize("source,target", [([], []), ([[1, 0]], []),
    ([[1, 0], [2, 0]], [[1, 0], [0, 1]]),
    ([[1, 0], [0, 1]], [[1, 0], [0, 2]]),
    ([[1, 0]], [[5, 0]]), ([[1, 0]], [[1]]), ([[1]], [[1]])])
def test_invalid_or_nonisometric_input_is_rejected(source, target):
    with pytest.raises(ValueError):
        extend_symplectic_isometry(5, source, target)


def test_characteristic_two_not_silently_admitted_to_odd_prime_contract():
    with pytest.raises(ValueError):
        extend_symplectic_isometry(2, [[1, 0]], [[0, 1]])
