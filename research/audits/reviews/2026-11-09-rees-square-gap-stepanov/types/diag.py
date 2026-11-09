"""Where does the margin L1 come from?  Top type-frequencies rho=(r,c) by |Fhat|, and the L1 left
after removing the frequencies supported on at most two rows and two columns (|supp r|,|supp c| <= 2)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sep_types import run
k = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    d = run(k, p)
    absF, nz, F0, W = d['absF'], d['nz'], d['F0'], d['W']
    idx = np.argwhere(nz)
    vals = absF[nz]
    order = np.argsort(-vals)
    print('k', k, 'p', p, 'marginL1', '%.4g' % d['L1'], 'permL1', '%.4g' % d['PW'], 'n_rho', len(vals))
    for t in order[:8]:
        rc = idx[t]
        print('   r=', tuple(rc[:k]), 'c=', tuple(rc[k:]), '|Fhat|/Fhat0 = %.4g' % (vals[t] / F0))
    rs = (idx[:, :k] != 0).sum(1); cs = (idx[:, k:] != 0).sum(1)
    for a in range(0, k + 1):
        for b in range(0, k + 1):
            sel = (rs == a) & (cs == b)
            if sel.any():
                print('   supp(r)=%d supp(c)=%d  count=%6d  L1 share=%.4g  permL1 share=%.4g' % (a, b, sel.sum(), vals[sel].sum() / F0,
                      (vals * W[nz])[sel].sum() / (F0 * float(__import__("math").factorial(k)) ** 2)))
    sys.stdout.flush()
