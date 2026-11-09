"""Direct ternary-clause CNF for k = 2 (no auxiliary adders): variables are one-hot Phi_j(l) in S
and one-hot gamma_alpha in F_p^2 (p^2 values).  Forbidden triples (phi_1, phi_2, gamma) per
(alpha, label) are excluded by 3-literal clauses.  Weak nondegeneracy per projective direction.
Models are re-verified by gadget_cnf.verify.  CLI: p S L [--strong]."""
import sys, itertools, time, argparse
import pycosat
from gadget_sat import parse_S, parse_L
from gadget_cnf import CNF, verify


def solve2(p, S, L, d=2, weak=True, nondeg=True, verbose=False):
    assert d == 2
    k = 2
    S = sorted(S)
    Sset = set(S)
    alphas = [a for a in itertools.product(range(p), repeat=2) if any(a)]
    unit = {(1, 0), (0, 1)}
    gvals = list(itertools.product(range(p), repeat=2))
    c = CNF()
    phi = {(l, j): c.onehot(len(S)) for l in L for j in range(2)}
    g = {a: c.onehot(len(gvals)) for a in alphas if a not in unit}
    dir_nz = {}
    for a in alphas:
        lead = next(x for x in a if x)
        key = tuple((x * pow(lead, -1, p)) % p for x in a)
        for l in L:
            nz = c.var()
            dir_nz.setdefault(key, []).append(nz)
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
                        val = (base + gv[0] * l[0] + gv[1] * l[1]) % p
                        if val not in Sset:
                            c.clauses.append([-phi[(l, 0)][i1], -phi[(l, 1)][i2], -g[a][ig]])
                        elif val == 0:
                            c.clauses.append([-nz, -phi[(l, 0)][i1], -phi[(l, 1)][i2], -g[a][ig]])
    if nondeg:
        if weak:
            for key, nzs in dir_nz.items():
                c.clauses.append(nzs)
        else:
            # strong: per alpha
            pass
    if verbose:
        print(f'  cnf: {c.n} vars, {len(c.clauses)} clauses', flush=True)
    t0 = time.time()
    sol = pycosat.solve(c.clauses)
    dt = time.time() - t0
    if sol == 'UNSAT':
        return 'unsat', None, dt
    pos = set(v for v in sol if v > 0)
    Phi = {l: tuple(S[[i for i, v in enumerate(phi[(l, j)]) if v in pos][0]] for j in range(2)) for l in L}
    gamma = {a: (0, 0) if a in unit else gvals[[i for i, v in enumerate(g[a]) if v in pos][0]] for a in alphas}
    ok, why = verify(p, S, 2, 2, L, Phi, gamma, nondeg=nondeg, weak=weak)
    assert ok, why
    return 'sat', (Phi, gamma), dt


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('L')
    ap.add_argument('--quiet', action='store_true')
    A = ap.parse_args()
    S = parse_S(A.p, A.S); L = parse_L(A.p, 2, A.L)
    r, sol, dt = solve2(A.p, S, L, verbose=not A.quiet)
    print(f'p={A.p} S={S} k=2 d=2 L={A.L} (|L|={len(L)}) weak-nondeg: {r.upper()} [{dt:.1f}s]', flush=True)
    if sol and not A.quiet:
        Phi, gamma = sol
        for l in L: print('  ', l, '->', Phi[l])
        for a, gg in gamma.items(): print('  ', a, '->', gg)
