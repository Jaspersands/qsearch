"""Driver for the referee's independent ALG-T (ref_alg.py).

Usage: ref_run.py GROUP SEED
  random    random banks at budget F(r), kappa in {2,3}, J in {3,4}
  planted   referee's planted banks: one or two early full circuits with q > c private
            directions (Rado-flat branch forced), with and without twisted E'-rounds whose
            private-direction components cancel inside every block of the REFEREE's split
            rule (so Z != empty, W != U), then pool columns; r up to 36
  agent     the agent's generators (run_tests.py: planted, vtwist, topbank; check/adv.py:
            topstall, multibig) used as DATA only: the banks are produced by the agent's code,
            then solved by the referee's code (different tie rules -> different flags)
  lemma2    Lemma 2 with absorbed singleton blocks at a small prime where failures are
            frequent: kappa = 2, J = 2, p = 257 (G*_3(257) >= 26 exactly), one absorbed
            singleton per round at most (E' = 3); first-pass failure frequency vs the bound
            rho * max(1/26, 2/256) summed over leaves
Every proof inequality is asserted inside ref_alg (strict).  Any AssertionError is a
counterexample to the bookkeeping and is printed with the bank.
"""
import os
import sys
import json
import time
import random
import traceback
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_alg as RA  # noqa

GROUP = sys.argv[1] if len(sys.argv) > 1 else "random"
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
rng = random.Random(SEED)
TOT = Counter()
FAILS = []


def merge(st):
    for k, v in st.items():
        if k.startswith("max"):
            TOT[k] = max(TOT[k], v)
        elif k == "minslack":
            TOT[k] = min(TOT.get(k, 10 ** 9), v)
        else:
            TOT[k] += v


def run(Fd, cols, P, label):
    st = Counter()
    st["maxblocks"] = st["maxload"] = st["maxrho"] = 0
    t0 = time.time()
    ok = False
    try:
        x = RA.solve_T(Fd, cols, P, rng, st)
        ok = RA.verify(Fd, cols, x)
    except RA.Unsolved as ex:
        print("UNSOLVED", label, ex, flush=True)
        FAILS.append((label, "unsolved", json.dumps(cols)))
    except AssertionError as ex:
        print("ASSERTION", label, repr(ex), flush=True)
        traceback.print_exc()
        FAILS.append((label, repr(ex), json.dumps(cols)))
    TOT["banks"] += 1
    TOT["solved"] += ok
    merge(st)
    return ok, st, time.time() - t0


def comb(p, basis, a):
    co = [rng.randrange(1, p) for _ in basis]
    return [sum(c * v[t] for c, v in zip(co, basis)) % p for t in range(a)]


def unit(a, i):
    v = [0] * a
    v[i] = 1
    return v


def fmt(st):
    return {k: v for k, v in st.items() if v}


# ---------------------------------------------------------------------------
# referee's planted banks
# ---------------------------------------------------------------------------


def my_planted(Fd, r, Qs, J, M, twist=0, mix=True):
    """Basis e_0..e_{r-1}; one full circuit of Q+1 generic columns in each coordinate block
    (keeps Q-J+1 private directions); then E' = remaining coordinates realised by circuits
    (k+1 columns, k <= J-1, inside span(E') + Omega); `twist` of those circuits carry
    components along a private direction v of the first big circuit, cancelled inside every
    block of the referee's split rule; then pool columns in span(E') (with proportional
    copies when mix)."""
    p = Fd.p
    cols = [unit(r, i) for i in range(r)]
    off = 0
    for Q in Qs:
        blk = [unit(r, i) for i in range(off, off + Q)]
        cols += [comb(p, blk, r) for _ in range(Q + 1)]
        off += Q
    # run the referee's forward pass on the prefix to learn Omega and a private direction
    st = RA.init_state(Fd, cols)
    status = RA.forward(Fd, cols, J, st)
    assert status == "stall", status
    UE = RA.flag_space(Fd, cols, st["rounds"])
    Om = UE.basis()
    # twist direction: a fresh coordinate e_{r-1}, never realised (as in the agent's vtwist),
    # so that the twisted round columns are in Rout, congruent to multiples of v modulo U
    v = unit(r, r - 1) if twist > 0 else None
    top = r - 1 if twist > 0 else r
    Ep = [unit(r, i) for i in range(off, top)]
    d = top - off
    real = 0
    ntw = 0
    while real < d:
        u = rng.random()
        if ntw < twist and d - real >= J:
            k = d - real                          # full circuit (blocks of size >= 2 exist)
        elif u < 0.6:
            k = min(J - 1, d - real)              # all columns of the round end inside U
        elif u < 0.8:
            k = min(d - real, max(1, J - 2))
        else:
            k = d - real                          # full circuit in the remaining quotient (adds Rout)
        base = len(cols)
        sub = [comb(p, Ep, r) for _ in range(k)]  # a k-dim generic subspace of span(E')
        us = [RA.vadd(comb(p, sub, r), comb(p, Om, r) if Om else [0] * r, p) for _ in range(k + 1)]
        E2 = UE.copy()
        for j in range(k):
            assert E2.add(us[j], tag=base + j)
        res, co = E2.reduce(us[k])
        assert not any(res)
        delta = {base + k: 1}
        for j in range(k):
            t = co.get(base + j, 0) % p
            assert t, "not a full circuit; retry"
            delta[base + j] = (-t) % p
        S = sorted(delta)
        if ntw < twist and v is not None and k + 1 > J:
            blocks = RA.split_blocks(Fd, S, delta, J)
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
                cols.append(RA.vadd(us[j], RA.vscale(tv[base + j], v, p), p))
            ntw += 1
        else:
            cols += us
        R = RA.Round(Fd, cols, S, delta, RA.split_blocks(Fd, S, delta, J))
        for w in R.W[1:]:
            assert UE.add(w)
        Om = UE.basis()
        real += min(J - 1, k)
    pool0 = len(cols)
    assert len(cols) <= M, (len(cols), M)
    while len(cols) < M:
        if mix and len(cols) > pool0 and len(cols) % 3 == 0:
            src = cols[rng.randrange(pool0, len(cols))]
            cols.append(RA.vscale(rng.randrange(1, p), src, p))
        else:
            cols.append(comb(p, Ep, r))
    return cols


def group_random():
    for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
        Fd = RA.Fld(p, k)
        for J in (3, 4):
            P = RA.Params(J, k)
            for r in (3, 4, 5, 6, 8, 10, 12):
                for rep in range(3):
                    M = P.F(r)
                    a = r + rng.randrange(0, 3)
                    basis = [[rng.randrange(p) for _ in range(a)] for _ in range(r)]
                    kind = rep % 3
                    if kind == 0:
                        cols = [comb(p, basis, a) for _ in range(M)]
                    elif kind == 1:   # many proportional / repeated columns
                        base = [comb(p, basis, a) for _ in range(r + 2)]
                        cols = [RA.vscale(rng.randrange(1, p), base[rng.randrange(len(base))], p) for _ in range(M)]
                        for i in range(r):
                            cols[rng.randrange(M)] = basis[i]
                    else:             # nested subspaces
                        cols = []
                        dd = 1
                        while len(cols) < M:
                            cols += [comb(p, basis[:dd], a) for _ in range(max(2, RA.DJ(dd, J) // 2))]
                            dd = min(r, dd + 1)
                        cols = cols[:M]
                    rr = RA.rank_of(cols, p, a)
                    if rr < 1 or len(cols) < P.F(rr):
                        continue
                    ok, st, dt = run(Fd, cols, P, "random p=%d k=%d J=%d r=%d kind=%d" % (p, k, J, rr, kind))
                    TOT["cases"] += 0
    print("TOTAL random", SEED, dict(TOT))


def group_planted():
    for (p, k) in [(1009, 2), (10007, 2), (10009, 3)]:
        Fd = RA.Fld(p, k)
        for J in ((2, 3, 4) if k == 2 else (3, 4)):
            P = RA.Params(J, k)
            c = P.c
            shapes = []
            # one big circuit with q = Q-J+1 > c; need b = r - Q >= q + 1  ->  r >= 2Q - J + 2
            for Q in (c + J, c + J + 2, c + J + 4):
                r = 2 * Q - J + 2 + rng.randrange(0, 3)
                shapes.append((r, [Q], 0))
                shapes.append((r + 3, [Q], 2))        # twisted: q = Q-J+2, needs r >= 2Q-J+4
            # two big circuits, each with private > c (|O_big| = 2)
            Q = c + J + 1
            r = 2 * (2 * Q) - J + 4
            shapes.append((r, [Q, Q], 0))
            shapes.append((r + 3, [Q, Q], 3))
            # one big with private exactly c (complete absorption), one with private c+2
            shapes.append((2 * (c + J - 1 + c + J + 1) - J + 5, [c + J - 1, c + J + 1], 1))
            # one big with private exactly c, no twist: complete absorption at load c, q+ = 0
            shapes.append((2 * (c + J - 1) - J + 2, [c + J - 1], 0))
            for (r, Qs, tw) in shapes:
                if r > 44:
                    continue
                M = P.F(r)
                try:
                    cols = my_planted(Fd, r, Qs, J, M, twist=tw, mix=(tw % 2 == 0))
                except AssertionError as ex:
                    print("generator skipped", r, Qs, tw, ex)
                    continue
                ok, st, dt = run(Fd, cols, P, "planted p=%d k=%d J=%d r=%d Qs=%s tw=%d" % (p, k, J, r, Qs, tw))
                print("planted p=%d k=%d J=%d r=%d Qs=%s tw=%d M=%d ok=%s %.0fs" % (p, k, J, r, Qs, tw, M, ok, dt), fmt(st), flush=True)
    print("TOTAL planted", SEED, dict(TOT))


def group_agent():
    """Banks from the agent's generators, solved by the referee's code."""
    AG = os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A")
    sys.path.insert(0, AG)
    sys.path.insert(0, os.path.join(AG, "..", "2026-11-05-rees-sde-q1"))
    import subquad as SQ  # noqa  (the agent's code: generators only)
    src = open(os.path.join(AG, "run_tests.py")).read()
    # execute the agent's module up to (not including) its module-level dispatch dict
    cut = src.index('{"heavy": group_heavy')
    ns = {"__name__": "agent_run_tests", "__file__": os.path.join(AG, "run_tests.py")}
    exec(compile(src[:cut], "agent_run_tests", "exec"), ns)
    gens = {k: ns[k] for k in ("planted", "vtwist", "topbank")}
    ns["rng"] = random.Random(SEED + 100)      # the agent's generators draw from their module rng
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd_ag = SQ.Field(p, k)
        Fd = RA.Fld(p, k)
        for J in (3, 4):
            P = RA.Params(J, k)
            Pag = SQ.Params(J, k)
            for r in (16, 20, 24):
                Q = 2 * (J - 1) + J + 1
                if r < 2 * Q - J + 2:
                    continue
                cols = gens["planted"](Fd_ag, r, [Q], J, Pag.F(r))
                ok, st, dt = run(Fd, cols, P, "agent-planted p=%d J=%d r=%d" % (p, J, r))
                print("agent-planted p=%d k=%d J=%d r=%d ok=%s %.0fs" % (p, k, J, r, ok, dt), fmt(st), flush=True)
            for r in (24, 28):
                try:
                    cols = gens["vtwist"](Fd_ag, r, 8, J, Pag.F(r))
                except AssertionError as ex:
                    print("vtwist generator skipped", repr(ex))
                    continue
                ok, st, dt = run(Fd, cols, P, "agent-vtwist p=%d J=%d r=%d" % (p, J, r))
                print("agent-vtwist p=%d k=%d J=%d r=%d ok=%s %.0fs" % (p, k, J, r, ok, dt), fmt(st), flush=True)
        # the agent's topbank shapes (r, b, k, nrest, m, degenerate), J = 3 and J = 4
        for (J, r, b, kk, nrest, m, dg) in [(3, 18, 5, 5, 7, 1, False), (3, 20, 6, 5, 7, 2, False),
                                             (3, 22, 7, 5, 7, 3, False), (3, 20, 6, 6, 6, 2, True),
                                             (3, 22, 7, 5, 8, 2, True), (3, 16, 6, 4, 5, 1, False),
                                             (3, 26, 8, 5, 9, 4, False), (4, 40, 4, 4, 30, 2, True),
                                             (4, 40, 4, 4, 30, 2, False)]:
            P = RA.Params(J, k)
            Pag = SQ.Params(J, k)
            for rep in range(2):
                try:
                    cols = gens["topbank"](Fd_ag, r, b, kk, nrest, m, J, Pag.F(r), dg)
                except Exception as ex:
                    print("topbank generator skipped", (J, r, b, kk, nrest, m, dg), repr(ex))
                    continue
                ok, st, dt = run(Fd, cols, P, "agent-topbank p=%d J=%d r=%d m=%d deg=%s" % (p, J, r, m, dg))
                print("agent-topbank p=%d k=%d J=%d r=%d m=%d deg=%s ok=%s %.0fs" % (p, k, J, r, m, dg, ok, dt), fmt(st), flush=True)
    print("TOTAL agent", SEED, dict(TOT))


def group_adv():
    """Banks from the agent's check generators (check/adv.py: topstall, multibig), solved by the
    referee's code; aimed at the top-phase stall T_m(b) and at |O_big| >= 2 with twists."""
    AG = os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A")
    CK = os.path.join(AG, "check")
    sys.path.insert(0, AG)
    sys.path.insert(0, os.path.join(AG, "..", "2026-11-05-rees-sde-q1"))
    import subquad as SQ  # noqa
    src = open(os.path.join(CK, "adv.py")).read()
    cut = src.index('{"topstall": group_topstall')
    ns = {"__name__": "agent_adv", "__file__": os.path.join(CK, "adv.py")}
    saved_argv = sys.argv
    sys.argv = ["adv.py", "topstall", str(SEED + 7)]
    exec(compile(src[:cut], "agent_adv", "exec"), ns)
    sys.argv = saved_argv
    SQ.recurse = ns["_orig_recurse"]          # undo the check's wrapper (not used by us anyway)
    p, k = 10007, 2
    Fd_ag = SQ.Field(p, k)
    Fd = RA.Fld(p, k)
    for (J, r, b, kk, dg) in [(4, 46, 5, 4, True), (5, 38, 5, 5, True), (4, 46, 5, 4, False)]:
        P = RA.Params(J, k)
        Pag = SQ.Params(J, k)
        cols = ns["topstall"](Fd_ag, J, r, b, kk, Pag.F(r), dg)
        ok, st, dt = run(Fd, cols, P, "adv-topstall p=%d J=%d r=%d deg=%s" % (p, J, r, dg))
        print("adv-topstall p=%d k=%d J=%d r=%d b=%d k=%d deg=%s ok=%s %.0fs" % (p, k, J, r, b, kk, dg, ok, dt), fmt(st), flush=True)
    for (J, r, Qs, s, noise) in [(3, 34, [8, 8], 2, 0), (3, 36, [7, 7, 7], 1, 3), (4, 44, [10, 10], 1, 0), (3, 28, [8], 3, 3)]:
        P = RA.Params(J, k)
        Pag = SQ.Params(J, k)
        try:
            cols = ns["multibig"](Fd_ag, J, r, Qs, s, Pag.F(r), noise)
        except AssertionError as ex:
            print("multibig generator skipped", repr(ex))
            continue
        ok, st, dt = run(Fd, cols, P, "adv-multibig p=%d J=%d r=%d Qs=%s s=%d" % (p, J, r, Qs, s))
        print("adv-multibig p=%d k=%d J=%d r=%d Qs=%s s=%d noise=%d ok=%s %.0fs" % (p, k, J, r, Qs, s, noise, ok, dt), fmt(st), flush=True)
    print("TOTAL adv", SEED, dict(TOT))


def group_lemma2():
    """Lemma 2 with absorbed blocks at p = 257, kappa = 2, J = 2 (2-block rounds), at most one
    absorbed singleton per round (E' = 3), G*_3(257) >= 26 (worst-case report section 1: exact
    G*_3(p) >= p/10 for p >= 256).  For each leaf: record the first-pass failure indicator and
    the bound rho*max(1/26, 2/256) = rho/26."""
    p, k, J = 257, 2, 2
    Fd = RA.Fld(p, k)
    Gstar = 26
    leaves = 0
    fails1 = 0
    bound_sum = 0.0
    passes = 0
    failsall = 0
    coinc_fails = 0
    nblocks3 = 0
    for it in range(400):
        r = rng.choice([3, 4, 5, 6])
        a = r
        basis = [[rng.randrange(p) for _ in range(a)] for _ in range(r)]
        M = RA.DJ(r, J) + 2 * r
        # planted: a full circuit of r columns in a (r-1)-space keeps r-2 private directions
        cols = [list(b) for b in basis]
        cols += [comb(p, basis[:r - 1], a) for _ in range(r)]
        while len(cols) < M:
            cols.append(comb(p, basis, a))
        st = RA.init_state(Fd, cols)
        rr = RA.rank_of(cols, p, a)
        # run to the first round, absorb one private column of it (3 blocks), continue
        status = RA.forward(Fd, cols, J, st, pause_after=1)
        if status != "paused":
            continue
        rounds = st["rounds"]
        UE = RA.flag_space(Fd, cols, rounds)
        R0 = rounds[0]
        priv = [i for i in R0.S if not UE.contains(cols[i])]
        if not priv:
            continue
        RA.absorb(Fd, cols, rounds, [priv[rng.randrange(len(priv))]])
        status = RA.forward(Fd, cols, J, st)
        if status != "reached":
            continue
        rounds = list(st["rounds"])
        UE = RA.flag_space(Fd, cols, rounds)
        assert len(UE) == rr
        B = st["B"]
        src = B
        if RA.steer_violations(Fd, cols, rounds, UE, src):
            continue
        nb = max(len(R.blocks) for R in rounds)
        if nb > 3:
            continue
        nblocks3 += (nb == 3)
        rho = RA.cross_pairs(rounds)
        bound = min(1.0, rho * max(1.0 / Gstar, 2.0 / 256))
        leaves += 1
        bound_sum += bound
        x, info = RA.backward(Fd, cols, rounds, UE, src, rng)
        if x is None:
            fails1 += 1
        else:
            assert RA.verify(Fd, cols, x)
        for t in range(20):
            x, info = RA.backward(Fd, cols, rounds, UE, src, rng)
            passes += 1
            if x is None:
                failsall += 1
                coinc_fails += info["coinc"]
            else:
                assert RA.verify(Fd, cols, x)
    print("lemma2 p=257 kappa=2 J=2 (+<=1 absorbed singleton): leaves=%d (with a 3-block round: %d), first-pass failures=%d, sum of Lemma-2 bounds=%.1f; all passes: %d fails / %d (every fail had a cross-class coincidence: %s)"
          % (leaves, nblocks3, fails1, bound_sum, failsall, passes, coinc_fails == failsall))
    print("TOTAL lemma2", SEED, dict(TOT))


if __name__ == "__main__":
    {"random": group_random, "planted": group_planted, "agent": group_agent, "adv": group_adv,
     "lemma2": group_lemma2}[GROUP]()
    if FAILS:
        print("FAILURES", len(FAILS))
        for f in FAILS[:5]:
            print(f[0], f[1], f[2][:400])
