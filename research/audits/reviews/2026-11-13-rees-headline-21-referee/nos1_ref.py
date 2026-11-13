"""Referee side check: which (p, kappa) need candidate S1 (the only use of Theorem is-import)?
Recompute Schedule 1H+ degrees with S1 forbidden at every level (degree = inf if no other candidate)."""
import math, sys
import rule_ref as R
INF = 10 ** 6
orig = R.degrees
def degrees_noS1(p, new=True):
    # monkeypatch: run the original but drop S1 by post-filter at each kappa (recursive use via e dict)
    cyc = R.Cyc(p) if p < R.SMALL else None
    e, plan = {}, {}
    src = R.degrees.__code__
    return None
# simplest: copy of R.degrees with S1 removed
import types
code = open(R.__file__).read()
start = code.index('def degrees('); end = code.index('def Eval(')
body = code[start:end].replace("cands = [(kap * math.ceil(math.log2(t)), 'S1')]", "cands = [(INF, 'none')]")
ns = dict(R.__dict__); ns['INF'] = INF
exec(body, ns)
deg = ns['degrees']
lim = int(sys.argv[1])
need = []
Em = {}
for p in R.sieve(lim):
    if p < 3: continue
    e, pl = deg(p)
    bad = [k for k in e if e[k] >= INF]
    if bad: need.append((p, bad))
    for c in range(2, 10):
        if p <= c: continue
        v = R.Eval(e, p, c)
        if v > Em.get(c, (0,))[0]: Em[c] = (v, [p])
        elif v == Em[c][0]: Em[c][1].append(p)
print('S1 indispensable at', len(need), 'primes; first:', need[:40])
print('max E without S1 (>=1e6 means some grade unsolvable):', {c: (v if v < INF else 'INF', ps[:6]) for c, (v, ps) in Em.items()})
