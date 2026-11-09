"""Higher-moment (Bonferroni) certificate for the two-level contraction.

Notation as in 2026-11-02-rees-weil-threshold.md §1: chi of order kappa,
Q_b = {x != 0 : chi(x) = w^b}, h = (p-1)/kappa, y_0 = 0, y_1..y_{kappa-1}
uniform, n = n_0(y) = #{x in Q_0 : x + y_i in Q_{-i}, i = 1..kappa-1}.

Lemma D (factorial moments).  For 1 <= k,
    E[(n)_k] = sum over distinct (x_1..x_k) in Q_0 of prod_{i>=1} N_i(x)/p,
    N_i(x) = #{y : x_l + y in Q_{-i} for l = 1..k},
and |N_i(x) - (p-k)/kappa^k| <= E_k(p) := (k-1-k/kappa+kappa^-k) sqrt(p) + k/kappa - k kappa^-k.

Theorem 4 (Bonferroni).  With lam = (p-1)/kappa^kappa, q_k = kappa^-k (1-k/p),
eps_k = kappa^k E_k(p)/(p-k) and any even m >= 0,
    P(n = 0) <= B_m(p) := sum_{k=0}^m (-1)^k C(h,k) q_k^(kappa-1)
                          + sum_{k=1}^m C(h,k) q_k^(kappa-1) [(1+eps_k)^(kappa-1) - 1].
If kappa * B_m(p) < 1, a fraction >= 1 - kappa B_m(p) of y works for every column,
so p is not two-level exceptional.  Analytic form (used for asymptotics):
    B_m(p) <= e^-lam + lam^(m+1)/(m+1)! + (kappa-1) lam e^lam / p
              + sum_{k=1}^m lam^k/k! [(1+eps_k)^(kappa-1) - 1].

Modes:
  check K pmax      brute force over all y for primes p = 1 mod K, p <= pmax:
                    exact factorial moments vs Lemma D, exact P(n=0) vs B_m.
  table Kmin Kmax   smallest p (real, bisection) with kappa*B_m(p) < 1 for the
                    best even m, from the exact finite form B_m and from the
                    analytic form; compares with T_A ~ (kappa-1)kappa^kappa.
"""
import sys
from fractions import Fraction
from math import comb, exp, factorial, log, sqrt, lgamma

import mpmath as mp

mp.mp.dps = 60


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def primroot(p):
    n, f, q = p - 1, [], 2
    while q * q <= n:
        if n % q == 0:
            f.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        f.append(n)
    g = 2
    while any(pow(g, (p - 1) // r, p) == 1 for r in f):
        g += 1
    return g


def coset_index(p, K):
    g = primroot(p)
    idx = [-1] * p
    x = 1
    for e in range(p - 1):
        idx[x] = e % K
        x = x * g % p
    return idx


def E_k(p, K, k):
    return (k - 1 - k / K + K ** (-k)) * sqrt(p) + k / K - k * K ** (-k)


def B_exact(p, K, m):
    """Finite form B_m(p), high precision (p may be real for bisection)."""
    p = mp.mpf(p)
    h = (p - 1) / K
    tot = mp.mpf(0)
    err = mp.mpf(0)
    for k in range(0, m + 1):
        ch = mp.binomial(h, k)
        qk = mp.mpf(K) ** (-k) * (1 - k / p)
        a = ch * qk ** (K - 1)
        tot += (-1) ** k * a
        if k >= 1:
            eps = mp.mpf(K) ** k * ((k - 1 - mp.mpf(k) / K + mp.mpf(K) ** (-k)) * mp.sqrt(p)
                                     + mp.mpf(k) / K - k * mp.mpf(K) ** (-k)) / (p - k)
            err += a * ((1 + eps) ** (K - 1) - 1)
    return tot + err


def B_analytic(p, K, m):
    p = mp.mpf(p)
    lam = (p - 1) / mp.mpf(K) ** K
    s = mp.e ** (-lam) + lam ** (m + 1) / mp.factorial(m + 1) + (K - 1) * lam * mp.e ** lam / p
    for k in range(1, m + 1):
        eps = mp.mpf(K) ** k * ((k - 1 - mp.mpf(k) / K + mp.mpf(K) ** (-k)) * mp.sqrt(p)
                                 + mp.mpf(k) / K - k * mp.mpf(K) ** (-k)) / (p - k)
        s += lam ** k / mp.factorial(k) * ((1 + eps) ** (K - 1) - 1)
    return s


def check(K, pmax):
    from itertools import product
    for p in primes_upto(pmax):
        if p < 3 or (p - 1) % K:
            continue
        idx = coset_index(p, K)
        Q0 = [x for x in range(1, p) if idx[x] == 0]
        h = len(Q0)
        # Rows i >= 1 are independent: for each x, row i accepts the set
        # S_i(x) = {y : x + y in Q_{-i}}.  n(y) = #{x : y_i in S_i(x) for all i}.
        # Enumerate y exactly.
        rowsets = [[(-i) % K for _ in range(1)] for i in range(K)]
        dist = {}
        fm_emp = [Fraction(0)] * 6
        count = 0
        for y in product(range(p), repeat=K - 1):
            n = 0
            for x in Q0:
                ok = True
                for i in range(1, K):
                    v = (x + y[i - 1]) % p
                    if v == 0 or idx[v] != (-i) % K:
                        ok = False
                        break
                if ok:
                    n += 1
            dist[n] = dist.get(n, 0) + 1
            count += 1
        tot = count
        p0 = Fraction(dist.get(0, 0), tot)
        out = [f"K={K} p={p} h={h} P(n=0)={float(p0):.4f}"]
        for k in range(1, 5):
            fk = Fraction(sum(c * _ff(n, k) for n, c in dist.items()), tot)
            main = Fraction(_ff(h, k)) * (Fraction(p - k, p * K ** k)) ** (K - 1)
            eps = K ** k * E_k(p, K, k) / (p - k) if p > k else float("inf")
            lo = float(main) * max(0.0, 1 - eps) ** (K - 1)
            hi = float(main) * (1 + eps) ** (K - 1)
            ok = lo - 1e-12 <= float(fk) <= hi + 1e-12
            out.append(f"E(n)_{k}={float(fk):.4g} in[{lo:.3g},{hi:.3g}]:{'ok' if ok else 'FAIL'}")
        bs = []
        for m in (0, 2, 4):
            b = float(B_exact(p, K, m))
            bs.append(f"B_{m}={b:.4f}{'' if b >= float(p0) - 1e-12 else '(FAIL)'}")
        print(" ".join(out + bs), flush=True)


def _ff(n, k):
    r = 1
    for t in range(k):
        r *= n - t
    return r


def threshold(K, form, mmax=80):
    f = B_exact if form == "exact" else B_analytic
    best = None
    for m in range(0, mmax + 1, 2):
        def good(p):
            try:
                return K * f(p, K, m) < 1
            except Exception:
                return False
        hi = mp.mpf(K) ** (K + 2)
        if not good(hi):
            continue
        lo = mp.mpf(K) ** (K - 1)
        if good(lo):
            best = (lo, m) if best is None or lo < best[0] else best
            continue
        for _ in range(200):
            mid = (lo + hi) / 2
            if good(mid):
                hi = mid
            else:
                lo = mid
            if hi - lo < 1e-6 * hi:
                break
        # monotone check on a grid above hi (the bound need not be monotone in p)
        grid_ok = all(good(hi * (1 + mp.mpf(t) / 50)) for t in range(0, 200))
        if grid_ok and (best is None or hi < best[0]):
            best = (hi, m)
    return best


def table(K0, K1):
    print("kappa | T_B exact-form (best m) | T_B analytic (best m) | (kappa-1)kappa^kappa | kappa^kappa ln kappa | ratio T_A/T_B")
    for K in range(K0, K1 + 1):
        be = threshold(K, "exact")
        ba = threshold(K, "analytic")
        ta = (K - 1) * mp.mpf(K) ** K
        fmt = lambda b: "none" if b is None else f"{mp.nstr(b[0], 5)} (m={b[1]})"
        r = "-" if be is None else mp.nstr(ta / be[0], 4)
        print(f"{K} | {fmt(be)} | {fmt(ba)} | {mp.nstr(ta, 5)} | {mp.nstr(mp.mpf(K) ** K * mp.log(K), 5)} | {r}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "check":
        check(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == "table":
        table(int(sys.argv[2]), int(sys.argv[3]))
