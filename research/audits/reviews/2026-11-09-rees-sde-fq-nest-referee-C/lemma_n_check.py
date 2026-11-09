"""Referee C, Lemma N sanity check: for S = P u {0} (kappa >= 2) and L the nested set, in every
FEASIBLE (Phi, gamma) (no nondegeneracy imposed), a direction [alpha] is degenerate (all realizers
y_{lam alpha} vanish on L) iff gamma_{r alpha} = r gamma_alpha for a fixed r not in P.
Enumerates models of the free encoding (free_cnf.build) with the nondegeneracy clauses removed,
and with random extra unit clauses to diversify, and tests the equivalence on each model."""
import sys, os, random, itertools
import pycosat
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import free_cnf as F
from gadget_sat import parse_S, parse_L

def models(p, Sspec, k, Lspec, nmax, seed=1):
    S = sorted(parse_S(p, Sspec)); L = parse_L(p, k, Lspec)
    n, cl, M = F.build(p, S, k, L, True, None)
    ndirs = sum(1 for a in itertools.product(range(p), repeat=2) if any(a) and a[0 if a[0] else 1] == 1)
    base = cl[:-ndirs]          # drop the per-direction nondegeneracy clauses
    P, creps = F.stab(p, S); r = creps[1]
    rng = random.Random(seed)
    tested = degen = 0
    phivars = [v for l in L for v in M['phi'][l]]
    gvars = [v for s in M['g'] for v in M['g'][s]]
    for trial in range(nmax):
        extra = [[rng.choice(gvars)] for _ in range(rng.randint(0, 3))] + [[rng.choice(phivars)] for _ in range(rng.randint(0, 6))]
        sol = pycosat.solve(base + extra)
        if sol == 'UNSAT':
            continue
        pos = {v for v in sol if v > 0}
        Phi = {l: M['phis'][[i for i, v in enumerate(M['phi'][l]) if v in pos][0]] for l in L}
        gamma = {}
        for s in M['slots']:
            a = M['alpha'][s]
            val = (0,) * k if a in M['unit'] else M['gv'][[i for i, v in enumerate(M['g'][s]) if v in pos][0]]
            for lam in P:
                gamma[((lam * a[0]) % p, (lam * a[1]) % p)] = tuple((lam * x) % p for x in val)
        tested += 1
        for D in [a for a in itertools.product(range(p), repeat=2) if any(a) and a[0 if a[0] else 1] == 1]:
            zero = all((lam * D[0] * Phi[l][0] + lam * D[1] * Phi[l][1] +
                        sum(gamma[((lam * D[0]) % p, (lam * D[1]) % p)][i] * l[i] for i in range(k))) % p == 0
                       for lam in range(1, p) for l in L)
            rD = ((r * D[0]) % p, (r * D[1]) % p)
            crit = gamma[rD] == tuple((r * x) % p for x in gamma[D])
            assert zero == crit, (p, Sspec, D, zero, crit)
            degen += zero
    return tested, degen

for args in [(5, 'pow:2', 2, 'nest'), (5, 'pow:2', 2, 'all'), (7, 'pow:2', 2, 'nest'), (7, 'pow:3', 2, 'nest'), (11, 'pow:2', 2, 'nest')]:
    t, d = models(*args, nmax=int(sys.argv[1]) if len(sys.argv) > 1 else 200)
    print(f'{args}: {t} feasible models tested, {d} degenerate directions met, equivalence held on all', flush=True)
