"""Bounded exact checks for one integral-similarity output-size family.

These controls concern expanded witnesses, not decision hardness. Large cases
use modular coefficients and symbolic induction identities, never expanded units.
"""

import sys

import pytest
from sympy import Matrix, Poly, Rational, ZZ, expand, eye, linsolve, symbols, sympify, zeros
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form


MAX_EXPANDED_EXPONENT = 1024
MAX_ORDER_M = 256
MAX_MODULUS_BITS = 512
MAX_EXPONENT_BITS = 256


def _order_parameter(m):
    if type(m) is not int or not 2 <= m <= MAX_ORDER_M:
        raise ValueError("order parameter exceeds bounded test scope")
    return 1 << m


def _pair_multiply(x, y):
    a, b = x
    c, d = y
    return a * c + 2 * b * d, a * d + b * c


def _pell_power(k, modulus=None):
    if type(k) is not int:
        raise ValueError("integer exponent required")
    if modulus is None:
        if abs(k) > MAX_EXPANDED_EXPONENT:
            raise ValueError("expanded exponent exceeds resource cap")
    elif (type(modulus) is not int or modulus < 2
          or modulus.bit_length() > MAX_MODULUS_BITS
          or abs(k).bit_length() > MAX_EXPONENT_BITS):
        raise ValueError("modular power exceeds resource cap")

    def multiply(x, y):
        a, b = _pair_multiply(x, y)
        return (a, b) if modulus is None else (a % modulus, b % modulus)

    result = (1, 0)
    base = (1, 1) if k >= 0 else (-1, 1)
    if modulus is not None:
        base = tuple(x % modulus for x in base)
    remaining = abs(k)
    while remaining:
        if remaining & 1:
            result = multiply(result, base)
        remaining >>= 1
        if remaining:
            base = multiply(base, base)
    return result


def _matrices(f):
    return (
        Matrix([[0, 2 * f * f], [1, 0]]),
        Matrix([[f * f, 2 * f * f], [1 - Rational(1, 2) * f * f, -f * f]]),
    )


def _transporter(f, a, b):
    f, a, b = map(sympify, (f, a, b))
    return Matrix([[a, 2 * f * b], [b / f - a / 2, a - f * b]])


def _expanded_witness(m, sign=1):
    # Check before constructing f, k, or any Pell coefficients.
    if type(m) is not int or not 2 <= m <= MAX_EXPANDED_EXPONENT.bit_length():
        raise ValueError("expanded witness exceeds resource cap")
    if sign not in (-1, 1):
        raise ValueError("exponent sign must be +/-1")
    f = _order_parameter(m)
    a, b = _pell_power(sign * (f // 2))
    return f, a, b, _transporter(f, a, b)


def _v2(n):
    if n == 0:
        raise ValueError("valuation of zero is not finite")
    n = abs(n)
    return (n & -n).bit_length() - 1


def test_solve_all_intertwiner_equations_and_determinant_symbolically():
    f = symbols("f", nonzero=True)
    p, q, r, s, a, b = symbols("p q r s a b")
    A, B = _matrices(f)
    unknown = Matrix([[p, q], [r, s]])
    solutions = linsolve(list(B * unknown - unknown * A), (q, s))
    assert len(solutions) == 1
    q_value, s_value = next(iter(solutions))
    assert expand(q_value - f**2 * (p + 2 * r)) == 0
    assert expand(s_value - ((1 - f**2 / 2) * p - f**2 * r)) == 0
    general = unknown.subs({q: q_value, s: s_value})
    reparametrized = general.subs({p: a, r: b / f - a / 2})
    C = _transporter(f, a, b)
    assert (reparametrized - C).applyfunc(expand) == zeros(2)
    assert (B * C - C * A).applyfunc(expand) == zeros(2)
    assert expand(C.det() - (a**2 - 2 * b**2)) == 0


def test_characteristic_polynomial_and_rational_transporter_symbolically():
    f = symbols("f", positive=True)
    x = symbols("x")
    A, B = _matrices(f)
    expected = x**2 - 2 * f**2
    assert expand(A.charpoly(x).as_expr() - expected) == 0
    assert expand(B.charpoly(x).as_expr() - expected) == 0
    assert Poly(expected, x).discriminant() == 8 * f**2
    Q = Matrix([[1, 0], [-Rational(1, 2), 1]])
    assert Q.det() == 1 and not all(v.is_Integer for v in Q)
    assert (B * Q - Q * A).applyfunc(expand) == zeros(2)
    for m in range(2, 9):
        assert Poly(expected.subs(f, _order_parameter(m)), x, domain=ZZ).is_irreducible


@pytest.mark.parametrize("m", [2, 3, 5])
def test_integrality_congruence_including_negative_and_nonunit_controls(m):
    f = _order_parameter(m)
    for a in range(-9, 10):
        for b in range(-2 * f, 2 * f + 1):
            C = _transporter(f, a, b)
            integral = all(v.is_Integer for v in C)
            assert integral == ((b - (f // 2) * a) % f == 0)
            if integral:
                assert C.det() == a * a - 2 * b * b
    assert not all(v.is_Integer for v in _transporter(f, 1, 0))


@pytest.mark.parametrize("sign", [-1, 1])
def test_pell_valuations_and_inverse_by_independent_linear_recurrence(sign):
    a, b = 1, 0
    assert _pell_power(0) == (1, 0)
    with pytest.raises(ValueError):
        _v2(0)
    for n in range(1, 129):
        if sign == 1:
            a, b = a + 2 * b, a + b
        else:
            a, b = -a + 2 * b, a - b
        k = sign * n
        assert _pell_power(k) == (a, b)
        assert a * a - 2 * b * b == (-1) ** n
        assert a % 2 == 1 and _v2(b) == _v2(k)
        c, d = _pell_power(-k)
        assert (a * c + 2 * b * d, a * d + b * c) == (1, 0)
        for m in range(2, 7):
            f = _order_parameter(m)
            assert ((b - (f // 2) * a) % f == 0) == (k % f == f // 2)
            assert (b % f == 0) == (k % f == 0)


@pytest.mark.parametrize("m", [2, 3, 4, 5, 8, 11])
@pytest.mark.parametrize("sign", [-1, 1])
def test_bounded_expanded_witness_and_exact_integer_bit_bounds(m, sign):
    f, a, b, C = _expanded_witness(m, sign)
    A, B = _matrices(f)
    assert all(v.is_Integer for v in C)
    assert B * C == C * A and C.det() == 1
    assert C.inv() * B * C == A
    k = f // 2
    assert (1 << (k - 1)) < abs(a) < (1 << (2 * k))
    assert k <= abs(a).bit_length() <= 2 * k
    if m == 2 and sign == 1:
        assert C == Matrix([[3, 16], [-1, -5]])


@pytest.mark.parametrize("m", [2, 3, 4, 6])
def test_order_ideal_multiplication_index_and_principal_generator(m):
    f, a, b, C = _expanded_witness(m)
    A, B = _matrices(f)
    # Columns are bases in the fixed maximal-order basis (1, sqrt(2)).
    R = Matrix([[1, 0], [0, f]])
    J = Matrix([[2, 0], [f, 2 * f]])
    theta = Matrix([[0, 2 * f], [f, 0]])
    assert theta * R == R * A
    assert theta * J == J * B
    coordinates = R.inv() * J
    assert coordinates == Matrix([[2, 0], [1, 2]])
    assert all(v.is_Integer for v in coordinates)
    assert abs(coordinates.det()) == 4
    S = smith_normal_form(coordinates, domain=ZZ)
    assert [abs(S[i, i]) for i in range(2)] == [1, 4]

    beta = Matrix([[2 * a, 4 * b], [2 * b, 2 * a]])
    assert beta.det() == 4
    assert beta * R == J * C
    assert hermite_normal_form(beta * R) == hermite_normal_form(J)
    # Extending J to Z[sqrt(2)] removes the conductor restriction.
    sqrt_two = Matrix([[0, 2], [1, 0]])
    assert hermite_normal_form(J.row_join(sqrt_two * J)) == 2 * eye(2)


def test_symbolic_norm_and_lower_bound_induction_for_compact_squaring():
    a, b = symbols("a b")
    next_a, next_b = a**2 + 2 * b**2, 2 * a * b
    assert expand(next_a**2 - 2 * next_b**2 - (a**2 - 2 * b**2)**2) == 0
    assert expand(next_a - (2 * a**2 - 1) + (a**2 - 2 * b**2 - 1)) == 0
    assert _pell_power(2) == (3, 2)
    assert 3 * 3 - 2 * 2 * 2 == 1
    # If a >= t+1, t=2**(k-1), then a_(2k) > 2*t**2=2**(2k-1).
    t = symbols("t", positive=True)
    margin = expand(2 * (t + 1)**2 - 1 - 2 * t**2)
    assert margin == 4 * t + 1 and margin.is_positive


@pytest.mark.parametrize("m", [128, 256])
def test_large_compact_certificate_uses_only_bounded_residues(m, monkeypatch):
    f = _order_parameter(m)
    k, modulus = f // 2, 2 * f
    original = _pair_multiply
    calls = 0

    def bounded_multiply(x, y):
        nonlocal calls
        calls += 1
        assert all(0 <= v < modulus for v in (*x, *y))
        product = original(x, y)
        assert max(v.bit_length() for v in product) <= 2 * modulus.bit_length() + 2
        return product

    monkeypatch.setattr(sys.modules[__name__], "_pair_multiply", bounded_multiply)
    with pytest.raises(ValueError, match="resource cap"):
        _pell_power(k)
    assert calls == 0
    a, b = _pell_power(k, modulus)
    assert calls <= 2 * k.bit_length()
    assert a % 2 == 1 and b % f == f // 2
    assert (2 * b - f * a) % (2 * f) == 0
    assert (a * a - 2 * b * b) % modulus == 1

    # Independent circuit traversal carries the exact norm and the lower-bound
    # exponent via the symbolic identities above; residues alone do not prove it.
    x, y, norm, lower_bits = 3, 2, 1, 2
    for _ in range(m - 2):
        x, y = (x * x + 2 * y * y) % modulus, (2 * x * y) % modulus
        norm *= norm
        lower_bits *= 2
        assert x.bit_length() <= m + 2 and y.bit_length() <= m + 2
    assert (x, y) == (a, b) and norm == 1
    assert lower_bits == k and lower_bits.bit_length() == m
    assert lower_bits > MAX_EXPANDED_EXPONENT
    # Neighboring exponent classes are not integral witnesses.
    for offset in (-1, 1):
        c, d = _pell_power(k + offset, modulus)
        assert (2 * d - f * c) % (2 * f) != 0


@pytest.mark.parametrize("k,modulus", [
    (MAX_EXPANDED_EXPONENT + 1, None),
    (-MAX_EXPANDED_EXPONENT - 1, None),
    (1 << MAX_EXPONENT_BITS, 17),
    (2, 1 << MAX_MODULUS_BITS),
])
def test_power_resource_caps_reject_before_multiplication(k, modulus, monkeypatch):
    def forbidden(*args):
        pytest.fail("coefficient multiplication occurred before resource rejection")

    monkeypatch.setattr(sys.modules[__name__], "_pair_multiply", forbidden)
    with pytest.raises(ValueError, match="resource cap"):
        _pell_power(k, modulus)


def test_witness_resource_cap_precedes_even_order_parameter_construction(monkeypatch):
    def forbidden(*args):
        pytest.fail("order parameter constructed before resource rejection")

    monkeypatch.setattr(sys.modules[__name__], "_order_parameter", forbidden)
    for m in (MAX_EXPANDED_EXPONENT.bit_length() + 1, 10**9):
        with pytest.raises(ValueError, match="resource cap"):
            _expanded_witness(m)
