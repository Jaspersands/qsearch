"""Run btc (C port of bt.py) on a label set and verify any SAT answer with bt.verify."""
import os, sys, subprocess, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bt import setup, pclass_reps, verify

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'btc')


def decide_c(p, kappa, k, d, L, node_limit=0):
    ctx = setup(p, kappa, k, d)
    reps = pclass_reps(p, ctx['P'], L)
    inp = f'{p} {kappa} {k} {d} {len(reps)}\n' + '\n'.join(' '.join(map(str, l)) for l in reps) + '\n'
    r = subprocess.run(['nice', '-n', '19', BIN, str(node_limit)], input=inp, capture_output=True, text=True)
    lines = r.stdout.split('\n')
    head = lines[0].split()
    if head[0] == 'TIMEOUT':
        return 'timeout', int(head[1]), None
    if head[0] == 'UNSAT':
        return 'UNSAT', int(head[1]), None
    assert head[0] == 'SAT', r.stdout + r.stderr
    fi = list(map(int, lines[1].split())); gi = list(map(int, lines[2].split()))
    slots = [(D, ci) for D in range(len(ctx['dirs'])) for ci in range(len(ctx['creps']))]
    gamma, Phi = {}, {}
    for s, g in zip(slots, gi):
        a = tuple((ctx['creps'][s[1]] * x) % p for x in ctx['dirs'][s[0]])
        gv = ctx['gvals'][g]
        for lam in ctx['P']:
            gamma[tuple((lam * x) % p for x in a)] = tuple((lam * x) % p for x in gv)
    for l, f in zip(reps, fi):
        ph = ctx['phis'][f]
        for lam in ctx['P']:
            Phi[tuple((lam * x) % p for x in l)] = tuple((lam * x) % p for x in ph)
    ok, why = verify(ctx, L, Phi, gamma)
    assert ok, why
    return 'SAT', int(head[1]), (Phi, gamma)
