#!/opt/anaconda3/bin/python
"""Generic executor for multi-representation descent (MRD) plans, with exact verification.

Runs the plans printed by exponents_hcd.py / exponents_r7.py on concrete banks at small a and checks
every output: x in (P_kappa u 0)^M, x != 0, sum x_b lambda_b = 0.  Finite exact checks: they can only
falsify the constructions (Theorem HC, Proposition HC').
Solvers used inside plans:
  two-level (lem:app-s2-tensor + witness) at modulus kap' with an exhaustively found (alpha, beta)
  for target K (K = (0,) is a plain contraction); Gaussian elimination; and, where no two-level
  contraction exists (p in E_2(D)), a brute-force D-solver on D*a+1 columns (CW guarantees a solution).
"""
import sys, random, itertools, functools
ARGV = sys.argv[:]; sys.argv = sys.argv[:1]   # exponents.py parses argv at import
import exponents_hcd as H
sys.argv = ARGV

inv = lambda y, p: pow(y, p - 2, p)


def nullvec(vecs, dim, p):
    n = len(vecs)
    M = [[vecs[j][i] % p for j in range(n)] for i in range(dim)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, dim) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][c], p)
        M[r] = [y * iv % p for y in M[r]]
        for i in range(dim):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(y - f * z) % p for y, z in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == dim:
            break
    free = next(c for c in range(n) if c not in piv)
    x = [0] * n; x[free] = 1
    for i, c in enumerate(piv):
        x[c] = (-M[i][free]) % p
    return x


@functools.lru_cache(None)
def witness(p, k, K):
    """(alpha, beta) of a two-level union step RC(k; Z_k -> K), or None (exhaustive)."""
    g, ind = H.classes(p, k)
    allowed = lambda i, j: {0} | {x for x, e in ind.items() if e in {(m - i - j) % k for m in K}}
    A = [[allowed(i, j) for j in range(k)] for i in range(k)]
    X0 = [set(A[0][j]) for j in range(k)]; X0[0].discard(0)
    beta = [0] * k
    def rec(i, Xs):
        if i == k:
            return [min(x) for x in Xs]
        for b in range(p):
            Y = []
            for j in range(k):
                s = {x for x in Xs[j] if (x + b) % p in A[i][j]}
                if not s:
                    break
                Y.append(s)
            else:
                beta[i] = b
                r = rec(i + 1, Y)
                if r:
                    return r
        return None
    al = rec(1, X0)
    return None if al is None else (tuple(al), tuple(beta))


class Solver:
    """Returns nonzero x with sum x v = 0 and every nonzero x_b of class (mod kap) in K (classes w.r.t.
    the primitive root g); arity() columns in F_p^a."""
    def __init__(self, p, kap, K, a):
        self.p, self.kap, self.K, self.a = p, kap, K, a
        self.g, self.ind = H.classes(p, kap)
        w = witness(p, kap, K)
        if w is not None:
            al, be = w
            z = [pow(self.g, m, p) for m in range(kap)]
            self.C = [[z[i] * z[j] * (al[j] + be[i]) % p for j in range(kap)] for i in range(kap)]
            self.kind = 'two-level'
        else:
            assert K == (0,), 'brute force only for plain D-solvers'
            self.kind = 'brute'
    def arity(self):
        a = self.a
        return (a + 1) * ((self.kap - 1) * a + 1) if self.kind == 'two-level' else self.kap * a + 1
    def __call__(self, vecs):
        p, k, a = self.p, self.kap, self.a
        assert len(vecs) == self.arity()
        if self.kind == 'brute':
            vals = [0] + [x for x, e in self.ind.items() if e == 0]
            for x in itertools.product(vals, repeat=len(vecs)):
                if any(x) and all(sum(xi * v[i] for xi, v in zip(x, vecs)) % p == 0 for i in range(a)):
                    return list(x)
            raise AssertionError('CW violated?')
        B, N = a + 1, (k - 1) * a + 1
        z = [pow(self.g, m, p) for m in range(k)]
        blocks = []
        for nu in range(N):
            idx = list(range(nu * B, (nu + 1) * B))
            c = nullvec([vecs[b] for b in idx], a, p)
            bs = next(t for t in range(B) if c[t])
            c = [y * inv(c[bs], p) % p for y in c]
            cells = {}
            for t, b in enumerate(idx):
                if c[t]:
                    i = self.ind[c[t]]
                    cells.setdefault(i, []).append((b, c[t] * inv(z[i], p) % p))
            T = []
            for i in range(k):
                v = [0] * a
                for b, w in cells.get(i, []):
                    v = [(y + w * q) % p for y, q in zip(v, vecs[b])]
                T.append(v)
            blocks.append((cells, T))
        V = [sum((blocks[nu][1][i] for i in range(1, k)), []) for nu in range(N)]
        eta = nullvec(V, (k - 1) * a, p)
        ns = next(n for n in range(N) if eta[n])
        eta = [y * inv(eta[ns], p) % p for y in eta]
        x = [0] * len(vecs)
        for nu in range(N):
            if eta[nu]:
                j = self.ind[eta[nu]]
                vp = eta[nu] * inv(z[j], p) % p
                for i, lst in blocks[nu][0].items():
                    for b, w in lst:
                        x[b] = self.C[i][j] * vp * w % p
        return x


class Found(Exception):
    def __init__(self, x):
        self.x = x


def rep_table(p, k, ratios):
    """value -> nontrivial y in (P u 0)^len(ratios) with sum y_i c_i = value (exact DP)."""
    g, ind = H.classes(p, k)
    Pv = [x for x, e in ind.items() if e == 0]
    tab = {0: ((), False)}  # value -> (assignment, nontrivial)
    for c in ratios:
        new = {}
        for v, (asg, nt) in tab.items():
            for y in [0] + Pv:
                w = (v + y * c) % p
                cand = (asg + (y,), nt or y != 0)
                if w not in new or (cand[1] and not new[w][1]):
                    new[w] = cand
        tab = new
    return {v: asg for v, (asg, nt) in tab.items() if nt}


def run_plan(p, k, plan, lams, a):
    g, ind = H.classes(p, k)
    inP = lambda y: y != 0 and ind[y] == 0
    objs = [(list(l), [(1, {b: 1})]) for b, l in enumerate(lams)]
    stages, fin = [s for s in plan if s[0] in ('half', 'u')], plan[-1]
    def combine(group, x, m):
        zeta = pow(g, m, p)
        I = [n for n in range(len(group)) if x[n] and ind[x[n]] == 0]
        J = [n for n in range(len(group)) if x[n] and ind[x[n]] == m]
        assert len(I) + len(J) == sum(1 for y in x if y)
        def side(S, scale):
            out = []
            for kk in range(len(group[0][1])):
                rep = {}
                for n in S:
                    cf = x[n] * scale % p
                    for col, cc in group[n][1][kk][1].items():
                        rep[col] = cf * cc % p
                out.append(rep)
            return out
        if not I or not J:
            S, sc = (I, 1) if I else (J, inv(zeta, p))
            raise Found(side(S, sc)[0])
        u = [0] * a
        for n in I:
            u = [(y + x[n] * q) % p for y, q in zip(u, group[n][0])]
        eps = (-inv(zeta, p)) % p
        ratios = [r for r, _ in group[0][1]]
        reps = [(r, d) for r, d in zip(ratios, side(I, 1))] + [(r * eps % p, d) for r, d in zip(ratios, side(J, inv(zeta, p)))]
        return (u, reps)
    try:
        for st in stages:
            if st[0] == 'half':
                S = Solver(p, k // 2, (0,), a); m = k // 2
            else:
                S = Solver(p, k, (0, st[1]), a); m = st[1]
            A = S.arity()
            assert len(objs) % A == 0
            nxt = []
            for i in range(0, len(objs), A):
                grp = objs[i:i + A]
                x = S([o[0] for o in grp])
                nxt.append(combine(grp, x, m))
            objs = nxt
        for o in objs:
            if not any(o[0]):
                raise Found(o[1][0][1])
        ratios = [r for r, _ in objs[0][1]]
        tab = rep_table(p, k, ratios)
        if fin[0] == 'F0':
            y = tab[0]
            x = {}
            for yk, (r, d) in zip(y, objs[0][1]):
                if yk:
                    for col, cc in d.items():
                        x[col] = yk * cc % p
            raise Found(x)
        if fin[0] == 'F1':
            eta, rho = nullvec([o[0] for o in objs], a, p), 1
        elif fin[0] == 'F2':
            eta, rho = Solver(p, fin[1], (0,), a)([o[0] for o in objs]), pow(g, fin[2], p)
        else:
            eta, rho = Solver(p, k, fin[1], a)([o[0] for o in objs]), pow(g, fin[2], p)
        if fin[0] in ('F2', 'F3'):   # any offset rho with rho*eta_nu in Tn for all nu is valid
            rho = next(pow(g, c, p) for c in range(k)
                       if all(not e or pow(g, c, p) * e % p in tab for e in eta))
        x = {}
        for n, o in enumerate(objs):
            if eta[n]:
                y = tab[rho * eta[n] % p]
                for yk, (r, d) in zip(y, o[1]):
                    if yk:
                        for col, cc in d.items():
                            x[col] = yk * cc % p
        raise Found(x)
    except Found as F:
        xv = [0] * len(lams)
        for col, cc in F.x.items():
            xv[col] = cc
        return xv


def plan_arity(p, k, plan, a):
    A = 1
    for st in plan:
        if st[0] == 'half':
            A *= Solver(p, k // 2, (0,), a).arity()
        elif st[0] == 'u':
            A *= Solver(p, k, (0, st[1]), a).arity()
        elif st[0] == 'F1':
            A *= a + 1
        elif st[0] == 'F2':
            A *= Solver(p, st[1], (0,), a).arity()
        elif st[0] == 'F3':
            A *= Solver(p, k, st[1], a).arity()
    return A


def verify(x, lams, p, k, a):
    g, ind = H.classes(p, k)
    return any(x) and all(y == 0 or ind[y] == 0 for y in x) and \
        all(sum(y * l[i] for y, l in zip(x, lams)) % p == 0 for i in range(a))


def banks(p, a, n, rng):
    yield 'uniform', [[rng.randrange(p) for _ in range(a)] for _ in range(n)]
    yield 'all-e1', [[1] + [0] * (a - 1) for _ in range(n)]
    S = [[rng.randrange(p) for _ in range(a)] for _ in range(2)]
    yield 'two-values', [rng.choice(S) for _ in range(n)]
    g = H.X.primitive_root(p)
    yield 'coset-reps', [[pow(g, rng.randrange(p - 1), p) * (i == b % a) for i in range(a)] for b in range(n)]


if __name__ == '__main__':
    import ast
    rng = random.Random(11)
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    PLANS = [
        (41, 8, (('half', None), ('F3', (0, 1, 2, 3), 0))),
        (41, 8, (('half', None), ('half', None), ('F1',))),
        (41, 8, (('half', None), ('half', None), ('half', None), ('F0',))),
        (73, 8, (('half', None), ('F2', 4, 0))),
        (17, 8, (('half', None), ('F3', (0, 1, 4, 5), 0))),
        (89, 8, (('half', None), ('F2', 4, 0))),
        (31, 6, (('half', None), ('F3', (0, 1, 2), 0))),
        (19, 6, (('half', None), ('F2', 3, 0))),
        (43, 6, (('half', None), ('F2', 3, 0))),
        (13, 6, (('half', None), ('F2', 3, 0))),
        (67, 6, (('half', None), ('F2', 2, 0))),
        (13, 4, (('half', None), ('F2', 2, 0))),
        (5, 4, (('half', None), ('half', None), ('F1',))),
        (7, 6, (('half', None), ('half', None), ('F2', 2, 0))),
    ]
    if len(sys.argv) > 2:
        PLANS = [ast.literal_eval(sys.argv[2])]
    tot = ok = 0
    for p, k, plan in PLANS:
        # recompute the F-class offset c from the plan's own ratio set (plans from exponents_hcd use c = min class)
        for a in (1, 2):
            try:
                n = plan_arity(p, k, plan, a)
            except AssertionError as e:
                print(p, k, plan, 'a=%d' % a, 'SKIP', e); continue
            if n > 20000 or (a == 2 and any(Solver(p, k // 2, (0,), a).kind == 'brute' for st in plan if st[0] == 'half')):
                print(f'p={p} k={k} a={a} plan={plan}: arity {n}: NOT run (too large / brute force at a=2)')
                continue
            res = []
            for _ in range(trials):
                for name, L in banks(p, a, n, rng):
                    x = run_plan(p, k, plan, L, a)
                    good = verify(x, L, p, k, a)
                    tot += 1; ok += good; res.append(good)
            print(f'p={p} k={k} a={a} plan={plan} M={n}: {sum(res)}/{len(res)} verified', flush=True)
    print(f'TOTAL {ok}/{tot} verified')
