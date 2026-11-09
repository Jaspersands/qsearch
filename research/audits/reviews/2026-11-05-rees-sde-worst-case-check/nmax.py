"""Independent exact computation of N(kappa, a, p) for a = 1, 2.

N = largest M such that some bank of M columns in F_p^a has no nonzero x in (P u {0})^M with
sum x_i lam_i = 0.  Solvability is monotone under adding columns, and scaling a column by an
element of P does not change it, so a DFS over nondecreasing multisets of column classes
(nonzero vectors modulo P) with pruning of solvable prefixes is exhaustive.
For a = 2 and M >= 3 an unsolvable bank has rank 2 (a rank-1 bank with three nonzero columns is
solvable whenever N(kappa,1,p) = 2; in general a rank-1 bank has at most N(kappa,1,p) <= 2 N(kappa,1,p)
unsolvable columns), so the maximum is attained in rank 2 and by GL_2 we may assume e1, e2 are in it.
Solvability: DP over the reachable set of values with some nonzero weight.
"""
import sys
import numpy as np


def kth_powers(p, k):
    return sorted({pow(y, k, p) for y in range(1, p)})


def classes_mod_P(p, a, P):
    seen, reps = set(), []
    import itertools
    for v in itertools.product(range(p), repeat=a):
        if not any(v) or v in seen:
            continue
        orb = {tuple(u * x % p for x in v) for u in P}
        seen |= orb
        reps.append(v)
    return reps


class Bank:
    """Incremental reachable sets: Z = values reachable with all weights 0 so far ({0}),
    N = values reachable with at least one nonzero weight."""

    def __init__(self, p, a, P):
        self.p, self.a, self.P = p, a, P
        self.size = p ** a

    def idx(self, v):
        i = 0
        for x in v:
            i = i * self.p + (x % self.p)
        return i

    def shifts(self, v):
        return [self.idx(tuple(u * x for x in v)) for u in self.P]

    def add(self, N, v):
        """N' = (N + {0} u P v) u (P v)."""
        p, a = self.p, self.a
        out = N.copy()
        # translation by w on Z_p^a: implement via reshape/roll
        Nr = N.reshape((p,) * a)
        for u in self.P:
            w = tuple(u * x % p for x in v)
            out |= np.roll(Nr, shift=w, axis=tuple(range(a))).reshape(-1)
            out[self.idx(w)] = True
        return out


def nmax(p, k, a, maxdepth=12):
    P = kth_powers(p, k)
    reps = classes_mod_P(p, a, P)
    bk = Bank(p, a, P)
    z = 0
    best = [0, None]
    start = []
    if a == 2:
        start = [(1, 0), (0, 1)]
    N0 = np.zeros(bk.size, bool)
    for v in start:
        N0 = bk.add(N0, v)
    if N0[z]:
        return 0, None
    nodes = [0]

    def dfs(N, cur, lo):
        nodes[0] += 1
        if len(cur) > best[0]:
            best[0], best[1] = len(cur), list(cur)
        if len(cur) >= maxdepth:
            return
        for j in range(lo, len(reps)):
            N2 = bk.add(N, reps[j])
            if not N2[z]:
                cur.append(reps[j])
                dfs(N2, cur, j)
                cur.pop()

    dfs(N0, list(start), 0)
    return best[0], best[1], nodes[0]


if __name__ == "__main__":
    cases = [(2, 7), (2, 13), (3, 7), (3, 13), (3, 19), (3, 31), (4, 13), (4, 17)]
    for k, p in cases:
        r1 = nmax(p, k, 1)
        r2 = nmax(p, k, 2)
        print(f"kappa={k} p={p} N(a=1)={r1[0]} N(a=2)={r2[0]} CW(a=2)={2*k} "
              f"witness={r2[1]} nodes={r2[2]}", flush=True)
