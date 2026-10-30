"""Independent exhaustive finite geometry; no quantum-state simulation."""
from itertools import combinations, product

import pytest

from theorems.coisotropic_symmetry import maximal_isotropic_subspace


def pairing(u, v, p):
    n = len(u)//2
    return (sum(u[n+i]*v[i] for i in range(n))
            - sum(u[i]*v[n+i] for i in range(n))) % p


def span(rows, p, width):
    return frozenset(
        tuple(sum(c*row[j] for c, row in zip(coefficients, rows)) % p
              for j in range(width))
        for coefficients in product(range(p), repeat=len(rows))
    )


def all_subspaces(p, width):
    """Enumerate unique RREF bases independently of the production reducer."""
    for dimension in range(width+1):
        for pivots in combinations(range(width), dimension):
            slots = [(i, j) for i, pivot in enumerate(pivots)
                     for j in range(pivot+1, width) if j not in pivots]
            for values in product(range(p), repeat=len(slots)):
                rows = [[int(j == pivot) for j in range(width)] for pivot in pivots]
                for (i, j), value in zip(slots, values):
                    rows[i][j] = value
                yield tuple(map(tuple, rows))


def check_decomposition(p, n, rows):
    result = maximal_isotropic_subspace(p, n, rows)
    ambient = span(rows, p, 2*n)
    isotropic = result.isotropic_basis
    isotropic_span = span(isotropic, p, 2*n)
    radical = frozenset(v for v in ambient
                        if all(pairing(v, w, p) == 0 for w in rows))
    assert result.prime == p and result.n == n
    assert span(result.span_basis, p, 2*n) == ambient
    assert len(ambient) == p**result.span_dimension
    assert span(result.radical_basis, p, 2*n) == radical
    assert len(radical) == p**result.radical_dimension
    assert result.span_dimension == result.radical_dimension + 2*result.pair_count
    assert len(isotropic) == result.isotropic_dimension <= n
    assert len(isotropic_span) == p**len(isotropic)
    assert isotropic_span <= ambient
    assert all(pairing(a, b, p) == 0 for a in isotropic for b in isotropic)
    # No vector of the input span can enlarge the returned commuting space.
    assert frozenset(v for v in ambient
                     if all(pairing(v, w, p) == 0 for w in isotropic)) == isotropic_span
    decomposition = result.radical_basis + tuple(
        v for pair in result.symplectic_pairs for v in pair)
    assert span(decomposition, p, 2*n) == ambient
    assert len(decomposition) == result.span_dimension
    for i, (a, b) in enumerate(result.symplectic_pairs):
        assert pairing(a, b, p) == 1
        for c, d in result.symplectic_pairs[i+1:]:
            assert all(pairing(u, v, p) == 0 for u in (a, b) for v in (c, d))
    assert all(type(x) is int and 0 <= x < p for row in decomposition for x in row)
    if result.isotropic_dimension == n:
        assert result.n_generators == isotropic[:n]
        assert len(span(result.n_generators, p, 2*n)) == p**n
    else:
        assert result.n_generators is None
    return result


@pytest.mark.parametrize("n,expected_count", [(1, 6), (2, 212)])
def test_exhaustive_ternary_subspaces(n, expected_count):
    bases = list(all_subspaces(3, 2*n))
    assert len(bases) == expected_count
    spaces = [span(rows, 3, 2*n) for rows in bases]
    assert len(set(spaces)) == expected_count
    isotropic_spaces = [(len(rows), space) for rows, space in zip(bases, spaces)
                        if all(pairing(a, b, 3) == 0 for a in rows for b in rows)]
    for rows, space in zip(bases, spaces):
        result = check_decomposition(3, n, rows)
        # Independent maximum over every isotropic subspace, not just the formula.
        assert result.isotropic_dimension == max(
            dimension for dimension, candidate in isotropic_spaces if candidate <= space)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_full_noncommuting_symmetry_space(p):
    rows = [[int(i == j) for j in range(4)] for i in range(4)]
    result = check_decomposition(p, 2, rows)
    assert result.span_dimension == 4
    assert result.radical_dimension == 0
    assert result.pair_count == 2
    assert result.n_generators is not None


def test_noncommuting_coisotropic_space_with_radical():
    result = check_decomposition(3, 2, [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)])
    assert (result.span_dimension, result.radical_dimension, result.pair_count) == (3, 1, 1)
    assert len(result.n_generators) == 2


@pytest.mark.parametrize("p", [5, 7])
def test_nonunit_pair_normalization(p):
    rows = [(1, 0, 0, 3), (0, 1, 1, 0)]
    assert pairing(*rows, p) == 2
    result = check_decomposition(p, 2, rows)
    assert result.pair_count == 1
    assert result.radical_dimension == 0


def test_large_prime_without_field_enumeration():
    p, n = 2**61-1, 4
    rows = [tuple(int(i == j) for j in range(2*n)) for i in range(2*n)]
    result = maximal_isotropic_subspace(p, n, rows)
    assert result.span_basis == tuple(rows)
    assert result.radical_dimension == 0
    assert result.pair_count == result.isotropic_dimension == n
    assert result.n_generators == tuple(rows[:n])
    for i, (a, b) in enumerate(result.symplectic_pairs):
        assert a == rows[i]
        assert b == tuple((p-1)*x for x in rows[n+i])
        assert pairing(a, b, p) == 1


def test_dimension_n_span_need_not_have_n_commuting_generators():
    result = check_decomposition(3, 2, [(1, 0, 0, 0), (0, 0, 1, 0)])
    assert result.span_dimension == 2
    assert result.isotropic_dimension == 1
    assert result.n_generators is None


def test_dependent_unsorted_rows_preserved_and_order_independent():
    rows = [[1, 2, 1, 0], [0, 1, 2, 1], [1, 0, 0, 1],
            [0, 0, 0, 0], [2, 1, 2, 0], [1, 2, 1, 0]]
    original = [row[:] for row in rows]
    # Enumerate only the reference span's independent rows to keep it small.
    expected = check_decomposition(3, 2, rows[:2])
    assert maximal_isotropic_subspace(3, 2, rows) == expected
    assert maximal_isotropic_subspace(3, 2, list(reversed(rows))) == expected
    assert rows == original


@pytest.mark.parametrize("n,rows", [(2, []), (2, [[0]*4]), (0, []), (0, [[], []])])
def test_empty_and_zero_spans(n, rows):
    result = check_decomposition(3, n, rows)
    assert result.span_dimension == result.radical_dimension == result.pair_count == 0
    assert result.n_generators == (() if n == 0 else None)


@pytest.mark.parametrize("p", [2, 4, 9, 15, 1, 0, -3, True, 3.0, "3"])
def test_prime_guard(p):
    with pytest.raises(ValueError):
        maximal_isotropic_subspace(p, 1, [(1, 0)])


@pytest.mark.parametrize("n", [-1, True, 1.0, "1"])
def test_invalid_qudit_count(n):
    with pytest.raises(ValueError):
        maximal_isotropic_subspace(3, n, [])


@pytest.mark.parametrize("rows", [
    [(1,)], [(1, 0, 0)], [(1, 0), (0,)], [(1, 3)], [(1, -1)],
    [(True, 0)], [(1.0, 0)], [("1", 0)], [(None, 0)],
])
def test_invalid_coordinates(rows):
    with pytest.raises(ValueError):
        maximal_isotropic_subspace(3, 1, rows)
