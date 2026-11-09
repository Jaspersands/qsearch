"""Strict-mode re-implementation of WNEST (2026-11-08-rees-sde-p3-nest.md, Theorem A), written
to BREAK the theorem: every invariant the proof uses is asserted at run time, in exact integer
arithmetic (27*Phi is an integer; no floats anywhere in the decision path).

Independent of wnest.py (only the problem statement and the proof text were used); the
two variants that differ between the proof text and wnest.py are selectable:
  variant="proof": WNEST at q >= 4, KOW rounds with pool q+1 for q <= 3  (the text of Theorem A)
  variant="code" : WNEST at q >= 3, KOW rounds with pool q + ceil(log_3(q+1))  (wnest.py)

Asserted invariants (names used in the report):
  I0  every pool column is nonzero in the quotient (else finish by Lemma 1)
  I1  coloop deletion drops the rank by exactly the number of coloops
  I2  Lemma P: deleting a series class of size a drops the rank by EXACTLY a-1
  I3  Delta = |F| - 1.5 rank(F) never decreases during peeling; Delta(F*) >= N - 1.5 q
  I4  after peeling: no coloop, all series classes <= 2, D(F*) != 0
  I5  Lemma M: Var computed by the class formula (2/9) sum a_j^2 equals the brute-force variance
      (when 3^k <= 3^11) and is <= 4 N*/9
  I6  Lemma D: Phi(prefix) = average of Phi(prefix, v); the chosen branch never increases Phi;
      (wt - 2N*/3)^2 <= Var;  Phi(empty) == Var;  delta != 0
  I7  weight window: r* + 2 <= wt <= 2N/3 + (2/3) sqrt(N)  (N = pool size)
  I8  dim D(X) >= 2, delta' independent of delta, supp delta = X
  I9  Lemma G: the 8 union identities hold in the quotient; unions are 0/1 subsets of X
  I10 either <h1,h2> has dim 2 in the quotient, or a nonempty union is zero-sum in the quotient
  I11 accounting: m needed = max over stages of (consumed + pool) <= guarantee(n) <= closed form
  I12 the final witness is nonempty, has distinct indices, and sums to zero over the ORIGINAL
      vectors (0/1 weights only)
Interpreter: /opt/anaconda3/bin/python.
"""
import math, itertools
import numpy as np

# ------------------------------------------------------------------ exact F_3 linear algebra
def rref(M):
    M = np.array(M, dtype=np.int64) % 3
    rows, cols = M.shape
    piv, r = [], 0
    for c in range(cols):
        if r == rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        p = r + nz[0]
        if p != r:
            M[[r, p]] = M[[p, r]]
        M[r] = (M[r] * M[r, c]) % 3
        col = M[:, c].copy(); col[r] = 0
        M = (M - np.outer(col, M[r])) % 3
        piv.append(c); r += 1
    return M[:r], piv

def rank(M):
    M = np.asarray(M)
    if M.size == 0:
        return 0
    return len(rref(M)[1])

def kernel(M):
    """rows: basis of {x : M x = 0}; M is q x N (N columns)."""
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
    if len(gens) == 0:
        return [] if not np.any(np.asarray(t) % 3) else None
    G = np.array(gens, dtype=np.int64).T % 3
    k = G.shape[1]
    R, piv = rref(np.hstack([G, (np.asarray(t) % 3).reshape(-1, 1)]))
    if k in piv:
        return None
    c = [0] * k
    for i, pc in enumerate(piv):
        c[pc] = int(R[i, k])
    return c

def proj_key(v):
    """(canonical projective representative, scalar s with s*v = canonical) or (None, 0)."""
    nz = np.nonzero(v)[0]
    if len(nz) == 0:
        return None, 0
    s = int(v[nz[0]])
    return tuple(((v * s) % 3).tolist()), s

def series_classes(B):
    cl = {}
    for j in range(B.shape[1]):
        key, _ = proj_key(B[:, j])
        cl.setdefault(key, []).append(j)
    return cl

# ------------------------------------------------------------------ pool size, bounds
def pool_size(q):
    N = 1
    while N - 1.5 * q < 3 + math.sqrt(N):       # the only float: compared exactly below
        N += 1
    # exact re-check: N - 1.5q >= 3 + sqrt(N)  <=>  (2N - 3q - 6) >= 0 and (2N-3q-6)^2 >= 4N
    assert 2 * N - 3 * q - 6 >= 0 and (2 * N - 3 * q - 6) ** 2 >= 4 * N
    assert not (2 * (N - 1) - 3 * q - 6 >= 0 and (2 * (N - 1) - 3 * q - 6) ** 2 >= 4 * (N - 1))
    return N

def closed_form(n):
    return n * n / 4 + (8 / 9) * (n + 2) ** 1.5 + 4 * n + 2 * math.sqrt(n) + 15

def piece_cap(N):
    """integer cap on |X| for a pool of size N: floor(2N/3 + (2/3) sqrt N)."""
    return math.floor(2 * N / 3 + 2 * math.sqrt(N) / 3)

def guarantee(n, variant="proof"):
    consumed, best, q = 0, 0, n
    qmin = 4 if variant == "proof" else 3
    while q > 0:
        if q >= qmin:
            N = pool_size(q)
            best = max(best, consumed + N)
            consumed += piece_cap(N)
            q -= 2
        else:
            pool = q + 1 if variant == "proof" else q + max(1, math.ceil(math.log(q + 1, 3) - 1e-12))
            best = max(best, consumed + pool)
            consumed += q + 1
            q -= 1
    return max(best, consumed + 1)

# ------------------------------------------------------------------ Lemma D, exact
def phi27(B, prefix):
    """27 * E[(wt - 2N/3)^2 | x_1..x_j = prefix], exact integer."""
    k, N = B.shape
    j = len(prefix)
    c = (np.array(prefix, dtype=np.int64) @ B[:j]) % 3 if j else np.zeros(N, dtype=np.int64)
    G = B[j:]
    det3 = 0                               # 3 * sum over constant coords of (1(c!=0) - 2/3)
    groups = {}
    for i in range(N):
        g = G[:, i]
        key, s = proj_key(g)
        if key is None:
            det3 += 1 if c[i] else -2
        else:
            groups.setdefault(key, []).append((int(c[i]), s))
    tot = 3 * det3 * det3                  # 27 * det^2 = 3 * (3 det)^2
    for members in groups.values():
        acc = 0
        for t in range(3):
            w3 = 0
            for (ci, s) in members:
                w3 += 1 if (ci + s * t) % 3 else -2
            acc += w3 * w3
        tot += acc                         # 27 * (1/3) * sum_t (w)^2 = sum_t (3w)^2
    return tot

def brute_variance27(B):
    """27 * Var[wt] by enumerating all codewords (3^k of them)."""
    k, N = B.shape
    tot = 0
    for x in itertools.product(range(3), repeat=k):
        d = (np.array(x, dtype=np.int64) @ B) % 3
        w3 = 3 * int(np.count_nonzero(d)) - 2 * N
        tot += w3 * w3
    # E[(3wt - 2N)^2] = tot / 3^k ; 27 Var = 3 * tot / 3^k
    assert (3 * tot) % (3 ** k) == 0
    return 3 * tot // (3 ** k)

def pick_codeword_strict(B, log=None):
    k, N = B.shape
    assert k >= 1
    var27 = phi27(B, [])
    prefix = []
    cur = var27
    for j in range(k):
        vals = [phi27(B, prefix + [v]) for v in range(3)]
        assert sum(vals) == 3 * cur, ("Phi(prefix) is not the average of Phi(prefix,v)", vals, cur)
        v = min(range(3), key=lambda t: (vals[t], t))
        assert vals[v] <= cur
        cur = vals[v]
        prefix.append(v)
    delta = (np.array(prefix, dtype=np.int64) @ B) % 3
    wt = int(np.count_nonzero(delta))
    assert cur == 3 * (3 * wt - 2 * N) ** 2, (cur, wt, N)          # Phi(full) = (wt - 2N/3)^2
    assert 27 * (3 * wt - 2 * N) ** 2 <= 27 * var27 * 1 and 3 * (3 * wt - 2 * N) ** 2 <= var27, \
        ("Lemma D violated", wt, N, var27 / 27)
    assert wt > 0
    return delta, wt, var27

# ------------------------------------------------------------------ peeling with Lemma P checks
def peel_strict(M, stats):
    """M: q x N nonzero columns in the quotient. Returns (idx, B, trace)."""
    q, N = M.shape
    idx = list(range(N))
    r = rank(M)
    delta_start = 2 * N - 3 * r                   # 2*Delta, integer
    cur2 = delta_start
    trace = []
    while True:
        sub = M[:, idx]
        B = kernel(sub)
        if B.shape[0] == 0:
            # F independent: every column is a coloop; the invariant forbids this unless N small
            raise AssertionError(("D(F) = 0 after peeling", len(idx), rank(sub)))
        zero = [j for j in range(len(idx)) if not np.any(B[:, j])]
        if zero:
            new_idx = [c for j, c in enumerate(idx) if j not in set(zero)]
            r_new = rank(M[:, new_idx]) if new_idx else 0
            r_old = rank(sub)
            assert r_old - r_new == len(zero), ("I1 coloop rank drop", r_old, r_new, len(zero))
            idx = new_idx
            cur2 = 2 * len(idx) - 3 * r_new
            trace.append(("coloop", len(zero)))
            assert cur2 >= delta_start, ("I3", cur2, delta_start)
            continue
        cl = series_classes(B)
        big = [c for c in cl.values() if len(c) >= 3]
        if not big:
            stats["max_class"] = max(stats.get("max_class", 0), max(len(c) for c in cl.values()))
            return idx, B, trace
        a_class = max(big, key=len)
        a = len(a_class)
        new_idx = [c for j, c in enumerate(idx) if j not in set(a_class)]
        r_old = rank(sub)
        r_new = rank(M[:, new_idx]) if new_idx else 0
        assert r_old - r_new == a - 1, ("I2 Lemma P violated", a, r_old, r_new)
        stats["max_class"] = max(stats.get("max_class", 0), a)
        stats["peeled_classes"] = stats.get("peeled_classes", 0) + 1
        idx = new_idx
        cur2 = 2 * len(idx) - 3 * r_new
        trace.append(("class", a))
        assert cur2 >= delta_start, ("I3", cur2, delta_start)

# ------------------------------------------------------------------ gadget
UNIONS = {(0, 1): [(1, 1), (1, 2), (2, 2)], (0, 2): [(1, 2), (2, 1), (2, 2)],
          (1, 0): [(1, 0), (1, 1), (2, 0)], (1, 1): [(1, 0), (2, 0), (2, 1)],
          (1, 2): [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
          (2, 0): [(1, 1), (2, 0), (2, 2)], (2, 1): [(2, 0), (2, 1), (2, 2)],
          (2, 2): [(1, 0), (1, 2), (2, 1)]}

class Fail(Exception):
    pass

class StrictRun:
    def __init__(self, n, vectors, variant="proof", brute_var=True):
        self.n = n
        self.vecs = [np.asarray(v, dtype=np.int64) % 3 for v in vectors]
        for v in self.vecs:
            assert v.shape == (n,)
        self.variant = variant
        self.brute_var = brute_var
        self.pool = []            # indices not yet consumed, in input order
        self.next = 0
        self.gens = []
        self.pieces = []
        self.costs = []
        self.m_needed = 0
        self.stats = {}
        self.max_slack = -10 ** 9        # max over pieces of wt - (r*+2)
        self.max_over_q = -10 ** 9       # max over pieces of |X| - q
        self.max_zsig = -1.0             # max (wt - mu)/sigma
    def pull(self, k):
        while len(self.pool) < k:
            if self.next >= len(self.vecs):
                return False
            self.pool.append(self.next); self.next += 1
        self.m_needed = max(self.m_needed, self.next)
        return True
    def S(self, sel):
        return (np.sum([self.vecs[i] for i in sel], axis=0) % 3) if sel else np.zeros(self.n, dtype=np.int64)
    def P(self):
        if not self.gens:
            return np.eye(self.n, dtype=np.int64)
        return kernel(np.array(self.gens, dtype=np.int64))
    def finish(self, base):
        sol = list(base)
        t = (-self.S(base)) % 3
        for (a, b), real in reversed(self.pieces):
            c = solve_in_span(self.gens[:b], t)
            assert c is not None, "Lemma 1 unwinding: target not in realized subgroup"
            alpha = tuple(c[a:b])
            if any(alpha):
                sel = real[alpha]
                sol += sel
                t = (t - self.S(sel)) % 3
        assert not np.any(t)
        assert len(sol) > 0 and len(set(sol)) == len(sol), "I12 witness not a set"
        assert not np.any(self.S(sol)), "I12 witness does not sum to zero"
        return sol
    def kow_round(self, q, P):
        if self.variant == "proof":
            pool = q + 1
        else:
            pool = q + max(1, math.ceil(math.log(q + 1, 3) - 1e-12))
        if not self.pull(pool):
            raise Fail("exhausted at KOW round q=%d" % q)
        F = self.pool[:pool]
        M = (P @ np.array([self.vecs[i] for i in F]).T) % 3
        zero = [j for j in range(pool) if not np.any(M[:, j])]
        if zero:
            return self.finish([F[zero[0]]])
        B = kernel(M)
        assert B.shape[0] >= 1
        # sparsest dependency (small k)
        k = B.shape[0]
        best = None
        for co in itertools.product(range(3), repeat=min(k, 7)):
            if not any(co):
                continue
            d = (np.array(co + (0,) * (k - len(co)), dtype=np.int64) @ B) % 3
            w = int(np.count_nonzero(d))
            if w and (best is None or w < best[0]):
                best = (w, d)
        d = best[1]
        A = [F[i] for i in range(pool) if d[i] == 1]
        Bs = [F[i] for i in range(pool) if d[i] == 2]
        cost = len(A) + len(Bs)
        assert cost <= q + 1 or self.variant == "code"
        self.costs.append((q, 1, cost, pool))
        used = set(A + Bs)
        self.pool = [i for i in self.pool if i not in used]
        if not Bs or not A:
            return self.finish(A or Bs)
        u = self.S(A)
        if not np.any((P @ u) % 3):
            return self.finish(A)
        self.gens.append(u % 3)
        self.pieces.append(((len(self.gens) - 1, len(self.gens)), {(1,): A, (2,): A + Bs}))
        return None
    def wnest_round(self, q, P):
        N = pool_size(q)
        if not self.pull(N):
            raise Fail("exhausted at WNEST round q=%d (need pool %d)" % (q, N))
        F = self.pool[:N]
        M = (P @ np.array([self.vecs[i] for i in F]).T) % 3
        assert M.shape == (q, N)
        zero = [j for j in range(N) if not np.any(M[:, j])]
        if zero:
            self.costs.append((q, "zero", 1, N))
            return self.finish([F[zero[0]]])
        rF = rank(M)
        assert rF <= q
        idx, B, trace = peel_strict(M, self.stats)
        Nst, rst = len(idx), rank(M[:, idx])
        k = B.shape[0]
        assert k == Nst - rst
        assert 2 * Nst - 3 * rst >= 2 * N - 3 * rF, "I3"
        # Delta(F*) >= N - 1.5 q >= 3 + sqrt(N) >= 3 + sqrt(N*)   =>  N* - 1.5 r* >= 3 + sqrt(N*)
        assert (2 * Nst - 3 * rst - 6) >= 0 and (2 * Nst - 3 * rst - 6) ** 2 >= 4 * Nst, "window premise"
        cl = series_classes(B)
        sizes = sorted((len(c) for c in cl.values()), reverse=True)
        assert all(np.any(B[:, j]) for j in range(Nst)), "I4 coloop after peeling"
        assert sizes[0] <= 2, "I4 class > 2 after peeling"
        var27_formula = 6 * sum(a * a for a in sizes)                      # 27 * (2/9) sum a^2
        delta, wt, var27 = pick_codeword_strict(B)
        assert var27 == var27_formula, ("I5 Lemma M formula vs Phi(empty)", var27, var27_formula)
        if self.brute_var and k <= 11:
            assert brute_variance27(B) == var27, "I5 brute-force variance"
        assert var27 <= 12 * Nst, "I5 Var <= 4N*/9"                        # 27*4N/9 = 12N
        assert wt >= rst + 2, ("I7 lower window", wt, rst, Nst)
        assert wt <= piece_cap(N), ("I7 upper window", wt, N, piece_cap(N))
        assert 3 * (3 * wt - 2 * Nst) ** 2 <= var27
        self.max_slack = max(self.max_slack, wt - (rst + 2))
        self.max_over_q = max(self.max_over_q, wt - q)
        sigma = math.sqrt(var27 / 27)
        if sigma > 0:
            self.max_zsig = max(self.max_zsig, (wt - 2 * Nst / 3) / sigma)
        Xloc = np.nonzero(delta)[0]
        X = [F[idx[j]] for j in Xloc]
        MX = M[:, [idx[j] for j in Xloc]]
        BX = kernel(MX)
        assert BX.shape[0] >= 2, "I8 dim D(X) < 2"
        dl = delta[Xloc]
        assert np.all(dl)
        dp = None
        for row in BX:
            if rank(np.vstack([dl, row])) == 2:
                dp = row; break
        assert dp is not None, "I8 no independent delta'"
        cls = {}
        for i, col in enumerate(X):
            cls.setdefault((int(dl[i]), int(dp[i])), []).append(col)
        real = {al: [c for ab in UNIONS[al] for c in cls.get(ab, [])] for al in UNIONS}
        Xset = set(X)
        for al, sel in real.items():
            assert len(set(sel)) == len(sel) and set(sel) <= Xset, "I9 realizer not a 0/1 subset of X"
        assert set(real[(1, 2)]) == Xset
        h1, h2 = self.S(real[(1, 0)]), self.S(real[(0, 1)])
        for al, sel in real.items():
            assert not np.any((P @ (self.S(sel) - al[0] * h1 - al[1] * h2)) % 3), "I9 gadget identity"
        self.costs.append((q, 2, len(X), N, Nst, rst, wt, round(sigma, 3), trace))
        used = set(X)
        self.pool = [i for i in self.pool if i not in used]
        if rank((P @ np.vstack([h1, h2]).T) % 3) < 2:
            for al, sel in real.items():
                if sel and not np.any((P @ self.S(sel)) % 3):
                    return self.finish(sel)
            raise AssertionError("I10 dependent h1,h2 but no nonempty zero-sum union")
        k0 = len(self.gens)
        self.gens += [h1 % 3, h2 % 3]
        assert rank(np.array(self.gens)) == len(self.gens)
        self.pieces.append(((k0, k0 + 2), real))
        return None
    def run(self):
        qmin = 4 if self.variant == "proof" else 3
        while True:
            q = self.n - len(self.gens)
            if q == 0:
                if not self.pull(1):
                    raise Fail("exhausted at q=0")
                c = self.pool.pop(0)
                return self.finish([c])
            P = self.P()
            assert P.shape[0] == q
            res = self.wnest_round(q, P) if q >= qmin else self.kow_round(q, P)
            if res is not None:
                return res

def solve_checked(n, vectors, variant="proof", brute_var=True):
    """Run WNEST on the instance; return (witness or None, run).  Asserts I11 on success: the
    columns needed never exceed guarantee(n) (variant) nor the closed form of Theorem A."""
    R = StrictRun(n, vectors, variant, brute_var)
    try:
        sol = R.run()
    except Fail as e:
        return None, R, str(e)
    assert R.m_needed <= guarantee(n, variant), ("I11 guarantee", R.m_needed, guarantee(n, variant))
    if variant == "proof":
        assert R.m_needed <= closed_form(n), ("I11 closed form", R.m_needed, closed_form(n))
    return sol, R, None

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    for n in (4, 5, 6, 7, 8, 9, 10, 15, 20):
        cf = closed_form(n)
        print(n, "guarantee proof/code", guarantee(n, "proof"), guarantee(n, "code"), "closed", round(cf, 2))
    for n in (6, 11, 20):
        m = math.ceil(closed_form(n))
        vec = [rng.integers(0, 3, n) for _ in range(m)]
        sol, R, err = solve_checked(n, vec, "proof")
        print(n, m, "needed", R.m_needed, "pieces", len(R.costs), "max slack", R.max_slack, err)
