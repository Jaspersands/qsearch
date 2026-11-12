"""Query-exponent checks for Theorem thm:main and the Outlook paragraph "Shorter zero sums".

(1) 145 at c = 9 from the paper's own B_d, G(d,a): exponent of m in c(m+tau) prod_d B_d(g_d)
    with g_d <= m is 1 + sum_{d=2}^c d*ceil(log2(d+1)).
(2) The variant: grade d charged G(kappa_d, g_d)^{L_d}, L_d = ceil(log2 t_d), t_d = least t with a
    nontrivial solution of z_1^k + ... + z_t^k = 0 in F_p, k = kappa_d = gcd(d, p-1).
    Exponent = 1 + sum_d kappa_d * L_d  (kappa_d = 1 -> linear algebra, arity a+1, exponent 1).
    Max over all primes p > c: exhaustive t_d for primes below the Weil threshold of every
    even kappa <= c, and for larger primes t_d in {2,3} by parity of (p-1)/kappa (Weil), so the
    exponent depends only on p mod 2*lcm(1..c); enumerate all unit residues (Dirichlet).
(3) Brute-force check of "t_d = 2 iff (p-1)/kappa even" and of the Weil claim t <= 3 above the
    threshold, for all primes up to PMAX.
"""
import math
from math import gcd, ceil, log2, isqrt
from functools import reduce

from sympy import primerange


def G(d, a):
    return d ** (d * (d - 1) // 2) * (a + 1) ** d


def B(d, a):
    return G(d, a) ** ceil(log2(d + 1))


def Lexp(d):
    return ceil(log2(d + 1))


def t_min(k, p):
    """least t >= 2 with nontrivial z_1^k+...+z_t^k = 0 in F_p (k | p-1).
    Sets S_j of sums of j nonzero k-th powers are stable under the subgroup P of k-th powers,
    so track them by coset class (x -> x^((p-1)/k), 0 -> 'zero')."""
    if k == 1:
        return 2
    e = (p - 1) // k
    P = [pow(z, k, p) for z in range(1, p) if pow(z, e * 0 + 1, p) is not None]
    P = sorted(set(P))
    cls = lambda x: 0 if x == 0 else pow(x, e, p)
    reps = {1: 1}  # class -> representative element ; S_1 = P
    for t in range(2, k + 2):
        new = {}
        for r in reps.values():
            for w in P:
                x = (r + w) % p
                c = cls(x)
                if c not in new:
                    new[c] = x
        if 0 in new:
            return t
        reps = new
    raise AssertionError("Chevalley-Warning violated")


def weil_ok(k, p):
    return p + 1 - (k - 1) * (k - 2) * math.sqrt(p) > 3 * k


def threshold(k):
    """least P with weil_ok(k, p) for all p >= P (monotone in p for p large)."""
    p = 2
    while not all(weil_ok(k, q) for q in range(p, p + 2000)):
        p += 1
    return p


def variant_exp(c, p, tcache):
    e = 1
    detail = []
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        if k == 1:
            e += 1; detail.append((d, 1, 1)); continue
        t = tcache(k, p)
        L = ceil(log2(t))
        e += k * L
        detail.append((d, k, L))
    return e, detail


def main():
    print("== (1) headline exponent from B_d ==")
    for c in range(2, 13):
        e = 1 + sum(d * Lexp(d) for d in range(2, c + 1))
        print(f"c={c}: 1+sum d*ceil(log2(d+1)) = {e}")
    c = 9
    # check B_d(g) <= d^{d(d-1)L/2}(m+1)^{dL} and C_c
    Cc = 1
    for d in range(2, c + 1):
        Cc *= d ** (d * (d - 1) * Lexp(d) // 2)
        for m in (1, 5, 19, 50):
            for g in range(0, m + 1):
                assert B(d, g) <= d ** (d * (d - 1) * Lexp(d) // 2) * (m + 1) ** (d * Lexp(d))
    print("C_9 = 2^%.1f" % log2(Cc))
    print("B_2(1)=%d B_2(3)=%d B_3(2)=%d B_4(2)=%.3e" % (B(2, 1), B(2, 3), B(3, 2), B(4, 2)))
    print("class-3 example: log2 Q = %.2f" % log2(3 * 6 * B(2, 3) * B(3, 2)))
    # monotonicity of B in d (Lemma bezout)
    for a in range(0, 30):
        for d in range(1, 12):
            assert B(d, a) <= B(d + 1, a)
    print("B_d(a) nondecreasing in d: ok (a<30, d<12); B_1(a)=a+1:", all(B(1, a) == a + 1 for a in range(50)))

    print("== (3) brute-force t_d facts ==")
    PMAX = 6000
    cache = {}
    def tc(k, p):
        if (k, p) not in cache:
            cache[(k, p)] = t_min(k, p)
        return cache[(k, p)]
    bad_parity = []
    bad_weil = []
    worst_t = {}
    for p in primerange(3, PMAX):
        for k in range(1, 10):
            if (p - 1) % k:
                continue
            t = tc(k, p)
            if (t == 2) != (((p - 1) // k) % 2 == 0):
                bad_parity.append((k, p, t))
            if weil_ok(k, p) and t > 3:
                bad_weil.append((k, p, t))
            worst_t[k] = max(worst_t.get(k, 0), t)
    print("parity rule violations:", bad_parity[:10], len(bad_parity))
    print("Weil-region t>3 violations:", bad_weil[:10], len(bad_weil))
    print("max t over primes < %d by kappa:" % PMAX, worst_t)
    thr = {k: threshold(k) for k in range(2, 10)}
    print("Weil thresholds (least p beyond which p+1-(k-1)(k-2)sqrt p > 3k):", thr)
    # t>4 cases (L>=3)
    big = sorted({(k, p, t) for (k, p), t in cache.items() if t > 4})
    print("cases with t > 4 (L >= 3):", big)

    print("== (2) variant exponent, max over primes p > c ==")
    for c in range(2, 13):
        P0 = max(thr[k] for k in range(2, min(c, 9) + 1)) if c <= 9 else None
        if c > 9:
            break
        best = (0, None, None)
        # exhaustive over primes up to max(P0, PMAX)
        for p in primerange(c + 1, max(P0, PMAX)):
            e, det = variant_exp(c, p, tc)
            if e > best[0]:
                best = (e, p, det)
        # large primes: exponent depends on p mod 2*lcm(1..c); t in {2,3} by parity
        Lc = reduce(lambda a, b: a * b // gcd(a, b), range(1, c + 1))
        mod = 2 * Lc
        def tpar(k, p):
            return 2 if ((p - 1) // k) % 2 == 0 else 3
        bestL = (0, None, None)
        for r in range(1, mod):
            if gcd(r, mod) != 1:
                continue
            # kappa_d = gcd(d, p-1) and parity of (p-1)/kappa depend on (p-1) mod 2*lcm
            e = 1; det = []
            pm1 = (r - 1) % mod
            for d in range(2, c + 1):
                k = gcd(d, pm1 if pm1 else mod)
                if k == 1:
                    e += 1; det.append((d, 1, 1)); continue
                t = 2 if ((pm1 // k) % 2 == 0 if pm1 else True) else 3
                # pm1 // k parity: (p-1)/k mod 2 equals (pm1/k) mod 2 since mod/k is even
                L = ceil(log2(t)); e += k * L; det.append((d, k, L))
            if e > bestL[0]:
                bestL = (e, r, det)
        print(f"c={c}: headline {1+sum(d*Lexp(d) for d in range(2,c+1))}; variant max small-p {best[0]} at p={best[1]}; "
              f"large-p max {bestL[0]} at p = {bestL[1]} mod {mod}  {bestL[2]}")


if __name__ == "__main__":
    main()
