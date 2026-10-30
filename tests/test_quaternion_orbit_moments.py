"""Bounded classical moment controls, not a moment-access or PIP algorithm.

Conventions: Hamilton coordinates are [1, i, j, k], ideals are LEFT ideals
I = O*alpha, and R(a) acts on column vectors by RIGHT multiplication by a.
For nrd(alpha) = q, normalize embedding sigma by sqrt(sigma(q)). Then
L_I = R L_O for R = blockdiag(R(a_sigma)), with ||a_sigma|| = 1.
At matching Gaussian widths the covariance blocks therefore obey

    C_I[sigma,tau] R(a_tau) = R(a_sigma) C_O[sigma,tau].

These equations are linear in the 4*d quaternion coordinates; their rank,
cross-block information, conditioning and moment evaluation are NOT promised.

Our discrete-Gaussian PROBABILITY convention is
    Pr[X=x] = exp(-pi*||x||^2/s^2) / sum_y exp(-pi*||y||^2/s^2).
In particular D_{Z,s} uses exp(-pi*n^2/s^2), not a wavefunction amplitude.
For a lattice basis with Gram d*I, its integer coefficients have width
s/sqrt(d). Independent identical even coefficient laws give the cumulant
identities below; discrete Gaussians are one such law.

The exact algebra tests assume supplied moments. They do not implement
efficient narrow Gaussian sampling, theta evaluation, numerical lattice
reconstruction, or a generic quaternion backend. A coherent grid-comb state
requires its actual position/momentum marginal, or a bounded approximation
error, before these discrete-Gaussian numbers can be substituted. Nearly
Gaussian low moments imply neither state isotropy nor loss of fine coherence.
"""

from itertools import combinations

import mpmath as mp
import sympy as sp


ALPHA = sp.Matrix([1, 2, 3, 4])
Q = 30


def _right_matrix(a):
    """Only the four-dimensional Hamilton multiplication identity."""
    w, x, y, z = a
    return sp.Matrix([
        [w, -x, -y, -z],
        [x, w, z, -y],
        [y, -z, w, x],
        [z, y, -x, w],
    ])


RIGHT_ALPHA = _right_matrix(ALPHA)
ROTATION = RIGHT_ALPHA / sp.sqrt(Q)

# Natural order Q(zeta_8) + Q(zeta_8)*j over F=Q(sqrt(2)), d=2.
# Columns are 1,zeta,zeta^2,zeta^3 and those same elements times j.
_HALF_ROOT = sp.sqrt(2) / 2
_PLUS = sp.Matrix([[1, _HALF_ROOT, 0, -_HALF_ROOT],
                   [0, _HALF_ROOT, 1, _HALF_ROOT]])
_MINUS = sp.Matrix([[1, -_HALF_ROOT, 0, _HALF_ROOT],
                    [0, _HALF_ROOT, -1, _HALF_ROOT]])
PLUS_BLOCK = sp.diag(_PLUS, _PLUS)
NATURAL_D2_BASIS = PLUS_BLOCK.col_join(sp.diag(_MINUS, _MINUS))


def _projected_axis_polynomial(v, degree):
    """Single-block cumulant polynomial with its common scalar removed."""
    return sp.expand(sum(v.dot(PLUS_BLOCK[:, j])**degree for j in range(PLUS_BLOCK.cols)))


def test_exact_alpha_normalized_isometry_and_scalar_covariance():
    # Keep all four columns: they represent 1*alpha, i*alpha, j*alpha, k*alpha.
    assert RIGHT_ALPHA == sp.Matrix([
        [1, -2, -3, -4],
        [2, 1, 4, -3],
        [3, -4, 1, 2],
        [4, 3, -2, 1],
    ])
    assert RIGHT_ALPHA[:, 0] == ALPHA
    assert ALPHA.dot(ALPHA) == Q
    assert RIGHT_ALPHA.T * RIGHT_ALPHA == Q * sp.eye(4)
    assert RIGHT_ALPHA.det() == Q**2
    assert ROTATION.T * ROTATION == sp.eye(4)
    assert ROTATION.det() == 1

    variance = sp.symbols("variance", positive=True)
    reference_covariance = variance * sp.eye(4)
    observed_covariance = ROTATION * reference_covariance * ROTATION.T
    assert observed_covariance == reference_covariance
    assert observed_covariance * ROTATION == ROTATION * reference_covariance


def test_exact_fourth_cumulant_contraction_diagonalizes_generator_axes():
    t = sp.Matrix(sp.symbols("t0:4", real=True))
    mu2, mu4 = sp.symbols("mu2 mu4", real=True)
    linear_forms = list(ROTATION.T * t)
    axis_quartic = sp.expand(sum(form**4 for form in linear_forms))
    raw_fourth = mu4 * sum(form**4 for form in linear_forms)
    raw_fourth += 6 * mu2**2 * sum(
        linear_forms[i]**2 * linear_forms[j]**2
        for i, j in combinations(range(4), 2)
    )
    fourth_cumulant = sp.expand(raw_fourth - 3 * mu2**2 * t.dot(t)**2)
    assert sp.expand(fourth_cumulant - (mu4 - 3*mu2**2)*axis_quartic) == 0

    # Divide by the NONZERO scalar kappa4 before forming this contraction.
    probe = sp.Matrix([1, 2, 4, 8])
    contraction = sp.hessian(axis_quartic, t).subs(dict(zip(t, probe))) / 12
    expected_eigenvalues = [sp.Rational(n, 30) for n in (2401, 64, 49, 36)]
    assert ROTATION.T * contraction * ROTATION == sp.diag(*expected_eigenvalues)

    eigenvectors, diagonal = contraction.diagonalize()
    assert contraction * eigenvectors == eigenvectors * diagonal
    assert set(diagonal.diagonal()) == set(expected_eigenvalues)
    assert len(set(diagonal.diagonal())) == 4
    ideal_inverse = RIGHT_ALPHA.inv()
    for eigenvector in eigenvectors.columnspace():
        coordinates = ideal_inverse * eigenvector
        support = [i for i, value in enumerate(coordinates) if value != 0]
        assert len(support) == 1
        index = support[0]
        recovered = eigenvector / coordinates[index]
        assert recovered == RIGHT_ALPHA[:, index]
        assert recovered.dot(recovered) == Q
        assert ideal_inverse * recovered == sp.eye(4)[:, index]

    # At kappa4=0 the entire contraction vanishes, so this attack has no axes.
    assert fourth_cumulant.subs(mu4, 3*mu2**2) == 0


def test_natural_d2_low_degree_block_cumulants_leave_continuous_phase():
    assert NATURAL_D2_BASIS.T * NATURAL_D2_BASIS == 2 * sp.eye(8)
    v = sp.Matrix(sp.symbols("x0:4", real=True))
    c, s = sp.symbols("c s", real=True)
    phase = _right_matrix([c, s, 0, 0])
    assert phase.T * phase == (c*c + s*s) * sp.eye(4)
    rotated = phase.T * v
    r1, r2 = v[0]**2 + v[1]**2, v[2]**2 + v[3]**2

    # Cumulants add over independent coefficients. Their common scalar can
    # depend on width; odd cumulants vanish for an even coefficient law.
    for degree, scale in ((2, 2), (4, sp.Rational(3, 2)), (6, sp.Rational(5, 4))):
        polynomial = _projected_axis_polynomial(v, degree)
        expected = scale * (r1**(degree//2) + r2**(degree//2))
        assert sp.expand(polynomial - expected) == 0
        assert sp.expand(
            _projected_axis_polynomial(rotated, degree)
            - (c*c + s*s)**(degree//2) * polynomial
        ) == 0
    # Thus every c^2+s^2=1 preserves moments through degree six as well,
    # since those moments are polynomials in the corresponding cumulants.


def test_natural_d2_eighth_degree_detects_the_missing_block_phase():
    v = sp.Matrix(sp.symbols("x0:4", real=True))
    r1, r2 = v[0]**2 + v[1]**2, v[2]**2 + v[3]**2
    angular = sp.re((v[0] + sp.I*v[1])**8).expand()
    angular += sp.re((v[2] + sp.I*v[3])**8).expand()
    polynomial = _projected_axis_polynomial(v, 8)
    assert sp.expand(polynomial - sp.Rational(35, 32)*(r1**4 + r2**4) - angular/32) == 0

    # Right multiplication by exp(i*pi/8) preserves the lower moments but
    # changes this axis polynomial. Information requires nonzero kappa8.
    c = sp.sqrt(2 + sp.sqrt(2)) / 2
    s = sp.sqrt(2 - sp.sqrt(2)) / 2
    phase = _right_matrix([c, s, 0, 0])
    e0 = sp.eye(4)[:, 0]
    assert sp.simplify(c*c + s*s) == 1
    assert _projected_axis_polynomial(e0, 8) == sp.Rational(9, 8)
    assert sp.simplify(_projected_axis_polynomial(phase.T*e0, 8)) == sp.Rational(17, 16)


def test_broad_discrete_gaussian_small_cumulant_but_exact_periodic_character():
    # The character identity is literal and exact on ALL integers, not a
    # floating-point evaluation at an approximately integral frequency.
    n = sp.symbols("n", integer=True)
    assert sp.exp(2*sp.pi*sp.I*n) == 1

    with mp.workdps(100):
        width = mp.mpf(4)
        cutoff = 32
        weights = [mp.exp(-mp.pi * k*k / width**2) for k in range(-cutoff, cutoff + 1)]
        sums = {
            power: mp.fsum(mp.mpf(k)**power * weight for k, weight in zip(range(-cutoff, cutoff + 1), weights))
            for power in (0, 2, 4)
        }

        # Beyond N, successive k^p*exp(-pi*k^2/s^2) ratios decrease.
        # These geometric majorants bound both omitted tails analytically;
        # mpmath evaluation is numerical, not an interval-arithmetic proof.
        first = mp.mpf(cutoff + 1)
        tails = {}
        for power in (0, 2, 4):
            ratio = ((first + 1)/first)**power * mp.exp(-mp.pi*(2*first + 1)/width**2)
            assert 0 < ratio < 1
            tails[power] = 2 * first**power * mp.exp(-mp.pi*first**2/width**2) / (1 - ratio)
        assert tails[4] < mp.mpf("1e-85")

        lower = {power: sums[power]/(sums[0] + tails[0]) for power in (2, 4)}
        upper = {power: (sums[power] + tails[power])/sums[0] for power in (2, 4)}
        kappa_lower = lower[4] - 3*upper[2]**2
        kappa_upper = upper[4] - 3*lower[2]**2
        assert mp.mpf("1.93e-17") < kappa_lower <= kappa_upper < mp.mpf("1.95e-17")
        assert kappa_upper - kappa_lower < mp.mpf("1e-84")
        assert mp.mpf("2.98e-18") < kappa_lower/upper[2]**2
        assert kappa_upper/lower[2]**2 < mp.mpf("3.00e-18")

        # A centered continuous Gaussian of the same variance has a tiny
        # character at 2*pi, whereas the integer-supported law has value 1.
        gaussian_character = mp.exp(-2*mp.pi**2*lower[2])
        assert mp.mpf("1.4e-22") < gaussian_character < mp.mpf("1.5e-22")
