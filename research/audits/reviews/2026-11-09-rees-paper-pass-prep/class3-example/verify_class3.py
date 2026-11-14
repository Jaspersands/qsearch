"""Exact checks for the class-three worked example (filiform n4) of main-core.tex.

L = span(x1,x2,x3,x4), [x1,x2] = x3, [x1,x3] = x4, over F_p, p in {5, 7}.
Cover A basis (index: name = element of L[t]):
  0: X1 = t x1   1: X2 = t x2   2: X3 = t x3   3: X4 = t x4
  4: Y3 = t^2 x3 5: Y4 = t^2 x4 6: W4 = t^3 x4
Main hidden subgroup: h = F_p v, v = x1 + x2 + x3 + x4 ("H")
Contrast:             h = span(x4) = Z(L)              ("Z")

Every check prints a line starting with a tag [Cn] and PASS/FAIL; README.md
maps each claim of example.tex to these tags.  Usage:
  nice -n 19 /opt/anaconda3/bin/python verify_class3.py [--full7]
--full7 is accepted for compatibility; the fibre check is now full at both primes.
"""
import sys
import itertools
from math import gcd, log2, ceil
import numpy as np
import sympy as sp

FAILS = []


def check(tag, ok, msg):
    print(f"[{tag}] {'PASS' if ok else 'FAIL'}: {msg}", flush=True)
    if not ok:
        FAILS.append(tag)


# ------------------------------------------------------------------ algebra data
M = 4
L_BR = {(0, 1): (2, 1), (0, 2): (3, 1)}        # [x1,x2]=x3, [x1,x3]=x4


def L_tensor(p=None):
    T = np.zeros((M, M, M), dtype=np.int64)
    for (i, j), (k, v) in L_BR.items():
        T[i, j, k] = v
        T[j, i, k] = -v
    return T % p if p else T


GRADE = np.array([1, 1, 1, 1, 2, 2, 3])
LIDX = np.array([0, 1, 2, 3, 2, 3, 3])          # underlying L basis vector
NAMES = ["X1", "X2", "X3", "X4", "Y3", "Y4", "W4"]
N = 7
GAMMA = {1: [0, 1, 2, 3], 2: [2, 3], 3: [3]}   # gamma_k(L) spanned by these x's


def cover_tensor_from_L():
    """[t^i x, t^j y] = t^(i+j)[x,y], expressed in the cover basis; checks
    that [gamma_i, gamma_j] lies in gamma_(i+j) and that grades > 3 vanish."""
    TL = L_tensor()
    T = np.zeros((N, N, N), dtype=np.int64)
    pos = {(GRADE[a], LIDX[a]): a for a in range(N)}
    for a in range(N):
        for b in range(N):
            v = TL[LIDX[a], LIDX[b]]
            g = GRADE[a] + GRADE[b]
            if not v.any():
                continue
            assert g <= 3, "nonzero bracket above class"
            for k in np.nonzero(v)[0]:
                assert k in GAMMA[g], "bracket not in gamma_(i+j)"
                T[a, b, pos[(g, k)]] = v[k]
    return T


def hand_cover_tensor():
    T = np.zeros((N, N, N), dtype=np.int64)
    for (a, b, c) in [(0, 1, 4), (0, 2, 5), (0, 4, 6)]:   # [X1,X2]=Y3,[X1,X3]=Y4,[X1,Y3]=W4
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


def E(s, a, p):
    """E_s on cover coordinates (..., 7) -> L coordinates (..., 4)."""
    out = np.zeros(a.shape[:-1] + (M,), dtype=np.int64)
    for j in range(N):
        out[..., LIDX[j]] += pow(s, int(GRADE[j]), p) * a[..., j]
    return out % p


def dil(theta, a, p):
    sc = np.array([pow(theta, int(g), p) for g in GRADE])
    return (a * sc) % p


def enc(v, p):
    w = p ** np.arange(v.shape[-1])
    return (v * w).sum(-1)


def all_vectors(dim, p):
    return np.array(list(itertools.product(range(p), repeat=dim)), dtype=np.int64)[:, ::-1]


def span(basis, dim, p):
    basis = np.array(basis, dtype=np.int64).reshape(-1, dim)
    if len(basis) == 0:
        return np.zeros((1, dim), dtype=np.int64)
    coeffs = all_vectors(len(basis), p)
    return (coeffs @ basis) % p


def rank(rows, p):
    m = [list(map(int, r)) for r in rows]
    r = 0
    if not m:
        return 0
    ncol = len(m[0])
    for c in range(ncol):
        piv = next((i for i in range(r, len(m)) if m[i][c] % p), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], -1, p)
        m[r] = [x*inv % p for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] % p:
                f = m[i][c]
                m[i] = [(x - f*y) % p for x, y in zip(m[i], m[r])]
        r += 1
    return r


def in_span(basis, v, p):
    return rank(list(basis) + [v], p) == rank(list(basis), p)


# ------------------------------------------------------------------ H data
H_MAIN = [(1, 1, 1, 1)]                        # v = x1 + x2 + x3 + x4
H_CENT = [(0, 0, 0, 1)]                        # x4
HLIFT_MAIN = [(1, 1, 1, 1, 0, 0, 0)]           # t v = X1 + X2 + X3 + X4
HLIFT_CENT = [(0, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 0, 1)]  # X4, Y4, W4
U_TWO = (0, 0, 0, 2, 0, -3, 1)                 # 2 X4 - 3 Y4 + W4


def hlift_from_definition(h, p):
    """sum_k t^k (h cap gamma_k) by brute force over h's elements."""
    elems = span(h, M, p)
    rows = []
    for k in (1, 2, 3):
        inter = [v for v in elems if all(v[i] == 0 for i in range(M) if i not in GAMMA[k])]
        for v in inter:
            row = [0]*N
            for j in range(N):
                if GRADE[j] == k:
                    row[j] = int(v[LIDX[j]])
            rows.append(row)
    return rows


# ------------------------------------------------------------------ C1 cover structure
def c1_cover(p):
    T = cover_tensor_from_L() % p
    check("C1a", np.array_equal(T, hand_cover_tensor() % p),
          f"p={p}: cover brackets of L[t] restricted to A are exactly [X1,X2]=Y3, [X1,X3]=Y4, [X1,Y3]=W4")
    I = np.eye(N, dtype=np.int64)
    jac = all(not ((br(T, I[a], br(T, I[b], I[c], p), p) + br(T, I[b], br(T, I[c], I[a], p), p)
                    + br(T, I[c], br(T, I[a], I[b], p), p)) % p).any()
              for a in range(N) for b in range(N) for c in range(N))
    check("C1b", jac, f"p={p}: Jacobi identity on all basis triples of A")
    TL = L_tensor(p)
    J = np.eye(M, dtype=np.int64)
    jacL = all(not ((br(TL, J[a], br(TL, J[b], J[c], p), p) + br(TL, J[b], br(TL, J[c], J[a], p), p)
                     + br(TL, J[c], br(TL, J[a], J[b], p), p)) % p).any()
               for a in range(M) for b in range(M) for c in range(M))
    check("C1c", jacL, f"p={p}: Jacobi identity on L")
    # class 3, centre of A, centre of L
    allA = all_vectors(N, p)
    cent = [v for v in allA if all(not br(T, v, I[b], p).any() for b in range(N))]
    check("C1d", len(cent) == p**3 and all(v[:3].sum() == 0 and v[4] == 0 for v in cent),
          f"p={p}: Z(A) = span(X4, Y4, W4) ({len(cent)} elements)")
    allL = all_vectors(M, p)
    centL = [v for v in allL if all(not br(TL, v, J[b], p).any() for b in range(M))]
    check("C1e", len(centL) == p and all(v[:3].sum() == 0 for v in centL),
          f"p={p}: Z(L) = F_p x4 = gamma_3(L)")
    trip = br(T, br(T, I[0], I[1], p), I[0], p)
    check("C1f", trip.any(), f"p={p}: [[X1,X2],X1] = {trip.tolist()} != 0, so A has class 3")
    # E_s is a Lie homomorphism, delta_theta an automorphism, E_s o delta = E_{theta s}
    okE = all(np.array_equal(E(s, br(T, I[a], I[b], p), p), br(TL, E(s, I[a], p), E(s, I[b], p), p))
              for s in range(p) for a in range(N) for b in range(N))
    okD = all(np.array_equal(dil(th, br(T, I[a], I[b], p), p), br(T, dil(th, I[a], p), dil(th, I[b], p), p))
              for th in range(1, p) for a in range(N) for b in range(N))
    okC = all(np.array_equal(E(s, dil(th, I[a], p), p), E(th*s % p, I[a], p))
              for s in range(p) for th in range(1, p) for a in range(N))
    check("C1g", okE and okD and okC,
          f"p={p}: E_s Lie hom (all s), delta_theta Lie aut, E_s o delta_theta = E_(theta s)")
    return T


# ------------------------------------------------------------------ C2 BCH homomorphism
def c2_symbolic():
    """Exact over Q(s, theta, a_i, b_i): E_s(a*b) = E_s(a)*E_s(b), delta(a*b) = delta(a)*delta(b),
    and associativity of the truncated BCH product on A; denominators are 2 and 12 only."""
    s, th = sp.symbols('s theta')
    a = sp.symbols('a0:7')
    b = sp.symbols('b0:7')
    cc = sp.symbols('c0:7')
    TA = hand_cover_tensor()
    TL = L_tensor()

    def sbr(T, x, y, n):
        return [sp.expand(sum(T[i, j, k]*x[i]*y[j] for i in range(n) for j in range(n) if T[i, j, k]))
                for k in range(n)]

    def sbch(T, x, y, n):
        xy = sbr(T, x, y, n)
        t1 = sbr(T, x, xy, n)
        t2 = sbr(T, y, sbr(T, y, x, n), n)
        return [sp.expand(x[k] + y[k] + sp.Rational(1, 2)*xy[k] + sp.Rational(1, 12)*(t1[k] + t2[k]))
                for k in range(n)]

    def sE(x):
        out = [0]*M
        for j in range(N):
            out[LIDX[j]] += s**int(GRADE[j])*x[j]
        return [sp.expand(o) for o in out]

    def sD(x):
        return [sp.expand(th**int(GRADE[j])*x[j]) for j in range(N)]

    lhs = sE(sbch(TA, a, b, N))
    rhs = sbch(TL, sE(a), sE(b), M)
    okE = all(sp.expand(l - r) == 0 for l, r in zip(lhs, rhs))
    lhs = sD(sbch(TA, a, b, N))
    rhs = sbch(TA, sD(a), sD(b), N)
    okD = all(sp.expand(l - r) == 0 for l, r in zip(lhs, rhs))
    assoc = all(sp.expand(l - r) == 0 for l, r in
                zip(sbch(TA, sbch(TA, a, b, N), cc, N), sbch(TA, a, sbch(TA, b, cc, N), N)))
    inv = all(sp.expand(v) == 0 for v in sbch(TA, a, [-x for x in a], N))
    check("C2a", okE, "symbolic over Q: E_s(a*b) = E_s(a)*E_s(b) for generic a, b in A, generic s (class-3 BCH)")
    check("C2b", okD, "symbolic over Q: delta_theta(a*b) = delta_theta(a)*delta_theta(b)")
    check("C2c", assoc and inv, "symbolic over Q: BCH_3 on A is associative and a*(-a) = 0")
    prod = sbch(TA, a, b, N)
    print("      a*b on A =", [str(x) for x in prod])
    return okE and okD


def c2_numeric(T, p, trials=20000, seed=1):
    rng = np.random.default_rng(seed + p)
    a = rng.integers(0, p, (trials, N))
    b = rng.integers(0, p, (trials, N))
    TL = L_tensor(p)
    ok = all(np.array_equal(E(s, bch(T, a, b, p), p), bch(TL, E(s, a, p), E(s, b, p), p)) for s in range(p))
    okd = all(np.array_equal(dil(th, bch(T, a, b, p), p), bch(T, dil(th, a, p), dil(th, b, p), p))
              for th in range(1, p))
    check("C2d", ok and okd, f"p={p}: {trials} random pairs, E_s and delta_theta respect BCH mod p, all s, theta")


# ------------------------------------------------------------------ C3 tuple oracle fibres
def left_coset_labels(TL, h, p):
    G = all_vectors(M, p)
    Hel = span(h, M, p)
    lab = np.full(len(G), p**M)
    for u in Hel:
        lab = np.minimum(lab, enc(bch(TL, G, np.broadcast_to(u, G.shape), p), p))
    table = np.zeros(p**M, dtype=np.int64)
    table[enc(G, p)] = lab
    return table


def c3_fibres(T, p, h, hlift, name, full=True, chunk=40000):
    TL = L_tensor(p)
    # h is a Lie subalgebra, the hlift of the definition equals the stated one
    hel = span(h, M, p)
    closed = all(in_span(h, br(TL, x, y, p), p) for x in np.array(h) for y in np.array(h))
    check("C3a", closed, f"p={p} {name}: h is a Lie subalgebra")
    hl_def = hlift_from_definition(h, p)
    same = rank(hl_def, p) == len(hlift) and all(in_span(hl_def, v, p) for v in hlift)
    check("C3b", same, f"p={p} {name}: sum_k t^k (h cap gamma_k) = span{[list(v) for v in hlift]}")
    f = left_coset_labels(TL, h, p)
    # f hides H: f(x) = f(y) iff x^{-1} * y in h
    G = all_vectors(M, p)
    rng = np.random.default_rng(7)
    idx = rng.integers(0, len(G), (20000, 2))
    x, y = G[idx[:, 0]], G[idx[:, 1]]
    q = bch(TL, (-x) % p, y, p)
    inh = np.array([in_span(h, v, p) for v in q])
    check("C3c", np.array_equal(f[enc(x, p)] == f[enc(y, p)], inh),
          f"p={p} {name}: f hides H (20000 random pairs)")
    if not full:
        # identity fibre exactly, over all of A
        A = all_vectors(N, p)
        ok = np.ones(len(A), dtype=bool)
        for s in (1, 2, 3):
            ok &= f[enc(E(s, A, p), p)] == f[0]
        fib = A[ok]
        hl = set(enc(span(hlift, N, p), p).tolist())
        check("C3d", set(enc(fib, p).tolist()) == hl,
              f"p={p} {name}: fibre of hat f over 0 is exactly exp(hlift) ({len(fib)} = p^{len(hlift)} points of {len(A)})")
        return
    A = all_vectors(N, p)
    hat = np.zeros(len(A), dtype=np.int64)
    for s in (1, 2, 3):
        hat = hat * (p**M) + f[enc(E(s, A, p), p)]
    hl = span(hlift, N, p)
    rep = np.full(len(A), p**N, dtype=np.int64)
    for st in range(0, len(A), chunk):
        a = A[st:st+chunk]
        r = rep[st:st+chunk]
        for u in hl:
            r = np.minimum(r, enc(bch(T, a, np.broadcast_to(u, a.shape), p), p))
        rep[st:st+chunk] = r
    pairs = len(set(zip(hat.tolist(), rep.tolist())))
    nh, nr = len(set(hat.tolist())), len(set(rep.tolist()))
    check("C3d", pairs == nh == nr == p**(N - len(hlift)),
          f"p={p} {name}: over all {len(A)} points of A, the fibres of hat f = (f E_1, f E_2, f E_3) are "
          f"exactly the left cosets a*exp(hlift): {nh} fibres = {nr} cosets of size p^{len(hlift)}")
    # also: two evaluations do not suffice (main H only): fibres of (f E_1, f E_2)
    hat2 = f[enc(E(1, A, p), p)] * (p**M) + f[enc(E(2, A, p), p)]
    sizes = np.unique(hat2, return_counts=True)[1]
    print(f"      p={p} {name}: two-point oracle (f E_1, f E_2) has {len(sizes)} fibres of size(s) {sorted(set(sizes.tolist()))}")
    return hat2


# ------------------------------------------------------------------ C4 two-point failure
def c4_two_points(T, p, h, hlift, name):
    A = all_vectors(N, p)

    def pull(points):
        ok = np.ones(len(A), dtype=bool)
        for s in points:
            v = E(s, A, p)
            ok &= member(v)
        return A[ok]

    hel = set(enc(span(h, M, p), p).tolist())
    lut = np.zeros(p**M, dtype=bool)
    lut[list(hel)] = True

    def member(v):
        return lut[enc(v, p)]

    P12 = pull((1, 2))
    P123 = pull((1, 2, 3))
    P1 = pull((1,))
    keyHL = set(enc(span(hlift, N, p), p).tolist())
    check("C4a", set(enc(P123, p).tolist()) == keyHL,
          f"p={p} {name}: E_1^-1(h) cap E_2^-1(h) cap E_3^-1(h) = hlift ({len(P123)} points)")
    allth = set(enc(pull(range(1, p)), p).tolist()) == keyHL
    check("C4b", allth, f"p={p} {name}: hlift = intersection of E_s^-1(h) over all s in F_p^x")
    u = np.array(U_TWO) % p
    if name == "H":
        Pu = set(enc((span(list(hlift) + [tuple(u)], N, p)), p).tolist())
        check("C4c", set(enc(P12, p).tolist()) == Pu and len(P12) == p**(len(hlift)+1),
              f"p={p} H: two-point pullback E_1^-1(h) cap E_2^-1(h) = hlift + F_p u, u = 2X4-3Y4+W4 "
              f"({len(P12)} = p^{len(hlift)+1} points)")
        ev = {s: E(s, u, p).tolist() for s in (1, 2, 3)}
        check("C4d", ev[1] == [0]*4 and ev[2] == [0]*4 and ev[3] == [0, 0, 0, 6 % p],
              f"p={p} H: E_1(u) = {ev[1]}, E_2(u) = {ev[2]}, E_3(u) = {ev[3]} = 6 x4 (not in h)")
        bad = []
        for th in range(1, p):
            du = dil(th, u, p)
            e1 = E(1, du, p)
            expect = (th*(th-1)*(th-2)) % p
            assert e1.tolist() == [0, 0, 0, expect]
            if expect:
                bad.append(th)
        check("C4e", bad == [t for t in range(1, p) if t not in (1, 2)],
              f"p={p} H: E_1(delta_theta u) = theta(theta-1)(theta-2) x4, not in h for theta in {bad}")
    keyP12 = set(enc(P12, p).tolist())
    keyP1 = set(enc(P1, p).tolist())
    pres12 = [th for th in range(1, p) if set(enc(dil(th, P12, p), p).tolist()) == keyP12]
    pres1 = [th for th in range(1, p) if set(enc(dil(th, P1, p), p).tolist()) == keyP1]
    presHL = [th for th in range(1, p) if set(enc(dil(th, span(hlift, N, p), p), p).tolist()) == keyHL]
    if name == "H":
        check("C4f", pres12 == [1] and pres1 == [1] and presHL == list(range(1, p)),
              f"p={p} H: dilations preserving E_1^-1(h): {pres1}; preserving the two-point pullback: {pres12}; "
              f"preserving hlift: {presHL}")
    else:
        check("C4g", set(enc(P12, p).tolist()) == keyHL and pres12 == list(range(1, p)) and pres1 == [1],
              f"p={p} Z: two-point pullback already equals hlift (x4 in h); every dilation preserves it; "
              f"single point preserved by {pres1}")


# ------------------------------------------------------------------ C5 automorphisms
def automorphisms(p):
    """All Lie automorphisms of L, by exhausting the images P1, P2 of the generators x1, x2."""
    TL = L_tensor(p)
    V = all_vectors(M, p)
    out = []
    for v1 in V:
        P2 = V
        P1 = np.broadcast_to(v1, V.shape)
        P3 = br(TL, P1, P2, p)
        P4 = br(TL, P1, P3, p)
        ok = ~br(TL, P1, P4, p).any(1) & ~br(TL, P2, P3, p).any(1) & ~br(TL, P2, P4, p).any(1) \
            & ~br(TL, P3, P4, p).any(1)
        mats = np.stack([P1, P2, P3, P4], axis=1)[ok]       # row i = image of x_(i+1)
        det = np.round(np.linalg.det(mats.astype(float))).astype(np.int64) % p
        out.append(mats[det != 0])
    return np.concatenate(out)


def plucker_key(B, p):
    """Canonical key of the row space of B (..., k, 4): normalized Pluecker coordinates."""
    k = B.shape[-2]
    cols = list(itertools.combinations(range(M), k))
    minors = np.stack([np.round(np.linalg.det(B[..., :, list(c)].astype(float))).astype(np.int64) % p
                       for c in cols], axis=-1) if k else np.zeros(B.shape[:-2] + (1,), dtype=np.int64)
    first = np.argmax(minors != 0, axis=-1)
    lead = np.take_along_axis(minors, first[..., None], axis=-1)[..., 0]
    inv = np.array([0] + [pow(int(x), -1, p) for x in range(1, p)])[lead]
    return enc((minors * inv[..., None]) % p, p)


def subalgebras(p):
    TL = L_tensor(p)
    out = []
    V = all_vectors(M, p)
    # enumerate subspaces by RREF: choose pivots, fill free entries
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


def central_scalars(auts, B, p):
    k = len(B)
    if k == 0:
        stab = auts
    else:
        img = (B[None, :, :] @ auts) % p                 # rows of B mapped: v -> v @ mats
        stab = auts[plucker_key(img, p) == plucker_key(B[None], p)[0]]
    return stab, sorted(set((stab[:, 3, 3] % p).tolist()))


def c5_auts(p, full_subalgebra_scan):
    auts = automorphisms(p)
    check("C5a", len(auts) == (p-1)**2 * p**5,
          f"p={p}: |Aut(L)| = {len(auts)} = (p-1)^2 p^5, by exhausting the images of x1, x2")
    a = auts[:, 0, 0]
    b = auts[:, 1, 1]
    form = (auts[:, 1, 0] == 0).all() and (auts[:, 2, :2] == 0).all() and (auts[:, 3, :3] == 0).all()
    check("C5b", form and np.array_equal(auts[:, 3, 3] % p, (a*a*b) % p) and np.array_equal(auts[:, 2, 2] % p, a*b % p),
          f"p={p}: every automorphism has phi(x2) in span(x2,x3,x4) and acts on Z = F_p x4 by a^2 b "
          f"(a = x1-coeff of phi(x1), b = x2-coeff of phi(x2))")
    check("C5b2", sorted(set((auts[:, 3, 3] % p).tolist())) == list(range(1, p)),
          f"p={p}: Aut(L) acts on the centre by every scalar in F_p^x (L is graded)")
    out = {}
    for name, h in (("H", H_MAIN), ("Z", H_CENT)):
        B = np.array(h, dtype=np.int64)
        stab, sc = central_scalars(auts, B, p)
        out[name] = (len(stab), sc)
        print(f"      p={p} {name}: |Stab_Aut(L)(h)| = {len(stab)}, central scalars of the stabilizer = {sc}")
    check("C5c", out["H"][1] == list(range(1, p)),
          f"p={p} H: automorphisms preserving h act on the centre by every scalar in F_p^x (|Stab| = {out['H'][0]})")
    # no element of the 2-torus diag(a,b,ab,a^2b) except the identity preserves h
    Bm = np.array(H_MAIN, dtype=np.int64)
    key = plucker_key(Bm[None], p)[0]
    torus_ok = []
    for aa in range(1, p):
        for bb in range(1, p):
            D = np.diag([aa, bb, aa*bb % p, aa*aa*bb % p])
            if plucker_key(((Bm @ D) % p)[None], p)[0] == key:
                torus_ok.append((aa, bb, aa*aa*bb % p))
    check("C5d", torus_ok == [(1, 1, 1)],
          f"p={p} H: torus elements diag(a,b,ab,a^2b) preserving h: {torus_ok}; in particular the standard "
          f"dilations (a=b=theta) and tau_b = diag(1,b,b,b) preserve h only when trivial")
    # explicit conjugator phi: x1 -> v, x2, x3, x4 fixed; psi_theta = phi delta_theta phi^-1
    phi = np.array([[1, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.int64)
    autset = set(map(lambda A_: A_.tobytes(), auts[(auts[:, 0, 0] == 1) & (auts[:, 1, 1] == 1)]))
    isaut = (phi % p).tobytes() in autset
    B0 = np.array([[1, 0, 0, 0]], dtype=np.int64)
    maps = plucker_key(((B0 @ phi) % p)[None], p)[0] == key
    phinv = np.round(np.linalg.inv(phi.astype(float))).astype(np.int64) % p
    conj_ok = []
    for th in range(1, p):
        D = np.diag([th, th, th*th % p, pow(th, 3, p)])
        C = (phinv @ D @ phi) % p           # row convention: v -> v phi^-1 D phi, i.e. phi o delta o phi^-1
        formula = np.array([[th, 0, (th - th*th) % p, (th - th**3) % p], [0, th, 0, 0],
                            [0, 0, th*th % p, 0], [0, 0, 0, pow(th, 3, p)]], dtype=np.int64)
        conj_ok.append(np.array_equal(C, formula) and C.tobytes() in set(map(lambda A_: A_.tobytes(), auts[auts[:, 0, 0] == th]))
                       and plucker_key(((Bm @ C) % p)[None], p)[0] == key)
    check("C5e", isaut and maps and all(conj_ok),
          f"p={p} H: phi = (x1 -> x1+x2+x3+x4) is an automorphism with phi(F_p x1) = h, and psi_theta = "
          f"phi delta_theta phi^-1 = (x1 -> theta x1 + (theta-theta^2) x3 + (theta-theta^3) x4, "
          f"x_k -> theta^k' x_k) is an automorphism preserving h that scales x4 by theta^3, every theta")
    # the scalars need the derived coordinates of v: automorphisms preserving EVERY line
    # F_p(x1 + x2 + alpha x3 + beta x4) act trivially on the centre
    keep = np.ones(len(auts), dtype=bool)
    for al in range(p):
        for be in range(p):
            B = np.array([[1, 1, al, be]], dtype=np.int64)
            keep &= plucker_key((B[None, :, :] @ auts) % p, p) == plucker_key(B[None], p)[0]
    sc = sorted(set((auts[keep][:, 3, 3] % p).tolist()))
    check("C5h", sc == [1],
          f"p={p}: the {int(keep.sum())} automorphisms preserving all p^2 lines F_p(x1+x2+alpha x3+beta x4) "
          f"act on the centre only by {sc}; so a scalar != 1 needs the derived coordinates (v3, v4) of H")
    # the subalgebras inside V = span(x2,x3,x4) are all preserved by tau_b = diag(1,b,b,b)
    allset = set(map(lambda A_: A_.tobytes(), auts))
    tau_ok = all((np.diag([1, b, b, b]).astype(np.int64) % p).tobytes() in allset for b in range(1, p))
    check("C5i", tau_ok, f"p={p}: tau_b = diag(1,b,b,b) is an automorphism (it scales the abelian ideal "
                         f"span(x2,x3,x4) and so preserves every subalgebra inside it, with central scalar b)")
    if full_subalgebra_scan:
        subs = subalgebras(p)
        bad = []
        for B in subs:
            _, sc = central_scalars(auts, B, p)
            if sc != list(range(1, p)):
                bad.append((B.tolist(), sc))
        check("C5f", not bad,
              f"p={p}: for EVERY one of the {len(subs)} Lie subalgebras h of L, Stab_Aut(L)(h) acts on the "
              f"centre by all of F_p^x (exceptions: {bad[:3]})")
    else:
        subs = subalgebras(p)
        # orbit argument: union of Aut-orbits of torus-stable (coordinate) subalgebras covers all
        allkeys = {}
        for B in subs:
            allkeys.setdefault(len(B), set()).add(int(plucker_key(B[None], p)[0]))
        coord = [B for B in subs if all(((B != 0).sum(1)) == 1)]
        cover = {}
        for B in coord:
            img = (B[None, :, :] @ auts) % p
            cover.setdefault(len(B), set()).update(plucker_key(img, p).tolist())
        ok = all(allkeys[k] <= cover.get(k, set()) for k in allkeys)
        check("C5f", ok,
              f"p={p}: every one of the {len(subs)} Lie subalgebras is Aut(L)-conjugate to one of the "
              f"{len(coord)} coordinate subalgebras, which the 2-torus diag(a,b,ab,a^2b) preserves; hence "
              f"every Stab_Aut(L)(h) acts on the centre by all of F_p^x")
    # no nontrivial automorphism preserves every line: the automorphisms fixing all 1-dim subalgebras
    lines = [B for B in subs if len(B) == 1]
    keep = np.ones(len(auts), dtype=bool)
    for B in lines:
        img = (B[None, :, :] @ auts) % p
        keep &= plucker_key(img, p) == plucker_key(B[None], p)[0]
    check("C5g", keep.sum() == 1,
          f"p={p}: only the identity automorphism preserves every line of L (so no nontrivial automorphism "
          f"is H-independent)")


# ------------------------------------------------------------------ C6 stages, labels, arities
def G_(d, a):
    return d**(d*(d-1)//2) * (a+1)**d


def B_(d, a):
    return G_(d, a) ** ceil(log2(d+1))


def min_arity(d, g, p, Mmax=6):
    """Smallest M such that EVERY tuple of M labels in F_p^g admits a nonzero s with
    sum s_i^d lambda_i = 0 (exhaustive over all label tuples)."""
    W = sorted(set(pow(x, d, p) for x in range(p)))       # values of s^d (incl. 0)
    labels = all_vectors(g, p)
    for Mm in range(1, Mmax+1):
        ws = np.array([w for w in itertools.product(W, repeat=Mm) if any(w)], dtype=np.int64)
        ok = True
        for tup in itertools.product(range(len(labels)), repeat=Mm):
            lam = labels[list(tup)]                    # Mm x g
            if not (((ws @ lam) % p) == 0).all(1).any():
                ok = False
                break
        if ok:
            return Mm
    return None


def c6_stages(p):
    k3, k2 = gcd(3, p-1), gcd(2, p-1)
    check("C6a", B_(3, 1) == 46656 and B_(2, 2) == 324 and B_(2, 1) == 64,
          f"B_3(1) = G(3,1)^2 = {G_(3,1)}^2 = {B_(3,1)}, B_2(2) = G(2,2)^2 = {G_(2,2)}^2 = {B_(2,2)}")
    for tau in (1,):
        Q = 3*(4+tau)*B_(2, 2)*B_(3, 1)
        check("C6b", abs(log2(Q) - 27.76) < 0.005,
              f"Q_q = 3(4+1) B_2(2) B_3(1) = {Q}, log2 = {log2(Q):.4f} (Table 1 filiform row: 27.76)")
    m3 = min_arity(3, 1, p)
    m2line = min_arity(2, 1, p)
    print(f"      p={p}: kappa_3 = {k3}, kappa_2 = {k2}; Chevalley-Warning arities kappa*g+1: "
          f"stage 3: {k3*1+1}, stage 2: {k2*2+1}")
    check("C6c", m3 == (2 if k3 == 1 else 3) and m2line == 3,
          f"p={p}: exact minimum arity, every label tuple: stage 3 (degree 3, one equation): {m3}; "
          f"degree 2, one equation (labels on the line K_2^perp): {m2line}")
    # degree 2, two equations: 5 always suffices (CW), 4 does not: explicit counterexamples
    if p % 4 == 1:
        nsq = next(x for x in range(2, p) if pow(x, (p-1)//2, p) == p-1)
        # s1^2 - n s2^2 = 0 has only the trivial solution for n a nonsquare
        ce = [(1, 0), ((-nsq) % p, 0), (0, 1), (0, (-nsq) % p)]
    else:
        ce = [(1, 0), (1, 0), (0, 1), (0, 1)]
    lam = np.array(ce, dtype=np.int64)
    sols = [s for s in itertools.product(range(p), repeat=4) if any(s)
            and not ((np.array([x*x % p for x in s]) @ lam) % p).any()]
    check("C6d", not sols, f"p={p}: the 4 labels {ce} in F_p^2 admit no nonzero solution of the degree-2 "
          f"system, so 4 < 5 = kappa_2 g_2 + 1 columns can fail for arbitrary labels")
    if k3 == 3:
        sols = [s for s in itertools.product(range(p), repeat=2) if any(s)
                and (pow(s[0], 3, p) + 2*pow(s[1], 3, p)) % p == 0]
        check("C6e", not sols, f"p={p}: labels (1, 2) at stage 3: s1^3 + 2 s2^3 = 0 has no nonzero solution")
    # Lemma bezout conversion at p=5, d=3: kappa = 1, u with 3u = 1 mod (p-1)
    if k3 == 1:
        u = next(u for u in range(1, p) if (3*u) % (p-1) == 1)
        ok = all(pow(pow(x, u, p), 3, p) == x for x in range(1, p))
        check("C6f", ok, f"p={p}: Lemma bezout at d=3: kappa=1, s_i = x_i^{u}, s_i^3 = x_i for x_i != 0")


def c6_labels(T, p):
    """Label laws at stages 3 and 2 for both H, via Lemma central: uniform on K_d^perp.
    Computed directly: trace of rho_H Pi_lambda over the cover, using f-hat."""
    for name, h, hlift in (("H", H_MAIN, HLIFT_MAIN), ("Z", H_CENT, HLIFT_CENT)):
        hl = span(hlift, N, p)
        K3 = [v for v in hl if not v[:6].any()]
        K2 = [v for v in hl if not v[[0, 1, 2, 3, 6]].any()]
        lab3 = [l for l in range(p) if all((l*v[6]) % p == 0 for v in K3)]
        lab2 = [l for l in itertools.product(range(p), repeat=2)
                if all((l[0]*v[4] + l[1]*v[5]) % p == 0 for v in K2)]
        if name == "H":
            check("C6g", len(K3) == 1 and len(lab3) == p and len(K2) == 1 and len(lab2) == p*p,
                  f"p={p} H: K_3 = 0 and K_2 = 0, so stage-3 labels range over F_p and stage-2 labels over "
                  f"all of F_p^2 (a_3 = 1, a_2 = 2)")
        else:
            check("C6h", len(K3) == p and lab3 == [0] and len(K2) == p
                  and set(lab2) == {(m, 0) for m in range(p)},
                  f"p={p} Z: K_3 = F_p W4, every stage-3 label is 0; K_2 = F_p Y4, stage-2 labels in F_p(1,0)")
    # A^(2) structure: Z_2 = span(Y3,Y4) central in the quotient by W4
    T2 = T[:6, :6, :6]
    I = np.eye(6, dtype=np.int64)
    cent = all(not br(T2, I[a], I[b], p).any() for a in (4, 5) for b in range(6))
    nz = sorted({(NAMES[a], NAMES[b], NAMES[int(np.nonzero(T2[a, b])[0][0])]) for a in range(6) for b in range(6)
                 if a < b and T2[a, b].any()})
    check("C6i", cent and nz == [("X1", "X2", "Y3"), ("X1", "X3", "Y4")],
          f"p={p}: A^(2) = A/F_p W4 has brackets {nz}; Z_2 = span(Y3,Y4) is central; X4 is central of grade one")
    # grade one: h^perp
    hp = [v for v in all_vectors(M, p) if all((v @ np.array(b)) % p == 0 for b in H_MAIN)]
    expect = set(enc(span([(1, p-1, 0, 0), (0, 1, p-1, 0), (0, 0, 1, p-1)], M, p), p).tolist())
    check("C6j", set(enc(np.array(hp), p).tolist()) == expect and len(hp) == p**3,
          f"p={p} H: Fourier samples on G_1 = tL are uniform on h^perp = {{y : y1+y2+y3+y4 = 0}} (p^3 points); "
          f"the image of h in L/gamma_2 is only F_p(x1+x2)")


def main():
    full7 = "--full7" in sys.argv
    c2_symbolic()
    for p in (5, 7):
        print(f"=== p = {p} ===", flush=True)
        T = c1_cover(p)
        c2_numeric(T, p)
        full = True
        c3_fibres(T, p, H_MAIN, HLIFT_MAIN, "H", full=full)
        c3_fibres(T, p, H_CENT, HLIFT_CENT, "Z", full=full)
        c4_two_points(T, p, H_MAIN, HLIFT_MAIN, "H")
        c4_two_points(T, p, H_CENT, HLIFT_CENT, "Z")
        c5_auts(p, full_subalgebra_scan=(p == 5))
        c6_stages(p)
        c6_labels(T, p)
    print("FAILURES:", FAILS if FAILS else "none")


if __name__ == "__main__":
    main()
