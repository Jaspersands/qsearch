"""Exact controls for packet-matched oscillator parity, not a receiver backend.

Use the ACTUAL positive comb w_x=exp(-pi*|x|^2/s^2), x in L=M Z^N,
with packet amplitude nu^(-N/2) exp(-pi*|u-x|^2/(2nu^2)). Set the
oscillator length ell=nu/sqrt(pi), so alpha_x=sqrt(pi/2)*x/nu is real.
The vacuum-fixing passive representation Gamma(V)|alpha>=|V alpha>
then gives, for P=V^dagger diag(+/-1) V and c=pi/(4nu^2),

  K_P(y,x)=<alpha_y|Gamma(P)|alpha_x>
          =exp(-c*(|x|^2+|y|^2-2*y^T*P*x)),
  E_P=sum_xy w_y*w_x*K_P(y,x) / S,
  S=sum_xy w_y*w_x*K_I(y,x), Z=sum_x w_x^2,
  1 <= S/Z <= rho_(2nu)(L) = 1+eta.

All cross terms and the physical normalizer S are retained. If P=A+iB,
the kernel has magnitude exp(-c*(|y-Ax|^2+|Bx|^2)) and phase
2*c*y^T*B*x. Real P is an orthogonal coordinate reflection; nonreal P
acts on phase space by [[A,-B],[B,A]], not on position alone. Selecting
conjugate circular modes in pairs can give real P. Selecting all modes
gives P=-I and E_P=1 since L=-L. For m measured parities z_j, the joint
law is 2^(-m)*sum_T prod_(j in T) z_j E_(P_T). Efficient evaluation of
each specified moment does NOT supply an efficient sampler of this law.

One-neighbor control (assume the supplied broad coefficient sampler):
sample X with law w_x^2/Z and retain |X|<=R. Round M^-1*A*X to find Y.
An approximate rounding accurate to 1/8 in coefficient infinity norm
finds every candidate within r<=1/(8*||M^-1||). Omitted points have
distance >=r. For a=pi*r^2/(4nu^2), packing gives their kernel sum
<=2*exp(-a+N*log(3)), provided a-N*log(3)>=log(2). Multiplying by
exp(pi*R^2/s^2) bounds the omitted weighted sum. Completing the square
gives the uniform bound, even if the rounded point is far away,

  |(w_y/w_x)*K_P(y,x)|
    <= exp(4*pi*nu^2*|x|^2/(s^2*(s^2+4nu^2))).

If this is <=2 for |x|<=R, sample-average its real part, zero outside R.
For coefficient tail mass tau, the expectation error is at most
eta+(1+eta)*sqrt(tau)+epsilon when
a>=N*log(3)+pi*R^2/s^2+log(2/epsilon). The tail term follows from
||T^dagger Gamma(P) T||<=||T||^2<=1+eta for packet synthesis T.

A bounded alternative avoids R: let t(x) be the deterministic rounding
map on ALL lattice labels and retain only pairs y=t(x), t(y)=x, including
fixed points. Use the same precision algorithm for both calls. These
form a partial involution; this step requires Hermitian P, not merely a
general passive unitary. The two-cycle calculation is checked below.
Use score 2*w_x*w_y*Re(K_P(y,x))/(w_x^2+w_y^2), or zero without a pair.
Its magnitude is <=1 and its mean is the retained quadratic form / Z.
All omitted pairs have |y-Ax|^2+|Bx|^2>=r^2, with the same conservative
r above, since this distance is symmetric in x,y. Factoring half the
Gaussian and applying the shifted-theta maximum gives uniform row and
column error <=beta=rho_(sqrt(8)*nu)(L)*exp(-pi*r^2/(8nu^2)). The Schur
bound therefore gives |mean(score)-E_P|<=eta+beta. Rounding uses dyadic
approximants with precision chosen from each input's bit length to meet
the same absolute margin; no exact real-floor oracle is assumed.
Bounded scores can also simulate ONE product-parity
bit by a coin with probability (1+score)/2, not the full parity vector.

Both controls assume the oscillator vacuum is precisely phi_nu and that
P has efficiently computable entries. They are not claims about a
mismatched Hermite scale, squeezing, number conditioning, full joint
record sampling, or a finite Hermite-transform circuit. A normalized
finite-source ket error e adds at most 2e for these norm-one observables;
mode-implementation, numerical and sampler errors are separate.

Primary background: Arrazola--Lutkenhaus, PRA 90, 042335 (2014), Sec. II,
https://arxiv.org/abs/1406.7189 (coherent-state passive transformations);
de Gosson, Lett. Math. Phys. 111, 73 (2021), subgroup U(n),
https://pmc.ncbi.nlm.nih.gov/articles/PMC8550114/ (phase-space realification).
The matching/tail argument above is derived here, not attributed to them.

Symbolic tests are exact. Numerical tests use finite sums with explicit
analytic tails and separate roundoff allowances, not interval arithmetic.
They do not assume that a Gaussian COMB is itself a Gaussian state.
"""

from itertools import product

import mpmath as mp
import numpy as np
import sympy as sp


CIRCULAR = sp.Matrix([
    [1, sp.I, 0, 0], [0, 0, 1, sp.I],
    [1, -sp.I, 0, 0], [0, 0, 1, -sp.I],
]) / sp.sqrt(2)


def _right_quaternion(a, b, c, d):
    return sp.Matrix([[a, -b, -c, -d], [b, a, d, -c],
                      [c, -d, a, b], [d, c, -b, a]])


def _theta_window(width, cutoff):
    exponent = mp.pi / width**2
    value = mp.fsum(mp.exp(-exponent*j*j)
                    for j in range(-cutoff, cutoff+1))
    tail = 2*mp.exp(-exponent*(cutoff+1)**2) / (
        1-mp.exp(-exponent*(2*cutoff+3))
    )
    return value, tail


def _theta_excess_upper(width, dimension):
    q = mp.exp(-mp.pi / width**2)
    return mp.expm1(dimension*mp.log1p(2*q/(1-q**3)))


def test_packet_width_and_coherent_displacement_normalization():
    nu = sp.Symbol("nu", positive=True)
    x, y = sp.symbols("x y", real=True)
    ell = nu/sp.sqrt(sp.pi)
    alpha_x, alpha_y = sp.sqrt(sp.pi/2)*x/nu, sp.sqrt(sp.pi/2)*y/nu
    assert sp.simplify(sp.sqrt(2)*ell*alpha_x-x) == 0
    coherent_exponent = -(alpha_x**2+alpha_y**2)/2 + alpha_y*alpha_x
    assert sp.simplify(coherent_exponent+sp.pi*(x-y)**2/(4*nu**2)) == 0
    q = sp.Symbol("q", real=True)
    assert sp.integrate(sp.exp(-sp.pi*q*q/nu**2)/nu,
                        (q, -sp.oo, sp.oo)) == 1


def test_circular_doublets_and_conjugate_pair_selection_are_distinct():
    assert CIRCULAR*CIRCULAR.H == sp.eye(4)
    intertwiner = sp.Matrix([[0, -1], [1, 0]])
    for q in ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)):
        rotation = _right_quaternion(*q)
        transformed = sp.simplify(CIRCULAR*rotation*CIRCULAR.H)
        first = transformed[:2, :2]
        assert transformed == sp.diag(first, sp.conjugate(first))
        assert first.H*first == sp.eye(2) and first.det() == 1
        assert intertwiner*sp.conjugate(first)*intertwiner.H == first

    single = sp.simplify(CIRCULAR.H*sp.diag(-1, 1, 1, 1)*CIRCULAR)
    paired = sp.simplify(CIRCULAR.H*sp.diag(-1, 1, -1, 1)*CIRCULAR)
    assert single == sp.diag(sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.eye(2))
    assert paired == sp.diag(-1, -1, 1, 1)
    assert single.H == single and single*single == sp.eye(4)
    assert sp.re(single).det() == 0  # It is not a real orthogonal action.
    assert paired.T*paired == sp.eye(4)


def test_complex_parity_is_phase_space_and_keeps_kernel_phase():
    parity = sp.Matrix([[0, sp.I], [-sp.I, 0]])
    a, b = sp.re(parity), sp.im(parity)
    phase_space = a.row_join(-b).col_join(b.row_join(a))
    omega = sp.zeros(2).row_join(sp.eye(2)).col_join(
        (-sp.eye(2)).row_join(sp.zeros(2)))
    assert phase_space.T*phase_space == sp.eye(4)
    assert phase_space.T*omega*phase_space == omega
    assert phase_space*phase_space == sp.eye(4)
    assert phase_space[:2, 2:] != sp.zeros(2)

    x, y = sp.Matrix([1, 0]), sp.Matrix([0, 1])
    kernel = sp.exp(-sp.pi*(x.dot(x)+y.dot(y)-2*(y.T*parity*x)[0])/4)
    assert sp.simplify(kernel + sp.I*sp.exp(-sp.pi/2)) == 0
    # Every real-coordinate pullback has a positive real kernel between these
    # positive packets. This imaginary matrix element rules out that identity.
    assert sp.re(kernel) == 0 and sp.im(kernel) != 0


def test_weighted_kernel_complete_square_and_uniform_bound_constants():
    s, nu = sp.symbols("s nu", positive=True)
    xx, yy, y_ax, bx_squared = sp.symbols("xx yy y_ax bx_squared", real=True)
    c, d = sp.pi/(4*nu**2), sp.pi/s**2
    contraction = c/(c+d)
    original = d*(xx-yy)-c*(xx+yy-2*y_ax)
    # |Ax|^2=|x|^2-|Bx|^2; retain the negative B term in the equality.
    completed = -(c+d)*(yy-2*contraction*y_ax+contraction**2*(xx-bx_squared))
    completed += d**2*xx/(c+d)-c**2*bx_squared/(c+d)
    assert sp.simplify(original-completed) == 0
    assert sp.simplify(d**2/(c+d)-4*sp.pi*nu**2/(s**2*(s**2+4*nu**2))) == 0
    assert sp.simplify(c**2/(c+d)-sp.pi*s**2/(4*nu**2*(s**2+4*nu**2))) == 0


def test_shifted_packing_tail_constants_and_rounding_margin():
    # Separation >=8r: a radius-(k+1)r ball has <=((k+5)/4)^N points.
    k = sp.Symbol("k", integer=True, positive=True)
    assert sp.simplify(k+2-(k+5)/4) == 3*(k+1)/4
    # k+2<=3^k<=3^(k^2), by induction, and k^2>=1+3(k-1).
    assert sp.simplify(3*(k+2)-(k+3)) == 2*k+3
    assert sp.factor(k*k-1-3*(k-1)) == (k-2)*(k-1)
    # Thus sum exp(-b*k^2)<=exp(-b)/(1-exp(-3b))<=8/7 exp(-b)
    # for b>=log(2); the claimed factor 2 is conservative.
    assert 1/(1-sp.Rational(1, 2)**3) == sp.Rational(8, 7) < 2
    assert sp.Rational(1, 8)+sp.Rational(1, 8) < sp.Rational(1, 2)

    with mp.workdps(80):
        dimension, r, s, radius = 4, 1/(8*mp.sqrt(5)), mp.mpf(4)/5, 4
        nu, epsilon = mp.mpf(1)/256, mp.mpf("1e-12")
        a = mp.pi*r*r/(4*nu*nu)
        required = dimension*mp.log(3)+mp.pi*radius**2/s**2+mp.log(2/epsilon)
        bound = 2*mp.exp(-a+dimension*mp.log(3)+mp.pi*radius**2/s**2)
        assert a >= required and bound < epsilon
        log_magnitude = 4*mp.pi*nu**2*radius**2/(s**2*(s**2+4*nu**2))
        assert log_magnitude < mp.log(2)


def test_reciprocal_matching_score_and_schur_tail_identity():
    u, v = sp.symbols("u v", positive=True)
    real_kernel = sp.Symbol("real_kernel", real=True)
    score = 2*u*v*real_kernel/(u*u+v*v)
    assert sp.simplify((u*u+v*v)*score-2*u*v*real_kernel) == 0
    assert sp.factor(u*u+v*v-2*u*v) == (u-v)**2
    assert sp.simplify(score.subs(v, u)-real_kernel) == 0

    # For a Hermitian unitary P=A+iB, A is symmetric, B antisymmetric,
    # and A^T A+B^T B=I. The distance below is therefore symmetric.
    t = sp.Symbol("t", real=True)
    ca, sa = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    a, b = sp.diag(ca, -ca), sp.Matrix([[0, sa], [-sa, 0]])
    x, y = sp.Matrix(sp.symbols("x0:2", real=True)), sp.Matrix(sp.symbols("y0:2", real=True))
    distance = (y-a*x).dot(y-a*x)+(b*x).dot(b*x)
    reverse = (x-a*y).dot(x-a*y)+(b*y).dot(b*y)
    assert sp.simplify(distance-reverse) == 0
    assert sp.simplify(distance-x.dot(x)-y.dot(y)+2*(y.T*a*x)[0]) == 0
    # If a pair is discarded its distance >=r. Split exp(-c*distance/2)
    # off, then sum exp(-c*|y-Ax|^2/2) over a shifted lattice. Poisson
    # gives the centered maximum rho_sqrt(8)*nu, for both rows and columns.
    nu, r = sp.symbols("nu r", positive=True)
    c = sp.pi/(4*nu**2)
    assert sp.simplify(c/2-sp.pi/(sp.sqrt(8)*nu)**2) == 0
    assert c*r*r/2 == sp.pi*r*r/(8*nu**2)


def test_reciprocal_matching_requires_hermitian_parity_not_any_passive_unitary():
    cycle = sp.Matrix([[0, 0, 1, 0], [1, 0, 0, 0],
                       [0, 1, 0, 0], [0, 0, 0, 1]])
    assert cycle.T*cycle == sp.eye(4) and cycle.T != cycle
    x = sp.Matrix([1, 0, 0, 0])
    y = cycle*x
    assert (y-cycle*x).dot(y-cycle*x) == 0
    assert (x-cycle*y).dot(x-cycle*y) == 2
    # An exact unit-kernel edge is discarded by the reciprocal test. Thus
    # the small-tail argument is false for a general passive three-cycle.
    assert cycle*y != x


def test_one_neighbor_and_reciprocal_scores_against_four_dimensional_gram():
    # A rotated Z^4 comb with a nonorthogonal PUBLIC basis. The rounded
    # estimators receive that public basis, not its short frame.
    short = np.array(_right_quaternion(1, 2, 2, 0)/3, dtype=float)
    shear = np.eye(4)
    shear[0, 1] = 1
    basis, inverse = short@shear, np.linalg.inv(short@shear)
    short_coefficients = np.array(list(product(range(-2, 3), repeat=4)), dtype=int)
    points = short_coefficients@short.T
    public_coefficients = np.rint(short_coefficients@np.linalg.inv(shear).T).astype(int)
    s, nu, radius = 0.8, 1/256, 4
    weights = np.exp(-np.pi*np.sum(points*points, axis=1)/s**2)
    z = weights@weights
    c = np.pi/(4*nu**2)
    identity_distances = np.sum((points[:, None, :]-points[None, :, :])**2, axis=2)
    physical_norm = weights@np.exp(-c*identity_distances)@weights
    assert abs(physical_norm/z-1) < 1e-13

    t = 1/5000
    ca, sa = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    near_real = np.eye(4, dtype=complex)
    near_real[:2, :2] = [[ca, 1j*sa], [-1j*sa, -ca]]
    circular = np.eye(4, dtype=complex)
    circular[:2, :2] = [[0, 1j], [-1j, 0]]
    for local in (near_real, circular, -np.eye(4)):
        parity = short@local@short.T
        assert np.allclose(parity@parity, np.eye(4), atol=1e-14)
        a, b = parity.real, parity.imag
        transformed, imaginary = points@a.T, points@b.T
        # Rows y, columns x. This form avoids subtracting large near-equal norms.
        distances = np.sum((points[:, None, :]-transformed[None, :, :])**2, axis=2)
        distances += np.sum(imaginary*imaginary, axis=1)[None, :]
        kernel = np.exp(-c*distances+2j*c*(points@b@points.T))
        direct = (weights@kernel@weights)/physical_norm
        assert abs(direct.imag) < 1e-13 and abs(direct.real) <= 1+1e-13

        candidate_coefficients = np.rint(transformed@inverse.T).astype(int)
        candidates = candidate_coefficients@basis.T
        back_coefficients = np.rint((candidates@a.T)@inverse.T).astype(int)
        mutual = np.all(back_coefficients == public_coefficients, axis=1)
        assert np.max(np.abs(np.rint(candidates@short))) <= 2
        squared_distance = np.sum((candidates-transformed)**2, axis=1)
        squared_distance += np.sum(imaginary*imaginary, axis=1)
        candidate_kernel = np.exp(-c*squared_distance+2j*c*np.sum(candidates*imaginary, axis=1))
        candidate_weights = np.exp(-np.pi*np.sum(candidates*candidates, axis=1)/s**2)
        one_score = candidate_weights/weights*candidate_kernel
        one_score[np.linalg.norm(points, axis=1) > radius] = 0
        paired_score = 2*weights*candidate_weights/(weights**2+candidate_weights**2)
        paired_score *= candidate_kernel.real*mutual
        assert np.max(np.abs(one_score)) <= 2
        assert np.max(np.abs(paired_score)) <= 1+1e-13
        one_mean = np.dot(weights**2, one_score.real)/z
        paired_mean = np.dot(weights**2, paired_score)/z

        with mp.workdps(90):
            # Coefficient-box error is bounded in ket norm by its omitted L1
            # weight. No narrow-lattice enumeration is used by the estimator.
            partial, tail = _theta_window(mp.mpf(4)/5, 2)
            omitted = sum(mp.binomial(4, j)*partial**(4-j)*tail**j for j in range(1, 5))
            assert 4*omitted < mp.mpf("1e-17")
            r = 1/(8*mp.sqrt(5))  # inverse Frobenius norm sqrt(5).
            nu_mp = mp.mpf(1)/256
            eta = _theta_excess_upper(2*nu_mp, 4)
            beta = (1+_theta_excess_upper(mp.sqrt(8)*nu_mp, 4))*mp.exp(-mp.pi*r*r/(8*nu_mp**2))
            assert eta+beta < mp.mpf("1e-30")
            roundoff = mp.mpf("1e-10")  # NumPy evaluation is not interval arithmetic.
            assert abs(paired_mean-direct.real) <= eta+beta+4*omitted+roundoff
            assert abs(one_mean-direct.real) <= mp.mpf("1e-12")+4*omitted+roundoff
        if np.array_equal(local, -np.eye(4)):
            assert abs(direct.real-1) < 1e-13
        else:
            assert np.any(~mutual) or np.max(np.abs(candidate_kernel.imag)) > 0.1


def test_actual_infinite_z4_comb_circular_parity_and_phase_countercontrol():
    # Z^4 is the Hamilton Lipschitz-order lattice. Two untouched coordinates
    # cancel exactly. The active two-dimensional sums factor into 1D pairs.
    with mp.workdps(90):
        for s, nu, cutoff in ((mp.mpf(4), mp.mpf(1)/16, 16),
                              (mp.mpf(2), mp.mpf(1), 10)):
            c = mp.pi/(4*nu**2)
            pairs = tuple(product(range(-cutoff, cutoff+1), repeat=2))
            gram = mp.fsum(mp.exp(-mp.pi*(x*x+y*y)/s**2-c*(x-y)**2) for x, y in pairs)
            oscillatory = mp.fsum(
                mp.exp(-(mp.pi/s**2+c)*(x*x+y*y))*mp.cos(2*c*x*y)
                for x, y in pairs)
            absolute = mp.fsum(mp.exp(-(mp.pi/s**2+c)*(x*x+y*y)) for x, y in pairs)
            mean = (oscillatory/gram)**2
            _, amplitude_tail = _theta_window(s, cutoff)
            # Each 1D normalized ket differs by <=2*amplitude_tail. The
            # two-mode ket differs by <=4*tail, hence expectation by <=8*tail.
            error = 8*amplitude_tail+mp.mpf("1e-70")
            assert error < mp.mpf("1e-20")
            if s == 4:
                assert mp.mpf("0.1249999999") < mean-error < mean+error < mp.mpf("0.1250000001")
                # A real quarter-turn preserves this square comb and has
                # overlap exactly 1, unlike the single circular-mode parity.
                assert 1-mean > mp.mpf("0.87")
            else:
                assert mp.mpf("0.63023") < mean-error < mean+error < mp.mpf("0.63024")
                assert (absolute/gram)**2-mean > mp.mpf("0.12")
                z_1d, z_tail = _theta_window(s/mp.sqrt(2), cutoff)
                assert gram > z_1d+z_tail  # Z is not S at overlapping widths.


def test_joint_parity_projector_walsh_identity_and_global_evenness():
    u = sp.symbols("u0:3", nonzero=True)
    for outcome in product((-1, 1), repeat=3):
        expanded = sp.Integer(0)
        for mask in product((0, 1), repeat=3):
            term = sp.prod(outcome[j]**mask[j]*u[j]**(1-2*mask[j]) for j in range(3))
            expanded += term/8
        factored = sp.prod((u[j]+outcome[j]/u[j])/2 for j in range(3))
        assert sp.expand(expanded-factored) == 0
    # For the actual infinite comb w(-x)=w(x). Substituting y -> -y in
    # the numerator for P=-I gives S, not Z, exactly at every packet width.
    x, y, nu, s = sp.symbols("x y nu s", real=True, nonzero=True)
    w = lambda v: sp.exp(-sp.pi*v*v/s**2)
    total_parity = w(x)*w(y)*sp.exp(-sp.pi*(x+y)**2/(4*nu**2))
    normalizer = w(x)*w(y)*sp.exp(-sp.pi*(x-y)**2/(4*nu**2))
    assert sp.simplify(total_parity.subs(y, -y)-normalizer) == 0


def test_mismatched_oscillator_vacuum_invalidates_coherent_packet_formula():
    nu, vacuum_width = sp.symbols("nu vacuum_width", positive=True)
    # Circular parity swaps position and momentum in this plane. A packet
    # width nu becomes vacuum_width^2/nu. The two-dimensional overlap is
    # not the matched coherent-vacuum value 1 unless the widths agree.
    transformed_width = vacuum_width**2/nu
    overlap_2d = 2*nu*transformed_width/(nu**2+transformed_width**2)
    assert sp.simplify(overlap_2d-2*nu**2*vacuum_width**2/(nu**4+vacuum_width**4)) == 0
    assert overlap_2d.subs(vacuum_width, nu) == 1
    assert overlap_2d.subs(vacuum_width, 2*nu) == sp.Rational(8, 17)
