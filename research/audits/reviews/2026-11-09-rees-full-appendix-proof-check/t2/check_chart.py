"""t2 check 1: module primitives and Lemma tb-chart (appendix-torsion-blackbox.tex 884-1049).

Part A. Howell construction (with random lifts), membership (P2), kernel (P3), Smith (P4)
        against brute force on random submodules of (Z/p^e)^k.
Part B. Lemma tb-chart end to end: L = F_{s,c}(Z/p^e)/I for random ideals I (ground truth by
        an integer lattice), Y = k exact uniform samples of I^perp (the exact-QFT law),
        Steps 3-5, and the chart checked against F/I: sum e_i = n, p^{e_i} lift in I, the
        structure constants agree modulo I, the lifts generate F/I.
Part C. The C_9 x C_3 example of Step 3 and the mod-p column scan, over random ideals.
Part D. Failure branches (rows of Y generating a proper subgroup of I^perp, as on the
        failure event with exact transforms, or arbitrary rows, as approximate transforms
        allow): how often do the computed constants pass the Lie-ring check stated after
        lem:tb-howell-rounds, and does a passing chart ever have class > c?
Finite checks only.
"""
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zmod import (Ring, howell, member, left_kernel, smith, matmul, eye, span_bf,  # noqa
                  ZLattice, dual_generators, FreeLieZ)

rng = random.Random(20261109)
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ============================================================================ Part A
def check_hf(R, rows, k):
    """(HF1), (HF2) by brute force."""
    p, e = R.p, R.e
    js = [j for (j, a, r) in rows]
    assert js == sorted(js) and len(set(js)) == len(js)
    for (j, a, r) in rows:
        assert all(x == 0 for x in r[:j]) and r[j] == p ** a and 0 <= a < e
    for t, (j, a, r) in enumerate(rows):
        later = span_bf(R, [rr for (_, _, rr) in rows[t + 1:]], k)
        assert tuple(x * p ** (e - a) % R.M for x in r) in later


def part_a():
    log("== Part A: Howell / membership / kernel / Smith vs brute force")
    n_tests = 0
    for (p, e, k) in [(2, 3, 3), (3, 2, 3), (3, 2, 4), (3, 3, 3), (5, 2, 3), (7, 2, 2), (2, 4, 3)]:
        R = Ring(p, e)
        M = R.M
        for trial in range(60):
            q0 = rng.randrange(0, 5)
            gens = []
            for _ in range(q0):
                # random vectors with structured valuations
                gens.append([rng.randrange(M) * (p ** rng.randrange(e)) % M for _ in range(k)])
            S = span_bf(R, gens, k)
            for lifts in (None, rng):
                rows, maxrem = howell(R, gens, k, rng=lifts)
                assert maxrem <= max(q0, 0), (maxrem, q0)  # (P1) remaining set never exceeds q0
                assert len(rows) <= k
                check_hf(R, rows, k)
                assert span_bf(R, [r for (_, _, r) in rows], k) == S
                # membership on all vectors if small, else random
                allv = list(S) + [tuple(rng.randrange(M) for _ in range(k)) for _ in range(40)]
                for v in allv:
                    lam = member(R, rows, v)
                    assert (lam is not None) == (tuple(x % M for x in v) in S)
                    if lam is not None:
                        w = [sum(l * r[i] for l, (_, _, r) in zip(lam, rows)) % M for i in range(k)]
                        assert w == [x % M for x in v]
            # (P3) left kernel
            if q0:
                Lam = left_kernel(R, gens, k)
                bf = set()
                for lam in __import__("itertools").product(range(M), repeat=q0):
                    if all(sum(l * g[i] for l, g in zip(lam, gens)) % M == 0 for i in range(k)):
                        bf.add(lam)
                assert span_bf(R, Lam, q0) == bf
            # (P4) Smith
            if q0:
                P, Q, Qi, exps, D = smith(R, gens)
                D2 = matmul(matmul(P, gens, M), Q, M)
                assert D2 == D
                for i in range(len(D)):
                    for j in range(len(D[0])):
                        if i != j:
                            assert D[i][j] == 0
                for t in range(min(len(D), len(D[0]))):
                    assert D[t][t] == (p ** exps[t] % M)
                assert matmul(Q, Qi, M) == eye(k)
                # row span of C times Q = (+) p^{a_t} e_t
                RS = span_bf(R, gens, k)
                RSQ = {tuple(sum(v[i] * Q[i][j] for i in range(k)) % M for j in range(k)) for v in RS}
                target = span_bf(R, [[(p ** exps[t] if i == t else 0) % M for i in range(k)]
                                     for t in range(k)], k)
                assert RSQ == target
            n_tests += 1
    # the (3 | 1) example over Z/9
    R = Ring(3, 2)
    Lam = left_kernel(R, [[3]], 1)
    assert span_bf(R, Lam, 1) == {(0,), (3,), (6,)}
    log("  Part A passed:", n_tests, "random modules; (3|1) over Z/9 gives Lambda = 3Z/9")


# ============================================================================ Part B
def random_ideal(FL, R, ngens):
    d, M, p, e = FL.d, R.M, R.p, R.e
    L = ZLattice(d, M)
    gens = []
    for _ in range(ngens):
        v = [0] * d
        # sparse random generator with random valuations
        for j in rng.sample(range(d), rng.randrange(1, min(d, 3) + 1)):
            v[j] = rng.randrange(1, M) * p ** rng.randrange(e) % M
        gens.append(v)
        L.insert(v)
    # close under bracket with the basis (ideal)
    while True:
        before = L.index()
        for g in list(L.basis()):
            for j in range(d):
                w = [1 if i == j else 0 for i in range(d)]
                L.insert(FL.bracket(g, w, M))
        if L.index() == before:
            break
    return L


def sample_perp(Ncols, R, d, t):
    M = R.M
    out = []
    for _ in range(t):
        y = [rng.randrange(M) for _ in range(d)]
        out.append([sum(Ncols[j][i] * y[j] for j in range(d)) % M for i in range(d)])
    return out


def span_order(rows_list, d, M):
    """|span of rows in (Z/M)^d| via the integer lattice (ground truth)."""
    L = ZLattice(d, M)
    for r in rows_list:
        L.insert(r)
    return M ** d // L.index()


def chart(R, FL, Y, mode="howell"):
    """Steps 3-5 of the proof of lem:tb-chart.  Y: k x d."""
    p, e, M = R.p, R.e, R.M
    k, d = len(Y), FL.d
    cols = [[Y[i][j] for i in range(k)] for j in range(d)]
    J, H = [], []
    if mode == "howell":
        for j in range(d):
            if member(R, H, cols[j]) is None:
                J.append(j)
                H, _ = howell(R, [cols[i] for i in J], k)
    else:  # the false variant: test the columns modulo p
        Rp = Ring(p, 1)
        Hp = []
        for j in range(d):
            if member(Rp, Hp, [x % p for x in cols[j]]) is None:
                J.append(j)
                Hp, _ = howell(Rp, [[x % p for x in cols[i]] for i in J], k)
    r = len(J)
    if r == 0:
        return dict(J=J, m=0, eps=[], lifts=[], exps=[], c={}, coords=lambda v: [])
    C = [[cols[J[b]][i] for b in range(r)] for i in range(k)]
    P, Q, Qi, avals, D = smith(R, C)
    I = [i for i in range(r) if avals[i] < e]
    CQ = matmul(C, Q, M)
    eps = [[CQ[x][i] for x in range(k)] for i in I]
    exps = [e - avals[i] for i in I]
    lifts = []
    for i in I:
        v = [0] * d
        for a in range(r):
            v[J[a]] = (v[J[a]] + Q[a][i]) % M
        lifts.append(v)
    # check Y lift = eps
    for v, ep in zip(lifts, eps):
        assert [sum(Y[x][j] * v[j] for j in range(d)) % M for x in range(k)] == ep

    def coords(v):
        Pv = [sum(P[x][y] * v[y] for y in range(k)) % M for x in range(k)]
        out = []
        for pos, i in enumerate(I):
            a = avals[i]
            assert Pv[i] % p ** a == 0
            out.append((Pv[i] // p ** a) % p ** exps[pos])
        return out

    # Step 5: z_ab = Y [w_ka, w_kb]
    z = {}
    for a in range(r):
        for b in range(r):
            wa = [1 if t == J[a] else 0 for t in range(d)]
            wb = [1 if t == J[b] else 0 for t in range(d)]
            br = FL.bracket(wa, wb, M)
            z[a, b] = [sum(Y[x][t] * br[t] for t in range(d)) % M for x in range(k)]
    # the two contractions of Step 5: u_ib = sum_a Q_ai z_ab, then sum_b Q_bj u_ib
    U = {}
    for ii, i in enumerate(I):
        for b in range(r):
            vec = [0] * k
            for a in range(r):
                co = Q[a][i]
                if co:
                    vec = [(x + co * y) % M for x, y in zip(vec, z[a, b])]
            U[ii, b] = vec
    cst = {}
    for ii in range(len(I)):
        for jj, j in enumerate(I):
            vec = [0] * k
            for b in range(r):
                co = Q[b][j]
                if co:
                    vec = [(x + co * y) % M for x, y in zip(vec, U[ii, b])]
            cst[ii, jj] = coords(vec)
    return dict(J=J, m=len(I), eps=eps, lifts=lifts, exps=exps, c=cst, coords=coords)


def lie_check(R, exps, cst):
    """The check stated after lem:tb-howell-rounds."""
    p, M = R.p, R.M
    m = len(exps)
    for i in range(m):
        if any(cst[i, i]):
            return False
        for j in range(m):
            for kk in range(m):
                if (cst[i, j][kk] + cst[j, i][kk]) % p ** exps[kk]:
                    return False
                if (p ** exps[i] * cst[i, j][kk]) % p ** exps[kk]:
                    return False

    def br(x, y):
        out = [0] * m
        for i in range(m):
            if x[i]:
                for j in range(m):
                    if y[j]:
                        for kk in range(m):
                            out[kk] += x[i] * y[j] * cst[i, j][kk]
        return [out[kk] % p ** exps[kk] for kk in range(m)]

    E = [[1 if t == i else 0 for t in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            for kk in range(m):
                s = [0] * m
                for (a, b, cc) in ((i, j, kk), (j, kk, i), (kk, i, j)):
                    t = br(br(E[a], E[b]), E[cc])
                    s = [x + y for x, y in zip(s, t)]
                if any(s[t] % p ** exps[t] for t in range(m)):
                    return False
    return br


def chart_class(R, exps, br, cbound):
    """Is gamma_{cbound+1} of the chart zero?  Additive spans computed in psi-coordinates."""
    p, e = R.p, max(exps) if exps else 1
    m = len(exps)
    if m == 0:
        return True
    Re = Ring(p, e)

    def psi(t):
        return [t[i] * p ** (e - exps[i]) % Re.M for i in range(m)]

    def psinv(v):
        return [(v[i] // p ** (e - exps[i])) % p ** exps[i] for i in range(m)]

    E = [[1 if t == i else 0 for t in range(m)] for i in range(m)]
    gam = [psi(x) for x in E]  # gamma_1 generators
    for _ in range(cbound):
        rows, _ = howell(Re, gam, m)
        gens = [psinv(r) for (_, _, r) in rows]
        gam = [psi(br(g, x)) for g in gens for x in E]
        gam = [g for g in gam if any(g)]
        if not gam:
            return True
    return not gam


def verify_chart(R, FL, I_lat, n, ch):
    p, M = R.p, R.M
    d = FL.d
    exps, lifts, cst = ch["exps"], ch["lifts"], ch["c"]
    ok = sum(exps) == n
    for i, v in enumerate(lifts):
        ok &= I_lat.contains([x * p ** exps[i] for x in v])
    for i in range(len(lifts)):
        for j in range(len(lifts)):
            br = FL.bracket(lifts[i], lifts[j], M)
            comb = [0] * d
            for kk, co in enumerate(cst[i, j]):
                comb = [x + co * y for x, y in zip(comb, lifts[kk])]
            ok &= I_lat.contains([(x - y) % M for x, y in zip(br, comb)])
    G = ZLattice(d, M)
    for b in I_lat.basis():
        G.insert(b)
    for v in lifts:
        G.insert(v)
    ok &= (G.index() == 1)
    return bool(ok)


def part_b():
    log("== Part B: Lemma tb-chart end to end on F_{s,c}(Z/p^e)/I, random ideals I")
    cases = [(3, 2, 2, 2), (3, 2, 3, 2), (3, 3, 2, 2), (5, 2, 2, 3), (5, 2, 2, 4), (5, 3, 2, 3),
             (7, 2, 3, 3), (5, 2, 1, 4), (3, 2, 4, 2)]
    tot = good = fails_pass = 0
    for (p, e, s, c) in cases:
        R = Ring(p, e)
        FL = FreeLieZ(s, c)
        d = FL.d
        for trial in range(25):
            I_lat = random_ideal(FL, R, rng.randrange(1, 4))
            idx = I_lat.index()  # = |F/I| = p^n
            n = 0
            while idx % p == 0:
                idx //= p
                n += 1
            assert idx == 1
            Ncols = dual_generators(I_lat)
            perp_order = span_order([[Ncols[j][i] for i in range(d)] for j in range(d)], d, R.M)
            assert perp_order == p ** n
            k = n + 3
            Y = sample_perp(Ncols, R, d, k)
            if span_order(Y, d, R.M) != p ** n:
                continue  # failure event of lem:tb-kernel; see Part D
            ch = chart(R, FL, Y)
            assert len(ch["J"]) <= n
            ok = verify_chart(R, FL, I_lat, n, ch)
            br = lie_check(R, ch["exps"], ch["c"])
            ok &= bool(br)
            if br:
                ok &= chart_class(R, ch["exps"], br, c)
            # coordinate map (c) on random elements of A
            for _ in range(5):
                u = [rng.randrange(R.M) for _ in range(d)]
                v = [sum(Y[x][j] * u[j] for j in range(d)) % R.M for x in range(k)]
                t = ch["coords"](v)
                w = [0] * k
                for ti, ep in zip(t, ch["eps"]):
                    w = [(a + ti * b) % R.M for a, b in zip(w, ep)]
                ok &= (w == v)
            tot += 1
            good += ok
            if not ok:
                log("  FAIL", (p, e, s, c), "n", n)
        log(f"  (p,e,s,c)={(p, e, s, c)} d={d}: cumulative {good}/{tot} charts verified")
    log("  Part B:", good, "of", tot, "charts verified against F/I")
    return good == tot


# ============================================================================ Part C
def part_c():
    log("== Part C: C_9 x C_3 (s=2, c=2, p=3, e=2) and the mod-p column scan")
    R = Ring(3, 2)
    FL = FreeLieZ(2, 2)  # basis x1, x2, [x1,x2]
    d = FL.d
    I_lat = ZLattice(d, 9)
    I_lat.insert([0, 3, 0])
    I_lat.insert([0, 0, 1])
    assert I_lat.index() == 27
    Ncols = dual_generators(I_lat)
    perp = span_bf(R, [[Ncols[j][i] for i in range(d)] for j in range(d)], d)
    assert all(v[1] % 3 == 0 and v[2] == 0 for v in perp) and len(perp) == 27
    howell_ok = modp_ok = runs = 0
    for _ in range(200):
        Y = sample_perp(Ncols, R, d, 6)
        if span_order(Y, d, 9) != 27:
            continue
        runs += 1
        ch = chart(R, FL, Y, "howell")
        howell_ok += verify_chart(R, FL, I_lat, 3, ch)
        chp = chart(R, FL, Y, "modp")
        gen = span_order([[Y[x][j] for x in range(6)] for j in chp["J"]], 6, 9)
        modp_ok += (gen == 27)
    log(f"  C9xC3: Howell scan correct in {howell_ok}/{runs}; mod-p scan spans A in {modp_ok}/{runs}")
    # random ideals: how often is the mod-p scan wrong?
    wrong = tot = 0
    for (p, e, s, c) in [(3, 2, 2, 2), (5, 2, 2, 3), (3, 3, 2, 2)]:
        R = Ring(p, e)
        FL = FreeLieZ(s, c)
        d = FL.d
        for _ in range(30):
            I_lat = random_ideal(FL, R, rng.randrange(1, 4))
            idx, n = I_lat.index(), 0
            while idx % p == 0:
                idx //= p
                n += 1
            Ncols = dual_generators(I_lat)
            Y = sample_perp(Ncols, R, d, n + 3)
            if span_order(Y, d, R.M) != p ** n:
                continue
            chp = chart(R, FL, Y, "modp")
            k = len(Y)
            gen = span_order([[Y[x][j] for x in range(k)] for j in chp["J"]], k, R.M) if chp["J"] else 1
            tot += 1
            wrong += (gen != p ** n)
    log(f"  random ideals: mod-p scan misses part of A in {wrong}/{tot} charts")
    return howell_ok == runs and modp_ok == 0


# ============================================================================ Part D
def part_d():
    log("== Part D: failure branches -- Lie check pass rate and class of passing charts")
    stats = {}
    for (p, e, s, c) in [(3, 2, 2, 2), (5, 2, 2, 3), (5, 2, 3, 2), (5, 3, 2, 3), (7, 2, 2, 4)]:
        R = Ring(p, e)
        FL = FreeLieZ(s, c)
        d = FL.d
        st = dict(exact_fail=0, exact_pass_lie=0, exact_ideal=0, exact_class_gt_c=0,
                  arb=0, arb_pass_lie=0, arb_class_gt_c=0)
        for trial in range(25):
            I_lat = random_ideal(FL, R, rng.randrange(1, 4))
            idx, n = I_lat.index(), 0
            while idx % p == 0:
                idx //= p
                n += 1
            Ncols = dual_generators(I_lat)
            # exact law, too few samples -> rows generate a proper subgroup of I^perp
            for kk in range(1, n + 1):
                Y = sample_perp(Ncols, R, d, kk)
                if span_order(Y, d, R.M) == p ** n:
                    continue
                st["exact_fail"] += 1
                ch = chart(R, FL, Y)
                # is ker Y an ideal?  ker Y = (row span of Y)^perp
                KY = ZLattice(d, R.M)
                for r in Y:
                    KY.insert(r)
                kcols = dual_generators(KY)
                isideal = all(
                    all(sum(Y[x][t] * b for t, b in enumerate(FL.bracket(
                        [kcols[j2][i] for i in range(d)], [1 if t2 == j else 0 for t2 in range(d)],
                        R.M))) % R.M == 0 for x in range(len(Y)))
                    for j2 in range(d) for j in range(d))
                st["exact_ideal"] += isideal
                br = lie_check(R, ch["exps"], ch["c"])
                if br:
                    st["exact_pass_lie"] += 1
                    if not chart_class(R, ch["exps"], br, c):
                        st["exact_class_gt_c"] += 1
            # arbitrary rows (approximate transforms can return any vector)
            for _ in range(3):
                kk = rng.randrange(1, n + 4)
                Y = [[rng.randrange(R.M) * p ** rng.randrange(e) % R.M for _ in range(d)] for _ in range(kk)]
                st["arb"] += 1
                ch = chart(R, FL, Y)
                br = lie_check(R, ch["exps"], ch["c"])
                if br:
                    st["arb_pass_lie"] += 1
                    if not chart_class(R, ch["exps"], br, c):
                        st["arb_class_gt_c"] += 1
        stats[(p, e, s, c)] = st
        log(f"  {(p, e, s, c)} d={d}: {st}")
    return stats


if __name__ == "__main__":
    t0 = time.time()
    part_a()
    okb = part_b()
    okc = part_c()
    part_d()
    log("RESULT", "B ok" if okb else "B FAIL", "C ok" if okc else "C FAIL",
        f"time {time.time() - t0:.1f}s")
    (Path(__file__).resolve().parent / "check_chart.out").write_text("\n".join(LOG) + "\n")
