"""Exact minimal arity M*(p, kappa, a) = D_H(C_p^a) for small cases.

M*(p,kappa,a) is the least M such that EVERY M columns in F_p^a admit a
nonzero x in (H U {0})^M with sum x_i lambda_i = 0, H = (F_p^*)^kappa.
This is the weighted Davenport constant with weight set H.  A zero column
is trivially solvable, and a column matters only through its class
lambda*H, so we search multisets of classes of F_p^a \\ {0} mod H.

Exhaustive DFS: classes added in nondecreasing index order; R = set of
H-weighted nonempty subset sums.  Adding class c (representative v) keeps the
sequence zero-sum free iff no element of -vH lies in R.  WLOG (GL_a action)
the multiset contains the class of e_1, which has index 0.
M* = 1 + (longest zero-sum-free multiset).  Bounds: Chevalley-Warning gives
M* <= kappa*a + 1; direct sums give M* >= a*(M*(p,kappa,1) - 1) + 1.

Usage: python davenport.py a PMAX [time_limit_per_case]
"""
import sys
import time
import itertools
import numpy as np
from sympy import primerange, primitive_root


def classes(p, k, a):
    g = primitive_root(p)
    H = sorted({pow(x, k, p) for x in range(1, p)})
    seen, reps = set(), []
    for v in itertools.product(range(p), repeat=a):
        if not any(v) or v in seen:
            continue
        orbit = [tuple(c * x % p for x in v) for c in H]
        seen.update(orbit)
        reps.append((v, orbit))
    # put e_1's class first
    e1 = tuple([1] + [0] * (a - 1))
    reps.sort(key=lambda t: 0 if e1 in t[1] else 1)
    return H, reps


def longest_zsf(p, k, a, limit):
    H, reps = classes(p, k, a)
    n = len(reps)
    shape = (p,) * a
    # orbit index arrays for fast translation: translate R by vector u
    def translate(R, u):
        out = R
        for ax, s in enumerate(u):
            if s:
                out = np.roll(out, s, axis=ax)
        return out
    neg_orbits = [[tuple((-x) % p for x in w) for w in orb] for _, orb in reps]
    best = [0, None]
    t0 = time.time()
    timed_out = [False]

    def dfs(start, R, seq):
        if len(seq) > best[0]:
            best[0], best[1] = len(seq), list(seq)
        if time.time() - t0 > limit:
            timed_out[0] = True
            return
        if len(seq) >= k * a:          # Chevalley-Warning cap
            return
        for c in range(start, n):
            if any(R[w] for w in neg_orbits[c]):
                continue
            Rn = R.copy()
            for w in reps[c][1]:
                Rn[w] = True
                Rn |= translate(R, w)
            seq.append(c)
            dfs(c, Rn, seq)
            seq.pop()
            if timed_out[0]:
                return
            if not seq:                # first element fixed to class 0 (e_1)
                return

    R0 = np.zeros(shape, dtype=bool)
    dfs(0, R0, [])
    ex = [reps[c][0] for c in best[1]] if best[1] else []
    return best[0], ex, timed_out[0], len(reps)


def main():
    a, pmax = int(sys.argv[1]), int(sys.argv[2])
    limit = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    one = {}
    for p in primerange(3, pmax + 1):
        for k in range(2, p):
            if (p - 1) % k:
                continue
            L, ex, to, ncl = longest_zsf(p, k, a, limit)
            M = L + 1
            cw = k * a + 1
            tag = "LOWER BOUND ONLY (timeout)" if to else "exact"
            print(f"p={p} kappa={k} h={(p-1)//k} a={a} classes={ncl} M*={'>=' if to else ''}{M} "
                  f"CW={cw} sched2={(a+1)*((k-1)*a+1)} [{tag}] extremal_minus_one={ex}", flush=True)


if __name__ == "__main__":
    main()
