"""End-to-end executor (falsifier) for the nodes of the fragment: Lemma R chains, Lemma S stages,
Lemma F finishes.  Written from the fragment's definitions; uses certificates from certs_stage1.json.
Every output is checked: x in (P_kappa u {0})^M, x != 0, sum x_b lambda_b = 0.  Finite checks only.
AI-written 2026-11-13, pending human review."""
import json, random, sys
from certs import prim_root, check_rc

def inv(x, p): return pow(x, p - 2, p)

def null_vector(cols, p):
    """nonzero c with sum c_k cols[k] = 0 (len(cols) > dim)."""
    n, a = len(cols), len(cols[0])
    M = [[cols[k][i] % p for k in range(n)] for i in range(a)]
    piv, r = [], 0
    for cidx in range(n):
        pr = next((i for i in range(r, a) if M[i][cidx]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][cidx], p); M[r] = [x * iv % p for x in M[r]]
        for i in range(a):
            if i != r and M[i][cidx]:
                f = M[i][cidx]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(cidx); r += 1
        if r == a: break
    free = next(cidx for cidx in range(n) if cidx not in piv)
    c = [0] * n; c[free] = 1
    for i, pc in enumerate(piv): c[pc] = (-M[i][free]) % p
    return c

class Ctx:
    def __init__(self, p, kappa):
        self.p, self.k = p, kappa; self.g = prim_root(p)
    def cls(self, x, D):
        z = pow(self.g, (self.p - 1) // D, self.p); y = pow(x, (self.p - 1) // D, self.p); t = 1
        for c in range(D):
            if t == y: return c
            t = t * z % self.p
        raise AssertionError
    def root(self, w):  # kappa-th root of w in P (brute force; small p only or via search)
        p, k = self.p, self.k
        if w == 0: return 0
        for r in range(1, p):
            if pow(r, k, p) == w: return r
        raise AssertionError('no root')

def value(rel, lam, p, a):
    v = [0] * a
    for b, c in rel.items():
        for i in range(a): v[i] = (v[i] + c * lam[b][i]) % p
    return v

def ge_node(ctx, lam, idx, a):
    """relation on columns idx (len a+1) with a coefficient 1."""
    c = null_vector([lam[b] for b in idx], ctx.p)
    k0 = next(i for i, x in enumerate(c) if x); f = inv(c[k0], ctx.p)
    return {idx[i]: x * f % ctx.p for i, x in enumerate(c) if x}

def refine(ctx, rels, lam, a, step):
    """Lemma R: rels = list of (r-1)a+1 relations with D-classes in R and a coefficient of class 0."""
    D, R, K, alpha, beta = step; p = ctx.p
    Rn = [i for i in R if i != 0]
    U = []
    for rel in rels:
        parts = {i: [0] * a for i in R}
        for b, c in rel.items():
            i = ctx.cls(c, D); assert i in R, ('input class outside R', i, R)
            for t in range(a): parts[i][t] = (parts[i][t] + c * lam[b][t]) % p
        U.append(parts)
    stacked = [sum((U[n][i] for i in Rn), []) for n in range(len(rels))]
    eta = null_vector(stacked, p) if Rn and a > 0 else [1] + [0] * (len(rels) - 1)
    ns = next(n for n, x in enumerate(eta) if x); f = inv(eta[ns], p); eta = [x * f % p for x in eta]
    out = {}
    for n, rel in enumerate(rels):
        if not eta[n]: continue
        j = ctx.cls(eta[n], D)
        for b, c in rel.items():
            v = eta[n] * (alpha[j] + beta[ctx.cls(c, D)]) % p * c % p
            if v: out[b] = v
    for b, c in out.items(): assert (ctx.cls(c, D) in K), 'output class outside K'
    assert any(ctx.cls(c, D) == 0 for c in out.values())
    return out

def chain(ctx, lam, cols, a, steps):
    """tower/union chain: GE then the steps; returns relation and the number of columns used."""
    rels = [ge_node(ctx, lam, cols[i:i + a + 1], a) for i in range(0, len(cols) - a, a + 1)]
    for st in steps:
        N = (len(st[1]) - 1) * a + 1
        rels = [refine(ctx, rels[i:i + N], lam, a, st) for i in range(0, len(rels) - N + 1, N)]
    return rels[0]

def arity(a, steps): 
    n = a + 1
    for st in steps: n *= (len(st[1]) - 1) * a + 1
    return n

def check_solution(ctx, rel, lam, a):
    p, k = ctx.p, ctx.k
    assert rel and all(ctx.cls(c, k) == 0 for c in rel.values()), 'not in P_kappa'
    assert value(rel, lam, p, a) == [0] * a, 'not a relation'
    return True

def step_from_cert(cert, D, R, K=None):
    al = cert['alpha']; be = {int(i): v for i, v in cert['beta'].items()}
    return (D, sorted(R), set(cert.get('K', K) or [0]), al, be)

def stage_finish_F1(ctx, lam, a, node_steps, m):
    """one stage over a {0,m}-chain node, then F1 (Gaussian elimination + y search), kappa = ctx.k."""
    p, k = ctx.p, ctx.k
    q = pow(ctx.g, m, p); eps = (-inv(q, p)) % p
    A = arity(a, node_steps)
    objs = []
    for o in range(a + 1):
        cols = list(range(o * A * (a + 1) // (a + 1) * 0 + o * A, (o + 1) * A))
        rel = chain(ctx, lam, cols, a, node_steps)
        I = {b: c for b, c in rel.items() if ctx.cls(c, k) == 0}
        J = {b: c * inv(q, p) % p for b, c in rel.items() if ctx.cls(c, k) == m}
        assert len(I) + len(J) == len(rel)
        if not J: return I, 'stage-solution'
        if not I: return J, 'stage-solution'
        objs.append((value(I, lam, p, a), I, J))
    eta = null_vector([o[0] for o in objs], p)
    P = [x for x in range(1, p) if ctx.cls(x, k) == 0]
    out = {}
    for n, (v, I, J) in enumerate(objs):
        if not eta[n]: continue
        y = None
        for y1 in [0] + P:
            z = (eta[n] - y1) * inv(eps, p) % p
            if z == 0 or ctx.cls(z, k) == 0:
                if y1 or z: y = (y1, z); break
        assert y, 'T_1 does not contain eta'
        for b, c in I.items():
            if y[0]: out[b] = (out.get(b, 0) + y[0] * c) % p
        for b, c in J.items():
            if y[1]: out[b] = (out.get(b, 0) + y[1] * c) % p
    return {b: c for b, c in out.items() if c}, 'F1'

def bank(kind, M, a, p, rng):
    if kind == 'uniform': return [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    if kind == 'repeated': base = [rng.randrange(p) for _ in range(a)]; return [list(base) for _ in range(M)]
    if kind == 'axis': return [[(1 if i == (b % a) else 0) for i in range(a)] for b in range(M)]
    if kind == 'zeros': return [[0] * a if b % 3 else [rng.randrange(p) for _ in range(a)] for b in range(M)]

if __name__ == '__main__':
    C = json.load(open('certs_stage1.json'))
    rng = random.Random(7); tot = ok = 0
    tests = []
    for p in (2521, 7561, 1171, 2017):    # kappa = 9 tower 3 -> 9 (p = 1 mod 9)
        if (p - 1) % 9: continue
        tl3 = C['two-level 3']['found'].get(str(p)); tw = C['tower (9;{0,3,6})']['found'].get(str(p))
        if tw is None: continue
        if tl3 is None:  # above T_exist(3): find one
            from certs import find_rc
            w = find_rc(p, 3, [0, 1, 2], [0]); tl3 = {'alpha': w[0], 'beta': {str(i): v for i, v in w[1].items()}}
        tests.append(('tower9', p, 9, [step_from_cert(tl3, 3, [0, 1, 2]), step_from_cert(tw, 9, [0, 3, 6])]))
    for p in (1021, 3001, 9901):         # kappa = 5 two-level
        c5 = C['two-level 5']['found'].get(str(p))
        if c5: tests.append(('TL5', p, 5, [step_from_cert(c5, 5, range(5))]))
    for p in (12601, 10501, 15121):      # kappa = 7 union step {0,m}, stage, F1  (p >= 9604)
        c7 = C['union (7;Z7->{0,m})']['found'].get(str(p))
        if c7: tests.append(('U7stage', p, 7, [step_from_cert(c7, 7, range(7))], c7['K'][1]))
    for t in tests:
        name, p, k = t[:3]; ctx = Ctx(p, k)
        for a in (1, 2, 3):
            for kind in ('uniform', 'repeated', 'axis', 'zeros'):
                for rep in range(3):
                    if name == 'U7stage':
                        A = arity(a, t[3]) * (a + 1)
                        lam = bank(kind, A, a, p, rng)
                        rel, how = stage_finish_F1(ctx, lam, a, t[3], t[4])
                    else:
                        A = arity(a, t[3]); lam = bank(kind, A, a, p, rng)
                        rel, how = chain(ctx, lam, list(range(A)), a, t[3]), 'chain'
                    tot += 1
                    if check_solution(ctx, rel, lam, a): ok += 1
        print(name, p, 'ok so far', ok, '/', tot, flush=True)
    print('ALL', ok, '/', tot)
