# Independent referee brute force for lem:tb-howell-rounds (proposal 2026-11-04-rees-normal-form).
# Written from the lemma text only; shares no code with howell_check.py.
import itertools, random, sys

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
rng = random.Random(SEED)

class Zpe:
    def __init__(self, p, e):
        self.p, self.e, self.M = p, e, p ** e
    def v(self, x):
        x %= self.M
        if x == 0: return self.e
        k = 0
        while x % self.p == 0: x //= self.p; k += 1
        return k
    def unitinv(self, x, k):
        return pow((x % self.M) // self.p ** k, -1, self.M)

STATS = {"maxrem_ratio": 0.0, "p3": 0, "p3_variants": 0, "smith": 0, "rounds": 0, "rtf": 0,
         "rtf_bad": 0, "n6": 0, "n2": 0}

# ---------- Step 2 construction, randomized (tie-breaks, lifts), then randomized post-processing
def howell(Z, gens, n, randomize=True, post=True):
    M, p, e = Z.M, Z.p, Z.e
    rem = [[x % M for x in g] for g in gens]
    rem = [r for r in rem if any(r)]
    q0 = len(rem)
    out = []  # (pos, a, row)
    for j in range(n):
        if q0: STATS["maxrem_ratio"] = max(STATS["maxrem_ratio"], len(rem) / q0)
        assert len(rem) <= max(q0, 0) or q0 == 0, "remaining set exceeds q0"
        vals = [Z.v(r[j]) for r in rem]
        cand = [i for i, a in enumerate(vals) if a < e]
        if not cand: continue
        amin = min(vals[i] for i in cand)
        ties = [i for i in cand if vals[i] == amin]
        idx = rng.choice(ties) if randomize else ties[0]
        piv = rem.pop(idx)
        u = Z.unitinv(piv[j], amin)
        piv = [(x * u) % M for x in piv]
        assert piv[j] == p ** amin
        new = []
        for r in rem:
            assert r[j] % p ** amin == 0
            f = r[j] // p ** amin
            if randomize: f += rng.randrange(p ** amin) * p ** (e - amin)  # arbitrary lift
            r = [(x - f * y) % M for x, y in zip(r, piv)]
            if any(r): new.append(r)
        app = [(p ** (e - amin) * x) % M for x in piv]
        if any(app): new.append(app)
        rem = new
        out.append([j, amin, piv])
    assert not rem
    if post:
        # add random multiples of later rows to earlier rows: keeps (HF1), (HF2) and the span
        for t in range(len(out)):
            for s in range(t + 1, len(out)):
                if rng.random() < 0.5:
                    c = rng.randrange(M)
                    out[t][2] = [(x + c * y) % M for x, y in zip(out[t][2], out[s][2])]
    return [tuple(o) for o in out]

def member(Z, v, H, n):
    """Membership scan of Step 2 with multipliers recorded (P2)."""
    M, p = Z.M, Z.p
    v = [x % M for x in v]
    lam = [0] * len(H)
    pos = {h[0]: t for t, h in enumerate(H)}
    for j in range(n):
        if v[j] == 0: continue
        if j not in pos: return None
        t = pos[j]; _, a, r = H[t]
        if v[j] % p ** a: return None
        f = v[j] // p ** a
        lam[t] = (lam[t] + f) % M
        v = [(x - f * y) % M for x, y in zip(v, r)]
    return lam if not any(v) else None

def span_bf(Z, rows, n):
    M = Z.M
    S = {tuple([0] * n)}
    frontier = list(S)
    rows = [tuple(x % M for x in r) for r in rows]
    while frontier:
        nf = []
        for x in frontier:
            for g in rows:
                y = tuple((a + b) % M for a, b in zip(x, g))
                if y not in S: S.add(y); nf.append(y)
        frontier = nf
    return S

def check_howell_axioms(Z, H, n):
    M, p, e = Z.M, Z.p, Z.e
    for t, (j, a, r) in enumerate(H):
        assert all(r[i] == 0 for i in range(j)) and r[j] == p ** a and a < e
        if t: assert H[t - 1][0] < j
        later = span_bf(Z, [h[2] for h in H[t + 1:]], n)
        assert tuple((p ** (e - a) * x) % M for x in r) in later, "HF2"

def left_kernel(Z, A, n):
    a = len(A)
    rows = [list(A[i]) + [1 if s == i else 0 for s in range(a)] for i in range(a)]
    H = howell(Z, rows, n + a)
    out = []
    for (j, aa, r) in H:
        if j >= n:
            assert not any(r[:n]), "row with pivot beyond n not of form (0|lam)"
            out.append(r[n:])
    return out, H

def smith(Z, C, ncols):
    """Step 4 on an a x n matrix; returns exps (len ncols), Q, Qinv, and P for the check."""
    M, p, e = Z.M, Z.p, Z.e
    C = [[x % M for x in r] for r in C]
    a = len(C)
    P = [[int(i == j) for j in range(a)] for i in range(a)]
    Q = [[int(i == j) for j in range(ncols)] for i in range(ncols)]
    Qi = [[int(i == j) for j in range(ncols)] for i in range(ncols)]
    exps = []
    for t in range(min(a, ncols)):
        best = None
        for i in range(t, a):
            for j in range(t, ncols):
                vv = Z.v(C[i][j])
                if vv < e and (best is None or vv < best[0]): best = (vv, i, j)
        if best is None: break
        at, i, j = best
        C[t], C[i] = C[i], C[t]; P[t], P[i] = P[i], P[t]
        for r in C: r[t], r[j] = r[j], r[t]
        for r in Q: r[t], r[j] = r[j], r[t]
        Qi[t], Qi[j] = Qi[j], Qi[t]
        u = Z.unitinv(C[t][t], at)
        C[t] = [(x * u) % M for x in C[t]]; P[t] = [(x * u) % M for x in P[t]]
        for i2 in range(a):
            if i2 != t and C[i2][t]:
                f = C[i2][t] // p ** at
                C[i2] = [(x - f * y) % M for x, y in zip(C[i2], C[t])]
                P[i2] = [(x - f * y) % M for x, y in zip(P[i2], P[t])]
        for j2 in range(ncols):
            if j2 != t and C[t][j2]:
                f = C[t][j2] // p ** at
                for r in C: r[j2] = (r[j2] - f * r[t]) % M
                for r in Q: r[j2] = (r[j2] - f * r[t]) % M
                Qi[t] = [(x + f * y) % M for x, y in zip(Qi[t], Qi[j2])]
        exps.append(at)
    exps += [e] * (ncols - len(exps))
    return exps, Q, Qi, P

def matmul(Z, A, B):
    M = Z.M
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) % M for j in range(len(B[0]))] for i in range(len(A))]

def rowvec(Z, v, Q):
    M = Z.M
    return [sum(v[i] * Q[i][j] for i in range(len(v))) % M for j in range(len(Q[0]))]

def test_smith(Z, trials):
    M, p, e = Z.M, Z.p, Z.e
    for _ in range(trials):
        a, n = rng.randint(1, 4), rng.randint(1, 3)
        C = [[rng.choice([rng.randrange(M), p * rng.randrange(M), p ** (e - 1) * rng.randrange(p), 0]) for _ in range(n)] for _ in range(a)]
        exps, Q, Qi, P = smith(Z, C, n)
        I = matmul(Z, Q, Qi); assert I == [[int(i == j) for j in range(n)] for i in range(n)], "Qinv"
        D = matmul(Z, matmul(Z, P, C), Q)
        for i in range(a):
            for j in range(n):
                want = (p ** exps[j] % M) if (i == j) else 0
                assert D[i][j] == want, "PCQ diag"
        # rowspan(C) Q == (+) p^{a_t} e_t
        RS = span_bf(Z, C, n)
        RSQ = {tuple(rowvec(Z, list(v), Q)) for v in RS}
        tgt = span_bf(Z, [[(p ** exps[t] if s == t else 0) % M for s in range(n)] for t in range(n)], n)
        assert RSQ == tgt, "rowspan C Q"
        STATS["smith"] += 1

def test_P3(Z, trials, amax, nmax):
    M, p, e = Z.M, Z.p, Z.e
    for _ in range(trials):
        a, n = rng.randint(1, amax), rng.randint(1, nmax)
        mode = rng.randrange(4)
        def ent():
            if mode == 0: return rng.randrange(M)
            if mode == 1: return p * rng.randrange(M)
            if mode == 2: return rng.choice([0, p ** (e - 1) * rng.randrange(p), p * rng.randrange(M), rng.randrange(M)])
            return rng.choice([0, 0, p ** rng.randrange(e)])
        A = [[ent() for _ in range(n)] for _ in range(a)]
        if a >= 2 and rng.random() < 0.3: A[1] = [(x * rng.randrange(M)) % M for x in A[0]]  # dependent rows
        ker, H = left_kernel(Z, A, n)
        check_howell_axioms(Z, H, n + a)
        brute = {lam for lam in itertools.product(range(M), repeat=a)
                 if all(sum(lam[i] * A[i][j] for i in range(a)) % M == 0 for j in range(n))}
        got = span_bf(Z, ker, a)
        assert got == brute, ("P3 kernel", A)
        STATS["p3"] += 1

def echelon_counterexample():
    # Over Z/9, alpha = (3): an echelon form of (3 | 1) without the appended 3*(3|1) = (0|3)
    # has no row with pivot in the last block, yet the kernel {0,3,6} is nonzero.
    Z = Zpe(3, 2)
    ker, H = left_kernel(Z, [[3]], 1)
    assert span_bf(Z, ker, 1) == {(0,), (3,), (6,)}
    return H

# ---------------- Lie rings in the lemma's representation
class LieRing:
    def __init__(self, Z, es, c):  # c[(i,j)] = list of integer coords (len m)
        self.Z, self.es, self.m = Z, es, len(es)
        self.c = c
        M, p, e = Z.M, Z.p, Z.e
        for i in range(self.m):
            for j in range(self.m):
                cij = c.get((i, j), [0] * self.m)
                cji = c.get((j, i), [0] * self.m)
                for k in range(self.m):
                    assert (cij[k] + cji[k]) % p ** es[k] == 0
                    assert (p ** es[i] * cij[k]) % p ** es[k] == 0, "well-defined"
        B = [[int(a == b) for b in range(self.m)] for a in range(self.m)]
        for x, y, z in itertools.product(B, repeat=3):
            s = [(a + b + d) % p ** self.es[k] for k, (a, b, d) in enumerate(zip(self.br(x, self.br(y, z)), self.br(y, self.br(z, x)), self.br(z, self.br(x, y))))]
            assert not any(s), "Jacobi"
    def br(self, x, y):
        z = [0] * self.m
        for (i, j), v in self.c.items():
            if x[i] and y[j]:
                for k in range(self.m): z[k] += x[i] * y[j] * v[k]
        return [z[k] % self.Z.p ** self.es[k] for k in range(self.m)]
    def psi(self, t):
        Z = self.Z
        return [(Z.p ** (Z.e - self.es[i]) * t[i]) % Z.M for i in range(self.m)]
    def psiinv(self, v):
        Z = self.Z
        out = []
        for i in range(self.m):
            d = Z.p ** (Z.e - self.es[i]); assert v[i] % d == 0
            out.append((v[i] // d) % Z.p ** self.es[i])
        return out
    def brV(self, x, y):
        # lifts of psiinv arbitrary: perturb by random multiples of p^{e_i} to test lift-independence
        X = [a + rng.randrange(3) * self.Z.p ** self.es[i] for i, a in enumerate(self.psiinv(x))]
        Y = [a + rng.randrange(3) * self.Z.p ** self.es[i] for i, a in enumerate(self.psiinv(y))]
        return self.psi(self.br(X, Y))
    def elements(self):
        return [list(t) for t in itertools.product(*[range(self.Z.p ** x) for x in self.es])]

def rows(H): return [h[2] for h in H]

def present(L, S, K):
    """(N2) + (N3)."""
    Z = L.Z; M, p, e = Z.M, Z.p, Z.e; m = L.m
    s, k = rows(S), rows(K)
    a = len(s)
    ker, _ = left_kernel(Z, s + k, m)
    Rg = [lam[:a] for lam in ker]
    if Rg:
        d, Q, Qi, _ = smith(Z, Rg, a)
    else:
        d = [e] * a; Q = [[int(i == j) for j in range(a)] for i in range(a)]; Qi = Q
    I = [i for i in range(a) if d[i] >= 1]
    u = {i: [sum(Qi[i][j] * s[j][t] for j in range(a)) % M for t in range(m)] for i in I}
    def coord(yv):
        lam = member(Z, yv, S, m); assert lam is not None
        lq = rowvec(Z, lam, Q) if a else []
        return {i: lq[i] % p ** d[i] for i in I}
    sc = {(i, j): coord(L.brV(u[i], u[j])) for i in I for j in I}
    # (N3) socle tensor from the structure constants
    T = {}
    for i in I:
        for j in I:
            for kk in I:
                val = (p ** (d[i] + d[j] - 2) * sc[(i, j)][kk]) % p ** d[kk]
                assert val % p ** (d[kk] - 1) == 0, "socle divisibility"
                T[(i, j, kk)] = (val // p ** (d[kk] - 1)) % p
    def sigma(t):  # t: dict i -> int
        return [sum(t[i] * u[i][c] for i in I) % M for c in range(m)]
    def iota_sigma(x):  # x: dict i -> F_p
        return sigma({i: (x[i] % p) * p ** (d[i] - 1) for i in I})
    return dict(I=I, d=d, u=u, coord=coord, sc=sc, T=T, sigma=sigma, iota_sigma=iota_sigma)

def idealizer(L, S, Kp):
    """(N6)."""
    Z = L.Z; M, p, e = Z.M, Z.p, Z.e; m = L.m
    s, kp = rows(S), rows(Kp)
    if not kp: return S
    b, Qp, _, _ = smith(Z, kp, m)
    theta = lambda v: [(p ** (e - b[l]) * x) % M for l, x in enumerate(rowvec(Z, v, Qp))]
    A = [sum((theta(L.brV(si, kl)) for kl in kp), []) for si in s]
    ker, _ = left_kernel(Z, A, len(kp) * m)
    gens = [[sum(lam[i] * s[i][t] for i in range(len(s))) % M for t in range(m)] for lam in ker]
    return howell(Z, gens, m)

def setof(L, H):
    return {tuple(L.psiinv(list(v))) for v in span_bf(L.Z, rows(H), L.m)}

def fp_basis(vecs, p, n):
    B = []  # reduced echelon over F_p
    for v in vecs:
        v = [x % p for x in v]
        for (piv, b) in B:
            if v[piv]: f = v[piv]; v = [(x - f * y) % p for x, y in zip(v, b)]
        nz = [i for i, x in enumerate(v) if x]
        if nz:
            piv = nz[0]; inv = pow(v[piv], -1, p); v = [(x * inv) % p for x in v]
            B2 = []
            for (pv, b) in B:
                if b[piv]: f = b[piv]; b = [(x - f * y) % p for x, y in zip(b, v)]
                B2.append((pv, b))
            B = B2 + [(piv, v)]
    return B

def rtf(L, Hset, oracle="truth"):
    """Algorithm RtF with procedures (N1)-(N6); oracle 'truth' or 'random'. Returns output set, calls, rounds."""
    Z = L.Z; M, p, e = Z.M, Z.p, Z.e; m = L.m
    b = sum(L.es)
    S = howell(Z, [L.psi([int(i == j) for j in range(m)]) for i in range(m)], m)
    K = []
    calls = rounds = 0
    elems = L.elements()
    while True:
        rounds += 1
        Sset, Kset = setof(L, S), setof(L, K)
        assert Kset <= Sset
        # (N1)
        eq = all(member(Z, r, K, m) is not None for r in rows(S)) if K else not S
        assert eq == (Sset == Kset)
        if eq: return Kset, calls, rounds
        P = present(L, S, K)
        I, d, u = P["I"], P["d"], P["u"]
        validate_present(L, S, K, Sset, Kset, P)
        m0 = len(I)
        calls += 1
        # oracle answer: list of vectors in F_p^{m0} (indexed by I order)
        if oracle == "truth":
            ret = []
            for x in itertools.product(range(p), repeat=m0):
                xv = dict(zip(I, x))
                y = tuple(L.psiinv(P["iota_sigma"](xv)))
                if y in Hset: ret.append(list(x))
        else:
            ret = [[rng.randrange(p) for _ in range(m0)] for _ in range(rng.randint(0, m0 + 1))]
            if rng.random() < 0.5 and ret: ret = ret[:1]
        if len(ret) > m0 and oracle != "truth": return Kset, calls, rounds  # treated as stopped
        B = [bv for (_, bv) in fp_basis(ret, p, m0)]
        if not B: return Kset, calls, rounds
        # closure under the bracket of Omega (tensor T)
        def brT(x, y):
            return [sum(x[ii] * y[jj] * P["T"][(I[ii], I[jj], I[kk])] for ii in range(m0) for jj in range(m0)) % p for kk in range(m0)]
        Bech = fp_basis(B, p, m0)
        closed = True
        for x in B:
            for y in B:
                z = brT(x, y)
                for (piv, bv) in Bech:
                    if z[piv]: f = z[piv]; z = [(q - f * w) % p for q, w in zip(z, bv)]
                if any(z): closed = False
        if not closed: return Kset, calls, rounds
        # (N5)
        Kp = howell(Z, rows(K) + [P["iota_sigma"](dict(zip(I, x))) for x in B], m)
        Uspan = span_bf(Zpe(p, 1), B, m0)
        Kp_brute = {tuple(y) for y in map(tuple, (L.psiinv(list(v)) for v in span_bf(Z, rows(S), m)))
                    if any(all(tuple(L.psiinv([(a - c) % M for a, c in zip(L.psi(list(y)), P["iota_sigma"](dict(zip(I, x))))])) in Kset for _ in [0]) for x in Uspan)}
        assert setof(L, Kp) == Kp_brute, "N5"
        Kpset = setof(L, Kp)
        assert Kset < Kpset
        # (N6)
        Sp = idealizer(L, S, Kp)
        Kgen = Kpset if len(Sset) * len(Kpset) <= 400000 else {tuple(L.psiinv(r)) for r in rows(Kp)} | {tuple(L.psiinv(r)) for r in rows(K)}
        brute = {y for y in Sset if all(tuple(L.br(list(y), list(k))) in Kpset for k in Kgen)}
        assert setof(L, Sp) == brute, "N6 idealizer"
        STATS["n6"] += 1
        S, K = Sp, Kp
        assert rounds <= b + 1

def validate_present(L, S, K, Sset, Kset, P):
    Z = L.Z; M, p = Z.M, Z.p
    I, d, u = P["I"], P["d"], P["u"]
    U = {i: tuple(L.psiinv(u[i])) for i in I}
    order = 1
    for i in I: order *= p ** d[i]
    assert order * len(Kset) == len(Sset), "N2 order"
    for i in I:
        assert U[i] in Sset
        assert tuple(L.psiinv([(p ** d[i] * x) % M for x in u[i]])) in Kset
    for t in itertools.product(*[range(p ** d[i]) for i in I]):
        if any(t):
            y = tuple(L.psiinv(P["sigma"](dict(zip(I, t)))))
            assert y not in Kset, "N2 independence"
    for y in Sset:
        t = P["coord"](L.psi(list(y)))
        diff = [(a - c) % M for a, c in zip(L.psi(list(y)), P["sigma"](t))]
        assert tuple(L.psiinv(diff)) in Kset, "N2 coord"
    for i in I:
        for j in I:
            lhs = L.psi(L.br(list(U[i]), list(U[j])))
            rhs = P["sigma"](P["sc"][(i, j)])
            assert tuple(L.psiinv([(a - c) % M for a, c in zip(lhs, rhs)])) in Kset, "N2 constants"
    # (N3): iota is a Lie map F_p^{m0} -> (S/K)[p] modulo K, onto
    for i in I:
        for j in I:
            xi = {k: int(k == i) for k in I}; xj = {k: int(k == j) for k in I}
            lhs = L.psi(L.br(L.psiinv(P["iota_sigma"](xi)), L.psiinv(P["iota_sigma"](xj))))
            rhs = P["iota_sigma"]({k: P["T"][(i, j, k)] for k in I})
            assert tuple(L.psiinv([(a - c) % M for a, c in zip(lhs, rhs)])) in Kset, "N3 tensor"
    socle = [y for y in Sset if tuple((p * a) % (p ** L.es[k]) for k, a in enumerate(y)) in Kset]
    assert len(socle) == p ** len(I) * len(Kset), "N3 socle size"
    STATS["n2"] += 1

def subring_gen(L, gens):
    Z = L.Z
    H = howell(Z, [L.psi(g) for g in gens], L.m)
    while True:
        rs = rows(H)
        H2 = howell(Z, rs + [L.brV(x, y) for x in rs for y in rs], L.m)
        if setof(L, H2) == setof(L, H): return H
        H = H2

def put(c, m, i, j, vec):
    c[(i, j)] = list(vec); c[(j, i)] = [-x for x in vec]

def rings():
    out = []
    # mixed Heisenberg over Z/9: x,y order 9, z order 3, [x,y] = z
    Z = Zpe(3, 2); c = {}; put(c, 3, 0, 1, [0, 0, 1]); out.append(LieRing(Z, [2, 2, 1], c))
    # Z/27 x + Z/9 y + Z/3 z, [x,y] = z, [x,z]=0
    Z = Zpe(3, 3); c = {}; put(c, 3, 0, 1, [0, 0, 1]); out.append(LieRing(Z, [3, 2, 1], c))
    # Z/27 x + Z/9 y, [x,y] = 3y  (class grows with e; fine for the linear algebra)
    Z = Zpe(3, 3); c = {}; put(c, 2, 0, 1, [0, 3]); out.append(LieRing(Z, [3, 2], c))
    # Z/25 x + Z/5 y, [x,y] = 5x
    Z = Zpe(5, 2); c = {}; put(c, 2, 0, 1, [5, 0]); out.append(LieRing(Z, [2, 1], c))
    # Z/25 x + Z/25 y + Z/5 z, [x,y] = z
    Z = Zpe(5, 2); c = {}; put(c, 3, 0, 1, [0, 0, 1]); out.append(LieRing(Z, [2, 2, 1], c))
    # p = 2 (linear algebra only): Z/8 x + Z/4 y + Z/2 z, [x,y] = z
    Z = Zpe(2, 3); c = {}; put(c, 3, 0, 1, [0, 0, 1]); out.append(LieRing(Z, [3, 2, 1], c))
    # Z/8 x + Z/8 y, [x,y] = 2y
    Z = Zpe(2, 3); c = {}; put(c, 2, 0, 1, [0, 2]); out.append(LieRing(Z, [3, 3], c))
    # filiform-type over Z/9 with mixed orders: x (9), y (3), z (3), [x,y] = z
    Z = Zpe(3, 2); c = {}; put(c, 3, 0, 1, [0, 0, 1]); out.append(LieRing(Z, [2, 1, 1], c))
    # Z/9: x(9), y(9), z(9), w(3): [x,y]=z, [x,z]=w  (needs 9[x,z]=0 in w: ok; 3 z? [x,3z]=3w=0 fine)
    Z = Zpe(3, 2); c = {}; put(c, 4, 0, 1, [0, 0, 1, 0]); put(c, 4, 0, 2, [0, 0, 0, 1]); out.append(LieRing(Z, [2, 2, 2, 1], c))
    return out

def main():
    for (p, e, tr, amax, nmax) in [(3, 2, 150, 3, 3), (2, 3, 150, 3, 3), (3, 3, 60, 2, 3), (5, 2, 60, 2, 3)]:
        Z = Zpe(p, e)
        test_P3(Z, tr, amax, nmax)
        test_smith(Z, 60)
    echelon_counterexample()
    for L in rings():
        elems = L.elements()
        for _ in range(12 if len(elems) <= 800 else 5):
            gens = [rng.choice(elems) for _ in range(rng.randint(0, 2))]
            Hs = setof(L, subring_gen(L, gens)) if gens else {tuple([0] * L.m)}
            out, calls, rounds = rtf(L, Hs, "truth")
            assert out == Hs, "RtF output"
            assert calls <= sum(L.es) and rounds <= sum(L.es) + 1
            STATS["rtf"] += 1
            out, calls, rounds = rtf(L, Hs, "random")
            assert calls <= sum(L.es) and rounds <= sum(L.es) + 1
            STATS["rtf_bad"] += 1
    print("seed", SEED, "OK", STATS)

main()
