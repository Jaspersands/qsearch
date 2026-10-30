"""Finite exact controls for left ideals in B = (-1, -11) over Q.

Coordinates always refer to O = Z[1, i, (1+j)/2, (i+k)/2], k = ij.
Lattice matrices have basis vectors as columns. These self-contained fixtures
are not a generic PIP backend, a completeness/performance proof for one, or a
cryptographic-hardness claim. Rational definite quaternion PIP is a fixed-4D
classical lattice problem, where fixed-dimensional shortest-vector methods
apply. An expanded-height enumeration bound is not a binary-time bound.
"""

from fractions import Fraction
from itertools import product
from math import gcd, isqrt

import numpy as np
import pytest
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form


ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)
I = (0, 1, 0, 0)
H = (0, 0, 1, 0)
IH = (0, 0, 0, 1)
ORDER_BASIS = (ONE, I, H, IH)
ALPHA = (1, 1, 0, 0)
NO_BASIS = sp.Matrix(
    [[2, 0, 0, 1], [0, 2, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
)
YES_HNF = sp.Matrix(
    [[2, 1, 0, 1], [0, 1, 0, 0], [0, 0, 2, 1], [0, 0, 0, 1]]
)
RATIONAL_FIXTURES = (
    ZERO,
    ONE,
    I,
    H,
    IH,
    ALPHA,
    (-2, 3, 1, -1),
    (Fraction(1, 2), Fraction(-2, 3), Fraction(3, 5), Fraction(-4, 7)),
)


def _standard(q):
    a, b, c, d = map(Fraction, q)
    return a + c / 2, b + d / 2, c / 2, d / 2


def _order(q):
    w, x, y, z = map(Fraction, q)
    return w - y, x - z, 2 * y, 2 * z


def _mul(q, r):
    """Multiply in [1,i,j,k] first, independently of the order norm form."""
    w, x, y, z = _standard(q)
    W, X, Y, Z = _standard(r)
    return _order(
        (
            w * W - x * X - 11 * y * Y - 11 * z * Z,
            w * X + x * W + 11 * (y * Z - z * Y),
            w * Y + y * W + z * X - x * Z,
            w * Z + z * W + x * Y - y * X,
        )
    )


def _conjugate(q):
    a, b, c, d = q
    return a + c, -b, -c, -d


def _trace(q):
    return 2 * q[0] + q[2]


def _norm(q):
    a, b, c, d = q
    return a * a + a * c + 3 * c * c + b * b + b * d + 3 * d * d


def _multiplication_matrix(q, side):
    if side == "left":
        columns = [_mul(q, e) for e in ORDER_BASIS]
    elif side == "right":
        columns = [_mul(e, q) for e in ORDER_BASIS]
    else:
        raise ValueError("side must be left or right")
    return sp.Matrix.hstack(*(sp.Matrix(v) for v in columns))


def _integral(values):
    return all(sp.sympify(x).is_Integer is True for x in values)


def _in_no(q):
    a, b, c, d = q
    return _integral(q) and (a + d) % 2 == 0 and (b + c) % 2 == 0


def test_presentation_and_order_coordinate_conventions():
    j, k = (-1, 0, 2, 0), (0, -1, 0, 2)
    assert _standard(H) == (Fraction(1, 2), 0, Fraction(1, 2), 0)
    assert _standard(IH) == (0, Fraction(1, 2), 0, Fraction(1, 2))
    assert _standard(j) == (0, 0, 1, 0)
    assert _standard(k) == (0, 0, 0, 1)
    assert _mul(I, I) == (-1, 0, 0, 0)
    assert _mul(j, j) == (-11, 0, 0, 0)
    assert _mul(I, j) == k
    assert _mul(j, I) == tuple(-x for x in k)
    assert _mul(k, k) == (-11, 0, 0, 0)
    assert _mul(I, H) == IH
    for q in RATIONAL_FIXTURES:
        assert _order(_standard(q)) == q
        assert _mul(ONE, q) == _mul(q, ONE) == q


def test_order_closure_conjugation_and_associativity_on_basis():
    assert _mul(H, H) == (-3, 0, 1, 0)
    assert _mul(H, I) == (0, 1, 0, -1)
    for q, r in product(ORDER_BASIS, repeat=2):
        assert _integral(_mul(q, r))
    for q in ORDER_BASIS:
        assert _integral(_conjugate(q))
    # Bilinearity makes basis closure and basis associativity exact certificates.
    for q, r, s in product(ORDER_BASIS, repeat=3):
        assert _mul(_mul(q, r), s) == _mul(q, _mul(r, s))


@pytest.mark.parametrize("q", RATIONAL_FIXTURES)
def test_exact_rational_norm_trace_and_multiplication_determinants(q):
    norm = _norm(q)
    w, x, y, z = _standard(q)
    assert norm == w * w + x * x + 11 * y * y + 11 * z * z
    assert _trace(q) == 2 * w
    assert _conjugate(_conjugate(q)) == q
    assert _mul(q, _conjugate(q)) == _mul(_conjugate(q), q) == (norm, 0, 0, 0)
    assert _multiplication_matrix(q, "left").det() == norm**2
    assert _multiplication_matrix(q, "right").det() == norm**2
    for r in RATIONAL_FIXTURES:
        assert _norm(_mul(q, r)) == norm * _norm(r)
        assert _conjugate(_mul(q, r)) == _mul(_conjugate(r), _conjugate(q))


def test_multiplication_determinants_as_exact_polynomial_identities():
    q = sp.symbols("a b c d")
    for side in ("left", "right"):
        matrix = sp.zeros(4)
        for coefficient, e in zip(q, ORDER_BASIS):
            matrix += coefficient * _multiplication_matrix(e, side)
        assert sp.expand(matrix.det() - _norm(q) ** 2) == 0


def test_trace_gram_discriminant_and_sign_convention():
    gram = sp.Matrix(
        [[_trace(_mul(q, _conjugate(r))) for r in ORDER_BASIS] for q in ORDER_BASIS]
    )
    assert gram == sp.Matrix(
        [[2, 0, 1, 0], [0, 2, 0, 1], [1, 0, 6, 0], [0, 1, 0, 6]]
    )
    assert gram.det() == 11**2
    assert [gram[:n, :n].det() for n in range(1, 5)] == [2, 4, 22, 121]
    q = sp.Matrix(sp.symbols("a b c d"))
    assert sp.expand((q.T * gram * q)[0] - 2 * _norm(q)) == 0
    raw_trace_gram = sp.Matrix(
        [[_trace(_mul(q, r)) for r in ORDER_BASIS] for q in ORDER_BASIS]
    )
    # The un-conjugated reduced-trace pairing has the opposite sign.
    assert raw_trace_gram.det() == -(11**2)


def test_positive_norm_form_square_completion_and_coordinate_bound():
    a, b, c, d = q = sp.symbols("a b c d")
    completed = (a + c / 2) ** 2 + (b + d / 2) ** 2 + sp.Rational(11, 4) * (c * c + d * d)
    assert sp.expand(_norm(q) - completed) == 0
    remainder = ((a + c) ** 2 + (b + d) ** 2) / 2 + 2 * (c * c + d * d)
    assert sp.expand(_norm(q) - sum(x * x for x in q) / 2 - remainder) == 0
    for q in product(range(-2, 3), repeat=4):
        assert 4 * _norm(q) >= 11 * (q[2] ** 2 + q[3] ** 2)
        assert 2 * _norm(q) >= sum(x * x for x in q)
        assert (_norm(q) == 0) == (q == ZERO)


def test_yes_left_ideal_hnf_index_and_norm_two_generator():
    # O*alpha is the image of RIGHT multiplication, not left multiplication.
    basis = _multiplication_matrix(ALPHA, "right")
    assert basis == sp.Matrix(
        [[1, -1, 0, -1], [1, 1, 1, 0], [0, 0, 1, 1], [0, 0, -1, 1]]
    )
    assert _norm(ALPHA) == 2
    assert basis.det() == YES_HNF.det() == 4
    assert hermite_normal_form(basis) == YES_HNF
    change = basis.inv() * YES_HNF
    assert _integral(change) and abs(change.det()) == 1
    assert _integral(YES_HNF.inv() * sp.Matrix(ALPHA))
    for e in ORDER_BASIS:
        assert _integral(YES_HNF.inv() * _multiplication_matrix(e, "left") * YES_HNF)
    assert hermite_normal_form(_multiplication_matrix(ALPHA, "left")) != YES_HNF


def test_no_basis_is_exactly_the_parity_lattice_of_index_four():
    assert tuple(tuple(NO_BASIS[:, i]) for i in range(4)) == (
        (2, 0, 0, 0), (0, 2, 0, 0), (0, 1, 1, 0), (1, 0, 0, 1)
    )
    assert NO_BASIS.det() == 4
    assert hermite_normal_form(NO_BASIS) == NO_BASIS
    a, b, c, d = sp.symbols("a b c d")
    coefficients = sp.Matrix([(a - d) / 2, (b - c) / 2, c, d])
    assert NO_BASIS * coefficients == sp.Matrix([a, b, c, d])
    # These inverse coordinates characterize membership for all integral q.
    for q in product(range(-2, 3), repeat=4):
        a, b, c, d = q
        inverse_coordinates = (Fraction(a - d, 2), Fraction(b - c, 2), c, d)
        assert _in_no(q) == _integral(inverse_coordinates)


def test_no_is_left_stable_exactly_but_not_assumed_two_sided():
    inverse = NO_BASIS.inv()
    for e in ORDER_BASIS:
        action = _multiplication_matrix(e, "left")
        coefficients = inverse * action * NO_BASIS
        assert _integral(coefficients)
        assert NO_BASIS * coefficients == action * NO_BASIS
        for col in range(4):
            assert _in_no(_mul(e, tuple(NO_BASIS[:, col])))
    assert any(
        not _integral(inverse * _multiplication_matrix(e, "right") * NO_BASIS)
        for e in ORDER_BASIS
    )


def test_norm_two_is_impossible_in_no_by_complete_bound_and_parity():
    # Completion of squares gives 11*(c^2+d^2) <= 8 at norm 2,
    # hence c=d=0 globally, not merely inside a sampled search window.
    assert (4 * 2) // 11 == 0
    norm_two = {
        (a, b, 0, 0)
        for a, b in product(range(-isqrt(2), isqrt(2) + 1), repeat=2)
        if a * a + b * b == 2
    }
    assert norm_two == {(a, b, 0, 0) for a, b in product((-1, 1), repeat=2)}
    assert all(_norm(q) == 2 for q in norm_two)
    assert all(q[0] % 2 == q[1] % 2 == 1 for q in norm_two)
    assert all(not _in_no(q) for q in norm_two)
    assert ALPHA in norm_two


def test_no_minimum_four_and_norm_ideal_two_are_different_invariants():
    r, s, t, u = sp.symbols("r s t u")
    restricted_norm = sp.Poly(_norm(NO_BASIS * sp.Matrix([r, s, t, u])), r, s, t, u)
    # Even polynomial coefficients certify even norms on the entire lattice.
    assert all(int(coefficient) % 2 == 0 for coefficient in restricted_norm.coeffs())
    witnesses = ((2, 0, 0, 0), (-1, -1, 1, 1))
    assert all(_in_no(q) for q in witnesses)
    assert tuple(_norm(q) for q in witnesses) == (4, 6)
    assert gcd(*(_norm(q) for q in witnesses)) == 2
    # Positivity + evenness + no norm 2 leaves minimum 4, attained by 2 in I.
    # Independently enumerate ALL vectors of norm <= 6 using 2*nrd >= ||q||^2.
    bound = isqrt(2 * 6)
    small_norms = [
        _norm(q)
        for q in product(range(-bound, bound + 1), repeat=4)
        if q != ZERO and _in_no(q) and _norm(q) <= 6
    ]
    assert set(small_norms) == {4, 6}
    assert min(small_norms) == 4
    assert gcd(*small_norms) == 2


def test_same_index_yes_and_no_do_not_turn_norm_ideal_into_a_generator():
    assert YES_HNF.det() == NO_BASIS.det() == 4
    assert YES_HNF != NO_BASIS
    assert _norm(ALPHA) == isqrt(int(NO_BASIS.det())) == 2
    assert _integral(YES_HNF.inv() * sp.Matrix(ALPHA))
    assert not _in_no(ALPHA)
    # If NO = O*gamma, then gamma lies in NO since 1 lies in O, and
    # [O:NO] = nrd(gamma)^2 forces nrd(gamma)=2 by definiteness.
    # The complete norm-2 exclusion above therefore rules out principality.
    # Its norm ideal is still 2Z; an index or norm-ideal match is not a witness.
    for a, b in product((-1, 1), repeat=2):
        gamma = (a, b, 0, 0)
        assert _norm(gamma) ** 2 == NO_BASIS.det()
        assert not _in_no(gamma)
        assert hermite_normal_form(_multiplication_matrix(gamma, "right")) != NO_BASIS


def test_fixed_quadratic_slice_misses_every_norm_two_generator_of_yes():
    """A fixed slice is not an exact-generator guarantee, nor an HSVP result.

    K=Q(j) has O_K=Z+Z*h here. This control says nothing about adaptive
    quadratic-field selection or any approximation guarantee.
    """
    j = (-1, 0, 2, 0)
    commutator = _multiplication_matrix(j, "left") - _multiplication_matrix(j, "right")
    assert commutator.nullspace() == [sp.Matrix(ONE), sp.Matrix(H)]
    a, c = sp.symbols("a c", integer=True)
    slice_vector = sp.Matrix([a, 0, c, 0])
    inverse_coordinates = YES_HNF.inv() * slice_vector
    assert inverse_coordinates == sp.Matrix([a / 2, 0, c / 2, 0])
    # Integral inverse coordinates iff a,c are even: I intersect K = 2*O_K.
    u, v = sp.symbols("u v", integer=True)
    intersection_vector = sp.Matrix([2 * u, 0, 2 * v, 0])
    assert YES_HNF * sp.Matrix([u, 0, v, 0]) == intersection_vector
    slice_norm = _norm(intersection_vector)
    assert sp.expand(slice_norm - 4 * (u * u + u * v + 3 * v * v)) == 0
    assert sp.expand(slice_norm - ((2 * u + v) ** 2 + 11 * v * v)) == 0
    # If v!=0 the norm is >=11; if v=0 and u!=0 it is 4*u^2>=4.
    assert _norm((2, 0, 0, 0)) == 4
    assert min(
        _norm((2 * u, 0, 2 * v, 0))
        for u, v in product(range(-2, 3), repeat=2) if (u, v) != (0, 0)
    ) == 4
    # Nonzero O*alpha norms are 2*nrd(y)>=2, attained by alpha itself.
    assert _norm(ALPHA) == 2
    assert 4 * 2 < 11  # The completed-square bound forces c=d=0 at norm 2.
    norm_two_vectors = {(a, b, 0, 0) for a, b in product((-1, 1), repeat=2)}
    for vector in norm_two_vectors:
        assert _norm(vector) == 2
        assert _integral(YES_HNF.inv() * sp.Matrix(vector))
        assert vector[1] != 0  # K requires b=d=0.


@pytest.mark.parametrize(
    "change",
    (
        sp.eye(4),
        sp.Matrix([[1, 5, -2, 0], [0, 1, 3, -1], [0, 0, 1, 4], [0, 0, 0, 1]]),
        sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]),
    ),
    ids=("original", "integral-shear", "signed-permutation"),
)
def test_bounded_principal_fixtures_and_expanded_height_bound(change):
    """Check known witnesses under basis changes; do not pretend to solve PIP.

    For an integral ideal basis A of entry height H >= 1, Hadamard gives
    D=abs(det A) <= 16*H^4. A principal generator has N^2=D, so N<=4*H^2.
    Since ||gamma||^2 <= 2*N, each order coordinate has abs value <= 3*H.
    Thus (6*H+1)^4 order-coordinate candidates suffice in expanded height.
    Cofactors are <=6*H^3, so integral A-coordinates of a generator are
    bounded by 72*H^4/D <= 72*H^4. Neither bound is polynomial in log H.
    """
    assert _integral(change) and abs(change.det()) == 1
    for gamma in product(range(-1, 2), repeat=4):
        if gamma == ZERO:
            continue
        original = _multiplication_matrix(gamma, "right")
        canonical = hermite_normal_form(original)
        for basis in (original * change, canonical * change):
            assert _integral(basis)
            assert hermite_normal_form(basis) == canonical
            height = max(abs(int(x)) for x in basis)
            determinant = abs(basis.det())
            norm = _norm(gamma)
            assert height >= 1 and determinant == norm**2
            assert determinant <= 16 * height**4
            assert norm <= 4 * height**2
            assert sum(x * x for x in gamma) <= 2 * norm <= 8 * height**2
            assert max(abs(x) for x in gamma) <= 3 * height
            adjugate = basis.adjugate()
            assert max(abs(x) for x in adjugate) <= 6 * height**3
            coefficients = basis.inv() * sp.Matrix(gamma)
            assert _integral(coefficients)
            assert basis * coefficients == sp.Matrix(gamma)
            assert max(abs(x) for x in coefficients) * determinant <= 72 * height**4


def test_cyclotomic_order_bound_has_no_small_prime_exception():
    # The SU(2) classification is external. Check its elementary numerical
    # ingredient, including M=1,2 and the exceptional 1/2 factor at 2.
    for order in range(1, 513):
        phi = int(sp.totient(order))
        factors = sp.factorint(order)
        ratio = sp.prod(sp.Rational(prime)**(power-2)*(prime-1)**2
                        for prime, power in factors.items())
        assert ratio == sp.Rational(phi**2, order)
        assert ratio >= sp.Rational(1, 2)
        assert order <= 2*phi**2


def test_direct_quotient_full_fourier_marginal_retains_abort_and_norm_units():
    units = [q for q in product(range(-1, 2), repeat=4) if _norm(q) == 1]
    assert set(units) == {ONE, I, tuple(-x for x in ONE), tuple(-x for x in I)}
    good = {_mul(unit, ALPHA) for unit in units}
    for gamma in good:
        assert _norm(gamma) == 2
        assert hermite_normal_form(_multiplication_matrix(gamma, "right")) == YES_HNF
    xs = [ZERO, ONE, I, H]
    px = [Fraction(i, 10) for i in (1, 2, 3, 4)]
    ys = [_mul(z, ALPHA) for z in (ZERO, ONE, I, H, tuple(-x for x in ONE))]
    py = {y: Fraction(i+1, 15) for i, y in enumerate(ys)}
    fibers = {}
    for index, x in enumerate(xs):
        if x == ZERO:
            continue
        inverse = tuple(Fraction(v, _norm(x)) for v in _conjugate(x))
        for y in ys:
            gamma = _mul(inverse, y)
            assert _mul(x, gamma) == y
            vector = fibers.setdefault(gamma, np.zeros(len(xs)))
            vector[index] = np.sqrt(float(px[index]*py[y]))
    marginal = {}
    for gamma, vector in fibers.items():
        output = np.fft.fft(vector, norm="ortho")
        marginal[gamma] = float(np.vdot(output, output).real)
        assert marginal[gamma] == pytest.approx(float(np.vdot(vector, vector)), abs=1e-14)
    exact_good = sum(px[i]*sum(py.get(_mul(x, gamma), 0) for gamma in good)
                     for i, x in enumerate(xs) if x != ZERO)
    assert sum(marginal.values()) == pytest.approx(float(1-px[0]), abs=1e-14)
    assert sum(value for gamma, value in marginal.items() if gamma in good) == pytest.approx(float(exact_good))
    assert exact_good <= len(units)*max(py.values())


def test_source_error_must_be_paid_before_claiming_tiny_quotient_success():
    # A hypothetical perturbation that moves tau mass to a good record
    # saturates the TV correction. Tiny ideal success alone is not enough.
    ideal, tau = Fraction(1, 2**80), Fraction(1, 100)
    actual = ideal+tau
    assert abs(actual-ideal) == tau
    assert actual > 10**20*ideal
