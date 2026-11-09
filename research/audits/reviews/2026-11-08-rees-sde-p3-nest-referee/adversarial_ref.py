"""Run the referee's WNEST on structured adversarial instances with m = ceil(theorem bound) exactly.
Every witness is re-summed over the original vectors (WNEST.finish); every per-piece claim asserted."""
import math, sys, time
import numpy as np
from wnest_ref import WNEST, Fail, theorem_bound, guarantee, Nq

rng = np.random.default_rng(81108)


def rand_inv(n):
    from f3 import rank
    while True:
        A = rng.integers(0, 3, size=(n, n))
        if rank(A) == n:
            return A


def fam(name, n, m):
    if name == "random":
        return [rng.integers(0, 3, n) for _ in range(m)]
    if name == "duplicates":          # 5 distinct vectors, each repeated
        base = [rng.integers(0, 3, n) for _ in range(5)]
        return [base[i % 5] for i in range(m)]
    if name == "dup_blocks":          # each vector repeated twice consecutively (series-free but class 2)
        out = []
        while len(out) < m:
            v = rng.integers(0, 3, n); out += [v, v]
        return out[:m]
    if name == "negpairs":
        out = []
        while len(out) < m:
            v = rng.integers(0, 3, n); out += [v, (2 * v) % 3]
        return out[:m]
    if name.startswith("chain"):      # circuits of length L in coordinate blocks of size L-1, cycled
        L = int(name[5:]); b = min(L - 1, n); g = max(1, n // b); out = []; j = 0
        T = rand_inv(n)
        while len(out) < m:
            blk = j % g; j += 1
            U = np.zeros((n, b), dtype=np.int64)
            U[blk * b:(blk + 1) * b] = rng.integers(0, 3, size=(b, b))
            c = rng.integers(1, 3, size=b)
            cols = [U[:, i] for i in range(b)] + [(-(U @ c)) % 3]
            out += [(T @ x) % 3 for x in cols]
        return out[:m]
    if name == "subspace":            # 90% in a random n/3-dim subspace
        k = max(1, n // 3); Bm = rng.integers(0, 3, size=(n, k))
        return [(Bm @ rng.integers(0, 3, k)) % 3 if rng.random() < 0.9 else rng.integers(0, 3, n)
                for _ in range(m)]
    if name == "flag":                # first third from dim n/4, second from dim n/2, rest full
        T = rand_inv(n); out = []
        for i in range(m):
            k = n // 4 if i < m // 3 else (n // 2 if i < 2 * m // 3 else n)
            x = np.zeros(n, dtype=np.int64); x[:k] = rng.integers(0, 3, k); out.append((T @ x) % 3)
        return out
    if name == "coloops":             # basis vectors first, then a low-rank bank
        k = max(1, n // 4); Bm = rng.integers(0, 3, size=(n, k)); out = []
        for i in range(m):
            if i % 3 == 0:
                out.append(np.eye(n, dtype=np.int64)[(i // 3) % n])
            else:
                out.append((Bm @ rng.integers(0, 3, k)) % 3)
        return out
    if name == "weight1":             # +-e_i only
        out = []
        for i in range(m):
            x = np.zeros(n, dtype=np.int64); x[int(rng.integers(0, n))] = int(rng.integers(1, 3)); out.append(x)
        return out
    if name == "weight2":
        out = []
        for i in range(m):
            x = np.zeros(n, dtype=np.int64); idx = rng.choice(n, 2, replace=False)
            x[idx] = rng.integers(1, 3, 2); out.append(x)
        return out
    if name.startswith("blockdiag"):  # every dependency is block-local (sparse)
        b = int(name[9:]); g = max(1, n // b); out = []
        T = np.eye(n, dtype=np.int64)
        for i in range(m):
            blk = int(rng.integers(0, g)); x = np.zeros(n, dtype=np.int64)
            hi = n if blk == g - 1 else (blk + 1) * b
            x[blk * b:hi] = rng.integers(0, 3, hi - blk * b)
            out.append(x)
        return out
    if name == "projective":          # all points of PG(2,3) embedded in a random 3-dim subspace, cycled
        pts = [np.array(p) for p in np.ndindex(3, 3, 3) if any(p)]
        Bm = rng.integers(0, 3, size=(n, 3)); return [(Bm @ pts[i % 26]) % 3 for i in range(m)]
    if name == "simplex_dual":        # columns of a simplex-code generator (all projective points of PG(k-1,3))
        k = min(n, 4); pts = []
        for p in np.ndindex(*([3] * k)):
            p = np.array(p)
            if any(p) and p[np.nonzero(p)[0][0]] == 1:
                pts.append(p)
        T = rand_inv(n)
        out = []
        for i in range(m):
            x = np.zeros(n, dtype=np.int64)
            off = (i // len(pts)) % max(1, n - k + 1)
            x[off:off + k] = pts[i % len(pts)]; out.append((T @ x) % 3)
        return out
    if name.startswith("series"):     # pool starts with series classes of size a (private coordinates)
        aa = min(int(name[6:]), n // 2 + 1); c = max(1, (n // 2) // (aa - 1)); priv = c * (aa - 1); com = n - priv
        T = rand_inv(n); out = []
        for blk in range(c):
            U = np.zeros((n, aa), dtype=np.int64)
            P = rng.integers(0, 3, size=(aa - 1, aa - 1))
            while __import__("f3").rank(P) < aa - 1:
                P = rng.integers(0, 3, size=(aa - 1, aa - 1))
            U[blk * (aa - 1):(blk + 1) * (aa - 1), :aa - 1] = P
            U[blk * (aa - 1):(blk + 1) * (aa - 1), aa - 1] = (-(P @ rng.integers(1, 3, aa - 1))) % 3
            U[priv:, :] = rng.integers(0, 3, size=(com, aa))
            out += [(T @ U[:, i]) % 3 for i in range(aa)]
        k = 0
        while len(out) < m:          # the next 3n columns avoid the private coordinates
            x = rng.integers(0, 3, n)
            if k < 3 * n:
                x[:priv] = 0
            k += 1; out.append((T @ x) % 3)
        return out[:m]
    raise ValueError(name)


FAMS = ["random", "duplicates", "dup_blocks", "negpairs", "chain3", "chain5", "chain9", "subspace",
        "flag", "coloops", "weight1", "weight2", "blockdiag2", "blockdiag4", "projective", "simplex_dual", "series3", "series4", "series7"]

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--fams":
        FAMS = args[1].split(","); args = args[2:]
    ns = [int(a) for a in args] or [4, 5, 8, 12, 20, 30]
    reps = 4
    print("family          n   m=ceil(bound)  guarantee   pulled(max)  stages  end reasons (count)            maxcls  max(wt-q)  ok")
    total = 0
    for n in ns:
        m = math.ceil(theorem_bound(n)); g = guarantee(n)
        assert g <= m
        for f in FAMS:
            pulled, stg, ends, mc, ex = [], [], {}, 1, -99
            for rep in range(reps):
                vecs = fam(f, n, m); assert len(vecs) == m
                W = WNEST(vecs)
                try:
                    S = W.run()
                except Fail as e:
                    print("FAIL", f, n, e); raise
                s = sum((vecs[i] for i in S), np.zeros(n, dtype=np.int64)) % 3
                assert len(S) > 0 and not np.any(s) and len(set(S)) == len(S)
                pulled.append(W.pulled); stg.append(len(W.log))
                ends[W.end] = ends.get(W.end, 0) + 1
                for L in W.log:
                    if "wt" in L:
                        mc = max(mc, L["maxcls"]); ex = max(ex, L["wt"] - L["q"])
                assert W.pulled <= g, (f, n, W.pulled, g)
                total += 1
            print(f"{f:14s} {n:3d}  {m:9d}  {g:9d}   {max(pulled):9d}  {max(stg):5d}   {','.join(f'{k}:{v}' for k,v in sorted(ends.items())):30s} {mc:3d}    {ex:5d}    ok")
            sys.stdout.flush()
    print(f"{total} runs: every witness nonempty, distinct indices, sums to 0 over the original vectors; "
          f"pulled <= guarantee(n) <= m in all")
