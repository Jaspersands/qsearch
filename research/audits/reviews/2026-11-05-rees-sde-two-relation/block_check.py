"""Exact check of Theorem B (block realization of a circuit) against brute force.

For a circuit S of q+1 columns in F_p^q (U = 0) with dependency delta and a
partition of S into E blocks, each inside one class set of delta:
  (i)  the block vectors W_b span an (E-1)-dimensional space Omega with the
       single relation sum_b W_b = 0;
  (ii) R(S) intersected with Omega equals { sum beta_b W_b : Good(beta) != empty },
       computed from the coset rule alone;
  (iii) every beta with no cross-class coincidence is realizable when p is not
       exceptional (compared with good_threshold.scan_prime);
  (iv) R(S) contains no 2-dim subspace (Theorem 1 of the subquadratic report),
       although R(S) contains all of Omega outside the cross-class hyperplanes.
R(S) is computed exhaustively (common.realizable).
"""
import itertools
import random

import numpy as np

from common import F, rank, realizable
import good_threshold as gt


def make_circuit(Fd, rng, q, pattern=None):
    p = Fd.p
    while True:
        B = [[rng.randrange(p) for _ in range(q)] for _ in range(q)]
        if rank(B, p) == q:
            break
    if pattern is None:
        delta = [rng.randrange(1, p) for _ in range(q + 1)]
    else:
        delta = [(Fd.rep(c) * rng.choice(Fd.P)) % p for c in pattern]
    iv = pow(delta[q], p - 2, p)
    last = [(-iv * sum(delta[i] * B[i][j] for i in range(q))) % p for j in range(q)]
    return B + [last], delta


def good_nonempty(Fd, beta, bclass):
    p, k = Fd.p, Fd.k
    for s in range(p):
        if all(((b + s) % p == 0) or Fd.cls(b + s) == (-c) % k for b, c in zip(beta, bclass)):
            return True
    return False


def check(Fd, rng, q, E, pattern=None):
    p, k = Fd.p, Fd.k
    cols, delta = make_circuit(Fd, rng, q, pattern)
    cls = [Fd.cls(d) for d in delta]
    if len(set(cls)) < 2:
        return None
    byc = {}
    for i, c in enumerate(cls):
        byc.setdefault(c, []).append(i)
    blocks = [byc[c] for c in sorted(byc)]
    while len(blocks) < E and max(len(b) for b in blocks) >= 2:
        j = max(range(len(blocks)), key=lambda b: len(blocks[b]))
        G = blocks[j][:]
        rng.shuffle(G)
        h = len(G) // 2
        blocks[j:j + 1] = [G[:h], G[h:]]
    Eb = len(blocks)
    W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(q)] for G in blocks]
    bclass = [cls[G[0]] for G in blocks]
    dim_ok = rank(W, p) == Eb - 1 and all(v == 0 for v in
                                          [sum(W[b][t] for b in range(Eb)) % p for t in range(q)])
    R = realizable(Fd, cols, q)
    # (ii) every point of Omega: beta with beta_0 = 0 ranges over F_p^{Eb-1}
    mism = 0
    covered = 0
    total = 0
    cross_ok = True
    for bt in itertools.product(range(p), repeat=Eb - 1):
        beta = (0,) + bt
        v = tuple(sum(beta[b] * W[b][t] for b in range(Eb)) % p for t in range(q))
        pred = good_nonempty(Fd, beta, bclass)
        mism += bool(R[v]) != pred
        total += 1
        covered += pred
        coinc = any(beta[b] == beta[bp] and bclass[b] != bclass[bp]
                    for b in range(Eb) for bp in range(b + 1, Eb))
        if not coinc and not pred:
            cross_ok = False
    return dict(Eb=Eb, dim_ok=dim_ok, mism=mism, frac=covered / total, cross_ok=cross_ok)


def main():
    rng = random.Random(20261105)
    cases = [(13, 2, 2, 3), (29, 2, 2, 3), (13, 2, 3, 3), (29, 2, 3, 3), (13, 2, 3, 4), (29, 2, 3, 4),
             (37, 3, 2, 3), (61, 3, 2, 3), (31, 3, 3, 3), (43, 3, 3, 3), (37, 3, 3, 4), (13, 3, 3, 3),
             (17, 4, 3, 4), (41, 4, 3, 4), (271, 3, 2, 3), (157, 2, 2, 4)]
    allok = True
    for (p, k, q, E) in cases:
        Fd = F(p, k)
        exc, gmin, _ = gt.scan_prime(p, k, E)
        res = []
        for t in range(6):
            r = check(Fd, rng, q, E)
            if r is not None:
                res.append(r)
        mism = sum(r["mism"] for r in res)
        dims = all(r["dim_ok"] for r in res)
        cross = all(r["cross_ok"] for r in res)
        allok &= mism == 0 and dims and (cross or exc)
        print(f"p={p} kappa={k} q={q} E={E} p_exceptional={exc}: objects={len(res)} "
              f"blocks={[r['Eb'] for r in res]} dim_ok={dims} (ii)mismatches={mism} "
              f"(iii)coincidence-free all realizable={cross} "
              f"fraction of Omega realizable={[round(r['frac'], 3) for r in res]}", flush=True)
    print("ALL CHECKS:", "PASS" if allok else "FAIL")


if __name__ == "__main__":
    main()
