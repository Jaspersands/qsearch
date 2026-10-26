"""Exact matrix countercontrols, not executions of the quantum algorithms."""

import itertools
import math
import random

import pytest

from theorems.symplectic_socle_probes import (
    add, coefficient_verification_pairs, eye, graph_polynomial, lift_symplectic_matrix,
    lower_socle, multiply, query_matrix, recover_symmetric_matrix, scale,
    symplectic_form, transpose,
)


def symmetric(n, entries):
    result = [[0] * n for _ in range(n)]
    for (i, j), value in zip(itertools.combinations_with_replacement(range(n), 2), entries):
        result[i][j] = result[j][i] = value
    return tuple(map(tuple, result))


def inverse(a, modulus):
    n = len(a)
    rows = [list(row) + list(unit) for row, unit in zip(a, eye(n))]
    for c in range(n):
        pivot = next(r for r in range(c, n) if math.gcd(rows[r][c], modulus) == 1)
        rows[c], rows[pivot] = rows[pivot], rows[c]
        factor = pow(rows[c][c], -1, modulus)
        rows[c] = [x * factor % modulus for x in rows[c]]
        for r in range(n):
            if r != c:
                factor = rows[r][c]
                rows[r] = [(x - factor * y) % modulus for x, y in zip(rows[r], rows[c])]
    return tuple(tuple(row[n:]) for row in rows)


def graph_image(g, s, p):
    """Canonicalize the image of [I;pS] by independent ring elimination."""
    n = len(s)
    basis = eye(n) + scale(s, p, p * p)
    image = multiply(g, basis, p * p)
    normalized_bottom = multiply(image[n:], inverse(image[:n], p * p), p * p)
    assert all(x % p == 0 for row in normalized_bottom for x in row)
    return tuple(tuple(x // p for x in row) for row in normalized_bottom)


def rank(vectors, p):
    rows = [list(row) for row in vectors]
    pivots = 0
    for c in range(len(rows[0]) if rows else 0):
        candidates = [r for r in range(pivots, len(rows)) if rows[r][c] % p]
        if not candidates:
            continue
        r = candidates[0]
        rows[pivots], rows[r] = rows[r], rows[pivots]
        factor = pow(rows[pivots][c] % p, -1, p)
        rows[pivots] = [x * factor % p for x in rows[pivots]]
        for r in range(len(rows)):
            if r != pivots:
                factor = rows[r][c] % p
                rows[r] = [(x - factor * y) % p for x, y in zip(rows[r], rows[pivots])]
        pivots += 1
    return pivots


@pytest.mark.parametrize('p', [3, 5, 7, 2**127 - 1])
def test_public_queries_and_symplectic_lifts(p):
    rng = random.Random(131)
    n = 3
    j = symplectic_form(n)
    modulus = p * p
    for _ in range(12):
        s = symmetric(n, [rng.randrange(p) for _ in range(6)])
        x = symmetric(n, [rng.randrange(p) for _ in range(6)])
        i, k = rng.sample(range(n), 2)
        t = rng.randrange(p)
        g = query_matrix(x, t, i, k, p)
        assert multiply(multiply(transpose(g), j, modulus), g, modulus) == scale(j, 1, modulus)
        b, c = graph_polynomial(s, i, k, p)
        predicted = add(add(x, s, p), add(scale(b, t, p), scale(c, t * t, p), p), p)
        assert graph_image(g, s, p) == predicted
        # Deliberately perturb every lifted entry without changing its residue.
        perturbed = tuple(tuple((value + p * rng.randrange(p)) % modulus for value in row)
                          for row in g)
        repaired = lift_symplectic_matrix(perturbed, p)
        assert scale(repaired, 1, p) == scale(g, 1, p)
        assert multiply(multiply(transpose(repaired), j, modulus), repaired, modulus) == scale(j, 1, modulus)


@pytest.mark.parametrize('p', [3, 5])
@pytest.mark.parametrize('secret', [(0, 0, 0), (1, 0, 2), (1, 2, 1)])
def test_every_query_fiber_is_a_complete_polynomial_graph(p, secret):
    n = 2
    s = symmetric(n, [v % p for v in secret])
    b, c = graph_polynomial(s, 0, 1, p)
    fibers = {}
    # The actual matrix images, not the claimed graph polynomial, define labels.
    for entries in itertools.product(range(p), repeat=3):
        x = symmetric(n, entries)
        for t in range(p):
            actual = graph_image(query_matrix(x, t, 0, 1, p), s, p)
            fibers.setdefault(actual, []).append((x, t))
    assert len(fibers) == p**3
    for actual, entries in fibers.items():
        assert len(entries) == p
        assert {t for _, t in entries} == set(range(p))
        offset = add(actual, scale(s, -1, p), p)
        for x, t in entries:
            poly = add(scale(b, t, p), scale(c, t * t, p), p)
            assert x == add(offset, scale(poly, -1, p), p)
    # Replacing these canonical labels by any injective opaque relabeling
    # leaves exactly these fibers. The tests do not assert classical hardness.


@pytest.mark.parametrize('p', [3, 5, 11, 2**127 - 1])
def test_all_columns_recovered_from_correct_linear_coefficients(p):
    rng = random.Random(193)
    for n in (2, 3, 5):
        for _ in range(9):
            s = symmetric(n, [rng.randrange(p) for _ in range(n * (n + 1) // 2)])
            coefficients = [graph_polynomial(s, i, (i + 1) % n, p)[0] for i in range(n)]
            assert recover_symmetric_matrix(coefficients, p) == s


def test_ring_representatives_are_not_a_homomorphism():
    p = 5
    zero = symmetric(2, (0, 0, 0))
    actual_product = multiply(query_matrix(zero, 4, 0, 1, p),
                              query_matrix(zero, 4, 0, 1, p), p * p)
    reduced_representative = query_matrix(zero, 3, 0, 1, p)
    assert actual_product != reduced_representative
    for entries in itertools.product(range(p), repeat=3):
        s = symmetric(2, entries)
        assert graph_image(actual_product, s, p) == graph_image(reduced_representative, s, p)


@pytest.mark.parametrize('p', [3, 5, 2**127 - 1])
def test_two_query_pairs_certify_coefficients_and_one_pair_does_not(p):
    s = ((1, 2), (2, 1))
    b, c = graph_polynomial(s, 0, 1, p)
    pairs = coefficient_verification_pairs(b, c, 0, 1, p)
    assert all(graph_image(left, s, p) == graph_image(right, s, p) for left, right in pairs)
    # Perturb B by D and C by -D: the t=1 test cannot see the error.
    d = ((1, 0), (0, 0))
    wrong = coefficient_verification_pairs(add(b, d, p), add(c, scale(d, -1, p), p),
                                           0, 1, p)
    assert graph_image(wrong[0][0], s, p) == graph_image(wrong[0][1], s, p)
    assert graph_image(wrong[1][0], s, p) != graph_image(wrong[1][1], s, p)


@pytest.mark.parametrize('p', [3, 5])
def test_socle_pairing_annihilator_recovers_reduction_not_lift(p):
    n = 2
    j = symplectic_form(n)
    sym = [symmetric(n, (int(k == r) for k in range(3))) for r in range(3)]
    zero = ((0, 0), (0, 0))

    def block(a, b, c):
        return tuple(tuple(a[r][k] if r < n and k < n else
                           b[r][k - n] if r < n else
                           c[r - n][k] if k < n else -a[k - n][r - n]
                           for k in range(2 * n)) for r in range(2 * n))

    a_basis = [tuple(tuple(int(r == i and c == k) for c in range(n)) for r in range(n))
               for i in range(n) for k in range(n)]
    parabolic = [block(a, zero, zero) for a in a_basis] + [block(zero, b, zero) for b in sym]
    radical = [block(zero, b, zero) for b in sym]
    full = parabolic + [block(zero, zero, c) for c in sym]
    # Move to a nonstandard Lagrangian by a genuine symplectic basis change.
    shift = symmetric(n, (1, 1, 2))
    change = tuple(tuple(int(r == c) + (shift[r - n][c]
                         if r >= n and c < n else 0)
                         for c in range(2 * n)) for r in range(2 * n))
    change_inverse = inverse(change, p)

    def conjugate(x):
        return multiply(multiply(change, x, p), change_inverse, p)

    parabolic, radical, full = [list(map(conjugate, basis)) for basis in (parabolic, radical, full)]

    def pairing(x, y):
        product = multiply(x, y, p)
        return sum(product[i][i] for i in range(2 * n)) % p

    assert rank([[pairing(x, y) for y in full] for x in full], p) == 10
    assert rank([[pairing(x, y) for y in full] for x in parabolic], p) == 7
    assert all(pairing(x, y) == 0 for x in parabolic for y in radical)
    image_columns = [col for x in radical for col in transpose(x)]
    w_columns = transpose(tuple(row[:n] for row in change))
    assert rank(image_columns, p) == n
    assert rank(image_columns + list(w_columns), p) == n
    assert all(add(multiply(transpose(x), j, p), multiply(j, x, p), p)
               == scale(eye(2 * n), 0, p) for x in full)
    # Standard socle parabolic has identical membership for every lift S.
    x = block(eye(n), sym[0], zero)
    g = add(eye(2 * n), scale(x, p, p * p), p * p)
    for entries in itertools.product(range(p), repeat=3):
        s = symmetric(2, entries)
        assert graph_image(g, s, p) == s


def test_rank_one_prime_three_really_has_nonunique_lagrangians():
    # SL_2(Z/9) stabilizers of <(1,0)> and <(1,3)> coincide.
    stabilizers = [set(), set()]
    for a, b, c, d in itertools.product(range(9), repeat=4):
        if (a * d - b * c) % 9 != 1:
            continue
        for idx, slope in enumerate((0, 3)):
            if (c + d * slope - slope * (a + b * slope)) % 9 == 0:
                stabilizers[idx].add((a, b, c, d))
    assert stabilizers[0] == stabilizers[1]
    assert stabilizers[0]


def test_unguarded_field_lie_query_is_not_valid():
    x = ((1, 0), (0, -1))
    naive = add(eye(2), x, 5)
    j = symplectic_form(1)
    assert multiply(multiply(transpose(naive), j, 5), naive, 5) != scale(j, 1, 5)


def test_scope_and_bad_answer_guards():
    for p, s in [(2, ((1, 0), (0, 1))), (5, ((1,),))]:
        with pytest.raises(ValueError):
            query_matrix(s, 1, 0, 1, p)
    with pytest.raises(ValueError):
        query_matrix(((0, 1), (0, 0)), 1, 0, 1, 5)
    with pytest.raises(ValueError):
        lift_symplectic_matrix(scale(eye(4), 0, 25), 5)
    s = ((1, 2), (2, 3))
    coefficients = [graph_polynomial(s, i, 1 - i, 5)[0] for i in range(2)]
    corrupted = [list(row) for row in coefficients[0]]
    corrupted[0][0] = 1  # This entry must vanish for E_01.
    coefficients[0] = tuple(map(tuple, corrupted))
    with pytest.raises(ValueError):
        recover_symmetric_matrix(coefficients, 5)
