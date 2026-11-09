"""Referee B: is the Lemma Q label reduction (solve4/solve5: Phi consistent on P-classes of labels,
solved on one representative per class of the P-closure) COMPLETE, i.e. does it return SAT whenever
the unreduced problem (gadget_cnf.solve, weak nondegeneracy, no Lemma Q, no Lemma R) is SAT?
(1) p = 5: solve4 on every spanning GL_2-orbit representative (also = what WNEST_5 calls).
(2) p = 7, kappa = 2 and 3, k = d = 2: random label sets, both P-closed and arbitrary, compare.
Disagreements (unreduced SAT, reduced UNSAT) would show the reduction is incomplete, which matters
only for UNSAT verdicts.
"""
import sys, itertools, numpy as np, multiprocessing as mp, time
sys.path.insert(0, '../2026-11-08-rees-sde-fq-nest')
from gadget_cnf4 import solve4
from gadget_cnf import solve as solve_unred

def job5(mask):
    vecs = [v for v in itertools.product(range(5), repeat=2) if any(v)]
    L = [vecs[i] for i in range(24) if mask >> i & 1]
    r, sol, dt = solve4(5, [0, 1, 4], 2, 2, L, weak=True)
    return len(L), r

def job7(args):
    p, S, L = args
    r4 = solve4(p, S, 2, 2, L, weak=True)[0]
    ru = solve_unred(p, S, 2, 2, L, nondeg=True, weak=True)[0]
    return len(L), r4, ru, L

if __name__ == '__main__':
    t0 = time.time()
    reps = [int(r) for r in np.load('reps_f5.npy')]
    by = {}
    with mp.Pool(8) as pool:
        for c, r in pool.imap_unordered(job5, reps, chunksize=40):
            by.setdefault(c, {'sat': 0, 'unsat': 0})[r] += 1
    print('(1) p=5 solve4 (Lemma Q + R reduced CNF, as called by WNEST_5) over all spanning orbit reps:')
    print('   ', {c: by[c] for c in sorted(by)})
    print('    unsat total:', sum(v['unsat'] for v in by.values()), f'[{time.time()-t0:.0f}s]', flush=True)
    rng = np.random.default_rng(77)
    tasks = []
    for p, S in ((7, [0, 1, 2, 4]), (7, [0, 1, 6])):
        P = [s for s in S if s]
        allv = [v for v in itertools.product(range(p), repeat=2) if any(v)]
        classes = []
        seen = set()
        for v in allv:
            if v in seen:
                continue
            cl = sorted({((l * v[0]) % p, (l * v[1]) % p) for l in P}); classes.append(cl); seen |= set(cl)
        for t in range(150):
            if t % 2 == 0:
                c = int(rng.integers(2, 8))
                pick = rng.choice(len(classes), size=c, replace=False)
                L = sorted({l for i in pick for l in classes[i]})
            else:
                c = int(rng.integers(4, 16))
                L = [allv[i] for i in rng.choice(len(allv), size=c, replace=False)]
            if not any((a[0] * b[1] - a[1] * b[0]) % p for a in L for b in L):
                continue
            tasks.append((p, S, L))
    dis = []; cnt = {}
    with mp.Pool(8) as pool:
        for c, r4, ru, L in pool.imap_unordered(job7, tasks, chunksize=2):
            key = (r4, ru); cnt[key] = cnt.get(key, 0) + 1
            if r4 != ru:
                dis.append((L, r4, ru))
                print('   DISAGREE (reduced, unreduced):', r4, ru, L, flush=True)
    print('(2) p=7 random label sets: (reduced, unreduced) verdict counts', cnt, f'[{time.time()-t0:.0f}s]')
    print('    disagreements:', len(dis))
