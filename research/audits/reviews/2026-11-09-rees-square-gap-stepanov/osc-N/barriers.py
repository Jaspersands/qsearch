"""Barrier numerics for the osc-N report (returned as text to the parent; no REPORT.md written) section 2.

(a) O1-N (full space).  A modulus-only (term-by-term) certificate built on the full-space kernel identity
    gives  value <= 2(mu' - W_deg) - N1_lab  (proved), so it fails whenever W_deg >= mu' = p^{2k}/k^{(k-1)^2}.
    Rigorous lower bound used for W_deg (disjoint strata, weight 1, separable automatically or by
    construction):
      - alpha all equal, cells nonzero:  p (p-1)^k ; beta all equal likewise; overlap p(p-1)
      - alpha with exactly one coincident pair (else distinct), beta distinct, no zero cell, separable:
        C(k,2) * N_{k x (k-1)},  N_{k x (k-1)} >= (p)_{k-1} * G(p-k+1, k^{k-2})   (Jensen on buckets)
        and the transpose stratum likewise.
    Prints the largest prime p = 1 mod k (scanning up to a bound) at which the barrier still holds,
    against the pigeonhole bound (k-1)k^{k-1}+k-1.
(b) Exact bucket-moment barrier: given the exact averaged factorial moments Lambda_1..Lambda_{k-1}
    (from bucket_cert.py exact), the unique law on {0..k-1} with those per-bucket factorial moments;
    if all atoms are >= 0 no bucket-moment certificate (moments of order <= k-1) can decide.
Usage: python barriers.py o1n kmin kmax | python barriers.py lp k p Lambda_1 ... Lambda_{k-1}
"""
import sys, math


def ff(x, n):
    r = 1
    for i in range(n):
        r *= (x - i)
    return r


def ffpos(x, n):
    return ff(x, n) if x >= n else 0


def balanced(nsum, D, k):
    q, r = divmod(nsum, D)
    return (D - r) * ffpos(q, k) + r * ffpos(q + 1, k)


def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True


def wdeg_low(k, p):
    a = 2 * p * (p - 1) ** k - p * (p - 1)
    b = 2 * math.comb(k, 2) * ff(p, k - 1) * balanced(p - k + 1, k ** (k - 2), k)
    return a + b


def holds(k, p):
    return wdeg_low(k, p) * k ** ((k - 1) ** 2) >= p ** (2 * k)


def o1n(kmin, kmax):
    """largest integer p = 1 mod k (primality ignored) at which the rigorous W_deg lower bound
    is >= mu'; found by bisection (the ratio W_deg_low/mu' decreases in p in this range; checked by
    sampling 50 points below the crossing)."""
    print("k  pigeonhole  crossing P_N   (k-1)k^k   P_N/pigeonhole  primes<=P_N with barrier (k<=4: listed)")
    for k in range(kmin, kmax + 1):
        pig = (k - 1) * k ** (k - 1) + k - 1
        lo, hi = 0, 8 * (k - 1) * k ** k // k  # p = 1 + k*n
        assert holds(k, 1 + k * 2) and not holds(k, 1 + k * hi)
        lo = 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if holds(k, 1 + k * mid): lo = mid
            else: hi = mid
        P = 1 + k * lo
        mono = all(holds(k, 1 + k * max(2, (lo * i) // 50)) for i in range(1, 51))
        extra = ''
        if k <= 4:
            extra = ' '.join(str(q) for q in range(k + 1, P + 1) if q % k == 1 and isprime(q) and holds(k, q))
        print(f'{k:2d}  {pig:10d}  {P:12d}  {(k-1)*k**k:12d}   {P/pig:.3f}   monotone-sample:{mono}  {extra}', flush=True)


def lp(k, p, lams):
    D = k ** (k - 1)
    phi = [1.0] + [x / D for x in lams]  # phi_m = per-bucket factorial moments, m = 0..k-1
    K = k - 1
    P = []
    for j in range(K + 1):
        P.append(sum((-1) ** (m - j) * math.comb(m, j) * phi[m] / math.factorial(m) for m in range(j, K + 1)))
    ok = all(x >= -1e-12 for x in P)
    print(f'k={k} p={p}: law on 0..{K}: ' + ' '.join(f'{x:.4g}' for x in P) + ('  REALIZABLE (no bucket-moment certificate)' if ok else '  not realizable (moment certificate exists)'))


if __name__ == '__main__':
    if sys.argv[1] == 'o1n':
        o1n(int(sys.argv[2]), int(sys.argv[3]))
    else:
        k = int(sys.argv[2]); p = int(sys.argv[3])
        lp(k, p, [float(x) for x in sys.argv[4:]])
