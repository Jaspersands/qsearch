"""Check of Proposition 4.1 (union step, second moment) [exact + float].
(1) brute force over all beta at tiny p: exact E n_j, E n_j^2 equal the moment formula;
(2) at primes just above T_U: exact rho_j from the formula (N_ij(c) by exact correlation),
    max |delta| <= Delta, rho_j <= the per-column bounds, sum_j (rho_j - 1) <= LHS_U(p);
(3) empirical success rate of a uniform beta (all X_j nonempty) against 1 - LHS_U(p).
"""
import sys, random
from fractions import Fraction as Fr
import numpy as np
from rc import primitive_root, is_prime
from thresholds import lhs_U, fourier, T_U
from mpmath import mpf, sqrt, exp

def classes(p, D, g):
    cls = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1): cls[x] = e % D; x = x * g % p
    return cls

def setA(p, D, K, cls, i, j):
    if i % D == 0 and j % D == 0: allowed = {0}
    else: allowed = {(k - i - j) % D for k in K}
    return np.array([c in allowed for c in cls], dtype=bool) & (np.arange(p) != 0)

def corr(a):  # N(c) = #{y in A : y + c in A}, exact via integer convolution
    p = len(a); ai = a.astype(np.int64)
    out = np.array([int(np.dot(ai, np.roll(ai, -c))) for c in range(p)]) if p < 2000 else None
    if out is None:
        f = np.fft.rfft(ai.astype(float)); out = np.rint(np.fft.irfft(np.conj(f) * f, n=p)).astype(np.int64)
    return out

def moments(p, D, R, K, g):
    cls = classes(p, D, g)
    res = []
    for j in range(D):
        A0 = setA(p, D, K, cls, 0, j)
        N0 = corr(A0)
        prod = np.ones(p, dtype=object)
        Asz = None
        for i in R:
            if i == 0: continue
            Ai = setA(p, D, K, cls, i, j); Asz = int(Ai.sum())
            prod = prod * corr(Ai).astype(object)
        r = len(R)
        En = Fr(int(A0.sum()) * Asz ** (r - 1), p ** (r - 1))
        En2 = En + sum(Fr(int(N0[c]) * int(prod[c]), p ** (r - 1)) for c in range(1, p))
        res.append((En, En2))
    return res

def brute(p, D, R, K, g):
    cls = classes(p, D, g)
    others = [i for i in R if i != 0]
    sets = {(i, j): set(np.nonzero(setA(p, D, K, cls, i, j))[0].tolist()) for i in R for j in range(D)}
    import itertools
    S1 = [0] * D; S2 = [0] * D; tot = 0
    for bs in itertools.product(range(p), repeat=len(others)):
        beta = dict(zip(others, bs)); beta[0] = 0; tot += 1
        for j in range(D):
            n = sum(1 for x in range(p) if all((x + beta[i]) % p in sets[(i, j)] for i in R))
            S1[j] += n; S2[j] += n * n
    return [(Fr(S1[j], tot), Fr(S2[j], tot)) for j in range(D)]

def delta_max(p, D, R, K, g):
    cls = classes(p, D, g); mx = 0
    for m in range(D):
        A = setA(p, D, K, cls, m, 0) if m != 0 else setA(p, D, K, cls, 1, D - 1)
        N = corr(A); s = int(A.sum())
        d = (N[1:] - s * s / p) / (s * s / p)
        mx = max(mx, float(np.max(np.abs(d))))
    return mx

def sample(p, D, R, K, g, trials, rng):
    cls = classes(p, D, g); xs = np.arange(p)
    A = {(i, j): setA(p, D, K, cls, i, j) for i in R for j in range(D)}
    ok = 0
    for _ in range(trials):
        beta = {i: (rng.randrange(p) if i else 0) for i in R}
        good = True
        for j in range(D):
            m = np.ones(p, dtype=bool)
            for i in R: m &= A[(i, j)][(xs + beta[i]) % p]
            if not m.any(): good = False; break
        ok += good
    return ok / trials

if __name__ == "__main__":
    rng = random.Random(7)
    for (p, D, R, K) in [(31, 5, [0, 1, 2], [0, 1]), (41, 5, [0, 1, 3], [0, 2]), (29, 7, [0, 1, 2], [0, 1, 2])]:
        g = primitive_root(p)
        assert moments(p, D, R, K, g) == brute(p, D, R, K, g)
        print("brute force p=%d D=%d R=%s K=%s: moment formula exact for every column" % (p, D, R, K), flush=True)
    cases = [(5, list(range(5)), [0, 1, 2]), (7, list(range(7)), [0, 1, 2]), (7, [0, 1, 2], [0, 1])]
    for D, R, K in cases:
        r = len(R); c0, G = fourier(D, K)
        tu = T_U(D, r, K)
        p = int(tu) + 1
        while not (is_prime(p) and p % D == 1): p += 1
        g = primitive_root(p)
        mo = moments(p, D, R, K, g)
        rho = [float(e2 / (e * e)) for e, e2 in mo]
        L = lhs_U(p, D, r, c0, G)
        pd = mpf(p)
        Dl = (G * G * sqrt(pd) + 2 * c0 * G + c0 * c0 / pd) * pd / (c0 * c0 * (pd - 1) ** 2)
        q = c0 * (pd - 1) / pd
        E0 = (pd - 1) / D * q ** (r - 1); EU = c0 * (pd - 1) * q ** (r - 1)
        b0 = float(1 / E0 + (1 + Dl) ** (r - 1)); bU = float(1 / EU + 1 + (r * Dl) ** 2 * exp(r * Dl) / 2)
        dm = delta_max(p, D, R, K, g)
        exact_sum = sum(x - 1 for x in rho)
        assert dm <= float(Dl) and rho[0] <= b0 and max(rho[1:]) <= bU and exact_sum <= float(L)
        rate = sample(p, D, R, K, g, 200, rng)
        print("D=%d R=%s K=%s T_U=%.1f p=%d: max|delta|=%.4f <= Delta=%.4f; rho_0=%.4f <= %.4f; max rho_j=%.4f <= %.4f; "
              "sum(rho_j-1)=%.4f <= LHS=%.4f; uniform beta success %.3f >= 1-LHS=%.3f" % (
              D, R, K, float(tu), p, dm, float(Dl), rho[0], b0, max(rho[1:]), bU, exact_sum, float(L), rate, 1 - float(L)), flush=True)
