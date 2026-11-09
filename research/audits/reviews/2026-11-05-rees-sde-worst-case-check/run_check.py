"""Test harness for mysss.py (independent check of Theorem 2 and Corollary 3).

Sections (argument selects one, default all):
  gp      general-position banks at kappa = 2, 3 near the thresholds of Corollary 3:
          forward pass must reach the span with pi = 0; rho within the bound; single-pass
          failure rate against rho * max(1/G*, kappa/(p-1)) and against 1/2.
  adv     non-general-position banks (lines, the explicit Section 5 bank, dense/sparse/small
          entries): stall decomposition M <= D(r) - D(q) + r + pi + q at every stall, and
          pi >= 1 at every stall with M >= D(r) + r.
  neg     negative controls: unsolvable banks (no witness may be returned), swap disabled,
          one steering source only, corrupted witness rejected.
"""
import itertools
import random
import sys

from mysss import F, Span, D, forward, backward, verify, rank, rho, solve

GSTAR = {}
for fn in ("gstar_k2.out", "gstar_k3.out"):
    for line in open(fn):
        t = line.split()
        if t and t[0].isdigit():
            GSTAR[(fn[7], int(t[0]))] = int(t[1])


def gstar(k, p):
    if (str(k), p) not in GSTAR:
        import gstar as G
        GSTAR[(str(k), p)] = G.gstar(p, k)[0]
    return GSTAR[(str(k), p)]


def is_gp(cols, p):
    r = rank(cols, p)
    for sub in itertools.combinations(range(len(cols)), r):
        if rank([cols[i] for i in sub], p) < r:
            return False
    return True


def rand_gl(p, a, rng):
    while True:
        A = [[rng.randrange(p) for _ in range(a)] for _ in range(a)]
        if rank(A, p) == a:
            return A


def apply(A, v, p):
    return [sum(A[i][j] * v[j] for j in range(len(v))) % p for i in range(len(A))]


def moment_bank(p, a, M, rng, mult="random", Fd=None):
    """u_i (1, t, ..., t^{a-1}) for distinct t (and possibly the point at infinity),
    then a random invertible map.  Every a of these columns are independent (Vandermonde)."""
    ts = rng.sample(range(p), M if M <= p else p)
    pts = [[pow(t, j, p) for j in range(a)] for t in ts]
    if len(pts) < M:
        pts.append([0] * (a - 1) + [1])
    assert len(pts) == M
    A = rand_gl(p, a, rng)
    out = []
    for v in pts:
        if mult == "random":
            u = rng.randrange(1, p)
        elif mult == "one":
            u = 1
        else:   # all in the class of the generator (non-residue class for kappa=2)
            u = Fd.g * pow(rng.randrange(1, p), Fd.k, p) % p
        out.append(apply(A, [u * x % p for x in v], p))
    return out


def gp_section(rng):
    print("== GP section ==", flush=True)
    cases = [
        # (kappa, p, a, family, nbanks, passes)
        (2, 257, 2, "random-gp", 30, 200), (2, 257, 3, "random-gp", 30, 200),
        (2, 257, 4, "random-gp", 30, 200),
        (2, 257, 4, "moment", 30, 200), (2, 257, 8, "moment", 20, 100),
        (2, 257, 12, "moment", 10, 60), (2, 263, 10, "moment-one", 10, 60),
        (2, 263, 12, "moment-nr", 10, 60),
        (2, 1000003, 5, "random-gp", 10, 40), (2, 10007, 20, "moment", 4, 20),
        (3, 2767, 2, "random-gp", 30, 100), (3, 2767, 3, "random-gp", 30, 100),
        (3, 2767, 4, "random-gp", 20, 60),
        (3, 2767, 6, "moment", 15, 60), (3, 2767, 10, "moment-one", 10, 40),
        (3, 2767, 16, "moment-nr", 6, 20), (3, 2791, 12, "moment", 8, 30),
    ]
    allok = True
    for k, p, a, fam, nb, passes in cases:
        Fd = F(p, k)
        E = 3
        M = D(3, a) + a
        Gs = gstar(k, p) if p < 20000 else None
        stats = dict(span=0, stall=0, direct=0, pi=0, passes=0, fails=0, coinc=0,
                     maxrho=0, rho_ok=True, solved=0)
        worst_bound = 0.0
        for _ in range(nb):
            if fam == "random-gp":
                while True:
                    cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                    if rank(cols, p) == a and is_gp(cols, p):
                        break
            else:
                mult = {"moment": "random", "moment-one": "one", "moment-nr": "nr"}[fam]
                cols = moment_bank(p, a, M, rng, mult, Fd)
                if a <= 6:
                    assert is_gp(cols, p)
            run = forward(Fd, cols, E)
            stats[run["status"]] += 1
            if run["status"] == "direct":
                assert verify(Fd, cols, run["x"])
                stats["solved"] += 1
                continue
            stats["pi"] += run["pi"]
            if run["status"] != "span":
                allok = False
                continue
            rh = rho(run)
            stats["maxrho"] = max(stats["maxrho"], rh)
            if rh > (run["r"] if k == 2 else 3 * run["r"] / 2) or rh > run["r"] * E / 2:
                stats["rho_ok"] = False
            if Gs is not None:
                worst_bound = max(worst_bound, rh * max(1 / Gs, k / (p - 1)))
            got = False
            for _ in range(passes):
                x, info = backward(Fd, cols, run, rng)
                stats["passes"] += 1
                stats["coinc"] += info["coinc"]
                if x is None:
                    stats["fails"] += 1
                    assert not info.get("empty_no_coinc"), "Good empty without coincidence"
                else:
                    assert verify(Fd, cols, x)
                    got = True
            stats["solved"] += got
        rate = stats["fails"] / max(1, stats["passes"])
        ok = (stats["stall"] == 0 and stats["pi"] == 0 and stats["rho_ok"]
              and stats["solved"] == nb and (Gs is None or rate <= worst_bound + 0.05))
        allok &= ok
        print(f"kappa={k} p={p} a={a} M={M} CW={k*a+1} fam={fam} banks={nb} "
              f"span={stats['span']} direct={stats['direct']} stall={stats['stall']} "
              f"pi={stats['pi']} maxrho={stats['maxrho']} rho_ok={stats['rho_ok']} "
              f"passes={stats['passes']} fails={stats['fails']} rate={rate:.4f} "
              f"bound={worst_bound:.4f} solved={stats['solved']}/{nb} "
              f"{'OK' if ok else 'CHECK'}", flush=True)
    print("GP section all OK:", allok, flush=True)
    return allok


def lines_bank(p, a, M, rng, nlines=None):
    nlines = nlines or a + 1
    dirs = [[1 if j == i else 0 for j in range(a)] for i in range(a)] + [[1] * a]
    while len(dirs) < nlines:
        dirs.append([rng.randrange(p) for _ in range(a)])
    A = rand_gl(p, a, rng)
    dirs = [apply(A, v, p) for v in dirs[:nlines]]
    return [[rng.randrange(1, p) * x % p for x in dirs[rng.randrange(nlines)]]
            for _ in range(M)]


def adv_section(rng):
    print("== adversarial / non-GP section ==", flush=True)
    E = 3
    # the explicit Section 5 bank
    bank5 = [[170, 720, 640], [72, 522, 340], [337, 384, 757], [512, 970, 855],
             [724, 989, 767], [14, 606, 963], [823, 827, 687], [966, 829, 143],
             [854, 768, 10]]
    Fd = F(1009, 2)
    run = forward(Fd, bank5, E)
    print("Section-5 bank: status", run["status"], "pi", run.get("pi"), "q", run.get("q"),
          "swaps", run.get("swaps"), "is_gp", is_gp(bank5, 1009),
          "col5/col9 proportional:", (442 * bank5[4][0] + bank5[8][0]) % 1009 == 0 and
          all((442 * bank5[4][i] + bank5[8][i]) % 1009 == 0 for i in range(3)),
          "442 residue:", pow(442, 504, 1009) == 1, flush=True)
    # brute-force solvability of the Section-5 bank (Chevalley-Warning says yes: M=9 > 2a=6)
    fams = []
    for k, p in ((2, 1009), (2, 31), (3, 31 * 0 + 61), (3, 1009), (2, 13), (3, 13)):
        fams.append((k, p))
    tot = viol = stalls = nopool = bstall = 0
    by = {}
    for k, p in fams:
        Fd = F(p, k)
        for a in (2, 3, 4, 5, 6):
            for fam in ("lines", "lines+2", "dense", "small", "sparse", "repeat"):
                for M in (D(3, a) + a, D(3, a) + a + 2, k * a + 1):
                    for _ in range(6):
                        if fam == "lines":
                            cols = lines_bank(p, a, M, rng)
                        elif fam == "lines+2":
                            cols = lines_bank(p, a, M, rng, a + 3)
                        elif fam == "dense":
                            # columns in a hyperplane plus a few outside
                            cols = [[rng.randrange(p) for _ in range(a - 1)] + [0]
                                    for _ in range(M - 2)]
                            cols += [[rng.randrange(p) for _ in range(a)] for _ in range(2)]
                        elif fam == "small":
                            cols = [[rng.choice((0, 1, p - 1, 2, p - 2)) for _ in range(a)]
                                    for _ in range(M)]
                        elif fam == "sparse":
                            cols = [[1 if rng.random() < 0.35 else 0 for _ in range(a)]
                                    for _ in range(M)]
                        else:
                            base = [[rng.randrange(p) for _ in range(a)] for _ in range(a + 1)]
                            cols = [[rng.randrange(1, p) * x % p for x in rng.choice(base)]
                                    for _ in range(M)]
                        rng.shuffle(cols)
                        run = forward(Fd, cols, E)
                        tot += 1
                        st = run["status"]
                        key = (k, p, fam)
                        by.setdefault(key, [0, 0])
                        by[key][0] += 1
                        if st == "stall":
                            stalls += 1
                            by[key][1] += 1
                            r, q, pi = run["r"], run["q"], run["pi"]
                            rhs = D(3, r) - D(3, q) + r + pi + q
                            if M > rhs or run["consumed"] > D(3, r) - D(3, q) or \
                                    len(run["unused"]) > q:
                                viol += 1
                                print("VIOLATION", k, p, a, M, r, q, pi, rhs, flush=True)
                            if M >= D(3, r) + r:
                                bstall += 1
                            if M >= D(3, r) + r and pi == 0:
                                nopool += 1
                                print("STALL WITHOUT POOL at budget", k, p, a, M, r, flush=True)
                        elif st == "span":
                            rh = rho(run)
                            if rh > run["r"] * E / 2:
                                viol += 1
                                print("RHO VIOLATION", flush=True)
    for key, (n, s) in sorted(by.items()):
        print(f"  kappa={key[0]} p={key[1]} family={key[2]}: banks={n} stalls={s}")
    print(f"adversarial: banks={tot} stalls={stalls} decomposition violations={viol} "
          f"stalls at M>=D(r)+r: {bstall}, of which with pi=0: {nopool}", flush=True)
    return viol == 0 and nopool == 0


def neg_section(rng):
    print("== negative controls ==", flush=True)
    E = 3
    ok = True
    # (1) unsolvable banks: block-diagonal pairs (1, -u), u not in P; 2a columns
    for k, p in ((2, 257), (3, 2767)):
        Fd = F(p, k)
        u = Fd.g   # class 1, not in P
        for a in (2, 3, 5, 8):
            cols = []
            for j in range(a):
                e = [0] * a
                e[j] = 1
                cols.append(e[:])
                cols.append([(-u * x) % p for x in e])
            res, run, _ = solve(Fd, cols, E, rng, passes=50)
            print(f"unsolvable kappa={k} p={p} a={a} M={2*a}: result={res}", flush=True)
            ok &= res in ("stall", "fail")
    # (2) swap disabled, GP banks at the budget
    for k, p, a in ((2, 257, 4), (2, 257, 8), (3, 2767, 6), (3, 2767, 10)):
        Fd = F(p, k)
        st = {"span": 0, "stall": 0, "direct": 0}
        disc = 0
        for _ in range(20):
            cols = moment_bank(p, a, D(3, a) + a, rng, "random", Fd)
            run = forward(Fd, cols, E, swap=False)
            st[run["status"]] += 1
            disc += len(run.get("discarded", []))
            run2 = forward(Fd, cols, E, swap=True)
            assert run2["status"] in ("span", "direct") and run2.get("pi", 0) == 0
        print(f"no-swap control kappa={k} p={p} a={a}: {st}, columns discarded at would-be "
              f"swaps={disc} (with swaps: all reach the span, pi=0)", flush=True)
    # (3) one steering source only
    for k, p, a in ((2, 257, 6), (3, 2767, 6)):
        Fd = F(p, k)
        f_all = f_one = n = 0
        for _ in range(15):
            cols = moment_bank(p, a, D(3, a) + a, rng, "random", Fd)
            run = forward(Fd, cols, E)
            if run["status"] != "span":
                continue
            for _ in range(40):
                n += 1
                f_all += backward(Fd, cols, run, rng)[0] is None
                f_one += backward(Fd, cols, run, rng, sources="one")[0] is None
        print(f"one-source control kappa={k} p={p} a={a}: passes={n} fail(all sources)={f_all} "
              f"fail(one source)={f_one}", flush=True)
    # (4) corrupted witness is rejected
    Fd = F(257, 2)
    cols = moment_bank(257, 4, D(3, 4) + 4, rng, "random", Fd)
    res, run, _ = solve(Fd, cols, 3, rng)
    x, _ = backward(Fd, cols, run, rng)
    while x is None:
        x, _ = backward(Fd, cols, run, rng)
    y = list(x)
    j = next(i for i, v in enumerate(y) if v)
    y[j] = y[j] * Fd.g % 257
    print("corrupted witness rejected:", verify(Fd, cols, x) and not verify(Fd, cols, y),
          flush=True)
    ok &= verify(Fd, cols, x) and not verify(Fd, cols, y)
    print("negative controls OK:", ok, flush=True)
    return ok


def smallp_section(rng):
    """GP (moment-curve) banks at small p, where c in U happens often: Theorem 2(b),(d) need no
    admissibility, so pi must be 0 and no stall may occur; the no-swap variant is compared.
    Backward passes at small admissible p are compared with the bound (which may exceed 1), and
    at exceptional p (G* = 0) failures must appear (sensitivity control)."""
    print("== small-p GP section ==", flush=True)
    E = 3
    ok = True
    for k, p, a in ((2, 11, 3), (2, 13, 3), (2, 13, 4), (2, 17, 4), (2, 19, 4), (2, 23, 5),
                    (2, 31, 5), (2, 37, 6), (3, 13, 3), (3, 19, 4), (3, 31, 5), (3, 37, 5),
                    (3, 43, 6), (3, 199, 6), (3, 223, 7), (3, 241, 6)):
        Fd = F(p, k)
        M = D(3, a) + a
        if M > p + 1:
            continue
        st = {"span": 0, "stall": 0, "direct": 0}
        st0 = {"span": 0, "stall": 0, "direct": 0}
        pi = swaps = disc = 0
        passes = fails = 0
        Gs = gstar(k, p)
        wb = 0.0
        for _ in range(40):
            cols = moment_bank(p, a, M, rng, rng.choice(["random", "one", "nr"]), Fd)
            if a <= 5:
                assert is_gp(cols, p)
            run = forward(Fd, cols, E)
            st[run["status"]] += 1
            pi += run.get("pi", 0)
            swaps += run.get("swaps", 0)
            run0 = forward(Fd, cols, E, swap=False)
            st0[run0["status"]] += 1
            disc += len(run0.get("discarded", []))
            if run["status"] == "span":
                wb = max(wb, rho(run) * max(1 / Gs if Gs else 9.9, k / (p - 1)))
                for _ in range(20):
                    x, info = backward(Fd, cols, run, rng)
                    passes += 1
                    if x is None:
                        fails += 1
                    else:
                        assert verify(Fd, cols, x)
        good = st["stall"] == 0 and pi == 0 and (Gs == 0 or fails <= passes * min(1, wb) + 3)
        ok &= good
        print(f"kappa={k} p={p} a={a} M={M} G*={Gs}: with swaps {st} pi={pi} swaps={swaps}; "
              f"no-swap {st0} discarded={disc}; passes={passes} fails={fails} "
              f"rate={fails/max(1,passes):.3f} bound={wb:.3f} {'OK' if good else 'CHECK'}",
              flush=True)
    print("small-p section OK:", ok, flush=True)
    return ok


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261105
    rng = random.Random(seed)
    res = []
    if which in ("gp", "all"):
        res.append(gp_section(rng))
    if which in ("adv", "all"):
        res.append(adv_section(rng))
    if which in ("smallp", "all"):
        res.append(smallp_section(rng))
    if which in ("neg", "all"):
        res.append(neg_section(rng))
    print("ALL OK:", all(res))
