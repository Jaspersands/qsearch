"""Independent re-implementation of the weight-doubling node (2026-11-05 check).

Written from the statement in 2026-11-05-rees-s3-arity.md, Part P, without
reading that report's code.  Everything is exact arithmetic mod p; every
output of every recursive call is verified exactly.

Usage:  python wdcheck.py <part> <out.json>
  part in {exact, reads, indep, node, neg, all}
"""
import json
import math
import sys
import time
from fractions import Fraction

import numpy as np
from scipy import stats

sys.setrecursionlimit(100000)


# ----------------------------------------------------------------------------
# exact quantities
# ----------------------------------------------------------------------------

def jstar(p):
    return math.ceil(math.log2(p - 1)) if p > 2 else 0


def sigma_exact(p):
    """E[K], K = number of i.i.d. uniform draws of F_p until the subset sums
    (including the empty sum) cover F_p.  Exact, by DP over reachable sets."""
    full = (1 << p) - 1

    def shift(mask, b):
        # mask of R + b
        return ((mask << b) | (mask >> (p - b))) & full

    memo = {full: Fraction(0)}
    # process masks in decreasing popcount order via recursion with memo
    order = []
    seen = {1}
    stack = [1]
    while stack:
        m = stack.pop()
        order.append(m)
        if m == full:
            continue
        for b in range(1, p):
            m2 = m | shift(m, b)
            if m2 not in seen:
                seen.add(m2)
                stack.append(m2)
    order.sort(key=lambda m: -bin(m).count("1"))
    for m in order:
        if m == full:
            continue
        # E(m) = 1 + (1/p) E(m) [beta=0, and beta with m+beta=m: only 0]
        #          + (1/p) sum_{b != 0} E(m | m+b)
        s = Fraction(0)
        for b in range(1, p):
            m2 = m | shift(m, b)
            assert m2 != m, "R + b = R for b != 0 would contradict ⟨b⟩ = F_p"
            s += memo[m2]
        memo[m] = (p + s) / (p - 1)
    return memo[1]


def N_table(p, nmax, sig=None):
    """Exact N_j(d) for 0 <= j <= j*, 0 <= d <= nmax."""
    J = jstar(p)
    if sig is None:
        sig = sigma_exact(p)
    N = {J: [Fraction(d + 1) for d in range(nmax + 1)]}
    for j in range(J - 1, -1, -1):
        row = [Fraction(1)]
        for d in range(1, nmax + 1):
            row.append(row[-1] + sig * N[j + 1][d - 1])
        N[j] = row
    return N


# ----------------------------------------------------------------------------
# column streams
# ----------------------------------------------------------------------------

class Overrun(Exception):
    pass


class Stream:
    """i.i.d. columns of F_p^n (or another law, for negative controls)."""

    def __init__(self, p, n, rng, law="uniform", cap=None, source=None):
        self.p, self.n, self.rng, self.law = p, n, rng, law
        self.cols = []
        self.cap = cap
        self.source = source  # optional iterator of precomputed columns
        self.buf = None
        self.bpos = 0

    def _draw_batch(self, k=4096):
        p, n = self.p, self.n
        if self.law == "uniform":
            return self.rng.integers(0, p, size=(k, n), dtype=np.int64)
        if self.law == "bernoulli":  # entries in {0,1}: not uniform
            return self.rng.integers(0, 2, size=(k, n), dtype=np.int64)
        if self.law == "hyperplane":  # last coord equals first coord
            b = self.rng.integers(0, p, size=(k, n), dtype=np.int64)
            if n >= 2:
                b[:, n - 1] = b[:, 0]
            return b
        raise ValueError(self.law)

    def next(self):
        if self.cap is not None and len(self.cols) >= self.cap:
            raise Overrun()
        if self.source is not None:
            v = next(self.source)
        else:
            if self.buf is None or self.bpos >= len(self.buf):
                self.buf = self._draw_batch()
                self.bpos = 0
            v = self.buf[self.bpos]
            self.bpos += 1
        self.cols.append(v)
        return len(self.cols) - 1

    @property
    def count(self):
        return len(self.cols)


# ----------------------------------------------------------------------------
# linear algebra mod p
# ----------------------------------------------------------------------------

def kernel_vector(A, p):
    """Nonzero x with A x = 0 mod p, A of shape (d, d+1)."""
    A = [list(map(int, row)) for row in A]
    d = len(A)
    m = d + 1
    piv_cols = []
    r = 0
    for col in range(m):
        pr = None
        for i in range(r, d):
            if A[i][col] % p:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][col], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(d):
            if i != r and A[i][col] % p:
                f = A[i][col]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv_cols.append(col)
        r += 1
        if r == d:
            break
    free = [c for c in range(m) if c not in piv_cols][0]
    x = [0] * m
    x[free] = 1
    for i, pc in enumerate(piv_cols):
        x[pc] = (-A[i][free]) % p
    return x


def sym(x, p):
    x %= p
    return x - p if x > p // 2 else x


# ----------------------------------------------------------------------------
# the recursion
# ----------------------------------------------------------------------------

class Solver:
    def __init__(self, p, stream, record=False, peek=False):
        self.peek = peek  # negative control: inner switch choice reads coordinate d
        self.p = p
        self.J = jstar(p)
        self.S = stream
        self.record = record
        self.log = []  # (j, d, beta, Ck, k_in_loop)
        self.calls = 0

    def wsum(self, w, d):
        p = self.p
        acc = np.zeros(d, dtype=np.int64)
        for i, a in w.items():
            acc = (acc + a * self.S.cols[i][:d]) % p
        return acc

    def check(self, w, j, d, t):
        p = self.p
        assert len(w) > 0
        bound = 1 if j == 0 else 2 ** (j - 1)
        for i, a in w.items():
            assert a != 0 and a % p != 0
            if j == 0:
                assert a == 1
            else:
                assert -bound <= a <= bound
        assert np.array_equal(self.wsum(w, d), np.asarray(t, dtype=np.int64) % p)

    def solve(self, j, d, t):
        """Returns dict index -> integer weight in D^(j), sum_i w_i v_i[:d] = t."""
        self.calls += 1
        p, S = self.p, self.S
        t = np.asarray(t, dtype=np.int64) % p
        if j == self.J:
            assert not t.any()
            idx = [S.next() for _ in range(d + 1)]
            if d == 0:
                w = {idx[0]: 1}
            else:
                A = np.stack([S.cols[i][:d] for i in idx], axis=1)
                x = kernel_vector(A, p)
                w = {i: sym(a, p) for i, a in zip(idx, x) if a % p}
            self.check(w, j, d, t)
            return w
        if d == 0:
            w = {S.next(): 1}
            self.check(w, j, d, t)
            return w
        # 1. switches on the first d-1 coordinates, beta on coordinate d
        blocks = []
        reach = {0: None}
        while len(reach) < p:
            c0 = S.count
            alpha = self.solve(j + 1, d - 1, np.zeros(d - 1, dtype=np.int64))
            beta = 0
            for i, a in alpha.items():
                beta = (beta + a * int(S.cols[i][d - 1])) % p
            if self.peek:
                # BROKEN on purpose: draw a second switch and keep the one whose
                # coordinate-d value is smaller.  This reads coordinate d before
                # the choice, so beta is no longer uniform.
                alpha2 = self.solve(j + 1, d - 1, np.zeros(d - 1, dtype=np.int64))
                beta2 = 0
                for i, a in alpha2.items():
                    beta2 = (beta2 + a * int(S.cols[i][d - 1])) % p
                if beta2 < beta:
                    alpha, beta = alpha2, beta2
            Ck = S.count - c0
            k = len(blocks)
            blocks.append((alpha, beta))
            if self.record:
                self.log.append((j, d, beta, Ck, k))
            new = {}
            for r in reach:
                r2 = (r + beta) % p
                if r2 not in reach and r2 not in new:
                    new[r2] = (k, r)
            reach.update(new)
        # 2. default (all x') forward sum on coordinates 1..d
        xs, xps = [], []
        cvec = np.zeros(d, dtype=np.int64)
        for alpha, beta in blocks:
            x = {i: -((-a) // 2) for i, a in alpha.items()}   # ceil(a/2)
            xp = {i: -(a // 2) for i, a in alpha.items()}     # -floor(a/2)
            for i in alpha:
                assert x[i] - xp[i] == alpha[i]
            xs.append(x)
            xps.append(xp)
            for i, a in xp.items():
                if a:
                    cvec = (cvec + a * S.cols[i][:d]) % p
        # 3. recurse on fresh columns
        sub = self.solve(j, d - 1, (t - cvec)[: d - 1])
        # 4. last-coordinate residual and backward choice
        resid = (t - cvec - self.wsum(sub, d)) % p
        assert not resid[: d - 1].any()
        a = int(resid[d - 1])
        T = set()
        cur = a
        while reach[cur] is not None:
            k, prev = reach[cur]
            T.add(k)
            cur = prev
        assert sum(blocks[k][1] for k in T) % p == a
        w = dict(sub)
        for k in range(len(blocks)):
            src = xs[k] if k in T else xps[k]
            for i, v in src.items():
                if v:
                    assert i not in w
                    w[i] = v
        self.check(w, j, d, t)
        return w


def run_once(p, n, rng, law="uniform", record=False, target=None, level=0, peek=False):
    S = Stream(p, n, rng, law=law)
    sol = Solver(p, S, record=record, peek=peek)
    t = np.zeros(n, dtype=np.int64) if target is None else target
    w = sol.solve(level, n, t)
    # final exact check over all n coordinates
    acc = np.zeros(n, dtype=np.int64)
    for i, a in w.items():
        acc = (acc + a * S.cols[i]) % p
    assert np.array_equal(acc, np.asarray(t) % p)
    if level == 0:
        assert all(a == 1 for a in w.values()) and len(w) > 0
    return S.count, sol


# ----------------------------------------------------------------------------
# parts
# ----------------------------------------------------------------------------

def part_exact():
    out = {"sigma": {}, "closed_form_ok": {}, "p3_formula_ok": None}
    for p in [3, 5, 7, 11, 13, 17]:
        s = sigma_exact(p)
        B0 = math.ceil(2 * math.log2(p - 1))
        out["sigma"][p] = {"exact": f"{s.numerator}/{s.denominator}",
                           "float": float(s),
                           "bound_min_p_B0p4": min(p, B0 + 4),
                           "bound_ok": s <= min(p, B0 + 4)}
        J = jstar(p)
        N = N_table(p, 200, s)
        ok = all(N[0][n] <= (s + 1) ** J * math.comb(n + J + 1, J + 1)
                 for n in range(201))
        mono = all(N[0][n + 1] > N[0][n] for n in range(200))
        # local log-log slopes at large n
        sl = {nn: math.log(N[0][2 * nn] / N[0][nn]) / math.log(2)
              for nn in (25, 50, 100)}
        out["closed_form_ok"][p] = {"bound_ok_n_le_200": ok, "increasing": mono,
                                    "jstar": J, "degree_1_plus_jstar": J + 1,
                                    "slope_n_to_2n": sl}
    N3 = N_table(3, 100)
    out["p3_formula_ok"] = all(N3[0][n] == 1 + Fraction(3 * n * (n + 1), 2)
                               for n in range(101))
    return out


def part_reads(seed=11):
    rng = np.random.default_rng(seed)
    plan = {3: ([4, 8, 16, 32, 48], 120), 5: ([3, 6, 10, 14], 40),
            7: ([2, 4, 6, 8], 30), 11: ([2, 3, 4, 5, 6], 20)}
    rows = []
    for p, (ns, runs) in plan.items():
        N = N_table(p, max(ns))
        for n in ns:
            t0 = time.time()
            R = [run_once(p, n, rng)[0] for _ in range(runs)]
            m, se = float(np.mean(R)), float(np.std(R, ddof=1) / math.sqrt(runs))
            ex = float(N[0][n])
            rows.append({"p": p, "n": n, "runs": runs, "mean": m, "se": se,
                         "exact_N0": ex, "z": (m - ex) / se if se > 0 else 0.0,
                         "max": int(max(R)), "secs": round(time.time() - t0, 1)})
            print(rows[-1], flush=True)
    # inhomogeneous targets at levels 0 and 1
    inh = []
    for p in [5, 7, 11]:
        for level in [0, 1]:
            for n in [1, 3, 5]:
                for _ in range(5):
                    t = rng.integers(0, p, size=n)
                    run_once(p, n, rng, target=t, level=level)
                inh.append({"p": p, "level": level, "n": n, "runs": 5, "all_exact": True})
    return {"rows": rows, "inhomogeneous": inh}


def part_indep(seed=12):
    """Tests of the law of the switch values beta_k at every level:
    (u0) beta of the FIRST switch of each loop is uniform (no selection);
    (uall) all betas pooled (approximately uniform, by Wald);
    (pair) beta_{k+1} independent of beta_k (contingency test; survival to
           k+1 depends on beta_1..beta_k only, so the conditional law of
           beta_{k+1} must be uniform for every value of beta_k);
    (Ck)  beta_k independent of the read count C_k of its block.
    The 'peek' rows are a deliberately broken variant (negative control)."""
    rng = np.random.default_rng(seed)
    out = []
    plan = [(3, 24, 60, False), (5, 8, 30, False), (7, 6, 25, False), (11, 4, 25, False),
            (5, 8, 30, True), (7, 6, 15, True)]
    for p, n, runs, peek in plan:
        logs = []
        for _ in range(runs):
            _, sol = run_once(p, n, rng, record=True, peek=peek)
            logs.append(sol.log)
        levels = sorted({e[0] for L in logs for e in L})
        for j in levels:
            first, allb, Cb = [], [], []
            pairs = np.zeros((p, p))
            for L in logs:
                prev = None
                for (jj, d, beta, Ck, k) in L:
                    if jj != j:
                        continue
                    allb.append(beta)
                    Cb.append((beta, Ck))
                    if k == 0:
                        first.append(beta)
                    if prev is not None and prev[0] == d and k == prev[2] + 1:
                        pairs[prev[1], beta] += 1
                    prev = (d, beta, k)
            c0 = np.bincount(first, minlength=p)
            ca = np.bincount(allb, minlength=p)
            pt = pairs[pairs.sum(axis=1) > 0]
            pt = pt[:, pt.sum(axis=0) > 0]
            pair_p = float(stats.chi2_contingency(pt).pvalue) if pt.shape[0] > 1 and pt.shape[1] > 1 and pairs.sum() >= 5 * p * p else None
            Cs = np.array([c for (_, c) in Cb])
            med = np.median(Cs)
            tab = np.zeros((2, p))
            for (b, c) in Cb:
                tab[int(c > med), b] += 1
            tab = tab[:, tab.sum(axis=0) > 0]
            ck_p = float(stats.chi2_contingency(tab).pvalue) if tab.shape[1] > 1 and (tab.sum(axis=1) > 0).all() else None
            row = {"p": p, "n": n, "peek": peek, "level": j, "switches": len(allb),
                   "first_switches": len(first),
                   "u0_pvalue": float(stats.chisquare(c0).pvalue),
                   "uall_pvalue": float(stats.chisquare(ca).pvalue),
                   "pair_pvalue": pair_p, "pairs": int(pairs.sum()),
                   "beta_vs_Ck_pvalue": ck_p, "beta_counts_all": ca.tolist()}
            out.append(row)
            print(row, flush=True)
    return out


def random_subspace(p, g, a, rng):
    while True:
        B = rng.integers(0, p, size=(a, g), dtype=np.int64)
        if rank_mod(B, p) == a:
            return B


def rref(A, p):
    A = [list(map(int, r)) for r in A]
    rows, cols = len(A), (len(A[0]) if A else 0)
    piv = []
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return A[:r], piv


def rank_mod(A, p):
    return len(rref(A, p)[1]) if len(A) else 0


def node_params(p, g, tau, N0g):
    # exact ceil(log_p(2/tau)) and ceil(log_2(2/tau)) for rational tau
    tt = 0
    while Fraction(p) ** tt < Fraction(2) / Fraction(tau).limit_denominator(10 ** 9):
        tt += 1
    t = g + tt
    L = math.ceil(2 * N0g)
    k = 0
    while 2 ** k < Fraction(2) / Fraction(tau).limit_denominator(10 ** 9):
        k += 1
    return t, L, k, t + k * L


def run_node(p, g, a, tau, rng, N0g, bank_law="subspace"):
    """One node of Cor. P.4.  Returns ('ok', |T|) or ('abort', reason)."""
    t, L, k, M = node_params(p, g, tau, N0g)
    if bank_law == "subspace":
        B = random_subspace(p, g, a, rng) if a > 0 else np.zeros((0, g), dtype=np.int64)
        X = rng.integers(0, p, size=(M, a), dtype=np.int64)
        bank = (X @ B) % p if a > 0 else np.zeros((M, g), dtype=np.int64)
    elif bank_law == "hyperplane":  # adversarial: first t span F_p^g, rest have v_g = v_1
        bank = rng.integers(0, p, size=(M, g), dtype=np.int64)
        bank[:g] = np.eye(g, dtype=np.int64)
        bank[g:, g - 1] = bank[g:, 0]
    else:
        raise ValueError(bank_law)
    # 1. span of the first t labels, reduced echelon basis
    R, piv = rref(bank[:t], p)
    W = np.array(R, dtype=np.int64).reshape(len(R), g)
    dimW = len(piv)

    def coords(lam):
        # lam in W iff lam == sum_i lam[piv_i] * W_i
        x = np.array([int(lam[c]) for c in piv], dtype=np.int64)
        recon = (x @ W) % p if dimW else np.zeros(g, dtype=np.int64)
        return x if np.array_equal(recon, lam % p) else None

    for b in range(k):
        start = t + b * L
        block = bank[start:start + L]

        def src():
            for lam in block:
                x = coords(lam)
                if x is None:
                    raise LookupError("label outside W")
                yield x

        S = Stream(p, dimW, rng, source=src(), cap=L)
        sol = Solver(p, S)
        try:
            w = sol.solve(0, dimW, np.zeros(dimW, dtype=np.int64))
        except Overrun:
            continue
        except LookupError:
            return ("abort", "outside_W", M)
        T = [start + i for i in w]
        assert all(v == 1 for v in w.values()) and len(T) > 0
        assert not (bank[T].sum(axis=0) % p).any()   # exact check in F_p^g
        return ("ok", len(T), M)
    return ("abort", "all_blocks_overrun", M)


def part_node(seed=13):
    rng = np.random.default_rng(seed)
    out = {"rows": [], "overrun": []}
    plan = [(3, 4, 0.05, 300), (3, 8, 0.05, 200), (3, 12, 0.05, 100),
            (5, 4, 0.05, 150), (5, 6, 0.05, 80),
            (7, 3, 0.05, 120), (7, 5, 0.05, 40),
            (11, 3, 0.05, 60),
            (3, 8, 0.5, 300), (5, 4, 0.5, 200), (7, 3, 0.5, 200), (11, 2, 0.5, 200)]
    for p, g, tau, trials in plan:
        N = N_table(p, g)
        N0g = N[0][g]
        ab = {"outside_W": 0, "all_blocks_overrun": 0}
        sizes = []
        t0 = time.time()
        for _ in range(trials):
            a = int(rng.integers(0, g + 1))
            res = run_node(p, g, a, tau, rng, N0g)
            if res[0] == "ok":
                sizes.append(res[1])
            else:
                ab[res[1]] += 1
            M = res[2]
        t, L, k, M = node_params(p, g, tau, N0g)
        row = {"p": p, "g": g, "tau": tau, "t": t, "L": L, "k": k, "M": M,
               "trials": trials, "aborts": ab, "abort_rate": sum(ab.values()) / trials,
               "mean_support": float(np.mean(sizes)) if sizes else None,
               "davenport": g * (p - 1) + 1, "secs": round(time.time() - t0, 1)}
        out["rows"].append(row)
        print(row, flush=True)
    # per-block overrun probability at full dimension a = g vs Markov 1/2
    for p, g, runs in [(3, 8, 400), (5, 4, 300), (7, 3, 300), (11, 2, 300)]:
        N = N_table(p, g)
        L = math.ceil(2 * N[0][g])
        over = 0
        Rs = []
        for _ in range(runs):
            R, _ = run_once(p, g, rng)
            Rs.append(R)
            over += R > L
        out["overrun"].append({"p": p, "g": g, "L": L, "runs": runs,
                               "Pr_R_gt_L": over / runs, "markov": 0.5,
                               "Pr_R_gt_N0": float(np.mean(np.array(Rs) > float(N[0][g])))})
        print(out["overrun"][-1], flush=True)
    # arity vs g at tau = 1e-3 (exact N_0), log-log slope
    ar = []
    for p in [3, 5, 7, 11]:
        N = N_table(p, 256)
        Ms = {}
        for g in [8, 16, 32, 64, 128, 256]:
            Ms[g] = node_params(p, g, Fraction(1, 1000), N[0][g])[3]
        slopes = {f"{g}->{2*g}": math.log2(Ms[2 * g] / Ms[g]) for g in [8, 16, 32, 64, 128]}
        ar.append({"p": p, "c": p - 1, "degree_claimed": 1 + jstar(p),
                   "schedule1_degree": (p - 1) * math.ceil(math.log2(p)),
                   "M": Ms, "slopes": slopes})
        print(ar[-1], flush=True)
    out["arity_vs_g"] = ar
    return out


def part_neg(seed=14):
    rng = np.random.default_rng(seed)
    out = {}
    # (1) non-uniform i.i.d. columns: {0,1} entries at p = 7.  The exact
    # expectation N_0 is derived for uniform columns only; expect a clear z.
    rows = []
    for p, n, runs in [(7, 4, 40), (7, 6, 30), (5, 6, 40)]:
        N = N_table(p, n)
        R = [run_once(p, n, rng, law="bernoulli")[0] for _ in range(runs)]
        m, se = float(np.mean(R)), float(np.std(R, ddof=1) / math.sqrt(runs))
        rows.append({"p": p, "n": n, "law": "bernoulli{0,1}", "runs": runs, "mean": m,
                     "se": se, "uniform_N0": float(N[0][n]), "z": (m - float(N[0][n])) / se})
        print(rows[-1], flush=True)
    out["biased_columns"] = rows
    # (2) structured bank: span is all of F_p^g but every later label has
    # v_g = v_1.  Every beta at the top dimension vanishes; the node must
    # abort with probability 1 and never return a wrong witness.
    rows = []
    for p, g, tau, trials in [(3, 4, 0.05, 30), (5, 3, 0.05, 30), (7, 3, 0.05, 20)]:
        N = N_table(p, g)
        ab = 0
        for _ in range(trials):
            res = run_node(p, g, g, tau, rng, N[0][g], bank_law="hyperplane")
            ab += res[0] == "abort"
        rows.append({"p": p, "g": g, "tau": tau, "trials": trials, "aborts": ab})
        print(rows[-1], flush=True)
    out["hyperplane_bank"] = rows
    return out


if __name__ == "__main__":
    part = sys.argv[1]
    outpath = sys.argv[2]
    res = {}
    t0 = time.time()
    if part in ("exact", "all"):
        res["exact"] = part_exact()
    if part in ("reads", "all"):
        res["reads"] = part_reads()
    if part in ("indep", "all"):
        res["indep"] = part_indep()
    if part in ("node", "all"):
        res["node"] = part_node()
    if part in ("neg", "all"):
        res["neg"] = part_neg()
    res["secs"] = round(time.time() - t0, 1)
    with open(outpath, "w") as f:
        json.dump(res, f, indent=1, default=str)
    print("done", res["secs"])
