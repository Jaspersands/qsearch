"""Headline-20 referee: own executor for fragment-v2 Lemmas ell-tensor and ell-node, written from
their statements (not from the author's ell_exec.py).  Builds the cells/weights recursively, applies
a table C (C_y = z^y B(y)), takes kappa-th roots by table, and checks the output against the core's
definition of a kappa-solution (w in (P u 0)^M, w != 0, r^kappa = w, sum w_b lambda_b = 0).
A falsifier only."""
import numpy as np, json, sys, time, random
from verify_tl6 import lpr
SRC = "../2026-11-13-rees-k9-below-21/"
def nullspace(M, p):
    """basis of {x : M x = 0 mod p}, M an (m x n) int64 array."""
    M = M.copy() % p; m, n = M.shape; piv = []; r = 0
    for c in range(n):
        if r == m: break
        nzr = np.nonzero(M[r:, c])[0]
        if len(nzr) == 0: continue
        k = r + nzr[0]
        if k != r: M[[r, k]] = M[[k, r]]
        M[r] = M[r] * pow(int(M[r, c]), p - 2, p) % p
        col = M[:, c].copy(); col[r] = 0
        M = (M - np.outer(col, M[r])) % p
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    B = []
    for f in free:
        x = np.zeros(n, dtype=np.int64); x[f] = 1
        for i, c in enumerate(piv): x[c] = (-M[i, f]) % p
        B.append(x)
    return B
class Ctx:
    def __init__(s, p, k, rng):
        s.p, s.k, s.rng = p, k, rng
        s.xi = lpr(p); s.z = [pow(s.xi, m, p) for m in range(k)]
        s.zinv = [pow(v, p - 2, p) for v in s.z]
        lg = {}; x = 1
        for i in range(p - 1): lg[x] = i; x = x * s.xi % p
        s.cl = np.zeros(p, dtype=np.int64)
        for v, i in lg.items(): s.cl[v] = i % k
    def dep(s, M):
        """random nonzero null vector, scaled so that its first nonzero entry is 1."""
        B = s.nullspace(M)
        assert B, "no dependence: dimension count violated"
        while True:
            x = np.zeros(M.shape[1], dtype=np.int64)
            for b in B: x = (x + s.rng.randrange(s.p) * b) % s.p
            if x.any(): break
        f = np.nonzero(x)[0][0]
        return x * pow(int(x[f]), s.p - 2, s.p) % s.p, int(f)
    def nullspace(s, M): return nullspace(M, s.p)
FORCED = False
LASTNZ = [0]
def M_l(k, a, l):
    out = 1
    for t in range(l): out *= (k - 1) ** t * a + 1
    return out
def build(ctx, lam, ids, l, a):
    """returns (cell array (flattened y, -1 = none), weight array, T (k^l x a), bstar position)."""
    p, k = ctx.p, ctx.k
    if l == 1:
        Mx = lam[:, ids] if a > 0 else np.zeros((0, len(ids)), dtype=np.int64)
        if a == 0: c = np.zeros(len(ids), dtype=np.int64); c[0] = 1; f = 0
        else: c, f = ctx.dep(Mx)
        cell = np.where(c != 0, ctx.cl[c], -1)
        w = np.where(c != 0, c * np.array(ctx.zinv)[np.where(c != 0, ctx.cl[c], 0)] % p, 0)
        T = np.zeros((k, a), dtype=np.int64)
        for m in range(k):
            sel = cell == m
            if sel.any() and a: T[m] = (lam[:, ids[sel]] * w[sel]).sum(axis=1) % p
        return cell, w, T, f
    Mprev = M_l(k, a, l - 1); N = (k - 1) ** (l - 1) * a + 1
    assert len(ids) == N * Mprev
    # rows of T with y having no zero coordinate
    ys = np.arange(k ** (l - 1)); good = np.ones(len(ys), dtype=bool); t = ys.copy()
    for _ in range(l - 1): good &= (t % k) != 0; t //= k
    subs = []
    for mu in range(N):
        bid = ids[mu * Mprev:(mu + 1) * Mprev]
        sb = build(ctx, lam, bid, l - 1, a)
        tries = 0
        while FORCED and a and not (sb[2][good] % p).any() and tries < 50:
            # forced mode: resample this block's columns (the bank stays a valid input bank)
            lam[:, bid] = np.array([[ctx.rng.randrange(p) for _ in bid] for _ in range(a)], dtype=np.int64)
            sb = build(ctx, lam, bid, l - 1, a); tries += 1
        subs.append(sb)
    if a == 0:
        th = np.zeros(N, dtype=np.int64); th[0] = 1; f = 0
    else:
        Mx = np.stack([sb[2][good].reshape(-1) for sb in subs], axis=1)
        assert Mx.shape[0] == N - 1
        th, f = ctx.dep(Mx)
    cell = np.full(len(ids), -1, dtype=np.int64); w = np.zeros(len(ids), dtype=np.int64)
    T = np.zeros((k ** l, a), dtype=np.int64)
    for mu, (c0, w0, T0, f0) in enumerate(subs):
        if th[mu] == 0: continue
        j = int(ctx.cl[th[mu]]); wp = int(th[mu]) * ctx.zinv[j] % p
        sl = slice(mu * Mprev, (mu + 1) * Mprev)
        has = c0 >= 0
        cell[sl] = np.where(has, c0 * k + j, -1); w[sl] = np.where(has, w0 * wp % p, 0)
        T[np.arange(k ** (l - 1)) * k + j] = (T[np.arange(k ** (l - 1)) * k + j] + wp * T0) % p
    bstar = f * Mprev + subs[f][3]
    return cell, w, T, bstar
def run(p, k, l, a, Cflat, bank, rng):
    ctx = Ctx(p, k, rng); M = M_l(k, a, l)
    if bank == "uniform": lam = np.array([[rng.randrange(p) for _ in range(M)] for _ in range(a)], dtype=np.int64).reshape(a, M)
    elif bank == "zeroheavy": lam = np.array([[rng.randrange(p) if rng.random() < 0.2 else 0 for _ in range(M)] for _ in range(a)], dtype=np.int64).reshape(a, M)
    elif bank == "repeated": base = [rng.randrange(p) for _ in range(a)]; lam = np.array([[base[i] * rng.choice([1, p - 1]) % p for _ in range(M)] for i in range(a)], dtype=np.int64).reshape(a, M)
    elif bank == "rank1": u = [rng.randrange(1, p) for _ in range(a)]; lam = np.array([[u[i] * s % p for s in [rng.randrange(p) for _ in range(M)]] for i in range(a)], dtype=np.int64).reshape(a, M)
    cell, w, T, bstar = build(ctx, lam, np.arange(M), l, a)
    # recompute T from cells/weights and check the axis relations of Lemma ell-tensor directly
    T2 = np.zeros((k ** l, a), dtype=np.int64)
    for c in set(cell[cell >= 0].tolist()):
        sel = cell == c
        if a: T2[c] = (lam[:, sel] * w[sel]).sum(axis=1) % p
    axis_ok = bool((T2 == T).all()); LASTNZ[0] = int((T2 % p != 0).any(axis=1).sum())
    Tt = T2.reshape((k,) * l + (a,))
    z = np.array(ctx.z, dtype=np.int64).reshape((k,) + (1,) * (l - 1 + 1))
    for r in range(l):
        Tr = np.moveaxis(Tt, r, 0)
        axis_ok &= bool(((Tr * z).sum(axis=0) % p == 0).all())
    wP = all(pow(int(v), (p - 1) // k, p) == 1 for v in set(w[w != 0].tolist()))
    axis_ok &= wP and int(w[bstar]) == 1 and int(cell[bstar]) == 0
    # axis-relation check of T (each coordinate)
    x = np.where(cell >= 0, Cflat[np.maximum(cell, 0)] * w % p, 0)
    e = (p - 1) // k
    ok = bool(x.any()) and int(x[bstar]) != 0
    nzx = x[x != 0]
    ok &= all(pow(int(v), e, p) == 1 for v in set(nzx.tolist()))
    ok &= bool(((lam * x).sum(axis=1) % p == 0).all()) if a else True
    roots = {}
    for v in range(1, p): roots.setdefault(pow(v, k, p), v)
    r = np.array([roots.get(int(v), -1) if v else 0 for v in x])
    ok &= bool((r >= 0).all()) and all(pow(int(rr), k, p) == int(xx) for rr, xx in zip(r[:2000], x[:2000]))
    active = len(set(cell[cell >= 0].tolist()))
    return ok and axis_ok, active, M
TABLES = {(19, 9): "B4_19.json", (37, 9): "B4_37.json", (73, 9): "B4_73.json", (13, 4): "B3_13_4.json", (13, 6): "B3_13_6.json"}
def table(p, k, perturb=False, rng=None):
    d = json.load(open(SRC + TABLES[(p, k)])); l = len(next(iter(d)))
    xi = lpr(p); C = np.zeros(k ** l, dtype=np.int64)
    for key, b in d.items():
        y = [int(ch) for ch in key]; flat = 0
        for t in y: flat = flat * k + t
        C[flat] = b * pow(xi, sum(y), p) % p
    if perturb:
        e = (p - 1) // k; P = [v for v in range(1, p) if pow(v, e, p) == 1]
        nz = [i for i in range(1, len(C)) if C[i]]
        for i in rng.sample(nz, 3): C[i] = rng.choice([v for v in P if v != C[i]])
    return C, l
if __name__ == "__main__":
    rng = random.Random(2026); t0 = time.time()
    plan = [((13, 4), a, b, n) for a in (1, 2, 3) for b in ("uniform", "zeroheavy", "repeated", "rank1") for n in range(2)]
    plan += [((13, 6), a, b, n) for a in (1, 2, 3) for b in ("uniform", "zeroheavy", "repeated", "rank1") for n in range(2)]
    plan += [((p, 9), 1, b, 0) for p in (19, 37, 73) for b in ("uniform", "repeated")]
    tot = good = 0
    for (p, k), a, b, n in plan:
        C, l = table(p, k)
        ok, act, M = run(p, k, l, a, C, b, rng); tot += 1; good += ok
        print(f"p={p} k={k} l={l} a={a} bank={b}: columns={M} active cells={act}/{k**l} -> {'ok' if ok else 'FAIL'}", flush=True)
    print(f"genuine tables: {good}/{tot} ok, {round(time.time()-t0)} s")
    bad = tot2 = 0
    for (p, k), a in [((13, 4), 3), ((13, 6), 3), ((37, 9), 1), ((19, 9), 1)]:
        for n in range(3 if k < 9 else 1):
            C, l = table(p, k, perturb=True, rng=rng)
            ok, act, M = run(p, k, l, a, C, "zeroheavy" if k < 9 else "repeated", rng); tot2 += 1; bad += not ok
            print(f"  perturbed p={p} k={k} a={a}: active={act} -> {'FAIL (good)' if not ok else 'ok (undetected)'}", flush=True)
    print(f"perturbed tables (3 entries changed within P), degenerate-prone banks: {bad}/{tot2} runs FAIL")
    FORCED = True
    tot = good = 0
    for (p, k), a in [((13, 4), 1), ((13, 4), 2), ((13, 4), 3), ((13, 6), 1), ((13, 6), 2), ((13, 6), 3), ((19, 9), 1), ((37, 9), 1), ((73, 9), 1)]:
        for n in range(2 if k < 9 else 1):
            C, l = table(p, k)
            cell_ok, act, M = run(p, k, l, a, C, "uniform", rng); tot += 1; good += cell_ok
            print(f"  FORCED genuine p={p} k={k} a={a}: active={act}/{k**l} nonzeroT={LASTNZ[0]} -> {'ok' if cell_ok else 'FAIL'}", flush=True)
    print(f"FORCED genuine: {good}/{tot} ok")
    bad = tot2 = 0
    for (p, k), a in [((13, 4), 2), ((13, 4), 3), ((13, 6), 2), ((13, 6), 3), ((37, 9), 1), ((19, 9), 1), ((73, 9), 1)]:
        for n in range(3 if k < 9 else 1):
            C, l = table(p, k, perturb=True, rng=rng)
            ok, act, M = run(p, k, l, a, C, "uniform", rng); tot2 += 1; bad += not ok
            print(f"  FORCED perturbed p={p} k={k} a={a}: nonzeroT={LASTNZ[0]} -> {'FAIL (good)' if not ok else 'ok (undetected)'}", flush=True)
    print(f"FORCED perturbed: {bad}/{tot2} runs FAIL (want all)")
    print("time", round(time.time() - t0), "s")
