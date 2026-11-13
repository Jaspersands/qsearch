"""End-to-end executor for Schedule 1H+ plans, written from fragment.tex lemmas
(lem:refine, cor:chain, rem:designated, lem:stage2, lem:finishK) and core lem:stage/lem:finish.
Executes the least-degree non-S1 candidate chosen by plus.py at each kappa, on label banks,
and checks every returned kappa-solution from scratch.  S1 (Lemma rounds) needs the imported
Ivanyos-Santha collision step and is not executed."""
import random, sys, json
from fp import least_primitive_root
from rc import RCSearch, check_rc
from plus import PlusDegrees, T_EXIST

class Ctx:
    def __init__(self, p, S, P):
        self.p = p; self.g = least_primitive_root(p)
        self.lg = {}; x = 1
        for i in range(p - 1): self.lg[x] = i; x = x * self.g % p
        self.S, self.P = S, P
        e, how = P.degrees(p, want_trace=True)
        self.e = e; self.plans = {}
        for k in e:
            if k == 1: continue
            c = [x for x in P.last_cands[(p, k)] if x[2][0] != "S1"]
            best = min(c, key=lambda x: x[0])
            self.plans[k] = best
    def cl(self, x, D): return self.lg[x % self.p] % D
    def inv(self, x): return pow(x, self.p - 2, self.p)
    def root(self, w, k):
        """k-th root of w in P_k (table root finding; stands in for Las Vegas root finding)."""
        L = self.lg[w % self.p]; assert L % k == 0
        return pow(self.g, L // k, self.p)
    def cert(self, D, R, K):
        st, c = self.S.status(self.p, D, list(R), list(K), rtrials=2000, exhaustive=self.p <= 600)
        assert st == "FOUND", (self.p, D, R, K, st)
        alpha, bl = c; beta = dict(zip(sorted(R), bl))
        ok, _ = check_rc(self.p, D, sorted(R), sorted(K), alpha, beta); assert ok
        return alpha, beta

def kernel_vec(ctx, M, ncols):
    """nonzero x with M x = 0 (M: list of rows), ncols > rank; first nonzero coord normalised to 1."""
    p = ctx.p
    A = [row[:] for row in M]; piv = []; r = 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if pr is None: continue
        A[r], A[pr] = A[pr], A[r]; iv = ctx.inv(A[r][c]); A[r] = [v * iv % p for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]; A[i] = [(vi - f * vr) % p for vi, vr in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = next(c for c in range(ncols) if c not in piv)
    x = [0] * ncols; x[free] = 1
    for i, c in enumerate(piv): x[c] = (-A[i][free]) % p
    f = next(v for v in x if v); fi = ctx.inv(f)
    return [v * fi % p for v in x]

def lincomb(ctx, ws, cols, a):
    s = [0] * a
    for w, v in zip(ws, cols):
        if w:
            for t in range(a): s[t] = (s[t] + w * v[t]) % ctx.p
    return s

# ---------------- nodes: run(cols) -> w (a K-relation at modulus D with a coefficient 1)
class GE:
    D = 1; K = frozenset({0})
    def __init__(self, ctx): self.ctx = ctx
    def arity(self, a): return a + 1
    def run(self, cols, a):
        n = a + 1; M = [[cols[b][t] for b in range(n)] for t in range(a)]
        return kernel_vec(self.ctx, M, n) + [0] * (len(cols) - n)

class SolverNode:
    def __init__(self, ctx, k): self.ctx = ctx; self.k = k; self.D = k; self.K = frozenset({0}); self.sol = make_solver(ctx, k)
    def arity(self, a): return self.sol.arity(a)
    def run(self, cols, a):
        w, r = self.sol.run(cols, a)
        f = next(x for x in w if x); fi = self.ctx.inv(f)       # rem:designated scaling by P_D element
        return [x * fi % self.ctx.p for x in w]

class Refine:
    """Lemma lem:refine."""
    def __init__(self, ctx, inner, D, R, K):
        self.ctx, self.inner, self.D, self.R, self.K = ctx, inner, D, tuple(sorted(R)), frozenset(K)
        assert D % inner.D == 0
        assert set(self.R) >= {x for x in range(D) if x % inner.D in inner.K}
        self.alpha, self.beta = ctx.cert(D, self.R, sorted(K))
    def arity(self, a): return self.inner.arity(a) * ((len(self.R) - 1) * a + 1)
    def run(self, cols, a):
        ctx, p, D = self.ctx, self.ctx.p, self.D
        N = self.inner.arity(a); n = (len(self.R) - 1) * a + 1
        cs = [self.inner.run(cols[nu * N:(nu + 1) * N], a) for nu in range(n)]
        Rn0 = [i for i in self.R if i != 0]
        U = []
        for nu in range(n):
            Ui = {i: [0] * a for i in self.R}
            for b, c in enumerate(cs[nu]):
                if c:
                    i = ctx.cl(c, D); assert i in self.R
                    for t in range(a): Ui[i][t] = (Ui[i][t] + c * cols[nu * N + b][t]) % p
            U.append(Ui)
        M = [[U[nu][i][t] for nu in range(n)] for i in Rn0 for t in range(a)]
        eta = kernel_vec(ctx, M, n) if M else [1] + [0] * (n - 1)
        w = [0] * len(cols)
        for nu in range(n):
            if not eta[nu]: continue
            j = ctx.cl(eta[nu], D)
            for b, c in enumerate(cs[nu]):
                if c:
                    i = ctx.cl(c, D)
                    w[nu * N + b] = eta[nu] * (self.alpha[j] + self.beta[i]) % p * c % p
        s = (self.alpha[0] + self.beta[0]) % p; si = ctx.inv(s)     # designated -> 1
        return [x * si % p for x in w]

def make_node(ctx, pl):
    if pl[0] == "GE": return GE(ctx)
    if pl[0] == "H": return GE(ctx) if pl[1] == 1 else SolverNode(ctx, pl[1])
    if pl[0] == "chain":
        node = make_node(ctx, pl[1])
        for (D, R, K) in pl[2]: node = Refine(ctx, node, D, R, K)
        return node
    raise ValueError(pl)

# ---------------- solvers: run(cols) -> (w, r) a kappa-solution
class NodeSolver:
    """{0}-node at modulus k followed by k-th roots (Cor. cor:chain last sentence)."""
    def __init__(self, ctx, k, node): self.ctx, self.k, self.node = ctx, k, node; assert node.D == k and node.K == frozenset({0})
    def arity(self, a): return self.node.arity(a)
    def run(self, cols, a):
        w = self.node.run(cols, a)
        return w, [self.ctx.root(x, self.k) if x else 0 for x in w]

def realize(ctx, k, eps, j, t):
    """y in (P u {0})^{2^j}, y != 0, sum y_l c^{(j)}_l = t (t may be 0), or None. Direct search."""
    p = ctx.p
    inP = lambda x: x % p != 0 and ctx.cl(x, k) == 0
    if j == 0: return [t % p] if inP(t) else None
    y = realize(ctx, k, eps, j - 1, t)
    if y is not None: return y + [0] * len(y)
    ei = ctx.inv(eps)
    y = realize(ctx, k, eps, j - 1, t * ei)
    if y is not None: return [0] * len(y) + y
    for al in range(1, p):
        y1 = realize(ctx, k, eps, j - 1, al)
        if y1 is None: continue
        y2 = realize(ctx, k, eps, j - 1, (t - al) * ei)
        if y2 is not None and any(y2): return y1 + y2
    return None

class StagePlan:
    """Lemmas lem:stage2 / lem:stage, then lem:finish(i) (F0) or lem:finishK (F_K)."""
    def __init__(self, ctx, k, spl, m, s, fin):
        self.ctx, self.k, self.m, self.s = ctx, k, m, s
        self.N = make_node(ctx, spl)
        # the stage node must be a {0,m}-node at modulus k (an H_{k/2} solver qualifies with m = k/2)
        if isinstance(self.N, GE): assert k == 2 and m == 1
        else: assert {x % k for x in range(k) if x % self.N.D in self.N.K} == {0, m}, (self.N.D, self.N.K, m)
        self.q = pow(ctx.g, m, ctx.p); self.eps = (-ctx.inv(self.q)) % ctx.p
        self.fin = fin
        if fin[0] == "FK":
            self.Kn = make_node(ctx, fin[2]); self.Kset = frozenset(fin[1])
    def nF(self, a): return 1 if self.fin[0] == "F0" else self.Kn.arity(a)
    def arity(self, a): return self.N.arity(a) ** self.s * self.nF(a)
    def run(self, cols, a):
        ctx, p, k = self.ctx, self.ctx.p, self.k
        AN = self.N.arity(a); blk = AN ** self.s
        objs = []; ctype = [1]
        for B in range(self.nF(a)):
            level = [(cols[B * blk + b], [{B * blk + b: (1, 1)}]) for b in range(blk)]
            ctype = [1]
            for j in range(self.s):
                nxt = []
                for g0 in range(0, len(level), AN):
                    grp = level[g0:g0 + AN]
                    x = self.N.run([o[0] for o in grp], a)
                    I = [nu for nu in range(AN) if x[nu] and ctx.cl(x[nu], k) == 0]
                    J = [nu for nu in range(AN) if x[nu] and ctx.cl(x[nu], k) == self.m]
                    assert len(I) + len(J) == sum(1 for v in x if v) and I
                    if not J:
                        bump(f"k{k}:stage-early-exit")
                        sol = {}
                        for nu in I:
                            rho = ctx.root(x[nu], k)
                            for b, (wb, rb) in grp[nu][1][0].items(): sol[b] = (x[nu] * wb % p, rho * rb % p)
                        return self.emit(sol, len(cols))
                    bump(f"k{k}:stage-object")
                    u = lincomb(ctx, [x[nu] for nu in I], [grp[nu][0] for nu in I], a)
                    reps = []
                    for which, sc in ((I, lambda nu: x[nu]), (J, lambda nu: x[nu] * ctx.inv(self.q) % p)):
                        for kk in range(len(ctype)):
                            rep = {}
                            for nu in which:
                                xs = sc(nu); rho = ctx.root(xs, k)
                                for b, (wb, rb) in grp[nu][1][kk].items():
                                    assert b not in rep; rep[b] = (xs * wb % p, rho * rb % p)
                            reps.append(rep)
                    nxt.append((u, reps))
                level = nxt; ctype = ctype + [self.eps * c % p for c in ctype]
            assert len(level) == 1
            objs.append(level[0])
        bump(f"k{k}:finish-{self.fin[0]}")
        if self.fin[0] == "F0":
            y = realize(ctx, k, self.eps, self.s, 0); assert y is not None and any(y)
            return self.emit(self.combine(objs[0], y), len(cols))
        eta = self.Kn.run([o[0] for o in objs], a)
        for v in eta:
            if v: assert (ctx.cl(v, k) if self.Kn.D > 1 else 0) in self.Kset or self.Kn.D == 1
        u = next(u for u in range(k) if all((u + x) % k in self.Tcls(len(ctype)) for x in self.Kset))
        xu = pow(ctx.g, u, p); sol = {}
        for nu, o in enumerate(objs):
            if not eta[nu]: continue
            y = realize(ctx, k, self.eps, self.s, xu * eta[nu] % p); assert y is not None
            for b, wr in self.combine(o, y).items(): assert b not in sol; sol[b] = wr
        return self.emit(sol, len(cols))
    def Tcls(self, L):
        ctx = self.ctx
        return {c for c in range(self.k) if realize(ctx, self.k, self.eps, self.s, pow(ctx.g, c, ctx.p)) is not None}
    def combine(self, o, y):
        ctx, p, k = self.ctx, self.ctx.p, self.k; sol = {}
        for kk, yk in enumerate(y):
            if not yk: continue
            rho = ctx.root(yk, k)
            for b, (wb, rb) in o[1][kk].items(): assert b not in sol; sol[b] = (yk * wb % p, rho * rb % p)
        return sol
    def emit(self, sol, M):
        w = [0] * M; r = [0] * M
        for b, (wb, rb) in sol.items(): w[b] = wb; r[b] = rb
        return w, r

_SOLVERS = {}
STATS = {}
def bump(k): STATS[k] = STATS.get(k, 0) + 1
def make_solver(ctx, k):
    key = (ctx.p, k)
    if key in _SOLVERS: return _SOLVERS[key]
    if k == 1:
        class GES:
            def arity(s, a): return a + 1
            def run(s, cols, a): w = GE(ctx).run(cols, a); return w, w
        sol = GES()
    else:
        deg, desc, pl = ctx.plans[k]
        if pl[0] == "chain": sol = NodeSolver(ctx, k, make_node(ctx, pl))
        elif pl[0] == "stage": sol = StagePlan(ctx, k, pl[1], pl[2], pl[3], pl[4])
        else: raise ValueError(pl)
    _SOLVERS[key] = sol; return sol

def check_solution(ctx, k, cols, w, r, a):
    p = ctx.p
    assert len(w) == len(cols) and any(w), "zero or wrong length"
    for wb, rb in zip(w, r):
        if wb: assert pow(rb, k, p) == wb % p, "root"
        else: assert rb == 0
    assert lincomb(ctx, w, cols, a) == [0] * a, "relation"
    return True

def banks(ctx, M, a, rng):
    p = ctx.p; g = ctx.g
    yield "uniform", [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    yield "zero", [[0] * a for _ in range(M)]
    v = [rng.randrange(1, p) for _ in range(a)]
    yield "constant", [v[:] for _ in range(M)]
    for cls in range(1, 4):
        sc = lambda: pow(g, cls + 9 * rng.randrange(p), p)   # scalars in one coset of P_9 (if 9|p-1)
        yield f"rank1-coset{cls}", [[sc() * vt % p for vt in v] for _ in range(M)]
    yield "e1e2-blocks", [[1 if t == (b * a) // M else 0 for t in range(a)] for b in range(M)]
    yield "sparse01", [[rng.choice([0, 0, 0, 1]) for _ in range(a)] for _ in range(M)]
    yield "zero-interleaved", [[rng.randrange(p) for _ in range(a)] if b % 3 == 0 else [0] * a for b in range(M)]
    yield "pm1", [[rng.choice([1, p - 1]) for _ in range(a)] for _ in range(M)]

if __name__ == "__main__":
    S = RCSearch("rc_cache.json"); P = PlusDegrees(S)
    jobs = [tuple(map(int, x.split(":"))) for x in sys.argv[1:]]   # p:k:a:reps
    for (p, k, a, reps) in jobs:
        ctx = Ctx(p, S, P); _SOLVERS.clear()
        sol = make_solver(ctx, k); M = sol.arity(a)
        deg, desc, pl = ctx.plans[k]
        rng = random.Random(1000 * p + 10 * k + a); n_ok = 0; n = 0
        for rep in range(reps):
            for name, cols in banks(ctx, M, a, rng):
                w, r = sol.run(cols, a); check_solution(ctx, k, cols, w, r, a); n_ok += 1; n += 1
        st = dict(sorted(STATS.items())); STATS.clear()
        print(f"p={p} k={k} a={a} plan_deg={deg} e+={ctx.e[k]} arity={M} plan={desc} : {n_ok}/{n} banks OK {st}", flush=True)
