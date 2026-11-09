"""Exhaustive check of Lemma 2 (brackets for E C(M_S, m)) and of the Bonferroni steps of
Theorem 1, against the exact joint law of (n_0..n_{k-1}) over all y in {0} x F_p^{k-1}.

k = 3: matrix products over (y1, y2); k = 4: one matrix product per y1.
Usage: python exact_check.py k p1 p2 [mmax]
"""
import sys, itertools, math
import numpy as np
import mpmath as mp
import cert

mp.mp.dps = 50


def primes(a, b):
    out = []
    for n in range(max(a, 2), b + 1):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            out.append(n)
    return out


def gen(p):
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in set(f for f in range(2, p) if (p - 1) % f == 0 and all(f % d for d in range(2, int(f ** 0.5) + 1)))):
            return g


def ind_table(p, k):
    g = gen(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e % k
        x = x * g % p
    return ind


def joint_counts(p, k):
    """Array n[j] of shape (p,)*(k-1): n_j(y_1..y_{k-1})."""
    ind = ind_table(p, k)
    xs = np.arange(p)
    shift = (xs[:, None] + xs[None, :]) % p          # [x, y] -> x + y
    I = ind[shift]                                    # coset index of x + y (-1 for 0)
    out = []
    for j in range(k):
        inQ = (ind == (-j) % k)                       # row 0: x in Q_{-j}
        A = [None] + [((I == (-(i + j)) % k) & inQ[:, None]).astype(np.float64) for i in range(1, k)]
        if k == 3:
            n = A[1].T @ A[2]                         # [y1, y2] = sum_x A1[x,y1] A2[x,y2]
        elif k == 4:
            n = np.empty((p, p, p))
            for y1 in range(p):
                w = A[1][:, y1]
                n[y1] = (A[2] * w[:, None]).T @ A[3]
        else:
            raise ValueError
        out.append(np.rint(n).astype(np.int64))
    return out


def main():
    k, p1, p2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    mmax = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    nfail = 0; nchk = 0
    for p in primes(p1, p2):
        if (p - 1) % k:
            continue
        ns = joint_counts(p, k)
        tot = ns[0].size
        lam_true = ((p - 1) / k) ** k / p ** (k - 1)
        pm = mp.mpf(p)
        data = cert.prepare(k, pm, pm, 4 * k)
        line = [f"p={p} Lambda={(p-1)/k**k:.4f} E n_j/lam_true=" +
                ",".join(f"{ns[j].mean()/lam_true:.6f}" for j in range(k))]
        for r in range(1, k + 1):
            for S in itertools.combinations(range(k), r):
                M = sum(ns[j] for j in S)
                for m in range(0, mmax + 1):
                    ex = mp.mpf(int(sum(math.comb(int(v), m) * int(c) for v, c in zip(*np.unique(M, return_counts=True))))) / tot
                    # bracket from cert (only where eta_m < 1; otherwise upper bound with (1+eta))
                    h = (pm - 1) / k
                    e = cert.eta(k, m, pm)
                    rho = (pm - m) / (pm * mp.mpf(k) ** m)
                    u = cert.gbinom(r * h, m) * rho ** (k - 1) * (1 + e) ** (k - 1) if m else mp.mpf(1)
                    l = cert.gbinom(r * h, m) * rho ** (k - 1) * (1 - e) ** (k - 1) if (m and e < 1) else (mp.mpf(1) if m == 0 else mp.mpf(0))
                    nchk += 1
                    if not (l - mp.mpf(10) ** -30 <= ex <= u + mp.mpf(10) ** -30):
                        nfail += 1
                        line.append(f"  FAIL S={S} m={m} exact={mp.nstr(ex,10)} bracket=[{mp.nstr(l,10)},{mp.nstr(u,10)}]")
                # Bonferroni step: P(M_S = 0) vs L_r / U_r of cert (pointwise at p)
                P0 = mp.mpf(int((M == 0).sum())) / tot
                v, K = cert.best_LU(k, r, pm, pm, data)
                ok = (P0 >= v - mp.mpf(10) ** -30) if r % 2 == 0 else (P0 <= v + mp.mpf(10) ** -30)
                nchk += 1
                if not ok:
                    nfail += 1
                    line.append(f"  FAIL Bonferroni S={S} P0={mp.nstr(P0,10)} bound={mp.nstr(v,10)} K={K}")
        W0 = np.ones_like(ns[0], dtype=bool)
        for j in range(k):
            W0 &= ns[j] > 0
        Pall = W0.mean()
        val, R, Ks, Km = cert.bestF(k, pm, pm)
        nchk += 1
        if val > Pall + 1e-30:
            nfail += 1
            line.append(f"  FAIL F={mp.nstr(val,8)} > P(all)={Pall}")
        line.append(f"  P(all n_j>0)={Pall:.6g} (1-e^-L)^k={(1-math.exp(-(p-1)/k**k))**k:.6g} F={mp.nstr(val,6)} Kmax={Km}")
        print("\n".join(line), flush=True)
    print(f"checks={nchk} failures={nfail}")


if __name__ == "__main__":
    main()
