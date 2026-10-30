"""Bounded exact controls for a trace-normalized quaternion norm target.

The parent setting assumes F totally real of degree d, B totally definite,
I a nonzero locally principal left O-ideal, q totally positive, and
nrd(I) = q*O_F. For NONZERO x in I, zeta=nrd(x)/q is a totally positive
algebraic integer. The parent trace bound is Tr(zeta)>=d, with equality
exactly at zeta=1. We use the supplied Siegel gap Tr(zeta)>=3*d/2 for
zeta!=1 as context, not a theorem proved by this finite enumeration.

An approximate-SVP inference additionally needs an attainable target slice
(minimum squared length d). Since Q_q is SQUARED length, gamma^2<3/2 is
the strict sufficient threshold for UNCORRECTED output. Its boundary is
not an algorithmic impossibility: integral scalar units correct the 3/2
and 5/3 exceptions. The parent's corrected gamma^2<7/4 claim depends on
the supplied Smyth trace classification; the identities here do not prove
that classification. Off-target does not mean nongenerator: units can
generate I while their reduced norms differ from the chosen q.

For the supplied integral basis of a 2-power real cyclotomic center,
Tr(O_F)=d*Z makes a non-target normalized norm have trace at least 2*d.
The corresponding strict gamma^2<2 inference again needs an attainable
target slice. Small quotient-ring checks below certify the basis traces,
not a general integral-basis theorem or an approximate-SVP backend.

The main fixtures use F=Q(sqrt(5)), phi^2=phi+1, and the Hamilton order
O=O_F+O_F*i+O_F*j+O_F*k. All ideal fixtures are explicitly principal,
hence locally principal; no maximal-order assumption or generic backend,
hidden-generator recovery, or general proof is supplied by these tests.
The Q(sqrt(3)) fixture shows that ordinary principality and the correct
norm ideal alone need not make the chosen exact norm attainable.
"""

from fractions import Fraction
from itertools import product

import pytest
import sympy as sp


FZERO = (0, 0)
FONE = (1, 0)
PHI = (0, 1)
ZERO = (FZERO,) * 4
ONE = (FONE, FZERO, FZERO, FZERO)
I = (FZERO, FONE, FZERO, FZERO)
J = (FZERO, FZERO, FONE, FZERO)
K = (FZERO, FZERO, FZERO, FONE)
DEGREE = 2


def _fadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def _fneg(x):
    return -x[0], -x[1]


def _fmul(x, y):
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c + b * d


def _fsum(values):
    result = FZERO
    for value in values:
        result = _fadd(result, value)
    return result


def _ftrace(x):
    return 2 * x[0] + x[1]


def _fnorm(x):
    a, b = x
    return a * a + a * b - b * b


def _finverse(x):
    a, b = x
    norm = _fnorm(x)
    if norm == 0:
        raise ZeroDivisionError("zero field element")
    return Fraction(a + b) / norm, Fraction(-b) / norm


def _totally_positive(x):
    # Both embeddings are real: positive product and sum means both positive.
    return _fnorm(x) > 0 and _ftrace(x) > 0


def _integral(values):
    return all(sp.sympify(x).is_Integer is True for x in values)


def _qadd(x, y):
    return tuple(_fadd(a, b) for a, b in zip(x, y))


def _qmul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (
        _fsum((_fmul(a, e), _fneg(_fmul(b, f)), _fneg(_fmul(c, g)), _fneg(_fmul(d, h)))),
        _fsum((_fmul(a, f), _fmul(b, e), _fmul(c, h), _fneg(_fmul(d, g)))),
        _fsum((_fmul(a, g), _fmul(c, e), _fmul(d, f), _fneg(_fmul(b, h)))),
        _fsum((_fmul(a, h), _fmul(d, e), _fmul(b, g), _fneg(_fmul(c, f)))),
    )


def _qconjugate(x):
    return (x[0],) + tuple(_fneg(a) for a in x[1:])


def _qnorm(x):
    return _fsum(_fmul(a, a) for a in x)


def _flatten(x):
    return tuple(value for pair in x for value in pair)


def _unflatten(values):
    values = tuple(values)
    assert len(values) == 8
    return tuple((values[j], values[j + 1]) for j in range(0, 8, 2))


ORDER_BASIS = tuple(_unflatten(int(i == j) for i in range(8)) for j in range(8))
ALPHA = (PHI, FONE, FZERO, FZERO)


def _right_matrix(x):
    return sp.Matrix.hstack(*(sp.Matrix(_flatten(_qmul(e, x))) for e in ORDER_BASIS))


def _normalized_norm(x, q):
    if not _totally_positive(q):
        raise ValueError("normalizing q must be totally positive")
    return _fmul(_qnorm(x), _finverse(q))


def _weighted_trace(x, q):
    return _ftrace(_normalized_norm(x, q))


def _polarized_gram(q, basis=ORDER_BASIS):
    diagonal = [_weighted_trace(e, q) for e in basis]
    return sp.Matrix(
        [
            [
                (_weighted_trace(_qadd(e, f), q) - diagonal[i] - diagonal[j])
                * Fraction(1, 2)
                for j, f in enumerate(basis)
            ]
            for i, e in enumerate(basis)
        ]
    )


@pytest.fixture(scope="module")
def bounded_norms():
    """The whole [-1,1]^8 box, retaining zero to test its explicit exclusion."""
    records = []
    for coordinates in product(range(-1, 2), repeat=8):
        x = _unflatten(coordinates)
        norm = _qnorm(x)
        records.append((x, norm, _ftrace(norm)))
    return records


def test_exact_integral_field_basis_trace_inverse_and_real_embeddings():
    assert _fmul(PHI, PHI) == (1, 1)
    assert _finverse(PHI) == (-1, 1)
    assert _fmul(PHI, (-1, 1)) == FONE
    phi_plus, phi_minus = (1 + sp.sqrt(5)) / 2, (1 - sp.sqrt(5)) / 2
    for a, b in product(range(-2, 3), repeat=2):
        x = (a, b)
        conjugate = (a + b, -b)
        assert _ftrace(x) == 2 * a + b
        assert _fmul(x, conjugate) == (_fnorm(x), 0)
        assert sp.simplify((a + b * phi_plus) + (a + b * phi_minus)) == _ftrace(x)
        assert sp.expand((a + b * phi_plus) * (a + b * phi_minus)) == _fnorm(x)
        if x != FZERO:
            assert _fmul(x, _finverse(x)) == FONE
            assert _totally_positive(_fmul(x, x))
    with pytest.raises(ZeroDivisionError):
        _finverse(FZERO)


def test_hamilton_order_relations_integral_closure_and_norm_multiplicativity():
    minus_one = ((-1, 0), FZERO, FZERO, FZERO)
    for e in (I, J, K):
        assert _qmul(e, e) == minus_one
    assert _qmul(I, J) == K
    assert _qmul(J, I) == tuple(_fneg(a) for a in K)
    for x, y in product(ORDER_BASIS, repeat=2):
        assert _integral(_flatten(_qmul(x, y)))
    for x, y, z in product((ONE, I, J, K), repeat=3):
        assert _qmul(_qmul(x, y), z) == _qmul(x, _qmul(y, z))
    rational = ((Fraction(1, 2), Fraction(-1, 3)), PHI, FONE, (-1, 2))
    fixtures = (ZERO, ONE, I, J, K, ALPHA, rational)
    for x in fixtures:
        assert _qmul(x, _qconjugate(x)) == (_qnorm(x), FZERO, FZERO, FZERO)
        for y in fixtures:
            assert _qnorm(_qmul(x, y)) == _fmul(_qnorm(x), _qnorm(y))
            assert _qconjugate(_qmul(x, y)) == _qmul(_qconjugate(y), _qconjugate(x))


def test_order_trace_form_and_rational_polarization_are_exact():
    gram = _polarized_gram(FONE)
    expected = sp.diag(*(sp.Matrix([[2, 1], [1, 3]]) for _ in range(4)))
    assert gram == expected
    assert gram.det() == 5**4
    assert all(gram[:n, :n].det() > 0 for n in range(1, 9))
    coordinates = sp.symbols("a0 b0 a1 b1 a2 b2 a3 b3")
    pairs = _unflatten(coordinates)
    norm_trace = _ftrace(_qnorm(pairs))
    squares = sum((a + b) ** 2 + a * a + 2 * b * b for a, b in pairs)
    assert sp.expand(norm_trace - squares) == 0
    vector = sp.Matrix(coordinates)
    assert sp.expand((vector.T * gram * vector)[0] - norm_trace) == 0


def test_zero_is_excluded_from_every_positive_trace_claim(bounded_norms):
    assert len(bounded_norms) == 3**8
    assert [(x, norm, trace) for x, norm, trace in bounded_norms if x == ZERO] == [(ZERO, FZERO, 0)]
    assert _normalized_norm(ZERO, FONE) == FZERO
    assert not _totally_positive(FZERO)
    assert sum(x != ZERO for x, _, _ in bounded_norms) == 3**8 - 1
    for invalid_q in (FZERO, (-1, 0), PHI):
        with pytest.raises(ValueError, match="totally positive"):
            _normalized_norm(ONE, invalid_q)


def test_complete_bounded_box_has_trace_lower_bound_and_exact_target_equality(bounded_norms):
    for x, norm, trace in bounded_norms:
        if x == ZERO:
            continue
        assert _integral(norm)
        assert _totally_positive(norm)
        assert _fnorm(norm) >= 1
        assert trace >= DEGREE
        assert (trace == DEGREE) == (norm == FONE)
        # This is the exact quadratic-field AM-GM identity, not float sampling.
        assert trace**2 - 4 * _fnorm(norm) == 5 * norm[1] ** 2
    assert sum(trace == DEGREE for _, _, trace in bounded_norms) == 8


def test_bounded_off_target_norms_have_trace_at_least_three(bounded_norms):
    off_target = [(x, norm, trace) for x, norm, trace in bounded_norms if x != ZERO and norm != FONE]
    assert len(off_target) == 3**8 - 1 - 8
    assert min(trace for _, _, trace in off_target) == 3
    assert all(trace >= Fraction(3, 2) * DEGREE for _, _, trace in off_target)
    assert sum(trace == 3 for _, _, trace in off_target) == 16
    # The universal Siegel theorem is not inferred from these finite counts.


def test_scalar_phi_generates_order_but_is_off_the_norm_one_slice():
    scalar_phi = (PHI, FZERO, FZERO, FZERO)
    inverse = ((-1, 1), FZERO, FZERO, FZERO)
    assert _qmul(scalar_phi, inverse) == _qmul(inverse, scalar_phi) == ONE
    multiplication = _right_matrix(scalar_phi)
    assert multiplication.det() == 1
    assert _integral(multiplication) and _integral(multiplication.inv())
    assert multiplication * _right_matrix(inverse) == sp.eye(8)
    assert _qnorm(scalar_phi) == (1, 1) != FONE
    assert _fnorm(_qnorm(scalar_phi)) == 1
    assert _totally_positive(_qnorm(scalar_phi))
    assert _weighted_trace(scalar_phi, FONE) == 3
    assert _weighted_trace(ONE, FONE) == 2


@pytest.mark.parametrize("gamma", (Fraction(1), Fraction(7, 6), Fraction(6, 5)))
def test_strict_length_approximation_threshold_for_attained_slice(gamma, bounded_norms):
    assert gamma**2 < Fraction(3, 2)
    minimum_squared_length = min(trace for x, _, trace in bounded_norms if x != ZERO)
    assert minimum_squared_length == DEGREE == _weighted_trace(ONE, FONE)
    assert gamma**2 * minimum_squared_length < Fraction(3, 2) * DEGREE
    admissible = [
        norm for x, norm, trace in bounded_norms
        if x != ZERO and trace <= gamma**2 * minimum_squared_length
    ]
    assert admissible and all(norm == FONE for norm in admissible)


def test_threshold_equality_only_fails_for_uncorrected_output():
    scalar_phi = (PHI, FZERO, FZERO, FZERO)
    minimum_squared_length = _weighted_trace(ONE, FONE)
    candidate_squared_length = _weighted_trace(scalar_phi, FONE)
    gamma_squared = Fraction(3, 2)
    assert candidate_squared_length / minimum_squared_length == gamma_squared
    assert candidate_squared_length <= gamma_squared * DEGREE
    assert _qnorm(scalar_phi) != FONE
    # An inclusive contract may return phi, but this is NOT an impossibility.
    # Compute the correcting unit from zeta, not from a hidden generator.
    zeta = _normalized_norm(scalar_phi, FONE)
    unit = _fadd(zeta, (-1, 0))
    inverse = _finverse(unit)
    assert unit == PHI and inverse == (-1, 1)
    assert _integral(unit) and _integral(inverse)
    assert _fmul(unit, unit) == zeta
    assert _fmul(unit, inverse) == FONE
    for target_generator in (ONE, ALPHA):
        q = _qnorm(target_generator)
        x = _qmul(scalar_phi, target_generator)
        assert _normalized_norm(x, q) == zeta
        corrected = tuple(_fmul(inverse, a) for a in x)
        assert corrected == target_generator
        assert _integral(_flatten(corrected))
        assert _normalized_norm(corrected, q) == FONE
        assert _weighted_trace(corrected, q) == DEGREE


@pytest.mark.parametrize(
    "coefficients, root_coefficients, inverse_coefficients, intervals",
    (
        ((1, -3, 1), (1, -1), (1, -2), ((0, 1), (2, 3))),
        ((1, -5, 6, -1), (1, -3, 1), (1, -4, 3), ((0, 1), (1, 2), (3, 4))),
    ),
    ids=("quadratic-trace-three", "cubic-trace-five"),
)
def test_exception_polynomials_have_integral_unit_square_root_corrections(
    coefficients, root_coefficients, inverse_coefficients, intervals
):
    """Exact exception identities, not a classification of low-trace integers."""
    z = sp.Symbol("z")
    polynomial = sp.Poly.from_list(coefficients, z, domain=sp.QQ)
    unit = sp.Poly.from_list(root_coefficients, z, domain=sp.QQ)
    inverse = sp.Poly.from_list(inverse_coefficients, z, domain=sp.QQ)
    variable = sp.Poly(z, z, domain=sp.QQ)
    one = sp.Poly(1, z, domain=sp.QQ)
    assert polynomial.is_irreducible
    assert len(intervals) == polynomial.degree()
    assert all(polynomial.count_roots(left, right) == 1 for left, right in intervals)
    assert all(left >= 0 for left, _ in intervals)
    assert polynomial.eval(0) != 0  # All roots are strictly positive.
    trace = -polynomial.nth(polynomial.degree() - 1)
    assert trace / polynomial.degree() in (sp.Rational(3, 2), sp.Rational(5, 3))
    assert trace / polynomial.degree() < sp.Rational(7, 4)
    assert (-1) ** polynomial.degree() * polynomial.TC() == 1
    quotient, remainder = (unit**2 - variable).div(polynomial)
    assert remainder.is_zero
    assert quotient.as_expr() == (1 if polynomial.degree() == 2 else z - 1)
    assert _integral(unit.all_coeffs()) and _integral(inverse.all_coeffs())
    assert (unit * inverse).rem(polynomial) == one
    assert (inverse**2 * variable).rem(polynomial) == one

    # All coefficients below are algebraic integers. Integral scalar units
    # preserve any O_F-ideal, regardless of whether Z[z] is the full O_F.
    zero = sp.Poly(0, z, domain=sp.QQ)
    alpha = (one, variable, one, zero)  # Known noncentral fixture only.
    q = sum((a**2 for a in alpha), zero).rem(polynomial)
    assert q == (variable**2 + 2).rem(polynomial)  # Totally positive.
    q_inverse = sp.invert(q, polynomial)
    assert (q * q_inverse).rem(polynomial) == one
    x = tuple((unit * a).rem(polynomial) for a in alpha)
    x_norm = sum((a**2 for a in x), zero).rem(polynomial)
    assert (x_norm * q_inverse).rem(polynomial) == variable
    corrected = tuple((inverse * a).rem(polynomial) for a in x)
    assert corrected == alpha
    assert all(_integral(a.all_coeffs()) for a in x + corrected)
    corrected_norm = sum((a**2 for a in corrected), zero).rem(polynomial)
    assert corrected_norm == q
    assert (corrected_norm * q_inverse).rem(polynomial) == one


def test_known_noncentral_principal_fixture_has_exact_norm_ideal_and_left_stability():
    q = _qnorm(ALPHA)
    assert q == (2, 1) and _totally_positive(q)
    assert _qmul(ALPHA, J) != _qmul(J, ALPHA)
    inverse = tuple(_fmul(a, _finverse(q)) for a in _qconjugate(ALPHA))
    assert _qmul(ALPHA, inverse) == _qmul(inverse, ALPHA) == ONE
    basis = _right_matrix(ALPHA)
    assert _integral(basis)
    assert basis.det() == _fnorm(q) ** 2 == 25
    for e in ORDER_BASIS:
        for f in ORDER_BASIS:
            x = _qmul(f, ALPHA)
            assert _integral(basis.inv() * sp.Matrix(_flatten(_qmul(e, x))))
    # Every x=y*alpha has nrd(x)=nrd(y)*q; alpha itself attains q.
    # Thus nrd(I)=q*O_F, not merely a norm-ideal inclusion.
    assert _normalized_norm(ALPHA, q) == FONE


def test_weighted_gram_pulls_back_to_order_trace_form_under_known_right_multiplication():
    q = _qnorm(ALPHA)
    multiplication = _right_matrix(ALPHA)
    weighted = _polarized_gram(q)
    unweighted = _polarized_gram(FONE)
    assert all(value.is_Rational is True for value in weighted)
    assert weighted == sp.eye(8)
    assert all(weighted[:n, :n].det() > 0 for n in range(1, 9))
    assert multiplication.T * weighted * multiplication == unweighted
    ideal_basis = tuple(_qmul(e, ALPHA) for e in ORDER_BASIS)
    assert _polarized_gram(q, ideal_basis) == unweighted
    assert weighted.det() * multiplication.det() ** 2 == unweighted.det()
    assert multiplication.T * unweighted * multiplication != unweighted


def test_bounded_principal_ideal_normalization_matches_order_norms(bounded_norms):
    q = _qnorm(ALPHA)
    q_inverse = _finverse(q)
    for y, norm, trace in bounded_norms:
        if y == ZERO:
            continue
        x = _qmul(y, ALPHA)
        assert x != ZERO
        assert _qnorm(x) == _fmul(norm, q)
        zeta = _fmul(_qnorm(x), q_inverse)
        assert zeta == norm and _integral(zeta) and _totally_positive(zeta)
        assert _ftrace(zeta) == trace >= DEGREE
        assert (trace == DEGREE) == (_qnorm(x) == q)
        if _qnorm(x) != q:
            assert trace >= 3


def test_missing_integrality_breaks_trace_equality_in_q_sqrt_two():
    sqrt_two = sp.sqrt(2)
    x = ((1 + sqrt_two) / 2, sp.Rational(1, 2), 0, 0)
    norm = sp.expand(sum(coefficient**2 for coefficient in x))
    conjugate = norm.xreplace({sqrt_two: -sqrt_two})
    assert norm == 1 + sqrt_two / 2 != 1
    assert norm.is_positive is True and conjugate.is_positive is True
    assert sp.simplify(norm + conjugate) == 2
    assert sp.expand(norm * conjugate) == sp.Rational(1, 2)
    t = sp.Symbol("t")
    assert sp.minpoly(norm, t) == 2 * t**2 - 4 * t + 1
    assert sp.Poly(sp.minpoly(norm, t), t).monic().all_coeffs() == [1, -2, sp.Rational(1, 2)]
    # This nonintegral norm cannot be a totally positive algebraic INTEGER.
    # x is in J=(1/2)*O: doubling its integral-basis coordinates is integral.
    integral_basis_coordinates = (sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2), 0)
    assert _integral(2 * value for value in integral_basis_coordinates)
    assert not _integral(integral_basis_coordinates)
    ideal_norm_generator = sp.Rational(1, 2) ** 2
    assert ideal_norm_generator == sp.Rational(1, 4) != 1
    assert not ideal_norm_generator.is_Integer
    # All norms in J lie in (1/4)*O_F, with 1/4 attained by scalar 1/2.
    # Hence nrd(J)=(1/4)*O_F, NOT the falsely selected target ideal O_F.
    corrected_zeta = sp.expand(norm / ideal_norm_generator)
    assert corrected_zeta == 4 + 2 * sqrt_two
    assert sp.minpoly(corrected_zeta, t) == t**2 - 8 * t + 8
    assert sp.simplify(corrected_zeta + corrected_zeta.xreplace({sqrt_two: -sqrt_two})) == 8


def test_principal_order_and_correct_norm_ideal_need_not_attain_chosen_norm():
    """In Q(sqrt(3)), I=O is principal but q=2+sqrt(3) is not a norm in O."""
    sqrt_three = sp.sqrt(3)
    q, inverse = 2 + sqrt_three, 2 - sqrt_three
    assert q.is_positive is True and inverse.is_positive is True
    assert sp.expand(q * inverse) == 1
    assert sp.simplify(q + inverse) == 4
    # O_F=Z[sqrt(3)]; this unimodular multiplication proves q*O_F=O_F.
    multiplication = sp.Matrix([[2, 3], [1, 2]])
    assert multiplication.det() == 1
    assert multiplication.inv() == sp.Matrix([[2, -3], [-1, 2]])
    assert _integral(multiplication.inv())
    # I=O*1 is globally (hence locally) principal and its norm ideal is O_F:
    # norms of integral quaternions are integral and nrd(1)=1 is attained.
    a = sp.symbols("a0:4", integer=True)
    b = sp.symbols("b0:4", integer=True)
    s = sp.Symbol("s")
    norm = sp.rem(sum((ai + bi * s) ** 2 for ai, bi in zip(a, b)), s**2 - 3, s)
    rational_coefficient = sum(ai**2 + 3 * bi**2 for ai, bi in zip(a, b))
    sqrt_coefficient = 2 * sum(ai * bi for ai, bi in zip(a, b))
    assert sp.expand(norm - rational_coefficient - s * sqrt_coefficient) == 0
    assert sp.Poly(norm, s).nth(1) == sqrt_coefficient
    assert sqrt_coefficient.is_even is True
    assert all(coefficient % 2 == 0 for coefficient in sp.Poly(sqrt_coefficient, *a, *b).coeffs())
    assert sp.Poly(2 + s, s).nth(1) == 1  # Odd: impossible for every x in O.
    # Even with the correct norm ideal, x=1 has normalized trace 4, not d=2.
    assert sp.expand(1 / q - inverse).simplify() == 0
    assert sp.simplify(inverse + q) == 4 > 2


@pytest.mark.parametrize("k", (3, 4, 5))
def test_bounded_two_power_real_cyclotomic_basis_has_trace_image_degree_times_z(k):
    """Check supplied basis traces, not the general integral-basis theorem."""
    z = sp.Symbol("z")
    degree = 2 ** (k - 2)
    cyclotomic = sp.Poly(z ** (2 * degree) + 1, z, domain=sp.QQ)
    assert cyclotomic == sp.Poly(sp.cyclotomic_poly(2**k, z), z, domain=sp.QQ)
    # z^(-j) = -z^(2*d-j) modulo Phi_(2^k).
    basis = (sp.Poly(1, z, domain=sp.QQ),) + tuple(
        sp.Poly(z**j - z ** (2 * degree - j), z, domain=sp.QQ)
        for j in range(1, degree)
    )
    assert sp.Matrix([[p.nth(i) for p in basis] for i in range(degree)]) == sp.eye(degree)

    def coordinates(value):
        remainder = value.rem(cyclotomic)
        result = tuple(remainder.nth(i) for i in range(degree))
        reconstructed = sum((c * p for c, p in zip(result, basis)), sp.Poly(0, z, domain=sp.QQ))
        assert reconstructed == remainder
        assert _integral(result)
        return sp.Matrix(result)

    multiplication = [
        sp.Matrix.hstack(*(coordinates(p * other) for other in basis))
        for p in basis
    ]
    assert [matrix.trace() for matrix in multiplication] == [degree] + [0] * (degree - 1)
    trace_gram = sp.Matrix(
        [[(left * right).trace() for right in multiplication] for left in multiplication]
    )
    assert trace_gram == sp.diag(degree, *([2 * degree] * (degree - 1)))
    coefficients = sp.symbols(f"c0:{degree}", integer=True)
    general_trace = sum(c * matrix.trace() for c, matrix in zip(coefficients, multiplication))
    assert general_trace == degree * coefficients[0]
    # With the supplied O_F-basis premise, the trace image is exactly d*Z.
    # Positivity + trace equality rigidity then exclude traces between d and
    # 2*d for non-target normalized norms. No new SVP procedure is tested.


@pytest.mark.parametrize("k", (3, 4, 5))
def test_natural_cyclotomic_quaternion_order_has_correct_target_gram_scale(k):
    """Use the CM field trace, independently of the real-basis trace test."""
    d = 2 ** (k - 2)
    degree = 2 * d
    companion = sp.zeros(degree)
    for j in range(degree - 1):
        companion[j + 1, j] = 1
    companion[0, degree - 1] = -1
    assert companion**degree == -sp.eye(degree)
    powers = [companion**j for j in range(degree)]
    # Tr_F(N_L/F(x)) = Tr_L(x*conjugate(x))/2, not Tr_L itself.
    gram_l = sp.Matrix([
        [(left * right.inv()).trace() / 2 for right in powers]
        for left in powers
    ])
    assert gram_l == d * sp.eye(2 * d)
    gram = sp.diag(gram_l, gram_l)
    assert gram == d * sp.eye(4 * d)
    # Delta^(1/(4*d))/sqrt(d)=1, checked without floating roots.
    assert gram.det() == d ** (4 * d)
    one = sp.eye(4 * d)[:, 0]
    one_plus_u = one + sp.eye(4 * d)[:, 2 * d]
    assert (one.T * gram * one)[0] == d
    assert (one_plus_u.T * gram * one_plus_u)[0] == 2 * d
    # nrd(1+u)=2 for u^2=-1: sqrt(2) length is an inclusive off-target.
    assert ((one_plus_u.T * gram * one_plus_u)[0] / d) == 2
