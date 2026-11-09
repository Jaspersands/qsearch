"""RMS of n|Fhat|/Fhat0 per support class (m_r, m_c), binned by lambda = p/k^(k-1), for k = 3, 4, 5."""
import numpy as np, itertools
files = {3: 'class_values_k3_wide.npz', 4: 'class_values_k4_wide.npz', 5: 'class_values_k5.npz'}
bins = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 200]
for k, fn in files.items():
    d = np.load(fn); ps, ms, V = d['ps'], [tuple(m) for m in d['ms']], d['V']
    supp = np.array([sum(1 for x in m if x) for m in ms])
    lam = ps / k ** (k - 1)
    print('k=%d' % k)
    hdr = '   class      ' + ' '.join('%7s' % ('<%g' % b) for b in bins[1:])
    print(hdr)
    for mr in range(0, k + 1):
        for mc in range(mr, k + 1):
            if mr + mc == 0 or mr == 1 or mc == 1: continue
            I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mc)
            vals = V[:, I][:, :, J]
            rms = np.sqrt((abs(vals) ** 2).mean(axis=(1, 2)))
            mx = abs(vals).max(axis=(1, 2))
            row = []
            for lo, hi in zip(bins[:-1], bins[1:]):
                s = (lam >= lo) & (lam < hi)
                row.append('%7.3f' % mx[s].mean() if s.any() else '      -')
            print('  (%d,%d) max  ' % (mr, mc) + ' '.join(row))
