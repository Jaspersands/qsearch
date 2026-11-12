r"""Independent executor for the multi-representation descent (Lemmas S, F; Cor. HCD; Cor. 41).

Referee code, 2026-11-12; written without reading the attack's executors.
A solver for exponent kappa returns ROOTS r_b (not only weights) with sum r_b^kappa lam_b = 0,
r != 0. Roots are taken from a full table at the (small) test primes; at large p this step is
Las Vegas root finding (see report).  Every output is verified exactly.

Plans (from s1h_independent.e_table): 'GE', 'S1t' (not executed; replaced by the recursive
HCD where available, or by exhaustive search for odd kappa at tiny a -- marked), 'sxHCD+F0/F1/F2(D)'.
Corollary 41: stage = kappa-4 two-level contraction (lem:app-s2-tensor + witness), finish =
kappa-8 two-level union step to K = {0,1,2,3}.
"""
import sys, random, itertools, math, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from s1h_independent import Field, e_table

class Ctx:
    def __init__(self, p):
        self.F = Field(p); self.p = p
        self.roots = {}   # (kappa) -> dict w -> some r with r^kappa = w
    def root(self, kappa, w):
        p = self.p
        if w % p == 0: return 0
        if kappa not in self.roots:
            d = {}
            for r in range(1, p):
                d.setdefault(pow(r, kappa, p), r)
            self.roots[kappa] = d
        return self.roots[kappa][w % p]          # KeyError = not a kappa-th power (bug)
    def cl(self, kappa, x): return int(self.F.log[x % self.p]) % kappa

def nullvec(vecs, p):
    """nonzero x with sum x_i vecs[i] = 0 (len(vecs) > dim) by Gaussian elimination."""
    n = len(vecs); a = len(vecs[0])
    # matrix a x n
    M = [[vecs[j][i] % p for j in range(n)] for i in range(a)]
    piv = []; r = 0
    for c in range(n):
        pr = next((i for i in range(r, a) if M[i][c]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [v * inv % p for v in M[r]]
        for i in range(a):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(vi - f * vr) % p for vi, vr in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == a: break
    free = next(c for c in range(n) if c not in piv)
    x = [0] * n; x[free] = 1
    for i, c in enumerate(piv): x[c] = (-M[i][free]) % p
    return x

def lin(coefs, vecs, p):
    a = len(vecs[0]); out = [0] * a
    for c, v in zip(coefs, vecs):
        if c:
            for i in range(a): out[i] = (out[i] + c * v[i]) % p
    return out

def represent(ctx, kappa, cs, eta):
    """y in (P u 0)^r, y != 0, with sum y_k cs_k = eta; returns list of roots (y_k = root^kappa)."""
    p = ctx.p
    Pk = sorted(set(pow(u, kappa, p) for u in range(1, p)))
    # DP over k: reach[k] = dict value -> (prev value, y_k, nonzero_so_far)
    layer = {(0, False): None}
    hist = []
    for c in cs:
        new = {}
        for (v, nz) in layer:
            if (v, nz) not in new: new[(v, nz)] = ((v, nz), 0)
            for y in Pk:
                key = ((v + y * c) % p, True)
                if key not in new: new[key] = ((v, nz), y)
        hist.append(new); layer = new
    key = (eta % p, True)
    if key not in layer: return None
    ys = []
    for k in range(len(cs) - 1, -1, -1):
        prev, y = hist[k][key]; ys.append(y); key = prev
    ys.reverse()
    return [ctx.root(kappa, y) for y in ys]

PLANS = {}
def plan_for(ctx, kappa):
    if (ctx.p, kappa) not in PLANS:
        e, pl = e_table(ctx.F, kmax=kappa, prefer_hcd=True)
        PLANS[(ctx.p, kappa)] = (e, pl)
    return PLANS[(ctx.p, kappa)]

def arity_of(ctx, kappa, a):
    if kappa == 1: return a + 1
    e, pl = plan_for(ctx, kappa)
    pn = pl[kappa]
    if pn == 'S1t':
        return None
    s = int(pn.split('x')[0]); D = kappa // 2
    ND = arity_of(ctx, D, a)
    fin = pn.split('+')[1]
    if fin == 'F0': Nf = 1
    elif fin == 'F1': Nf = a + 1
    else: Nf = arity_of(ctx, int(fin[3:-1]), a)
    return None if ND is None or Nf is None else ND ** s * Nf

def solve(ctx, kappa, lams, stats):
    """lams: list of vectors (len = arity). Returns roots list."""
    p = ctx.p; n = len(lams)
    if kappa == 1:
        return nullvec(lams, p)
    e, pl = plan_for(ctx, kappa); pn = pl[kappa]
    s = int(pn.split('x')[0]); D = kappa // 2; fin = pn.split('+')[1]
    a = len(lams[0])
    ND = arity_of(ctx, D, a)
    q = int(ctx.F.pw[D])                       # element of class D mod kappa (g^D)
    eps = (-pow(q, p - 2, p)) % p
    # objects: (vector, cs, reps) where reps[k] = dict col -> root ; value of rep k = cs[k]*vector
    objs = [(lams[b], [1], [{b: 1}]) for b in range(n)]
    for stage in range(s):
        new = []
        for g0 in range(0, len(objs) - ND + 1, ND):
            grp = objs[g0:g0 + ND]
            if len(grp) < ND: break
            sig = to_list(solve(ctx, D, [o[0] for o in grp], stats), ND)
            x = [pow(si, D, p) for si in sig]
            I = [i for i in range(ND) if x[i] and ctx.cl(kappa, x[i]) == 0]
            J = [i for i in range(ND) if x[i] and ctx.cl(kappa, x[i]) == D]
            assert len(I) + len(J) == sum(1 for v in x if v), 'inner node not a {0,D}-node'
            if not J or not I:
                side = I if I else J
                mult = (lambda i: x[i]) if I else (lambda i: x[i] * pow(q, p - 2, p) % p)
                out = {}
                for i in side:
                    rt = ctx.root(kappa, mult(i))
                    for b, r in grp[i][2][0].items(): out[b] = rt * r % p
                stats['early'] += 1
                return out
            u = lin([x[i] if i in I else 0 for i in range(ND)], [o[0] for o in grp], p)
            cs = grp[0][1]; r = len(cs)
            reps = []
            for k in range(r):
                d = {}
                for i in I:
                    rt = ctx.root(kappa, x[i])
                    for b, rr in grp[i][2][k].items(): d[b] = rt * rr % p
                reps.append(d)
            for k in range(r):
                d = {}
                for i in J:
                    rt = ctx.root(kappa, x[i] * pow(q, p - 2, p) % p)
                    for b, rr in grp[i][2][k].items(): d[b] = rt * rr % p
                reps.append(d)
            new.append((u, cs + [c * eps % p for c in cs], reps))
        objs = new
    cs = objs[0][1]
    if fin == 'F0':
        ys = represent(ctx, kappa, cs, 0)
        o = objs[0]; out = {}
        for k, yr in enumerate(ys):
            if yr:
                for b, rr in o[2][k].items(): out[b] = yr * rr % p
        return out
    if fin == 'F1':
        Nf = a + 1; xs = nullvec([o[0] for o in objs[:Nf]], p); rho = 1
    else:
        Dp = int(fin[3:-1]); Nf = arity_of(ctx, Dp, a)
        sg = to_list(solve(ctx, Dp, [o[0] for o in objs[:Nf]], stats), Nf)
        xs = [pow(v, Dp, p) for v in sg]
        rho = None
        for rr in range(1, p):
            if all(represent_ok(ctx, kappa, cs, rr * v % p) for v in set(xs) if v):
                rho = rr; break
        assert rho is not None
    out = {}
    for nu, xv in enumerate(xs):
        if not xv: continue
        ys = represent(ctx, kappa, cs, rho * xv % p)
        assert ys is not None, 'Tn does not cover'
        for k, yr in enumerate(ys):
            if yr:
                for b, rr in objs[nu][2][k].items(): out[b] = yr * rr % p
    return out

_RC = {}
def represent_ok(ctx, kappa, cs, eta):
    key = (ctx.p, kappa, tuple(cs), eta)
    if key not in _RC: _RC[key] = represent(ctx, kappa, cs, eta) is not None
    return _RC[key]

def to_list(out, n):
    if isinstance(out, list): return out
    v = [0] * n
    for b, r in out.items(): v[b] = r
    return v

def verify(ctx, kappa, lams, roots):
    p = ctx.p
    if not any(roots): return False
    tot = lin([pow(r, kappa, p) for r in roots], lams, p)
    return all(t == 0 for t in tot)

def banks(ctx, kappa, a, n, rng):
    p = ctx.p
    def rv(): return [rng.randrange(p) for _ in range(a)]
    P = sorted(set(pow(u, kappa, p) for u in range(1, p)))
    yield 'uniform', [rv() for _ in range(n)]
    v = rv(); v[0] = v[0] or 1
    yield 'all-equal', [list(v) for _ in range(n)]
    E = [[int(i == j) for i in range(a)] for j in range(a)]
    # e_j times elements of one P-class (dead-like), cycling
    yield 'unit-P-classes', [[x * rng.choice(P) % p for x in E[b % a]] for b in range(n)]
    yield 'unit-same', [E[(b // max(1, n // a)) % a] for b in range(n)]
    yield 'zeros-mixed', [([0] * a if rng.random() < 0.3 else rv()) for _ in range(n)]
    base = [rv() for _ in range(2)]
    cls = rng.randrange(kappa)
    g = int(ctx.F.g)
    yield 'two-dirs-one-class', [[x * pow(g, cls, p) * rng.choice(P) % p for x in base[b % 2]] for b in range(n)]

if __name__ == '__main__':
    rng = random.Random(20261112)
    report = []
    cases = [(13, 4), (17, 4), (17, 8), (29, 4), (37, 6), (41, 4), (41, 8), (73, 8), (73, 6),
             (2521, 2), (2521, 4), (2521, 6), (2521, 8), (1801, 8), (31, 6), (61, 4)]
    for p, kappa in cases:
        ctx = Ctx(p)
        e, pl = plan_for(ctx, kappa)
        for a in (1, 2, 3):
            n = arity_of(ctx, kappa, a)
            if n is None or n > 6000:
                report.append((p, kappa, a, pl[kappa], n, 'skipped')); continue
            stats = {'early': 0}; ok = tot = 0
            for rep in range(3 if n > 1000 else 6):
                for name, lams in banks(ctx, kappa, a, n, rng):
                    out = to_list(solve(ctx, kappa, lams, stats), n)
                    tot += 1; ok += verify(ctx, kappa, lams, out)
            report.append((p, kappa, a, pl[kappa], e[kappa], n, f'{ok}/{tot}', stats['early']))
            print(report[-1], flush=True)
    json.dump(report, open(__file__.replace('.py', '.json'), 'w'), indent=0)
