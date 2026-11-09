"""Independent implementation of threshold-7 Theorem 2.2 (nested triangular recursion through an
admissible chain), run end to end with exact arithmetic mod p.

Contractions: random beta (Proposition 4.1 design) with alpha_j chosen by a full scan of F_p, or
the complete DFS of rcdfs.c at small p.  Every contraction is re-checked with rc.check (pow).
Every output is checked with pow(): each weight is a kappa-th power, the weights form a nonzero
relation, at most C(a+L+1, L+1) columns are used, and after kappa-th roots and the Bezout
exponent of lem:app-s2-gcd(b), sum_b s_b^d lambda_b = 0 for a d with gcd(d, p-1) = kappa.
Usage: chain_solver.py   (runs the fixed test plan, output chain_solver.out)
"""
import random, math, sys
import numpy as np
from rc import primitive_root, is_prime, check, feasible

class Ctx:
    def __init__(self, p, g):
        self.p, self.g = p, g
        self.tab = {}
    def cls(self, x, D):
        if D not in self.tab:
            z = pow(self.g, (self.p - 1) // D, self.p); t = {}; y = 1
            for c in range(D): t[y] = c; y = y * z % self.p
            self.tab[D] = t
        return self.tab[D][pow(x % self.p, (self.p - 1) // D, self.p)]

# ---------- linear algebra mod p: reduced echelon bases ----------
def reduce(v, basis, p):
    v = list(v)
    for piv, b in basis:
        c = v[piv]
        if c: v = [(x - c * y) % p for x, y in zip(v, b)]
    return v

def add(basis, v, p):
    r = reduce(v, basis, p)
    piv = next(i for i, x in enumerate(r) if x)
    inv = pow(r[piv], p - 2, p); r = [x * inv % p for x in r]
    nb = []
    for q, b in basis:
        c = b[piv]
        nb.append((q, [(x - c * y) % p for x, y in zip(b, r)]) if c else (q, b))
    nb.append((piv, r))
    return nb

def nullvec(cols, p):
    """nonzero x with sum x_k cols[k] = 0 (cols are residues; len(cols) > rank)."""
    n = len(cols); a = len(cols[0])
    M = [[cols[k][i] for k in range(n)] for i in range(a)]
    piv_cols, row = [], 0
    for c in range(n):
        pr = next((r for r in range(row, a) if M[r][c]), None)
        if pr is None: continue
        M[row], M[pr] = M[pr], M[row]
        inv = pow(M[row][c], p - 2, p); M[row] = [x * inv % p for x in M[row]]
        for r in range(a):
            if r != row and M[r][c]:
                f = M[r][c]; M[r] = [(x - f * y) % p for x, y in zip(M[r], M[row])]
        piv_cols.append(c); row += 1
        if row == a: break
    free = next(c for c in range(n) if c not in piv_cols)
    x = [0] * n; x[free] = 1
    for r, c in enumerate(piv_cols): x[c] = (-M[r][free]) % p
    return x

def combo(w, lam, p, a):
    s = [0] * a
    for b, c in w.items():
        for i in range(a): s[i] = (s[i] + c * lam[b][i]) % p
    return s

class Solver:
    def __init__(self, ctx, a, steps, lam):
        self.c, self.a, self.steps, self.lam = ctx, a, steps, lam
        self.next = 0
    def fresh(self):
        b = self.next; self.next += 1
        assert b < len(self.lam), "ran out of columns"
        return b
    def P(self, t, V):
        p, a = self.c.p, self.a
        if t == 0:
            m = a - len(V)
            bs = [self.fresh() for _ in range(m + 1)]
            res = [reduce(self.lam[b], V, p) for b in bs]
            if m == 0:
                x = [1]
            else:
                x = nullvec(res, p)
            k0 = next(k for k in range(len(x)) if x[k]); inv = pow(x[k0], p - 2, p)
            w = {bs[k]: x[k] * inv % p for k in range(len(x)) if x[k]}
            return w, bs[k0]
        D, R, K, alpha, beta = self.steps[t - 1]
        Dprev, Kprev = (1, [0]) if t == 1 else (self.steps[t - 2][0], self.steps[t - 2][2])
        Vk = list(V); rounds = []
        while True:
            c, bst = self.P(t - 1, Vk)
            for b, x in c.items():
                assert self.c.cls(x, Dprev) in Kprev or Dprev == 1
            e = combo(c, self.lam, p, a)
            assert not any(reduce(e, Vk, p))
            ib = {b: self.c.cls(x, D) for b, x in c.items()}
            assert all(i in beta for i in ib.values()), "class outside R_t"
            v = combo({b: beta[ib[b]] * x % p for b, x in c.items()}, self.lam, p, a)
            if not any(reduce(v, Vk, p)):
                break
            rounds.append((c, ib, e, v, list(Vk)))
            Vk = add(Vk, v, p)
        # stop round
        w = {b: x * (alpha[0] + beta[ib[b]]) % p for b, x in c.items()}
        w = {b: x for b, x in w.items() if x}
        assert w.get(bst) == 1
        rho = [(x + y) % p for x, y in zip(e, v)]
        tau = [(-x) % p for x in rho]
        for (cc, ibb, ek, vk, Vb) in reversed(rounds):
            rt = reduce(tau, Vb, p); rv = reduce(vk, Vb, p)
            i0 = next(i for i, x in enumerate(rv) if x)
            zeta = rt[i0] * pow(rv[i0], p - 2, p) % p
            assert all((x - zeta * y) % p == 0 for x, y in zip(rt, rv))
            if zeta:
                n = self.c.cls(zeta, D)
                for b, x in cc.items():
                    val = zeta * x % p * (alpha[n] + beta[ibb[b]]) % p
                    if val: w[b] = val
                tau = [(x - zeta * (alpha[n] * y + z)) % p for x, y, z in zip(tau, ek, vk)]
            assert not any(reduce(tau, Vb, p))
        for b, x in w.items(): assert self.c.cls(x, D) in K
        assert not any(reduce(combo(w, self.lam, p, a), V, p))
        return w, bst

def kth_root_table(p, k):
    t = {}
    for y in range(1, p): t.setdefault(pow(y, k, p), y)
    return t

def run(ctx, kap, a, steps, lam, roots):
    p = ctx.p; L = len(steps); M = math.comb(a + L + 1, L + 1)
    lam = lam[:M]
    S = Solver(ctx, a, steps, lam)
    w, _ = S.P(L, [])
    assert S.next <= M and w
    for b, x in w.items(): assert x and pow(x, (p - 1) // kap, p) == 1
    assert not any(combo(w, lam, p, a))
    u = {b: roots[x] for b, x in w.items()}
    q = (p - 1) // kap
    dp = next(d for d in range(2, 10 ** 6) if math.gcd(d, q) == 1)
    d = kap * dp; assert math.gcd(d, p - 1) == kap
    tt = pow(dp, -1, q)
    s = {b: pow(x, tt, p) for b, x in u.items()}
    tot = [0] * a
    for b, x in s.items():
        sd = pow(x, d, p)
        for i in range(a): tot[i] = (tot[i] + sd * lam[b][i]) % p
    assert not any(tot) and any(s.values())
    return S.next, M, len(w)

def families(p, a, M, rng):
    v = [rng.randrange(p) for _ in range(a)]
    fam = {
        'random': [[rng.randrange(p) for _ in range(a)] for _ in range(M)],
        'zero': [[0] * a for _ in range(M)],
        'repeat': [list(v) for _ in range(M)],
        'units': [[1 if i == (b % a) else 0 for i in range(a)] for b in range(M)],
        'hyperplane': [[0] + [rng.randrange(p) for _ in range(a - 1)] for _ in range(M)],
        'rank1': [[rng.randrange(1, p) * x % p for x in v] for _ in range(M)] if True else None,
        'sparse': [[rng.randrange(p) if rng.random() < 0.3 else 0 for _ in range(a)] for _ in range(M)],
        'mixed': [([0] * a if b % 3 == 0 else ([1 if i == b % a else 0 for i in range(a)] if b % 3 == 1 else [rng.randrange(p) for _ in range(a)])) for b in range(M)],
    }
    return fam

def sample_pair(p, g, D, R, K, rng, tries=200):
    """random beta (beta_0 = 0), alpha_0 = 1, alpha_j by a full scan of F_p."""
    cls = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1): cls[x] = e % D; x = x * g % p
    Ks = set(k % D for k in K)
    okc = {m: np.array([(c >= 0 and ((c + m) % D) in Ks) for c in cls]) | (np.arange(p) == 0) for m in range(D)}
    xs = np.arange(p)
    for t in range(1, tries + 1):
        beta = {i: (rng.randrange(p) if i else 0) for i in R}
        alpha = [1] + [None] * (D - 1); good = True
        for i in R:
            if not okc[i % D][(1 + beta[i]) % p]: good = False
        for j in range(1, D):
            if not good: break
            m = np.ones(p, dtype=bool)
            for i in R: m &= okc[(i + j) % D][(xs + beta[i]) % p]
            nz = np.nonzero(m)[0]
            if len(nz) == 0: good = False
            else: alpha[j] = int(nz[rng.randrange(len(nz))])
        if good:
            assert check(p, g, D, R, K, alpha, beta)
            return alpha, beta, t
    raise RuntimeError("no pair found")

def dfs_pair(p, g, D, R, K):
    st, alpha, beta, n = feasible(p, D, R, K, g=g)
    assert st == 1, ("infeasible step", p, D, R, K)
    return alpha, beta

def chain_steps(spec):
    """spec: list of (D, K); R_t = pi^{-1}(K_{t-1})"""
    steps, Dp, Kp = [], 1, [0]
    for D, K in spec:
        R = [x for x in range(D) if (x % Dp) in Kp]
        steps.append((D, R, K)); Dp, Kp = D, K
    return steps

def primes_above(x, kap, n):
    out, p = [], int(x) + 1
    while len(out) < n:
        if p % kap == 1 and is_prime(p): out.append(p)
        p += 1
    return out

if __name__ == "__main__":
    rng = random.Random(20261105)
    plan = []
    # union chain Z_k -> {0,1,2} -> {0} just above Theta_2 (sampled pairs)
    for kap, th, n in [(5, 3781, 3), (7, 30824, 2)]:
        for p in primes_above(th, kap, n):
            plan.append((kap, p, [(kap, [0, 1, 2]), (kap, [0])], 'sample'))
    # chains at primes of E_2 (complete-DFS pairs), including L = 3, 4 and a mixed chain
    plan += [(5, 31, [(5, [0, 1]), (5, [0])], 'dfs'),
             (5, 181, [(5, [0, 1, 2]), (5, [0, 1]), (5, [0])], 'dfs'),
             (7, 113, [(7, [0, 1, 2]), (7, [0, 1]), (7, [0])], 'dfs'),
             (7, 43, [(7, [0, 2, 4]), (7, [0, 2]), (7, [0])], 'dfs'),
             (7, 43, [(7, [0, 3, 4, 5, 6]), (7, [0, 4]), (7, [0, 5]), (7, [0])], 'dfs'),
             (6, 67, [(2, [0]), (6, [0, 5]), (6, [0])], 'dfs'),
             (4, 17, [(2, [0]), (4, [0])], 'dfs')]
    total = 0
    for kap, p, spec, how in plan:
        g = primitive_root(p); ctx = Ctx(p, g)
        steps = []
        for (D, R, K) in chain_steps(spec):
            if how == 'sample':
                alpha, beta, tries = sample_pair(p, g, D, R, K, rng)
            else:
                alpha, beta = dfs_pair(p, g, D, R, K); tries = 0
            steps.append((D, R, K, alpha, beta))
        roots = kth_root_table(p, kap)
        L = len(steps)
        amax = 4 if L <= 2 else (3 if L == 3 else 2)
        nrun = 0
        for a in range(1, amax + 1):
            M = math.comb(a + L + 1, L + 1)
            for name, lam in families(p, a, M, rng).items():
                used, Mx, supp = run(ctx, kap, a, steps, lam, roots)
                nrun += 1
        total += nrun
        print("kappa=%d p=%d chain %s (%s pairs) L=%d: %d runs OK (a=1..%d, 8 column families, columns used <= C(a+L+1,L+1))" % (
            kap, p, " -> ".join("(%d,%s)" % (D, set(K)) for D, K in spec), how, L, nrun, amax), flush=True)
    print("total runs OK:", total)
