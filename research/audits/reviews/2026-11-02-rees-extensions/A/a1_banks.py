"""Item A falsifier hunt (brief section 4): per-bank witness counts for the filiform family,
where the class grows with r (c = r+1), at the smallest prime allowed by Cor fpt-r's
Schedule 3 branch, p >= 16(r+1)^2.

For the trivial hidden subgroup the stage-d label rank is a_d = g_d = r-d+2, the largest
possible. A bank is M = 4u columns, u = r+1, i.i.d. uniform on F_p^a (the intrinsic
coordinates of K_d^perp). N = number of nonzero y in (P_kappa u {0})^M with A y = 0; the
per-trial acceptance of kernel rejection is N / p^(M - rank A). Thm random-column (i)
promises acceptance >= 1/(4 kappa^M) outside a bank event of probability <= 4/mu + 2p^(a-M).

Counting: a DP over partial sums in F_p (exact Python integers) for a = 1. For a >= 2,
the character sum N + 1 = p^(-a) sum_xi prod_i g(xi . lambda_i), g(t) = sum_{y in P} w^(ty),
with the xi in the left kernel of A (all t_i = 0) counted exactly as p^(a-rank) (h+1)^M and
only the remaining terms (each at most ((1+sqrt p)/2)^M in size) in float64; for a = 2 it is
cross-checked against a float DP. kappa = 1 grades are
linear and need no rejection (Thm power-sde (i)); they are skipped.

Run: /opt/anaconda3/bin/python a1_banks.py   (about 90 seconds)
"""
import sys
import time
from math import gcd

import numpy as np


def powers_with_zero(p, k):
    return sorted({pow(x, k, p) for x in range(1, p)} | {0})


def rank_mod_p(A, p):
    A = [list(map(int, row)) for row in A]
    rows, cols = len(A), len(A[0])
    rk = 0
    for c in range(cols):
        piv = next((i for i in range(rk, rows) if A[i][c] % p), None)
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        inv = pow(A[rk][c], -1, p)
        A[rk] = [x * inv % p for x in A[rk]]
        for i in range(rows):
            if i != rk and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk


def count_exact_a1(cols, p, P):
    cnt = [0] * p
    cnt[0] = 1
    for lam in cols:
        new = [0] * p
        shifts = [(y * lam) % p for y in P]
        for s, v in enumerate(cnt):
            if v:
                for t in shifts:
                    new[(s + t) % p] += v
        cnt = new
    return cnt[0] - 1


def count_float(cols, p, P, a):
    cnt = np.zeros((p,) * a, dtype=np.float64)
    cnt[(0,) * a] = 1.0
    for lam in cols:
        new = np.zeros_like(cnt)
        for y in P:
            shift = tuple(int(y * l % p) for l in lam)
            new += np.roll(cnt, shift, axis=tuple(range(a)))
        cnt = new
    return cnt[(0,) * a] - 1.0


def count_charsum(A, p, P, rk):
    a, M = A.shape
    t = np.arange(p)
    g = np.exp(2j * np.pi * np.outer(t, np.array(P)) / p).sum(axis=1)
    grids = np.meshgrid(*([np.arange(p)] * a), indexing="ij")
    xi = np.stack([x.ravel() for x in grids])            # a x p^a
    T = (A.T.astype(np.int64) @ xi) % p                   # M x p^a
    zero = (T == 0).all(axis=0)
    prod = np.ones(xi.shape[1], dtype=np.complex128)
    for i in range(M):
        prod *= g[T[i]]
    rem = prod[~zero].sum().real
    main_exact = int(zero.sum()) * (len(P)) ** M
    assert int(zero.sum()) == p ** (a - rk)
    return (main_exact + rem) / float(p) ** a - 1.0


def main():
    rng = np.random.default_rng(20261102)
    plan = [  # (r, p, d, banks)
        (1, 67, 2, 200),
        (2, 149, 2, 60),
        (3, 257, 2, 20),
        (3, 257, 4, 200),
    ]
    for r, p, d, banks in plan:
        u = r + 1
        M = 4 * u
        a = r - d + 2
        k = gcd(d, p - 1)
        P = powers_with_zero(p, k)
        bound = 1.0 / (4.0 * k ** M)
        accs, exists = [], 0
        t0 = time.time()
        for _ in range(banks):
            A = rng.integers(0, p, size=(a, M))
            cols = [tuple(int(A[i, j]) for i in range(a)) for j in range(M)]
            rk = rank_mod_p(A.tolist(), p)
            if a == 1:
                N = count_exact_a1([c[0] for c in cols], p, P)
            else:
                N = count_charsum(A, p, P, rk)
                if a == 2 and _ < 3:
                    Nd = count_float(cols, p, P, a)
                    assert abs(Nd - N) <= 1e-9 * max(1.0, N), (Nd, N)
            exists += N >= 1
            accs.append(float(N) / float(p) ** (M - rk))
        accs = np.array(accs)
        kind = "exact DP" if a == 1 else "exact main term + float64 character sum"
        print(f"filiform r={r} p={p} d={d} kappa={k} a={a} M={M}: banks={banks} ({kind}); "
              f"witness exists {exists}/{banks}; acceptance min {accs.min():.3e} mean {accs.mean():.3e}; "
              f"bound 1/(4k^M)={bound:.3e}; banks below bound {(accs < bound).sum()}; "
              f"min/bound={accs.min() / bound:.1f}; {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
