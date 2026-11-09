"""One exact Sage reuse of the already prescribed p5 irreducible control."""
import itertools
import json
from collections import Counter
from pathlib import Path
from sage.all import GF, PolynomialRing, QQ

field = GF(5)
ring = PolynomialRing(field, 'X')
X = ring.gen()
Q = X**2 + 2  # Analysis truth only; the estimator receives F and public h.
d, m = 2, 3

def chi(x):
    return 0 if x == 0 else (1 if x.is_square() else -1)

def F(x):
    return chi(Q(x)) or 1

def native_phase(poly):
    if poly.degree() != m:
        return None
    factors = poly.factor()  # PUBLIC polynomial only.
    if len(factors) != m or any(f.degree() != 1 or e != 1 for f, e in factors):
        return None
    value = chi(poly.leading_coefficient())**d
    for f, _ in factors:
        value *= F(-f[0] / f[1])
    return value

source = []
for roots in itertools.combinations(list(field), m):
    monic = ring.one()
    for x in roots:
        monic *= X-x
    source.extend(a*monic for a in field if a)
counts = Counter(tuple(int(c) for c in (R % Q).list()) for R in source)
N, K0, D, U = len(source), 25, 625, 24
energy = sum(v*v for v in counts.values())
signed_sum = sum(native_phase(R) for R in source)
assert N == 40 and energy == 72 and signed_sum == 8
actual_zero = QQ(signed_sum**2)/(N*D)
mask_H = QQ(energy)/(N*K0)
mask_zero = QQ(N)/D
mixture_zero = (mask_H-mask_zero)/U
assert actual_zero == QQ(8)/3125 and mixture_zero == QQ(1)/3000
features = []
for h in [ring.zero(), ring.one(), X, X*(X-1), Q, X*Q]:
    observations = []
    for R in source:
        translated_phase = native_phase(R+h)
        observations.append(0 if translated_phase is None else native_phase(R)*translated_phase)
    features.append({'h': str(h), 'mean': str(QQ(sum(observations))/N),
                     'counts': {str(k):v for k,v in sorted(Counter(observations).items())}})
result = {'scope': 'Exact reuse of existing p5 control; full population of the classical estimator, no Monte Carlo confidence, new parameter sweep, FFT or quantum execution.',
          'N': N, 'fiber_energy': energy, 'signed_sum': signed_sum,
          'actual_zero': str(actual_zero), 'independent_mixture_zero': str(mixture_zero),
          'chosen_sign_feature_population': features}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, separators=(',',':')))
