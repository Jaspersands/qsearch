"""Finite falsifiers of proposed labels, not a toy HSP search benchmark."""
from itertools import product

import pytest


@pytest.mark.parametrize("p", [5, 7])
def test_singleton_orbit_requires_almost_one_bank_point_per_object(p):
    orbit = [x+(1,) for x in product(range(p), repeat=3)]
    assert len(orbit) == p**3
    for size in (0, 1, p**3-2, p**3-1):
        bank = orbit[:size]
        labels = {tuple(int(point == query) for query in bank) for point in orbit}
        assert len(labels) == min(size+1, p**3)
        assert (len(labels) == len(orbit)) == (size >= p**3-1)


def test_point_stabilizer_formula_with_full_ut4_control():
    p, w = 5, (2, 3, 1, 2)
    alpha, beta = w[1]*pow(w[3], -1, p) % p, w[2]*pow(w[3], -1, p) % p
    count, images = 0, set()
    for a, b, c, d, e, f in product(range(p), repeat=6):
        image = ((w[0]+a*w[1]+b*w[2]+c*w[3]) % p,
                 (w[1]+d*w[2]+e*w[3]) % p, (w[2]+f*w[3]) % p, w[3])
        formula = f == 0 and (e+d*beta) % p == 0 and (c+a*alpha+b*beta) % p == 0
        assert (image == w) == formula
        count += formula
        images.add(image)
    assert count == p**3 and len(images) == p**3


def test_nonzero_indicator_semantic_coset_split_by_extension_evaluation():
    p = 5
    def indicator(x):
        value = 1
        for actual, target in zip(x, (0, 0, 0, 1)):
            value = value*(1-pow((actual-target) % p, p-1, p)) % p
        return value
    # h=I+E12 fixes e4, so substitution by h^-1 preserves its indicator.
    for x in product(range(p), repeat=4):
        shifted = ((x[0]-x[1]) % p, x[1], x[2], x[3])
        assert indicator(x) == indicator(shifted)
    assert indicator((0, 0, 0, 1)) == 1
    # At (0,t,0,1), F(h^-1*x)-F(x)=t^8-t^4. In F25,
    # t^2=3 defines an extension because 3 is a nonsquare modulo5.
    assert 3 not in {a*a % p for a in range(p)}
    t4, t8 = 3**2 % p, 3**4 % p
    assert (t8-t4) % p == 2


def test_singleton_stabilizer_is_not_normal():
    p = 5
    identity = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
    def shear(i, j, value):
        out = [list(row) for row in identity]
        out[i][j] = value % p
        return out
    def multiply(a, b):
        return [[sum(a[i][k]*b[k][j] for k in range(4)) % p for j in range(4)]
                for i in range(4)]
    h, g, inverse_g = shear(0, 1, 1), shear(1, 3, 1), shear(1, 3, -1)
    conjugate = multiply(multiply(g, h), inverse_g)
    assert tuple(row[3] for row in h) == (0, 0, 0, 1)
    assert tuple(row[3] for row in conjugate) == (p-1, 0, 0, 1)


@pytest.mark.parametrize("satisfiable", [False, True])
def test_nonzero_selector_predicate_distinguishes_constraint_satisfiability(satisfiable):
    p = 5
    def predicate(x, z, y):
        constraints = (x*(x-1), x-1) if satisfiable else (x, x-1)
        chi = 1
        for q in constraints:
            chi = chi*(1-pow(q % p, 4, p)) % p
        delta = 1
        for value, target in zip(y, (0, 0, 0, 1)):
            delta = delta*(1-pow((value-target) % p, 4, p)) % p
        return ((1-pow(z, 4, p))+(1-pow((z-1) % p, 4, p))*chi*delta) % p
    moved = False
    for x, z in product(range(p), repeat=2):
        for y in product(range(p), repeat=4):
            value = predicate(x, z, y)
            assert value in (0, 1)
            if z == 0:
                assert value == 1
            h_inverse_y = ((y[0]-y[1]) % p, y[1], y[2], y[3])
            g_inverse_y = ((y[0]-y[3]) % p, y[1], y[2], y[3])
            assert value == predicate(x, z, h_inverse_y)
            moved |= value != predicate(x, z, g_inverse_y)
    assert moved == satisfiable
