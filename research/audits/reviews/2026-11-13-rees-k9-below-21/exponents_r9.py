#!/opt/anaconda3/bin/python
"""Rule R9 = R8 + verified l-level {0}-nodes (this report).  Finite exact computation; CONDITIONAL like R8.

R8 is 2026-11-13-rees-k9-bottleneck/exponents_r8.py, imported read-only.  The only change: at the pairs listed in
NEW0 the chain degree deg[{0}] used by R8's base is replaced by min(deg[{0}], NEW0), where NEW0 is the degree l
of an l-level {0}-contraction whose full table was verified by two programs (ell_common.verify and
verify_full_basis.py) and executed end to end (tensor_exec.py).  No two-class l-level node, no l-level finish is
added (so R9 is an upper bound of what these objects give, not their optimum).
usage: exponents_r9.py [PMAX] [set]   set = all (default) | no73 | only13 | no13
"""
import sys, os, math, functools
HERE = os.path.dirname(os.path.abspath(__file__))
BN = os.path.join(os.path.dirname(HERE), '2026-11-13-rees-k9-bottleneck')
sys.path.insert(0, BN)
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_r8 as R8
sys.argv = ARGV
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
SET = sys.argv[2] if len(sys.argv) > 2 else 'all'

NEW0_ALL = {(9, 37): 4, (9, 19): 4, (9, 73): 4, (4, 13): 3, (6, 13): 3}
NEW0 = dict(NEW0_ALL)
if SET == 'no73':
    NEW0.pop((9, 73))
elif SET == 'only13':
    NEW0 = {k: v for k, v in NEW0.items() if k[1] == 13}
elif SET == 'no13':
    NEW0 = {k: v for k, v in NEW0.items() if k[1] != 13}
for k in list(NEW0):
    if os.environ.get('R9_DROP') and str(k) in os.environ['R9_DROP']:
        NEW0.pop(k)

_deg_orig = R8.deg


def deg_new(k, p, K):
    d = _deg_orig(k, p, K)
    if tuple(K) == (0,) and (k, p) in NEW0:
        return NEW0[(k, p)] if d is None else min(d, NEW0[(k, p)])
    return d


R8.deg = deg_new          # r8() looks deg up in its module globals at call time
R8.r8.cache_clear(); R8.stage_options.cache_clear()
r9 = R8.r8
E = R8.E

if __name__ == '__main__':
    P = [q for q in R8.X.primes_upto(PMAX) if q > 2]
    print('R9 = R8 + NEW0 =', NEW0, ' primes 3..%d' % PMAX)
    for (k, p) in sorted(NEW0):
        print(f'  kappa={k} p={p}: R8 plan -> R9 = {r9(k, p, True)}')
    for c in range(2, 10):
        vals = sorted(((E(r9, c, p), p) for p in P if p > c), reverse=True)
        top = vals[0][0]
        print(f'c={c} R9 max {top} attained at', sorted(q for v, q in vals if v == top)[:40],
              ' next:', next(((v, q) for v, q in vals if v < top), None), flush=True)
    vals = sorted(((E(r9, 9, p), p) for p in P if p > 9), reverse=True)[:24]
    print('c=9 R9 top primes:', vals)
    for p in (13, 19, 37, 73, 43, 127, 181, 433, 631, 673, 1009, 2017, 2521, 7561):
        print(f'c=9 p={p}: e_d(R9) =', [r9(math.gcd(d, p - 1), p) for d in range(2, 10)],
              'kappa_d =', [math.gcd(d, p - 1) for d in range(2, 10)], 'E9 =', E(r9, 9, p))
