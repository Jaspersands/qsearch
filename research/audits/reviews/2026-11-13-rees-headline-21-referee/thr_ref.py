"""Referee recomputation of Lemma SM thresholds (independent code, exact rational + interval sqrt).
Phi(p) < 1 decided with p as an integer using Fraction arithmetic and a rigorous upper bound on sqrt."""
from fractions import Fraction as Fr
from math import isqrt
import sys

def sqrt_lower(p):  # rational lower bound for sqrt(p) (so (D-1)^2/sqrt p is upper-bounded)
    s = isqrt(p * 10**12)
    return Fr(s, 10**6)

def rho_up(p, D, r, k, j0):
    h = Fr(p - 1, D)
    gam = (1 + Fr((D - 1) ** 2) / sqrt_lower(p)) * Fr(p, p - 1) ** 2
    mu = (h if j0 else k * h) * (k * h / p) ** (r - 1)
    return 1 / mu + gam ** (r - 1)

def Phi(p, D, r, k):
    r0 = rho_up(p, D, r, k, True); r1 = rho_up(p, D, r, k, False)
    return (1 - 1 / r0) + (D - 1) * (1 - 1 / r1), r0, r1

def Psi(p, D, r, k):
    r0 = rho_up(p, D, r, k, True); r1 = rho_up(p, D, r, k, False)
    return 4 * (r0 - 1) + 4 * (D - 1) * (r1 - 1)

def first(f, D, r, k, bound):
    lo, hi = D + 2, 10 ** 12
    while hi - lo > 1:
        mid = (lo + hi) // 2
        v = f(mid, D, r, k); v = v[0] if isinstance(v, tuple) else v
        if v < bound: hi = mid
        else: lo = mid
    return hi

def isprime(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % q == 0: return n == q
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

STEPS = [('TL3',3,3,1),('TL4',4,4,1),('TL5',5,5,1),('TW9 (9;{0,3,6})',9,3,1),('U7 (7;Z7->{0,m})',7,7,2)]
for name, D, r, k in STEPS:
    T = first(Phi, D, r, k, 1)
    TS = first(Psi, D, r, k, Fr(1, 2))
    # first prime = 1 mod D at or above T, and 1-Phi there
    q = T
    while not (q % D == 1 and isprime(q)): q += 1
    ph, r0, r1 = Phi(q, D, r, k)
    # largest prime = 1 mod D below T (must be uncertified-or-table)
    print(f'{name:20s} T_exist={T:>10d} T_samp={TS:>11d}  first prime>=T: {q}  1-Phi={float(1-ph):.3e}  '
          f'Phi(T-1)={float(Phi(T-1,D,r,k)[0]):.6f} Phi(T)={float(Phi(T,D,r,k)[0]):.6f}  p/mu0 bound (2D)^r={(2*D)**r}')
