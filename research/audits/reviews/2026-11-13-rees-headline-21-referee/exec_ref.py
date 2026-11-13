"""Referee end-to-end executor for the NEW node types of fragment.tex at the binding small primes:
Lemma R chains with union targets and same-modulus refinements, Lemma S stages over {0,m}-nodes with
m != kappa/2, Lemma F_K finishes by chain K-nodes.  Written from the fragment, independent of executor.py.
Checks every output: kappa-solution (weights in P u {0}, nonzero, sum w*lambda = 0)."""
import json, os, random, sys
import rule_ref as RR
from paths_ref import chains_paths, path
from chk_ref import least_prim_root
SRC = RR.SRC
W = json.load(open(os.path.join(SRC, 'tierB_witnesses.json')))
CJ = json.load(open(os.path.join(SRC, 'certs_stage1.json')))
WIT = {}
for w in W: WIT[(w['p'], w['D'], frozenset(w['R']), frozenset(w['K']))] = (w['alpha'], {int(i): x for i, x in w['beta'].items()})

class Ctx:
    def __init__(self, p):
        self.p = p; self.g = least_prim_root(p)
    def cl(self, x, D):
        p = self.p; x %= p; assert x
        z = pow(self.g, (p - 1) // D, p); y = pow(x, (p - 1) // D, p); t = 1
        for c in range(D):
            if t == y: return c
            t = t * z % p
        raise AssertionError
    def inv(self, x): return pow(x % self.p, self.p - 2, self.p)

def nullvec(ctx, cols, dim):
    """nonzero vector eta with sum eta_nu cols[nu] = 0 (cols: list of length-dim lists), len(cols) > dim."""
    p = ctx.p; n = len(cols); assert n > dim
    M = [[cols[nu][i] % p for nu in range(n)] for i in range(dim)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, dim) if M[i][c]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; iv = ctx.inv(M[r][c]); M[r] = [x * iv % p for x in M[r]]
        for i in range(dim):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == dim: break
    free = next(c for c in range(n) if c not in piv)
    eta = [0] * n; eta[free] = 1
    for i, c in enumerate(piv): eta[c] = (-M[i][free]) % p
    return eta, free

def comb(ctx, w, cols, a):
    s = [0] * a
    for wb, v in zip(w, cols):
        if wb:
            for i in range(a): s[i] = (s[i] + wb * v[i]) % ctx.p
    return s

class GE:
    mod = 1
    def __init__(s, ctx): s.ctx = ctx
    def N(s, a): return a + 1
    def run(s, cols, a):
        eta, f = nullvec(s.ctx, cols[:a + 1], a)
        return eta + [0] * (len(cols) - a - 1), f

class Refine:
    def __init__(s, ctx, inner, D, R, K, alpha, beta):
        s.ctx, s.inner, s.mod, s.R, s.K, s.al, s.be = ctx, inner, D, sorted(R), set(K), alpha, beta
    def N(s, a): return s.inner.N(a) * ((len(s.R) - 1) * a + 1)
    def run(s, cols, a):
        ctx, p, D = s.ctx, s.ctx.p, s.mod
        Nin, n = s.inner.N(a), (len(s.R) - 1) * a + 1
        cs, U = [], []
        for nu in range(n):
            blk = cols[nu * Nin:(nu + 1) * Nin]
            c, bst = s.inner.run(blk, a)
            assert c[bst] == 1
            assert ctx.cl(1, D) == 0
            Ui = {i: [0] * a for i in s.R}
            for b, cb in enumerate(c):
                if cb:
                    i = ctx.cl(cb, D); assert i in Ui, ('class outside R', i)
                    for t in range(a): Ui[i][t] = (Ui[i][t] + cb * blk[b][t]) % p
            cs.append((c, bst)); U.append(Ui)
        vecs = [sum((U[nu][i] for i in s.R if i), []) for nu in range(n)]
        eta, nst = nullvec(ctx, vecs, (len(s.R) - 1) * a)
        w = [0] * len(cols)
        for nu in range(n):
            if not eta[nu]: continue
            j = ctx.cl(eta[nu], D); c, _ = cs[nu]
            for b, cb in enumerate(c):
                if cb:
                    w[nu * Nin + b] = eta[nu] * (s.al[j] + s.be[ctx.cl(cb, D)]) % p * cb % p
        bst = nst * Nin + cs[nst][1]
        assert w[bst] and ctx.cl(w[bst], D) == 0
        iv = ctx.inv(w[bst]); w = [x * iv % p for x in w]
        # K-relation check
        assert comb(ctx, w, cols, a) == [0] * a
        assert all(ctx.cl(x, D) in s.K for x in w if x)
        return w, bst

class Plan:
    """s = 1 stage over a {0,m}-node T at modulus kap, then F_K by K-node F (Lemmas S, F_K)."""
    def __init__(s, ctx, kap, T, m, F, K):
        s.ctx, s.kap, s.T, s.m, s.F, s.K = ctx, kap, T, m, F, sorted(K); s.mod = kap
    def N(s, a): return s.T.N(a) * s.F.N(a)
    def run(s, cols, a):
        ctx, p, kap = s.ctx, s.ctx.p, s.kap
        q = pow(ctx.g, s.m, p); eps = (-ctx.inv(q)) % p
        NT, NF = s.T.N(a), s.F.N(a)
        objs = []
        for g_ in range(NF):
            blk = cols[g_ * NT:(g_ + 1) * NT]; off = g_ * NT
            x, _ = s.T.run(blk, a)
            I = [b for b, xb in enumerate(x) if xb and ctx.cl(xb, kap) == 0]
            J = [b for b, xb in enumerate(x) if xb and ctx.cl(xb, kap) == s.m % kap]
            assert len(I) + len(J) == sum(1 for xb in x if xb) and I
            if not J:
                w = [0] * len(cols)
                for b in I: w[off + b] = x[b]
                return s.fin(w, cols, a)
            u = comb(ctx, [x[b] if b in I else 0 for b in range(NT)], blk, a)
            R1 = {off + b: x[b] for b in I}; R2 = {off + b: x[b] * ctx.inv(q) % p for b in J}
            assert comb(ctx, [R2.get(off + b, 0) for b in range(NT)], blk, a) == [eps * t % p for t in u]
            objs.append((u, R1, R2))
        eta, _ = s.F.run([o[0] for o in objs], a)
        Pset = {pow(x, kap, p) for x in range(1, p)}
        Tcl = set()
        for y1 in list(Pset) + [0]:
            for y2 in list(Pset) + [0]:
                if y1 or y2:
                    v = (y1 + eps * y2) % p
                    if v: Tcl.add(ctx.cl(v, kap))
        sh = next(u_ for u_ in range(kap) if all((u_ + k) % kap in Tcl for k in s.K))
        w = [0] * len(cols)
        for nu, en in enumerate(eta):
            if not en: continue
            ep = pow(ctx.g, sh, p) * en % p
            y = next((y1, y2) for y1 in list(Pset) + [0] for y2 in list(Pset) + [0]
                     if (y1 or y2) and (y1 + eps * y2) % p == ep)
            u, R1, R2 = objs[nu]
            for b, wb in R1.items():
                if y[0]: w[b] = y[0] * wb % p
            for b, wb in R2.items():
                if y[1]: w[b] = y[1] * wb % p
        return s.fin(w, cols, a)
    def fin(s, w, cols, a):
        ctx, p, kap = s.ctx, s.ctx.p, s.kap
        assert any(w) and comb(ctx, w, cols, a) == [0] * a
        assert all(ctx.cl(x, kap) == 0 for x in w if x), 'weight outside P'
        b = next(i for i, x in enumerate(w) if x); iv = ctx.inv(w[b])
        return [x * iv % p for x in w], b

def solver(ctx, D, e):
    p = ctx.p
    if D in (3, 4, 5):
        c = CJ[f'two-level {D}']['found'].get(str(p))
        if c:
            return Refine(ctx, GE(ctx), D, range(D), [0], c['alpha'], {int(i): x for i, x in c['beta'].items()})
    if D == 2:
        return Plan(ctx, 2, GE(ctx), 1, GE(ctx), [0, 1])
    raise NotImplementedError(D)

def build(ctx, kap, K, e):
    b = chains_paths(ctx.p, kap, e)
    pth = path(b, (kap, frozenset(K)))
    node = None
    for st in pth:
        if st[0] == 'GE': node = GE(ctx)
        elif st[0] == 'solver': node = solver(ctx, st[1], e)
        else:
            D2, R, K2 = st; al, be = WIT[(ctx.p, D2, R, K2)]
            node = Refine(ctx, node, D2, R, K2, al, be)
    return node, pth

def banks(p, a, N, rng):
    yield 'uniform', [[rng.randrange(p) for _ in range(a)] for _ in range(N)]
    v = [rng.randrange(1, p) for _ in range(a)]
    yield 'repeated', [list(v) for _ in range(N)]
    yield 'axis', [[1 if i == (b % a) else 0 for i in range(a)] for b in range(N)]
    yield 'zero-heavy', [[rng.randrange(p) if rng.random() < 0.1 else 0 for _ in range(a)] for _ in range(N)]
    yield 'two-values', [[rng.choice([1, p - 1]) for _ in range(a)] for _ in range(N)]

CASES = [  # (p, kappa, two-class K, m, finish K) as found by rule_ref degrees
    (13, 4, [0, 1], 1, [0, 1, 2]), (13, 6, [0, 3], 3, [0, 1, 3]), (19, 6, [0, 3], 3, [0, 1, 3]),
    (19, 9, [0, 1], 1, [0, 1, 4]), (37, 9, [0, 4], 4, [0, 2, 5]), (73, 8, [0, 4], 4, [0, 1, 4]),
    (73, 9, [0, 1], 1, [0, 1, 5]), (5, 4, [0, 1], 1, [0, 1, 2])]
if __name__ == '__main__':
    rng = random.Random(20261113); tot = 0
    for p, kap, TK, m, FK in CASES:
        ctx = Ctx(p); e, pl = RR.degrees(p)
        T, pT = build(ctx, kap, TK, e); F, pF = build(ctx, kap, FK, e)
        P = Plan(ctx, kap, T, m, F, FK)
        for a in (1, 2):
            N = P.N(a)
            for name, cols in banks(p, a, N, rng):
                for rep in range(3 if name == 'uniform' else 1):
                    if rep: cols = [[rng.randrange(p) for _ in range(a)] for _ in range(N)]
                    P.run(cols, a); tot += 1
        print(p, kap, 'e =', e[kap], 'two-class path', pT, 'finish path', pF, 'ok', flush=True)
    # same-modulus union chain at 43, kappa = 7: chain0 of degree 4, then 7-solver
    ctx = Ctx(43); e, _ = RR.degrees(43); N7, p7 = build(ctx, 7, [0], e)
    for a in (1, 2):
        for name, cols in banks(43, a, N7.N(a), rng):
            w, b = N7.run(cols, a)
            assert all(ctx.cl(x, 7) == 0 for x in w if x); tot += 1
    print(43, 7, 'chain0 path', p7, 'ok')
    print('ALL OK', tot, 'runs')
