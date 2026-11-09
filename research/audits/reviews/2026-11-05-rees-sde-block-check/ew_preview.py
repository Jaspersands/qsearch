"""E_W(c) preview for a Theorem C ('random-label two-level') option.

E_W(c) = max_{p > c} (1 + sum_{d=2}^c e_d(p)), e_d(p) the exponent of (g_d+1) in a per-grade bound valid
for ALL g_d at that p (Theorem bb-envelope / Lemma tb-count-grade).  Theorem C's guards (p >= 64 g^2 at
kappa = 2, p >= max(2750, 1000 g^2) at kappa = 3, and the bank union bound) grow with g_d, so at a fixed
p the option is unavailable for large g_d and e_d(p) is unchanged: E_W^true = paper values.

HYPOTHETICAL (deliberately over-generous, NOT a valid reading): pretend the option had the g-independent
guard 'p not in E_cg(E, kappa)' with E = max(3, kappa) (E_cg(3,2) = {}, E_cg(3,3) = 22 primes <= 241,
p >= p_W(kappa,kappa) for kappa >= 4) and exponent 2.  This shows what would be at stake.
"""
import math
from functools import reduce
from math import gcd

from sympy import isprime, primerange

ECG33 = {7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 211, 241}
PAPER = [5, 11, 23, 38, 56, 77, 107, 143]


def clog2(x):
    return (x - 1).bit_length()


def T2(k):
    return 16 * k ** (2 * k + 2)


def p_weil(k, E):
    def ok(p):
        return all(p - e > (k ** e - 1) * (e - 1) * math.sqrt(p) for e in range(2, E + 1))
    lo, hi = 2, 2
    while not ok(hi):
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


PW = {k: p_weil(k, max(3, k)) for k in range(2, 10)}


def e_d(d, p, hypo):
    k = gcd(d, p - 1)
    if k == 1:
        return 1
    if p >= T2(k):
        return 2
    if hypo:
        if k == 2 or (k == 3 and p not in ECG33) or (k >= 4 and p >= PW[k]):
            return 2
    return k * clog2(k + 1)


def EW(c, hypo, direct_to=300000):
    best, arg = 0, None
    for p in primerange(c + 1, direct_to):
        v = 1 + sum(e_d(d, p, hypo) for d in range(2, c + 1))
        if v > best:
            best, arg = v, p
    # above direct_to: e_d depends only on p mod L and the threshold interval
    L = reduce(lambda a, b: a * b // gcd(a, b), range(2, c + 1), 1)
    ths = sorted({T2(k) for k in range(2, c + 1)} | ({PW[k] for k in range(4, c + 1)} if hypo else set()))
    ths = [t for t in ths if t > direct_to]
    bounds = [direct_to] + ths
    for lo in bounds:
        for u in range(1, L + 1):
            if gcd(u, L) != 1:
                continue
            q = lo + ((u - lo) % L)
            while not isprime(q):
                q += L
            v = 1 + sum(e_d(d, q, hypo) for d in range(2, c + 1))
            if v > best:
                best, arg = v, q
    return best, arg


if __name__ == "__main__":
    print("p_W(max(3,k),k):", PW)
    true_vals, hyp = [], []
    for c in range(2, 10):
        true_vals.append(EW(c, False))
        hyp.append(EW(c, True))
    print("E_W (paper guards, = Theorem C option under its true g-dependent guards):", [v for v, _ in true_vals])
    assert [v for v, _ in true_vals] == PAPER
    print("E_W hypothetical g-independent guard                                    :", [v for v, _ in hyp],
          "witness p:", [p for _, p in hyp])
