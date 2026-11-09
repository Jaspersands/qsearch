"""Test ALG-T (subquad.py) on adversarial banks at the budget F(r) = D_J(r) + C r.

Usage: run_tests.py GROUP SEED
GROUP in: heavy (heavy_found_3.jsonl), fams (structured families of q1/fams.py plus
degenerate families), planted (planted private-direction banks), critical (search-agent
critical banks, padded), stress (planted + fams with capacity c = 1, strict off),
climb (hill climb maximising the least achievable load).
Every witness is verified; every count inequality of the proof is asserted (strict).
"""
import os
import sys
import json
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-q1"))
from subquad import Field, Params, solve_T, new_stats, check, DJ, rank, init_state, forward_fast as forward, split_blocks  # noqa
from fastla import Ech  # noqa
import time
from fams import family_list  # noqa

GROUP = sys.argv[1] if len(sys.argv) > 1 else "heavy"
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
rng = random.Random(SEED)
TOT = Counter()


def merge(st):
    for k, v in st.items():
        if k == "trace":
            continue
        if k.startswith("max"):
            TOT[k] = max(TOT[k], v)
        else:
            TOT[k] += v


def run(Fd, cols, P, label):
    st = new_stats()
    x = solve_T(Fd, cols, P, rng, st)
    ok = x is not None and check(Fd, cols, x)
    TOT["banks"] += 1
    TOT["solved"] += ok
    merge(st)
    if not ok:
        print("UNSOLVED", label, json.dumps(cols), flush=True)
    return ok, st


def comb(p, basis, a):
    co = [rng.randrange(1, p) for _ in basis]
    return [sum(c * v[t] for c, v in zip(co, basis)) % p for t in range(a)]


def unit(a, i):
    v = [0] * a
    v[i] = 1
    return v


def planted(Fd, r, Qs, J, M, mix=True):
    """Basis e_1..e_r; for each Q in Qs a full circuit of Q+1 columns generic in a fresh
    coordinate block (each keeps Q-J+1 private directions); then generic columns of
    Omega + E' (E' = remaining coordinates, Omega = what the big rounds realised), enough
    to realise E' by full circuits; then pool columns in E'.  Optionally the last part is
    mixed with proportional copies (lines) of pool columns."""
    p = Fd.p
    cols = [unit(r, i) for i in range(r)]
    off = 0
    for Q in Qs:
        blk = [unit(r, off + i) for i in range(Q)]
        cols += [comb(p, blk, r) for _ in range(Q + 1)]
        off += Q
    st = init_state(Fd, cols)
    forward(Fd, cols, J, rng, st, rule="first")
    # forward_fast returns "direct" (a monochromatic circuit among the block columns, e.g. Q = 1)
    # before it sets st["Ub"]: that was the KeyError 'Ub' of the break pass.  No round has then
    # been realised, so Omega = 0 (the bank is still a valid bank; the later columns are as before).
    Om = st["Ub"] if "Ub" in st else []
    Ep = [unit(r, i) for i in range(off, r)]
    qq, n2 = r - off, 0
    while qq >= 1:
        n2 += qq + 1
        qq -= min(J - 1, qq)
    for _ in range(n2):
        y = comb(p, Ep, r)
        w = comb(p, Om, r) if Om else [0] * r
        cols.append([(u + v) % p for u, v in zip(y, w)])
    pool0 = len(cols)
    while len(cols) < M:
        if mix and len(cols) % 3 == 0 and len(cols) > pool0:
            src = cols[rng.randrange(pool0, len(cols))]
            t = rng.randrange(1, p)
            cols.append([t * z % p for z in src])      # proportional copy of a pool column
        else:
            cols.append(comb(p, Ep, r))
    return cols[:M]


def degenerate(Fd, a, M):
    """extra degenerate families: many proportional columns, nested subspaces,
    concentrated low rank, repeated columns."""
    p = Fd.p
    out = {}
    base = [[rng.randrange(p) for _ in range(a)] for _ in range(a + 1)]
    out["proportional"] = [[rng.randrange(1, p) * z % p for z in base[i % (a + 1)]] for i in range(M)]
    basis = [[rng.randrange(p) for _ in range(a)] for _ in range(a)]
    nest = []
    d = 1
    while len(nest) < M:
        cnt = max(2, DJ(d, 3) // 2)
        nest += [comb(p, basis[:d], a) for _ in range(cnt)]
        d = min(a, d + 1)
    out["nested"] = nest[:M]
    low = [comb(p, basis[:a // 2], a) for _ in range(M - a)] + [comb(p, basis, a) for _ in range(a)]
    rng.shuffle(low)
    out["half_rank_dense"] = low
    rep = [list(base[rng.randrange(3)]) for _ in range(M // 2)] + [comb(p, basis, a) for _ in range(M - M // 2)]
    out["repeated"] = rep
    return out


def vtwist(Fd, r, Q, J, M):
    """As planted(..., [Q]), but the rounds realising E' all carry components along
    v = e_r, cancelled inside every block of size >= 2 (so v is never realised), and the
    pool avoids v.  Then the round columns outside U are many (all v-round columns with a
    nonzero v-component) while their span modulo U adds only v: the U-recursion count fails
    and only the Rado flat W = U + Fv has enough columns."""
    p = Fd.p
    cols = [unit(r, i) for i in range(r)]
    blk = [unit(r, i) for i in range(Q)]
    cols += [comb(p, blk, r) for _ in range(Q + 1)]
    st = init_state(Fd, cols)
    forward(Fd, cols, J, rng, st, rule="first")
    EU = Ech(p, r)
    for R in st["rounds"]:
        for w in R.W[1:]:
            EU.add(w)
    Om = [row for _, row, _ in EU.rows]
    Ep = [unit(r, i) for i in range(Q, r - 1)]
    d = r - Q - 1
    real = 0
    while real < d:
        k = d - real
        base = len(cols)
        us = [[(x + y) % p for x, y in zip(comb(p, Ep, r), comb(p, Om, r))] for _ in range(k + 1)]
        E2 = EU.copy()
        for j in range(k):
            assert E2.add(us[j], {base + j: 1})
        res, co = E2.reduce(us[k], track=True)
        assert not any(res)
        delta = {base + k: 1}
        for j in range(k):
            t = co.get(base + j, 0) % p
            assert t
            delta[base + j] = (-t) % p
        S = sorted(delta)
        blocks = split_blocks(Fd, S, delta, J, rng, "first")
        tv = {}
        for G in blocks:
            if len(G) == 1:
                tv[G[0]] = 0
                continue
            ts = [rng.randrange(1, p) for _ in G[:-1]]
            last = (-sum(delta[i] * t for i, t in zip(G[:-1], ts)) * pow(delta[G[-1]], p - 2, p)) % p
            for i, t in zip(G, ts + [last]):
                tv[i] = t
        for j in range(k + 1):
            v = list(us[j])
            v[r - 1] = (v[r - 1] + tv[base + j]) % p
            cols.append(v)
        W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(r)] for G in blocks]
        assert all(w[r - 1] == 0 for w in W)
        for w in W[1:]:
            assert EU.add(w)
        real += min(J - 1, k)
        Om = [row for _, row, _ in EU.rows]
    assert len(cols) <= M, (len(cols), M)
    while len(cols) < M:
        cols.append(comb(p, Ep, r))
    return cols


def group_vtwist():
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        P = Params(3, k)
        for r in (24, 28, 30):
            for rep in range(2 if r < 30 else 1):
                t0 = time.time()
                cols = vtwist(Fd, r, 8, 3, P.F(r))
                ok, st = run(Fd, cols, P, "vtwist p=%d r=%d" % (p, r))
                print("vtwist p=%d k=%d r=%d M=%d ok=%s %.0fs" % (p, k, r, len(cols), ok, time.time() - t0),
                      {x: st[x] for x in st if st[x]}, flush=True)


def topbank(Fd, r, b, k, nrest, m, J, M, degenerate=False):
    """Case-3 stall with a complete absorption (private k-J+1 <= c in one big round) that
    leaves codimension m = q+ >= 1 above U+, with many reserved columns outside U+, so the
    top phase runs.  degenerate=True (m = 2): every reserved column outside U+ except one is
    congruent mod U+ to a multiple of e_b, so the top pass stalls at codim 1."""
    p = Fd.p
    assert r - b == k + nrest + m
    cols = [unit(r, i) for i in range(r)]
    Y = [unit(r, i) for i in range(b)]
    if degenerate:
        assert m == 2
        gens = []
        for j in range(b + 2, r):
            v = unit(r, j)
            v[b] = rng.randrange(1, p)
            gens.append(v)
    else:
        rest = [unit(r, i) for i in range(b, r)]
        gens = [comb(p, rest, r) for _ in range(k + nrest)]
    G = [comb(p, gens, r) for _ in range(k + nrest)]
    A1, Orest = G[:k], G[k:]
    cols += [comb(p, A1, r) for _ in range(k + 1)]
    st = init_state(Fd, cols)
    forward(Fd, cols, J, rng, st, rule="first")
    EU = Ech(p, r)
    for R in st["rounds"]:
        for w in R.W[1:]:
            EU.add(w)
    Om1 = [row for _, row, _ in EU.rows]
    space = Om1 + Y + Orest
    qq, n2 = b + nrest, 0
    while qq >= 1:
        n2 += qq + 1
        qq -= min(J - 1, qq)
    cols += [comb(p, space, r) for _ in range(n2)]
    assert len(cols) <= M, (len(cols), M)
    while len(cols) < M:
        cols.append(comb(p, Y, r))
    return cols


def group_topbank():
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        P = Params(3, k)
        # (r, b, k, nrest, m, degenerate)
        shapes = [(18, 5, 5, 7, 1, False), (20, 6, 5, 7, 2, False), (22, 7, 5, 7, 3, False),
                  (20, 6, 6, 6, 2, True), (22, 7, 5, 8, 2, True), (16, 6, 4, 5, 1, False)]
        for (r, b, kk, nrest, m, dg) in shapes:
            for rep in range(3):
                cols = topbank(Fd, r, b, kk, nrest, m, 3, P.F(r), dg)
                ok, st = run(Fd, cols, P, "topbank")
                print("topbank p=%d r=%d b=%d k=%d nrest=%d m=%d deg=%s ok=%s" % (p, r, b, kk, nrest, m, dg, ok),
                      {x: st[x] for x in st if st[x] and x != "trace"}, st.get("trace"), flush=True)


def group_topbank2():
    """J = 3 with q+ = 4 (U+-recursion branch), and J = 4 with a degenerate top phase."""
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        for (J, r, b, kk, nrest, m, dg) in [(3, 26, 8, 5, 9, 4, False), (3, 28, 9, 5, 10, 4, False),
                                             (4, 40, 4, 4, 30, 2, True), (4, 40, 4, 4, 30, 2, False)]:
            P = Params(J, k)
            for rep in range(2):
                t0 = time.time()
                cols = topbank(Fd, r, b, kk, nrest, m, J, P.F(r), dg)
                ok, st = run(Fd, cols, P, "topbank2")
                print("topbank2 p=%d J=%d r=%d b=%d k=%d nrest=%d m=%d deg=%s ok=%s %.0fs" % (
                    p, J, r, b, kk, nrest, m, dg, ok, time.time() - t0),
                    {x: st[x] for x in st if st[x] and x != "trace"}, st.get("trace"), flush=True)


class LightField(Field):
    """Field without the materialised list of kappa-th powers (for p ~ 10^9);
    randP draws y^kappa for uniform y != 0, which is uniform on P."""
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k, self.h = p, k, (p - 1) // k
        g = 2
        while not self._primroot(g):
            g += 1
        self.g = g
        z = pow(g, self.h, p)
        self.zlog = {pow(z, j, p): j for j in range(k)}

    def randP(self, rng):
        return pow(rng.randrange(1, self.p), self.k, self.p)


def isprime(n):
    if n < 2:
        return False
    for d in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % d == 0:
            return n == d
    dd, s = n - 1, 0
    while dd % 2 == 0:
        dd //= 2
        s += 1
    for a_ in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a_, dd, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def group_thmprime():
    """J = 3 (E = 7) at primes inside the range of Corollary A_3."""
    for (lo, k) in [(2330000, 2), (689000000, 3)]:
        p = lo
        while not (isprime(p) and (p - 1) % k == 0):
            p += 1
        Fd = LightField(p, k)
        P = Params(3, k)
        nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
        for r, Qs in [(14, [7]), (20, [10]), (24, [8, 4])]:
            run(Fd, planted(Fd, r, Qs, 3, P.F(r), True), P, "thm planted")
        for r in (24, 28):
            run(Fd, vtwist(Fd, r, 8, 3, P.F(r)), P, "thm vtwist")
        for (r, b, kk, nrest, m, dg) in [(18, 5, 5, 7, 1, False), (26, 8, 5, 9, 4, False)]:
            run(Fd, topbank(Fd, r, b, kk, nrest, m, 3, P.F(r), dg), P, "thm topbank")
        for a in (11, 12):
            for name, gen in family_list(rng, p, a, P.F(a), nr).items():
                run(Fd, gen(), P, "thm " + name)
        print("thmprime p=%d k=%d" % (p, k), dict(TOT), flush=True)


def group_vtwist2():
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        for (J, r, Q) in [(3, 32, 8), (3, 36, 10), (3, 40, 12), (4, 36, 11), (4, 40, 12)]:
            if J < k:
                continue
            P = Params(J, k)
            t0 = time.time()
            cols = vtwist(Fd, r, Q, J, P.F(r))
            ok, st = run(Fd, cols, P, "vtwist2")
            print("vtwist2 p=%d k=%d J=%d r=%d Q=%d M=%d ok=%s %.0fs" % (p, k, J, r, Q, len(cols), ok, time.time() - t0),
                  {x: st[x] for x in st if st[x] and x != "trace"}, st.get("trace"), flush=True)


def group_heavy():
    path = os.path.join(HERE, "..", "2026-11-05-rees-sde-q1", "heavy_found_3.jsonl")
    for J in (3, 4):
        P = Params(J, 2)
        for line in open(path):
            d = json.loads(line)
            Fd = Field(d["p"], d["k"])
            cols = d["cols"]
            if len(cols) >= P.F(rank(cols, Fd.p)[0]):
                run(Fd, cols, P, "heavy J=%d" % J)
        print("heavy J=%d" % J, dict(TOT), flush=True)


def group_fams():
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
        for J in (3, 4):
            if J < k:
                continue
            P = Params(J, k)
            for a in (8, 11, 12, 14, 16):
                M = P.F(a)
                for rep in range(2 if a <= 12 else 1):
                    fams = dict(family_list(rng, p, a, M, nr))
                    for name, cols in list(degenerate(Fd, a, M).items()):
                        fams[name] = (lambda c=cols: c)
                    for name, gen in fams.items():
                        cols = gen()
                        run(Fd, cols, P, "%s p=%d k=%d J=%d a=%d" % (name, p, k, J, a))
                print("fams p=%d k=%d J=%d a=%d" % (p, k, J, a), dict(TOT), flush=True)


def group_planted(strict=True, cap=None):
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        for J in (3, 4):
            P = Params(J, k, c=cap, strict=strict)
            shapes = [(14, [7]), (16, [8]), (20, [10]), (20, [6, 6]), (24, [8, 4]),
                      (18, [9]), (22, [11])]
            for r, Qs in shapes:
                M = P.F(r)
                for mix in (False, True):
                    cols = planted(Fd, r, Qs, J, M, mix)
                    run(Fd, cols, P, "planted p=%d J=%d r=%d Qs=%s" % (p, J, r, Qs))
            print("planted p=%d k=%d J=%d strict=%s c=%s" % (p, k, J, strict, P.c), dict(TOT), flush=True)


def group_critical():
    bdir = os.path.join(HERE, "..", "2026-11-05-rees-sde-q1-search", "banks")
    for fn in sorted(os.listdir(bdir)):
        d = json.load(open(os.path.join(bdir, fn)))
        cols = d.get("cols") or d.get("bank")
        p, k = d["p"], d.get("kappa", d.get("k"))
        Fd = Field(p, k)
        J = max(3, k)
        P = Params(J, k)
        r = rank(cols, p)[0]
        cols = [list(v) for v in cols]
        # pad with proportional copies of existing columns (keeps the structure)
        while len(cols) < P.F(r):
            v = cols[rng.randrange(len(cols))]
            t = rng.randrange(1, p)
            cols.append([t * z % p for z in v])
        run(Fd, cols, P, fn)
    print("critical", dict(TOT), flush=True)


def group_stress():
    group_planted(strict=False, cap=1)
    for (p, k) in [(10007, 2)]:
        Fd = Field(p, k)
        nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
        P = Params(3, k, c=1, strict=False)
        for a in (8, 11):
            M = P.F(a)
            for name, gen in family_list(rng, p, a, M, nr).items():
                run(Fd, gen(), P, "stress " + name)
        print("stress fams", dict(TOT), flush=True)


def group_climb():
    """maximise the least achievable load, J = 3, kappa = 2, a = 12, starting from planted."""
    p, k, J = 10007, 2, 3
    Fd = Field(p, k)
    P = Params(J, k)
    for start in range(3):
        r = 12
        M = P.F(r)
        best = planted(Fd, r, [6] if start else [5], J, M, mix=bool(start % 2))
        _, st = run(Fd, best, P, "climb start")
        bs = (st["max_needed_load"], st["maxq"])
        for it in range(80):
            c2 = [list(v) for v in best]
            i = rng.randrange(r, M)
            u = rng.random()
            if u < 0.4:
                j = rng.randrange(M)
                t = rng.randrange(1, p)
                c2[i] = [t * z % p for z in best[j]]
            elif u < 0.7:
                j, j2 = rng.randrange(M), rng.randrange(M)
                t, t2 = rng.randrange(1, p), rng.randrange(1, p)
                c2[i] = [(t * z + t2 * w) % p for z, w in zip(best[j], best[j2])]
            else:
                c2[i] = [rng.randrange(p) for _ in range(r)]
            _, st2 = run(Fd, c2, P, "climb")
            s2 = (st2["max_needed_load"], st2["maxq"])
            if s2 >= bs:
                best, bs = c2, s2
        print("climb start", start, "best (needed load, q)", bs, dict(TOT), flush=True)


{"heavy": group_heavy, "fams": group_fams, "planted": group_planted, "critical": group_critical,
 "stress": group_stress, "climb": group_climb, "vtwist": group_vtwist, "topbank": group_topbank, "topbank2": group_topbank2, "thmprime": group_thmprime, "vtwist2": group_vtwist2}[GROUP]()
print("TOTAL", GROUP, SEED, dict(TOT))
