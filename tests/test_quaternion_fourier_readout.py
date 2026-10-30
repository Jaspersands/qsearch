"""Bounded Cartesian-readout controls, not a sampler or transporter algorithm.

Conventions in N real coordinates:
  phi_nu(u) = nu**(-N/2) * exp(-pi*||u||**2/(2*nu**2)), normalized in L2;
  source coefficients = exp(-pi*||x||**2/s**2), x in L;
  Fourier kernel = exp(-2*pi*i*k.x);
  D_{L,r} is a PROBABILITY law proportional to exp(-pi*||x||**2/r**2).
The source normalizer includes its packet Gram matrix, not just coefficient
squares. Its Fourier amplitude is proportional to
  exp(-2*pi*nu**2*||k||**2) * sum_y exp(-pi*s**2*||k-y||**2), y in L*.

Exact identities below are coordinatewise and hence tensorize. Numerical
checks use only Z, fixed cutoffs (at most 32), and 90-digit arithmetic.
Analytic Gaussian tail majorants and a separate roundoff allowance are
reported in assertions; mpmath evaluations are NOT directed interval proofs.
These controls do not implement preparation, a finite-grid QFT, alias bounds,
general lattice theta evaluation, narrow Gaussian sampling, or a speedup.
"""

import mpmath as mp
import sympy as sp


# Right multiplication by (1+2i+3j+4k)/sqrt(30), in Hamilton coordinates.
SHORT_FRAME = sp.Matrix([
    [1, -2, -3, -4],
    [2, 1, 4, -3],
    [3, -4, 1, 2],
    [4, 3, -2, 1],
]) / sp.sqrt(30)
UNIMODULAR = sp.Matrix([[1, 4, 0, 0], [4, 17, 0, 0],
                        [0, 0, 1, 0], [0, 0, 0, 1]])
PUBLIC_BASIS = SHORT_FRAME * UNIMODULAR


def _gs_squared(basis):
    assert basis.shape == (4, 4)
    vectors = sp.GramSchmidt([basis[:, i] for i in range(4)])
    return [sp.simplify(v.dot(v)) for v in vectors]


def _theta_window(width, shift, cutoff):
    """Finite Z+shift sum and a two-sided omitted-tail upper bound."""
    assert isinstance(cutoff, int) and 1 <= cutoff <= 32
    assert width > 0 and abs(shift) <= mp.mpf("0.5")
    value = mp.fsum(mp.exp(-mp.pi * (j + shift)**2 / width**2)
                    for j in range(-cutoff, cutoff + 1))
    first = mp.mpf(cutoff + 1) - abs(shift)
    ratio = mp.exp(-mp.pi * (2*first + 1) / width**2)
    assert 0 < ratio < 1
    tail = 2 * mp.exp(-mp.pi * first**2 / width**2) / (1 - ratio)
    return value, tail


def test_exact_gaussian_completion_and_probability_scales_keep_c():
    s, nu = sp.symbols("s nu", positive=True)
    k, y, v = sp.symbols("k y v", real=True)
    A = s*s + 2*nu*nu
    c = s*s / A
    nu_prime_sq = 1 / (2*A)
    s_prime_sq = s*s / (2*nu*nu*A)
    r_sq = A / (4*nu*nu*s*s)

    # Unit packet norm and the overlap exponent e^(-pi*v^2/(4*nu^2)).
    assert sp.integrate(sp.exp(-sp.pi*k*k/nu**2)/nu,
                        (k, -sp.oo, sp.oo)) == 1
    assert sp.expand((k*k + (k-v)**2)/(2*nu**2)
                     - (k-v/2)**2/nu**2 - v*v/(4*nu**2)) == 0

    original = 2*nu*nu*k*k + s*s*(k-y)**2
    completed = (c*y)**2/s_prime_sq + (k-c*y)**2/(2*nu_prime_sq)
    assert sp.simplify(original - completed) == 0
    assert sp.simplify(2*original - y*y/r_sq - 2*A*(k-c*y)**2) == 0
    assert sp.simplify(s_prime_sq/(2*c*c) - r_sq) == 0
    assert sp.simplify(r_sq - 1/(4*nu**2) - 1/(2*s**2)) == 0
    assert sp.simplify(nu_prime_sq/(2*sp.pi) - 1/(4*sp.pi*A)) == 0
    assert sp.simplify(c*c/(4*nu_prime_sq) - c*s*s/2) == 0

    # A legal finite-width example where replacing c by 1 changes the law.
    values = {s: 2, nu: 1}
    assert c.subs(values) == sp.Rational(2, 3)
    assert r_sq.subs(values) == sp.Rational(3, 8)
    wrong_center = (c*y)**2/s_prime_sq + (k-y)**2/(2*nu_prime_sq)
    assert (original-wrong_center).subs(values | {k: 0, y: 1}) == -sp.Rational(10, 3)


def test_skew_public_basis_needs_reversed_dual_gram_schmidt():
    assert SHORT_FRAME.T * SHORT_FRAME == sp.eye(4)
    assert UNIMODULAR.det() == 1
    assert PUBLIC_BASIS.T * PUBLIC_BASIS != sp.eye(4)
    dual = PUBLIC_BASIS.inv().T
    assert PUBLIC_BASIS.T * dual == sp.eye(4)
    primal_gs = _gs_squared(PUBLIC_BASIS)
    ordinary_dual_gs = _gs_squared(dual)
    reversed_dual_gs = _gs_squared(dual[:, ::-1])
    assert primal_gs == [17, sp.Rational(1, 17), 1, 1]
    assert ordinary_dual_gs == [305, sp.Rational(1, 305), 1, 1]
    assert reversed_dual_gs == [1/value for value in primal_gs[::-1]]
    assert ordinary_dual_gs != [1/value for value in primal_gs]
    assert _gs_squared(SHORT_FRAME.inv().T) == [1, 1, 1, 1]
    assert sp.trace(dual.T * dual) == 324  # Public inverse Frobenius norm squared.


def test_exact_interference_midpoint_identity_and_positive_mixture_bound():
    s, nu = sp.symbols("s nu", positive=True)
    k, y, u = sp.symbols("k y u", real=True)
    A = s*s + 2*nu*nu
    c = s*s / A
    r_sq = A / (4*nu*nu*s*s)
    midpoint = y + u/2
    pair = 4*nu*nu*k*k + s*s*((k-y)**2 + (k-y-u)**2)
    completed = 2*A*(k-c*midpoint)**2 + midpoint**2/r_sq + s*s*u*u/2
    assert sp.simplify(pair - completed) == 0
    pair_integral = sp.integrate(sp.exp(-2*sp.pi*A*k*k), (k, -sp.oo, sp.oo))
    assert sp.simplify(pair_integral - 1/sp.sqrt(2*A)) == 0

    # Integrating pairs yields exp(-pi*s^2*u^2/2)*rho_r(L*+u/2).
    # Coefficient overlap supplies the difference from the weaker Gram bound.
    assert sp.simplify(c*s*s/2 + 1/(4*r_sq) - s*s/2) == 0
    R, slack, q, cross = sp.symbols("R slack q cross", nonnegative=True)
    assert sp.simplify((q + R*cross)/(1+R) - q - R*(cross-q)/(1+R)) == 0
    # If R <= E=R+slack, TV <= R/(1+R) <= E/(1+E).
    difference = (R+slack)/(1+R+slack) - R/(1+R)
    assert sp.simplify(difference - slack/((1+R)*(1+R+slack))) == 0


def test_z_parseval_and_interference_ratio_with_explicit_tail_budgets():
    with mp.workdps(90):
        s, nu = mp.mpf(2), mp.mpf(2)/5
        A = s*s + 2*nu*nu
        r = mp.sqrt(A)/(2*nu*s)
        cutoff, u_cutoff = 12, 8  # At most 625 primal pairs, 16 nonzero u's.
        xs = tuple(range(-cutoff, cutoff+1))
        weights = tuple(mp.exp(-mp.pi*x*x/(s*s)) for x in xs)
        primal_norm = mp.fsum(
            wx*wy*mp.exp(-mp.pi*(x-y)**2/(4*nu*nu))
            for x, wx in zip(xs, weights) for y, wy in zip(xs, weights)
        )
        amplitude_sum, amplitude_tail = _theta_window(s, 0, cutoff)
        # Packet overlaps are <=1, bounding all pairs with an omitted index.
        primal_tail = 2*amplitude_sum*amplitude_tail + amplitude_tail**2
        rho0, tail0 = _theta_window(r, 0, cutoff)
        rhohalf, tailhalf = _theta_window(r, mp.mpf("0.5"), cutoff)
        theta_u, tail_u = _theta_window(mp.sqrt(2)/s, 0, u_cutoff)
        ratios_lo, ratios_hi = [], []
        for u in range(-u_cutoff, u_cutoff+1):
            if u == 0:
                continue
            numerator, tail = (rhohalf, tailhalf) if u % 2 else (rho0, tail0)
            weight = mp.exp(-mp.pi*s*s*u*u/2)
            ratios_lo.append(weight*numerator/(rho0+tail0))
            ratios_hi.append(weight*(numerator+tail)/rho0)
        R_lo = mp.fsum(ratios_lo)
        # Shifted theta <= centered theta bounds every omitted u ratio by 1.
        R_hi = mp.fsum(ratios_hi) + tail_u
        prefactor = 2*nu*s*s/mp.sqrt(2*A)
        fourier_lo = prefactor*rho0*(1+R_lo)
        fourier_hi = prefactor*(rho0+tail0)*(1+R_hi)

        # Analytic tail budgets are distinct from this non-certified floating
        # allowance. No adaptive quadrature or unbounded lattice enumeration.
        roundoff = mp.mpf("1e-70")
        assert primal_tail < mp.mpf("1e-55")
        assert tail0 + tailhalf + tail_u < mp.mpf("1e-120")
        assert fourier_hi - fourier_lo < mp.mpf("1e-65")
        assert primal_norm <= fourier_hi + roundoff
        assert fourier_lo <= primal_norm + primal_tail + roundoff
        R_source_lo = primal_norm/(prefactor*(rho0+tail0)) - 1
        R_source_hi = (primal_norm+primal_tail)/(prefactor*rho0) - 1
        assert R_source_lo <= R_hi + roundoff
        assert R_lo <= R_source_hi + roundoff
        assert mp.mpf("0.00366") < R_lo <= R_hi < mp.mpf("0.003662")
        assert R_hi < theta_u - 1  # The shifted-theta bound is strictly loose.

        probability_sum, probability_tail = _theta_window(s/mp.sqrt(2), 0, cutoff)
        gram_theta, gram_tail = _theta_window(2*nu, 0, cutoff)
        assert primal_norm > probability_sum + probability_tail
        assert (primal_norm+primal_tail)/probability_sum - 1 < gram_theta+gram_tail-1


def test_sampler_H_constant_bounds_conservative_ratio_for_all_legal_N_epsilon():
    # Universal bound, not inferred from the finite numerical cases below:
    # q=exp(-pi*H^2)=eps/(32*N)<=1/32; xi<=2q/(1-q^3)<=3q.
    # xi<1/2 gives log((1+xi)/(1-xi)) <= 3xi, by integrating
    # 2/(1-t^2). Thus N*log(ratio)<=9eps/32. Finally exp(z)-1
    # <=z/(1-z) for 0<=z<1, so ratio^N-1 <= (9/23)*eps < eps.
    q_max = sp.Rational(1, 32)
    assert 2/(1-q_max**3) < 3
    assert 3*q_max < sp.Rational(1, 2)
    assert 2/(1-sp.Rational(1, 2)**2) < 3
    exponent_factor = sp.Rational(9, 32)
    assert exponent_factor/(1-exponent_factor) == sp.Rational(9, 23) < 1

    with mp.workdps(90):
        for dimension in (1, 4, 16, 64):
            for epsilon in (mp.mpf(1), mp.mpf(1)/16, mp.mpf("1e-8"), mp.mpf("1e-30")):
                H = mp.sqrt(mp.log(32*dimension/epsilon)/mp.pi)
                q = mp.exp(-mp.pi*H*H)
                xi_upper = 2*q/(1-q**3)
                assert xi_upper < 3*epsilon/(32*dimension) < mp.mpf("0.5")
                log_ratio = mp.log1p(xi_upper) - mp.log1p(-xi_upper)
                sampler_bound = mp.expm1(dimension*log_ratio)
                theta_bound = mp.expm1(dimension*mp.log1p(xi_upper))
                assert 0 < sampler_bound < mp.mpf(9)*epsilon/23 < epsilon
                assert 0 < theta_bound < epsilon


def test_public_primal_and_dual_width_conditions_are_separate():
    # The hidden short frame and public skew frame generate the SAME lattice.
    # Failing a sufficient public-basis bound is not a hardness assertion.
    primal_sq = max(_gs_squared(PUBLIC_BASIS))
    dual = PUBLIC_BASIS.inv().T
    dual_sq = max(_gs_squared(dual))
    frobenius_sq = sp.trace(dual.T * dual)
    dimension = 4
    s_sq = 128*primal_sq  # Primal probability width s/sqrt(2)=8*sqrt(17).
    nu_good = sp.Rational(1, 8)/sp.sqrt(dimension*frobenius_sq)
    assert nu_good == sp.Rational(1, 288)
    assert nu_good**2 * dimension * frobenius_sq == sp.Rational(1, 64)
    assert 1/(4*nu_good**2*dual_sq) >= 16*dimension

    with mp.workdps(90):
        epsilon = mp.mpf(1)/16
        H = mp.sqrt(mp.log(32*dimension/epsilon)/mp.pi)
        primal_ratio = mp.sqrt(mp.mpf(int(s_sq))/(2*int(primal_sq)))
        nu_bad = mp.mpf(1)/4
        r_bad_sq = 1/(4*nu_bad**2) + 1/(2*mp.mpf(int(s_sq)))
        assert primal_ratio > H
        assert mp.sqrt(r_bad_sq) > H  # A short dual frame would suffice.
        assert mp.sqrt(r_bad_sq/int(dual_sq)) < H  # This public one does not.

        nu = mp.mpf(1)/288
        r_sq = 1/(4*nu**2) + 1/(2*mp.mpf(int(s_sq)))
        assert mp.sqrt(r_sq/int(dual_sq)) > 4*mp.sqrt(dimension) > H
        assert 1/(2*nu*mp.sqrt(int(dual_sq))) > H
        assert r_sq != mp.mpf(int(s_sq))/2  # Dual and primal probability widths.
        # The Fourier interference bound uses primal GS, with no inverse norm.
        q = mp.exp(-mp.pi*primal_ratio**2)
        xi_upper = 2*q/(1-q**3)
        assert mp.expm1(dimension*mp.log1p(xi_upper)) < epsilon
