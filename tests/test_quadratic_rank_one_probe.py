"""Exact identities for source triage; no hidden-oracle search is run."""

from itertools import product

import pytest


def mm(a, b, p):
    return [[sum(x*y for x, y in zip(row, col)) % p for col in zip(*b)] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def update(w, p):
    matrix = eye(len(w))
    matrix[0] = [(int(j == 0) + value) % p for j, value in enumerate(w)]
    return matrix


def isometry(a, g, p):
    return mm(mm(transpose(g), a, p), g, p) == a


def coordinates(a, b, p):
    u = min(a, (-a) % p)
    inverse = pow(u, -1, p)
    return u, a * inverse % p, tuple(x * inverse % p for x in b)


def coset_equal(g, h, s, p):
    a, b = g
    c, d = h
    return g == h or (c == -a % p and d == tuple((x + 2*a*t) % p for x, t in zip(b, s)))


@pytest.mark.parametrize("p", [3, 5, 7])
@pytest.mark.parametrize("dimension", [2, 3])
def test_symmetric_probe_hides_only_the_unknown_reflection(p, dimension):
    alpha = 2 % p
    c = [(i + 1) % p for i in range(dimension - 1)]
    inverse = pow(alpha, -1, p)
    # Schur complement I guarantees nonsingularity without revealing A
    # to any algorithm; these are just exact identity fixtures.
    a = [[alpha] + c]
    a += [[c[i]] + [(int(i == j) + c[i]*c[j]*inverse) % p
                    for j in range(dimension - 1)] for i in range(dimension - 1)]
    found = []
    for w in product(range(p), repeat=dimension):
        if (1 + w[0]) % p and isometry(a, update(w, p), p):
            found.append(w)
    reflection = ((-2) % p,) + tuple((-2*x*inverse) % p for x in c)
    assert set(found) == {(0,) * dimension, reflection}
    r = update(reflection, p)
    assert mm(r, r, p) == eye(dimension)
    assert r != eye(dimension)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_alternating_probe_is_an_abelian_line_not_a_reflection(p):
    b = [[0, 1, 0, 0], [-1 % p, 0, 0, 0],
         [0, 0, 0, 1], [0, 0, -1 % p, 0]]
    found = set()
    for w in product(range(p), repeat=4):
        if (1 + w[0]) % p and isometry(b, update(w, p), p):
            found.add(w)
    assert found == {(0, t, 0, 0) for t in range(p)}


@pytest.mark.parametrize("p", [3, 5, 7, 11])
def test_affine_coset_coordinates_preserve_all_pairs(p):
    elements = [(a, (b,)) for a in range(1, p) for b in range(p)]
    s = (2 % p,)
    for g in elements:
        ug, eg, yg = coordinates(*g, p)
        assert eg in (1, p - 1)
        for h in elements:
            uh, eh, yh = coordinates(*h, p)
            mapped_equal = ug == uh and coset_equal((eg, yg), (eh, yh), s, p)
            assert mapped_equal == coset_equal(g, h, s, p)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_vector_translation_and_lower_central_obstruction(p):
    s = (1, 2 % p)
    for a in range(1, p):
        for b in product(range(p), repeat=2):
            h = (-a % p, tuple((x + 2*a*t) % p for x, t in zip(b, s)))
            u, e, y = coordinates(a, b, p)
            u2, e2, y2 = coordinates(*h, p)
            assert u == u2
            assert coset_equal((e, y), (e2, y2), s, p)
    # [reflection,translation(v)] translates by -2v; this map is onto
    # in odd characteristic, so the lower central series cannot terminate.
    assert {(-2*x) % p for x in range(p)} == set(range(p))
