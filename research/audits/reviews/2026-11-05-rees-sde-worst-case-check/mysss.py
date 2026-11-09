"""Independent implementation of the source-steered block solver of Theorem 2
(research/audits/reviews/2026-11-05-rees-sde-worst-case.md, Section 3), written from the
statement only.  Exact arithmetic mod p.

Target: nonzero x in (P u {0})^M with sum_i x_i lam_i = 0, P = (F_p^*)^kappa.

forward(...) returns a dict with status in {"span", "stall", "direct"} and the run data,
including the number of true-pool events pi, swaps, rounds (blocks, classes, W's, e), the
final reserved basis B, and at a stall the column-count decomposition used in Theorem 2(b).
backward(...) runs one back substitution and returns (x or None, info).
Variants (negative controls): swap=False (true-pool and would-be-swap columns are discarded),
sources="one" (only the first basis column gets a random weight, the others weight 0).
"""
import random


# ---------------------------------------------------------------- field
class F:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k, self.h = p, k, (p - 1) // k
        n, fac, m, f = p - 1, [], p - 1, 2
        while f * f <= m:
            if m % f == 0:
                fac.append(f)
                while m % f == 0:
                    m //= f
            f += 1
        if m > 1:
            fac.append(m)
        self.g = next(g for g in range(2, p) if all(pow(g, n // q, p) != 1 for q in fac))
        z = pow(self.g, self.h, p)
        self.log = {pow(z, j, p): j for j in range(k)}

    def cls(self, y):
        y %= self.p
        assert y
        return self.log[pow(y, self.h, self.p)]

    def inQ0(self, y, c):
        """y in Q_c u {0}"""
        y %= self.p
        return y == 0 or self.cls(y) == c % self.k

    def randP(self, rng):
        while True:
            y = rng.randrange(1, self.p)
            return pow(y, self.k, self.p)


# ---------------------------------------------------------------- linear algebra
class Span:
    """Incremental echelon basis; coords(v) gives coefficients on the inserted vectors."""

    def __init__(self, p, a):
        self.p, self.a = p, a
        self.rows = []   # (pivot, reduced vector, combination over inserted vectors)
        self.n = 0

    def reduce(self, v):
        p = self.p
        v = [x % p for x in v]
        comb = [0] * self.n
        for piv, row, rc in self.rows:
            f = v[piv]
            if f:
                v = [(x - f * y) % p for x, y in zip(v, row)]
                for j, c in enumerate(rc):
                    if c:
                        comb[j] = (comb[j] + f * c) % p
        return v, comb

    def coords(self, v):
        """None if v not in span, else coefficients c with sum c_j inserted_j = v."""
        w, comb = self.reduce(v)
        if any(w):
            return None
        return comb

    def insert(self, v):
        p = self.p
        w, comb = self.reduce(v)
        assert any(w)
        piv = next(i for i, x in enumerate(w) if x)
        iv = pow(w[piv], p - 2, p)
        w = [x * iv % p for x in w]
        # new vector = v ; w = (v - sum comb_j ins_j) * iv
        rc = [(-c * iv) % p for c in comb] + [iv]
        for t in range(len(self.rows)):
            self.rows[t] = (self.rows[t][0], self.rows[t][1], self.rows[t][2] + [0])
        self.rows.append((piv, w, rc))
        self.n += 1


def rank(vecs, p):
    if not vecs:
        return 0
    S = Span(p, len(vecs[0]))
    r = 0
    for v in vecs:
        if S.coords(v) is None:
            S.insert(v)
            r += 1
    return r


def lin(p, coefs, vecs, a):
    out = [0] * a
    for c, v in zip(coefs, vecs):
        if c:
            for i in range(a):
                out[i] = (out[i] + c * v[i]) % p
    return out


# ---------------------------------------------------------------- D_E
def D(E, q, memo={}):
    if q == 0:
        return 0
    key = (E, q)
    if key not in memo:
        memo[key] = max(k + 1 + D(E, q - min(E - 1, k)) for k in range(1, q + 1))
    return memo[key]


# ---------------------------------------------------------------- forward pass
def forward(Fd, cols, E, swap=True, order=None, split="first"):
    p, a = Fd.p, len(cols[0])
    M = len(cols)
    idx = list(order) if order is not None else list(range(M))
    for i in idx:
        if not any(x % p for x in cols[i]):
            x = [0] * M
            x[i] = 1
            return {"status": "direct", "x": x, "why": "zero column"}
    # reserve: first r independent indices (in scan order)
    SB = Span(p, a)
    B = []
    for i in idx:
        if SB.coords(cols[i]) is None:
            SB.insert(cols[i])
            B.append(i)
    r = len(B)
    unused = [i for i in idx if i not in B]
    U = Span(p, a)            # basis of U = W's in flag order
    Uvecs = []
    rounds, pool, nswaps, discarded = [], [], 0, []
    while U.n < r:
        Ucur = U.n
        # T-span is U + span(T): copy U then add T vectors
        UT = Span(p, a)
        for w in Uvecs:
            UT.insert(w)
        Tlist = []
        event = None
        for c in unused:
            co = UT.coords(cols[c])
            if co is None:
                UT.insert(cols[c])
                Tlist.append(c)
                continue
            delta = {c: 1}
            for j, t in enumerate(Tlist):
                cj = co[Ucur + j]
                if cj:
                    delta[t] = (-cj) % p
            event = (c, delta)
            break
        if event is None:
            q = r - U.n
            return {"status": "stall", "r": r, "q": q, "pi": len(pool), "rounds": rounds,
                    "B": B, "unused": unused, "pool": pool, "swaps": nswaps,
                    "discarded": discarded, "consumed": sum(len(R["S"]) for R in rounds)}
        c, delta = event
        S = sorted(delta)
        if len(S) == 1:                       # c in U
            # write c in basis B
            SBc = Span(p, a)
            for s in B:
                SBc.insert(cols[s])
            gam = SBc.coords(cols[c])
            cand = [B[j] for j, gj in enumerate(gam) if gj and U.coords(cols[B[j]]) is None]
            unused.remove(c)
            if cand and swap:
                sig = cand[0]
                B[B.index(sig)] = c
                unused.append(sig)
                nswaps += 1
            elif cand:                          # control: would-be swap discarded
                discarded.append(c)
            else:
                pool.append(c)
            continue
        for i in S:
            unused.remove(i)
        e = lin(p, [delta[i] for i in S], [cols[i] for i in S], a)
        cl = {i: Fd.cls(delta[i]) for i in S}
        if len(set(cl.values())) == 1 and not any(e):
            zeta = pow(Fd.g, (-cl[S[0]]) % Fd.k, p)    # zeta in Q_{-cls}
            x = [0] * M
            for i in S:
                x[i] = zeta * delta[i] % p
            return {"status": "direct", "x": x, "why": "monochromatic circuit"}
        El = min(E, len(S))
        groups = {}
        for i in S:
            groups.setdefault(cl[i], []).append(i)
        blocks = [g for _, g in sorted(groups.items())]
        assert len(blocks) <= El, "more classes than blocks: E < kappa?"
        while len(blocks) < El:
            j = max(range(len(blocks)), key=lambda b: len(blocks[b]))
            g = blocks[j]
            blocks[j] = g[:1] if split == "first" else g[:len(g) // 2]
            blocks.append(g[1:] if split == "first" else g[len(g) // 2:])
        W = [lin(p, [delta[i] for i in g], [cols[i] for i in g], a) for g in blocks]
        bcls = [cl[g[0]] for g in blocks]
        start = U.n
        for b in range(1, El):
            U.insert(W[b])
            Uvecs.append(W[b])
        assert U.n == start + El - 1, "Omega not of dimension E_l - 1"
        assert U.coords(e) is not None and (start == 0 and not any(e) or
                                             _in_first(U, e, start, p))
        rounds.append({"S": S, "delta": delta, "blocks": blocks, "bcls": bcls, "W": W,
                       "e": e, "start": start, "El": El})
    return {"status": "span", "r": r, "rounds": rounds, "B": B, "pi": len(pool),
            "pool": pool, "swaps": nswaps, "discarded": discarded, "Uvecs": Uvecs,
            "unused": unused}


def _in_first(U, v, n, p):
    """v in span of the first n inserted vectors of U."""
    co = U.coords(v)
    return co is not None and all(c == 0 for c in co[n:])


def rho(run):
    tot = 0
    for R in run["rounds"]:
        bc = R["bcls"]
        tot += sum(1 for i in range(len(bc)) for j in range(i) if bc[i] != bc[j])
    return tot


# ---------------------------------------------------------------- backward pass
def good_set(Fd, betas, bcls):
    p = Fd.p
    # cross-class coincidence?
    for i in range(len(betas)):
        for j in range(i):
            if bcls[i] != bcls[j] and betas[i] == betas[j]:
                s = (-betas[i]) % p
                ok = all(Fd.inQ0(betas[b] + s, -bcls[b]) for b in range(len(betas)))
                return ([s] if ok else []), True
    return None, False


def backward(Fd, cols, run, rng, sources="all", exact_good=None):
    p, a, M = Fd.p, len(cols[0]), len(cols)
    B = run["B"]
    x = [0] * M
    t = {}
    for j, s in enumerate(B):
        t[s] = Fd.randP(rng) if (sources == "all" or j == 0) else 0
        x[s] = t[s]
    tau = [(-v) % p for v in lin(p, [t[s] for s in B], [cols[s] for s in B], a)]
    Uvecs = run["Uvecs"]
    Ufull = Span(p, a)
    for w in Uvecs:
        Ufull.insert(w)
    coinc = 0
    for R in reversed(run["rounds"]):
        n = R["start"] + R["El"] - 1
        co = Ufull.coords(tau)
        assert co is not None and all(c == 0 for c in co[n:]), "tau left U_l"
        betas = [0] + [co[R["start"] + b - 1] for b in range(1, R["El"])]
        forced, hit = good_set(Fd, betas, R["bcls"])
        if hit:
            coinc += 1
            if not forced:
                return None, {"fail": True, "coinc": coinc}
            s = forced[0]
        else:
            if exact_good is None:
                exact_good = p <= 40000
            if exact_good:
                G = [s for s in range(p) if all(Fd.inQ0(betas[b] + s, -R["bcls"][b])
                                                  for b in range(len(betas)))]
                if not G:
                    return None, {"fail": True, "coinc": coinc, "empty_no_coinc": True}
                s = rng.choice(G)
            else:
                for _ in range(10 ** 6):
                    s = rng.randrange(p)
                    if all(Fd.inQ0(betas[b] + s, -R["bcls"][b]) for b in range(len(betas))):
                        break
                else:
                    return None, {"fail": True, "coinc": coinc, "empty_no_coinc": True}
        for b, g in enumerate(R["blocks"]):
            for i in g:
                x[i] = R["delta"][i] * (betas[b] + s) % p
        val = lin(p, [x[i] for i in R["S"]], [cols[i] for i in R["S"]], a)
        tau = [(u - v) % p for u, v in zip(tau, val)]
    assert not any(tau)
    return x, {"fail": False, "coinc": coinc}


def verify(Fd, cols, x):
    p, a = Fd.p, len(cols[0])
    if x is None or not any(v % p for v in x):
        return False
    if not all(Fd.inQ0(v, 0) for v in x):
        return False
    return not any(lin(p, x, cols, a))


def solve(Fd, cols, E, rng, passes=20, **kw):
    run = forward(Fd, cols, E, swap=kw.get("swap", True))
    if run["status"] == "direct":
        assert verify(Fd, cols, run["x"])
        return "solved-direct", run, 0
    if run["status"] == "stall":
        return "stall", run, 0
    for k in range(1, passes + 1):
        x, info = backward(Fd, cols, run, rng, sources=kw.get("sources", "all"))
        if x is not None:
            assert verify(Fd, cols, x), "invalid witness"
            return "solved", run, k
    return "fail", run, passes
