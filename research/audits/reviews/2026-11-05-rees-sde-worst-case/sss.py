"""Source-steered block solver (SSS) for the diagonal SDE target.

Problem: columns lam_1..lam_M in F_p^a, kappa | p-1, P = nonzero kappa-th powers.
Find x in (P u {0})^M, x != 0, with sum_i x_i lam_i = 0.

Algorithm (see ../2026-11-05-rees-sde-worst-case.md, Section 3):
  0. r = rank; reserve a basis B (r input columns) of V = span of all columns.
  1. Forward pass on the other columns: scan unused columns, keep a set T independent
     modulo U; the first column c dependent on U + span T gives a circuit S modulo U
     (support of the unique relation).  |S| = 1 means c in U: c goes to the pool.
     Otherwise split supp(delta) into min(E,|S|) blocks refining the coset classes,
     add W_1..W_{E_l-1} to U.  A monochromatic circuit with e = 0 is a solution.
     Stop when dim U = r ("ok") or when the unused non-pool columns run out ("stall").
  2. Backward pass: tau = -sum_k t_k sigma_k, t_k uniform in P, sigma_k in B; for
     l = L..1 decompose tau, draw s uniformly in Good_l(beta), set weights
     x_i = delta_i (beta_b + s), tau <- tau - value.  Fail if some Good set is empty.
Everything is exact integer arithmetic.  Output is verified.
"""
import random


class Field:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k, self.h = p, k, (p - 1) // k
        g = 2
        while not self._primroot(g):
            g += 1
        self.g = g
        z = pow(g, self.h, p)
        self.zlog = {pow(z, j, p): j for j in range(k)}
        self.P = sorted({pow(y, k, p) for y in range(1, p)})

    def _primroot(self, g):
        p, n, f, fac = self.p, self.p - 1, 2, []
        while f * f <= n:
            if n % f == 0:
                fac.append(f)
                while n % f == 0:
                    n //= f
            f += 1
        if n > 1:
            fac.append(n)
        return all(pow(g, (p - 1) // q, p) != 1 for q in fac)

    def cls(self, y):
        return self.zlog[pow(y % self.p, self.h, self.p)]

    def in_class0(self, y, c):
        """y in Q_c u {0}."""
        y %= self.p
        return y == 0 or self.cls(y) == c % self.k

    def randP(self, rng):
        return self.P[rng.randrange(len(self.P))]


def solve_in_span(basis, v, p):
    """Coordinates c with sum c_j basis_j = v, or None.  basis: list of vectors."""
    n = len(basis)
    a = len(v)
    # augmented matrix a x (n+1)
    A = [[basis[j][i] % p for j in range(n)] + [v[i] % p] for i in range(a)]
    piv, row = [], 0
    for col in range(n):
        pr = next((r for r in range(row, a) if A[r][col]), None)
        if pr is None:
            continue
        A[row], A[pr] = A[pr], A[row]
        iv = pow(A[row][col], p - 2, p)
        A[row] = [x * iv % p for x in A[row]]
        for r in range(a):
            if r != row and A[r][col]:
                f = A[r][col]
                A[r] = [(x - f * y) % p for x, y in zip(A[r], A[row])]
        piv.append(col)
        row += 1
    for r in range(row, a):
        if A[r][n]:
            return None
    c = [0] * n
    for r, col in enumerate(piv):
        c[col] = A[r][n]
    # free columns (dependent basis) set to 0: fine for our use (basis is independent)
    return c


def rank(vecs, p):
    basis = []
    for v in vecs:
        if solve_in_span(basis, v, p) is None:
            basis.append(v)
    return len(basis), basis


class Round:
    pass


def split_blocks(Fd, S, delta, E, rng, rule):
    """Partition S into min(E,|S|) blocks refining the classes of delta."""
    classes = {}
    for i in S:
        classes.setdefault(Fd.cls(delta[i]), []).append(i)
    blocks = [list(v) for _, v in sorted(classes.items())]
    target = min(E, len(S))
    while len(blocks) < target:
        big = max(range(len(blocks)), key=lambda b: len(blocks[b]))
        G = blocks[big]
        if rule == "random":
            G = G[:]
            rng.shuffle(G)
            cut = rng.randrange(1, len(G))
        else:
            cut = 1
        blocks[big] = G[:cut]
        blocks.append(G[cut:])
    return blocks


def forward(Fd, cols, E, rng, reserve, rule="random", order=None):
    p = Fd.p
    a = len(cols[0])
    r = rank(cols, p)[0]
    unused = [i for i in (order if order is not None else range(len(cols))) if i not in reserve]
    Ubasis = []          # list of vectors (W's), in flag order
    rounds, pool = [], []
    while len(Ubasis) < r:
        T, found = [], None
        for c in unused:
            co = solve_in_span(Ubasis + [cols[i] for i in T], cols[c], p)
            if co is None:
                T.append(c)
                continue
            delta = {c: 1}
            for j, i in enumerate(T):
                t = co[len(Ubasis) + j]
                if t:
                    delta[i] = (-t) % p
            found = (c, delta)
            break
        if found is None:
            return rounds, Ubasis, pool, "stall"
        c, delta = found
        S = sorted(delta)
        if len(S) == 1:
            pool.append(c)
            unused.remove(c)
            continue
        for i in S:
            unused.remove(i)
        e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        if len({Fd.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = Fd.cls(delta[S[0]])
            zeta = pow(Fd.g, (-cc) % Fd.k, p)
            x = [0] * len(cols)
            for i in S:
                x[i] = zeta * delta[i] % p
            return rounds, Ubasis, pool, ("direct", x)
        R = Round()
        R.S, R.delta, R.e = S, delta, e
        R.blocks = split_blocks(Fd, S, delta, E, rng, rule)
        R.bclass = [Fd.cls(delta[G[0]]) for G in R.blocks]
        R.W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(a)] for G in R.blocks]
        R.start = len(Ubasis)              # coordinates of W_1.. in the flag
        Ubasis += R.W[1:]
        R.end = len(Ubasis)
        rounds.append(R)
    return rounds, Ubasis, pool, "ok"


def good_draw(Fd, beta, bclass, rng, exhaustive=30000, trials=200000):
    """Uniform s with beta_b + s in Q_{-c_b} u {0} for all b; None if empty."""
    p = Fd.p
    ok = lambda s: all(Fd.in_class0(beta[b] + s, -bclass[b]) for b in range(len(beta)))
    if p <= exhaustive:
        G = [s for s in range(p) if ok(s)]
        return (rng.choice(G), len(G)) if G else (None, 0)
    for _ in range(trials):
        s = rng.randrange(p)
        if ok(s):
            return s, -1
    return None, 0


def backward(Fd, cols, rounds, Ubasis, sources, rng):
    p = Fd.p
    a = len(cols[0])
    x = [0] * len(cols)
    tau = [0] * a
    for k in sources:
        t = Fd.randP(rng)
        x[k] = t
        tau = [(u - t * v) % p for u, v in zip(tau, cols[k])]
    minG = None
    for R in reversed(rounds):
        co = solve_in_span(Ubasis[:R.end], tau, p)
        assert co is not None
        beta = [0] + co[R.start:R.end]
        s, g = good_draw(Fd, beta, R.bclass, rng)
        if s is None:
            return None, "emptyGood"
        if g > 0:
            minG = g if minG is None else min(minG, g)
        for b, G in enumerate(R.blocks):
            for i in G:
                x[i] = R.delta[i] * (beta[b] + s) % p
        val = [sum(x[i] * cols[i][t] for i in R.S) % p for t in range(a)]
        tau = [(u - v) % p for u, v in zip(tau, val)]
    if any(tau):
        return None, "residual"   # must not happen
    return x, "ok"


def check(Fd, cols, x):
    p = Fd.p
    if x is None or not any(x):
        return False
    if any(xi and Fd.cls(xi) != 0 for xi in x):
        return False
    return all(sum(x[i] * cols[i][t] for i in range(len(cols))) % p == 0 for t in range(len(cols[0])))


def sss(Fd, cols, E, rng, passes=30, rule="random", forwards=1):
    """Returns (x or None, status)."""
    p = Fd.p
    if any(not any(c) for c in cols):
        i = next(i for i, c in enumerate(cols) if not any(c))
        x = [0] * len(cols)
        x[i] = 1
        return x, "zero column"
    last = None
    for f in range(forwards):
        order = list(range(len(cols)))
        if f > 0:
            rng.shuffle(order)
        r, B = 0, []
        reserve, bas = [], []
        for i in order:
            if solve_in_span(bas, cols[i], p) is None:
                bas.append(cols[i])
                reserve.append(i)
        rounds, Ub, pool, st = forward(Fd, cols, E, rng, set(reserve), rule, order)
        if isinstance(st, tuple):
            assert check(Fd, cols, st[1])
            return st[1], "direct"
        if st == "stall":
            last = "stall"
            continue
        for _ in range(passes):
            x, s2 = backward(Fd, cols, rounds, Ub, reserve, rng)
            if x is not None:
                assert check(Fd, cols, x), "invalid witness"
                return x, "ok"
            last = s2
    return None, last


def count_used(a, E):
    """Forward cost when every round is a full circuit, plus a reserved basis: M_E(a) - 1 + a."""
    q, M = a, 0
    while q >= 1:
        M += q + 1
        q -= min(E - 1, q)
    return M + a


def worst_forward_cost(q, E, memo=None):
    """max over greedy runs of columns consumed by rounds to reach quotient 0, where a
    round at quotient q uses a circuit of k+1 columns (1<=k<=q) and gains min(E-1,k)."""
    if memo is None:
        memo = {}
    if q == 0:
        return 0
    if q in memo:
        return memo[q]
    best = max(k + 1 + worst_forward_cost(q - min(E - 1, k), E, memo) for k in range(1, q + 1))
    memo[q] = best
    return best


# ---------------------------------------------------------------------------
# Variant with basis swaps and subspace recursion (Section 4 of the report)
# ---------------------------------------------------------------------------

def forward_swap(Fd, cols, E, rng, reserve, rule="random", order=None):
    """As forward(), but a column z found in U is swapped into the reserved basis B
    when its B-expansion has a nonzero coefficient on some sigma in B outside U
    (sigma is released to the unused list); otherwise z is a true pool column."""
    p = Fd.p
    a = len(cols[0])
    r = len(reserve)
    B = list(reserve)
    unused = [i for i in (order if order is not None else range(len(cols))) if i not in set(B)]
    Ubasis, rounds, pool, swaps = [], [], [], 0
    while len(Ubasis) < r:
        T, found = [], None
        for c in unused:
            co = solve_in_span(Ubasis + [cols[i] for i in T], cols[c], p)
            if co is None:
                T.append(c)
                continue
            delta = {c: 1}
            for j, i in enumerate(T):
                t = co[len(Ubasis) + j]
                if t:
                    delta[i] = (-t) % p
            found = (c, delta)
            break
        if found is None:
            return dict(rounds=rounds, U=Ubasis, pool=pool, B=B, status="stall", swaps=swaps)
        c, delta = found
        S = sorted(delta)
        if len(S) == 1:
            unused.remove(c)
            cb = solve_in_span([cols[i] for i in B], cols[c], p)
            out = [B[j] for j in range(r) if cb[j] and solve_in_span(Ubasis, cols[B[j]], p) is None]
            if out:
                sig = out[0]
                B[B.index(sig)] = c
                unused.append(sig)
                swaps += 1
            else:
                pool.append(c)
            continue
        for i in S:
            unused.remove(i)
        e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        if len({Fd.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = Fd.cls(delta[S[0]])
            zeta = pow(Fd.g, (-cc) % Fd.k, p)
            x = [0] * len(cols)
            for i in S:
                x[i] = zeta * delta[i] % p
            return dict(status="direct", x=x)
        R = Round()
        R.S, R.delta, R.e = S, delta, e
        R.blocks = split_blocks(Fd, S, delta, E, rng, rule)
        R.bclass = [Fd.cls(delta[G[0]]) for G in R.blocks]
        R.W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(a)] for G in R.blocks]
        R.start = len(Ubasis)
        Ubasis += R.W[1:]
        R.end = len(Ubasis)
        rounds.append(R)
    return dict(rounds=rounds, U=Ubasis, pool=pool, B=B, status="ok", swaps=swaps)


def budget(r, E):
    return worst_forward_cost(r, E) + r


def coords_in(basisvecs, v, p):
    return solve_in_span(basisvecs, v, p)


def restrict(cols_idx, cols, span_basis, p):
    """Express the columns cols_idx in coordinates of span_basis (a basis of a subspace)."""
    return [coords_in(span_basis, cols[i], p) for i in cols_idx]


def sss_rec(Fd, cols, E, rng, passes=20, rule="random", depth=0, stats=None):
    """Recursive SSS: on a stall, recurse on the columns lying in U_L or in span(B cap U_L)
    when there are at least budget(dim, E) of them.  Returns (x, status)."""
    p = Fd.p
    if stats is None:
        stats = {}
    n = len(cols)
    for i, c in enumerate(cols):
        if not any(c):
            x = [0] * n
            x[i] = 1
            return x, "zero column"
    # three columns on one line: a one-dimensional instance (budget(1) = 3)
    if rank(cols, p)[0] > 1:
        lines = {}
        for i, c in enumerate(cols):
            j = next(t for t in range(len(c)) if c[t])
            iv = pow(c[j], p - 2, p)
            lines.setdefault(tuple(x * iv % p for x in c), []).append(i)
        for key, idx in lines.items():
            if len(idx) >= 3:
                sc = [[cols[i][next(t for t in range(len(key)) if key[t])]] for i in idx[:3]]
                y, st = sss_rec(Fd, sc, E, rng, passes, rule, depth + 1, stats)
                if y is not None:
                    x = [0] * n
                    for j2, i in enumerate(idx[:3]):
                        x[i] = y[j2]
                    assert check(Fd, cols, x)
                    return x, "ok(line)"
    # coloops (columns outside the span of the others) carry weight 0 in every solution
    rfull = rank(cols, p)[0]
    keep = [i for i in range(n) if rank(cols[:i] + cols[i + 1:], p)[0] == rfull]
    if len(keep) < n:
        if not keep:
            return None, "all coloops"
        sub = rank([cols[i] for i in keep], p)[1]
        sc = restrict(keep, cols, sub, p)
        y, st = sss_rec(Fd, sc, E, rng, passes, rule, depth, stats)
        if y is None:
            return None, st
        x = [0] * n
        for j, i in enumerate(keep):
            x[i] = y[j]
        assert check(Fd, cols, x)
        return x, st + "[coloops]"
    order = list(range(n))
    reserve, bas = [], []
    for i in order:
        if solve_in_span(bas, cols[i], p) is None:
            bas.append(cols[i])
            reserve.append(i)
    r = len(reserve)
    res = forward_swap(Fd, cols, E, rng, reserve, rule, order)
    stats["swaps"] = stats.get("swaps", 0) + res.get("swaps", 0)
    if res["status"] == "direct":
        assert check(Fd, cols, res["x"])
        return res["x"], "direct"
    if res["status"] == "ok":
        for _ in range(passes):
            x, s2 = backward(Fd, cols, res["rounds"], res["U"], res["B"], rng)
            if x is not None:
                assert check(Fd, cols, x)
                return x, "ok" if depth == 0 else "ok(rec%d)" % depth
        return None, "emptyGood"
    # stall: try subspaces
    if depth == 0:
        stats["last_res"] = res
    UL = res["U"]
    cand = []
    if UL:
        rb, Ubas = rank(UL, p)
        inU = [i for i in range(n) if solve_in_span(Ubas, cols[i], p) is not None]
        cand.append((inU, Ubas))
    BinU = [cols[i] for i in res["B"] if UL and solve_in_span(UL, cols[i], p) is not None]
    if BinU:
        yb, Ybas = rank(BinU, p)
        inY = [i for i in range(n) if solve_in_span(Ybas, cols[i], p) is not None]
        cand.append((inY, Ybas))
    for idx, sb in cand:
        rk = rank([cols[i] for i in idx], p)[0] if idx else 0
        if idx and len(idx) >= budget(rk, E) and rk < r:
            sub = rank([cols[i] for i in idx], p)[1]
            sc = restrict(idx, cols, sub, p)
            y, st = sss_rec(Fd, sc, E, rng, passes, rule, depth + 1, stats)
            if y is not None:
                x = [0] * n
                for j, i in enumerate(idx):
                    x[i] = y[j]
                assert check(Fd, cols, x)
                return x, st
    return None, "stall(pool=%d,codim=%d)" % (len(res["pool"]), r - len(UL))


def finish_stall(Fd, cols, E, rng, res, passes=20, rule="random"):
    """Fallback F1 after a stall at U_L: continue the forward pass on T u (B \\ U_L),
    putting a block that contains a B column in position >= 1 when possible, then run
    the backward pass with sources = unused B columns and pool columns."""
    p = Fd.p
    a = len(cols[0])
    rounds, Ub = list(res["rounds"]), list(res["U"])
    B = list(res["B"])
    r = len(B)
    used = set(i for R in rounds for i in R.S) | set(B) | set(res["pool"])
    T = [i for i in range(len(cols)) if i not in used]
    Bout = [i for i in B if solve_in_span(Ub, cols[i], p) is None]
    unused = T + Bout
    Bset = set(B)
    while len(Ub) < r:
        TT, found = [], None
        for c in unused:
            co = solve_in_span(Ub + [cols[i] for i in TT], cols[c], p)
            if co is None:
                TT.append(c)
                continue
            delta = {c: 1}
            for j, i in enumerate(TT):
                t = co[len(Ub) + j]
                if t:
                    delta[i] = (-t) % p
            found = (c, delta)
            break
        if found is None:
            return None, "stall2"
        c, delta = found
        S = sorted(delta)
        unused = [i for i in unused if i not in delta]
        if len(S) == 1:
            continue
        R = Round()
        R.S, R.delta = S, delta
        R.e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        bl = split_blocks(Fd, S, delta, E, rng, rule)
        # put a block without B columns first if possible
        nb = [b for b in range(len(bl)) if not (set(bl[b]) & Bset)]
        if nb:
            bl = [bl[nb[0]]] + [bl[b] for b in range(len(bl)) if b != nb[0]]
        R.blocks = bl
        R.bclass = [Fd.cls(delta[G[0]]) for G in bl]
        R.W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(a)] for G in bl]
        R.start = len(Ub)
        Ub += R.W[1:]
        R.end = len(Ub)
        rounds.append(R)
    usedB = set(i for R in rounds for i in R.S) & Bset
    sources = [i for i in B if i not in usedB] + list(res["pool"])
    if not sources:
        return None, "nosources"
    for _ in range(passes):
        x, s2 = backward(Fd, cols, rounds, Ub, sources, rng)
        if x is not None:
            assert check(Fd, cols, x)
            return x, "ok(finish)"
    return None, "emptyGood(finish)"


def sss_full(Fd, cols, E, rng, passes=20, rule="random", forwards=3):
    """Recursive SSS, then F1 on a stall, then random column orders."""
    best = None
    for f in range(forwards):
        perm = list(range(len(cols)))
        if f:
            rng.shuffle(perm)
        pc = [cols[i] for i in perm]
        stats = {}
        x, st = sss_rec(Fd, pc, E, rng, passes, rule, stats=stats)
        if x is None and st.startswith("stall"):
            x, st2 = finish_stall(Fd, pc, E, rng, stats["last_res"], passes, rule)
            st = st2 if x is not None else st + "/" + st2
        if x is not None:
            y = [0] * len(cols)
            for j, i in enumerate(perm):
                y[i] = x[j]
            assert check(Fd, cols, y)
            return y, st + ("" if f == 0 else "[order%d]" % f)
        best = st
    return None, best


def sss_theorem(Fd, cols, E, rng, passes=20, rule="random"):
    """Exactly the algorithm of Theorem 2: reserved basis, greedy circuits with swaps,
    sources = final B.  No recursion, no fallback.  Returns (x, status, n_true_pool)."""
    p = Fd.p
    for i, c in enumerate(cols):
        if not any(c):
            x = [0] * len(cols)
            x[i] = 1
            return x, "zero column", 0
    reserve, bas = [], []
    for i in range(len(cols)):
        if solve_in_span(bas, cols[i], p) is None:
            bas.append(cols[i])
            reserve.append(i)
    res = forward_swap(Fd, cols, E, rng, reserve, rule)
    if res["status"] == "direct":
        assert check(Fd, cols, res["x"])
        return res["x"], "direct", 0
    if res["status"] == "stall":
        return None, "stall", len(res["pool"])
    for _ in range(passes):
        x, s2 = backward(Fd, cols, res["rounds"], res["U"], res["B"], rng)
        if x is not None:
            assert check(Fd, cols, x)
            return x, "ok", len(res["pool"])
    return None, "emptyGood", len(res["pool"])
