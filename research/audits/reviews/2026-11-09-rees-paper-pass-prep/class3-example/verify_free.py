"""Exact checks for the class-three worked example on the FREE two-generator class-three
Lie algebra (example_free.tex).

L = span(x, y, z, u, w), z = [x,y], u = [x,z], w = [y,z] (other basis brackets 0), p > 3.
Coordinates on L: (x, y, z, u, w) = indices 0..4.
Cover A, basis (index: element of L[t]):
  0 tx  1 ty  2 tz  3 tu  4 tw  5 t^2z  6 t^2u  7 t^2w  8 t^3u  9 t^3w
Main H:      h = F_p v,  v = x + z + u
Contrast H': h' = F_p c, c = z + u        (inside [G,G])

Each check prints [Fn] PASS/FAIL; README.md maps the claims of example_free.tex and
fixes.tex to these tags.  Usage:
  nice -n 19 /opt/anaconda3/bin/python verify_free.py
"""
import itertools
from math import gcd, log2, ceil
import numpy as np
import sympy as sp

FAILS = []


def check(tag, ok, msg):
    print(f"[{tag}] {'PASS' if ok else 'FAIL'}: {msg}", flush=True)
    if not ok:
        FAILS.append(tag)


M = 5
LNAMES = ["x", "y", "z", "u", "w"]
L_BR = {(0, 1): (2, 1), (0, 2): (3, 1), (1, 2): (4, 1)}
GRADE = np.array([1, 1, 1, 1, 1, 2, 2, 2, 3, 3])
LIDX = np.array([0, 1, 2, 3, 4, 2, 3, 4, 3, 4])
N = 10
CNAMES = ["tx", "ty", "tz", "tu", "tw", "t2z", "t2u", "t2w", "t3u", "t3w"]
GAMMA = {1: [0, 1, 2, 3, 4], 2: [2, 3, 4], 3: [3, 4]}

V_MAIN = (1, 0, 1, 1, 0)        # x + z + u
C_CONTR = (0, 0, 1, 1, 0)       # z + u
H_MAIN = [V_MAIN]
H_CONTR = [C_CONTR]
HLIFT_MAIN = [(1, 0, 1, 1, 0, 0, 0, 0, 0, 0)]                                   # t v
HLIFT_CONTR = [(0, 0, 1, 1, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 1, 1, 0, 0, 0)]  # t c, t^2 c
E_U = (0, 0, 0, 2, 0, 0, -3, 0, 1, 0)   # 2tu - 3t^2u + t^3u
E_W = (0, 0, 0, 0, 2, 0, 0, -3, 0, 1)   # 2tw - 3t^2w + t^3w


def L_tensor(p=None):
    T = np.zeros((M, M, M), dtype=np.int64)
    for (i, j), (k, v) in L_BR.items():
        T[i, j, k] = v
        T[j, i, k] = -v
    return T % p if p else T


def cover_tensor():
    TL = L_tensor()
    T = np.zeros((N, N, N), dtype=np.int64)
    pos = {(GRADE[a], LIDX[a]): a for a in range(N)}
    for a in range(N):
        for b in range(N):
            v = TL[LIDX[a], LIDX[b]]
            g = GRADE[a] + GRADE[b]
            if not v.any():
                continue
            assert g <= 3, "nonzero bracket above class 3"
            for k in np.nonzero(v)[0]:
                assert k in GAMMA[g]
                T[a, b, pos[(g, k)]] = v[k]
    return T


def hand_cover_tensor():
    T = np.zeros((N, N, N), dtype=np.int64)
    for a, b, c in [(0, 1, 5), (0, 2, 6), (1, 2, 7), (0, 5, 8), (1, 5, 9)]:
        T[a, b, c] = 1
        T[b, a, c] = -1
    return T


def br(T, x, y, p):
    n = T.shape[0]
    x, y = np.broadcast_arrays(x, y)
    outer = (x[..., :, None] * y[..., None, :]).reshape(x.shape[:-1] + (n*n,))
    return (outer @ T.reshape(n*n, n)) % p


def bch(T, x, y, p):
    i2, i12 = pow(2, -1, p), pow(12, -1, p)
    xy = br(T, x, y, p)
    return (x + y + i2*xy + i12*(br(T, x, xy, p) + br(T, y, br(T, y, x, p), p))) % p


def Emat(s, p):
    E = np.zeros((N, M), dtype=np.int64)
    for j in range(N):
        E[j, LIDX[j]] = pow(s, int(GRADE[j]), p)
    return E


def dil(theta, a, p):
    return (a * np.array([pow(theta, int(g), p) for g in GRADE])) % p


def enc(v, p):
    return (v * (p ** np.arange(v.shape[-1]))).sum(-1)


def all_vectors(dim, p):
    return np.array(list(itertools.product(range(p), repeat=dim)), dtype=np.int64)[:, ::-1]


def span(basis, dim, p):
    basis = np.array(basis, dtype=np.int64).reshape(-1, dim)
    if len(basis) == 0:
        return np.zeros((1, dim), dtype=np.int64)
    return (all_vectors(len(basis), p) @ basis) % p


def rank(rows, p):
    m = [[int(x) % p for x in r] for r in rows]
    if not m:
        return 0
    r = 0
    for c in range(len(m[0])):
        piv = next((i for i in range(r, len(m)) if m[i][c]), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], -1, p)
        m[r] = [x*inv % p for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f*y) % p for x, y in zip(m[i], m[r])]
        r += 1
    return r


def in_span(basis, v, p):
    return rank(list(basis) + [v], p) == rank(list(basis), p)


def nullspace(A, ncol, p):
    A = [[int(x) % p for x in r] for r in A]
    piv, r = [], 0
    for c in range(ncol):
        k = next((i for i in range(r, len(A)) if A[i][c]), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [x*inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f*y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    out = []
    for f in [c for c in range(ncol) if c not in piv]:
        v = [0]*ncol
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][f]) % p
        out.append(v)
    return out


def hlift_from_definition(h, p):
    rows = []
    for k in (1, 2, 3):
        # h cap gamma_k by linear algebra: combinations of h with zero coords outside gamma_k
        H = np.array(h, dtype=np.int64).reshape(-1, M)
        if len(H) == 0:
            continue
        outside = [i for i in range(M) if i not in GAMMA[k]]
        coeffs = nullspace(H[:, outside].T.tolist(), len(H), p) if outside else np.eye(len(H), dtype=int).tolist()
        for cf in coeffs:
            vec = (np.array(cf) @ H) % p
            row = [0]*N
            for j in range(N):
                if GRADE[j] == k:
                    row[j] = int(vec[LIDX[j]])
            rows.append(row)
    return rows


def pullback(h, points, p):
    """{a in A : E_s(a) in h for s in points}, by linear algebra."""
    H = np.array(h, dtype=np.int64).reshape(-1, M)
    F = nullspace(H.tolist(), M, p) if len(H) else np.eye(M, dtype=int).tolist()   # h^perp
    rows = []
    for s in points:
        E = Emat(s, p)
        for f in F:
            rows.append(list((E @ np.array(f)) % p))
    return nullspace(rows, N, p) if rows else np.eye(N, dtype=int).tolist()


def same(A, B, p):
    return rank(A, p) == rank(B, p) == rank(list(A) + list(B), p)


# ---------------------------------------------------------------- F1 structure
def f1(p):
    T = cover_tensor() % p
    check("F1a", np.array_equal(T, hand_cover_tensor() % p),
          f"p={p}: cover brackets: [tx,ty]=t2z, [tx,tz]=t2u, [ty,tz]=t2w, [tx,t2z]=t3u, [ty,t2z]=t3w, others 0")
    I, J = np.eye(N, dtype=np.int64), np.eye(M, dtype=np.int64)
    TL = L_tensor(p)
    jac = all(not ((br(T, I[a], br(T, I[b], I[c], p), p) + br(T, I[b], br(T, I[c], I[a], p), p)
                    + br(T, I[c], br(T, I[a], I[b], p), p)) % p).any()
              for a in range(N) for b in range(N) for c in range(N))
    jacL = all(not ((br(TL, J[a], br(TL, J[b], J[c], p), p) + br(TL, J[b], br(TL, J[c], J[a], p), p)
                     + br(TL, J[c], br(TL, J[a], J[b], p), p)) % p).any()
               for a in range(M) for b in range(M) for c in range(M))
    check("F1b", jac and jacL, f"p={p}: Jacobi on L and on A")
    # lower central series of L
    def lcs_next(basis):
        return [br(TL, J[i], np.array(b), p) for i in range(M) for b in basis]
    g2 = lcs_next(J)
    g3 = lcs_next(g2)
    g4 = lcs_next(g3)
    ok = rank(g2, p) == 3 and all(in_span([J[2], J[3], J[4]], v, p) for v in g2) \
        and rank(g3, p) == 2 and all(in_span([J[3], J[4]], v, p) for v in g3) and rank(g4, p) == 0
    check("F1c", ok, f"p={p}: gamma_2 = span(z,u,w), gamma_3 = span(u,w), gamma_4 = 0: (g1,g2,g3) = (5,3,2), n = 10")
    allL = all_vectors(M, p)
    cent = [v for v in allL if all(not br(TL, v, J[b], p).any() for b in range(M))]
    check("F1d", len(cent) == p**2 and all(not v[:3].any() for v in cent), f"p={p}: Z(L) = gamma_3 = span(u,w)")
    if p == 5:
        allA = all_vectors(N, p)
        ok = np.ones(len(allA), dtype=bool)
        for b in range(N):
            ok &= ~br(T, allA, I[b], p).any(-1)
        cA = allA[ok]
        check("F1e", len(cA) == p**6 and not cA[:, [0, 1, 2, 5]].any(),
              f"p={p}: Z(A) = span(tu, tw, t2u, t2w, t3u, t3w) ({len(cA)} elements)")
    okE = all(np.array_equal(br(T, I[a], I[b], p) @ Emat(s, p) % p,
                             br(TL, I[a] @ Emat(s, p) % p, I[b] @ Emat(s, p) % p, p))
              for s in range(p) for a in range(N) for b in range(N))
    okD = all(np.array_equal(dil(th, br(T, I[a], I[b], p), p), br(T, dil(th, I[a], p), dil(th, I[b], p), p))
              for th in range(1, p) for a in range(N) for b in range(N))
    check("F1f", okE and okD, f"p={p}: E_s Lie homomorphisms, delta_theta Lie automorphisms")
    trip = br(T, br(T, I[0], I[1], p), I[0], p)
    check("F1g", trip.any(), f"p={p}: [[tx,ty],tx] = -t3u != 0: A has class 3")
    return T


def f2_symbolic():
    s, th = sp.symbols('s theta')
    a, b, cc = sp.symbols('a0:10'), sp.symbols('b0:10'), sp.symbols('c0:10')
    TA, TL = hand_cover_tensor(), L_tensor()

    def sbr(T, x, y, n):
        return [sp.expand(sum(T[i, j, k]*x[i]*y[j] for i in range(n) for j in range(n) if T[i, j, k]))
                for k in range(n)]

    def sbch(T, x, y, n):
        xy = sbr(T, x, y, n)
        t1, t2 = sbr(T, x, xy, n), sbr(T, y, sbr(T, y, x, n), n)
        return [sp.expand(x[k] + y[k] + sp.Rational(1, 2)*xy[k] + sp.Rational(1, 12)*(t1[k] + t2[k])) for k in range(n)]

    def sE(x):
        out = [0]*M
        for j in range(N):
            out[LIDX[j]] += s**int(GRADE[j])*x[j]
        return [sp.expand(o) for o in out]

    def sD(x):
        return [sp.expand(th**int(GRADE[j])*x[j]) for j in range(N)]

    okE = all(sp.expand(l - r) == 0 for l, r in zip(sE(sbch(TA, a, b, N)), sbch(TL, sE(a), sE(b), M)))
    okD = all(sp.expand(l - r) == 0 for l, r in zip(sD(sbch(TA, a, b, N)), sbch(TA, sD(a), sD(b), N)))
    assoc = all(sp.expand(l - r) == 0 for l, r in zip(sbch(TA, sbch(TA, a, b, N), cc, N), sbch(TA, a, sbch(TA, b, cc, N), N)))
    check("F2a", okE, "symbolic over Q: E_s(a*b) = E_s(a)*E_s(b), generic a, b in A and s (class-3 BCH)")
    check("F2b", okD, "symbolic over Q: delta_theta is a BCH homomorphism")
    check("F2c", assoc, "symbolic over Q: BCH_3 on A is associative")


def f2_numeric(T, p, trials=20000):
    rng = np.random.default_rng(11 + p)
    a, b = rng.integers(0, p, (trials, N)), rng.integers(0, p, (trials, N))
    TL = L_tensor(p)
    ok = all(np.array_equal(bch(T, a, b, p) @ Emat(s, p) % p, bch(TL, a @ Emat(s, p) % p, b @ Emat(s, p) % p, p))
             for s in range(p))
    check("F2d", ok, f"p={p}: {trials} random pairs, E_s respects BCH mod p for all s")


# ---------------------------------------------------------------- F3 tuple-oracle fibres
def left_coset_labels(TL, h, p):
    G = all_vectors(M, p)
    lab = np.full(len(G), p**M)
    for hh in span(h, M, p):
        lab = np.minimum(lab, enc(bch(TL, G, np.broadcast_to(hh, G.shape), p), p))
    table = np.zeros(p**M, dtype=np.int64)
    table[enc(G, p)] = lab
    return table


def f3_fibres(T, p, h, hlift, name, chunk=400000):
    TL = L_tensor(p)
    closed = all(in_span(h, br(TL, np.array(x), np.array(y), p), p) for x in h for y in h)
    check("F3a", closed and same(hlift_from_definition(h, p), hlift, p),
          f"p={p} {name}: h is a subalgebra and sum_k t^k (h cap gamma_k) = span{[list(v) for v in hlift]}")
    G = all_vectors(M, p)
    normal = all(in_span(h, br(TL, G[i], np.array(hv), p), p) for i in range(len(G)) for hv in h)
    check("F3b", not normal, f"p={p} {name}: h is not an ideal (H not normal)")
    f = left_coset_labels(TL, h, p)
    rng = np.random.default_rng(3)
    idx = rng.integers(0, len(G), (20000, 2))
    x, y = G[idx[:, 0]], G[idx[:, 1]]
    q = bch(TL, (-x) % p, y, p)
    inh = np.array([in_span(h, vv, p) for vv in q])
    check("F3c", np.array_equal(f[enc(x, p)] == f[enc(y, p)], inh), f"p={p} {name}: f hides H (20000 random pairs)")
    # all of A, in chunks: hat f, fibre sizes, invariance under right multiplication by hlift generators
    total = p**N
    hats = np.empty(total, dtype=np.int64)
    hats2 = np.empty(total, dtype=np.int64)
    invariant = True
    gens = [np.array(g) % p for g in hlift]
    E1, E2, E3 = Emat(1, p), Emat(2, p), Emat(3, p)

    def hatf(a):
        return (f[enc(a @ E1 % p, p)] * p**M + f[enc(a @ E2 % p, p)]) * p**M + f[enc(a @ E3 % p, p)]

    weights = p ** np.arange(N)
    for st in range(0, total, chunk):
        ids = np.arange(st, min(st+chunk, total))
        a = (ids[:, None] // weights) % p
        hv = hatf(a)
        hats[st:st+len(ids)] = hv
        hats2[st:st+len(ids)] = f[enc(a @ E1 % p, p)] * p**M + f[enc(a @ E2 % p, p)]
        for g in gens:
            if not np.array_equal(hatf(bch(T, a, np.broadcast_to(g, a.shape), p)), hv):
                invariant = False
    _, counts = np.unique(hats, return_counts=True)
    size = p**len(hlift)
    check("F3d", invariant and (counts == size).all() and len(counts) == total // size,
          f"p={p} {name}: EXHAUSTIVE over all {total} points of A: hat f is constant on every left coset "
          f"a*exp(hlift) (invariant under right multiplication by the generators of hlift) and every fibre has "
          f"exactly p^{len(hlift)} points, so the fibres are exactly these cosets ({len(counts)} fibres)")
    _, c2 = np.unique(hats2, return_counts=True)
    print(f"      p={p} {name}: two-point oracle (f E_1, f E_2): {len(c2)} fibres, sizes {sorted(set(c2.tolist()))}")
    fib0 = np.nonzero(hats == hats[0])[0]
    a0 = (fib0[:, None] // weights) % p
    check("F3e", set(enc(a0, p).tolist()) == set(enc(span(hlift, N, p), p).tolist()),
          f"p={p} {name}: fibre of hat f over 0 is exactly hlift ({len(fib0)} points)")
    return c2


# ---------------------------------------------------------------- F4 points
def f4_points(p, h, hlift, name):
    P123, P12, P1 = pullback(h, (1, 2, 3), p), pullback(h, (1, 2), p), pullback(h, (1,), p)
    check("F4a", same(P123, hlift, p) and same(pullback(h, range(1, p), p), hlift, p),
          f"p={p} {name}: three-point pullback = hlift = intersection over all s in F_p^x")
    eu, ew = [x % p for x in E_U], [x % p for x in E_W]
    check("F4b", same(P12, list(hlift) + [eu, ew], p),
          f"p={p} {name}: two-point pullback = hlift + span(e_u, e_w), e_u = 2tu-3t^2u+t^3u, e_w = 2tw-3t^2w+t^3w "
          f"(dim {rank(P12, p)} vs {len(hlift)})")
    if name == "H":
        evals = [(np.array(eu) @ Emat(s, p) % p).tolist() for s in range(1, p)]
        ok = all(evals[s-1] == [0, 0, 0, (s*(s-1)*(s-2)) % p, 0] for s in range(1, p))
        check("F4c", ok and evals[2] == [0, 0, 0, 6 % p, 0],
              f"p={p}: E_s(e_u) = s(s-1)(s-2) u: E_1 = E_2 = 0, E_3(e_u) = 6u, not in h")

    def pres(P):
        return [th for th in range(2, p) if rank(list(P) + [dil(th, np.array(v), p).tolist() for v in P], p) == rank(P, p)]
    check("F4d", pres(P12) == [] and pres(P1) == [] and pres(hlift) == list(range(2, p)),
          f"p={p} {name}: dilations theta != 1 preserving: E_1^-1(h): {pres(P1)}; two-point pullback: {pres(P12)}; "
          f"hlift: {pres(hlift)}")


def f4_remark(p):
    """fixes.tex (b): k points s=1..k give a pullback preserved by EVERY dilation iff gamma_(k+1) in h;
    then it equals hlift. Checked for k = 1, 2, 3 on every Lie subalgebra of L."""
    TL = L_tensor(p)
    subs = subalgebras(TL, p)
    bad = []
    for B in subs:
        hl = hlift_from_definition(B.tolist(), p)
        for k in (1, 2, 3):
            P = pullback(B.tolist(), range(1, k+1), p)
            pr = all(rank(list(P) + [dil(th, np.array(v), p).tolist() for v in P], p) == rank(P, p)
                     for th in range(2, p))
            g = [np.eye(M, dtype=int)[i].tolist() for i in GAMMA.get(k+1, [])]
            cont = all(in_span(B.tolist(), v, p) for v in g) if len(B) else not g
            eq = same(P, hl, p) if hl else rank(P, p) == 0
            if pr != cont or (cont and not eq) or (not cont and eq):
                bad.append((B.tolist(), k, pr, cont, eq))
    check("F4e", not bad, f"p={p}: for k = 1, 2, 3 and EVERY one of the {len(subs)} subalgebras h: the pullback at "
                          f"1..k is preserved by every dilation iff gamma_(k+1) in h, and then equals hlift "
                          f"(otherwise strictly larger). bad: {bad[:2]}")
    return subs


def subalgebras(TL, p):
    out = []
    for k in range(0, M+1):
        for piv in itertools.combinations(range(M), k):
            free = [(r, c) for r in range(k) for c in range(M) if c > piv[r] and c not in piv]
            for vals in itertools.product(range(p), repeat=len(free)):
                B = np.zeros((k, M), dtype=np.int64)
                for r, c in enumerate(piv):
                    B[r, c] = 1
                for (r, c), v in zip(free, vals):
                    B[r, c] = v
                if all(in_span(B, br(TL, B[i], B[j], p), p) for i in range(k) for j in range(i+1, k)):
                    out.append(B)
    return out


# ---------------------------------------------------------------- F5 automorphisms (p = 5)
def automorphisms(p):
    TL = L_tensor(p)
    V = all_vectors(M, p)
    out = []
    for v1 in V:
        P1 = np.broadcast_to(v1, V.shape)
        P2 = V
        P3 = br(TL, P1, P2, p)
        P4 = br(TL, P1, P3, p)
        P5 = br(TL, P2, P3, p)
        ok = np.ones(len(V), dtype=bool)
        imgs = [P1, P2, P3, P4, P5]
        for i in range(M):
            for j in range(i+1, M):
                lhs = br(TL, imgs[i], imgs[j], p)
                k = L_BR.get((i, j))
                rhs = imgs[k[0]] if k else np.zeros_like(lhs)
                ok &= (lhs == rhs).all(1)
        mats = np.stack(imgs, axis=1)[ok]
        det = np.round(np.linalg.det(mats.astype(float))).astype(np.int64) % p
        out.append(mats[det != 0].astype(np.int8))
    return np.concatenate(out)


def line_stab(auts, v, p):
    v = np.array(v, dtype=np.int64)
    r = np.zeros((len(auts), M), dtype=np.int16)
    for i in np.nonzero(v)[0]:
        r += int(v[i]) * auts[:, i, :].astype(np.int16)
    r = r.astype(np.int64) % p
    ok = np.ones(len(auts), dtype=bool)
    for i in range(M):
        for j in range(i+1, M):
            ok &= ((r[:, i]*v[j] - r[:, j]*v[i]) % p) == 0
    return ok


def central_info(auts, p):
    C = auts[:, 3:5, 3:5].astype(np.int64) % p        # action on span(u,w), rows = images of u, w
    scal = (C[:, 0, 1] == 0) & (C[:, 1, 0] == 0) & (C[:, 0, 0] == C[:, 1, 1])
    return C, scal, sorted(set(C[scal][:, 0, 0].tolist()))


def f5_auts(p):
    auts = automorphisms(p)
    gl2 = (p**2-1)*(p**2-p)
    check("F5a", len(auts) == gl2 * p**6, f"p={p}: |Aut(L)| = {len(auts)} = |GL_2(F_p)| p^6 (exhaustive over images of x, y)")
    A = auts[:, :2, :2].astype(np.int64) % p
    detA = (A[:, 0, 0]*A[:, 1, 1] - A[:, 0, 1]*A[:, 1, 0]) % p
    C, scal, sc = central_info(auts, p)
    # the action on gamma_3 is det(A) * A (in the basis u, w), with A the action on L/gamma_2
    pred = (detA[:, None, None] * A) % p
    check("F5b", np.array_equal(C, pred), f"p={p}: Aut(L) acts on Z(L) = span(u,w) by det(A) A, A = action on L/[L,L]")
    lin_scalar = (A[:, 0, 1] == 0) & (A[:, 1, 0] == 0) & (A[:, 0, 0] == A[:, 1, 1])
    cubes = sorted(set(pow(a, 3, p) for a in range(1, p)))
    check("F5c", np.array_equal(scal, lin_scalar) and sc == cubes
          and (C[scal][:, 0, 0] == (A[scal][:, 0, 0]**3) % p).all(),
          f"p={p}: an automorphism acts on the centre by a scalar zeta iff A = a I, and then zeta = a^3; "
          f"scalars occurring: {sc} (the cubes)")
    out = {}
    for name, v in (("H", V_MAIN), ("H'", C_CONTR)):
        st = line_stab(auts, v, p)
        Cs, ss, scs = central_info(auts[st], p)
        nmat = len(set(map(lambda m: m.tobytes(), Cs)))
        out[name] = (int(st.sum()), scs)
        print(f"      p={p} {name}: |Stab(h)| = {int(st.sum())}, acts on the centre through {nmat} matrices, scalars {scs}")
    check("F5d", out["H"][1] == cubes and out["H'"][1] == cubes,
          f"p={p}: Stab(h) acts on the centre by every cube scalar, for h = F_p(x+z+u) (|Stab| = {out['H'][0]}) "
          f"and h' = F_p(z+u) (|Stab| = {out[chr(72)+chr(39)][0]})")
    # torus diag(a,b) (graded automorphisms with diagonal A) preserving h: only identity
    tor = [(a, b) for a in range(1, p) for b in range(1, p)
           if rank([V_MAIN, (np.array(V_MAIN) * [a, b, a*b, a*a*b, a*b*b]) % p], p) == 1]
    check("F5e", tor == [(1, 1)], f"p={p} H: torus elements x->ax, y->by preserving h: {tor}")
    # graded automorphisms (A in GL_2 acting on each grade) preserving h
    graded = auts[(auts[:, 0, 2:] == 0).all(1) & (auts[:, 1, 2:] == 0).all(1)]
    gs = graded[line_stab(graded, V_MAIN, p)]
    Cg, sg, scg = central_info(gs, p)
    check("F5f", len(graded) == gl2 and scg == [1] and len(gs) == p,
          f"p={p} H: of the {len(graded)} graded automorphisms, {len(gs)} preserve h (x->x, y->y+cx); their "
          f"central scalars: {scg}")
    # explicit conjugator phi(x) = v, phi(y) = y and psi_theta = phi delta_theta phi^-1
    phi = None
    for m_ in auts[(auts[:, 1] == np.array([0, 1, 0, 0, 0])).all(1) & (auts[:, 0] == np.array(V_MAIN)).all(1)]:
        phi = m_.astype(np.int64)
    check("F5g", phi is not None and np.array_equal(phi, np.array(
        [[1, 0, 1, 1, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, p-1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])),
        f"p={p}: phi(x) = x+z+u, phi(y) = y extends to the automorphism z -> z-w, u -> u, w -> w")
    TLp = L_tensor(p)

    def is_aut(Mx):
        rows = [Mx[i] for i in range(M)]
        for i in range(M):
            for j in range(i+1, M):
                k = L_BR.get((i, j))
                rhs = rows[k[0]] if k else np.zeros(M, dtype=np.int64)
                if not np.array_equal(br(TLp, rows[i], rows[j], p), rhs % p):
                    return False
        return round(np.linalg.det(Mx.astype(float))) % p != 0
    phinv = np.round(np.linalg.inv(phi.astype(float))).astype(np.int64) % p
    good = True
    for th in range(1, p):
        D = np.diag([th, th, th**2 % p, th**3 % p, th**3 % p])
        Cm = (phinv @ D @ phi) % p          # row convention: v -> v phi^-1 D phi = phi o delta o phi^-1
        formula = np.array([[th, 0, (th-th**2) % p, (th-th**3) % p, (th**2-th**3) % p], [0, th, 0, 0, 0],
                            [0, 0, th**2 % p, 0, (th**3-th**2) % p], [0, 0, 0, th**3 % p, 0],
                            [0, 0, 0, 0, th**3 % p]], dtype=np.int64)
        r = (np.array(V_MAIN) @ Cm) % p
        good &= np.array_equal(Cm, formula) and is_aut(Cm) and rank([V_MAIN, r], p) == 1
    check("F5h", good, f"p={p}: psi_theta: x -> theta x + (theta-theta^2) z + (theta-theta^3) u + (theta^2-theta^3) w, y -> theta y, "
                       f"z -> theta^2 z + (theta^3-theta^2) w, u, w -> theta^3 u, theta^3 w is an automorphism "
                       f"preserving h, central scalar theta^3")
    # families
    G = all_vectors(M, p)
    TL = L_tensor(p)
    conj = set()
    vv = np.broadcast_to(np.array(V_MAIN), G.shape)
    cj = bch(TL, bch(TL, G, vv, p), (-G) % p, p)              # g * v * g^-1
    for r in cj:
        r = r.tolist()
        lead = next(x for x in r if x)
        conj.add(tuple((x * pow(lead, -1, p)) % p for x in r))
    fams = {"conjugates of H": sorted(conj),
            "lines F_p(v + q), q in gamma_3": [tuple((np.array(V_MAIN) + [0, 0, 0, a, b]) % p) for a in range(p) for b in range(p)],
            "lines F_p(x + c), c in gamma_2": [(1, 0, a, b, c) for a in range(p) for b in range(p) for c in range(p)]}
    res = {}
    for fname, lines in fams.items():
        keep = np.ones(len(auts), dtype=bool)
        for l in lines:
            keep &= line_stab(auts, l, p)
        Cf, sf, scf = central_info(auts[keep], p)
        mats = sorted(set(tuple(m.ravel().tolist()) for m in Cf))
        res[fname] = (len(lines), int(keep.sum()), scf, len(mats))
        print(f"      p={p} family '{fname}' ({len(lines)} lines): joint stabilizer {int(keep.sum())}, central "
              f"scalars {scf}, acts on the centre through {len(mats)} matrices")
    check("F5i", res["lines F_p(x + c), c in gamma_2"][2] == [1] and res["lines F_p(x + c), c in gamma_2"][3] == 1,
          f"p={p}: no H-independent family scales the centre: the joint stabilizers of the {res['conjugates of H'][0]} "
          f"conjugates of H, of the {p*p} lines F_p(v+q) (q central) and of the {p**3} lines F_p(x+c) "
          f"(c in [L,L]) act on the centre with scalars {res['conjugates of H'][2]}, "
          f"{res['lines F_p(v + q), q in gamma_3'][2]}, {res['lines F_p(x + c), c in gamma_2'][2]}")
    return auts


def f5_all_subalgebras(auts, subs, p, chunk=500000):
    """Every subalgebra is Aut-conjugate to a coordinate subalgebra (which the torus x->ax, y->by
    preserves; that torus contains x->ax, y->ay with central scalar a^3)."""
    def key(B):
        k = B.shape[-2]
        cols = list(itertools.combinations(range(M), k))
        mins = np.stack([np.round(np.linalg.det(B[..., :, list(c)].astype(float))).astype(np.int64) % p
                         for c in cols], -1)
        first = np.argmax(mins != 0, -1)
        lead = np.take_along_axis(mins, first[..., None], -1)[..., 0]
        inv = np.array([0] + [pow(int(x), -1, p) for x in range(1, p)])[lead]
        return enc((mins * inv[..., None]) % p, p)
    allkeys = {}
    for B in subs:
        if 0 < len(B) < M:
            allkeys.setdefault(len(B), set()).add(int(key(B[None])[0]))
    coord = [B for B in subs if 0 < len(B) < M and ((B != 0).sum(1) == 1).all()]
    reach = {}
    for B in coord:
        for st in range(0, len(auts), chunk):
            img = (B[None].astype(np.int64) @ auts[st:st+chunk].astype(np.int64)) % p
            reach.setdefault(len(B), set()).update(key(img).tolist())
    ok = all(allkeys[k] <= reach.get(k, set()) for k in allkeys)
    check("F5j", ok, f"p={p}: each of the {len(subs)} subalgebras is Aut(L)-conjugate to one of the {len(coord)+2} "
                     f"coordinate subalgebras; so Stab(h) acts on the centre by every cube scalar, for EVERY subgroup")


# ---------------------------------------------------------------- F6 arities and labels
def Gf(d, a):
    return d**(d*(d-1)//2) * (a+1)**d


def Bf(d, a):
    return Gf(d, a) ** ceil(log2(d+1))


def zero_free_max(d, g, p, cap=8):
    """Largest length of a sequence of labels in F_p^g with NO nonzero s, sum s_i^d lambda_i = 0
    (exhaustive DFS over multisets; signed-power-set reachability)."""
    W = sorted(set(pow(x, d, p) for x in range(1, p)))          # nonzero d-th powers
    labels = [l for l in itertools.product(range(p), repeat=g) if any(l)]
    L = len(labels)
    encl = [sum(c * p**i for i, c in enumerate(l)) for l in labels]
    size = p**g

    digits = [[(a // p**i) % p for i in range(g)] for a in range(size)]
    ADD = [[sum(((digits[a][i] + digits[b][i]) % p) * p**i for i in range(g)) for b in range(size)] for a in range(size)]

    def addv(a, b):
        return ADD[a][b]
    mult = {(w, j): sum(((w * ((encl[j] // p**i) % p)) % p) * p**i for i in range(g)) for w in W for j in range(L)}
    best = [0, None]

    def dfs(start, reach, depth, seq):
        # reach: set of sums of nontrivial-or-empty combos (0 = empty); zero-free if 0 only from empty
        if depth > best[0]:
            best[0], best[1] = depth, list(seq)
        if depth >= cap:
            return
        for j in range(start, L):
            new = set(reach)
            bad = False
            for r in reach:
                for w in W:
                    t = addv(r, mult[(w, j)])
                    if t == 0:
                        bad = True
                        break
                    new.add(t)
                if bad:
                    break
            if not bad:
                dfs(j, new, depth + 1, seq + [labels[j]])
    dfs(0, {0}, 0, [])
    return best


def f6(p):
    k3, k2 = gcd(3, p-1), gcd(2, p-1)
    check("F6a", Bf(3, 2) == 531441 and Bf(2, 3) == 1024,
          f"B_3(2) = G(3,2)^2 = {Gf(3,2)}^2 = {Bf(3,2)}; B_2(3) = G(2,3)^2 = {Gf(2,3)}^2 = {Bf(2,3)}")
    Q = 3*(5+1)*Bf(2, 3)*Bf(3, 2)
    check("F6b", abs(log2(Q) - 33.19) < 0.005, f"Q_q = 3(5+1) B_2(3) B_3(2) = {Q} = 2^{log2(Q):.4f} (Table 1: 33.19)")
    b3 = zero_free_max(3, 2, p)
    nu = next(x for x in range(2, p) if pow(x, (p-1)//2, p) == p-1)
    ce = []
    for i in range(3):
        e = [0, 0, 0]
        e[i] = 1
        f_ = [0, 0, 0]
        f_[i] = (-nu) % p
        ce += [tuple(e), tuple(f_)]
    lam = np.array(ce, dtype=np.int64)
    S6 = all_vectors(6, p)[1:]
    nsol = int((((S6**2 % p) @ lam % p) == 0).all(1).sum())
    b2 = [6 if nsol == 0 else None, ce]
    print(f"      p={p}: kappa_3 = {k3}, kappa_2 = {k2}; Chevalley-Warning arities: stage 3 {k3*2+1}, stage 2 {k2*3+1}")
    check("F6c", b2[0] == 6,
          f"p={p}: stage 2 (three quadratic equations, labels in F_p^3): the 6 labels {b2[1]} (nu = {nu} a nonsquare) "
          f"admit no nonzero solution, so with Chevalley-Warning the exact minimum arity is 7")
    exp3 = 2 if k3 == 1 else None
    check("F6d", (b3[0] == exp3) if k3 == 1 else (b3[0] + 1 <= 7),
          f"p={p}: stage 3 (two cubic equations, labels in F_p^2): longest zero-free label sequence has length "
          f"{b3[0]} (e.g. {b3[1]}), so the exact minimum arity is {b3[0]+1} (Chevalley-Warning: {k3*2+1})")


def f6_labels(p):
    for name, hl in (("H", HLIFT_MAIN), ("H'", HLIFT_CONTR)):
        S = span(hl, N, p)
        K3 = [v for v in S if not v[:8].any()]
        K2 = [v for v in S if not v[[0, 1, 2, 3, 4]].any()]           # image in G_2 meeting Z_2
        lab3 = [l for l in itertools.product(range(p), repeat=2) if all((l[0]*v[8] + l[1]*v[9]) % p == 0 for v in K3)]
        lab2 = [l for l in itertools.product(range(p), repeat=3)
                if all((l[0]*v[5] + l[1]*v[6] + l[2]*v[7]) % p == 0 for v in K2)]
        if name == "H":
            check("F6e", len(K3) == 1 and len(lab3) == p**2 and len(K2) == 1 and len(lab2) == p**3,
                  f"p={p} H: K_3 = 0, K_2 = 0: stage-3 labels range over F_p^2, stage-2 labels over F_p^3")
        else:
            ok = len(K3) == 1 and len(lab3) == p**2 and len(K2) == p and \
                set(lab2) == {(a, (-a) % p, b) for a in range(p) for b in range(p)}
            check("F6f", ok, f"p={p} H': K_3 = 0 (labels F_p^2); K_2 = F_p t^2(z+u), stage-2 labels in "
                             f"K_2^perp = {{lambda : lambda_z + lambda_u = 0}} (dim 2)")
    T = hand_cover_tensor()[:8, :8, :8]
    I = np.eye(8, dtype=np.int64)
    cent = all(not br(T, I[a], I[b], p).any() for a in (5, 6, 7) for b in range(8))
    nz = sorted((CNAMES[a], CNAMES[b], CNAMES[int(np.nonzero(T[a, b])[0][0])]) for a in range(8) for b in range(a+1, 8) if T[a, b].any())
    check("F6g", cent and nz == [("tx", "ty", "t2z"), ("tx", "tz", "t2u"), ("ty", "tz", "t2w")],
          f"p={p}: A^(2) = A/span(t3u,t3w) has brackets {nz}; Z_2 = span(t2z,t2u,t2w) central in A^(2) "
          f"(t2z is not central in A)")
    hp = [v for v in all_vectors(M, p) if (v @ np.array(V_MAIN)) % p == 0]
    check("F6h", len(hp) == p**4 and all((v[0] + v[2] + v[3]) % p == 0 for v in hp),
          f"p={p} H: grade-one samples are uniform on h^perp = {{y : y_x + y_z + y_u = 0}} (p^4 points); "
          f"the image of H in G/[G,G] is F_p x")


def main():
    f2_symbolic()
    for p in (5, 7):
        print(f"=== p = {p} ===", flush=True)
        T = f1(p)
        f2_numeric(T, p)
        f4_points(p, H_MAIN, HLIFT_MAIN, "H")
        f4_points(p, H_CONTR, HLIFT_CONTR, "H'")
        f6(p)
        f6_labels(p)
    p = 5
    print("=== p = 5: fibres, all-subalgebra checks, automorphisms ===", flush=True)
    T = cover_tensor() % p
    f3_fibres(T, p, H_MAIN, HLIFT_MAIN, "H")
    f3_fibres(T, p, H_CONTR, HLIFT_CONTR, "H'")
    subs = f4_remark(p)
    auts = f5_auts(p)
    f5_all_subalgebras(auts, subs, p)
    print("FAILURES:", FAILS if FAILS else "none")


if __name__ == "__main__":
    main()
