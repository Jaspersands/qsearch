"""Referee B: Lemma Q completeness test at p = 7, bounded version (q_check.py part (2) stalled on
hard unreduced UNSAT instances and was stopped after ~25 min).  Same comparison -- note's solve4
(Lemma Q + R reduced) vs note's unreduced gadget_cnf.solve (weak nondegeneracy) -- on random label
sets with <= 4 P-classes (P-closed) or <= 10 labels (arbitrary), each solver call with a pycosat
propagation limit; 'unknown' results are counted, not interpreted.
"""
import sys, itertools, numpy as np, multiprocessing as mp, time
sys.path.insert(0, '../2026-11-08-rees-sde-fq-nest')
import pycosat
import gadget_cnf, gadget_cnf4

LIMIT = 20_000_000
class Limited:
    @staticmethod
    def solve(clauses):
        r = pycosat.solve(clauses, prop_limit=LIMIT)
        if r == 'UNKNOWN':
            raise TimeoutError
        return r
gadget_cnf.pycosat = Limited
gadget_cnf4.pycosat = Limited

def job(args):
    p, S, L = args
    try:
        r4 = gadget_cnf4.solve4(p, S, 2, 2, L, weak=True)[0]
    except TimeoutError:
        r4 = 'unknown'
    try:
        ru = gadget_cnf.solve(p, S, 2, 2, L, nondeg=True, weak=True)[0]
    except TimeoutError:
        ru = 'unknown'
    return r4, ru, L

if __name__ == '__main__':
    t0 = time.time(); rng = np.random.default_rng(78); tasks = []
    for p, S in ((7, [0, 1, 2, 4]), (7, [0, 1, 6])):
        P = [s for s in S if s]
        allv = [v for v in itertools.product(range(p), repeat=2) if any(v)]
        classes, seen = [], set()
        for v in allv:
            if v not in seen:
                cl = sorted({((l * v[0]) % p, (l * v[1]) % p) for l in P}); classes.append(cl); seen |= set(cl)
        for t in range(200):
            if t % 2 == 0:
                pick = rng.choice(len(classes), size=int(rng.integers(2, 5)), replace=False)
                L = sorted({l for i in pick for l in classes[i]})
            else:
                L = [allv[i] for i in rng.choice(len(allv), size=int(rng.integers(4, 11)), replace=False)]
            if any((a[0] * b[1] - a[1] * b[0]) % p for a in L for b in L):
                tasks.append((p, S, L))
    cnt, dis = {}, []
    with mp.Pool(8) as pool:
        for r4, ru, L in pool.imap_unordered(job, tasks, chunksize=1):
            cnt[(r4, ru)] = cnt.get((r4, ru), 0) + 1
            if 'unknown' not in (r4, ru) and r4 != ru:
                dis.append(L); print('DISAGREE (reduced, unreduced):', r4, ru, L, flush=True)
    print(f'p=7 (kappa=2 and 3) random label sets, {len(tasks)} instances: (reduced, unreduced) counts {cnt}')
    print(f'disagreements (both decided): {len(dis)}  [{time.time()-t0:.0f}s]')
