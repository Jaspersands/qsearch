"""WNEST: worst-case F_3^n subset sum with m = n^2/4 + O(n^{3/2}) columns (deterministic).

Independent re-derivation of the referee's NEST (2026-11-08-rees-sde-p3-referee.md, section 3a)
plus the two ingredients that make it worst-case:
  (1) PEEL: in the pool F, delete coloops and series classes of size >= 3 until the dependency
      code D(F*) has dual distance >= 3 (no coloop, no series pair of size >= 3).  Deleting a
      series class of size a drops the rank by >= a-1, so N - 1.5*rank never decreases.
  (2) MOMENT: for a code with dual distance >= 3 the weight has mean 2N*/3 and variance
      (2/9) sum_c a_c^2 <= 4N*/9 (a_c = series class sizes, all <= 2).  The method of
      conditional expectations gives a codeword delta with |wt - 2N*/3| <= sigma deterministically.
  Then wt(delta) >= rank(F*) + 2, so X = supp(delta) has dim D(X) >= 2, and the nested-support
  gadget (Theorem 4 of the pass, re-derived in gadget()) realizes 2 dimensions at cost
  |X| <= 2N/3 + O(sqrt N) = q + O(sqrt q).
Every final witness is verified by direct summation over the ORIGINAL vectors.
Interpreter: /opt/anaconda3/bin/python.  No files written except by the caller.
"""
import math, sys, itertools
import numpy as np

# ---------------------------------------------------------------- F_3 linear algebra
def rref(M):
    M = np.array(M, dtype=np.int64) % 3
    rows, cols = M.shape
    piv = []
    r = 0
    for c in range(cols):
        if r == rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        p = r + nz[0]
        if p != r:
            M[[r, p]] = M[[p, r]]
        M[r] = (M[r] * M[r, c]) % 3          # inverse of 1 is 1, of 2 is 2
        col = M[:, c].copy()
        col[r] = 0
        M = (M - np.outer(col, M[r])) % 3
        piv.append(c)
        r += 1
    return M[:r], piv

def rank(M):
    M = np.asarray(M)
    if M.size == 0:
        return 0
    return len(rref(M)[1])

def kernel(M):
    """rows = basis of {x : M x = 0 mod 3}; M is q x N."""
    M = np.asarray(M, dtype=np.int64)
    q, N = M.shape
    if q == 0:
        return np.eye(N, dtype=np.int64)
    R, piv = rref(M)
    pivset = set(piv)
    free = [c for c in range(N) if c not in pivset]
    B = np.zeros((len(free), N), dtype=np.int64)
    for k, fc in enumerate(free):
        B[k, fc] = 1
        for i, pc in enumerate(piv):
            B[k, pc] = (-R[i, fc]) % 3
    return B

def solve_in_span(gens, t):
    """coefficients c with sum c_i gens_i = t (gens independent rows) or None."""
    if len(gens) == 0:
        return [] if not np.any(np.asarray(t) % 3) else None
    G = np.array(gens, dtype=np.int64).T % 3
    k = G.shape[1]
    A = np.hstack([G, (np.asarray(t) % 3).reshape(-1, 1)])
    R, piv = rref(A)
    if k in piv:
        return None
    c = [0] * k
    for i, pc in enumerate(piv):
        c[pc] = int(R[i, k])
    return c

# ---------------------------------------------------------------- PEEL
def canon_key(v):
    """projective canonical form of a nonzero F_3 vector: scale so first nonzero entry is 1."""
    nz = np.nonzero(v)[0]
    if len(nz) == 0:
        return None, 0
    s = int(v[nz[0]])                 # 1 or 2; multiply by s (= inverse) to make it 1
    return tuple(((v * s) % 3).tolist()), s

def peel(M):
    """M: q x N columns (current quotient).  Returns (idx, B) with idx the surviving column
    positions and B a basis (rows) of D(F*) restricted to idx, such that D(F*) has no coloop and
    no series class of size >= 3.  Invariant: len(idx) - 1.5*rank(F*) >= N - 1.5*rank(F)."""
    idx = list(range(M.shape[1]))
    while True:
        sub = M[:, idx]
        B = kernel(sub)                               # k x |idx|
        if B.shape[0] == 0:
            return idx, B
        # coloops: zero columns of B
        zero = [j for j in range(len(idx)) if not np.any(B[:, j])]
        if zero:
            zs = set(zero)
            idx = [c for j, c in enumerate(idx) if j not in zs]
            continue
        classes = {}
        for j in range(len(idx)):
            key, _ = canon_key(B[:, j])
            classes.setdefault(key, []).append(j)
        big = [cl for cl in classes.values() if len(cl) >= 3]
        if not big:
            return idx, B
        cl = max(big, key=len)                        # peel the largest series class
        cs = set(cl)
        idx = [c for j, c in enumerate(idx) if j not in cs]

def series_class_sizes(B):
    classes = {}
    for j in range(B.shape[1]):
        key, _ = canon_key(B[:, j])
        classes.setdefault(key, []).append(j)
    return sorted((len(c) for c in classes.values()), reverse=True)

# ---------------------------------------------------------------- MOMENT (deterministic codeword)
def second_moment(B, x_prefix):
    """E[(wt - 2N/3)^2] for delta = x B with x_1..x_j fixed (prefix) and the rest uniform.
    Exact: coordinates group by the projective class of their remaining linear form; classes
    are pairwise independent and centred, so only within-class covariances survive."""
    k, N = B.shape
    j = len(x_prefix)
    c = (np.array(x_prefix, dtype=np.int64) @ B[:j]) % 3 if j else np.zeros(N, dtype=np.int64)
    G = B[j:]                                         # remaining forms, (k-j) x N
    det = 0.0
    groups = {}
    for i in range(N):
        g = G[:, i] if G.shape[0] else np.zeros(0, dtype=np.int64)
        key, s = canon_key(g)
        if key is None:
            det += (1.0 if c[i] % 3 else 0.0) - 2.0 / 3.0
        else:
            groups.setdefault(key, []).append((int(c[i]), s))
    tot = det * det
    for members in groups.values():
        acc = 0.0
        for t in range(3):
            w = 0.0
            for (ci, s) in members:
                w += (1.0 if (ci + s * t) % 3 else 0.0) - 2.0 / 3.0
            acc += w * w
        tot += acc / 3.0
    return tot

def pick_codeword(B):
    """Deterministic x with (wt(xB) - 2N/3)^2 <= E[(wt - 2N/3)^2] (conditional expectations)."""
    k, N = B.shape
    sigma2 = second_moment(B, [])
    prefix = []
    for j in range(k):
        best = None
        for v in range(3):
            val = second_moment(B, prefix + [v])
            if best is None or val < best[0] - 1e-12:
                best = (val, v)
        prefix.append(best[1])
    delta = (np.array(prefix, dtype=np.int64) @ B) % 3
    wt = int(np.count_nonzero(delta))
    assert (wt - 2.0 * N / 3.0) ** 2 <= sigma2 + 1e-6, (wt, N, sigma2)
    return delta, wt, math.sqrt(sigma2)

# ---------------------------------------------------------------- the nested-support gadget (Theorem 4)
UNIONS = {(0, 1): [(1, 1), (1, 2), (2, 2)], (0, 2): [(1, 2), (2, 1), (2, 2)],
          (1, 0): [(1, 0), (1, 1), (2, 0)], (1, 1): [(1, 0), (2, 0), (2, 1)],
          (1, 2): [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
          (2, 0): [(1, 1), (2, 0), (2, 2)], (2, 1): [(2, 0), (2, 1), (2, 2)],
          (2, 2): [(1, 0), (1, 2), (2, 1)]}

def gadget_symbolic_check():
    """Re-derive Theorem 4: each union sum equals a1*h1 + a2*h2 modulo the two relations,
    as an identity in the six symbols w_ab.  Returns True iff all eight hold and h1, h2 are
    independent modulo the relations."""
    sym = [(a, b) for a in (1, 2) for b in range(3)]
    def vec(classes):
        return np.array([1 if s in classes else 0 for s in sym], dtype=np.int64)
    rel1 = np.array([1 if a == 1 else 2 for (a, b) in sym], dtype=np.int64)       # sum delta_i v_i
    rel2 = np.array([b for (a, b) in sym], dtype=np.int64)                         # sum delta'_i v_i
    h1, h2 = vec(UNIONS[(1, 0)]), vec(UNIONS[(0, 1)])
    R = np.vstack([rel1, rel2])
    ok = True
    for al, cls in UNIONS.items():
        diff = (vec(cls) - al[0] * h1 - al[1] * h2) % 3
        ok &= rank(np.vstack([R, diff])) == rank(R)
    indep = rank(np.vstack([R, h1, h2])) == rank(R) + 2
    return ok and indep

# ---------------------------------------------------------------- the solver
def pool_size(q):
    """smallest N with N - 1.5 q >= 3 + sqrt(N)  (then after peeling mu - sigma >= r* + 2)."""
    N = int(math.ceil(1.5 * q)) + 3
    while N - 1.5 * q < 3 + math.sqrt(N):
        N += 1
    return N

class Run:
    """Stream of columns (list of vectors) consumed from the front, as in KOW.  Realized
    subgroup kept as a list of generators with realizers; finish() unwinds Lemma 1."""
    def __init__(self, n, stream_fn, mode="wnest", check=True, rng=None, samples=300):
        self.n = n
        self.rng = rng
        self.samples = samples
        self.stream_fn = stream_fn       # i -> vector (np.int64 of length n) or None if exhausted
        self.stream = []
        self.pool = []
        self.gens = []
        self.pieces = []
        self.mode = mode
        self.check = check
        self.costs = []                  # (q, dims gained, |X|, N, N*, r*, wt bounds)
        self.failed = False
    def pull(self, k):
        while len(self.pool) < k:
            v = self.stream_fn(len(self.stream))
            if v is None:
                return False
            self.stream.append(np.asarray(v, dtype=np.int64) % 3)
            self.pool.append(len(self.stream) - 1)
        return True
    def S(self, sel):
        return (np.sum([self.stream[i] for i in sel], axis=0) % 3) if sel else np.zeros(self.n, dtype=np.int64)
    def quotient_map(self):
        if not self.gens:
            return np.eye(self.n, dtype=np.int64)
        return kernel(np.array(self.gens, dtype=np.int64))      # rows y with y.u = 0 on U; P v = 0 iff v in U
    def add_gens(self, gs, realizer):
        k0 = len(self.gens)
        self.gens += [g % 3 for g in gs]
        self.pieces.append(((k0, len(self.gens)), realizer))
    def finish(self, base):
        sol = list(base)
        t = (-self.S(base)) % 3
        for (a, b), real in reversed(self.pieces):
            c = solve_in_span(self.gens[:b], t)
            assert c is not None
            alpha = tuple(c[a:b])
            if any(alpha):
                sel = real[alpha]
                sol += sel
                t = (t - self.S(sel)) % 3
        assert not np.any(t)
        assert len(set(sol)) == len(sol) and len(sol) > 0
        assert not np.any(self.S(sol)), "witness does not sum to zero"
        return sol
    # -- KOW round (baseline): sparsest nonzero combination of the first q + r columns
    def kow_round(self, q, P, rng=None):
        r = max(1, math.ceil(math.log(q + 1, 3) - 1e-12))
        if not self.pull(q + r):
            self.failed = True
            return "exhausted"
        F = self.pool[:q + r]
        M = (P @ np.array([self.stream[i] for i in F]).T) % 3
        B = kernel(M)
        k = B.shape[0]
        if k <= 8:
            co = np.array([c for c in itertools.product(range(3), repeat=k) if any(c)])
        else:
            co = (rng or np.random.default_rng(0)).integers(0, 3, (6561, k))
        C = (co @ B) % 3
        w = np.count_nonzero(C, axis=1)
        w[w == 0] = 10 ** 9
        d = C[int(np.argmin(w))]
        A = [F[i] for i in range(len(F)) if d[i] == 1]
        Bs = [F[i] for i in range(len(F)) if d[i] == 2]
        self.costs.append((q, 1, len(A) + len(Bs)))
        used = set(A + Bs)
        self.pool = [i for i in self.pool if i not in used]
        if not Bs or not A:
            return self.finish(A or Bs)
        u = self.S(A)
        if not np.any((P @ u) % 3):
            return self.finish(A)
        self.add_gens([u], {(1,): A, (2,): A + Bs})
        return None
    # -- WNEST round
    def wnest_round(self, q, P):
        N = pool_size(q)
        if not self.pull(N):
            self.failed = True
            return "exhausted"
        F = self.pool[:N]
        M = (P @ np.array([self.stream[i] for i in F]).T) % 3
        zero = [j for j in range(N) if not np.any(M[:, j])]
        if zero:                                          # column already in the realized subgroup
            self.costs.append((q, "zero", 1))
            return self.finish([F[zero[0]]])
        rF = rank(M)
        idx, B = peel(M)
        Nst = len(idx)
        rst = rank(M[:, idx])
        if self.check:
            assert Nst - 1.5 * rst >= N - 1.5 * rF - 1e-9, (Nst, rst, N, rF)
            assert max(series_class_sizes(B)) <= 2
        delta, wt, sigma = pick_codeword(B)
        mu = 2.0 * Nst / 3.0
        det_wt = wt
        if self.mode == "wnest+":                          # Las Vegas refinement, same guarantee
            rng = self.rng or np.random.default_rng(0)
            co = rng.integers(0, 3, (self.samples, B.shape[0]))
            Cands = (co @ B) % 3
            ws = np.count_nonzero(Cands, axis=1)
            ok = np.nonzero((ws >= rst + 2) & (ws < wt))[0]
            if len(ok):
                j = ok[int(np.argmin(ws[ok]))]
                delta, wt = Cands[j], int(ws[j])
        if self.check:
            assert sigma ** 2 <= 4.0 * Nst / 9.0 + 1e-9
            assert wt >= rst + 2, (wt, rst, Nst, sigma)
            assert wt <= 2.0 * N / 3.0 + (2.0 / 3.0) * math.sqrt(N) + 1e-9
        Xloc = np.nonzero(delta)[0]
        X = [F[idx[j]] for j in Xloc]
        MX = M[:, [idx[j] for j in Xloc]]
        BX = kernel(MX)
        assert BX.shape[0] >= 2
        dl = delta[Xloc]
        # a second dependency independent of delta: some basis vector of D(X) is
        dp = None
        for row in BX:
            if rank(np.vstack([dl, row])) == 2:
                dp = row
                break
        assert dp is not None
        cls = {}
        for i, col in enumerate(X):
            cls.setdefault((int(dl[i]), int(dp[i])), []).append(col)
        real = {al: [c for ab in UNIONS[al] for c in cls.get(ab, [])] for al in UNIONS}
        self.costs.append((q, 2, len(X), N, Nst, rst, det_wt, round(mu, 2), round(sigma, 2)))
        used = set(X)
        self.pool = [i for i in self.pool if i not in used]
        h1, h2 = self.S(real[(1, 0)]), self.S(real[(0, 1)])
        for al, sel in real.items():                       # Theorem 4 identities in the quotient
            assert not np.any((P @ (self.S(sel) - al[0] * h1 - al[1] * h2)) % 3), "gadget identity failed"
        if rank((P @ np.vstack([h1, h2]).T) % 3) < 2:
            for al, sel in real.items():
                if sel and not np.any((P @ self.S(sel)) % 3):
                    return self.finish(sel)
            raise AssertionError("dependent h1,h2 but no nonempty zero-sum union")
        self.add_gens([h1, h2], real)
        return None
    def run(self, rng=None, qmin_kow=3):
        while True:
            q = self.n - len(self.gens)
            if q == 0:
                if not self.pull(1):
                    self.failed = True
                    return None
                c = self.pool.pop(0)
                return self.finish([c])
            P = self.quotient_map()
            if self.mode in ("wnest", "wnest+") and q >= qmin_kow:
                res = self.wnest_round(q, P)
            else:
                res = self.kow_round(q, P, rng)
            if res == "exhausted":
                return None
            if res is not None:
                return res

def stream_from_list(vectors):
    def f(i):
        return vectors[i] if i < len(vectors) else None
    return f

def stream_random(n, rng):
    def f(i):
        return rng.integers(0, 3, n)
    return f

def guarantee(n):
    """Exact worst-case m guaranteed by the per-piece bounds: at ambient dimension q >= 4 a WNEST
    piece costs at most floor(2N/3 + 2 sqrt(N)/3) for 2 dimensions with pool N = pool_size(q);
    for q <= 3 a KOW piece costs at most q + 1 for 1 dimension (pool q + 1).  m(n) = max over
    stages of (columns consumed before the stage + pool of the stage)."""
    consumed, best, q = 0, 0, n
    while q > 0:
        if q >= 4:
            N = pool_size(q)
            best = max(best, consumed + N)
            consumed += int(math.floor(2 * N / 3 + 2 * math.sqrt(N) / 3))
            q -= 2
        else:
            best = max(best, consumed + q + 1)
            consumed += q + 1
            q -= 1
    return max(best, consumed + 1)

def kow_recursion(n):
    """KOW Theorem 1.2 recursion as implemented in the pass: m_l = max(l + r, m_{l-1} + floor((l+r) 2 3^{r-1}/(3^r-1))),
    r = ceil(log_3(l+1)); m_0 = 1."""
    m = 1
    for l in range(1, n + 1):
        r = max(1, math.ceil(math.log(l + 1, 3) - 1e-12))
        m = max(l + r, m + (l + r) * 2 * 3 ** (r - 1) // (3 ** r - 1))
    return m

def bound(n):
    """m needed by the per-piece guarantee: sum over q = n, n-2, ... of (2N(q)/3 + 2 sqrt(N(q))/3)
    plus the last pool; crude upper bound used only for reporting."""
    tot = 0.0
    q = n
    while q >= 3:
        N = pool_size(q)
        tot += 2 * N / 3 + 2 * math.sqrt(N) / 3
        q -= 2
    return tot + 3 * n / 2 + 10

if __name__ == "__main__":
    print("gadget symbolic re-derivation (8 identities mod the two relations, h1,h2 independent):",
          gadget_symbolic_check())
    rng = np.random.default_rng(1108)
    print("pool sizes N(q) for q = 10, 20, 40, 80, 160:", [pool_size(q) for q in (10, 20, 40, 80, 160)])
    print("\nuniformly random instances [sampled]; m_used = columns ever pulled (= m needed for the run)")
    print(" n   mode   m_used          m_used/n^2        rounds   max(|X|-q) over 2-dim pieces")
    for n in (30, 60, 90, 120, 150):
        for mode in ("kow", "wnest"):
            ms, mx = [], []
            reps = 3 if n <= 90 else 2
            for rep in range(reps):
                R = Run(n, stream_random(n, rng), mode)
                sol = R.run(rng)
                assert sol is not None
                ms.append(len(R.stream))
                mx.append(max([c[2] - c[0] for c in R.costs if c[1] == 2], default=None))
            print(f"{n:3d}  {mode:5s}  {ms}  {[round(m / n / n, 4) for m in ms]}  {len(R.costs)}  {mx}")
            sys.stdout.flush()
    R = Run(120, stream_random(120, rng), "wnest")
    R.run()
    print("\nWNEST n=120 per-piece (q, d, |X|, N, N*, r*, wt, mu, sigma): first 4", R.costs[:4])
    print("   last 4", R.costs[-4:])
    print("all witnesses verified by direct summation (assert in Run.finish)")
