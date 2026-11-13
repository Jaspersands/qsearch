"""v2: end-to-end run of the TL6 node (GE, then Lemma R with RC(6; Z_6 -> {0})) using executor.py
(read-only import) at certificate primes, plus a perturbed-certificate control.  Finite falsifier."""
import json, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import executor as X
C = json.load(open(os.path.join(HERE, 'certs_tl6_all.json')))['found']
rng = random.Random(5); tot = ok = 0
for p in (2521, 7561, 12601, 100801, 1009, max(int(q) for q in C)):
    w = C[str(p)]; st = X.step_from_cert(w, 6, range(6)); ctx = X.Ctx(p, 6)
    for a in (1, 2, 3):
        for kind in ('uniform', 'repeated', 'axis', 'zeros'):
            for rep in range(3):
                A = X.arity(a, [st]); lam = X.bank(kind, A, a, p, rng)
                rel = X.chain(ctx, lam, list(range(A)), a, [st]); tot += 1
                ok += X.check_solution(ctx, rel, lam, a)
    print('TL6', p, 'ok so far', ok, '/', tot, flush=True)
# control: perturb alpha_1 of the 2521 certificate; the chain must fail (assertion or wrong class)
w = dict(C['2521']); w['alpha'] = list(w['alpha']); w['alpha'][1] = (w['alpha'][1] + 1) % 2521
st = X.step_from_cert(w, 6, range(6)); ctx = X.Ctx(2521, 6); bad = 0
for rep in range(6):
    lam = X.bank('uniform', X.arity(2, [st]), 2, 2521, rng)
    try:
        rel = X.chain(ctx, lam, list(range(X.arity(2, [st]))), 2, [st]); X.check_solution(ctx, rel, lam, 2)
    except AssertionError: bad += 1
print('perturbed 2521 certificate: failures', bad, '/ 6 (must be > 0)')
print('ALL', ok, '/', tot)
