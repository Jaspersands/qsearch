"""Exact k-dependency / d = 2 feasibility with the coset reduction (Lemma R of the note):

If (Phi, gamma) is a realization then so is the one with gamma_{lambda alpha} := lambda gamma_alpha
for every lambda in P (the kappa-th powers), because lambda * y_alpha in lambda S = S.  So WLOG
gamma is determined by its values on one representative alpha per (projective direction, coset of
P), i.e. kappa (p^{k}... ) -- here d = 2: (p+1) directions x kappa cosets, minus the two unit
directions at coset 0 where gamma = 0.  Free gamma variables: kappa (p+1) - 2 instead of p^2 - 3.
Also valid for S = any set with P S = S (e.g. S = {-K..K} with P = {+-1}).

Variables (one-hot): Phi_j(l) in S (j = 1, 2);  gamma_rep in F_p^k (p^k values).
Clauses: for each representative alpha and label l, forbid (phi_1, phi_2, gamma) with
<alpha, phi> + <gamma, l> not in S.  Weak nondegeneracy per direction (some realizer != 0).
Every model is re-verified over ALL alpha by gadget_cnf.verify.

CLI: p S k L [--kappa K] [--strong] [--quiet]
"""
import sys, itertools, time, argparse
import pycosat
from gadget_sat import parse_S, parse_L
from gadget_cnf import CNF, verify


def cosets(p, S):
    """Stabiliser P = {lambda : lambda S = S} and its cosets in F_p^*; returns (P, reps)."""
    Sset = set(S)
    P = [l for l in range(1, p) if {(l * s) % p for s in S} == Sset]
    Pset = set(P)
    reps = []
    seen = set()
    for x in range(1, p):
        if x in seen:
            continue
        reps.append(x)
        seen |= {(x * l) % p for l in P}
    return P, reps


def solve3(p, S, k, L, weak=True, verbose=False):
    S = sorted(S)
    Sset = set(S)
    P, creps = cosets(p, S)
    kappa = len(creps)
    # projective directions of F_p^2 with representative having first nonzero coordinate 1
    dirs = [(1, t) for t in range(p)] + [(0, 1)]
    unit = {(1, 0), (0, 1)}
    gvals = list(itertools.product(range(p), repeat=k))
    c = CNF()
    phi = {(l, j): c.onehot(len(S)) for l in L for j in range(2)}
    g = {}
    reps = []
    for dvec in dirs:
        for s in creps:
            a = tuple((s * x) % p for x in dvec)
            reps.append((dvec, a))
            if a in unit:
                continue
            g[a] = c.onehot(len(gvals))
    dir_nz = {dv: [] for dv in dirs}
    for dvec, a in reps:
        for l in L:
            nz = c.var()
            dir_nz[dvec].append(nz)
            for i1, s1 in enumerate(S):
                for i2, s2 in enumerate(S):
                    base = (a[0] * s1 + a[1] * s2) % p
                    if a in unit:
                        if base not in Sset:
                            c.clauses.append([-phi[(l, 0)][i1], -phi[(l, 1)][i2]])
                        elif base == 0:
                            c.clauses.append([-nz, -phi[(l, 0)][i1], -phi[(l, 1)][i2]])
                        continue
                    for ig, gv in enumerate(gvals):
                        val = (base + sum(gv[i] * l[i] for i in range(k))) % p
                        if val not in Sset:
                            c.clauses.append([-phi[(l, 0)][i1], -phi[(l, 1)][i2], -g[a][ig]])
                        elif val == 0:
                            c.clauses.append([-nz, -phi[(l, 0)][i1], -phi[(l, 1)][i2], -g[a][ig]])
    for dv, nzs in dir_nz.items():
        c.clauses.append(nzs)
    if verbose:
        print(f'  P={P} coset reps={creps}; cnf: {c.n} vars, {len(c.clauses)} clauses', flush=True)
    t0 = time.time()
    sol = pycosat.solve(c.clauses)
    dt = time.time() - t0
    if sol == 'UNSAT':
        return 'unsat', None, dt
    pos = set(v for v in sol if v > 0)
    Phi = {l: tuple(S[[i for i, v in enumerate(phi[(l, j)]) if v in pos][0]] for j in range(2)) for l in L}
    grep = {a: (0,) * k if a in unit else gvals[[i for i, v in enumerate(g[a]) if v in pos][0]] for _, a in reps}
    # expand to all alpha: gamma_{lambda a} = lambda gamma_a for lambda in P
    gamma = {}
    for _, a in reps:
        for lam in P:
            la = tuple((lam * x) % p for x in a)
            gamma[la] = tuple((lam * x) % p for x in grep[a])
    assert len(gamma) == p * p - 1
    ok, why = verify(p, S, k, 2, L, Phi, gamma, nondeg=True, weak=weak)
    assert ok, why
    return 'sat', (Phi, gamma), dt


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('k', type=int); ap.add_argument('L')
    ap.add_argument('--quiet', action='store_true')
    A = ap.parse_args()
    S = parse_S(A.p, A.S); L = parse_L(A.p, A.k, A.L)
    r, sol, dt = solve3(A.p, S, A.k, L, verbose=not A.quiet)
    print(f'p={A.p} S={S} k={A.k} d=2 L={A.L} (|L|={len(L)}) [coset-reduced, weak nondeg]: {r.upper()} [{dt:.1f}s]', flush=True)
    if sol and not A.quiet:
        Phi, gamma = sol
        for l in L: print('  ', l, '->', Phi[l])
        for a in sorted(gamma): print('  ', a, '->', gamma[a])
