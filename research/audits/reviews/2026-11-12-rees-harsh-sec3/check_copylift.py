"""State-level simulation of Lemma 3.3 (lifted source, oracle) and Lemma 3.6 (copy-only lift).

C1 (Lemma 3.6) Heisenberg over F_3 (|G|=27, |cover|=81, c=2) and over F_5 (|G|=125, |cover|=625):
   each input copy rho_H is a uniform mixture of normalised left-coset states |gH>; for every pair of
   cosets we simulate the pure state  |cover|^{-1/2} sum_a |a> (x) R_{E_1(a)}|g1 H> (x) R_{E_2(a)}|g2 H>,
   with R_g|x> = |x g^{-1}> computed by BCH, trace out both copies, average, and compare with
   rho_{exp(hlift)}  (entries |cover|^{-1} 1[a^{-1} b in hlift]).  Every subalgebra (F_3) / sampled (F_5).
C2 (Lemma 3.3) same groups: |cover|^{-1/2} sum_a |a>|f(E_1 a)>|f(E_2 a)>, labels traced out.
C3 negative controls: (i) one copy only (points {1}) gives a state != rho_{exp(hlift)} for H=1;
   (ii) leaving the evaluation workspace E_1(a) uncleaned (traced out) destroys coherence.
Also checks tr(rho_H R_g) = 1_H(g) numerically.
"""
import numpy as np, random, sys
from itertools import product
from lie import *

rng = random.Random(5)


def run(p, exhaustive):
    L = heisenberg(p)
    cov = Cover(L)
    Gp = Group(L)
    Gel = [list(t) for t in product(range(p), repeat=3)]
    gidx = {tuple(g): i for i, g in enumerate(Gel)}
    Ael = [cov.from_coords(list(t)) for t in product(range(p), repeat=cov.n)]
    nA, nG = len(Ael), len(Gel)
    pts = [1, 2]

    perm = {}
    for g in Gel:
        ginv = Gp.neg(g)
        perm[tuple(g)] = np.array([gidx[tuple(Gp.mul(x, ginv))] for x in Gel])

    def Rmat_apply(g, vec):
        # (R_g v)[x g^{-1}] = v[x]
        out = np.zeros_like(vec)
        out[perm[tuple(g)]] = vec
        return out

    # coordinates of a^{-1} * b for all pairs (independent of H)
    def coords(a):
        al = []
        for k in range(1, cov.c + 1):
            gk = L.gam(k)
            if gk:
                al += solve_in_basis(gk, a[k - 1], p)
        return al
    Q = np.array([[coords(cov.mul(cov.neg(a), b)) for b in Ael] for a in Ael])  # nA x nA x n

    def target_for(hl):
        N = np.array(annihilator(hl, cov.n, p) if hl else np.eye(cov.n, dtype=int), dtype=int)
        if N.size == 0:
            return np.ones((nA, nA)) / nA
        val = (Q @ N.T) % p
        return (np.all(val == 0, axis=2)).astype(float) / nA

    subs = [B for B in all_subspaces(3, p) if L.is_subalgebra(B)]
    if not exhaustive:
        subs = [[]] + rng.sample(subs, 6)
    worst = worst2 = 0.0
    trace_bad = 0
    for hh in subs:
        hl = cov.hlift_coords(hh)
        Helems = all_span(hh, p) if hh else [[0, 0, 0]]
        Hset = {tuple(h) for h in Helems}
        # cosets
        seen, cosets = set(), []
        for x in Gel:
            if tuple(x) in seen:
                continue
            C = [tuple(Gp.mul(x, h)) for h in Helems]
            seen.update(C)
            v = np.zeros(nG)
            for y in C:
                v[gidx[y]] = 1
            cosets.append(v / np.linalg.norm(v))
        # rho_H and the trace identity
        rhoH = sum(np.outer(v, v) for v in cosets) / len(cosets)
        for g in rng.sample(Gel, min(8, nG)):
            Rg = np.zeros((nG, nG))
            for i, x in enumerate(Gel):
                Rg[gidx[tuple(Gp.mul(x, Gp.neg(g)))], i] = 1
            if abs(np.trace(rhoH @ Rg) - (1.0 if tuple(g) in Hset else 0.0)) > 1e-9:
                trace_bad += 1
        # target
        target = target_for(hl)
        # C1: for each coset c, precompute R_{E_s(a)}|c> for all a: inner products
        Ea = [[cov.E(s, a) for a in Ael] for s in pts]
        rho = np.ones((nA, nA)) / nA
        for si, s in enumerate(pts):
            Gram = np.zeros((nA, nA))
            for v in cosets:
                W = np.array([Rmat_apply(Ea[si][i], v) for i in range(nA)])  # nA x nG
                Gram += W @ W.T
            Gram /= len(cosets)  # averaged over the coset mixture of this copy
            rho = rho * Gram     # copies are independent: entrywise product of their Gram factors
        worst = max(worst, np.abs(rho - target).max())
        # C2 oracle version
        f = CosetOracle(Gp, hh)
        labs = [tuple(f(Ea[si][i]) for si in range(len(pts))) for i in range(nA)]
        rho2 = np.array([[1.0 / nA if labs[i] == labs[j] else 0.0 for j in range(nA)] for i in range(nA)])
        worst2 = max(worst2, np.abs(rho2 - target).max())
    print("p=%d subalgebras=%d  C1 max|rho-target|=%.2e  C2 max|rho-target|=%.2e  trace identity failures=%d"
          % (p, len(subs), worst, worst2, trace_bad))
    # C3 negative controls for H = 1
    hl0 = cov.hlift_coords([])
    target0 = target_for(hl0)
    f0 = CosetOracle(Gp, [])
    lab1 = [f0(cov.E(1, a)) for a in Ael]
    one = np.array([[1.0 / nA if lab1[i] == lab1[j] else 0 for j in range(nA)] for i in range(nA)])
    # uncleaned workspace: labels of both points plus the workspace value E_1(a) itself kept and traced
    labs = [(f0(cov.E(1, a)), f0(cov.E(2, a)), tuple(cov.E(1, a))) for a in Ael]
    dirty = np.array([[1.0 / nA if labs[i] == labs[j] else 0 for j in range(nA)] for i in range(nA)])
    print("   C3 H=1: one point differs from target: %s ; uncleaned workspace with H=<x> differs:" % (np.abs(one - target0).max() > 1e-9), end=" ")
    hh = [[1, 0, 0]]
    hl = cov.hlift_coords(hh)
    fx = CosetOracle(Gp, hh)
    labs = [(fx(cov.E(1, a)), fx(cov.E(2, a)), tuple(cov.E(1, a))) for a in Ael]
    dirty = np.array([[1.0 / nA if labs[i] == labs[j] else 0 for j in range(nA)] for i in range(nA)])
    tgt = target_for(hl)
    print(np.abs(dirty - tgt).max() > 1e-9)
    sys.stdout.flush()
    return worst < 1e-9 and worst2 < 1e-9 and trace_bad == 0


if __name__ == "__main__":
    ok1 = run(3, True)
    ok2 = run(5, False)
    print("ALL OK:", ok1 and ok2)
