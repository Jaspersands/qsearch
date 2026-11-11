"""Cross-check of int_cnf.py (this note) against the earlier encoders gadget_cnf5.solve4 (Lemma R + Q,
2026-11-08 note) and free_cnf.run (Lemma R, no Q; referee C) on random P-closed spanning label sets:
the three modes of int_cnf (equi, freeR, free) and the two old encoders must give the same verdict
(Lemma N' predicts free == freeR == equi).  SAT models of every encoder are re-checked by the
encoder's own checker and the int_cnf models by int_cnf.check_solution.  Verdicts only (gadget_cnf5 runs with its LRAT check because its no-proof mode prints no model).
"""
import sys, os, random, itertools, tempfile, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..', '2026-11-08-rees-sde-fq-nest'))
sys.path.insert(2, os.path.join(HERE, '..', '2026-11-09-rees-sde-fq-nest-referee-C'))
import int_cnf as IC
import gadget_cnf5 as G5
import free_cnf as FC

work = tempfile.mkdtemp(dir=os.environ.get('SCR', None))
rng = random.Random(1111)

def rand_closed(p, P, size):
    allv = [l for l in itertools.product(range(p), repeat=2) if any(l)]
    while True:
        L = sorted({tuple((nu * x) % p for x in l) for l in rng.sample(allv, size) for nu in P})
        if any((a[0] * b[1] - a[1] * b[0]) % p for a in L for b in L): return L

def verdicts(p, S, L):
    out = {}
    for mode in ('equi', 'freeR', 'free'):
        r, info, sol = IC.solve(p, S, 2, L, mode, work=work, proof=False, tag='x')
        if r == 'SAT': assert info['model_check'] == 'OK', info
        out['int_' + mode] = r
    r, sol, dt = G5.solve4(p, S, 2, 2, L, ext=dict(solver='cadical', work=work, proof=True, keep=False, tag='g5'))
    out['gadget_cnf5'] = r.upper()
    r, info, sol = FC.run(p, S, 2, L, True, None, False, work)
    out['free_cnf'] = r
    return out

tot = dis = 0
for p, S, nsets, sizes in [(7, [0, 1, 6], 15, (2, 6)), (7, [0, 1, 2, 5, 6], 6, (2, 4)), (7, [0, 1, 2, 4], 15, (2, 6)),
                           (7, [0, 3, 4], 15, (2, 6)), (11, [0, 1, 2, 9, 10], 8, (2, 6)), (11, [0, 1, 3, 8, 10], 5, (2, 5))]:
    P, _ = IC.stabiliser(p, S)
    cnt = {}
    for _ in range(nsets):
        L = rand_closed(p, P, rng.randint(*sizes))
        v = verdicts(p, S, L)
        tot += 1
        if len(set(v.values())) != 1:
            dis += 1; print('DISAGREE', p, S, L, v, flush=True)
        cnt[v['int_equi']] = cnt.get(v['int_equi'], 0) + 1
    for name, L in (('nest', IC.parse_L(p, 2, 'nest')),) if p == 7 else ():
        v = verdicts(p, S, L); tot += 1
        if len(set(v.values())) != 1: dis += 1; print('DISAGREE', p, S, name, v, flush=True)
        cnt['nest:' + v['int_equi']] = 1
    print(f'p={p} S={S}: {cnt}', flush=True)
print(f'TOTAL {tot} label sets x 5 encoders, disagreements {dis}')
