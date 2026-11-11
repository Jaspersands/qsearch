"""Falsification tests for Lemma N' (2026-11-11-rees-sde-interval-s.md, section 1).

Test A (criterion): sample feasible (Phi, gamma) of the FREE problem (no Lemma R, no Lemma Q, no
nondegeneracy) for several S with F_p^* not inside S and random spanning label sets; for every
direction check: degenerate  <=>  gamma_{lam D} = lam gamma_D for all lam.
Test B (Lemma Q exact): for random P-closed spanning label sets, compare the verdict of the FREE
problem (no R, no Q, original nondegeneracy) with the P-equivariant problem (R + Q).
pycosat; models checked by int_cnf.check_solution (plain arithmetic).
"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import int_cnf as IC
import pycosat

def rand_labels(p, P, rng, size, closed):
    allv = [l for l in itertools.product(range(p), repeat=2) if any(l)]
    while True:
        L = set(rng.sample(allv, size))
        if closed:
            L = {tuple((nu * x) % p for x in l) for l in L for nu in P}
        L = sorted(L)
        # spanning
        if any((a[0] * b[1] - a[1] * b[0]) % p for a in L for b in L):
            return L

def test_A(p, S, rng, nsets, nmodels):
    P, _ = IC.stabiliser(p, S)
    nd = nl = viol = 0
    for _ in range(nsets):
        L = rand_labels(p, P, rng, rng.randint(3, 10), False)
        n, cl, meta = IC.build(p, S, 2, L, 'free', nondeg='none')
        for _ in range(nmodels):
            # random assumptions on a few gamma slots to diversify models
            extra = []
            for s in rng.sample(list(meta['Gv']), 2):
                extra.append([rng.choice(meta['Gv'][s])])
            if rng.random() < 0.7:
                # force gamma linear on a random line: gamma_{lam D} = lam g0 (g0 = 0 on a unit line)
                D0 = rng.choice(meta['dirs'])
                g0 = (0, 0) if D0 in ((1, 0), (0, 1)) else (rng.randrange(p), rng.randrange(p))
                for lam in range(1, p):
                    s = (D0, lam)
                    if s in meta['Gv']:
                        extra.append([meta['Gv'][s][meta['gvals'].index(((lam * g0[0]) % p, (lam * g0[1]) % p))]])
            sol = pycosat.solve(cl + extra)
            if sol == 'UNSAT':
                continue
            pos = {v for v in sol if v > 0}
            Phi, gamma = IC.decode(p, S, 2, L, 'free', meta, pos)
            for D in meta['dirs']:
                ys = []
                for lam in range(1, p):
                    a = ((lam * D[0]) % p, (lam * D[1]) % p)
                    g = gamma[a]
                    for l in L:
                        y = (a[0] * Phi[l][0] + a[1] * Phi[l][1] + g[0] * l[0] + g[1] * l[1]) % p
                        assert y in set(S)
                        ys.append(y)
                degen = not any(ys)
                gD = gamma[D]
                lin = all(gamma[((lam * D[0]) % p, (lam * D[1]) % p)] == ((lam * gD[0]) % p, (lam * gD[1]) % p) for lam in range(1, p))
                nd += degen; nl += lin; viol += degen != lin
    return nd, nl, viol

def test_B(p, S, rng, nsets):
    P, _ = IC.stabiliser(p, S)
    agree = dis = sat = 0
    for _ in range(nsets):
        L = rand_labels(p, P, rng, rng.randint(2, 8), True)
        r1, i1, s1 = IC.solve(p, S, 2, L, 'free', solver='pycosat')
        r2, i2, s2 = IC.solve(p, S, 2, L, 'equi', solver='pycosat')
        for r, i in ((r1, i1), (r2, i2)):
            if r == 'SAT': assert i['model_check'] == 'OK', i
        if r1 == r2: agree += 1
        else:
            dis += 1; print('  DISAGREE', p, S, L, r1, r2, flush=True)
        sat += r1 == 'SAT'
    return agree, dis, sat

rng = random.Random(20261111)
cases = [(7, [0, 1, 6]), (7, [0, 2, 5]), (7, [0, 3, 4]), (7, [0, 1, 2, 5, 6]), (7, [0, 1, 3, 4, 6]),
         (7, [0, 2, 3, 4, 5]), (7, [0, 1, 2, 4]), (7, [0, 1, 2]), (11, [0, 1, 2, 9, 10]), (11, [0, 1, 3, 8, 10]),
         (13, [0, 1, 2, 3, 10, 11, 12])]
ONLY_B11 = 'B11' in sys.argv   # rerun of test B at p = 11 only (the first run was stopped there to free solver slots)
for p, S in ([] if ONLY_B11 else cases):
    nA = 6 if p < 11 else 3
    nd, nl, viol = test_A(p, S, rng, nA, 4)
    print(f'A p={p} S={S}: degenerate directions {nd}, gamma-linear directions {nl}, violations {viol}', flush=True)
for p, S in ([c for c in cases[:10] if c[0] == 11] if ONLY_B11 else cases[:9]):
    nB = 25 if p == 7 else 6
    a, d, s = test_B(p, S, rng, nB)
    print(f'B p={p} S={S}: {a + d} P-closed label sets, free==equi on {a}, disagreements {d}, SAT {s}', flush=True)
