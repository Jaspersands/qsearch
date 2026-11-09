"""Decompose the type-frequency L1 (orbit_types.py) by support sizes of r and c, and report the
median of |Fhat(rho)| / sqrt(Fhat(0) * p) over rho != 0 (random-phase-over-orbits benchmark ~ 1)."""
import sys, os, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orbit_types import run
k = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    d = run(k, p, want_arrays=True)
    absF, nz, F0, W = d['absF'], d['nz'], d['F0'], d['W']
    idx = np.argwhere(nz); vals = absF[nz]; w = W[nz]
    kf = float(math.factorial(k)) ** 2
    print('k', k, 'p', p, 'L1 %.4g' % d['L1'], 'PW %.4g' % d['PW'], 'median|Fhat|/sqrt(F0 p) %.3g' % (np.median(vals) / math.sqrt(F0 * p)),
          'max|Fhat|/F0 %.3g' % (vals.max() / F0))
    rs = (idx[:, :k] != 0).sum(1); cs = (idx[:, k:] != 0).sum(1)
    tot = np.minimum(rs, cs)
    for a in range(k + 1):
        for b in range(k + 1):
            sel = (rs == a) & (cs == b)
            if sel.any() and (vals[sel].sum() / F0 > 0.01 or (vals * w)[sel].sum() / (F0 * kf) > 0.01):
                print('   |supp r|=%d |supp c|=%d n=%6d  L1 share %.4f  PW share %.4f  median|Fhat|/sqrt(F0 p) %.3g' % (
                    a, b, sel.sum(), vals[sel].sum() / F0, (vals * w)[sel].sum() / (F0 * kf), np.median(vals[sel]) / math.sqrt(F0 * p)))
    sys.stdout.flush()
