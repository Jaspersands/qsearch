"""Independent recomputation (written from the text of rem:fc-witness-h3(b) and rem:fc-zero-sum-arity(b),
not from hcheck.py) of log2 Q for Theorem free-coordinate(iii) with the weight-doubling node at every grade
of Gamma_F, the linear node at Gamma_1 (class-nine profile, eps = 1/3, the six primes of tab:fcs-budget).

Node arity: M_d = t + k_b * L with t = g_d + ceil(log_p(2/tau_d)) span labels, k_b = ceil(log2(2/tau_d))
blocks of L = ceil(2 Nbar_0(g_d)) labels; tau_d = eps / (9 (c-1) S n_d), n_d = prod_{d'<d} M_d'.
Rescaled form iff sqrt(p) >= 2(kappa-1)(kappa-2)+4: Nbar_0(n) = 1 + ceil(log2 p) * p/(p-1) * n(n+1)/2.
Otherwise tables: Nbar_0 = N_0 with sigma = min(p, ceil(2 log2(p-1)) + 4), N_J(n) = n + 1 at J = j*_h,
N_j(n) = 1 + sigma * sum_{e<n} N_{j+1}(e).
"""
import json
import math
import sys
from fractions import Fraction as F
from math import gcd

PROFILE = (19, 17, 16, 14, 12, 9, 6, 3, 1)
EPS = F(1, 3)
PRIMES = [("11", 11), ("1031", 1031), ("5281", 5281), ("2^31-1", 2 ** 31 - 1), ("2^61-1", 2 ** 61 - 1),
          ("2^127-1", 2 ** 127 - 1)]


def clog(base, x):  # least j >= 0 with base^j >= x (x rational)
    j = 0
    while F(base) ** j < x:
        j += 1
    return j


def jstar(p, h):
    D = {pow(x, (p - 1) // h * 0 + 1, p) for x in []}
    # mu_h u {0}: h-th roots of unity = kappa-th powers
    k = (p - 1) // h
    D = {pow(x, k, p) for x in range(1, p)} | {0}
    j = 0
    while len(D) < p:
        D = {(x - y) % p for x in D for y in D}
        j += 1
    return j


def N0_table(J, sigma, n):
    # N_j(e) for e = 0..n, j = J down to 0
    N = [F(e + 1) for e in range(n + 1)]
    for _ in range(J):
        pref, new = F(0), []
        for e in range(n + 1):
            new.append(1 + sigma * pref)
            pref += N[e]
        N = new
    return N[n]


def run(p):
    c, m = len(PROFILE), PROFILE[0]
    S = m + clog(p, 3 / EPS)
    acc, grades = 1, {}
    for d in range(2, c + 1):
        g = PROFILE[d - 1]
        k = gcd(d, p - 1)
        if k == 1:
            M, how = g + 1, "lin"
        else:
            assert k < p - 1
            h = (p - 1) // k
            tau = EPS / (9 * (c - 1) * S * acc)
            A = 2 * (k - 1) * (k - 2) + 4
            if p >= A * A:
                Nbar = 1 + (p - 1).bit_length() * F(p, p - 1) * F(g * (g + 1), 2)
                how = "rescaled"
            else:
                sigma = min(p, math.ceil(2 * math.log2(p - 1)) + 4)
                J = jstar(p, h)
                Nbar = N0_table(J, F(sigma), g)
                how = f"tables j*={J}"
            L = -(-2 * Nbar.numerator // Nbar.denominator)
            M = g + clog(p, 2 / tau) + clog(2, 2 / tau) * L
        grades[d] = (M, how)
        acc *= M
    Q = c * S * acc
    return round(math.log2(Q), 1), grades


if __name__ == "__main__":
    res = {}
    for lab, p in PRIMES:
        q, gr = run(p)
        res[lab] = dict(log2Q=q, grades={d: [M, how] for d, (M, how) in gr.items()})
        print(lab, q, {d: how for d, (M, how) in gr.items()})
    json.dump(res, open(sys.argv[1], "w"), indent=1)
