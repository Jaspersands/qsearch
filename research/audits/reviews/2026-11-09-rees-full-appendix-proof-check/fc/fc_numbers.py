"""Independent recomputation of the numbers of appendix-free-coordinate.tex (checker fc, 9 Nov 2026):
Table tab:fcs-budget columns (iii) Q / trials / total and w.-d. Q, Section app:fc-numbers (a),(b),
the uniform-kernel caps, Lemma lem:fc-params and Proposition prop:fc-uniform(a) constants.
Exact rationals for every threshold comparison; logs only for reporting.
Run: nice -n 19 timeout 600 /opt/anaconda3/bin/python -I fc_numbers.py
"""
import math
from fractions import Fraction as Fr
from sympy import isprime, nextprime
import numpy as np

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

LN2 = math.log(2)
def log2f(x):
    if isinstance(x, Fr):
        return math.log2(x.numerator) - math.log2(x.denominator)
    return math.log2(x)

def beta(M, n0, a, p, kappa):
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    return Fr(4) / (Fr(h) ** (n0 - 1) * q ** a) + Fr(p ** a - 1, (p - 1) * p ** (M - n0))

def least_arity(p, kappa, g, tau):
    M = 1
    while True:
        for n0 in range(1, M + 1):
            if beta(M, n0, g, p, kappa) <= tau:
                return M, n0
        M += 1

def least_k(base, target):  # least k >= 0 with base^k >= target (exact)
    k = 0; v = Fr(1)
    while v < target:
        v *= base; k += 1
    return k

def explicit_arity(p, kappa, g, tau):
    h = (p - 1) // kappa; q = Fr(h + 1, p)
    n0 = 1 + least_k(Fr(h), Fr(8) * q ** (-g) / tau)
    M = n0 + g + least_k(Fr(p), Fr(2) / tau)
    assert beta(M, n0, g, p, kappa) <= tau
    return M, n0

def ceil_2Bln2_times(B, x):  # ceil(2 B ln2 * x), x a positive rational; float is fine at these sizes (reporting)
    return math.ceil(2 * B * LN2 * float(x)) if float(x) < 1e300 else None

g = [19, 17, 16, 14, 12, 9, 6, 3, 1]          # g_1..g_9
m, c = 19, 9
eps = Fr(1, 3)
PRIMES = [11, 1031, 5281, 2**31 - 1, 2**61 - 1, 2**127 - 1]
for p in PRIMES:
    assert isprime(p)
say("[0] all six table primes are prime; 194522647344910884721 prime:", isprime(194522647344910884721), "; 105019 prime:", isprime(105019))

def kap(d, p): return math.gcd(d, p - 1)

def t_of(p):  # t = ceil(log_p(3/eps))
    return least_k(Fr(p), 3 / eps)

# ------------------------------------------------------------------ difference-set depth j*_h
def depth(p, h):
    """least J with D_J = F_p, D_0 = mu_h u {0}, D_{j+1} = D_j - D_j (FFT correlation)."""
    if h == p - 1:
        return 0
    # mu_h: elements of order dividing h
    gen = None
    for a in range(2, p):
        if all(pow(a, (p - 1) // r, p) != 1 for r in set(prime_factors(p - 1))):
            gen = a; break
    w = pow(gen, (p - 1) // h, p)
    D = np.zeros(p, dtype=bool); D[0] = True
    x = 1
    for _ in range(h):
        D[x] = True; x = x * w % p
    J = 0
    while not D.all():
        f = np.fft.rfft(D.astype(float))
        corr = np.fft.irfft(f * np.conj(f), n=p)
        D = corr > 0.5
        J += 1
    return J

def prime_factors(n):
    fs = []; d = 2
    while d * d <= n:
        while n % d == 0:
            fs.append(d); n //= d
        d += 1
    if n > 1: fs.append(n)
    return fs

# ------------------------------------------------------------------ [1] Table fcs-budget, (iii) columns
say("[1] Table tab:fcs-budget, part (iii) columns (least public arities) and explicit choice")
say("    claimed (iii) Q / trials / total:", "42.3/28.3/47.0  36.6/33.4/50.8  39.1/33.8/52.2  35.9/31.0/49.8  34.1/33.5/51.0  34.0/31.0/49.5")
for p in PRIMES:
    t = t_of(p); S = m + t
    Ms = {}; n0s = {}; nd = {}
    GF = [d for d in range(2, c + 1) if 2 <= kap(d, p) < p - 1]
    G0 = [d for d in range(2, c + 1) if kap(d, p) == p - 1 and p - 1 >= 2]
    assert not G0
    for d in range(2, c + 1):
        nd[d] = math.prod(Ms[e] for e in range(2, d))
        if kap(d, p) == 1:
            Ms[d] = g[d - 1] + 1
        else:
            tau = eps / (9 * (c - 1) * S * nd[d])
            Ms[d], n0s[d] = least_arity(p, kap(d, p), g[d - 1], tau)
    P = math.prod(Ms.values())
    Q = c * S * P
    N = S * sum(nd[d] for d in GF)
    B = math.ceil(log2f(27 * N / eps))
    # exactness of the ceiling: check 2^B >= 81N > 2^(B-1)
    assert 2 ** B >= 27 * N / eps > 2 ** (B - 1)
    caps = {}
    for d in GF:
        kappa = kap(d, p); h = (p - 1) // kappa; q = Fr(h + 1, p)
        caps[d] = math.ceil(2 * B * LN2 * float(q ** (-g[d - 1])))
    dmax = max(caps, key=lambda d: caps[d])
    total = sum(S * nd[d] * caps[d] for d in GF)
    # explicit choice
    Ms2 = {}
    for d in range(2, c + 1):
        n_d = math.prod(Ms2[e] for e in range(2, d))
        if kap(d, p) == 1:
            Ms2[d] = g[d - 1] + 1
        else:
            Ms2[d] = explicit_arity(p, kap(d, p), g[d - 1], eps / (9 * (c - 1) * S * n_d))[0]
    Q2 = c * S * math.prod(Ms2.values())
    nd2 = {d: math.prod(Ms2[e] for e in range(2, d)) for d in range(2, c + 1)}
    N2 = S * sum(nd2[d] for d in GF); B2 = math.ceil(log2f(27 * N2 / eps))
    caps2 = max(math.ceil(2 * B2 * LN2 * float(Fr((p - 1) // kap(d, p) + 1, p) ** (-g[d - 1]))) for d in GF)
    incr = [Ms2[d] - Ms[d] for d in GF]
    say(f"    p={p if p < 10**6 else ('2^%d-1' % (p.bit_length()))}: S={S} M=({','.join(str(Ms[d]) for d in range(2,c+1))}) "
        f"log2Q={log2f(Q):.2f} B={B} maxcap=2^{math.log2(caps[dmax]):.2f} (grade {dmax}, kappa={kap(dmax,p)}) total=2^{math.log2(total):.2f}; "
        f"explicit: M increments {incr}, dlog2Q={log2f(Q2)-log2f(Q):.2f}, maxcap 2^{math.log2(caps2):.2f}")

# ------------------------------------------------------------------ [2] w.-d. column
say("[2] Table tab:fcs-budget, w.-d. column (node of rem:fc-witness-h3(b), arities as stated)")
say("    claimed: 103.5, 93.0, 119.9, 127.1, 150.8, 142.0")
def N0_table(n, sigma, jstar):
    # N_{j*}(e) = e+1 ; N_j(n) = 1 + sigma * sum_{e<n} N_{j+1}(e)
    vals = [Fr(e + 1) for e in range(n + 1)]
    for _ in range(jstar):
        new = []
        acc = Fr(0)
        for e in range(n + 1):
            new.append(1 + sigma * acc)
            acc += vals[e]
        vals = new
    return vals[n]
for p in PRIMES:
    t = t_of(p); S = m + t
    Ms = {}; forms = {}
    for d in range(2, c + 1):
        n_d = math.prod(Ms[e] for e in range(2, d))
        kappa = kap(d, p)
        if kappa == 1:
            Ms[d] = g[d - 1] + 1; continue
        tau = eps / (9 * (c - 1) * S * n_d)
        gd = g[d - 1]
        if p >= (2 * (kappa - 1) * (kappa - 2) + 4) ** 2:      # sqrt p >= 2(k-1)(k-2)+4
            Nbar = 1 + Fr(math.ceil(math.log2(p)) * p, p - 1) * Fr(gd * (gd + 1), 2)
            forms[d] = 'resc'
        else:
            h = (p - 1) // kappa
            js = depth(p, h)
            sig = min(p, math.ceil(2 * math.log2(p - 1)) + 4)
            Nbar = N0_table(gd, Fr(sig), js)
            forms[d] = f'tab(j*={js})'
        Lblk = math.ceil(2 * Nbar)
        Ms[d] = gd + least_k(Fr(p), 2 / tau) + least_k(Fr(2), 2 / tau) * Lblk
    Q = c * S * math.prod(Ms.values())
    say(f"    p={p if p < 10**6 else ('2^%d-1' % (p.bit_length()))}: log2Q={log2f(Q):.2f}; forms {forms}")

# ------------------------------------------------------------------ [3] part (ii) numbers, u = 18
say("[3] app:fc-numbers (b): part (ii) at u=18, M=72, n0=37, B=56; uniform-kernel caps 4 kappa^72 B")
u = max(c, g[1] + 1); M = 4 * u; n0 = 2 * u + 1
B = math.ceil(math.log2(64 * (4 * u) ** (c - 1)))
assert 2 ** B >= 64 * (4 * u) ** (c - 1) > 2 ** (B - 1)
say(f"    u={u} M={M} n0={n0} B={B} 16u^2={16*u*u}")
P6 = [5281, 105019, 2**31 - 1, 2**61 - 1, 194522647344910884721, 2**127 - 1]
for p in P6:
    assert p >= 16 * u * u
    capmax = 0; bsum = Fr(0); ukmax = 0; dcap = None
    for d in range(2, c + 1):
        kappa = kap(d, p); h = (p - 1) // kappa; q = Fr(h + 1, p)
        cap = math.ceil(2 * B * LN2 * float(q ** (-g[d - 1])))
        if cap > capmax: capmax, dcap = cap, d
        bsum += (M ** (d - 2)) * beta(M, n0, g[d - 1], p, kappa)
        ukmax = max(ukmax, 4 * kappa ** M * B)
    kmax = max(kap(d, p) for d in range(2, c + 1))
    say(f"    p={p}: per-node cap 2^{math.log2(capmax):.2f} (grade {dcap}); bank sum/tree 2^{log2f(bsum):.1f}; uniform-kernel cap 2^{math.log2(ukmax):.1f} (kappa_max={kmax})")

# ------------------------------------------------------------------ [4] lem:fc-params and prop:fc-uniform(a)
say("[4] lem:fc-params closed forms and prop:fc-uniform(a)")
ok = True
for u in range(2, 121):
    t1 = Fr(4, 225) ** u / u ** 2
    t2 = Fr(2 * 4 ** (u - 1), 16 ** (u + 1) * u ** (u + 3))
    lhs1 = Fr(4 * u) ** (u - 1) * (Fr(4) / (Fr(15) ** (2 * u) * u ** (u + 1)) + Fr(2) / Fr(16 * u * u) ** (u + 1))
    if lhs1 != t1 + t2 or t1 + t2 >= Fr(1, 64):
        ok = False
    if u == 2:
        say(f"    u=2: terms 1/{float(1/t1):.2f} + 1/{float(1/t2):.0f} = {float(t1+t2):.4g} < 1.5e-4: {t1 + t2 < Fr(15, 100000)}")
say(f"    identity (4u)^(u-1)(...) = (4/225)^u/u^2 + 2*4^(u-1)/(16^(u+1)u^(u+3)) and sum < 1/64 for u=2..120: {ok}")
c1 = Fr(4, 15 ** 4 * 2 ** 3) + Fr(2, 64 ** 3)
say(f"    prop:fc-uniform(a): 4*15^-4*2^-3 + 2*64^-3 = {float(c1):.4g} = 2^{log2f(c1):.2f} < 2^-14: {c1 < Fr(1, 2**14)}")
# beta(4u,2u+1;a) <= 4*15^-2u u^-u-1 + 2p^-u-1 for every kappa <= u dividing p-1, a <= u-1, least prime >= 16u^2
okb = True
for u in range(2, 31):
    for p in [nextprime(16 * u * u - 1), 2**61 - 1]:
        for kappa in range(1, u + 1):
            if (p - 1) % kappa: continue
            for a in range(0, u):
                if beta(4 * u, 2 * u + 1, a, p, kappa) > Fr(4) / (Fr(15) ** (2 * u) * u ** (u + 1)) + Fr(2, p ** (u + 1)):
                    okb = False
say(f"    beta(4u,2u+1;a) <= 4*15^-2u*u^-u-1 + 2p^-u-1 (u=2..30, least prime >= 16u^2 and 2^61-1, all kappa<=u | p-1, a<=u-1): {okb}")

open(__file__.replace('.py', '_out.txt'), 'w').write("\n".join(out) + "\n")
