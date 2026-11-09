"""Runs of the block-refined triangular solver (brt.py) on random and adversarial columns.

  python brt_tests.py random        random columns, many (p, kappa, a, E), budget M_E(a)
  python brt_tests.py brute         small cases: compare with exhaustive kernel search
  python brt_tests.py adversarial   structured inputs (below CW, exact round dependencies
                                    with a planted top column, repeated columns, low rank)
Every returned x is checked: x != 0, x in Sq^M, sum x_i lambda_i = 0 (assert in brt.solve).
"""
import itertools
import random
import sys
import time

from common import F, kernel, check_witness
import brt


def rand_cols(rng, p, a, M):
    return [[rng.randrange(p) for _ in range(a)] for _ in range(M)]


def kernel_solvable(Fd, cols):
    """Exhaustive: does a nonzero x in Sq^M with sum x_i cols_i = 0 exist?"""
    p = Fd.p
    a = len(cols[0])
    K = kernel(cols, p)
    r = len(K)
    M = len(cols)
    for coef in itertools.product(range(p), repeat=r):
        if not any(coef):
            continue
        # projective normalisation: first nonzero coef = 1
        if next(c for c in coef if c) != 1:
            continue
        x = [sum(c * z[i] for c, z in zip(coef, K)) % p for i in range(M)]
        for lam in Fd.P[:1] + [Fd.rep(c) for c in range(1, Fd.k)]:
            y = [(lam * v) % p for v in x]
            if all(Fd.in_sq(v) for v in y):
                return True
    return False


def run_random():
    rng = random.Random(20261105)
    cases = []
    for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3), (65537, 2)]:
        for a in (3, 6, 10, 14):
            for E in (2, 3, 4, 5):
                cases.append((p, k, a, E))
    tot = 0
    for (p, k, a, E) in cases:
        Fd = F(p, k)
        M = brt.arity(a, E)
        st = {}
        t0 = time.time()
        trials = 12 if a <= 10 else 6
        nd_fail = 0
        for _ in range(trials):
            cols = rand_cols(rng, p, a, M)
            x, info = brt.solve(Fd, cols, E, rng)
            if x is not None:
                assert check_witness(Fd, cols, x)
            st[info["status"]] = st.get(info["status"], 0) + 1
            tot += 1
        print(f"random p={p} kappa={k} a={a} E={E} M={M} tri={(a+1)*(a+2)//2} "
              f"results={st} time={time.time()-t0:.1f}s", flush=True)
    print("total runs:", tot)


def run_brute():
    rng = random.Random(7)
    agree = disagree = 0
    for (p, k, a, E, n) in [(13, 2, 2, 3, 40), (29, 2, 2, 3, 40), (13, 2, 3, 3, 25), (29, 2, 3, 3, 10),
                            (37, 2, 3, 4, 15), (13, 3, 2, 3, 40), (31, 3, 2, 3, 40), (37, 3, 3, 3, 10),
                            (61, 3, 2, 3, 30), (13, 2, 4, 3, 6)]:
        Fd = F(p, k)
        M = brt.arity(a, E)
        st = {}
        for _ in range(n):
            cols = rand_cols(rng, p, a, M)
            x, info = brt.solve(Fd, cols, E, rng, restarts=30)
            if x is not None:
                assert check_witness(Fd, cols, x)
            sol = kernel_solvable(Fd, cols)
            key = (info["status"], sol)
            st[key] = st.get(key, 0) + 1
            if x is not None and not sol:
                disagree += 1  # impossible: x is a checked witness
            else:
                agree += 1
        print(f"brute p={p} kappa={k} a={a} E={E} M={M} (status, solvable)->count {st}", flush=True)
    print("witness-vs-exhaustive contradictions:", disagree)


def planted_top(Fd, a, E, rng, deterministic_cols=None):
    """Columns where every round after the first is exactly linearly dependent
    (so e_l = 0 and no round steers) and the top column is planted so that the
    level-1 residual has a cross-class coincidence whose forced s fails.
    Uses the deterministic split rule ("first"), which the adversary can predict."""
    p, k = Fd.p, Fd.k
    for attempt in range(200):
        cols = []
        q = a
        # round 1: a+1 random columns (always e_1 = 0)
        sizes = []
        while q >= 1:
            sizes.append(q + 1)
            q -= min(E - 1, q)
        for j, sz in enumerate(sizes):
            if j == 0:
                cols += [[rng.randrange(p) for _ in range(a)] for _ in range(sz)]
            else:
                base = [[rng.randrange(p) for _ in range(a)] for _ in range(sz - 1)]
                coef = [rng.randrange(1, p) for _ in range(sz - 1)]
                last = [sum(c * b[t] for c, b in zip(coef, base)) % p for t in range(a)]
                cols += base + [last]
        cols.append([0] * a)  # placeholder top
        r2 = random.Random(1)
        rounds, basis, top, used, status = brt.forward(Fd, cols, E, r2, split="first")
        if status != "ok":
            continue
        R = [R for R in rounds if R.kind == "level"][0]
        # plant beta with a cross-class coincidence: blocks 0 and the first block of
        # another class get offset 0, the rest get offsets chosen to violate the forced s
        cross = next(b for b in range(len(R.blocks)) if R.bclass[b] != R.bclass[0])
        beta = [0] * len(R.blocks)
        others = [b for b in range(len(R.blocks)) if b not in (0, cross)]
        if not others:
            continue
        for b in others:
            # forced s = 0: need beta_b in Q_{-c_b}; choose the wrong class
            wrong = (-(R.bclass[b]) + 1) % k
            beta[b] = Fd.rep(wrong)
        v = [sum(beta[b] * R.W[b][t] for b in range(len(R.blocks))) % p for t in range(a)]
        cols[-1] = [(-x) % p for x in v]   # top value y*lambda_top, tau = -y lambda_top = y v
        return cols
    return None


def run_adversarial():
    rng = random.Random(99)
    # (1) below Chevalley-Warning: a = 2, M = M_3(2) = 4, unsolvable instance
    for (p, k) in [(1009, 2), (1009, 3)]:
        Fd = F(p, k)
        g = Fd.rep(1)
        cols = [[1, 0], [g, 0], [0, 1], [0, g]] if k == 2 else [[1, 0], [g, 0], [0, 1], [0, g]]
        x, info = brt.solve(Fd, cols, 3, rng)
        print(f"adv below-CW p={p} kappa={k} M=4: solver={info['status']} exhaustive solvable="
              f"{kernel_solvable(F(13, k), [[1,0],[F(13,k).rep(1),0],[0,1],[0,F(13,k).rep(1)]])} (checked at p=13)")
    # (2) planted top column with non-steering rounds, deterministic split
    for (p, k, a, E) in [(1009, 2, 6, 3), (1009, 2, 8, 3), (1009, 3, 6, 3), (10007, 2, 10, 4)]:
        Fd = F(p, k)
        nfail = nok = 0
        ndf = 0
        rs = {}
        for _ in range(6):
            cols = planted_top(Fd, a, E, rng)
            if cols is None:
                continue
            r2 = random.Random(1)
            rounds, basis, top, used, status = brt.forward(Fd, cols, E, r2, split="first")
            nd = brt.nd_report(Fd, cols, rounds, basis, top)
            ndf += bool(nd)
            # solve with the same deterministic split
            x, info = brt.solve(Fd, cols, E, random.Random(5), split="first")
            if x is None:
                nfail += 1
            else:
                nok += 1
            x2, info2 = brt.solve(Fd, cols, E, random.Random(6), split="random")
            if x2 is not None:
                assert check_witness(Fd, cols, x2)
            rs[info2["status"]] = rs.get(info2["status"], 0) + 1
        print(f"adv planted-top p={p} kappa={k} a={a} E={E} M={brt.arity(a,E)}: ND' fails in {ndf}/6, "
              f"deterministic-split solver failed {nfail}, succeeded {nok}; random-split solver {rs}",
              flush=True)
    # (3) repeated columns and columns from a low-dimensional subspace
    for (p, k, a, E) in [(1009, 2, 6, 3), (1009, 3, 6, 3)]:
        Fd = F(p, k)
        M = brt.arity(a, E)
        st = {}
        for _ in range(10):
            base = rand_cols(rng, p, a, 3)
            cols = [list(base[rng.randrange(3)]) for _ in range(M)]
            x, info = brt.solve(Fd, cols, E, rng)
            assert x is None or check_witness(Fd, cols, x)
            st["rep:" + info["status"]] = st.get("rep:" + info["status"], 0) + 1
            B = rand_cols(rng, p, a, a - 2)
            cols = []
            for _ in range(M):
                c = [rng.randrange(p) for _ in B]
                cols.append([sum(ci * b[t] for ci, b in zip(c, B)) % p for t in range(a)])
            x, info = brt.solve(Fd, cols, E, rng)
            assert x is None or check_witness(Fd, cols, x)
            st["lowrank:" + info["status"]] = st.get("lowrank:" + info["status"], 0) + 1
        print(f"adv structured p={p} kappa={k} a={a} E={E} M={M}: {st}", flush=True)


if __name__ == "__main__":
    {"random": run_random, "brute": run_brute, "adversarial": run_adversarial}[sys.argv[1]]()
