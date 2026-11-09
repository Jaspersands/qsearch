"""Exact flexibility of two-relation objects (q+2 columns in F_p^q, general position).

For each sampled object S:
  R(S)      = realizable set (exhaustive, common.realizable);
  flex      = largest r such that some r-dim subspace lies in R(S) (exact, q <= 4);
  collapse  = union over the p+1 kernel directions k of the targets realizable by
              the class-collapse rule along k (blocks = class sets of k), i.e.
              { sum_c beta_c W_c(k) : Good(beta) != empty };
  cflex     = largest r such that an r-dim subspace lies in the collapse set.
Prints, per (p, kappa, q), the counts of objects with flex = 0, 1, 2, ... and
the same for cflex.  The objects are uniform q+2 columns conditioned on general
position (every q columns independent), so the kernel K is 2-dimensional and
every nonzero kernel vector has at most one zero (Lemma 2.2).
"""
import itertools
import random
import sys

import numpy as np

from common import F, kernel, rank, realizable, proj_points


def gp_object(Fd, rng, q):
    p = Fd.p
    while True:
        cols = [[rng.randrange(p) for _ in range(q)] for _ in range(q + 2)]
        if all(rank([cols[i] for i in sub], p) == q for sub in itertools.combinations(range(q + 2), q)):
            return cols


def canon(v, p):
    nz = next(x for x in v if x % p)
    iv = pow(nz, p - 2, p)
    return tuple((x * iv) % p for x in v)


def flexible_lines(Fd, R, q):
    p, k = Fd.p, Fd.k
    cs = np.arange(1, p)
    out = []
    for u in proj_points(p, q):
        pts = tuple((cs * x) % p for x in u)
        if R[pts].all():
            out.append(u)
    return out


def max_flex(Fd, R, q):
    """Exact largest dimension of a subspace inside R (q <= 4)."""
    p = Fd.p
    if R.all():
        return q
    lines = flexible_lines(Fd, R, q)
    if not lines:
        return 0
    L = set(lines)
    best = 1
    # planes: spanned by two flexible lines, all p+1 lines flexible
    planes = []
    seen = set()
    for u, v in itertools.combinations(lines, 2):
        ok = True
        pl = []
        for s in range(p):
            w = canon([(u[i] * s + v[i]) % p for i in range(q)], p)
            if w not in L:
                ok = False
                break
            pl.append(w)
        if ok:
            key = frozenset(pl + [u])
            if key not in seen:
                seen.add(key)
                planes.append(key)
    if planes:
        best = 2
    if q >= 4 and planes:
        # 3-spaces: a plane plus one more flexible line, all lines flexible
        for pl in planes:
            for w in lines:
                if w in pl:
                    continue
                okk = True
                for z in pl:
                    for s in range(1, p):
                        t = canon([(z[i] + s * w[i]) % p for i in range(q)], p)
                        if t not in L:
                            okk = False
                            break
                    if not okk:
                        break
                if okk:
                    return 3
    return best


def collapse_set(Fd, cols, q):
    p, k = Fd.p, Fd.k
    K = kernel(cols, p)
    assert len(K) == 2
    C = np.zeros((p,) * q, dtype=bool)
    C[(0,) * q] = True
    for (s, t) in [(1, 0)] + [(x, 1) for x in range(p)]:
        kv = [(s * K[0][i] + t * K[1][i]) % p for i in range(q + 2)]
        sup = [i for i in range(q + 2) if kv[i]]
        cls = {i: Fd.cls(kv[i]) for i in sup}
        classes = sorted(set(cls.values()))
        W = {c: [sum(kv[i] * cols[i][j] for i in sup if cls[i] == c) % p for j in range(q)]
             for c in classes}
        for beta in itertools.product(range(p), repeat=len(classes)):
            # Good(beta) nonempty?
            good = False
            for s0 in range(p):
                if all(((b + s0) % p == 0) or Fd.cls(b + s0) == (-c) % k
                       for b, c in zip(beta, classes)):
                    good = True
                    break
            if good:
                v = tuple(sum(b * W[c][j] for b, c in zip(beta, classes)) % p for j in range(q))
                C[v] = True
    return C


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    cases = [(5, 2, 2, 8), (7, 2, 2, 8), (11, 2, 2, 8), (13, 2, 2, 8), (17, 2, 2, 8), (29, 2, 2, 8),
             (7, 3, 2, 8), (13, 3, 2, 8), (19, 3, 2, 8), (31, 3, 2, 8), (37, 3, 2, 8), (43, 3, 2, 8),
             (7, 2, 3, 6), (11, 2, 3, 6), (13, 2, 3, 6), (17, 2, 3, 6), (19, 2, 3, 4),
             (13, 3, 3, 6), (19, 3, 3, 4), (31, 3, 3, 3),
             (7, 2, 4, 4), (11, 2, 4, 3), (13, 3, 4, 2)]
    for (p, k, q, n) in cases:
        Fd = F(p, k)
        fl = {}
        cf = {}
        dens = []
        for _ in range(n):
            cols = gp_object(Fd, rng, q)
            R = realizable(Fd, cols, q)
            f = max_flex(Fd, R, q)
            fl[f] = fl.get(f, 0) + 1
            dens.append(round(float(R.mean()), 3))
            if p ** q <= 30000 and k <= 3:
                C = collapse_set(Fd, cols, q)
                assert not (C & ~R).any(), "collapse realisation outside R"
                c = max_flex(Fd, C, q)
                cf[c] = cf.get(c, 0) + 1
        print(f"p={p} kappa={k} q={q} |S|={q+2}: max exact flexible dim counts {dict(sorted(fl.items()))}; "
              f"collapse-rule flexible dim counts {dict(sorted(cf.items())) if cf else 'skipped'}; "
              f"density of R(S) {dens}", flush=True)


if __name__ == "__main__":
    main()
