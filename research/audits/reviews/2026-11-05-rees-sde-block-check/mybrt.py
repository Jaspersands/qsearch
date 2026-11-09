"""Independent implementation of the steered block-refined triangular solver (Theorem C of
research/audits/reviews/2026-11-05-rees-sde-two-relation.md), written for the block-steered check.
No code is imported from that report's folder.

Problem: columns lam_1..lam_M in F_p^a, kappa | p-1, P = nonzero kappa-th powers.  Find x != 0 with
x_i in P u {0} and sum x_i lam_i = 0.

Data structures differ from brt.py: U is kept as an echelon basis with a coordinate map (each echelon
row stores its expression in the round basis), fresh columns are reduced modulo U once, dependencies
are found by incremental elimination of the reduced columns, and s is drawn by rejection sampling.
"""
import random


class Field:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k, self.h = p, k, (p - 1) // k
        # generator of F_p^*/P: an element whose h-th power has order exactly k
        rng = random.Random(p * 31 + k)
        fac = [q for q in range(2, k + 1) if k % q == 0 and all(q % r for r in range(2, q))]
        while True:
            g = rng.randrange(2, p)
            w = pow(g, self.h, p)
            if all(pow(w, k // q, p) != 1 for q in fac):
                break
        self.g, self.w = g, w
        self.log = {pow(w, j, p): j for j in range(k)}

    def cos(self, y):
        return self.log[pow(y % self.p, self.h, self.p)]

    def in_sq(self, y):
        y %= self.p
        return y == 0 or pow(y, self.h, self.p) == 1

    def rand_in_coset(self, c, rng):
        while True:
            y = rng.randrange(1, self.p)
            if self.cos(y) == c:
                return y


class Echelon:
    """Echelon basis of a subspace U of F_p^a, with coordinates in a fixed (round-ordered) basis."""

    def __init__(self, p, a):
        self.p, self.a = p, a
        self.rows = []        # list of (pivot, vector, coordvec) ; coordvec is a dict basis-index -> coeff
        self.nbasis = 0

    def reduce(self, v):
        """Return (residual, coords) with v = residual + sum coords[j] basis_j, residual reduced."""
        p = self.p
        v = [x % p for x in v]
        co = {}
        for piv, row, rc in self.rows:
            f = v[piv]
            if f:
                v = [(x - f * y) % p for x, y in zip(v, row)]
                for j, c in rc.items():
                    co[j] = (co.get(j, 0) + f * c) % p
        return v, co

    def add(self, v):
        """Add basis vector v (must be independent); returns its basis index."""
        p = self.p
        res, co = self.reduce(v)
        piv = next((i for i, x in enumerate(res) if x), None)
        assert piv is not None, "dependent basis vector"
        inv = pow(res[piv], p - 2, p)
        idx = self.nbasis
        self.nbasis += 1
        # res = v - sum co_j b_j  ->  normalised row = inv*(b_idx - sum co_j b_j)
        rc = {idx: inv}
        for j, c in co.items():
            rc[j] = (rc.get(j, 0) - inv * c) % p
        row = [(x * inv) % p for x in res]
        # keep rows fully reduced at the new pivot
        new_rows = []
        for pv, r, c in self.rows:
            f = r[piv]
            if f:
                r = [(x - f * y) % p for x, y in zip(r, row)]
                c = dict(c)
                for j, cc in rc.items():
                    c[j] = (c.get(j, 0) - f * cc) % p
            new_rows.append((pv, r, c))
        new_rows.append((piv, row, rc))
        self.rows = new_rows
        return idx

    def coords(self, v):
        """Coordinates of v in the round basis, or None if v not in U."""
        res, co = self.reduce(v)
        if any(res):
            return None
        return co


def dependency(vecs, p):
    """A nonzero relation among vecs (all of length n), with kernel dimension; incremental elimination."""
    n = len(vecs[0])
    piv_rows = []   # (pivot, row, combo) with row = sum combo_i vecs_i
    rels = []
    for i, v in enumerate(vecs):
        r = [x % p for x in v]
        comb = {i: 1}
        for pv, row, cb in piv_rows:
            f = r[pv]
            if f:
                r = [(x - f * y) % p for x, y in zip(r, row)]
                for j, c in cb.items():
                    comb[j] = (comb.get(j, 0) - f * c) % p
        piv = next((t for t, x in enumerate(r) if x), None)
        if piv is None:
            rels.append(comb)
            continue
        inv = pow(r[piv], p - 2, p)
        piv_rows.append((piv, [(x * inv) % p for x in r], {j: (c * inv) % p for j, c in comb.items()}))
    return rels


def arity(a, E):
    """f_E(q) = q + 1 + f_E(q - min(E-1, q)), f_E(0) = 1."""
    M, q = 1, a
    while q > 0:
        M += q + 1
        q -= min(E - 1, q)
    return M


def closed_arity(a, E):
    m, r = divmod(a, E - 1)
    return 1 + m * (a + 1) - (E - 1) * m * (m - 1) // 2 + ((r + 1) if r else 0)


def split_blocks(sup_by_class, nblocks, rng, mode):
    """Partition into nblocks blocks, each inside one class; every class gets >= 1 block."""
    classes = sorted(sup_by_class)
    cnt = {c: 1 for c in classes}
    extra = nblocks - len(classes)
    while extra > 0:
        # give a block to the class with most elements per block that can still be split
        c = max((c for c in classes if cnt[c] < len(sup_by_class[c])),
                key=lambda c: len(sup_by_class[c]) / cnt[c])
        cnt[c] += 1
        extra -= 1
    blocks, bcls = [], []
    for c in classes:
        items = list(sup_by_class[c])
        if mode == "random":
            rng.shuffle(items)
        n = cnt[c]
        for t in range(n):
            blocks.append(items[t::n])
            bcls.append(c)
    return blocks, bcls


def forward(Fd, cols, a, E, rng, mode="random"):
    p = Fd.p
    U = Echelon(p, a)
    rounds, ptr, h1 = [], 0, True
    while True:
        q = a - U.nbasis
        if q == 0:
            if ptr >= len(cols):
                return rounds, U, None, ptr, "budget", h1
            return rounds, U, ("top", ptr, cols[ptr]), ptr + 1, "ok", h1
        if ptr + q + 1 > len(cols):
            return rounds, U, None, ptr, "budget", h1
        idx = list(range(ptr, ptr + q + 1))
        ptr += q + 1
        resid = [U.reduce(cols[i])[0] for i in idx]
        rels = dependency(resid, p)
        assert rels
        # circuit test (H1): one relation with full support
        delta = [0] * (q + 1)
        if len(rels) == 1:
            for j, c in rels[0].items():
                delta[j] = c
        else:
            for rel in rels:
                coef = rng.randrange(1, p)
                for j, c in rel.items():
                    delta[j] = (delta[j] + coef * c) % p
            if not any(delta):
                for j, c in rels[0].items():
                    delta[j] = c
        full = len(rels) == 1 and all(delta)
        e = [sum(delta[t] * cols[idx[t]][j] for t in range(q + 1)) % p for j in range(a)]
        sup = [t for t in range(q + 1) if delta[t]]
        bycls = {}
        for t in sup:
            bycls.setdefault(Fd.cos(delta[t]), []).append(t)
        if len(bycls) == 1:
            rounds.append(dict(kind="stop", idx=idx, delta=delta, e=e, cls=next(iter(bycls)), sup=sup))
            return rounds, U, None, ptr, "stop", h1
        if not full:
            h1 = False
        nb = min(max(E, len(bycls)), len(sup))
        blocks, bcls = split_blocks(bycls, nb, rng, mode)
        W = [[sum(delta[t] * cols[idx[t]][j] for t in G) % p for j in range(a)] for G in blocks]
        bidx = [None]
        for b in range(1, nb):
            res, _ = U.reduce(W[b])
            if any(res):
                bidx.append(U.add(W[b]))
            else:
                bidx.append(None)
                h1 = False
        rounds.append(dict(kind="level", idx=idx, delta=delta, e=e, blocks=blocks, bcls=bcls, W=W,
                           bidx=bidx, full=full))


def level_beta(R, co):
    return [0 if bi is None else co.get(bi, 0) for bi in R["bidx"]]


def nd_fails(Fd, rounds, U, top):
    """(ND'): list of (level, b, b') whose steering form is identically zero."""
    p = Fd.p
    levels = [i for i, R in enumerate(rounds) if R["kind"] == "level"]
    srcs = [R["e"] for R in rounds]
    if top is not None:
        srcs.append(top[2])
    cos_ = [U.coords(v) for v in srcs]
    fails = []
    for i in levels:
        R = rounds[i]
        later = [c for c in cos_[i + 1:] if c is not None]
        for b in range(len(R["blocks"])):
            for b2 in range(b + 1, len(R["blocks"])):
                if R["bcls"][b] == R["bcls"][b2]:
                    continue
                if all((level_beta(R, c)[b] - level_beta(R, c)[b2]) % p == 0 for c in later):
                    fails.append((i, b, b2))
    return fails


def good_ok(Fd, beta, bcls, s):
    k = Fd.k
    for bb, c in zip(beta, bcls):
        y = (bb + s) % Fd.p
        if y and Fd.cos(y) != (-c) % k:
            return False
    return True


def backward(Fd, cols, a, rounds, U, top, rng, cap):
    p = Fd.p
    x = [0] * len(cols)
    if top is not None:
        y = Fd.rand_in_coset(0, rng)
        x[top[1]] = y
        tau = [(-y * v) % p for v in top[2]]
    else:
        R = rounds[-1]
        zeta = Fd.rand_in_coset((-R["cls"]) % Fd.k, rng)
        for t in R["sup"]:
            x[R["idx"][t]] = zeta * R["delta"][t] % p
        tau = [(-zeta * v) % p for v in R["e"]]
    draws = 0
    for R in reversed([R for R in rounds if R["kind"] == "level"]):
        co = U.coords(tau)
        assert co is not None
        beta = level_beta(R, co)
        taup = [(tau[j] - sum(beta[b] * R["W"][b][j] for b in range(len(beta)))) % p for j in range(a)]
        s = None
        for _ in range(cap):
            draws += 1
            t = rng.randrange(p)
            if good_ok(Fd, beta, R["bcls"], t):
                s = t
                break
        if s is None:
            return None, draws
        for b, G in enumerate(R["blocks"]):
            for t in G:
                x[R["idx"][t]] = R["delta"][t] * (beta[b] + s) % p
        tau = [(taup[j] - s * R["e"][j]) % p for j in range(a)]
    assert not any(tau)
    return x, draws


def verify(Fd, cols, x):
    p = Fd.p
    if not any(v % p for v in x):
        return False
    if not all(Fd.in_sq(v) for v in x):
        return False
    a = len(cols[0])
    return all(sum(x[i] * cols[i][j] for i in range(len(cols))) % p == 0 for j in range(a))


def span_coords(cols, p):
    """Coordinates of the columns in an echelon basis of their span (computed from the columns)."""
    a = len(cols[0])
    U = Echelon(p, a)
    for v in cols:
        if any(U.reduce(v)[0]):
            U.add(v)
    r = U.nbasis
    out = []
    for v in cols:
        co = U.coords(v)
        out.append([co.get(j, 0) for j in range(r)])
    return out, r


def solve(Fd, cols, E, rng, passes=30, mode="random", cap=None, reduce=True):
    a0 = len(cols[0])
    if reduce:
        cols2, a = span_coords(cols, Fd.p)
        if a == 0:
            return [1] + [0] * (len(cols) - 1), dict(status="ok", used=1, a=0)
    else:
        cols2, a = cols, a0
    if cap is None:
        cap = 400 * Fd.k ** E
    rounds, U, top, used, status, h1 = forward(Fd, cols2, a, E, rng, mode)
    info = dict(a=a, used=used, h1=h1, rounds=len(rounds), fstatus=status)
    if status == "budget":
        info["status"] = "budget"
        return None, info
    info["nd_fails"] = len(nd_fails(Fd, rounds, U, top))
    for t in range(passes):
        x, dr = backward(Fd, cols2, a, rounds, U, top, rng, cap)
        if x is not None:
            assert verify(Fd, cols, x), "invalid witness"
            info.update(status="ok", passes=t + 1)
            return x, info
    info["status"] = "fail"
    return None, info
