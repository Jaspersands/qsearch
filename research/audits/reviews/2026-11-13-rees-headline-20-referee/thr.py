"""Lemma SM thresholds (fragment.tex lem:sm) in exact rational arithmetic, written by the
headline-20 referee from the lemma text only.  sqrt(p) is bracketed by integer square roots
scaled by 10^40, so Phi_up uses a lower bound of sqrt(p) (gamma upper) and Phi_lo an upper bound."""
from fractions import Fraction as Fr
from math import isqrt
import sys
SC = 10**40
def sqrt_br(p):
    s = isqrt(p * SC * SC)
    return Fr(s, SC), Fr(s + 1, SC)
def quantities(p, D, r, k, sq):
    p = Fr(p)
    gam = (1 + Fr((D - 1) ** 2) / sq) * p * p / ((p - 1) ** 2)
    h = (p - 1) / D
    mu0 = h * (k * h / p) ** (r - 1)
    mu1 = k * h * (k * h / p) ** (r - 1)
    rho0 = 1 / mu0 + gam ** (r - 1)
    rho1 = 1 / mu1 + gam ** (r - 1)
    Phi = (1 - 1 / rho0) + (D - 1) * (1 - 1 / rho1)
    Psi = 4 * (rho0 - 1) + 4 * (D - 1) * (rho1 - 1)
    return Phi, Psi
def Phi_up(p, D, r, k): lo, hi = sqrt_br(p); return quantities(p, D, r, k, lo)[0]
def Phi_lo(p, D, r, k): lo, hi = sqrt_br(p); return quantities(p, D, r, k, hi)[0]
def Psi_up(p, D, r, k): lo, hi = sqrt_br(p); return quantities(p, D, r, k, lo)[1]
def Psi_lo(p, D, r, k): lo, hi = sqrt_br(p); return quantities(p, D, r, k, hi)[1]
def bisect(f, lo, hi):
    # least integer n in (lo, hi] with f(n) True, f monotone False->True
    assert not f(lo) and f(hi)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if f(m): hi = m
        else: lo = m
    return hi
def thresholds(D, r, k):
    Te = bisect(lambda n: Phi_up(n, D, r, k) < 1, 10, 10**12)
    assert Phi_lo(Te - 1, D, r, k) >= 1, "bracket not tight at T_exist"
    Ts = bisect(lambda n: Psi_up(n, D, r, k) <= Fr(1, 2), 10, 10**13)
    assert Psi_lo(Ts - 1, D, r, k) > Fr(1, 2), "bracket not tight at T_samp"
    return Te, Ts
def isprime(n):
    if n < 2: return False
    d = 2
    while d * d <= n:
        if n % d == 0: return False
        d += 1
    return True
if __name__ == "__main__":
    rows = [("TL3", 3, 3, 1), ("TL4", 4, 4, 1), ("TL5", 5, 5, 1), ("TW9", 9, 3, 1), ("U7", 7, 7, 2),
            ("TL6", 6, 6, 1), ("TL7", 7, 7, 1), ("TL8", 8, 8, 1), ("TL9", 9, 9, 1)]
    for name, D, r, k in rows:
        Te, Ts = thresholds(D, r, k)
        print(name, (D, r, k), "T_exist", Te, "T_samp", Ts)
    # band check for TL6
    D, r, k = 6, 6, 1
    Te, Ts = thresholds(D, r, k)
    q = Te
    while not (isprime(q) and q % 6 == 1): q += 1
    v = 1 - Phi_up(q, D, r, k)
    print("TL6 least prime =1 mod 6 >= T_exist:", q, "1-Phi_up =", float(v), "> 1.6e-5:", v > Fr(16, 10**6))
    # monotonicity spot check of Phi_up on primes =1 mod 6 in the band (sample)
    import random
    random.seed(1)
    xs = sorted(random.sample(range(Te, Ts), 200))
    vals = [Phi_up(x, D, r, k) for x in xs]
    print("Phi_up decreasing on 200 sampled points of band:", all(a >= b for a, b in zip(vals, vals[1:])))
    print("max Phi_up on band sample < 1:", max(vals) < 1, float(max(vals)))
    # least prime =1 mod 2520 above T_exist
    q = Te
    while not (isprime(q) and q % 2520 == 1): q += 1
    print("least prime =1 mod 2520 >= T_exist:", q, "1-Phi_up =", float(1 - Phi_up(q, D, r, k)))
