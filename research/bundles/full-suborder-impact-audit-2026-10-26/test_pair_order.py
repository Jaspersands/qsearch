"""Supplied-order regressions for the native-input boundary; no native search."""

from itertools import product

import pytest
from sympy import Matrix, Rational, eye, symbols, expand

from pair_order import commutator_norm, norm, pair_order, trace
from kernel_output import odd_maximal_order
from native_preprocessing import check_dictionary, check_order


@pytest.mark.parametrize("p", [7, 11, 19, 43])
@pytest.mark.parametrize("left,right", [
    ((0, 1, 0, 0), (0, 0, 1, 0)),
    ((2, 1, 2, -1), (-3, 2, 0, 1)),
    ((0, 2, 0, 0), (0, 0, 3, 0)),
])
def test_native_pair_formula_against_supplied_maximal_order(p, left, right):
    ambient = odd_maximal_order(p)
    a, b = Matrix(left), Matrix(right)
    ab = ambient.multiply(a, b)
    commutator = ab-ambient.multiply(b, a)
    t, n, u, m, v = map(int, (trace(ambient, a), norm(ambient, a),
                              trace(ambient, b), norm(ambient, b), trace(ambient, ab)))
    order = pair_order(t, n, u, m, v)
    change = Matrix.hstack(ambient.unit, a, b, ab)
    check_dictionary(order, ambient, change)
    d = commutator_norm(t, n, u, m, v)
    assert d == norm(ambient, commutator) == p*abs(change.det())
    assert check_order(order).det() == d*d
    assert (4*n-t*t)*(4*m-u*u)-(2*v-t*u)**2 == 4*d
    assert d >= p and (4*n-t*t)*m >= d


def test_discriminant_expression_and_scalar_shift_invariance_symbolically():
    t, n, u, m, v, x, y = symbols("t n u m v x y")
    d = 4*n*m-n*u*u-m*t*t-v*v+t*u*v
    assert expand((4*n-t*t)*(4*m-u*u)-(2*v-t*u)**2-4*d) == 0
    gram = Matrix([[2, t, u, v], [t, 2*n, t*u-v, n*u],
                   [u, t*u-v, 2*m, m*t], [v, n*u, m*t, 2*n*m]])
    assert expand(gram.det()-d*d) == 0
    shifted = {t: t+2*x, n: n+x*t+x*x,
               u: u+2*y, m: m+y*u+y*y,
               v: v+x*u+y*t+2*x*y}
    assert expand(d.subs(shifted, simultaneous=True)-d) == 0


def test_commuting_nonscalar_inputs_are_rejected():
    ambient = odd_maximal_order(11)
    a = eye(4)[:, 2]
    b = 3*ambient.unit+7*a
    data = tuple(map(int, (trace(ambient, a), norm(ambient, a), trace(ambient, b),
                          norm(ambient, b), trace(ambient, ambient.multiply(a, b)))))
    assert commutator_norm(*data) == 0
    with pytest.raises(ValueError, match="commutator"):
        pair_order(*data)


@pytest.mark.parametrize("data", [
    (2, 1, 0, 11, 0),
    (0, 0, 0, 11, 0),
    (0, 1, 0, 11, 100),
    (False, 1, 0, 11, 0),
    (0, Rational(1, 2), 0, 11, 0),
])
def test_invalid_or_nonpositive_data_rejected(data):
    with pytest.raises(ValueError):
        pair_order(*data)


def test_discriminant_divisibility_is_not_a_native_provenance_certificate():
    # a=i, b=5j in Hamilton's algebra, ramified at 2, not at the claimed p=5.
    order = pair_order(0, 1, 0, 25, 0)
    d = commutator_norm(0, 1, 0, 25, 0)
    assert d == 100 and d % 5 == 0
    assert check_order(order).det() == 10000
    i, j = eye(4)[:, 1], eye(4)[:, 2]/5
    assert order.multiply(i, i) == -order.unit
    assert order.multiply(j, j) == -order.unit
    assert order.multiply(i, j) == -order.multiply(j, i)


def test_transport_and_exact_division_do_not_create_a_new_direction():
    ambient = odd_maximal_order(11)
    a = eye(4)[:, 2]
    phi = ambient.unit+eye(4)[:, 1]+eye(4)[:, 3]
    degree = norm(ambient, phi)
    transported = ambient.multiply(ambient.multiply(phi, a), ambient.star(phi))
    returned = ambient.multiply(ambient.multiply(ambient.star(phi), transported), phi)
    assert returned == degree**2*a
    inverse = ambient.star(phi)/degree
    oriented = transported/degree
    for r, s in product(range(-2, 3), repeat=2):
        value = r*ambient.unit+s*oriented
        pullback = ambient.multiply(ambient.multiply(inverse, value), phi)
        assert pullback == r*ambient.unit+s*a
        assert ambient.multiply(a, pullback) == ambient.multiply(pullback, a)
