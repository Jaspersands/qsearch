r"""Referee check of Corollary 41 (kappa = 8, p = 41): witnesses, sumsets, and an executor
built on an independent implementation of lem:app-s2-tensor (two-level tensor) and
lem:app-s2-witness / union-target variant.  Written from the appendix text, not the attack code.
"""
import sys, random, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from hcd_executor import nullvec, lin, Ctx, to_list, verify

p = 41; xi = 6
ctx = Ctx(p)
def ind(x, k):  # coset index w.r.t. coset generator xi: x in xi^m Q0
    h = (p - 1) // k; z = pow(xi, h, p); v = pow(x, h, p)
    return next(m for m in range(k) if pow(z, m, p) == v)
assert len({pow(xi, (p - 1) // 8 * m, p) for m in range(8)}) == 8   # xi is a coset generator for 8 (and 4)

# --- sumsets
P8 = sorted({pow(u, 8, p) for u in range(1, p)}); D = set(P8) | {0}
def sumset(A, B): return {(a + b) % p for a in A for b in B}
S2 = sumset(D, D); S3 = sumset(S2, D); S4 = sumset(S3, D)
print('P8 =', P8, ' -1 class (mod 8):', ind(p - 1, 8))
print('|2D| =', len(S2), ' classes of 2D\\0:', sorted({ind(x, 8) for x in S2 if x}))
print('3D == F \\ (-P8):', S3 == set(range(p)) - {(-x) % p for x in P8}, ' 4D == F:', S4 == set(range(p)))
# t(41,8): least t with zero sum of t nonzero 8th powers
Sk = set(P8); t = 1
while 0 not in Sk: Sk = sumset(Sk, P8); t += 1
print('t(41,8) =', t)
eps = (-pow(pow(6, 4, p), p - 2, p)) % p
print('eps = -6^{-4} =', eps, ' in P8:', eps in P8)
Tn = {(y1 + eps * y2) % p for y1 in D for y2 in D if (y1, y2) != (0, 0)}
print('Tn(1,eps) == 2D\\0 :', Tn == S2 - {0}, ' 0 in Tn:', 0 in Tn)

# --- witness 1: kappa=4 two-level contraction
a4 = (10, 7, 21, 24); b4 = (0, 1, 10, 9)
ok1 = all((a4[j] + b4[i]) % p and ind((a4[j] + b4[i]) % p, 4) == (-i - j) % 4 for i in range(4) for j in range(4))
print('kappa=4 contraction: all 16 alpha_j+beta_i nonzero in Q^{(4)}_{-i-j}:', ok1, ' C00 =', (a4[0] + b4[0]) % p)
# --- witness 2: kappa=8 union step to K={0,1,2,3}
a8 = (26, 30, 30, 27, 35, 25, 2, 2); b8 = (0, 0, 0, 1, 1, 1, 2, 2); K = {0, 1, 2, 3}
cells = {(i, j): (a8[j] + b8[i]) % p for i in range(8) for j in range(8)}
ok2 = all(v and (ind(v, 8) + i + j) % 8 in K for (i, j), v in cells.items())
print('kappa=8 union step: all 64 nonzero with class+i+j in K:', ok2,
      ' C00 =', cells[(0, 0)], 'class', ind(cells[(0, 0)], 8), '(in Q0?', ind(cells[(0, 0)], 8) == 0, ')')

# --- independent two-level tensor (lem:app-s2-tensor) returning node coefficients x_b
def tensor_node(k, alpha, beta, lams):
    """Return coefficients x (not roots) with sum x_b lam_b = 0, x_b = C_ij * omega'_b^k."""
    a = len(lams[0]); N = (k - 1) * a + 1; B = a + 1
    assert len(lams) >= B * N
    z = [pow(xi, m, p) for m in range(k)]
    T = []; cellsets = []
    for nu in range(N):
        blk = list(range(nu * B, (nu + 1) * B))
        c = nullvec([lams[b] for b in blk], p)
        bs = next(i for i in range(B) if c[i]); inv = pow(c[bs], p - 2, p); c = [ci * inv % p for ci in c]
        S = {i: [] for i in range(k)}  # class -> list of (b, omega)
        for t_, b in enumerate(blk):
            if c[t_]:
                i = ind(c[t_], k); om = ctx.root(k, c[t_] * pow(z[i], p - 2, p) % p)
                if t_ == bs: assert i == 0; om = 1
                S[i].append((b, om))
        Ti = [lin([pow(om, k, p) for _, om in S[i]], [lams[b] for b, _ in S[i]], p) if S[i] else [0] * a for i in range(k)]
        T.append(Ti); cellsets.append(S)
    V = [sum((T[nu][i] for i in range(1, k)), []) for nu in range(N)]
    eta = nullvec(V, p)
    ns = next(i for i in range(N) if eta[i]); inv = pow(eta[ns], p - 2, p); eta = [e * inv % p for e in eta]
    x = [0] * len(lams)
    for nu in range(N):
        if not eta[nu]: continue
        j = ind(eta[nu], k); vp = 1 if nu == ns else ctx.root(k, eta[nu] * pow(z[j], p - 2, p) % p)
        if nu == ns: assert j == 0
        for i in range(k):
            Cij = z[i] * z[j] * (alpha[j] + beta[i]) % p
            for b, om in cellsets[nu][i]:
                x[b] = Cij * pow(vp * om % p, k, p) % p
    assert any(x)
    assert all(v == 0 for v in lin(x, lams, p))
    return x

def cor41(lams):
    a = len(lams[0]); G = (a + 1) * (3 * a + 1); Nobj = (a + 1) * (7 * a + 1)
    n = G * Nobj; assert len(lams) == n
    objs = []
    for g in range(Nobj):
        idx = list(range(g * G, (g + 1) * G))
        x = tensor_node(4, a4, b4, [lams[b] for b in idx])     # coefficients in P_4 u 0
        I = [t for t in range(G) if x[t] and ind(x[t], 8) == 0]
        J = [t for t in range(G) if x[t] and ind(x[t], 8) == 4]
        assert len(I) + len(J) == sum(1 for v in x if v)
        q = pow(xi, 4, p)
        if not I or not J:
            out = [0] * n
            for t in (I or J):
                w = x[t] if I else x[t] * pow(q, p - 2, p) % p
                out[idx[t]] = ctx.root(8, w)
            return out, 'early'
        u = lin([x[t] if t in I else 0 for t in range(G)], [lams[b] for b in idx], p)
        rep1 = {idx[t]: ctx.root(8, x[t]) for t in I}
        rep2 = {idx[t]: ctx.root(8, x[t] * pow(q, p - 2, p) % p) for t in J}
        objs.append((u, rep1, rep2))
    epsl = (-pow(q, p - 2, p)) % p
    # check object values
    for u, r1, r2 in objs:
        v1 = lin([pow(r, 8, p) for r in r1.values()], [lams[b] for b in r1], p)
        v2 = lin([pow(r, 8, p) for r in r2.values()], [lams[b] for b in r2], p)
        assert v1 == u and v2 == [epsl * c % p for c in u]
    x = tensor_node(8, a8, b8, [o[0] for o in objs])          # classes in K
    out = [0] * n
    for nu, xv in enumerate(x):
        if not xv: continue
        y = next((y1, y2) for y1 in D for y2 in D if (y1, y2) != (0, 0) and (y1 + epsl * y2) % p == xv)
        for yk, rep in zip(y, objs[nu][1:]):
            if yk:
                ry = ctx.root(8, yk)
                for b, r in rep.items(): out[b] = ry * r % p
    return out, 'full'

rng = random.Random(41)
for a in (1, 2):
    G = (a + 1) * (3 * a + 1); Nobj = (a + 1) * (7 * a + 1); n = G * Nobj
    res = {'early': 0, 'full': 0}; ok = 0; tot = 0
    for trial in range(30):
        kind = trial % 3
        if kind == 0: lams = [[rng.randrange(p) for _ in range(a)] for _ in range(n)]
        elif kind == 1:
            E = [[int(i == j) for i in range(a)] for j in range(a)]
            lams = [[c * rng.choice(P8) % p for c in E[b % a]] for b in range(n)]
        else:
            v = [rng.randrange(1, p) for _ in range(a)]; lams = [list(v) for _ in range(n)]
        out, how = cor41(lams); res[how] += 1; tot += 1
        ok += verify(ctx, 8, lams, out)
    print(f'Cor 41 executor a={a}: arity {n}, verified {ok}/{tot}, paths {res}')
