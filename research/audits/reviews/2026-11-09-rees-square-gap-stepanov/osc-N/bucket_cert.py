"""Bucket-moment certificate for (C1) existence below the pigeonhole bound (the osc-N report (returned as text to the parent; no REPORT.md written) section 3).

S = (s_1..s_k) distinct in F_p; for t notin S the profile (ind(s_j - t))_j mod the diagonal is its bucket
c in G = Z_k^k / diag, |G| = D = k^(k-1).  b_c(S) = bucket size, sum_c b_c = p - k.
(C1) exists  <=>  some S has a bucket with >= k points.
Lambda_M := E_S sum_c (b_c(S))_M   (falling factorial; E over ordered distinct S).

Double counting:  Lambda_M = (p)_M / (p)_k * avg_T sum_{d in Z_k^{M-1}} (n_d(T))_k,
  n_d(T) = #{s notin T : ind((s-t_a)/(s-t_1)) = d_a, a = 2..M},   sum_d n_d(T) = p - M.
Lower bound (discrete Jensen, no Weil):  sum_d (n_d)_k >= balanced value  G(p-M, k^(M-1)).
Exact: Lambda_1 = p - k;  Lambda_2 = p(p-1)[(h-1)_k + (k-1)(h)_k]/(p)_k  (two-point bijection).
Upper bound (Weil, M >= 3): |n_d - (p-M)/k^(M-1)| <= (1 - k^(1-M))(M-1) sqrt(p).
If no bucket >= k then (b)_M <= (k-1-m)_{M-m} (b)_m for every bucket, hence
CERT(m, M):  Lambda_M^low > (k-1-m)_{M-m} * Lambda_m^up   implies (C1) exists.

Usage:
  python bucket_cert.py primes k pmax        # certificate at each prime p = 1 mod k, p <= pmax
  python bucket_cert.py asym kmin kmax        # smallest certified lambda = (p-k)/k^(k-1), real p
  python bucket_cert.py exact k p1 p2 ...     # exact Lambda_M, max bucket, C1 existence (small k, p)
"""
import sys, math, itertools
import numpy as np


def ff(x, n):
    r = 1
    for i in range(n):
        r *= (x - i)
    return r


def ffpos(x, n):  # falling factorial, 0 if x < n (integers)
    return ff(x, n) if x >= n else 0


def balanced(nsum, D, k):  # min of sum_d (n_d)_k over nonneg integers, sum = nsum, D parts
    q, r = divmod(nsum, D)
    return (D - r) * ffpos(q, k) + r * ffpos(q + 1, k)


def chord_upper(nsum, D, k, lo, hi):  # max of sum (n_d)_k with lo <= n_d <= hi, sum fixed (chord bound)
    lo = max(0, lo)
    if hi <= lo:
        return D * ffpos(hi, k)
    glo, ghi = ffpos(lo, k), ffpos(hi, k)
    return D * glo + (nsum - D * lo) * (ghi - glo) / (hi - lo)


def lam_low(k, p, M):
    if M == 1:
        return p - k
    return ff(p, M) * balanced(p - M, k ** (M - 1), k) / ff(p, k)


def lam_up(k, p, m):
    h = (p - 1) // k
    if m == 1:
        return p - k
    if m == 2:
        return p * (p - 1) * (ffpos(h - 1, k) + (k - 1) * ffpos(h, k)) / ff(p, k)
    D = k ** (m - 1)
    nbar = (p - m) / D
    E = (1 - k ** (1 - m)) * (m - 1) * math.sqrt(p)
    return ff(p, m) * chord_upper(p - m, D, k, math.ceil(nbar - E), math.floor(nbar + E)) / ff(p, k)


def cert(k, p):
    """returns list of (m, M, ratio) with ratio = Lambda_M^low / ((k-1-m)_{M-m} Lambda_m^up) > 1"""
    out = []
    for M in range(2, k):
        lo = lam_low(k, p, M)
        for m in range(1, M):
            if m == 2 and M == 2:
                continue
            up = lam_up(k, p, m)
            c = ff(k - 1 - m, M - m)
            if c == 0 or up <= 0:
                continue
            out.append((m, M, lo / (c * up)))
    # also exact Lambda_2 as the LOWER side (it is exact):
    if k >= 3:
        l2 = lam_up(k, p, 2)
        out.append((1, 2, l2 / ((k - 2) * (p - k))))
    return out


def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True


def run_primes(k, pmax):
    pig = (k - 1) * k ** (k - 1) + k - 1
    print(f'k={k}: pigeonhole certifies p > {pig}')
    first_always = None
    for p in range(k + 1, pmax + 1):
        if p % k != 1 or not isprime(p):
            continue
        cs = cert(k, p)
        best = max(cs, key=lambda c: c[2]) if cs else (0, 0, 0)
        ok = best[2] > 1
        lam = (p - k) / k ** (k - 1)
        print(f'  p={p:6d} lambda={lam:.3f} best (m,M)=({best[0]},{best[1]}) ratio={best[2]:.4f} {"CERTIFIED" if ok else ""}  pigeonhole:{"yes" if p > pig else "no"}', flush=True)


def lgff(x, n):  # log of falling factorial for real x > n-1 (direct sum: lgamma differences cancel badly)
    return sum(math.log(x - i) for i in range(n))


def cert_real(k, lam, use_weil=True):
    """log-scale certificate at real p = k + lam k^(k-1); returns best margin (log) and (m, M)"""
    p = k + lam * k ** (k - 1)
    best = (-1e300, None)
    lp = lambda M: lgff(p, M) - lgff(p, k)
    for M in range(2, k):
        D = k ** (M - 1)
        nbar = (p - M) / D
        if nbar <= k - 1:
            continue
        llo = lp(M) + math.log(D) + lgff(nbar, k)  # Jensen: D * (nbar)_k
        cands = [(1, math.log(p - k))]
        h = (p - 1) / k
        if h - 1 > k - 1:
            cands.append((2, lgff(p, 2) - lgff(p, k) + math.log(math.exp(lgff(h - 1, k) - lgff(h, k)) + (k - 1)) + lgff(h, k)))
        if use_weil:
            for m in range(3, M):
                Dm = k ** (m - 1)
                nb = (p - m) / Dm
                E = (m - 1) * math.sqrt(p)
                top = max(nb + E, k)
                cands.append((m, lp(m) + math.log(Dm) + lgff(top, k)))
        for m, lup in cands:
            if m >= M:
                continue
            c = ff(k - 1 - m, M - m)
            if c <= 0:
                continue
            marg = llo - math.log(c) - lup
            if marg > best[0]:
                best = (marg, (m, M))
    return best


def run_asym(kmin, kmax):
    print('k  lam_pig=k-1  lam*(Jensen m=1)  lam*(+exact 2pt)  lam*(+Weil)  ((k-2)!)^(1/(k-2))  k/(2e)   pig/cert(Weil)')
    for k in range(kmin, kmax + 1):
        res = []
        for mode in ('j', 'j2', 'w'):
            lo, hi = 1e-3, float(k)
            for _ in range(60):
                mid = (lo + hi) / 2
                if mode == 'j':
                    b = cert_real_mode(k, mid, maxm=1)
                elif mode == 'j2':
                    b = cert_real_mode(k, mid, maxm=2)
                else:
                    b = cert_real_mode(k, mid, maxm=k)
                if b[0] > 0:
                    hi = mid
                else:
                    lo = mid
            res.append(hi)
        g = math.exp(math.lgamma(k - 1) / (k - 2)) if k > 2 else float('nan')
        print(f'{k:3d}  {k-1:5d}  {res[0]:10.4f}  {res[1]:10.4f}  {res[2]:10.4f}  {g:10.4f}  {k/(2*math.e):8.4f}  {(k-1)/res[2]:7.3f}', flush=True)


def cert_real_mode(k, lam, maxm):
    p = k + lam * k ** (k - 1)
    best = (-1e300, None)
    lp = lambda M: lgff(p, M) - lgff(p, k)
    h = (p - 1) / k
    for M in range(2, k):
        D = k ** (M - 1)
        nbar = (p - M) / D
        if nbar <= k - 1:
            continue
        llo = lp(M) + math.log(D) + lgff(nbar, k)
        if M == 2 and h - 1 > k - 1:  # exact two-point value
            llo = lgff(p, 2) - lgff(p, k) + math.log(math.exp(lgff(h - 1, k) - lgff(h, k)) + (k - 1)) + lgff(h, k)
        cands = [(1, math.log(p - k))]
        if maxm >= 2 and h - 1 > k - 1:
            cands.append((2, lgff(p, 2) - lgff(p, k) + math.log(math.exp(lgff(h - 1, k) - lgff(h, k)) + (k - 1)) + lgff(h, k)))
        for m in range(3, min(M, maxm + 1)):
            Dm = k ** (m - 1)
            nb = (p - m) / Dm
            E = (m - 1) * math.sqrt(p)
            top = max(nb + E, k)
            cands.append((m, lp(m) + math.log(Dm) + lgff(top, k)))
        for m, lup in cands:
            if m >= M:
                continue
            c = ff(k - 1 - m, M - m)
            if c <= 0:
                continue
            marg = llo - math.log(c) - lup
            if marg > best[0]:
                best = (marg, (m, M))
    return best


def primroot(p):
    n = p - 1; fac = []; d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac): return g


def run_exact(k, primes):
    """exact Lambda_M for M <= k over all normalised S (s_1 = 0, s_2 = 1; affine maps preserve buckets)"""
    for p in primes:
        g = primroot(p)
        ind = np.full(p, -1, dtype=np.int64)
        x = 1
        for e in range(p - 1):
            ind[x] = e % k; x = x * g % p
        D = k ** (k - 1)
        rest = np.array(list(itertools.permutations(range(2, p), k - 2)), dtype=np.int64)
        Ss = np.concatenate([np.zeros((len(rest), 1), dtype=np.int64), np.ones((len(rest), 1), dtype=np.int64), rest], axis=1)
        xs = np.arange(p)
        lam_sum = np.zeros(k + 1)
        maxb = 0; nS = 0
        chunk = max(1, 2000000 // (p * k))
        for s0 in range(0, len(Ss), chunk):
            S = Ss[s0:s0 + chunk]
            cells = (S[:, None, :] - xs[None, :, None]) % p  # s_j - t
            ic = ind[cells]
            ok = (ic >= 0).all(axis=2)
            rel = (ic - ic[:, :, :1]) % k
            cl = (rel[:, :, 1:] * (k ** np.arange(k - 1))).sum(axis=2)
            cl = np.where(ok, cl, D)
            n = S.shape[0]
            flat = cl + (D + 1) * np.arange(n)[:, None]
            B = np.bincount(flat.ravel(), minlength=n * (D + 1)).reshape(n, D + 1)[:, :D].astype(np.float64)
            maxb = max(maxb, int(B.max()))
            cur = np.ones_like(B)
            for M in range(1, k + 1):
                cur = cur * (B - (M - 1))
                lam_sum[M] += cur.sum()
            nS += n
        lam = (p - k) / k ** (k - 1)
        print(f'k={k} p={p} lambda={lam:.4f} max bucket={maxb} C1 {"EXISTS" if maxb >= k else "none"}', flush=True)
        for M in range(1, k + 1):
            exact = lam_sum[M] / nS
            low = lam_low(k, p, M) if M < k + 1 else float('nan')
            pois = (p - k) * lam ** (M - 1)
            print(f'   M={M}: Lambda_M={exact:.6g}  Jensen-low={low:.6g}  Poisson (p-k)lam^(M-1)={pois:.6g}'
                  + (f'  Weil-up={lam_up(k, p, M):.6g}' if 1 < M < k else ''), flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'primes':
        run_primes(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == 'asym':
        run_asym(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == 'exact':
        run_exact(int(sys.argv[2]), [int(a) for a in sys.argv[3:]])


def quant(k, p):
    """rigorous lower bound for the labelled open (C1) count and B = mu1_lab / bound, where
    mu1_lab = p^(2k-1)(p-1) k^-((k-1)^2) (the OSC(B) (N) normalisation times p(p-1)).
    For any S:  sum_c (b_c)_k >= (k-M)! [ sum_c (b_c)_M - (k-1-m)_{M-m} sum_c (b_c)_m ]   (m < M <= k-1),
    and sum_c (b_c)_k itself >= Jensen (M = k).  N1_lab = (p)_k * E_S sum_c (b_c)_k."""
    best = (0.0, None)
    for M in range(2, k + 1):
        lo = lam_low(k, p, M) if M < k else ff(p, k) * balanced(p - k, k ** (k - 1), k) / ff(p, k)
        if M == 2:
            lo = lam_up(k, p, 2)  # exact
        if M == k:
            val = lo
            if val > best[0]: best = (val, (0, k))
            continue
        for m in range(1, M):
            if m == 2 and M == 2: continue
            c = ff(k - 1 - m, M - m)
            val = math.factorial(k - M) * (lo - c * lam_up(k, p, m))
            if val > best[0]: best = (val, (m, M))
    n1 = ff(p, k) * best[0]
    mu1 = p ** (2 * k - 1) * (p - 1) / k ** ((k - 1) ** 2)
    return n1, mu1, best[1]


if __name__ == '__main__' and sys.argv[1] == 'quant':
    k = int(sys.argv[2])
    print(f'k={k}: rigorous lower bound for labelled open (C1) count; B = mu1/bound (OSC (N) needs B = O(1))')
    for p in map(int, sys.argv[3:]):
        n1, mu1, mM = quant(k, p)
        lam = (p - k) / k ** (k - 1)
        print(f'  p={p:8d} lambda={lam:7.3f}  N1_lab >= {n1:.4g}  mu1_lab={mu1:.4g}  B={mu1/n1 if n1>0 else float("inf"):.3g}  (m,M)={mM}', flush=True)
