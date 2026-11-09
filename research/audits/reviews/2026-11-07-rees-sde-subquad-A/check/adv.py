"""Adversarial runs of ALG-T (../subquad.py: solve_T, strict mode) by the referee.

Usage: adv.py GROUP SEED
  topstall  own generator aimed at the untested branch Lemma T_m(b) (top-phase stall,
            m = 2, J in {4,5}) and at the top phase with m = 2 (T_m(a), J >= 4).
  multibig  own generator: several early full circuits whose private directions each
            exceed c (|O_big| >= 2), plus s >= 1 twisted directions cancelled inside
            every block (so W = U + span(twisted) may differ from U).
  shuffle   the authors' generators (planted, vtwist, topbank; exec'd from run_tests.py
            without its dispatch) with the tail of the column order perturbed
            (k random transpositions, or a full shuffle of the non-basis tail).
  climb     hill climb from multibig/planted banks, J = 3, maximising (number of
            recursions, depth, least needed load) and recording the least slack of every
            recursion count (cols in flat - F(dim flat)).
Every witness is re-verified by an independent checker (pow test for P, exact sum).
Strict mode: every proof inequality is asserted inside solve_T; any AssertionError is
caught, printed with the bank, and counted as a FAILURE.
"""
import os
import sys
import json
import time
import random
import traceback
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.join(HERE, "..")
sys.path.insert(0, PARENT)
sys.path.insert(0, os.path.join(PARENT, "..", "2026-11-05-rees-sde-q1"))
import subquad  # noqa
from subquad import Field, Params, solve_T, new_stats, DJ, rank, init_state, forward_fast, split_blocks  # noqa
from fastla import Ech  # noqa

GROUP = sys.argv[1] if len(sys.argv) > 1 else "topstall"
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
rng = random.Random(SEED)
TOT = Counter()

# ---- recursion slack recorder (wraps subquad.recurse; does not change behaviour) ----
_orig_recurse = subquad.recurse
SLACK = []


def _rec(Fd, cols, Yb, P, rng_, stats, depth, kind):
    p = Fd.p
    n = sum(1 for v in cols if subquad.in_span(Yb, v, p))
    SLACK.append((kind, len(Yb), n - P.F(len(Yb))))
    return _orig_recurse(Fd, cols, Yb, P, rng_, stats, depth, kind)


subquad.recurse = _rec


def my_check(Fd, cols, x):
    p, k = Fd.p, Fd.k
    if x is None or not any(v % p for v in x):
        return False
    for v in x:
        if v % p and pow(v % p, (p - 1) // k, p) != 1:
            return False
    a = len(cols[0])
    return all(sum(x[i] * cols[i][t] for i in range(len(cols))) % p == 0 for t in range(a))


def run(Fd, cols, P, label):
    st = new_stats()
    SLACK.clear()
    t0 = time.time()
    try:
        x = solve_T(Fd, cols, P, rng, st)
        ok = my_check(Fd, cols, x)
        err = None
    except AssertionError as e:
        ok, err = False, repr(e)
        traceback.print_exc()
    TOT["banks"] += 1
    TOT["solved"] += ok
    if err:
        TOT["ASSERTION_FAIL"] += 1
    for k, v in st.items():
        if k == "trace":
            continue
        if k.startswith("max"):
            TOT[k] = max(TOT[k], v)
        else:
            TOT[k] += v
    for kind, d, s in SLACK:
        key = "minslack:" + kind
        TOT[key] = s if key not in TOT else min(TOT[key], s)
    if not ok:
        print("FAILURE", label, err, json.dumps(cols), flush=True)
    keys = {k: st[k] for k in st if st[k] and k != "trace"}
    print("%s ok=%s %.1fs" % (label, ok, time.time() - t0), keys,
          [(d["r"], d["q"], d["b"], d["eps"], d["X"], d["Rout"]) for d in st.get("trace", [])],
          "slack", SLACK[:], flush=True)
    return ok, st


def unit(a, i):
    v = [0] * a
    v[i] = 1
    return v


def comb(p, basis, a):
    if not basis:
        return [0] * a
    co = [rng.randrange(1, p) for _ in basis]
    return [sum(c * v[t] for c, v in zip(co, basis)) % p for t in range(a)]


def vadd(p, u, w):
    return [(x + y) % p for x, y in zip(u, w)]


# ---------------------------------------------------------------------------
# own generator 1: top-phase stall (Lemma T_m(b))
# ---------------------------------------------------------------------------

def topstall(Fd, J, r, b, k, M, degenerate=True):
    """B = e_0..e_{r-1}; Y = e_0..e_{b-1} (in U, b of them); gens g_j = e_j + t_j e_b
    (j = b+2..r-1) span, with Y, the hyperplane-pair H = U+ of codim 2.  One early full
    circuit of k+1 columns generic in a k-dim subspace of span(gens) keeps k-J+1 private
    directions; later full circuits realise Om1 + Y + Orest.  Then pool in Y.
    Mod H every e_j (j >= b+2) is a multiple of e_b, so the top pass stalls at codim 1."""
    p = Fd.p
    cols = [unit(r, i) for i in range(r)]
    Y = [unit(r, i) for i in range(b)]
    gens = []
    for j in range(b + 2, r):
        v = unit(r, j)
        if degenerate:
            v[b] = rng.randrange(1, p)
        else:
            v[b] = rng.randrange(1, p)
            v[b + 1] = rng.randrange(1, p)
        gens.append(v)
    nrest = len(gens) - k
    assert nrest >= 1
    G = [comb(p, gens, r) for _ in range(len(gens))]
    A1, Orest = G[:k], G[k:]
    cols += [comb(p, A1, r) for _ in range(k + 1)]
    st = init_state(Fd, cols)
    forward_fast(Fd, cols, J, rng, st, rule="first")
    EU = Ech(p, r)
    for R in st["rounds"]:
        for w in R.W[1:]:
            EU.add(w)
    Om1 = [row for _, row, _ in EU.rows]
    space = Om1 + Y + Orest
    qq, n2 = b + nrest, 0          # Om1 is already realised
    while qq >= 1:
        n2 += qq + 1
        qq -= min(J - 1, qq)
    cols += [comb(p, space, r) for _ in range(n2)]
    assert len(cols) <= M, (len(cols), M)
    while len(cols) < M:
        cols.append(comb(p, Y, r))
    return cols


def group_topstall():
    for (p, kap) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, kap)
        for (J, r, b, k, dg) in [(4, 46, 5, 4, True), (4, 48, 5, 4, True), (4, 48, 5, 5, True),
                                 (5, 38, 5, 5, True), (5, 40, 6, 6, True), (5, 40, 5, 5, False),
                                 (4, 46, 5, 4, False)]:
            if J < kap:
                continue
            P = Params(J, kap)
            for rep in range(2):
                cols = topstall(Fd, J, r, b, k, P.F(r), dg)
                run(Fd, cols, P, "topstall p=%d J=%d r=%d b=%d k=%d deg=%s" % (p, J, r, b, k, dg))
        print("PARTIAL", dict(TOT), flush=True)


# ---------------------------------------------------------------------------
# own generator 2: several big rounds with > c private directions, s twisted directions
# ---------------------------------------------------------------------------

def multibig(Fd, J, r, Qs, s, M, order_noise=0):
    p = Fd.p
    cols = [unit(r, i) for i in range(r)]
    off = 0
    for Q in Qs:
        blk = [unit(r, off + i) for i in range(Q)]
        cols += [comb(p, blk, r) for _ in range(Q + 1)]
        off += Q
    st = init_state(Fd, cols)
    forward_fast(Fd, cols, J, rng, st, rule="first")
    EU = Ech(p, r)
    for R in st["rounds"]:
        for w in R.W[1:]:
            EU.add(w)
    Om = [row for _, row, _ in EU.rows]
    vs = list(range(r - s, r))
    Ep = [unit(r, i) for i in range(off, r - s)]
    d = len(Ep)
    real = 0
    while real < d:
        k = d - real
        base = len(cols)
        us = [vadd(p, comb(p, Ep, r), comb(p, Om, r)) for _ in range(k + 1)]
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
        tv = {i: [0] * s for i in S}
        for G in blocks:
            if len(G) == 1:
                continue
            for z in range(s):
                if rng.random() < 0.3:
                    continue          # this twist direction absent from this block
                ts = [rng.randrange(1, p) for _ in G[:-1]]
                last = (-sum(delta[i] * t for i, t in zip(G[:-1], ts)) * pow(delta[G[-1]], p - 2, p)) % p
                for i, t in zip(G, ts + [last]):
                    tv[i][z] = t
        for j in range(k + 1):
            v = list(us[j])
            for z in range(s):
                v[vs[z]] = (v[vs[z]] + tv[base + j][z]) % p
            cols.append(v)
        W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(r)] for G in blocks]
        for w in W[1:]:
            assert EU.add(w)
        real += min(J - 1, k)
        Om = [row for _, row, _ in EU.rows]
    assert len(cols) <= M, (len(cols), M)
    while len(cols) < M:
        cols.append(comb(p, Ep, r))
    if order_noise:
        tail = list(range(r, M))
        for _ in range(order_noise):
            i, j = rng.sample(tail, 2)
            cols[i], cols[j] = cols[j], cols[i]
    return cols


def group_multibig():
    for (p, kap) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, kap)
        shapes = [(3, 34, [8, 8], 2), (3, 34, [8, 8], 1), (3, 30, [7, 7], 1), (3, 36, [7, 7, 7], 1),
                  (3, 32, [9, 7], 2), (3, 28, [8], 3), (3, 40, [8, 8, 8], 2)]
        if kap <= 4:
            shapes += [(4, 44, [10, 10], 1)]
        for (J, r, Qs, s) in shapes:
            if J < kap:
                continue
            P = Params(J, kap)
            for noise in (0, 3):
                try:
                    cols = multibig(Fd, J, r, Qs, s, P.F(r), noise)
                except AssertionError as e:
                    print("generator skipped", r, Qs, s, repr(e), flush=True)
                    continue
                run(Fd, cols, P, "multibig p=%d J=%d r=%d Qs=%s s=%d noise=%d" % (p, J, r, Qs, s, noise))
        print("PARTIAL", dict(TOT), flush=True)


# ---------------------------------------------------------------------------
# authors' generators with perturbed column order
# ---------------------------------------------------------------------------

def load_author_gens():
    src = open(os.path.join(PARENT, "run_tests.py")).read()
    cut = src.index('{"heavy": group_heavy')
    ns = {"__file__": os.path.join(PARENT, "run_tests.py"), "__name__": "author_gens"}
    saved = sys.argv
    sys.argv = ["run_tests.py", "none", "0"]
    exec(compile(src[:cut], "run_tests.py", "exec"), ns)
    sys.argv = saved
    ns["rng"] = rng
    return ns


def perturb(cols, r, mode):
    cols = [list(v) for v in cols]
    tail = list(range(r, len(cols)))
    if mode == "full":
        t = [cols[i] for i in tail]
        rng.shuffle(t)
        for i, v in zip(tail, t):
            cols[i] = v
    else:
        for _ in range(mode):
            i, j = rng.sample(tail, 2)
            cols[i], cols[j] = cols[j], cols[i]
    return cols


def group_shuffle():
    ns = load_author_gens()
    for (p, kap) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, kap)
        for J in (3, 4):
            if J < kap:
                continue
            P = Params(J, kap)
            for r, Qs in [(14, [7]), (20, [10]), (24, [8, 4]), (22, [11])]:
                base = ns["planted"](Fd, r, Qs, J, P.F(r), True)
                for mode in (1, 3, 10, "full"):
                    run(Fd, perturb(base, r, mode), P, "planted-perturb p=%d J=%d r=%d Qs=%s mode=%s" % (p, J, r, Qs, mode))
        P = Params(3, kap)
        for r in (24, 28):
            base = ns["vtwist"](Fd, r, 8, 3, P.F(r))
            for mode in (1, 3, 10):
                run(Fd, perturb(base, r, mode), P, "vtwist-perturb p=%d r=%d mode=%s" % (p, r, mode))
        for (r, b, kk, nrest, m, dg) in [(18, 5, 5, 7, 1, False), (22, 7, 5, 7, 3, False), (20, 6, 6, 6, 2, True)]:
            base = ns["topbank"](Fd, r, b, kk, nrest, m, 3, P.F(r), dg)
            for mode in (1, 3, 10):
                run(Fd, perturb(base, r, mode), P, "topbank-perturb p=%d r=%d m=%d mode=%s" % (p, r, m, mode))
        print("PARTIAL", dict(TOT), flush=True)


# ---------------------------------------------------------------------------
# hill climb
# ---------------------------------------------------------------------------

def score(st):
    tr = st.get("trace", [])
    nrec = sum(v for k, v in st.items() if k.startswith("rec:"))
    return (nrec, st.get("W_events", 0), len(tr), st.get("max_needed_load", 0))


def group_climb():
    p, kap, J = 10007, 2, 3
    Fd = Field(p, kap)
    P = Params(J, kap)
    starts = [("multibig", lambda: multibig(Fd, 3, 30, [7, 7], 1, P.F(30))),
              ("multibig", lambda: multibig(Fd, 3, 28, [8], 2, P.F(28))),
              ("topstall-like", lambda: multibig(Fd, 3, 24, [7], 1, P.F(24)))]
    for name, mk in starts:
        best = None
        while best is None:          # the generator itself can hit a zero coefficient
            try:
                best = mk()
            except AssertionError:
                print("generator retry", name, flush=True)
        r = rank(best, p)[0]
        _, st = run(Fd, best, P, "climb-start " + name)
        bs = score(st)
        M = len(best)
        for it in range(40):
            c2 = [list(v) for v in best]
            for _ in range(rng.randrange(1, 4)):
                i = rng.randrange(r, M)
                u = rng.random()
                if u < 0.35:
                    j = rng.randrange(M)
                    c2[i] = [rng.randrange(1, p) * z % p for z in best[j]]
                elif u < 0.7:
                    j, j2 = rng.randrange(M), rng.randrange(M)
                    t, t2 = rng.randrange(1, p), rng.randrange(1, p)
                    c2[i] = [(t * z + t2 * w) % p for z, w in zip(best[j], best[j2])]
                elif u < 0.85:
                    j = rng.randrange(r, M)
                    c2[i], c2[j] = c2[j], c2[i]
                else:
                    c2[i] = [rng.randrange(p) for _ in range(len(best[0]))]
            if not any(any(v) for v in c2):
                continue
            ok, st2 = run(Fd, c2, P, "climb %s it=%d" % (name, it))
            if not ok:
                continue
            s2 = score(st2)
            if s2 >= bs:
                best, bs = c2, s2
        print("climb", name, "best score (nrec, W, stalls, need)", bs, flush=True)
    print("PARTIAL", dict(TOT), flush=True)


{"topstall": group_topstall, "multibig": group_multibig, "shuffle": group_shuffle,
 "climb": group_climb}[GROUP]()
print("TOTAL", GROUP, SEED, dict(TOT))
