"""Binary-clause CNF for the d in {1,2} realization problem with the coset reduction (Lemma R)
and the P-scaling label reduction (Lemma Q):

  * phi(l) in S^d is ONE one-hot variable per label (|S|^d values);
  * gamma_{r_c alpha_D} in F_p^k is one one-hot per (direction D, coset c), p^k values
    (gamma = 0 for the unit directions at coset 0);
  * for every slot (D, c), label l, phi value and gamma value with
        r_c <alpha_D, phi> + <gamma, l>  not in S
    a binary clause forbids the pair;
  * labels are taken up to P-scaling (lambda l ~ l, phi ~ lambda phi);
  * weak nondegeneracy: for every direction D, some label l, coset c, with
        r_c <alpha_D, phi(l)> + <gamma_{D,c}, l> != 0.
Every model is expanded to all alpha and all labels and re-verified by gadget_cnf.verify.
CLI: p S k d L [--quiet] [--show]
"""
import sys, itertools, time, argparse
import pycosat
from gadget_sat import parse_S, parse_L
from gadget_cnf import CNF, verify
from gadget_cnf3 import cosets


def reduce_labels(p, P, L):
    """one representative per P-orbit of labels"""
    seen, reps = set(), []
    for l in L:
        if l in seen:
            continue
        reps.append(l)
        for lam in P:
            seen.add(tuple((lam * x) % p for x in l))
    return reps


def solve4(p, S, k, d, L, weak=True, verbose=False, fix=None):
    """fix: {(direction tuple, coset index): gamma tuple} forced values (case splits)"""
    S = sorted(S); Sset = set(S)
    P, creps = cosets(p, S)
    kappa = len(creps)
    # feasibility (with weak nondegeneracy) of L equals that of its P-closure (Lemma Q)
    Lclos = sorted({tuple((lam * x) % p for x in l) for l in L for lam in P})
    Lred = reduce_labels(p, P, Lclos)
    dirs = []
    for a in itertools.product(range(p), repeat=d):
        if any(a) and a[next(i for i, x in enumerate(a) if x)] == 1:
            dirs.append(a)
    unit = {tuple(1 if i == j else 0 for i in range(d)) for j in range(d)}
    phis = list(itertools.product(S, repeat=d))
    gvals = list(itertools.product(range(p), repeat=k))
    c = CNF()
    phi = {l: c.onehot(len(phis)) for l in Lred}
    slots = [(D, ci) for D in range(len(dirs)) for ci in range(kappa)]
    fixed = {(D, ci) for (D, ci) in slots if ci == 0 and dirs[D] in unit}
    g = {s: c.onehot(len(gvals)) for s in slots if s not in fixed}
    dir_nz = {D: [] for D in range(len(dirs))}
    for (D, ci) in slots:
        a = dirs[D]; r = creps[ci]
        for l in Lred:
            nz = c.var()
            dir_nz[D].append(nz)
            for pi, ph in enumerate(phis):
                base = (r * sum(a[j] * ph[j] for j in range(d))) % p
                if (D, ci) in fixed:
                    if base not in Sset:
                        c.clauses.append([-phi[l][pi]])
                    elif base == 0:
                        c.clauses.append([-nz, -phi[l][pi]])
                    continue
                for gi, gv in enumerate(gvals):
                    val = (base + sum(gv[i] * l[i] for i in range(k))) % p
                    if val not in Sset:
                        c.clauses.append([-phi[l][pi], -g[(D, ci)][gi]])
                    elif val == 0:
                        c.clauses.append([-nz, -phi[l][pi], -g[(D, ci)][gi]])
    for D, nzs in dir_nz.items():
        c.clauses.append(nzs)
    if fix:
        for (dvec, ci), gv in fix.items():
            D = dirs.index(tuple(dvec))
            c.clauses.append([g[(D, ci)][gvals.index(tuple(gv))]])
    if verbose:
        print(f'  P={P} coset reps={creps} |Lred|={len(Lred)}; cnf: {c.n} vars, {len(c.clauses)} clauses', flush=True)
    t0 = time.time()
    sol = pycosat.solve(c.clauses)
    dt = time.time() - t0
    if sol == 'UNSAT':
        return 'unsat', None, dt
    pos = set(v for v in sol if v > 0)
    Phi_red = {l: phis[[i for i, v in enumerate(phi[l]) if v in pos][0]] for l in Lred}
    grep = {}
    for (D, ci) in slots:
        a = tuple((creps[ci] * x) % p for x in dirs[D])
        grep[a] = (0,) * k if (D, ci) in fixed else gvals[[i for i, v in enumerate(g[(D, ci)]) if v in pos][0]]
    # expand gamma to all alpha and Phi to all labels
    gamma, Phi = {}, {}
    for a, gv in grep.items():
        for lam in P:
            gamma[tuple((lam * x) % p for x in a)] = tuple((lam * x) % p for x in gv)
    for l, ph in Phi_red.items():
        for lam in P:
            Phi[tuple((lam * x) % p for x in l)] = tuple((lam * x) % p for x in ph)
    assert len(gamma) == p ** d - 1 and set(Phi) == set(Lclos)
    Phi = {l: Phi[l] for l in L}
    ok, why = verify(p, S, k, d, L, Phi, gamma, nondeg=True, weak=weak)
    assert ok, why
    return 'sat', (Phi, gamma), dt


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('p', type=int); ap.add_argument('S'); ap.add_argument('k', type=int); ap.add_argument('d', type=int); ap.add_argument('L')
    ap.add_argument('--quiet', action='store_true'); ap.add_argument('--show', action='store_true')
    ap.add_argument('--fix', default='', help='D1,D2,c:x,y;...')
    A = ap.parse_args()
    fix = {}
    for item in filter(None, A.fix.split(';')):
        lhs, rhs = item.split(':')
        *dv, ci = [int(x) for x in lhs.split(',')]
        fix[(tuple(dv), ci)] = tuple(int(x) for x in rhs.split(','))
    S = parse_S(A.p, A.S); L = parse_L(A.p, A.k, A.L)
    r, sol, dt = solve4(A.p, S, A.k, A.d, L, verbose=not A.quiet, fix=fix)
    print(f'p={A.p} S={S} k={A.k} d={A.d} L={A.L} (|L|={len(L)}) [reduced, weak nondeg]{" fix=" + A.fix if A.fix else ""}: {r.upper()} [{dt:.1f}s]', flush=True)
    if sol and A.show:
        Phi, gamma = sol
        for l in sorted(Phi): print('  ', l, '->', Phi[l])
        for a in sorted(gamma): print('  ', a, '->', gamma[a])
