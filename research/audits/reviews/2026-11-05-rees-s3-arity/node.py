"""Fixed-arity zero-sum node at a grade d in Gamma_0 built on the weight-doubling solver
(report, Corollary P.4).  The bank is i.i.d. uniform on an UNKNOWN subspace K^perp of F_p^g.

Node of arity M(g, tau) = t + k * L with
    t = g + ceil(log_p(2/tau))        (span labels; W != K^perp w.p. <= p^(g-t)/(p-1) <= tau/2)
    L = ceil(2 * N_0(g))              (budget per attempt; Markov: overrun w.p. <= 1/2)
    k = ceil(log2(2/tau))             (independent attempts on disjoint blocks)
Abort probability <= tau/2 + 2^-k <= tau.  The witness is checked exactly in F_p^g.

Usage: nice -n 10 /opt/anaconda3/bin/python node.py OUT.json
"""
import json
import math
import sys
import time

import numpy as np

from doubling import Stream, solve, jstar_of, expected_consumption, covering_time, Exhausted


def rref(rows, p):
    R = (np.array(rows, dtype=np.int64) % p).copy()
    piv = []
    r = 0
    nr, nc = R.shape
    for c in range(nc):
        if r == nr:
            break
        nz = np.nonzero(R[r:, c])[0]
        if len(nz) == 0:
            continue
        i = r + int(nz[0])
        R[[r, i]] = R[[i, r]]
        R[r] = (R[r] * pow(int(R[r, c]), p - 2, p)) % p
        col = R[:, c].copy()
        col[r] = 0
        R = (R - np.outer(col, R[r])) % p
        piv.append(c)
        r += 1
    return R[:r], piv


def node_arity(p, g, tau, sp=None):
    t = g + math.ceil(math.log(2 / tau, p))
    L = math.ceil(2 * float(expected_consumption(p, g, sp)))
    k = math.ceil(math.log2(2 / tau))
    return t + k * L, t, L, k


def zero_sum_node(bank, p, tau, sp=None):
    """Returns a sorted list T of bank indices with sum 0 (checked), or None (abort)."""
    M, g = bank.shape
    Mreq, t, L, k = node_arity(p, g, tau, sp)
    assert M >= Mreq
    R, piv = rref(bank[:t], p)
    a = len(piv)
    js = jstar_of(p)
    for att in range(k):
        lo = t + att * L
        blk = bank[lo:lo + L].astype(np.int64)
        coords = blk[:, piv] if a else np.zeros((L, 0), dtype=np.int64)
        st = Stream(p, a, None, source=coords.astype(np.int16) if a else np.zeros((L, 1), dtype=np.int16))
        try:
            I, W = solve(0, a, np.zeros(a, dtype=np.int64), st, p, js)
        except Exhausted:
            continue
        # labels actually read must lie in W = span of the first t labels
        read = blk[: st.count]
        if a:
            back = (read[:, piv] @ R) % p
            if np.any(back != read % p):
                return None      # W != K^perp detected
        elif np.any(read % p):
            return None
        T = sorted(int(lo + i) for i in I)
        s = bank[T].astype(np.int64).sum(axis=0) % p
        assert len(T) > 0 and np.all(s == 0), "witness check failed"
        return T
    return None


def random_bank(p, g, a, M, rng):
    """M labels i.i.d. uniform on a uniformly random a-dimensional subspace of F_p^g."""
    while True:
        E = rng.integers(0, p, (a, g))
        if a == 0 or len(rref(E, p)[1]) == a:
            break
    C = rng.integers(0, p, (M, a))
    return (C @ E) % p if a else np.zeros((M, g), dtype=np.int64)


def main():
    out = sys.argv[1]
    rng = np.random.default_rng(11)
    res = []
    for p, g, tau, trials in [(3, 6, 0.05, 300), (3, 12, 0.05, 200), (5, 5, 0.05, 200),
                              (5, 8, 0.05, 100), (7, 4, 0.05, 100), (7, 6, 0.05, 60)]:
        sp = covering_time(p)
        Mreq, t, L, k = node_arity(p, g, tau, sp)
        ab = 0
        t0 = time.time()
        for _ in range(trials):
            a = int(rng.integers(0, g + 1))
            bank = random_bank(p, g, a, Mreq, rng)
            T = zero_sum_node(bank, p, tau, sp)
            ab += T is None
        row = {"p": p, "g": g, "tau": tau, "arity": Mreq, "t": t, "L": L, "k": k,
               "trials": trials, "aborts": ab, "davenport_g(p-1)+1": g * (p - 1) + 1,
               "seconds": time.time() - t0}
        print(row, flush=True)
        res.append(row)
        with open(out, "w") as f:
            json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
