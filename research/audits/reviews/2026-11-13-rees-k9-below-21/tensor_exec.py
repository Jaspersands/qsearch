#!/opt/anaconda3/bin/python
"""End-to-end executor of the l-level tensor node (Lemma T_l + Lemma W_l of the report).  /opt/anaconda3/bin/python.

Written from the definitions; shares no code with chain_exec.py / ref_exec.py / sat3.py.
Level 1: a+1 fresh columns, a nonzero dependence c normalised c_{b*} = 1; cell i = cl(c_b), weight c_b / z_i in Q_0.
Level t: N_t = (kappa-1)^{t-1} a + 1 level-(t-1) objects; dependence theta of the vectors (T^mu[y])_{y in (Z_kappa\\0)^{t-1}};
         theta_{mu*} = 1; cell (y, cl(theta_mu)), weight factor theta_mu / z_{cl(theta_mu)}.
Asserted at every level (the lemma's claim): sum_{y_r} z_{y_r} T[.., y_r, ..] = 0 along every axis r,
the designated column lies in cell 0..0, cells are disjoint.
Output x_b = z^y B(y) w_b; checked: x != 0, every nonzero x_b in Q_0, sum x_b lambda_b = 0.
usage: tensor_exec.py p kappa K table.json a nbanks [bank types]
"""
import sys, os, json, random, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RND = random.Random(777)
sys.path.insert(0, HERE)
import ell_common as E


def nullvec(Mat, p):
    """nonzero x with Mat @ x = 0 mod p (Mat: d x n, n > rank)."""
    A = Mat.copy() % p
    d, n = A.shape
    piv, r = [], 0
    for c in range(n):
        if r == d: break
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0: continue
        q = r + nz[0]
        if q != r: A[[r, q]] = A[[q, r]]
        A[r] = A[r] * pow(int(A[r, c]), p - 2, p) % p
        others = np.nonzero(A[:, c])[0]
        for o in others:
            if o != r: A[o] = (A[o] - A[o, c] * A[r]) % p
        piv.append(c); r += 1
    frees = [c for c in range(n) if c not in piv]
    while True:
        # a random nonzero element of the null space (any nonzero dependence is allowed by the lemma;
        # a random one avoids the trivial early exits and exercises more cells)
        x = np.zeros(n, dtype=np.int64)
        for f in frees:
            x[f] = RND.randrange(p)
        if not x[frees].any():
            continue
        for i, c in enumerate(piv):
            x[c] = (-sum(int(A[i, f]) * int(x[f]) for f in frees)) % p
        break
    assert not ((Mat @ x) % p).any()
    return x


class Ctx:
    def __init__(s, p, k, a, cols):
        s.p, s.k, s.a, s.cols, s.next = p, k, a, cols, 0
        s.g = E.primitive_root(p)
        s.z = [pow(s.g, m, p) for m in range(k)]
        s.cl = {x: E.cls(x, p, s.g, k) for x in range(1, p)}
        s.used = 0
        s.more = None
        s.forced = False
        s.discarded = 0

    def fresh(s, n):
        idx = list(range(s.next, s.next + n)); s.next += n
        while s.next > len(s.cols):
            assert s.more is not None, 'bank exhausted'
            s.cols.extend(s.more(1 << 14))
        return idx


def axis_check(T, t, ctx):
    p, k = ctx.p, ctx.k
    z = np.array(ctx.z, dtype=np.int64)
    for r in range(t):
        s = np.tensordot(z, np.moveaxis(T, r, 0), axes=(0, 0)) % p
        assert not s.any(), ('axis relation fails', t, r)


def build(t, ctx):
    """returns (cells: dict y -> list of (b, w)), T (array shape (k,)*t + (a,)), designated column."""
    p, k, a = ctx.p, ctx.k, ctx.a
    if t == 1:
        idx = ctx.fresh(a + 1)
        Mat = np.array([ctx.cols[b] for b in idx], dtype=np.int64).T  # a x (a+1)
        c = nullvec(Mat, p)
        bstar = next(i for i in range(a + 1) if c[i])
        c = c * pow(int(c[bstar]), p - 2, p) % p
        cells, T = {}, np.zeros((k, a), dtype=np.int64)
        for i, b in enumerate(idx):
            if c[i]:
                m = ctx.cl[int(c[i])]
                w = int(c[i]) * pow(ctx.z[m], p - 2, p) % p
                assert ctx.cl[w] == 0
                cells.setdefault((m,), []).append((b, w))
                T[m] = (T[m] + w * np.array(ctx.cols[b], dtype=np.int64)) % p
        axis_check(T, 1, ctx)
        assert (0,) in cells and cells[(0,)][0][0] == idx[bstar]
        return cells, T, idx[bstar]
    N = (k - 1) ** (t - 1) * a + 1
    objs = []
    while len(objs) < N:
        o = build(t - 1, ctx)
        if ctx.forced and not o[1][tuple(slice(1, None) for _ in range(t - 1))].any():
            ctx.discarded += 1   # a 'lucky' object (T = 0 off the zero indices); discard to exercise B
            continue
        objs.append(o)
    sub = tuple(slice(1, None) for _ in range(t - 1))
    Mat = np.array([o[1][sub].reshape(-1) for o in objs], dtype=np.int64).T
    th = nullvec(Mat, p)
    mstar = next(i for i in range(N) if th[i])
    th = th * pow(int(th[mstar]), p - 2, p) % p
    cells, T = {}, np.zeros((k,) * t + (a,), dtype=np.int64)
    for mu, (oc, oT, _) in enumerate(objs):
        if not th[mu]: continue
        m = ctx.cl[int(th[mu])]
        w = int(th[mu]) * pow(ctx.z[m], p - 2, p) % p
        T[(Ellipsis, m, slice(None))] = (T[(Ellipsis, m, slice(None))] + w * oT) % p
        for y, lst in oc.items():
            cells.setdefault(y + (m,), []).extend((b, ww * w % p) for b, ww in lst)
    axis_check(T, t, ctx)
    des = objs[mstar][2]
    assert any(b == des for b, _ in cells.get((0,) * t, []))
    return cells, T, des


def run(p, k, K, B, l, a, cols, more=None, forced=False):
    ctx = Ctx(p, k, a, cols)
    ctx.more, ctx.forced = more, forced
    cells, T, des = build(l, ctx)
    seen = set()
    x = {}
    for y, lst in cells.items():
        Cy = pow(ctx.g, sum(y), p) * B[y] % p
        for b, w in lst:
            assert b not in seen; seen.add(b)
            x[b] = Cy * w % p
    tot = np.zeros(a, dtype=np.int64)
    for b, v in x.items():
        tot = (tot + v * np.array(cols[b], dtype=np.int64)) % p
    Ks = {m % k for m in K}
    okc = all(ctx.cl[v] in Ks for v in x.values() if v)
    nonzero = any(x.values())
    run.cover = sum(1 for y in cells if T[y].any())
    run.discarded = ctx.discarded
    return (not tot.any()) and okc and nonzero, ctx.next, x[des]


def arity(k, l, a):
    n = 1
    for t in range(l):
        n *= (k - 1) ** t * a + 1
    return n


def bank(kind, p, k, a, n, rnd):
    g = E.primitive_root(p)
    if kind == 'uniform':
        return [[rnd.randrange(p) for _ in range(a)] for _ in range(n)]
    if kind == 'repeated':
        v = [rnd.randrange(1, p) for _ in range(a)]
        return [v[:] for _ in range(n)]
    if kind == 'cosetline':   # columns q_b * v with q_b in one coset Q_c (c fixed per bank)
        v = [rnd.randrange(1, p) for _ in range(a)]; c = rnd.randrange(k)
        return [[pow(g, c + k * rnd.randrange((p - 1) // k), p) * vi % p for vi in v] for _ in range(n)]
    if kind == 'lowrank':
        U = [[rnd.randrange(p) for _ in range(a)] for _ in range(2)]
        out = []
        for _ in range(n):
            s, t = rnd.randrange(p), rnd.randrange(p)
            out.append([(s * U[0][i] + t * U[1][i]) % p for i in range(a)])
        return out
    if kind == 'zeros':
        return [([0] * a if rnd.random() < 0.5 else [rnd.randrange(p) for _ in range(a)]) for _ in range(n)]
    raise ValueError(kind)


if __name__ == '__main__':
    p, k = int(sys.argv[1]), int(sys.argv[2])
    K = [int(x) for x in sys.argv[3].split(',')]
    tab = json.load(open(sys.argv[4]))
    B = {tuple(int(c) for c in key): v for key, v in tab.items()}
    l = len(next(iter(B)))
    a, nb = int(sys.argv[5]), int(sys.argv[6])
    kinds = sys.argv[7].split(',') if len(sys.argv) > 7 else ['uniform', 'repeated', 'cosetline', 'lowrank', 'zeros']
    forced = len(sys.argv) > 8 and sys.argv[8] == 'forced'
    rnd = random.Random(12345)
    n = arity(k, l, a)
    tot = good = 0
    for kind in kinds:
        for _ in range(nb):
            cols = bank(kind, p, k, a, n, rnd)
            more = (lambda m, kind=kind: bank(kind, p, k, a, m, rnd)) if forced else None
            try:
                ok, used, xd = run(p, k, K, B, l, a, cols, more, forced)
            except AssertionError as e:
                ok, used, xd = False, -1, None
                print('   assertion:', e)
            tot += 1; good += ok
            print(f'p={p} k={k} l={l} a={a} bank={kind}: {"VERIFIED" if ok else "FAILED"} columns={used}/{n} cells_with_nonzero_T={getattr(run, "cover", -1)} discarded={getattr(run, "discarded", 0)}', flush=True)
    print(f'SUMMARY p={p} k={k} K={K} l={l} a={a} forced={forced}: {good}/{tot} verified')
