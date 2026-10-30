"""Exact controls for integral descent in B=(Q(sqrt(-11))/Q, bar, -1).

Set R=Z[w], w^2=w-3, and O=R+jR, where j^2=-1 and ja=bar(a)j.
Coordinates are RIGHT R-coordinates x=a+jb; all lattice bases are columns.
Both fixtures are free rank-two R-modules with determinant ideal 2R and
locally principal right O-ideals with norm ideal 2Z. Only YES attains norm 2.
These are fixed-field certificates, not a generic PIP/descent/SVP backend,
a growing-degree complexity claim, or an obstruction on promised-YES inputs.

General-order scope: a common Steinitz model cannot follow from qR being
principal alone. One must first have R=O_L embedded in the right order,
full torsion-free rank-two right R-modules O and I, and local principality
I_p=g_p O_p over O_F. In compatible right L-coordinates, left multiplication
by g_p is L-linear with determinant nrd(g_p). Comparing at every finite
prime then gives det_R(I)=nrd(I)R*det_R(O). ONLY with this comparison and
nrd(I)=q O_F do the Steinitz classes agree. A common coefficient module E
still requires explicit module isomorphisms/pseudo-bases; it is not a literal
equality of the given modules. These tests verify only O=R+jR, where both
rank-two bases and determinant comparisons are explicit. They do not test
arbitrary orders, saturation, or the general Steinitz theorem.
"""

from fractions import Fraction
from itertools import product
from math import gcd, isqrt

import sympy as sp


ZERO = (0, 0)
ONE = (1, 0)
W = (0, 1)
Q = 2
IDENTITY = ((ONE, ZERO), (ZERO, ONE))
S = ((ZERO, (-1, 0)), (ONE, ZERO))
ORDER_BASIS = ((ONE, ZERO), (W, ZERO), (ZERO, ONE), (ZERO, W))
GENERATOR = (ONE, ONE)  # 1+j has norm 2 but is outside the NO ideal.
LOCAL_GENERATOR = (W, (-1, 1))  # w+j(w-1), of norm 6.
P_NO = ((ONE, ZERO), (W, (2, 0)))
P_NO_INVERSE = (
    (ONE, ZERO),
    ((0, Fraction(-1, 2)), (Fraction(1, 2), 0)),
)
# A skewed basis of (1+j)O: neither displayed column has norm 2.
P_YES = ((ONE, ZERO), ((3, 0), (2, 0)))
P_YES_INVERSE = (
    (ONE, ZERO),
    ((Fraction(-3, 2), 0), (Fraction(1, 2), 0)),
)


def _add(x, y):
    return x[0] + y[0], x[1] + y[1]


def _neg(x):
    return -x[0], -x[1]


def _mul(x, y):
    a, b = x
    c, d = y
    return a * c - 3 * b * d, a * d + b * c + b * d


def _bar(x):
    return x[0] + x[1], -x[1]


def _field_norm(x):
    a, b = x
    return a * a + a * b + 3 * b * b


def _quaternion_mul(x, y):
    a, b = x
    c, d = y
    return _add(_mul(a, c), _neg(_mul(_bar(b), d))), _add(
        _mul(b, c), _mul(_bar(a), d)
    )


def _norm(x):
    return _field_norm(x[0]) + _field_norm(x[1])


def _rho(x):
    a, b = x
    return ((a, _neg(_bar(b))), (b, _bar(a)))


def _j(x):
    return _neg(_bar(x[1])), _bar(x[0])


def _matrix_bar(matrix):
    return tuple(tuple(_bar(x) for x in row) for row in matrix)


def _star(matrix):
    return tuple(zip(*_matrix_bar(matrix)))


def _matrix_mul(left, right):
    return tuple(
        tuple(_add(_mul(left[i][0], right[0][j]), _mul(left[i][1], right[1][j]))
              for j in range(2))
        for i in range(2)
    )


def _matrix_vector(matrix, vector):
    return tuple(_add(_mul(row[0], vector[0]), _mul(row[1], vector[1])) for row in matrix)


def _det(matrix):
    return _add(_mul(matrix[0][0], matrix[1][1]), _neg(_mul(matrix[0][1], matrix[1][0])))


def _scalar_matrix(value):
    return (((value, 0), ZERO), (ZERO, (value, 0)))


def _flatten(vector):
    return tuple(coefficient for entry in vector for coefficient in entry)


def _integral(values):
    return all(sp.sympify(value).is_Integer is True for value in values)


def _integral_matrix(matrix):
    return _integral(coefficient for row in matrix for coefficient in _flatten(row))


def _z_matrix(matrix):
    return sp.Matrix.hstack(*(
        sp.Matrix(_flatten(_matrix_vector(matrix, e))) for e in ORDER_BASIS
    ))


def _data(basis, inverse):
    return _matrix_mul(_star(basis), basis), _matrix_mul(
        _matrix_mul(inverse, S), _matrix_bar(basis)
    )


def _in_no(x):
    a, c, b, e = _flatten(x)
    return _integral((a, c, b, e)) and (b + 3 * c) % 2 == 0 and (e - a - c) % 2 == 0


def test_split_representation_preserves_right_coordinates_and_exact_norm():
    assert _mul(W, W) == (-3, 1)
    assert _mul(W, _bar(W)) == (3, 0)
    assert _quaternion_mul((ZERO, ONE), (ZERO, ONE)) == ((-1, 0), ZERO)
    assert _quaternion_mul((ZERO, ONE), (W, ZERO)) == (ZERO, W)
    assert _quaternion_mul((W, ZERO), (ZERO, ONE)) == (ZERO, _bar(W))
    fixtures = ORDER_BASIS + (GENERATOR, LOCAL_GENERATOR,
        ((Fraction(1, 2), Fraction(-2, 3)), (Fraction(3, 5), Fraction(-4, 7))))
    for x in fixtures:
        matrix = _rho(x)
        assert _det(matrix) == (_norm(x), 0)
        assert _matrix_mul(_star(matrix), matrix) == _scalar_matrix(_norm(x))
        assert _matrix_mul(matrix, S) == _matrix_mul(S, _matrix_bar(matrix))
        assert _j(_j(x)) == tuple(_neg(entry) for entry in x)
        assert _quaternion_mul(x, (ZERO, ONE)) == _j(x)
        for y in fixtures:
            assert _rho(_quaternion_mul(x, y)) == _matrix_mul(matrix, _rho(y))
            assert _matrix_vector(matrix, y) == _quaternion_mul(x, y)
            assert _norm(_quaternion_mul(x, y)) == _norm(x) * _norm(y)
    for x, y in product(ORDER_BASIS, repeat=2):
        assert _integral(_flatten(_quaternion_mul(x, y)))


def test_both_modules_are_explicitly_free_but_keep_distinct_descent_metrics():
    expected = (
        (P_NO, P_NO_INVERSE,
         (((4, 0), (2, -2)), ((0, 2), (4, 0))),
         (((-1, 1), (-2, 0)), ((2, 0), W))),
        (P_YES, P_YES_INVERSE,
         (((10, 0), (6, 0)), ((6, 0), (4, 0))),
         (((-3, 0), (-2, 0)), ((5, 0), (3, 0)))),
    )
    for basis, inverse, expected_h, expected_d in expected:
        assert _matrix_mul(basis, inverse) == _matrix_mul(inverse, basis) == IDENTITY
        assert _det(basis) == (Q, 0)  # Explicit R-basis, determinant ideal qR.
        lattice = _z_matrix(basis)
        assert lattice.det() == Q**2
        h, d = _data(basis, inverse)
        assert h == expected_h and d == expected_d
        assert _integral_matrix(d)  # Right-j stability in these integral bases.
        assert _det(h) == (Q**2, 0)
        assert _matrix_mul(d, _matrix_bar(d)) == _scalar_matrix(-1)
        assert _matrix_mul(_matrix_mul(_star(d), h), d) == _matrix_bar(h)
        assert _matrix_mul(basis, d) == _matrix_mul(S, _matrix_bar(basis))
        assert _z_matrix(d) == lattice.inv() * _z_matrix(S) * _z_matrix(_matrix_bar(basis))
        # Right multiplication by every Z-basis element certifies full ideal
        # closure, not just closure of a few sampled ideal vectors.
        for e in ORDER_BASIS:
            right_action = sp.Matrix.hstack(*(
                sp.Matrix(_flatten(_quaternion_mul(f, e))) for f in ORDER_BASIS
            ))
            assert _integral(lattice.inv() * right_action * lattice)
    a, c, b, e = sp.symbols("a c b e", integer=True)
    coordinates = sp.Matrix([a, c, (b + 3 * c) / 2, (e - a - c) / 2])
    assert _z_matrix(P_NO) * coordinates == sp.Matrix([a, c, b, e])
    for entries in product(range(-1, 2), repeat=4):
        x = (entries[:2], entries[2:])
        assert _in_no(x) == _integral(_z_matrix(P_NO_INVERSE) * sp.Matrix(entries))


def test_no_norm_ideal_and_local_principality_have_exact_index_certificates():
    lattice = _z_matrix(P_NO)
    variables = sp.symbols("r s t u", integer=True)
    x = tuple(lattice * sp.Matrix(variables))
    norm_polynomial = sp.Poly(_norm((x[:2], x[2:])), *variables)
    assert all(int(coefficient) % 2 == 0 for coefficient in norm_polynomial.coeffs())
    witnesses = ((ONE, W), LOCAL_GENERATOR)
    assert all(_in_no(x) for x in witnesses)
    assert tuple(_norm(x) for x in witnesses) == (4, 6)
    assert gcd(*(_norm(x) for x in witnesses)) == Q  # nrd(I)=2Z, not just inclusion.

    # 2O is contained in I, so I_p=O_p for every odd prime p.
    assert _integral(lattice.inv() * (2 * sp.eye(4)))
    assert lattice.det() == 4
    principal = sp.Matrix.hstack(*(
        sp.Matrix(_flatten(_quaternion_mul(LOCAL_GENERATOR, e))) for e in ORDER_BASIS
    ))
    assert principal == _z_matrix(_rho(LOCAL_GENERATOR))
    assert principal.det() == _norm(LOCAL_GENERATOR)**2 == 36
    inclusion = lattice.inv() * principal
    assert _integral(inclusion)
    assert lattice * inclusion == principal
    assert inclusion.det() == 9 != 1
    # The index 9 is odd, hence this inclusion is an isomorphism over Z_2:
    # I_2=h O_2. It is NOT an equality of the global lattices.
    assert inclusion.det() % 2 == 1
    assert all(sp.denom(value) % 2 == 1 for value in inclusion.inv())


def test_no_norm_two_is_excluded_by_a_global_bound_not_a_sampled_box():
    a, c, b, e = sp.symbols("a c b e", integer=True)
    norm = _norm(((a, c), (b, e)))
    completed = (2 * a + c)**2 + (2 * b + e)**2 + 11 * (c*c + e*e)
    assert sp.expand(4 * norm - completed) == 0
    # At norm 2, 11*(c^2+e^2)<=8 forces c=e=0 for ALL integral vectors.
    assert 4 * Q < 11
    bound = isqrt(Q)
    candidates = {
        ((a, 0), (b, 0))
        for a, b in product(range(-bound, bound + 1), repeat=2)
        if a*a + b*b == Q
    }
    assert candidates == {((a, 0), (b, 0)) for a, b in product((-1, 1), repeat=2)}
    assert all(_norm(x) == Q and not _in_no(x) for x in candidates)
    assert GENERATOR in candidates
    # The preceding even-norm certificate, positivity, and complete exclusion
    # give minimum 4. Equivalently, H_NO/2 has minimum 2, not 1.
    assert _in_no((ONE, W)) and _norm((ONE, W)) == 4
    assert Fraction(_norm((ONE, W)), Q) == 2


def test_rational_unimodular_descent_satisfies_both_equations_but_is_not_integral():
    h, d = _data(P_NO, P_NO_INVERSE)
    u = (
        (ONE, (-1, 0)),
        ((Fraction(1, 2), Fraction(-1, 2)), (Fraction(1, 2), Fraction(1, 2))),
    )
    assert u == _matrix_mul(P_NO_INVERSE, _rho(GENERATOR))
    assert _det(u) == ONE
    assert _matrix_mul(d, _matrix_bar(u)) == _matrix_mul(u, S)
    assert _matrix_mul(_matrix_mul(_star(u), h), u) == _scalar_matrix(Q)
    assert _matrix_mul(P_NO, u) == _rho(GENERATOR)
    assert not _integral_matrix(u)
    assert _integral_matrix(_matrix_mul(_scalar_matrix(2), u))
    assert not _in_no(GENERATOR)
    assert _norm(GENERATOR) == Q


def test_matched_yes_generator_and_bounded_frame_completion_distinguish_exact_norm():
    h, d = _data(P_YES, P_YES_INVERSE)
    u = ((ONE, (-1, 0)), ((-1, 0), (2, 0)))
    assert _integral_matrix(u) and _det(u) == ONE
    assert _matrix_mul(d, _matrix_bar(u)) == _matrix_mul(u, S)
    assert _matrix_mul(_matrix_mul(_star(u), h), u) == _scalar_matrix(Q)
    assert _matrix_mul(P_YES, u) == _rho(GENERATOR)
    change = _z_matrix(P_YES_INVERSE) * _z_matrix(_rho(GENERATOR))
    assert change == _z_matrix(u)
    assert _integral(change) and _integral(change.inv()) and change.det() == 1
    assert _norm(GENERATOR) == Q
    assert [_norm(tuple(row[i] for row in P_YES)) for i in range(2)] == [10, 4]

    for basis, inverse, attainable in (
        (P_NO, P_NO_INVERSE, False), (P_YES, P_YES_INVERSE, True)
    ):
        h, d = _data(basis, inverse)
        found = False
        for entries in product(range(-1, 2), repeat=4):
            first = (entries[:2], entries[2:])
            second = _matrix_vector(d, tuple(_bar(x) for x in first))
            frame = tuple(zip(first, second))
            x = _matrix_vector(basis, first)
            norm = _norm(x)
            assert _integral_matrix(frame)
            assert _matrix_mul(d, _matrix_bar(frame)) == _matrix_mul(frame, S)
            assert _matrix_mul(basis, frame) == _rho(x)
            assert _det(frame) == (Fraction(norm, Q), 0)
            assert _matrix_mul(_matrix_mul(_star(frame), h), frame) == _scalar_matrix(norm)
            assert (_det(frame) == ONE) == (norm == Q)
            found |= norm == Q
        # YES is witnessed here; the NO completeness proof is the global
        # square-completion test above, not this bounded frame enumeration.
        assert found == attainable
