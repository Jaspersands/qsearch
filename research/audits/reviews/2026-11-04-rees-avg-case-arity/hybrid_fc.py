"""Hybrid solver: K triangular rounds (flexible vectors) + free-coordinate sampling
in the quotient F_p^a / U_K, then back-substitution.

Round i (i = 0..K-1) takes a - i + 1 fresh columns, a dependency d modulo U_i, and the
flexible vector v = sum_i beta_{coset d_i} d_i u_i (Lemma 1 of the 2026-11-02 linear-arity
report, i.e. the triangular solver prop:triangular-sde).  U_{i+1} = U_i + F_p v.
Then n = (a - K) + n0 fresh columns are mapped to the quotient (dim q = a - K) and the
free-coordinate sampler (F2)-(F3) of thm:free-coordinate is run there: free x in
P_kappa^{F'} uniform, pivots v_i = -R_i x must lie in D.  The resulting tau = -sum x u lies
in U_K and is absorbed by back-substitution.

Columns used: sum_{i<K} (a - i + 1) + (a - K) + n0.  Expected trials ~ q^{-(a-K)},
q = (h+1)/p ~ 1/kappa.  Every witness is checked exactly.

Usage: python hybrid_fc.py p kappa a n0 reps K1 K2 ...
"""
import random
import sys
import time
import numpy as np
from common import (Field, check_witness, rand_cols, rref, kernel_basis, solve_in_span,
                    quotient_map, apply, two_level_contraction)


def flexible_object(Fd, AB, cols, Phi, p):
    alpha, beta = AB
    imgs = [apply(Phi, u, p) for u in cols] if Phi is not None else [list(u) for u in cols]
    ker = kernel_basis(imgs, p)
    d = ker[0]
    lead = next(x for x in d if x)
    inv = pow(lead, -1, p)
    d = [x * inv % p for x in d]
    a = len(cols[0])
    e = [sum(d[l] * cols[l][i] for l in range(len(cols))) % p for i in range(a)]
    v = [sum(beta[Fd.coset(d[l])] * d[l] * cols[l][i] for l in range(len(cols)) if d[l]) % p
         for i in range(a)]
    return d, e, v


def lemma1_weights(Fd, AB, d, c):
    alpha, beta = AB
    n = Fd.coset(c)
    return [(c * dl * (alpha[n] + beta[Fd.coset(dl)])) % Fd.p if dl else 0 for dl in d]


def fc_sample(Fd, imgs, n0, rng, max_trials, batch=4096):
    """Free-coordinate sampler on columns imgs (in F_p^q).  Returns (x, trials) or (None, t)."""
    p = Fd.p
    q = len(imgs[0])
    n = len(imgs)
    R, piv = rref([[imgs[j][i] for j in range(n)] for i in range(q)], p)
    r = len(R)
    last = piv[-1] if piv else -1
    Fp_ = list(range(last + 1, n))
    if len(Fp_) < n0:
        return None, 0
    C = np.array([[(-R[i][l]) % p for l in Fp_] for i in range(r)], dtype=object) if r else None
    trials = 0
    nrng = np.random.default_rng(rng.randrange(2**63))
    while trials < max_trials:
        B = int(min(batch, max_trials - trials))
        # x_l = b^kappa, b uniform nonzero
        b = nrng.integers(1, p, size=(len(Fp_), B), dtype=np.int64).astype(object)
        X = np.vectorize(lambda t: pow(int(t), Fd.k, p), otypes=[object])(b) if Fd.k else b
        ok = np.ones(B, dtype=bool)
        V = None
        if r:
            V = C.dot(X) % p                       # r x B, exact (object ints)
            Vh = np.vectorize(lambda t: int(t) == 0 or pow(int(t), Fd.h, p) == 1, otypes=[bool])(V)
            ok = Vh.all(axis=0)
        idx = np.flatnonzero(ok)
        if idx.size:
            t0 = int(idx[0])
            x = [0] * n
            for jj, l in enumerate(Fp_):
                x[l] = int(X[jj, t0])
            for i in range(r):
                x[piv[i]] = int(V[i, t0])
            return x, trials + t0 + 1
        trials += B
    return None, trials


def solve(Fd, AB, cols_all, a, K, n0, rng, max_trials):
    p = Fd.p
    pos = 0
    objs, U = [], []
    for i in range(K):
        m = a - i + 1
        cols = cols_all[pos:pos + m]
        Phi = quotient_map(U, a, p, rng) if U else None
        d, e, v = flexible_object(Fd, AB, cols, Phi, p)
        if (Phi is not None and not any(apply(Phi, v, p))) or (Phi is None and not any(v)):
            # stop condition of the triangular solver: v in U_i, so the c = 1 weights of
            # this object already sum into U_i (always the case when all d_l are squares
            # at kappa = 2).  Finish by back-substitution; no free-coordinate step.
            w = lemma1_weights(Fd, AB, d, 1)
            x = [0] * (pos + m)
            for t, wt in enumerate(w):
                x[pos + t] = wt
            tau = [(-(e[t] + v[t])) % p for t in range(a)]
            return backsub(Fd, AB, objs, U, x, tau, a), 0, pos + m
        objs.append((pos, d, e, v))
        U.append(v)
        pos += m
    q = a - K
    n = q + n0
    cols = cols_all[pos:pos + n]
    Phi = quotient_map(U, a, p, rng) if U else None
    imgs = [apply(Phi, u, p) for u in cols] if Phi is not None else [list(u) for u in cols]
    x_fc, trials = fc_sample(Fd, imgs, n0, rng, max_trials)
    if x_fc is None:
        return None, trials, pos + n
    x = [0] * (pos + n)
    for l in range(n):
        x[pos + l] = x_fc[l]
    tau = [(-sum(x_fc[l] * cols[l][i] for l in range(n))) % p for i in range(a)]
    return backsub(Fd, AB, objs, U, x, tau, a), trials, pos + n


def backsub(Fd, AB, objs, U, x, tau, a):
    p = Fd.p
    for l in range(len(objs) - 1, -1, -1):
        st, d, e, v = objs[l]
        coef = solve_in_span(U[:l + 1], tau, p)
        assert coef is not None, "tau left U_l"
        c = coef[l]
        if c:
            w = lemma1_weights(Fd, AB, d, c)
            for t, wt in enumerate(w):
                x[st + t] = (x[st + t] + wt) % p     # supports are disjoint: x was 0 there
            n_ = Fd.coset(c)
            tau = [(tau[i] - c * (AB[0][n_] * e[i] + v[i])) % p for i in range(a)]
    assert not any(tau)
    return x


def main():
    p, k, a, n0, reps = map(int, sys.argv[1:6])
    Ks = list(map(int, sys.argv[6:]))
    Fd = Field(p, k)
    rng = random.Random(4110 + 7 * a + k)
    AB = two_level_contraction(Fd, rng)
    assert AB is not None, "no two-level contraction found (p in E_2(kappa)?)"
    qv = (Fd.h + 1) / p
    print(f"# p={p} kappa={k} a={a} n0={n0} reps={reps} alpha={AB[0]} beta={AB[1]}")
    print("K  columns  (a+1)(a+2)/2  witnesses  mean_trials  q^-(a-K)  ratio  sec")
    for K in Ks:
        t0 = time.time()
        okc, tr, used = 0, [], 0
        max_trials = int(60 * qv ** (-(a - K))) + 100
        for r in range(reps):
            M = sum(a - i + 1 for i in range(K)) + (a - K) + n0
            cols = rand_cols(rng, p, a, M)
            x, trials, used = solve(Fd, AB, cols, a, K, n0, rng, max_trials)
            tr.append(trials)
            if x is not None:
                assert check_witness(Fd, cols[:len(x)], x), "bad witness"
                okc += 1
        mt = sum(tr) / len(tr)
        print(f"{K:2d} {M:7d} {(a+1)*(a+2)//2:10d}   {okc:3d}/{reps:<3d}  {mt:11.1f}  "
              f"{qv**(-(a-K)):9.1f}  {mt*qv**(a-K):5.2f}  {time.time()-t0:6.1f}", flush=True)


if __name__ == "__main__":
    main()
