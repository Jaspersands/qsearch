"""Referee's independent implementation of ALG-T (Theorem A of
2026-11-07-rees-sde-subquad-A.md), written from the text of the report and its inputs.
Imports nothing from the agent's folders.

Differences from the agent's code (deliberate, so that the two are not the same program):
  * own echelon linear algebra with coefficient tracking;
  * forward pass: the swap removes the LAST eligible reserved column; blocks are made by
    splitting the SMALLEST class of size >= 2 and peeling its LAST element;
  * matroid intersection: own augmenting-path implementation with a different exchange-graph
    layout; the Edmonds certificate r1(Z) + r2(Rout - Z) = |I| is verified; on small
    instances the maximum is also cross-checked by brute force;
  * absorption order: the chosen I is absorbed in REVERSE order;
  * backward pass: Good enumerated exactly (p <= 60000) or by rejection with the forced
    value tested directly on a cross-class coincidence; every witness is re-verified by a
    separate function `verify` (pow test for P).
Every inequality of the proof is asserted at run time (strict), and every leaf is checked
for (F1), (F2) and (S) by independent code.  A violated assertion is a counterexample to
the bookkeeping of the proof; an unsolved bank (all passes fail) is recorded.
"""
import random
from collections import Counter
from fractions import Fraction

# ---------------------------------------------------------------------------
# field
# ---------------------------------------------------------------------------


class Fld:
    def __init__(self, p, k):
        assert (p - 1) % k == 0 and p > 2
        self.p, self.k, self.h = p, k, (p - 1) // k
        n, f, fac = p - 1, 2, []
        while f * f <= n:
            if n % f == 0:
                fac.append(f)
                while n % f == 0:
                    n //= f
            f += 1
        if n > 1:
            fac.append(n)
        g = 2
        while any(pow(g, (p - 1) // q, p) == 1 for q in fac):
            g += 1
        self.g = g
        z = pow(g, self.h, p)
        self.zlog = {pow(z, j, p): j for j in range(k)}
        self.Plist = sorted({pow(y, k, p) for y in range(1, p)})

    def cls(self, y):
        """coset index nu with y in g^nu P."""
        return self.zlog[pow(y % self.p, self.h, self.p)]

    def inQ0(self, y, c):
        """y in Q_c u {0}."""
        y %= self.p
        return y == 0 or self.cls(y) == c % self.k

    def randP(self, rng):
        return self.Plist[rng.randrange(len(self.Plist))]

    def isP(self, y):
        return y % self.p != 0 and pow(y % self.p, self.h, self.p) == 1


# ---------------------------------------------------------------------------
# linear algebra: incremental echelon basis with coefficient tracking
# ---------------------------------------------------------------------------


class Ech:
    """Rows kept in reduced form w.r.t. their pivots.  Each row carries a dict 'comb' giving it
    as a combination of the tagged vectors added (tag None = untracked)."""

    def __init__(self, p, a):
        self.p, self.a = p, a
        self.rows = []       # list of (pivot, vec, comb)

    def copy(self):
        e = Ech(self.p, self.a)
        e.rows = [(piv, list(v), dict(c)) for piv, v, c in self.rows]
        return e

    def __len__(self):
        return len(self.rows)

    def reduce(self, v, tag=None):
        """Return (residual, comb): v = residual + sum comb[tag']*vec(tag')."""
        p = self.p
        v = [x % p for x in v]
        comb = {}
        for piv, row, rc in self.rows:
            t = v[piv]
            if t:
                for j in range(self.a):
                    if row[j]:
                        v[j] = (v[j] - t * row[j]) % p
                for key, val in rc.items():
                    comb[key] = (comb.get(key, 0) + t * val) % p
        return v, comb

    def add(self, v, tag=None):
        """Add v (if independent).  Returns True if the rank grew."""
        p = self.p
        res, comb = self.reduce(v)
        piv = next((j for j in range(self.a) if res[j]), None)
        if piv is None:
            return False
        inv = pow(res[piv], p - 2, p)
        res = [x * inv % p for x in res]
        # comb: res = inv*(v - sum comb*vecs)  ->  as combination of tagged vectors
        newc = {key: (-val * inv) % p for key, val in comb.items()}
        if tag is not None:
            newc[tag] = (newc.get(tag, 0) + inv) % p
        # keep other rows reduced w.r.t. the new pivot
        for idx, (pv, row, rc) in enumerate(self.rows):
            t = row[piv]
            if t:
                row2 = [(x - t * y) % p for x, y in zip(row, res)]
                rc2 = dict(rc)
                for key, val in newc.items():
                    rc2[key] = (rc2.get(key, 0) - t * val) % p
                self.rows[idx] = (pv, row2, rc2)
        self.rows.append((piv, res, newc))
        return True

    def contains(self, v):
        res, _ = self.reduce(v)
        return not any(res)

    def basis(self):
        return [list(v) for _, v, _ in self.rows]


def rank_of(vecs, p, a):
    e = Ech(p, a)
    for v in vecs:
        e.add(v)
    return len(e)


def span_basis(vecs, p, a):
    e = Ech(p, a)
    for v in vecs:
        e.add(v)
    return e


def coords(E, v):
    """coordinates of v in the ORDER of E's tagged additions (tags 0..n-1), or None."""
    res, comb = E.reduce(v)
    if any(res):
        return None
    return [comb.get(i, 0) for i in range(len(E))]


def vadd(u, v, p):
    return [(x + y) % p for x, y in zip(u, v)]


def vscale(t, v, p):
    return [t * x % p for x in v]


# ---------------------------------------------------------------------------
# counts
# ---------------------------------------------------------------------------

_D = {}


def DJ(q, J):
    tab = _D.setdefault(J, [0])
    while len(tab) <= q:
        x = len(tab)
        tab.append(max(k + 1 + tab[x - min(J - 1, k)] for k in range(1, x + 1)))
    return tab[q]


class Params:
    def __init__(self, J, kappa, c=None, C=None, passes=40):
        assert J >= max(kappa, 2)
        self.J, self.kappa = J, kappa
        self.c = 2 * (J - 1) if c is None else c
        self.C = max(2, 2 * J - 4) if C is None else C
        self.passes = passes
        self.E = J + self.c

    def F(self, r):
        return DJ(r, self.J) + self.C * r if r > 0 else 0


# ---------------------------------------------------------------------------
# rounds, flags
# ---------------------------------------------------------------------------


class Round:
    __slots__ = ("S", "delta", "blocks", "bclass", "W", "e", "start", "end", "extra")

    def __init__(self, Fd, cols, S, delta, blocks):
        p, a = Fd.p, len(cols[0])
        self.S = sorted(S)
        self.delta = dict(delta)
        self.blocks = [list(G) for G in blocks]
        self.bclass = [Fd.cls(delta[G[0]]) for G in self.blocks]
        for G, c in zip(self.blocks, self.bclass):
            assert all(Fd.cls(delta[i]) == c for i in G), "block not inside a class"
        self.W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(a)] for G in self.blocks]
        self.e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        self.extra = 0


def flag_space(Fd, cols, rounds):
    """Verify (F1), (F2) for the rounds in order; return the tagged echelon basis of U_L
    (tags 0..dim-1 in flag order) or raise."""
    p, a = Fd.p, len(cols[0])
    E = Ech(p, a)
    n = 0
    for R in rounds:
        if not E.contains(R.e):
            raise AssertionError("(F2) fails: e_l not in U_{l-1}")
        R.start = n
        for w in R.W[1:]:
            if not E.add(w, tag=n):
                raise AssertionError("(F1) fails: block sum dependent")
            n += 1
        R.end = n
    return E


def steer_violations(Fd, cols, rounds, UE, src):
    """Number of cross-class pairs (j,b,b') whose functional vanishes on span(Src) and on
    every e_l, l > j.  (S) holds iff this is 0."""
    p = Fd.p
    cs = []
    for s in src:
        c = coords(UE, cols[s])
        assert c is not None, "source outside realized space"
        cs.append(c)
    ce = [coords(UE, R.e) for R in rounds]
    assert all(c is not None for c in ce)
    bad = 0
    for j, R in enumerate(rounds):
        nb = len(R.blocks)
        for b in range(nb):
            for b2 in range(b + 1, nb):
                if R.bclass[b] == R.bclass[b2]:
                    continue

                def phi(c):
                    x = c[R.start + b - 1] if b else 0
                    y = c[R.start + b2 - 1] if b2 else 0
                    return (x - y) % p
                if any(phi(c) for c in cs):
                    continue
                if any(phi(ce[l]) for l in range(j + 1, len(rounds))):
                    continue
                bad += 1
    return bad


def cross_pairs(rounds):
    return sum(1 for R in rounds for b in range(len(R.blocks)) for b2 in range(b + 1, len(R.blocks))
               if R.bclass[b] != R.bclass[b2])


# ---------------------------------------------------------------------------
# block splitting (referee's rule: split the smallest class of size >= 2, peel its last element)
# ---------------------------------------------------------------------------


def split_blocks(Fd, S, delta, J):
    classes = {}
    for i in S:
        classes.setdefault(Fd.cls(delta[i]), []).append(i)
    blocks = [v for _, v in sorted(classes.items(), reverse=True)]
    target = min(J, len(S))
    assert len(blocks) <= target, "more classes than J blocks: need J >= kappa"
    while len(blocks) < target:
        cand = [b for b in range(len(blocks)) if len(blocks[b]) >= 2]
        b = min(cand, key=lambda b: (len(blocks[b]), b))
        G = blocks[b]
        blocks[b] = G[:-1]
        blocks.append([G[-1]])
    return blocks


# ---------------------------------------------------------------------------
# forward pass SSS(J)
# ---------------------------------------------------------------------------


def forward(Fd, cols, J, st, pause_after=None):
    """st: dict with B (list), unused (list), rounds, pool, swaps. Returns 'reached', 'stall',
    'paused' (when the number of rounds reaches pause_after) or ('direct', x)."""
    p, a = Fd.p, len(cols[0])
    r = len(st["B"])
    UE = Ech(p, a)
    for R in st["rounds"]:
        for w in R.W[1:]:
            assert UE.add(w)
    while True:
        if len(UE) == r:
            return "reached"
        if pause_after is not None and len(st["rounds"]) >= pause_after:
            return "paused"
        E2 = UE.copy()
        T, found = [], None
        for ci in st["unused"]:
            res, comb = E2.reduce(cols[ci])
            if any(res):
                E2.add(cols[ci], tag=ci)
                T.append(ci)
                continue
            delta = {ci: 1}
            for i in T:
                t = comb.get(i, 0) % p
                if t:
                    delta[i] = (-t) % p
            found = (ci, delta)
            break
        if found is None:
            st["T"] = T
            return "stall"
        ci, delta = found
        S = sorted(delta)
        if len(S) == 1:
            st["unused"].remove(ci)
            EB = Ech(p, a)
            for s in st["B"]:
                EB.add(cols[s], tag=s)
            res, cb = EB.reduce(cols[ci])
            assert not any(res)
            out = [s for s in st["B"] if cb.get(s, 0) % p and not UE.contains(cols[s])]
            if out:
                sig = out[-1]                      # LAST eligible (agent: first)
                st["B"][st["B"].index(sig)] = ci
                st["unused"].append(sig)
                st["swaps"] += 1
            else:
                st["pool"].append(ci)
            continue
        for i in S:
            st["unused"].remove(i)
        e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        if len({Fd.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = Fd.cls(delta[S[0]])
            zeta = pow(Fd.g, (-cc) % Fd.k, p)
            x = [0] * len(cols)
            for i in S:
                x[i] = zeta * delta[i] % p
            return ("direct", x)
        blocks = split_blocks(Fd, S, delta, J)
        R = Round(Fd, cols, S, delta, blocks)
        st["rounds"].append(R)
        assert UE.contains(R.e), "(F2) in forward"
        for w in R.W[1:]:
            assert UE.add(w), "(F1) in forward"


def init_state(Fd, cols):
    p, a = Fd.p, len(cols[0])
    E = Ech(p, a)
    B = []
    for i, v in enumerate(cols):
        if E.add(v):
            B.append(i)
    unused = [i for i in range(len(cols)) if i not in set(B)]
    return dict(B=B, unused=unused, rounds=[], pool=[], swaps=0, T=[])


# ---------------------------------------------------------------------------
# matroid intersection: linear matroid mod U  x  partition matroid (capacity cap per round)
# ---------------------------------------------------------------------------


def matroid_intersection(Fd, cols, UE, elems, part, cap):
    """Max common independent set I; returns (I, Z) with the Edmonds certificate
    |I| = r1(Z) + r2(elems - Z), where r1 = rank modulo U, r2 = sum_l min(cap, |. cap S_l|).
    Standard augmenting-path algorithm (Schrijver Thm 41.2), own layout."""
    p, a = Fd.p, len(cols[0])
    resid = {}
    for i in elems:
        res, _ = UE.reduce(cols[i])
        resid[i] = res

    def indep1(S):
        return rank_of([resid[i] for i in S], p, a) == len(S)

    def indep2(S):
        return all(v <= cap for v in Counter(part[i] for i in S).values())

    I = set()
    while True:
        out = [x for x in elems if x not in I]
        Il = sorted(I)
        X1 = {x for x in out if indep1(Il + [x])}
        X2 = {x for x in out if indep2(Il + [x])}
        # arcs: y in I -> x not in I if I - y + x in M1 ;  x -> y if I - y + x in M2
        succ = {v: [] for v in elems}
        for y in Il:
            rest = [z for z in Il if z != y]
            for x in out:
                if indep1(rest + [x]):
                    succ[y].append(x)
                if indep2(rest + [x]):
                    succ[x].append(y)
        # BFS from X1
        prev = {}
        queue = []
        for x in sorted(X1):
            prev[x] = None
            queue.append(x)
        end = None
        qi = 0
        while qi < len(queue) and end is None:
            u = queue[qi]
            qi += 1
            if u in X2 and u not in I:
                end = u
                break
            for v in succ[u]:
                if v not in prev:
                    prev[v] = u
                    queue.append(v)
        if end is None:
            reach = set(prev)
            Z = [x for x in elems if x not in reach]
            r1 = rank_of([resid[i] for i in Z], p, a)
            r2 = sum(min(cap, v) for v in Counter(part[i] for i in elems if i in reach).values())
            assert r1 + r2 == len(I), ("Edmonds certificate", r1, r2, len(I))
            assert indep1(Il) and indep2(Il)
            return Il, Z
        path = []
        v = end
        while v is not None:
            path.append(v)
            v = prev[v]
        for v in path:
            if v in I:
                I.remove(v)
            else:
                I.add(v)
        assert indep1(sorted(I)) and indep2(sorted(I)), "augmentation broke independence"


def brute_max_common(Fd, cols, UE, elems, part, cap):
    """Brute-force maximum common independent set size (small instances only)."""
    from itertools import combinations
    p, a = Fd.p, len(cols[0])
    resid = {i: UE.reduce(cols[i])[0] for i in elems}
    best = 0
    for size in range(len(elems), 0, -1):
        for S in combinations(elems, size):
            if all(v <= cap for v in Counter(part[i] for i in S).values()) and \
               rank_of([resid[i] for i in S], p, a) == size:
                return size
    return best


# ---------------------------------------------------------------------------
# absorption (Lemma R)
# ---------------------------------------------------------------------------


def absorb(Fd, cols, rounds, I):
    """Absorb the columns of I (independent mod U) in the given order; returns the new flag
    basis (checks (F1)/(F2) after every step)."""
    where = {i: l for l, R in enumerate(rounds) for i in R.S}
    for i in I:
        UE = flag_space(Fd, cols, rounds)
        assert not UE.contains(cols[i]), "absorbed column already realized"
        l = where[i]
        R = rounds[l]
        b = next(b for b, G in enumerate(R.blocks) if i in G)
        G = R.blocks[b]
        assert len(G) >= 2, "Lemma R: column outside U in a singleton block"
        blocks = R.blocks[:b] + [[j for j in G if j != i]] + R.blocks[b + 1:] + [[i]]
        R2 = Round(Fd, cols, R.S, R.delta, blocks)
        R2.extra = R.extra + 1
        rounds[l] = R2
        UE2 = flag_space(Fd, cols, rounds)
        assert len(UE2) == len(UE) + 1
    return flag_space(Fd, cols, rounds)


# ---------------------------------------------------------------------------
# backward pass (Lemma 2)
# ---------------------------------------------------------------------------


def good_set(Fd, beta, bclass):
    p = Fd.p
    return [s for s in range(p) if all(Fd.inQ0(bb + s, -c) for bb, c in zip(beta, bclass))]


def draw_good(Fd, beta, bclass, rng, trials=20000):
    p = Fd.p
    # cross-class coincidence -> forced value
    for b in range(len(beta)):
        for b2 in range(b + 1, len(beta)):
            if beta[b] == beta[b2] and bclass[b] != bclass[b2]:
                s = (-beta[b]) % p
                return (s if all(Fd.inQ0(bb + s, -c) for bb, c in zip(beta, bclass)) else None), True
    if p <= 60000:
        G = good_set(Fd, beta, bclass)
        return (G[rng.randrange(len(G))] if G else None), False
    for _ in range(trials):
        s = rng.randrange(p)
        if all(Fd.inQ0(bb + s, -c) for bb, c in zip(beta, bclass)):
            return s, False
    return None, False


def backward(Fd, cols, rounds, UE, src, rng):
    """One back substitution.  Returns (x or None, info) where info records whether a
    cross-class coincidence occurred."""
    p, a = Fd.p, len(cols[0])
    x = [0] * len(cols)
    tau = [0] * a
    for s in src:
        t = Fd.randP(rng)
        x[s] = t
        tau = [(u - t * v) % p for u, v in zip(tau, cols[s])]
    coinc = False
    for R in reversed(rounds):
        co = coords(UE, tau)
        assert co is not None, "residual left the realized space"
        assert all(c == 0 for c in co[R.end:]), "residual not in U_l"
        beta = [0] + co[R.start:R.end]
        s, cflag = draw_good(Fd, beta, R.bclass, rng)
        coinc |= cflag
        if s is None:
            return None, dict(coinc=coinc, fail=True)
        for b, G in enumerate(R.blocks):
            for i in G:
                x[i] = R.delta[i] * (beta[b] + s) % p
        val = [sum(x[i] * cols[i][t] for i in R.S) % p for t in range(a)]
        tau = [(u - v) % p for u, v in zip(tau, val)]
    assert not any(tau), "telescoping failed"
    return x, dict(coinc=coinc, fail=False)


def verify(Fd, cols, x):
    p = Fd.p
    if x is None or not any(v % p for v in x):
        return False
    if not all(v % p == 0 or Fd.isP(v) for v in x):
        return False
    a = len(cols[0])
    return all(sum(x[i] * cols[i][t] for i in range(len(cols))) % p == 0 for t in range(a))


# ---------------------------------------------------------------------------
# ALG-T
# ---------------------------------------------------------------------------


class Unsolved(Exception):
    pass


def leaf(Fd, cols, rounds, UE, src, P, rng, stats, kind):
    assert src, "empty Src"
    used = {i for R in rounds for i in R.S}
    assert not (used & set(src)), "source inside a round"
    assert all(UE.contains(cols[s]) for s in src), "span(Src) not inside realized space"
    nb = max(len(R.blocks) for R in rounds) if rounds else 0
    assert nb <= P.E, ("too many blocks", nb, P.E)
    bad = steer_violations(Fd, cols, rounds, UE, src)
    assert bad == 0, ("(S) violated at leaf", kind, bad)
    rho = cross_pairs(rounds)
    assert 2 * rho <= P.E * len(UE), "rho bound"
    stats["leaf:" + kind] += 1
    stats["maxblocks"] = max(stats["maxblocks"], nb)
    stats["maxload"] = max(stats["maxload"], max([R.extra for R in rounds] + [0]))
    stats["maxrho"] = max(stats["maxrho"], rho)
    for k in range(P.passes):
        x, info = backward(Fd, cols, rounds, UE, src, rng)
        stats["passes"] += 1
        stats["coinc"] += info["coinc"]
        if x is not None:
            assert verify(Fd, cols, x), "invalid witness"
            stats["pass_fail"] += k
            return x
        stats["pass_fail_total"] += 1
    raise Unsolved(kind)


def recurse(Fd, cols, WE, P, rng, stats, depth, kind, r):
    p = Fd.p
    idx = [i for i in range(len(cols)) if WE.contains(cols[i])]
    dimW = len(WE)
    assert 0 < dimW < r, ("flat not proper", dimW, r)
    assert len(idx) >= P.F(dimW), ("recursion count fails", kind, len(idx), P.F(dimW), dimW)
    stats["rec:" + kind] += 1
    stats["minslack"] = min(stats.get("minslack", 10 ** 9), len(idx) - P.F(dimW))
    sub = [cols[i] for i in idx]
    y = solve_T(Fd, sub, P, rng, stats, depth + 1)
    x = [0] * len(cols)
    for j, i in enumerate(idx):
        x[i] = y[j]
    assert verify(Fd, cols, x)
    return x


def solve_T(Fd, cols, P, rng, stats=None, depth=0):
    p, a = Fd.p, len(cols[0])
    J, c, C = P.J, P.c, P.C
    if stats is None:
        stats = Counter()
        stats["maxblocks"] = stats["maxload"] = stats["maxrho"] = 0
    M = len(cols)
    for i, v in enumerate(cols):
        if not any(x % p for x in v):
            x = [0] * M
            x[i] = 1
            stats["zero"] += 1
            return x
    r = rank_of(cols, p, a)
    assert M >= P.F(r), ("budget", M, P.F(r))
    stats["maxdepth"] = max(stats["maxdepth"], depth)
    st = init_state(Fd, cols)
    status = forward(Fd, cols, J, st)
    if isinstance(status, tuple):
        assert verify(Fd, cols, status[1])
        stats["direct"] += 1
        return status[1]
    rounds, B = st["rounds"], st["B"]
    UE = flag_space(Fd, cols, rounds)
    if status == "reached":
        assert len(UE) == r
        return leaf(Fd, cols, rounds, UE, B, P, rng, stats, "reachV")
    # ------------------------------------------------------------------ stall
    q = r - len(UE)
    assert q >= 1
    T, pool = st["T"], st["pool"]
    Rcols = [i for R in rounds for i in R.S]
    assert len(Rcols) <= DJ(r, J) - DJ(q, J), "Theorem 2(b): round columns"
    assert set(B) | set(Rcols) | set(pool) | set(T) == set(range(M)) and \
        M == r + len(Rcols) + len(pool) + len(T), "column partition"
    assert len(T) <= q and rank_of([cols[i] for i in T], p, a) == len(T), "|T| <= q"
    pi = len(pool)
    assert pi >= (C - 1) * r + DJ(q, J) - q, "pi lower bound"
    assert pi >= 2
    Fr = sorted(set(B) | set(pool) | set(T))
    Fin = [i for i in Fr if UE.contains(cols[i])]
    BinU = [i for i in B if UE.contains(cols[i])]
    b = len(BinU)
    assert b >= 1 and len(UE) >= 1
    assert all(UE.contains(cols[i]) for i in pool), "pool outside U"
    YE = span_basis([cols[i] for i in BinU], p, a)
    assert all(YE.contains(cols[i]) for i in pool), "pool outside span(B cap U)"
    assert rank_of([cols[i] for i in Fin], p, a) == b, "Fin spans span(B cap U)"
    eps = len(UE) - b
    X = [i for i in Fr if not UE.contains(cols[i])]
    assert len(X) == (r - b) + len(T) and r - b == q + eps
    Rout = [i for i in Rcols if not UE.contains(cols[i])]
    stats["stall"] += 1
    stats["maxq"] = max(stats["maxq"], q)
    # ---- case 1
    if eps == 0:
        return leaf(Fd, cols, rounds, UE, Fin, P, rng, stats, "closure")
    # ---- case 2
    if b <= q:
        assert r >= q + b
        assert b + pi >= P.F(b), "(Y) count"
        return recurse(Fd, cols, YE, P, rng, stats, depth, "Y", r)
    # ---- case 3
    assert b >= q + 1 and eps >= 1 and r >= 2 * q + 2 and len(X) <= r - 1
    UpE = span_basis([cols[i] for i in Rcols], p, a)
    assert all(UpE.contains(cols[i]) for i in Fin)
    qplus = r - len(UpE)
    assert 0 <= qplus <= q
    rk_rout = rank_of(UE.basis() + [cols[i] for i in Rout], p, a) - len(UE)
    assert rk_rout == q - qplus
    outside_Up = [i for i in range(M) if not UpE.contains(cols[i])]
    assert set(outside_Up) <= set(X)
    if qplus >= 2 * (J - 1):
        assert r - 1 <= P.F(r) - P.F(r - qplus), "(I2)"
        return recurse(Fd, cols, UpE, P, rng, stats, depth, "U+", r)
    part = {i: l for l, R in enumerate(rounds) for i in R.S}
    I, Z = matroid_intersection(Fd, cols, UE, Rout, part, c)
    if len(Rout) <= 11:
        assert brute_max_common(Fd, cols, UE, Rout, part, c) == len(I), "matroid intersection vs brute"
    # least load, for the record
    need = 0
    while True:
        I0, _ = matroid_intersection(Fd, cols, UE, Rout, part, need)
        if len(I0) == q - qplus:
            break
        need += 1
    stats["max_need"] = max(stats["max_need"], need)
    if len(I) < q - qplus:
        # ---- case 3.1: Rado flat
        assert q > c
        WE = span_basis(UE.basis() + [cols[i] for i in Z], p, a)
        qW = r - len(WE)
        RZ = [i for i in Rout if i not in set(Z)]
        outside = [i for i in range(M) if not WE.contains(cols[i])]
        assert set(outside) <= set(RZ) | set(X), "columns outside W"
        cnt = Counter(part[i] for i in RZ)
        r2 = sum(min(c, v) for v in cnt.values())
        nbig = sum(1 for v in cnt.values() if v > c)
        assert all(len(R.S) <= r + 1 for R in rounds), "|S_l| <= r+1"
        assert r2 <= qW - 1 and nbig >= 1 and c * nbig <= r2, ("Lemma M internals", r2, qW, nbig)
        assert c + 1 <= qW <= q
        bound = (qW - 1) + ((qW - 1) // c) * (r + 1 - c) + (r - 1)
        assert len(outside) <= bound, ("outside-W bound", len(outside), bound)
        assert bound <= P.F(r) - P.F(r - qW), "(I1)"
        stats["W"] += 1
        stats["W_bigrounds"] = max(stats["W_bigrounds"], nbig)
        stats["W_neq_U"] += (len(WE) > len(UE))
        return recurse(Fd, cols, WE, P, rng, stats, depth, "W", r)
    # ---- cases 3.2 / 3.3: absorb (in reverse order)
    rounds = list(rounds)
    UE = absorb(Fd, cols, rounds, list(reversed(I)))
    assert len(UE) == r - qplus
    assert max(R.extra for R in rounds) <= c
    assert all(UE.contains(cols[i]) for R in rounds for i in R.S)
    stats["absorb"] += 1
    if qplus == 0:
        return leaf(Fd, cols, rounds, UE, B, P, rng, stats, "absorbedV")
    m = qplus
    assert 1 <= m <= 2 * J - 3
    Fin2 = [i for i in Fr if UE.contains(cols[i])]
    if rank_of([cols[i] for i in Fin2], p, a) == len(UE):
        return leaf(Fd, cols, rounds, UE, Fin2, P, rng, stats, "closureU+")
    Xp = [i for i in Fr if not UE.contains(cols[i])]
    assert set(i for i in range(M) if not UE.contains(cols[i])) == set(Xp)
    if len(Xp) <= P.F(r) - P.F(r - m):
        return recurse(Fd, cols, UE, P, rng, stats, depth, "U+small", r)
    assert m <= J - 2, "top phase reached with m >= J-1 (contradicts T_m(c))"
    # ---- top phase (Lemma T_m)
    Z, cur = [], UE.copy()
    for i in Xp:
        if cur.add(cols[i]):
            Z.append(i)
    assert len(Z) == m
    unused = [i for i in Xp if i not in set(Z)]
    tops = []
    Hcur = flag_space(Fd, cols, rounds + tops)
    while len(Hcur) < r:
        E2 = Ech(p, a)                 # untagged copy: flag tags must not collide with column tags
        for w in Hcur.basis():
            E2.add(w)
        Tt, found = [], None
        for ci in unused:
            res, comb = E2.reduce(cols[ci])
            if any(res):
                E2.add(cols[ci], tag=ci)
                Tt.append(ci)
                continue
            delta = {ci: 1}
            for i in Tt:
                t = comb.get(i, 0) % p
                if t:
                    delta[i] = (-t) % p
            found = (ci, delta)
            break
        if found is None:
            break
        ci, delta = found
        S = sorted(delta)
        if len(S) == 1:
            unused.remove(ci)
            continue
        for i in S:
            unused.remove(i)
        e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        if len({Fd.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = Fd.cls(delta[S[0]])
            zeta = pow(Fd.g, (-cc) % Fd.k, p)
            x = [0] * M
            for i in S:
                x[i] = zeta * delta[i] % p
            assert verify(Fd, cols, x)
            stats["top-direct"] += 1
            return x
        R = Round(Fd, cols, S, delta, [[i] for i in S])
        assert len(S) <= m + 1 <= J - 1
        tops.append(R)
        Hcur = flag_space(Fd, cols, rounds + tops)
    stats["top-rounds"] += len(tops)
    if len(Hcur) == r:
        used = {i for R in tops for i in R.S}
        src = [i for i in Fr if i not in used]
        assert set(Z) <= set(src)
        return leaf(Fd, cols, rounds + tops, Hcur, src, P, rng, stats, "top")
    mp = r - len(Hcur)
    outside = [i for i in range(M) if not Hcur.contains(cols[i])]
    assert 1 <= mp <= m
    assert len(outside) <= m + mp, ("T_m(b) outside count", len(outside), m, mp)
    assert m + mp <= P.F(r) - P.F(r - mp), "(TS)"
    return recurse(Fd, cols, Hcur, P, rng, stats, depth, "topstall", r)
