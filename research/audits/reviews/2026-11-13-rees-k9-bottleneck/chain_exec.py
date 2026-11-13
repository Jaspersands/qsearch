#!/opt/anaconda3/bin/python
"""End-to-end executor for R8 plans with chain nodes (finite exact checks; can only falsify).

Written from the definitions only (thm:app-s2-chain proof; Lemmas S and F of 2026-11-12-rees-exponent-k8-attack
sec. 2); it shares no code with mrd_execute.py or rc.py except that the RC witnesses are found here by its own
brute-force DFS (pure Python) and checked cell by cell with a discrete-log table built here.
Plan syntax: (('ch', m, chainpath), ..., finish) with chainpath = [(D1,K1),...,(DL,KL)],
finish = ('F0',) | ('F1',) | ('F2', Dp, chainpath_for_Dp) | ('F3', chainpath) -- a K-node given by its chain.
Usage: chain_exec.py trials
"""
import sys, random, itertools, functools, math

def prim_root(p):
    fs = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // f, p) != 1 for f in fs))

@functools.lru_cache(None)
def dlog(p):
    g = prim_root(p); L = {}; x = 1
    for e in range(p - 1):
        L[x] = e; x = x * g % p
    return g, L

def inv(x, p): return pow(x, p - 2, p)

@functools.lru_cache(None)
def rc_witness(p, D, R, K):
    """alpha (len D), beta (dict on R) with alpha_0 = 1, beta_0 = 0; alpha_j + beta_i in {0} u U_{k in K} Q^(D)_{k-i-j}."""
    g, L = dlog(p)
    ok = lambda y, i, j: y == 0 or (L[y] + i + j) % D in K
    Rr = [i for i in R if i != 0]
    cand0 = [set(x for x in range(p) if ok(x, 0, j)) for j in range(D)]
    cand0[0] = {1}
    beta = {0: 0}
    def rec(t, C):
        if t == len(Rr):
            return [min(c) for c in C]
        i = Rr[t]
        for b in range(p):
            if not ok((1 + b) % p, i, 0):
                continue
            C2 = []
            for j in range(D):
                s = {x for x in C[j] if ok((x + b) % p, i, j)}
                if not s: break
                C2.append(s)
            else:
                beta[i] = b
                r = rec(t + 1, C2)
                if r: return r
        return None
    al = rec(0, cand0)
    assert al is not None, ('no RC', p, D, R, K)
    be = dict(beta)
    for i in R:
        for j in range(D):
            assert ok((al[j] + be[i]) % p, i, j)
    return tuple(al), tuple(sorted(be.items()))

def lift(D, K, D2): return tuple(x for x in range(D2) if (x % D) in K)

# ---------- linear algebra mod p ----------
def rref_null(cols, dim, p):
    """nonzero c with sum c_b cols[b] = 0 (cols: list of dim-vectors), len(cols) > rank."""
    n = len(cols)
    M = [[cols[j][i] % p for j in range(n)] for i in range(dim)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, dim) if M[i][c]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][c], p); M[r] = [y * iv % p for y in M[r]]
        for i in range(dim):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(y - f * z) % p for y, z in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = next(c for c in range(n) if c not in piv)
    x = [0] * n; x[free] = 1
    for i, c in enumerate(piv): x[c] = (-M[i][free]) % p
    return x

def annihilator(basis, a, p):
    """rows Q (list of a-vectors) with {v : Qv = 0} = span(basis)."""
    if not basis:
        return [[int(i == j) for j in range(a)] for i in range(a)]
    # null space of the matrix whose rows are basis vectors
    k = len(basis)
    M = [list(v) for v in basis]
    piv, r = [], 0
    for c in range(a):
        pr = next((i for i in range(r, k) if M[i][c] % p), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][c], p); M[r] = [y * iv % p for y in M[r]]
        for i in range(k):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(y - f * z) % p for y, z in zip(M[i], M[r])]
        piv.append(c); r += 1
    out = []
    for fcol in [c for c in range(a) if c not in piv]:
        x = [0] * a; x[fcol] = 1
        for i, c in enumerate(piv): x[c] = (-M[i][fcol]) % p
        out.append(x)
    return out

def apply(Q, v, p): return [sum(q * y for q, y in zip(row, v)) % p for row in Q]

def lin(ws, vecs, p, a):
    s = [0] * a
    for b, w in ws.items():
        s = [(x + w * y) % p for x, y in zip(s, vecs[b])]
    return s

# ---------- chain node (thm:app-s2-chain) ----------
class Chain:
    def __init__(self, p, kap, path):
        self.p, self.kap, self.path = p, kap, path
        self.steps = []
        Dprev, Kprev = 1, (0,)
        for (D, K) in path:
            R = lift(Dprev, Kprev, D)
            al, be = rc_witness(p, D, R, tuple(K))
            self.steps.append((D, al, dict(be)))
            Dprev, Kprev = D, tuple(K)
        self.final = lift(Dprev, Kprev, kap)
    def arity(self, a):
        L = len(self.path); return math.comb(a + L + 1, L + 1)
    def __call__(self, vecs, a):
        p = self.p; g, Lg = dlog(p)
        stream = iter(range(len(vecs)))
        def P(t, U):
            """weights w (dict col->val), sum in span(U), designated col with weight 1, D_t-classes in K_t."""
            Q = annihilator(U, a, p)
            m = len(Q)
            if t == 0:
                cols = [next(stream) for _ in range(m + 1)]
                c = rref_null([apply(Q, vecs[b], p) if Q else [] for b in cols], m, p)
                nz = next(i for i in range(len(cols)) if c[i])
                s = inv(c[nz], p)
                return {cols[i]: c[i] * s % p for i in range(len(cols)) if c[i]}, cols[nz]
            D, al, be = self.steps[t - 1]
            V = list(U); rounds = []
            while True:
                w, des = P(t - 1, V)
                e = lin(w, vecs, p, a)
                v = lin({b: be[Lg[x] % D] * x % p for b, x in w.items()}, vecs, p, a)
                QV = annihilator(V, a, p)
                rounds.append((w, des, e, v, list(V), QV))
                if not any(apply(QV, v, p)) :
                    break
                V = V + [v]
            def weights(k, gam):
                w = rounds[k][0]; n = Lg[gam] % D
                return {b: gam * x * (al[n] + be[Lg[x] % D]) % p for b, x in w.items() if gam * x * (al[n] + be[Lg[x] % D]) % p}
            ks = len(rounds) - 1
            W = weights(ks, 1); des = rounds[ks][1]
            assert W.get(des) == 1
            tau = [(-(x + y)) % p for x, y in zip(rounds[ks][2], rounds[ks][3])]
            for k in range(ks - 1, -1, -1):
                w, _, e, v, Vk, QV = rounds[k]
                qt, qv = apply(QV, tau, p), apply(QV, v, p)
                i0 = next(i for i in range(len(qv)) if qv[i])
                gam = qt[i0] * inv(qv[i0], p) % p
                assert all((qt[i] - gam * qv[i]) % p == 0 for i in range(len(qv)))
                if gam:
                    n = Lg[gam] % D
                    for b, x in weights(k, gam).items():
                        assert b not in W
                        W[b] = x
                    tau = [(tt - gam * (al[n] * ee + vv)) % p for tt, ee, vv in zip(tau, e, v)]
            # check: value in span(U), classes
            Qu = annihilator(U, a, p)
            assert not any(apply(Qu, lin(W, vecs, p, a), p))
            return W, des
        W, des = P(len(self.steps), [])
        x = [0] * len(vecs)
        for b, y in W.items(): x[b] = y
        assert W[des] == 1 and all(Lg[y] % self.kap in self.final for y in W.values()), 'chain output class violation'
        return x

# ---------- descent (Lemmas S, F) ----------
EXITS = {}
class Found(Exception):
    def __init__(self, x, how='?'):
        self.x = x; EXITS[how] = EXITS.get(how, 0) + 1

def run(p, kap, plan, lams, a):
    g, Lg = dlog(p)
    cls = lambda y: Lg[y] % kap
    objs = [(list(l), [(1, {b: 1})]) for b, l in enumerate(lams)]   # (vector, [(ratio, rep)])
    *stages, fin = plan
    try:
        for (_, m, path) in stages:
            node = Chain(p, kap, path)
            assert set(node.final) <= {0, m}
            A = node.arity(a); nxt = []
            zm = pow(g, m, p); eps = (-inv(zm, p)) % p
            for s in range(0, len(objs) - A + 1, A):
                grp = objs[s:s + A]
                x = node([o[0] for o in grp], a)
                I = [n for n in range(A) if x[n] and cls(x[n]) == 0]
                J = [n for n in range(A) if x[n] and cls(x[n]) == m]
                assert len(I) + len(J) == sum(1 for y in x if y)
                def side(S, sc):
                    reps = []
                    for kk in range(len(grp[0][1])):
                        rep = {}
                        for n in S:
                            for col, cc in grp[n][1][kk][1].items():
                                rep[col] = x[n] * sc * cc % p
                        reps.append(rep)
                    return reps
                if not J: raise Found(side(I, 1)[0], 'stage-onesided')
                if not I: raise Found(side(J, inv(zm, p))[0], 'stage-onesided')
                u = [0] * a
                for n in I: u = [(y + x[n] * q) % p for y, q in zip(u, grp[n][0])]
                ratios = [r for r, _ in grp[0][1]]
                nxt.append((u, list(zip(ratios, side(I, 1))) + [(r * eps % p, d) for r, d in zip(ratios, side(J, inv(zm, p)))]))
            objs = nxt
        for o in objs:
            if not any(o[0]): raise Found(o[1][0][1], 'zero-object')
        ratios = [r for r, _ in objs[0][1]]
        Pv = [y for y in range(1, p) if cls(y) == 0]
        tab = {}
        for y in itertools.product([0] + Pv, repeat=len(ratios)):
            if any(y):
                tab.setdefault(sum(yy * r for yy, r in zip(y, ratios)) % p, y)
        def emit(coef):
            x = {}
            for n, cf in enumerate(coef):
                if cf:
                    for yk, (r, d) in zip(tab[cf], objs[n][1]):
                        if yk:
                            for col, cc in d.items(): x[col] = yk * cc % p
            raise Found(x, 'finish')
        if fin[0] == 'F0':
            y = tab[0]; x = {}
            for yk, (r, d) in zip(y, objs[0][1]):
                if yk:
                    for col, cc in d.items(): x[col] = yk * cc % p
            raise Found(x, 'finish')
        if fin[0] == 'F1':
            eta = rref_null([o[0] for o in objs[:a + 1]], a, p) + [0] * (len(objs) - a - 1)
        else:
            node = Chain(p, kap, fin[-1])
            A = node.arity(a)
            eta = node([o[0] for o in objs[:A]], a) + [0] * (len(objs) - A)
        rho = next(pow(g, c, p) for c in range(kap) if all(not e or pow(g, c, p) * e % p in tab for e in eta)) if fin[0] != 'F1' else 1
        assert all(not e or rho * e % p in tab for e in eta), 'finish class condition fails'
        emit([rho * e % p for e in eta])
    except Found as F:
        xv = [0] * len(lams)
        for col, cc in F.x.items(): xv[col] = cc
        return xv

def plan_arity(p, kap, plan, a):
    A = 1
    for st in plan[:-1]: A *= Chain(p, kap, st[2]).arity(a)
    fin = plan[-1]
    if fin[0] == 'F1': A *= a + 1
    elif fin[0] != 'F0': A *= Chain(p, kap, fin[-1]).arity(a)
    return A

def verify(x, lams, p, kap, a):
    g, Lg = dlog(p)
    return any(x) and all(y == 0 or Lg[y] % kap == 0 for y in x) and all(sum(y * l[i] for y, l in zip(x, lams)) % p == 0 for i in range(a))

def banks(p, a, n, rng):
    yield 'uniform', [[rng.randrange(p) for _ in range(a)] for _ in range(n)]
    yield 'all-e1', [[1] + [0] * (a - 1) for _ in range(n)]
    S = [[rng.randrange(p) for _ in range(a)] for _ in range(2)]
    yield 'two-values', [rng.choice(S) for _ in range(n)]
    g = prim_root(p)
    yield 'coset-reps', [[pow(g, rng.randrange(p - 1), p) * (i == b % a) for i in range(a)] for b in range(n)]
    yield 'one-class', [[pow(g, 9 * rng.randrange(p), p) * (i == b % a) for i in range(a)] for b in range(n)]

PLANS = {
    # (p, kappa): plan  (from exponents_r8.out; chain paths from chains_all_*.out)
    'p37': (37, 9, (('ch', 4, [(3, (0,)), (9, (0, 4))]), ('F3', [(9, (0, 2, 3, 5))]))),
    'p73': (73, 9, (('ch', 1, [(3, (0,)), (9, (0, 1))]), ('F2', 3, [(3, (0,))]))),
    'p19': (19, 9, (('ch', 1, [(3, (0,)), (9, (0, 1))]), ('F3', [(9, (0, 1, 4, 7)), (9, (0, 3, 8))]))),
    'p29k7': (29, 7, (('ch', 1, [(7, (0, 1, 2)), (7, (0, 1))]), ('F3', [(7, (0, 1, 4))]))),
    'p127chain': (127, 9, (('F3', [(3, (0,)), (9, (0, 3)), (9, (0,))]),)),
    'p181chain': (181, 9, (('F3', [(3, (0,)), (9, (0, 1)), (9, (0,))]),)),
    'p433chain': (433, 9, (('F3', [(3, (0,)), (9, (0, 1)), (9, (0,))]),)),
}

if __name__ == '__main__':
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    names = sys.argv[2:] or list(PLANS)
    rng = random.Random(2026)
    tot = ok = 0
    for nm in names:
        p, kap, plan = PLANS[nm]
        for a in (1, 2, 3):
            n = plan_arity(p, kap, plan, a)
            if n > 4000:
                print(f'{nm} a={a}: arity {n} NOT run'); continue
            res = []
            for _ in range(trials):
                for bname, L in banks(p, a, n, rng):
                    x = run(p, kap, plan, L, a)
                    good = verify(x, L, p, kap, a)
                    res.append(good); tot += 1; ok += good
                    if not good: print('   FAIL', nm, a, bname)
            print(f'{nm} p={p} a={a} M={n}: {sum(res)}/{len(res)} verified; exits {dict(EXITS)}', flush=True); EXITS.clear()
    print(f'TOTAL {ok}/{tot}')
