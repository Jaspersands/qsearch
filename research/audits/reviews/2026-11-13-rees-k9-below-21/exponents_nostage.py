#!/opt/anaconda3/bin/python
"""Load-bearing test: the class-c maxima WITHOUT Lemma S/F/Theorem HC and without the K_L != {0} chain corollary.

Grade value = R5, lowered only by {0}-nodes: chains to {0} as thm:app-s2-chain states them (deg[{0}] of
chains_all.json) and the l-level {0}-contractions of this report (NEW0).  No stages, no finishes, no
two-class nodes.  Finite exact computation, p <= PMAX; CONDITIONAL on R5 like R8.
usage: exponents_nostage.py [PMAX] [with73(1/0)]
"""
import sys, os, math, json, functools
HERE = os.path.dirname(os.path.abspath(__file__))
BN = os.path.join(os.path.dirname(HERE), '2026-11-13-rees-k9-bottleneck')
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '2026-11-12-rees-exponent-k8-attack'))
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_hcd as H
sys.argv = ARGV
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
W73 = (sys.argv[2] == '1') if len(sys.argv) > 2 else True
CH = json.load(open(os.path.join(BN, 'chains_all.json')))
NEW0 = {(9, 37): 4, (9, 19): 4, (4, 13): 3, (6, 13): 3}
if W73:
    NEW0[(9, 73)] = 4


@functools.lru_cache(None)
def r(k, p):
    v = H.r5(k, p)
    if k == 1 or v < 5:
        return v
    d = CH.get(f'{k}:{p}', {}).get('deg', {}).get('0')
    if d is not None:
        v = min(v, d)
    return min(v, NEW0.get((k, p), v))


def E(c, p):
    return 1 + sum(r(math.gcd(d, p - 1), p) for d in range(2, c + 1))


P = [q for q in H.X.primes_upto(PMAX) if q > 2]
print('no stages, no chain corollary; NEW0 =', NEW0, 'primes <=', PMAX)
for c in range(2, 10):
    vals = sorted(((E(c, p), p) for p in P if p > c), reverse=True)
    top = vals[0][0]
    print(f'c={c} max {top} at', sorted(q for v, q in vals if v == top)[:30], ' next:', next(((v, q) for v, q in vals if v < top), None))
