"""Shared code for the cyclic-case proof checks (2026-11-12-rees-h3z-cyclic-proof.md).

Group H_3(Z): (a,b,c)(a',b',c') = (a+a', b+b', c+c'+ab').  h = (a,b,c), w = (a,b) != 0,
X = (a, b, X3) with X3 = 2c - ab.  Everything here is exact integer arithmetic except the
Fejer acceptance ratio and the float Gram-Schmidt used only to *list* candidates
(every candidate is re-checked exactly).  Finite checks only falsify.
"""
import math, random
from fractions import Fraction
from fpylll import IntegerMatrix, LLL
from sympy import isprime, sqrt_mod, jacobi_symbol, factorint

# ---------------------------------------------------------------- group
def mul(g, h): return (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])
def inv(g): return (-g[0], -g[1], -g[2] + g[0] * g[1])
def pw(g, t): return (t * g[0], t * g[1], t * g[2] + (t * (t - 1) // 2) * g[0] * g[1])
def C2(t): return t * (t - 1) // 2

def in_H(g, h):
    """g in <h> (h non-central)?"""
    a, b = h[0], h[1]
    if a:
        if g[0] % a: return False
        k = g[0] // a
    else:
        if g[1] % b: return False
        k = g[1] // b
    return pw(h, k) == tuple(g)

# ---------------------------------------------------------------- parameters (Sec. C4)
def params(b, eta_s=2.0 ** -10):
    """Explicit parameter choice of the report, Sec. C4.  Returns a dict of exact integers."""
    p = {}
    p['b'] = b; p['eta_s'] = eta_s
    p['m1'] = 4                                   # stage-1 samples per batch
    p['logMb'] = 3 * b + 26; p['Mb'] = 1 << p['logMb']
    p['log_gamma1'] = -(2 * b + 19)               # strip half-width gamma = 2^-(2b+19)
    p['K'] = 6 * b + 67                           # ||Theta|| <= 2^-K
    p['logeps'] = -(p['K'] + 1)                   # SDA tolerance eps = 2^-(K+1)
    epsinv2 = 1 << (2 * (p['K'] + 1))
    # integer-only arithmetic (eta_s = 2^-10 fixed): every bound below is rounded UP
    assert eta_s == 2.0 ** -10
    L1e6 = math.ceil(2 * (p['K'] + 1) * math.log(2) * 10 ** 6) + 1        # ln(eps^-2), rounded up, x1e6
    p['Q'] = (2 * epsinv2 * L1e6) // 10 ** 6 + 1                           # Q >= 2 eps^-2 ln(eps^-2)
    p['mu_max'] = math.isqrt(p['Q'] * 23095 // 10000) + 1                 # >= sqrt(4Q/sqrt3)
    Mb, mu = p['Mb'], p['mu_max']
    P = ((192 * mu * Mb) << 20) // 10 + 1                                  # >= 19.2 mu Mb / eta_s^2
    P = max(P, 1 << (2 * b + 3)); p['P'] = P
    D = (9 * mu * mu * Mb * Mb) // 2 + 2 * P * mu * Mb + 1                 # >= 4.5 mu^2 Mb^2 + 2 P mu Mb
    p['D'] = D; p['N'] = (16 * D) << 20                                    # 16 D / eta_s^2
    p['V'] = 5 * P * P; p['R'] = (10 * P * P) << 10                        # 10 P^2 / eta_s
    n0 = max((2 * p['R']).bit_length(), (600 * p['Q'] * epsinv2).bit_length(), p['logMb'] + 1)
    p['n0'] = n0; p['N0'] = 1 << n0
    # stage 2 (A_v), Sec. C2
    p['m2'] = 4; p['logFA'] = 4 * b + 30; p['FA'] = 1 << p['logFA']; p['log_gamma2'] = -(2 * b + 21)
    p['logQpf'] = 2 * b + 2
    # oracle box exponent B: stage-1 domain [-P,P)^2 x [-R,R); stage-2 iota(t,s), t,s < F_A
    p['B'] = max(p['R'].bit_length() + 1, 2 * p['logFA'] + 2 * b + 2, 20 * b + 11)
    return p

# ---------------------------------------------------------------- SDA-ISO with full enumeration (Sec. C3)
def _gso(B):
    n = len(B); Bs = []; mu = [[0.0] * n for _ in range(n)]
    for i in range(n):
        v = list(B[i])
        for j in range(i):
            mu[i][j] = sum(B[i][k] * Bs[j][k] for k in range(len(v))) / sum(x * x for x in Bs[j])
            v = [v[k] - mu[i][j] * Bs[j][k] for k in range(len(v))]
        Bs.append(v)
    return Bs, mu, [sum(x * x for x in v) for v in Bs]

def enum_ball(Bint, center, radius_int):
    """All integer combinations z with ||z B - center|| <= radius (Fincke-Pohst, dim 3).
    Floats (after scaling) only produce a candidate list with 1% radius slack; callers recheck exactly."""
    s = max(0, radius_int.bit_length() - 30)
    Bf = [[float(x >> s) if x >= 0 else -float((-x) >> s) for x in row] for row in Bint]
    cf = [float(c) / 2 ** s for c in center]
    r2 = (float(radius_int) / 2 ** s * 1.01) ** 2
    Bs, mu, nb = _gso(Bf)
    n = len(Bf)
    # coordinates of center in GSO basis
    # center in GSO coordinates: center = sum t_i Bs_i (+ orthogonal part)
    t = [sum(cf[k] * Bs[i][k] for k in range(n)) / nb[i] for i in range(n)]
    # center in B-coordinates: solve z with sum z_j (B_j) components along Bs_i: c_i = t_i - sum_{j>i} z_j mu[j][i]
    out = []
    z = [0] * n
    def rec(i, partial):
        ci = t[i] - sum(z[j] * mu[j][i] for j in range(i + 1, n))
        w = math.sqrt(max(0.0, (r2 - partial) / nb[i]))
        lo, hi = math.ceil(ci - w), math.floor(ci + w)
        for zi in range(lo, hi + 1):
            z[i] = zi
            d = partial + (zi - ci) ** 2 * nb[i]
            if d <= r2:
                if i == 0: out.append(tuple(z))
                else: rec(i - 1, d)
        z[i] = 0
    rec(n - 1, 0.0)
    return out

def gauss_reduce(u, v):
    def n2(a): return a[0] * a[0] + a[1] * a[1]
    if n2(u) > n2(v): u, v = v, u
    while True:
        d, nn = u[0] * v[0] + u[1] * v[1], n2(u)
        m = (2 * d + nn) // (2 * nn)
        v = [v[0] - m * u[0], v[1] - m * u[1]]
        if n2(v) >= n2(u): return u
        u, v = v, u

def sda_iso_full(rho, N0, logeps, Q):
    """Lemma P version: list ALL q in [Q,2Q] with ||q theta_i|| <= eps (theta_i = rho_i/N0),
    keep those that are prime with c1 c2 != 0 mod q and -c2/c1 a nonzero square; return the
    smallest such q and mu = shortest vector of {mu1 = r mu2 mod q}.  Returns (mu1,mu2,q,stats)
    or (None, stats)."""
    epsN0 = N0 >> (-logeps)                     # eps*N0 (exact, powers of 2)
    W = max(1, (2 * epsN0) // Q)                # q in [Q,2Q] -> first coord in [QW,2QW], half-width QW/2 ~ eps N0
    A = IntegerMatrix.from_matrix([[W, rho[0], rho[1]], [0, N0, 0], [0, 0, N0]])
    LLL.reduction(A)
    Bint = [[int(A[i, j]) for j in range(3)] for i in range(3)]
    center = (3 * Q * W // 2, 0, 0)
    half = max(Q * W // 2 + W, epsN0)
    radius = math.isqrt(3 * half * half) + 1
    zs = enum_ball(Bint, center, radius)
    stats = {'enum_pts': len(zs), 'box_pts': 0, 'cands': 0}
    good = []
    for z in zs:
        v = [sum(z[i] * Bint[i][k] for i in range(3)) for k in range(3)]
        if v[0] % W: continue
        q = v[0] // W
        if q < 0: q, v = -q, [-x for x in v]
        if not (Q <= q <= 2 * Q): continue
        e = v[1:]                                  # e_i = q rho_i - c_i N0
        if max(abs(e[0]), abs(e[1])) > epsN0: continue
        stats['box_pts'] += 1
        c1 = (q * rho[0] - e[0]) // N0; c2 = (q * rho[1] - e[1]) // N0
        if q % 2 == 0 or c1 % q == 0 or c2 % q == 0 or math.gcd(c1, q) != 1: continue
        tq = (-c2 * pow(c1, -1, q)) % q
        if jacobi_symbol(tq, q) != 1: continue
        if not isprime(q): continue
        stats['cands'] += 1
        good.append((q, c1, c2, tq))
    if not good: return (None, stats)
    q, c1, c2, tq = min(good)
    r = int(sqrt_mod(tq, q))
    mu = gauss_reduce([q, 0], [r, 1])
    assert (c1 * mu[0] ** 2 + c2 * mu[1] ** 2) % q == 0 and mu != [0, 0]
    return (mu[0], mu[1], q, stats)

def theta_dist(rho, mu, N0):
    """||sum theta_i mu_i^2|| exactly."""
    v = sum(r * m * m for r, m in zip(rho, mu)) % N0
    return Fraction(min(v, N0 - v), N0)

# ---------------------------------------------------------------- exact samplers for the ideal law P*
def line_len(u, w, Mb):
    lo, hi = -10 ** 400, 10 ** 400
    for ui, wi in zip(u, w):
        if wi == 0:
            if not (0 <= ui < Mb): return 0
            continue
        if wi > 0: l, h = -(ui // wi), (Mb - 1 - ui) // wi
        else: l, h = -((Mb - 1 - ui) // (-wi)), ui // (-wi)
        lo, hi = max(lo, l), min(hi, h)
    return max(0, hi - lo + 1)

def fejer_sample(rng, L, Np, num, den):
    """Sample j in Z_Np with P(j) = F_L(x_j)/(Np L), x_j = j/Np + num/(den*Np), F_L = Fejer.
    Exact rejection sampler (envelope: L/Np on a core, Np/(L|k|(|k|-1)) on the tails)."""
    j0 = -((2 * num + den) // (2 * den))
    phi = (j0 * den + num) / den                   # in [-1/2, 1/2]
    half = Np // 2
    kc = -(-Np // L) + 1
    core_lo, core_hi = max(-half, -kc), min(Np - half - 1, kc)
    Wc = (core_hi - core_lo + 1) * L / Np
    Wt = Np / (L * kc) if kc < half else 0.0
    tot = Wc + 2 * Wt
    while True:
        r = rng.random() * tot
        if r < Wc:
            k = rng.randint(core_lo, core_hi); env = L / Np
        else:
            U = 1.0 - rng.random()
            k = int(math.ceil(kc / U))
            if k <= kc: continue
            if r >= Wc + Wt: k = -k
            if not (-half <= k <= Np - half - 1): continue
            env = Np / (L * abs(k) * (abs(k) - 1))
        x = (k + phi) / Np
        sx = math.sin(math.pi * x)
        if abs(sx) < 1e-300: FL = float(L) * L
        else:
            Lx = ((L * k) % Np) / Np + L * phi / Np       # L*x mod 1, k-part exact
            FL = math.sin(math.pi * Lx) ** 2 / sx ** 2
        pk = FL / (Np * L)
        if rng.random() * env <= pk:
            return (j0 + k) % Np

def egcd(a, b):
    if b == 0: return (a, 1, 0) if a >= 0 else (-a, -1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def fiber_lift(w, Mb):
    """g = gcd(w1,w2,Mb) and y_g with <y_g,w> = g mod Mb."""
    d, s, t = egcd(w[0], w[1])
    g, s2, _ = egcd(d, Mb)
    return g, ((s2 * s) % Mb, (s2 * t) % Mb)

def sample_ideal(rng, w, X3, A, N0, Mb):
    """One sample y in Z_Mb^2 from P*_alpha(y) = Mb^-4 sum_r F_{L_r}(<y,w>/Mb + alpha X3),
    alpha = A/N0 (A=0, N0=1 gives the untwisted abelian law)."""
    g, yg = fiber_lift(w, Mb)
    Np = Mb // g
    while True:                                    # line through a uniform point, prob L_r/Mb^2
        u = (rng.randrange(Mb), rng.randrange(Mb))
        L = line_len(u, w, Mb)
        if L > 0: break
    den = N0 // Np if N0 >= Np else 1
    num = (A * X3) % N0 if N0 >= Np else 0
    if N0 < Np:   # alpha has denominator dividing Np: shift is an exact grid shift
        num = ((A * X3) % N0) * (Np // N0); den = 1
    j = fejer_sample(rng, L, Np, num, den)
    yr = (rng.randrange(Mb), rng.randrange(Mb))
    jr = (yr[0] * w[0] + yr[1] * w[1]) % Mb
    z = ((yr[0] - (jr // g) * yg[0]) % Mb, (yr[1] - (jr // g) * yg[1]) % Mb)
    return ((j * yg[0] + z[0]) % Mb, (j * yg[1] + z[1]) % Mb)

# ---------------------------------------------------------------- decoders (Sec. C2)
def lll_rows(rows):
    M = IntegerMatrix.from_matrix(rows); LLL.reduction(M)
    return [[int(M[i, j]) for j in range(M.ncols)] for i in range(M.nrows)]

def prim(v):
    g = math.gcd(*v)
    return tuple(x // g for x in v) if g else tuple(v)

def decode_stage1(samples, b, N0, Mb, log_gamma):
    """samples: list of (y, A).  Lattice of the report's Lemma D (d_X = 3).  Returns
    (direction v or None, list of X' of the first two LLL vectors)."""
    gN0 = N0 >> (-log_gamma)
    om = [gN0 >> b, gN0 >> b, gN0 >> (2 * b + 3)]
    m = len(samples); s = N0 // Mb
    rows = []
    for j in range(3):
        r = [0] * (3 + m); r[j] = om[j]
        for k, (y, A) in enumerate(samples):
            r[3 + k] = (y[j] * s) if j < 2 else A
        rows.append(r)
    for k in range(m):
        r = [0] * (3 + m); r[3 + k] = N0; rows.append(r)
    Bred = lll_rows(rows)
    Xs = []
    for vec in Bred[:2]:
        if any(vec[j] % om[j] for j in range(3)): Xs.append(None); continue
        Xs.append(tuple(vec[j] // om[j] for j in range(3)))
    for X in Xs:
        if X is not None and (X[0] or X[1]):
            return prim((X[0], X[1])), Xs
    return None, Xs

def decode_stage2(samples, bounds, F, log_gamma):
    """samples: list of y in Z_F^2 (untwisted).  Lemma D with d_X = 2.  Returns primitive direction."""
    gF = F >> (-log_gamma)
    om = [max(1, gF // bounds[0]), max(1, gF // bounds[1])]
    m = len(samples)
    rows = []
    for j in range(2):
        r = [0] * (2 + m); r[j] = om[j]
        for k, y in enumerate(samples): r[2 + k] = y[j]
        rows.append(r)
    for k in range(m):
        r = [0] * (2 + m); r[2 + k] = F; rows.append(r)
    Bred = lll_rows(rows)
    vec = Bred[0]
    if vec[0] % om[0] or vec[1] % om[1]: return None
    X = (vec[0] // om[0], vec[1] // om[1])
    return prim(X) if X != (0, 0) else None

def contfrac_denoms(y, Qm, maxden):
    out = []; p0, q0, p1, q1 = 0, 1, 1, 0
    a_, b_ = y, Qm
    while b_:
        t = a_ // b_; a_, b_ = b_, a_ - t * b_
        p0, q0, p1, q1 = p1, q1, t * p1 + p0, t * q1 + q0
        if q1 > maxden: break
        out.append(q1)
    return out
