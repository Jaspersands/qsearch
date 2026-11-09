import numpy as np, sys
sys.path.insert(0, '.')
from gauss_fit_lib import gammas, load
k = 5
ps, ms, V, idx = load(k)
specs = [('113', '113', (2, -1)), ('122', '122', (1, 2)), ('113', '122', (1, 2)), ('113', '334', (2, -1)), ('14', '23', (0, 0)),
         ('113', '0', (2, -1)), ('122', '0', (1, 2))]
print('  p    lam  ' + '  '.join('%s/%s' % (a, b) for a, b, _ in specs))
for a, p in enumerate(ps):
    if p < 300: continue
    G = gammas(int(p), k)
    row = []
    for rn, cn, ex in specs:
        M = G[1] ** ex[0] * G[2] ** ex[1]
        R = V[a, idx[rn], idx[cn]] / M
        row.append('%+.3f%+.3fi' % (R.real, R.imag))
    print('%5d %5.2f  ' % (p, p / k ** (k - 1)) + '  '.join(row))
