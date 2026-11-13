"""Check 1: the true per-copy post-front-end state (random base point, exact label and y sampling) vs the
trial-H brute-force routine and the re-derived closed form.  Also: y distribution, flatness, l-sector,
associativity of BCH."""
import sys, numpy as np
from f23 import *
p = int(sys.argv[1]); N = int(sys.argv[2]); rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
# associativity
X = rng.integers(0, p, (200, 5)); Y = rng.integers(0, p, (200, 5)); Z = rng.integers(0, p, (200, 5))
print('assoc failures:', int((bch(bch(X, Y, p), Z, p) != bch(X, bch(Y, Z, p), p)).any(axis=1).sum()))
bad = dict(n=0, special=0, flat=0, trial=0, closed=0, ysupp=0, lsector=0)
for it in range(N):
    eta = rng.integers(0, p, 5)
    if (eta[:2] % p == 0).all(): continue
    c = true_copy(p, eta, rng)
    L = c['L']; bad['n'] += 1
    if L.f(eta) == 0:
        bad['special'] += 1; continue
    P = c['Py'].reshape(p, p, p)
    # y outcome: uniform on l = -1 sector?
    if not np.allclose(P[:, :, (-1) % p], 1.0 / p ** 2): bad['ysupp'] += 1
    if P.sum() - P[:, :, (-1) % p].sum() > 1e-9: bad['lsector'] += 1
    try:
        Pt = phase_of(c['phi'], p)
    except AssertionError:
        bad['flat'] += 1; continue
    Ptr = trial_copy(p, L, c['y'], eta)
    bad['trial'] += int((Pt != Ptr).any())
    Pc = closed_form(p, L, c['y'], eta)
    bad['closed'] += int((Pt != Pc).any())
print('p=%d' % p, bad)
