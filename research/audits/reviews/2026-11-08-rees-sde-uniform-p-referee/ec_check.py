"""Referee check of the EC family (kappa = 2, J = 3), independent of lookahead.py / ec_test.py.

(1) Build an EC bank with my own code (same recipe: generic basis B first, then L exact circuits
    u1, u2, w = c1 u1 + c2 u2 inside Pi_l, non-monochromatic relation, then random padding).
(2) Run the UNMODIFIED ALG-T forward pass (subquad.py of the Theorem A folder) and check Lemma E2:
    L rounds, each e_l = 0, 3 singleton blocks, S_l = circuit l, Src = B = first r columns,
    reached V before any padding column.
(3) Build the flag directly (no ALG-T) and enumerate t in P^r exactly:
      succ(t) : every level has Good_l(beta_l(t)) != empty          (true pass success, s irrelevant)
      nz(t)   : C t nowhere zero (no cross-class coincidence at any level)
    Report both fractions.  Lemma E3 claims they are the same problem ("exactly"); the referee
    expects nz < succ strictly, since a cross-class coincidence forces s = -beta_b and the third
    block then reads z, which lies in the right coset about half the time.
(4) Several random instances: the exact success probability is instance dependent.

Usage: ec_check.py p Lmax instances seed
"""
import itertools
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A"))
import subquad as SQ  # noqa  (unmodified Theorem A code)
from sss import rank, solve_in_span  # noqa

p, Lmax, inst, seed = map(int, sys.argv[1:5])
k, J = 2, 3
rng = random.Random(seed)
Fd = SQ.Field(p, k)
Par = SQ.Params(J, k)
P = Fd.P
Q0 = [set([0]) | {y for y in range(1, p) if Fd.cls(y) == c} for c in range(k)]


def rand_inv(r):
    while True:
        A = [[rng.randrange(p) for _ in range(r)] for _ in range(r)]
        if rank(A, p)[0] == r:
            return A


def ec_bank(L, M):
    r = 2 * L
    A, B = rand_inv(r), rand_inv(r)
    cols = [list(v) for v in B]
    circuits = []
    for l in range(L):
        u1, u2 = A[2 * l], A[2 * l + 1]
        while True:
            c1, c2 = rng.randrange(1, p), rng.randrange(1, p)
            # relation w - c1 u1 - c2 u2 = 0: delta = (-c1, -c2, 1); non-monochromatic
            if len({Fd.cls((-c1) % p), Fd.cls((-c2) % p), 0}) > 1:
                break
        w = [(c1 * u1[t] + c2 * u2[t]) % p for t in range(r)]
        circuits.append((u1, u2, w, c1, c2))
        cols += [list(u1), list(u2), w]
    while len(cols) < M:
        cols.append([rng.randrange(p) for _ in range(r)])
    return cols, circuits


def good_nonempty(beta, bclass):
    return any(all((beta[b] + s) % p in Q0[(-bclass[b]) % k] for b in range(len(beta))) for s in range(p))


for L in range(2, Lmax + 1):
    r = 2 * L
    M = Par.F(r)
    for it in range(inst):
        cols, circuits = ec_bank(L, M)
        # ---- (2) ALG-T forward pass, unmodified code
        st = SQ.init_state(Fd, cols)
        assert st["B"] == list(range(r)), "B is not the first r columns"
        status = SQ.forward_fast(Fd, cols, J, rng, st, rule="first")
        assert status == "ok", status
        rounds = st["rounds"]
        e2 = (len(rounds) == L and all(not any(R.e) for R in rounds)
              and all(len(R.blocks) == 3 and all(len(G) == 1 for G in R.blocks) for R in rounds)
              and all(sorted(R.S) == [r + 3 * l, r + 3 * l + 1, r + 3 * l + 2] for l, R in enumerate(rounds))
              and max(i for R in rounds for i in R.S) < r + 3 * L)
        # ---- (3) direct flag: blocks (u1, u2, w) with delta = (-c1, -c2, 1); block 0 = first block of
        # the sorted support as ALG-T does (sorted classes; singleton blocks).  Use ALG-T's own block
        # order so that the comparison of Good sets is like for like, but compute everything else here.
        Ub = []
        rinfo = []
        for R in rounds:
            # W_b = delta_i lambda_i for singleton blocks
            Ws = [[R.delta[G[0]] * cols[G[0]][t] % p for t in range(r)] for G in R.blocks]
            start = len(Ub)
            Ub += Ws[1:]
            rinfo.append((start, len(Ub), R.bclass, Ws))
        assert len(Ub) == r and rank(Ub, p)[0] == r
        Cs = [solve_in_span(Ub, cols[s], p) for s in range(r)]          # source coordinates
        Cmat = np.array(Cs, dtype=np.int64)                                # r x r : coordinates of sources
        # Good tables per level over offsets (beta_1, beta_2)
        tabs = []
        for (start, end, bclass, Ws) in rinfo:
            tab = np.zeros((p, p), dtype=bool)
            for b1 in range(p):
                for b2 in range(p):
                    tab[b1, b2] = good_nonempty([0, b1, b2], bclass)
            tabs.append(tab)
        # cross pairs and their functionals; nowhere-zero check
        Pv = np.array(P, dtype=np.int64)
        tot = ok = nz = 0
        for T in itertools.product(range(len(P)), repeat=r):
            tv = Pv[list(T)]
            tau = (-(tv @ Cmat)) % p                     # coordinates of tau_L in the W basis
            good = True
            nzero = True
            for (start, end, bclass, Ws), tab in zip(rinfo, tabs):
                b1, b2 = int(tau[start]), int(tau[start + 1])
                beta = [0, b1, b2]
                good &= bool(tab[b1, b2])
                for x in range(3):
                    for y in range(x + 1, 3):
                        if bclass[x] != bclass[y] and beta[x] == beta[y]:
                            nzero = False
            tot += 1
            ok += good
            nz += nzero
        print("p=%d L=%d r=%d M=%d inst=%d | Lemma E2 leaf structure: %s | exact success %.4f  "
              "nowhere-zero(Ct) %.4f  (over |P|^r = %d)" % (p, L, r, M, it, e2, ok / tot, nz / tot, tot),
              flush=True)
