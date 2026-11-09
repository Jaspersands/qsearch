"""My adversarial bank families (independent of run_tests.py / adv.py).

Every generator returns a bank of exactly M = F(r) columns (unless asked otherwise) in F_p^r,
of rank r.  The adaptive adversary (`adaptive`) builds the bank column by column while running
the forward pass incrementally (with the swap convention sigma -> its index position, under
which the incremental run equals a run from scratch), choosing each new column relative to the
current realized space U, the reserved basis B, the unused set T and the round columns.
"""
import copy
import random

import numpy as np

from la import Fq, Ech, I64
from algt import Par, Rec, forward, init_state, round_vectors

NAMES = ["uniform", "lines", "nested", "planted", "planted2", "twist", "adapt_rado",
         "adapt_top", "adapt_mix", "adapt_case2", "repeat"]


def rvec(rng, p, n):
    return [rng.randrange(p) for _ in range(n)]


def comb(rng, p, basis, n, nonzero=True):
    if not basis:
        return [0] * n
    out = [0] * n
    for v in basis:
        c = rng.randrange(1, p) if nonzero else rng.randrange(p)
        for t in range(n):
            out[t] = (out[t] + c * int(v[t])) % p
    return out


def unit(n, i):
    v = [0] * n
    v[i] = 1
    return v


def rand_basis(rng, p, r):
    while True:
        B = [rvec(rng, p, r) for _ in range(r)]
        e = Ech(p, r)
        if e.add_many(np.array(B, dtype=I64)) == r:
            return B


def pad_to(rng, p, cols, M, gens):
    while len(cols) < M:
        cols.append(comb(rng, p, gens, len(cols[0])))
    return cols[:M]


# ---------------------------------------------------------------------------
# static families


def fam_uniform(rng, p, k, J, r, M):
    return [rvec(rng, p, r) for _ in range(M)]


def fam_lines(rng, p, k, J, r, M):
    t = rng.choice([r + 1, r + 2, 2 * r])
    dirs = [rvec(rng, p, r) for _ in range(t)]
    cols = [[rng.randrange(1, p) * x % p for x in dirs[i % t]] for i in range(M)]
    if rng.random() < 0.5:
        rng.shuffle(cols)
    return cols


def fam_nested(rng, p, k, J, r, M):
    B = rand_basis(rng, p, r)
    cols = [list(v) for v in B] if rng.random() < 0.5 else []
    dims = sorted(rng.sample(range(1, r), min(r - 1, rng.randrange(1, 5)))) + [r]
    w = [rng.random() ** 2 for _ in dims]
    s = sum(w)
    while len(cols) < M:
        u = rng.random() * s
        acc = 0
        for d, ww in zip(dims, w):
            acc += ww
            if u <= acc:
                break
        cols.append(comb(rng, p, B[:d], r))
    return cols[:M]


def fam_repeat(rng, p, k, J, r, M):
    B = rand_basis(rng, p, r)
    cols = [list(v) for v in B]
    few = [comb(rng, p, B[:rng.randrange(1, r + 1)], r) for _ in range(rng.randrange(2, 6))]
    while len(cols) < M:
        if rng.random() < 0.6:
            v = rng.choice(few)
            cols.append([rng.randrange(1, p) * x % p for x in v] if rng.random() < 0.5 else list(v))
        else:
            cols.append(comb(rng, p, B[:rng.randrange(1, r + 1)], r))
    return cols


def realized(Fd, cols, J):
    """Run the forward pass on cols; return (state, status, U-basis rows)."""
    par = Par(J, Fd.k)
    arr = np.array(cols, dtype=I64) % Fd.p
    status, st = forward(Fd, arr, list(range(len(cols))), par, Rec())
    return status, st


def fam_planted(rng, p, k, J, r, M, nbig=1):
    """basis; nbig full circuits on fresh coordinate blocks of size Q (private Q-J+1 each);
    then circuits realizing the remaining coordinates together with generic U-components;
    then pool columns in the remaining coordinates, mixed with proportional copies."""
    Fd = Fq(p, k)
    cols = [unit(r, i) for i in range(r)]
    off = 0
    Qs = []
    tot = 0
    for _ in range(nbig):
        Q = rng.randrange(J + 1, max(J + 2, r // (nbig + 1)) + 1)
        if tot + Q > r - 2:
            break
        Qs.append(Q)
        tot += Q
    for Q in Qs:
        blk = [unit(r, off + i) for i in range(Q)]
        cols += [comb(rng, p, blk, r) for _ in range(Q + 1)]
        off += Q
    status, st = realized(Fd, cols, J)
    Om = [list(map(int, row)) for row in st["U"].rows]
    Ep = [unit(r, i) for i in range(off, r)]
    qq = r - off
    while qq >= 1:
        kk = qq if rng.random() < 0.85 else rng.randrange(1, qq + 1)
        for _ in range(kk + 1):
            y = comb(rng, p, Ep, r)
            w = comb(rng, p, Om, r, nonzero=False) if Om else [0] * r
            cols.append([(u + v) % p for u, v in zip(y, w)])
        qq -= min(J - 1, kk)
    pool0 = len(cols)
    while len(cols) < M:
        if len(cols) > pool0 and rng.random() < 0.35:
            src = cols[rng.randrange(pool0, len(cols))]
            t = rng.randrange(1, p)
            cols.append([t * z % p for z in src])
        else:
            if not Ep:
                cols.append(comb(rng, p, [unit(r, i) for i in range(r)], r))
                continue
            d = rng.randrange(min(2, len(Ep)), len(Ep) + 1)
            cols.append(comb(rng, p, rng.sample(Ep, d), r))
    return cols[:M]


def fam_twist(rng, p, k, J, r, M):
    """planted big round, then rounds whose columns carry a component along v = e_{r-1}
    cancelled inside every block (v never realized), pool avoiding v."""
    Fd = Fq(p, k)
    par = Par(J, k)
    Q = rng.randrange(J + 2, max(J + 3, r // 2 - 1) + 1)
    cols = [unit(r, i) for i in range(r)]
    blk = [unit(r, i) for i in range(Q)]
    cols += [comb(rng, p, blk, r) for _ in range(Q + 1)]
    status, st = realized(Fd, cols, J)
    U = st["U"].copy()
    Ep = [unit(r, i) for i in range(Q, r - 1)]
    d = r - Q - 1
    real = 0
    from algt import split_blocks
    while real < d and len(cols) < M:
        kk = d - real if rng.random() < 0.7 else rng.randrange(1, d - real + 1)
        Om = [list(map(int, row)) for row in U.rows]
        us = [[(x + y) % p for x, y in zip(comb(rng, p, Ep, r), comb(rng, p, Om, r, False))]
              for _ in range(kk + 1)]
        # relation: us[kk] = sum alpha_j us[j] mod U  -> build directly
        alpha = [rng.randrange(1, p) for _ in range(kk)]
        uu = comb(rng, p, Om, r, False)
        last = list(uu)
        for aj, v in zip(alpha, us[:kk]):
            last = [(x + aj * y) % p for x, y in zip(last, v)]
        us[kk] = last
        base = len(cols)
        delta = {base + kk: 1}
        for j in range(kk):
            delta[base + j] = (-alpha[j]) % p
        S = sorted(delta)
        blocks = split_blocks(Fd, S, delta, J, par)
        tv = {}
        for G in blocks:
            if len(G) == 1:
                tv[G[0]] = 0
                continue
            ts = [rng.randrange(1, p) for _ in G[:-1]]
            lastt = (-sum(delta[i] * t for i, t in zip(G[:-1], ts)) * pow(delta[G[-1]], p - 2, p)) % p
            for i, t in zip(G, ts + [lastt]):
                tv[i] = t
        for j in range(kk + 1):
            v = list(us[j])
            v[r - 1] = (v[r - 1] + tv[base + j]) % p
            cols.append(v)
        arr = np.array(cols, dtype=I64)
        rnd = dict(S=S, delta=delta, blocks=blocks)
        Ws, e = round_vectors(Fd, arr, rnd)
        for w in Ws[1:]:
            U.add(w)
        real += min(J - 1, kk)
    while len(cols) < M:
        if rng.random() < 0.3 and len(cols) > r + Q + 1:
            src = cols[rng.randrange(r + Q + 1, len(cols))]
            src = list(src)
            src[r - 1] = 0
            cols.append([rng.randrange(1, p) * z % p for z in src])
        else:
            cols.append(comb(rng, p, Ep[:rng.randrange(1, len(Ep) + 1)], r))
    return cols[:M]


# ---------------------------------------------------------------------------
# adaptive adversary


class Adv:
    def __init__(self, rng, p, k, J, r, M=None):
        self.rng, self.p, self.k, self.J, self.r = rng, p, k, J, r
        self.Fd = Fq(p, k)
        self.par = Par(J, k, sigma_place="index")
        self.M = M if M is not None else self.par.F(r)
        self.cols = rand_basis(rng, p, r) if rng.random() < 0.7 else [
            [rng.randrange(1, p) * x for x in unit(r, i)] for i in range(r)]
        arr = np.array(self.cols, dtype=I64)
        self.st = init_state(self.Fd, arr, list(range(r)))
        self.status = "stall"
        self.st["T"] = []

    def snapshot(self):
        st = self.st
        return dict(B=list(st["B"]), r=st["r"], pool=list(st["pool"]), unused=list(st["unused"]),
                    rounds=copy.deepcopy(st["rounds"]), U=st["U"].copy(), swaps=st["swaps"],
                    T=list(st.get("T", [])))

    def push(self, v):
        """Append column v; continue the pass.  Keep it if the pass still stalls."""
        snap = self.snapshot()
        self.cols.append([int(x) % self.p for x in v])
        idx = len(self.cols) - 1
        self.st["unused"].append(idx)
        arr = np.array(self.cols, dtype=I64)
        status, st = forward(self.Fd, arr, None, self.par, Rec(), st=self.st)
        if status != "stall":
            self.cols.pop()
            self.st = snap
            return False
        self.st = st
        return True

    # views of the state
    def U_rows(self):
        return [list(map(int, x)) for x in self.st["U"].rows]

    def BinU(self):
        U = self.st["U"]
        return [s for s in self.st["B"] if U.contains(np.array(self.cols[s], dtype=I64))]

    def q(self):
        return self.r - self.st["U"].dim

    # moves
    def mv_pool(self):
        BU = self.BinU()
        if not BU:
            return None
        rng = self.rng
        if self.st["pool"] and rng.random() < 0.4:
            src = self.cols[rng.choice(self.st["pool"])]
            return [rng.randrange(1, self.p) * x % self.p for x in src]
        d = rng.randrange(1, len(BU) + 1)
        return comb(rng, self.p, [self.cols[s] for s in rng.sample(BU, d)], self.r)

    def mv_swapin(self):
        if self.st["U"].dim == 0:
            return None
        Ur = self.U_rows()
        d = self.rng.randrange(1, len(Ur) + 1)
        return comb(self.rng, self.p, self.rng.sample(Ur, d), self.r)

    def mv_round(self, kk=None):
        T = self.st.get("T", [])
        if not T:
            return None
        kk = kk or self.rng.randrange(1, len(T) + 1)
        kk = min(kk, len(T))
        pick = self.rng.sample(T, kk)
        v = comb(self.rng, self.p, [self.cols[i] for i in pick], self.r)
        Ur = self.U_rows()
        if Ur:
            u = comb(self.rng, self.p, Ur, self.r, nonzero=False)
            v = [(x + y) % self.p for x, y in zip(v, u)]
        return v

    def mv_grow(self):
        return rvec(self.rng, self.p, self.r)

    def mv_growflat(self, gens):
        return comb(self.rng, self.p, gens, self.r)

    def mv_routcopy(self):
        Rc = [i for rnd in self.st["rounds"] for i in rnd["S"]]
        if not Rc:
            return None
        src = self.cols[self.rng.choice(Rc)]
        return [self.rng.randrange(1, self.p) * x % self.p for x in src]

    def fill(self, weights, maxfail=400):
        names = list(weights)
        w = [weights[n] for n in names]
        fails = 0
        while len(self.cols) < self.M and fails < maxfail:
            mv = self.rng.choices(names, w)[0]
            v = getattr(self, "mv_" + mv)()
            if v is None or not self.push(v):
                fails += 1
        # pad with pool (keeps the stall) or with anything
        tries = 0
        while len(self.cols) < self.M and tries < 5000:
            tries += 1
            v = self.mv_pool() or self.mv_routcopy() or self.mv_grow()
            if not self.push(v):
                self.cols.append([int(x) for x in v])   # break the stall; still a test bank
                self.status = "broken"
                break
        while len(self.cols) < self.M:
            self.cols.append(rvec(self.rng, self.p, self.r))
        return self.cols[:self.M]


def fam_adapt(rng, p, k, J, r, M, style):
    A = Adv(rng, p, k, J, r, M)
    if style == "rado":
        # big early circuits keeping private directions, then small rounds + swaps + pool
        for _ in range(rng.randrange(1, 3)):
            Q = rng.randrange(J + 1, max(J + 2, r // 2) + 1)
            for _ in range(Q):
                if A.q() > len(A.st.get("T", [])):
                    A.push(A.mv_grow())
            A.push(A.mv_round(Q) or A.mv_grow())
        return A.fill(dict(pool=4, swapin=2, round=1, grow=1, routcopy=1))
    if style == "top":
        return A.fill(dict(pool=3, swapin=3, round=2, grow=2, routcopy=1))
    if style == "case2":
        return A.fill(dict(pool=6, swapin=1, round=1, grow=1))
    return A.fill(dict(pool=rng.random() * 5, swapin=rng.random() * 3, round=rng.random() * 3,
                       grow=rng.random() * 3, routcopy=rng.random() * 2))


def make(name, rng, p, k, J, r, M=None):
    par = Par(J, k)
    M = par.F(r) if M is None else M
    if name == "uniform":
        return fam_uniform(rng, p, k, J, r, M)
    if name == "lines":
        return fam_lines(rng, p, k, J, r, M)
    if name == "nested":
        return fam_nested(rng, p, k, J, r, M)
    if name == "repeat":
        return fam_repeat(rng, p, k, J, r, M)
    if name == "planted":
        return fam_planted(rng, p, k, J, r, M, 1)
    if name == "planted2":
        return fam_planted(rng, p, k, J, r, M, 2)
    if name == "twist":
        return fam_twist(rng, p, k, J, r, M)
    if name == "adapt_rado":
        return fam_adapt(rng, p, k, J, r, M, "rado")
    if name == "adapt_top":
        return fam_adapt(rng, p, k, J, r, M, "top")
    if name == "adapt_case2":
        return fam_adapt(rng, p, k, J, r, M, "case2")
    if name == "adapt_mix":
        return fam_adapt(rng, p, k, J, r, M, "mix")
    raise KeyError(name)


# ---------------------------------------------------------------------------
# explicit stall designs (case 3 shapes): V = Y + (+)S_i + D,
#   Y   : b reserved columns u_i, realized later by circuits in Y + U (so B cap U = u's),
#   S_i : one full circuit each, of (J-1) + P_i generic columns + 1 (P_i private directions),
#   D   : m directions never realized (q+ = m), carried by the reserved w's and by T,
#   pool: columns in Y (and proportional copies), T: unused columns outside U.
# D-pattern "degenerate": all w's (and T) have D-component in span(d_1) except one w per
# further d_j, so the top pass realizes only d_1 and stalls at m' = m - 1 (Lemma T_m(b)).


def fam_design(rng, p, k, J, M=None, P_list=None, b=None, m=None, tcount=None, degenerate=None,
               tin=0, rmax=40):
    Fd = Fq(p, k)
    par = Par(J, k)
    c = par.c
    for _attempt in range(50):
        t = rng.randrange(1, 4) if P_list is None else len(P_list)
        PL = P_list or [rng.choice([rng.randrange(0, c + 1), rng.randrange(c + 1, c + 5)])
                        for _ in range(t)]
        mm = rng.randrange(0, 2 * J + 1) if m is None else m
        q = sum(PL) + mm
        bb = b if b is not None else rng.randrange(max(1, q - 2), q + 4)
        r = bb + sum((J - 1) + x for x in PL) + mm
        if r <= rmax and r >= 2:
            break
    else:
        return None
    dg = (rng.random() < 0.6) if degenerate is None else degenerate
    tc = tcount if tcount is not None else rng.randrange(0, sum(PL) + 2)
    M = par.F(r) if M is None else M
    # coordinates
    off = 0
    Yc = list(range(off, off + bb)); off += bb
    Sc = []
    for x in PL:
        Sc.append(list(range(off, off + (J - 1) + x))); off += (J - 1) + x
    Dc = list(range(off, off + mm)); off += mm
    assert off == r
    allS = [i for s in Sc for i in s]

    def vec(supp_coefs):
        v = [0] * r
        for i, cf in supp_coefs:
            v[i] = cf % p
        return v

    def gen_in(coords):
        return vec([(i, rng.randrange(1, p)) for i in coords])

    def dpart(which):
        if not Dc:
            return []
        if which == "gen":
            return [(i, rng.randrange(1, p)) for i in Dc]
        return [(Dc[which], rng.randrange(1, p))]

    # reserved basis: u's in Y, w's in S + D
    for _ in range(50):
        B = [vec([(i, rng.randrange(1, p))]) for i in Yc]
        nw = r - bb
        ws = []
        for j in range(nw):
            if dg and Dc:
                which = 0 if j < nw - (len(Dc) - 1) else (j - (nw - (len(Dc) - 1)) + 1)
                if j == nw - 1 and len(Dc) == 1:
                    which = 0
                d = dpart(which)
            else:
                d = dpart("gen")
            ws.append(vec([(i, rng.randrange(p)) for i in allS] + d))
        B += ws
        e = Ech(p, r)
        if e.add_many(np.array(B, dtype=I64)) == r:
            break
    else:
        return None
    cols = [list(v) for v in B]
    for s in Sc:
        cols += [gen_in(s) for _ in range(len(s) + 1)]
    # realize Y by circuits in Y + U
    for _ in range(4 * r):
        status, st = realized(Fd, cols, J)
        if status != "stall":
            break
        U = st["U"]
        missing = [i for i in Yc if not U.contains(np.array(unit(r, i), dtype=I64))]
        if not missing:
            break
        Ur = [list(map(int, x)) for x in U.rows]
        y = len(missing) if rng.random() < 0.8 else rng.randrange(1, len(missing) + 1)
        for _ in range(y + 1):
            v = gen_in(missing)
            w = comb(rng, p, Ur, r, nonzero=False)
            cols.append([(a_ + b_) % p for a_, b_ in zip(v, w)])
    # T and pool
    allP = [i for s, x in zip(Sc, PL) for i in s[(J - 1):]]
    tail = []
    for j in range(tc):
        d = dpart(0) if (dg and Dc) else dpart("gen") if Dc and rng.random() < 0.7 else []
        tail.append(vec([(i, rng.randrange(p)) for i in allP + allS] + d))
    for j in range(tin):
        tail.append(vec([(i, rng.randrange(p)) for i in allS]))
    npool = M - len(cols) - len(tail)
    pool = []
    for j in range(max(0, npool)):
        if pool and rng.random() < 0.3:
            src = rng.choice(pool)
            pool.append([rng.randrange(1, p) * x % p for x in src])
        else:
            d = rng.randrange(1, bb + 1)
            pool.append(vec([(i, rng.randrange(1, p)) for i in rng.sample(Yc, d)]))
    tail += pool
    rng.shuffle(tail)
    cols += tail
    cols = cols[:M] if len(cols) > M else cols
    # random change of coordinates
    for _ in range(20):
        G = [[rng.randrange(p) for _ in range(r)] for _ in range(r)]
        if Ech(p, r).add_many(np.array(G, dtype=I64)) == r:
            break
    out = [[sum(G[i][j] * v[j] for j in range(r)) % p for i in range(r)] for v in cols]
    return out


def make_design(style, rng, p, k, J, rmax=40):
    c = 2 * (J - 1)
    if style == "rado":
        PL = [rng.randrange(c + 1, c + 6)] + [rng.randrange(0, c + 6) for _ in range(rng.randrange(0, 3))]
        return fam_design(rng, p, k, J, P_list=PL, m=rng.randrange(0, 2 * J - 2), rmax=rmax)
    if style == "top":
        PL = [rng.randrange(0, c + 1) for _ in range(rng.randrange(1, 4))]
        mm = rng.randrange(1, max(2, J - 1))
        return fam_design(rng, p, k, J, P_list=PL, m=mm,
                          b=sum(PL) + mm + 1 + rng.choice([0, 0, 1]), degenerate=True,
                          tcount=sum(PL) + 1, rmax=rmax)
    if style == "u30":
        PL = [rng.randrange(0, c + 1) for _ in range(rng.randrange(1, 3))]
        return fam_design(rng, p, k, J, P_list=PL, m=rng.randrange(2 * J - 2, 2 * J + 3), rmax=rmax)
    return fam_design(rng, p, k, J, rmax=rmax)


NAMES += ["design_rado", "design_top", "design_u30", "design_mix"]
_make_old = make


def make(name, rng, p, k, J, r, M=None):
    if name.startswith("design_"):
        # r is used as an upper bound on the rank here; designs choose their own rank
        for _ in range(20):
            out = make_design(name[7:], rng, p, k, J, rmax=max(r, 12))
            if out is not None:
                return out
        return _make_old("uniform", rng, p, k, J, r, M)
    return _make_old(name, rng, p, k, J, r, M)
