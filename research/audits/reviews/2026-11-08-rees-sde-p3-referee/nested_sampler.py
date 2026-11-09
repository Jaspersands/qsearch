"""Counterexample to Theorem 6(i) of 2026-11-08-rees-sde-p3.md (barrier n^2/3 for pieces with
<= 2 sampled dependencies, Model A, random instances).

Algorithm NEST (inside Model A, P = {}, tau = 0 only, F = first f unused columns):
  at codimension q: F = first f = ceil(1.5(q+2)) + s unused columns; draw uniform samples of
  D(F); keep a sample delta with q+2 <= |supp delta| (smallest such).  X = supp delta has
  rank <= q, so dim D(X) >= 2: draw a uniform sample delta' of D(X) outside <delta>.
  supp delta' is inside supp delta = X (pattern set inside T_1), so Theorem 4's eight class
  unions realize <h1, h2> (or give a zero-sum set).  Cost |X| ~ q + 2 for TWO dimensions.
  Unused columns F \\ X go back to the front of the pool (exactly as KOW).
KOW baseline: same harness, sparsest of all nonzero kernel combinations of the first q + r columns.
Every final witness is verified by direct summation.  Reports m_used = number of stream columns
ever pulled into the pool (= the m needed for this run)."""
import math, sys, itertools
import numpy as np

def rref(M):
    M = M.copy() % 3; rows, cols = M.shape; piv = []; r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        p = r + nz[0]
        if p != r: M[[r, p]] = M[[p, r]]
        M[r] = (M[r] * M[r, c]) % 3
        col = M[:, c].copy(); col[r] = 0
        M = (M - np.outer(col, M[r])) % 3
        piv.append(c); r += 1
        if r == rows: break
    return M[:r], piv

def kernel(M):
    """basis (as rows) of {x: M x = 0}, M is q x f."""
    q, f = M.shape
    R, piv = rref(M)
    free = [c for c in range(f) if c not in set(piv)]
    B = np.zeros((len(free), f), dtype=np.int64)
    for k, fc in enumerate(free):
        B[k, fc] = 1
        for i, pc in enumerate(piv): B[k, pc] = (-R[i, fc]) % 3
    return B

def rank(M):
    if M.shape[0] == 0 or M.shape[1] == 0: return 0
    return len(rref(M)[1])

def solve_in_span(gens, t):
    """coefficients c with sum c_i gens_i = t (gens independent), or None."""
    if not gens: return [] if not np.any(t % 3) else None
    G = np.array(gens, dtype=np.int64).T % 3  # n x k
    k = G.shape[1]
    A = np.hstack([G, (t % 3).reshape(-1, 1)])
    R, piv = rref(A)
    if k in piv: return None
    c = [0] * k
    for i, pc in enumerate(piv): c[pc] = int(R[i, k])
    return c

GADGET = {(0, 1): [(1, 1), (1, 2), (2, 2)], (0, 2): [(1, 2), (2, 1), (2, 2)], (1, 0): [(1, 0), (1, 1), (2, 0)],
          (1, 1): [(1, 0), (2, 0), (2, 1)], (1, 2): [(a, b) for a in (1, 2) for b in range(3)],
          (2, 0): [(1, 1), (2, 0), (2, 2)], (2, 1): [(2, 0), (2, 1), (2, 2)], (2, 2): [(1, 0), (1, 2), (2, 1)]}

class Run:
    def __init__(self, n, rng, mode):
        self.n, self.rng, self.mode = n, rng, mode
        self.stream = []      # actual vectors
        self.pool = []        # unused indices, ordered
        self.gens = []        # generators of realized subgroup, in order
        self.pieces = []      # (gen_slice, realizer dict alpha-tuple -> list of indices)
        self.Ubasis = np.zeros((0, n), dtype=np.int64)
        self.nest_rounds = 0; self.kow_rounds = 0; self.costs = []
    def pull(self, k):
        while len(self.pool) < k:
            self.stream.append(self.rng.integers(0, 3, self.n)); self.pool.append(len(self.stream) - 1)
    def quotient_map(self):
        """matrix P (q x n) with ker P = U."""
        if self.Ubasis.shape[0] == 0: return np.eye(self.n, dtype=np.int64)
        return kernel(self.Ubasis)  # rows y with y.u = 0 for all u in U  -> P v = 0 iff v in U^perp-perp = U
    def vec(self, idx): return self.stream[idx]
    def S(self, sel):
        return (np.sum([self.stream[i] for i in sel], axis=0) % 3) if sel else np.zeros(self.n, dtype=np.int64)
    def add_gens(self, gs, realizer):
        k0 = len(self.gens); self.gens += [g % 3 for g in gs]
        self.pieces.append(((k0, len(self.gens)), realizer))
        self.Ubasis = np.array(self.gens, dtype=np.int64)
    def finish(self, base_set):
        """base_set: nonempty list with sum in U; extend by realizers to a zero-sum set."""
        sol = list(base_set); t = (-self.S(base_set)) % 3
        for (a, b), real in reversed(self.pieces):
            c = solve_in_span(self.gens[:b], t)
            assert c is not None
            alpha = tuple(c[a:b])
            if any(alpha):
                sel = real[alpha]; sol += sel; t = (t - self.S(sel)) % 3
        assert not np.any(t), "backtrack failed"
        assert len(set(sol)) == len(sol) and len(sol) > 0
        assert not np.any(self.S(sol)), "witness does not sum to zero"
        return sol
    def kow_round(self, q, P):
        r = max(1, math.ceil(math.log(q + 1, 3) - 1e-12))
        self.pull(q + r); F = self.pool[:q + r]
        M = (P @ np.array([self.stream[i] for i in F]).T) % 3
        B = kernel(M); k = B.shape[0]
        if k <= 8:
            co = np.array([c for c in itertools.product(range(3), repeat=k) if any(c)])
        else:
            co = self.rng.integers(0, 3, (6561, k))
        C = (co @ B) % 3; w = np.count_nonzero(C, axis=1); w[w == 0] = 10**9
        d = C[int(np.argmin(w))]
        A = [F[i] for i in range(len(F)) if d[i] == 1]; Bs = [F[i] for i in range(len(F)) if d[i] == 2]
        self.kow_rounds += 1; self.costs.append((q, 1, len(A) + len(Bs)))
        used = set(A + Bs); self.pool = [i for i in self.pool if i not in used]
        if not Bs or not A: return self.finish(A or Bs)
        u = self.S(A)
        if not np.any((P @ u) % 3): return self.finish(A)
        self.add_gens([u], {(1,): A, (2,): A + Bs})
        return None
    def nest_round(self, q, P, extra=3, samples=400):
        f = math.ceil(1.5 * (q + 2)) + extra
        self.pull(f); F = self.pool[:f]
        Fv = np.array([self.stream[i] for i in F]).T
        M = (P @ Fv) % 3
        B = kernel(M); k = B.shape[0]
        co = self.rng.integers(0, 3, (samples, k)); C = (co @ B) % 3
        w = np.count_nonzero(C, axis=1)
        order = np.argsort(w); chosen = None
        for j in order:
            if w[j] < 3: continue
            S_ = np.nonzero(C[j])[0]
            if w[j] >= q + 2 or len(S_) - rank(M[:, S_]) >= 2:
                chosen = C[j]; break
        if chosen is None: return "fail"
        Xloc = np.nonzero(chosen)[0]; X = [F[i] for i in Xloc]
        BX = kernel(M[:, Xloc]); assert BX.shape[0] >= 2
        dl = chosen[Xloc]
        while True:  # uniform sample of D(X) outside <delta>
            dp = (self.rng.integers(0, 3, BX.shape[0]) @ BX) % 3
            if rank(np.vstack([dl, dp])) == 2: break
        cls = {}
        for i, col in enumerate(X): cls.setdefault((int(dl[i]), int(dp[i])), []).append(col)
        real = {al: [c for ab in GADGET[al] for c in cls.get(ab, [])] for al in GADGET}
        self.nest_rounds += 1; self.costs.append((q, 2, len(X)))
        used = set(X); self.pool = [i for i in self.pool if i not in used]
        h1, h2 = self.S(real[(1, 0)]), self.S(real[(0, 1)])
        for al, sel in real.items():  # Theorem 4 identities, checked numerically in the quotient
            assert not np.any((P @ (self.S(sel) - al[0] * h1 - al[1] * h2)) % 3), "gadget identity failed"
        for al, sel in real.items():
            if not np.any((P @ (al[0] * h1 + al[1] * h2)) % 3) and sel:
                return self.finish(sel)
        self.add_gens([h1, h2], real)
        return None
    def run(self):
        while True:
            q = self.n - len(self.gens)
            if q == 0:
                self.pull(1); c = self.pool.pop(0); return self.finish([c])
            P = self.quotient_map()
            for i in list(self.pool[:1]):
                pass
            if self.mode == "nest" and q >= 4:
                res = self.nest_round(q, P)
                if res == "fail": res = self.kow_round(q, P)
            else:
                res = self.kow_round(q, P)
            if res is not None: return res

if __name__ == "__main__":
    rng = np.random.default_rng(20261108)
    print("n  mode  m_used  m_used/n^2   rounds(nest,kow)   [n^2/4 = , n^2/3 = ]")
    for n in (30, 60, 90, 120):
        for mode in ("kow", "nest"):
            ms = []
            for rep in range(3 if n <= 90 else 2):
                R = Run(n, rng, mode); sol = R.run()
                ms.append(len(R.stream))
                info = (R.nest_rounds, R.kow_rounds)
            print(f"{n:4d} {mode:5s} {ms} {[round(m/n/n,4) for m in ms]} {info}   [{n*n/4:.0f}, {n*n/3:.0f}]")
        sys.stdout.flush()
    # per-round cost profile of one NEST run at n = 120
    R = Run(120, rng, "nest"); R.run()
    print("NEST n=120 per-round (q, dims gained, |X|) first 8:", R.costs[:8], " last 6:", R.costs[-6:])
    print("all witnesses verified by direct summation (assert in Run.finish)")
