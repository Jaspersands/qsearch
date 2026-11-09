"""Systematic vs noise by p-scaling.  For each support bin (m_r,m_c): rms|V| over the bin's
multiset pairs, per prime, against the orbit-noise scale sigma = sqrt(p/N1).  A noise-like bin
has rms/sigma ~ const; a systematic (c/p) bin has rms ~ const, so rms/sigma grows like
sqrt(N1/p).  Prints log-log slopes of rms vs p and of sigma vs p over the upper half of the
primes, and the bin's rms/sigma at the lowest and highest primes."""
import numpy as np, sys
files = {3: 'class_values_k3_wide.npz', 4: 'class_values_k4_wide.npz', 5: 'class_values_k5.npz'}
for k in map(int, sys.argv[1:] or ['3', '4', '5']):
    d = np.load(files[k]); ps, ms, V, N1 = d['ps'].astype(float), [tuple(m) for m in d['ms']], d['V'], d['N1']
    ok = N1 > 0
    ps, V, N1 = ps[ok], V[ok], N1[ok]
    supp = np.array([sum(1 for x in m if x) for m in ms])
    sig = np.sqrt(ps / N1)
    up = ps >= np.median(ps)
    sl_sig = np.polyfit(np.log(ps[up]), np.log(sig[up]), 1)[0]
    print('k=%d primes %d..%d (%d), lambda %.2f..%.2f; slope of sigma=sqrt(p/N1) on upper half: %+.2f' % (
        k, ps.min(), ps.max(), len(ps), ps.min() / k ** (k - 1), ps.max() / k ** (k - 1), sl_sig))
    for mr in range(0, k + 1):
        for mc in range(mr, k + 1):
            if mr + mc == 0 or mr == 1 or mc == 1: continue
            I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mc)
            vals = V[:, I][:, :, J]
            rms = np.sqrt((abs(vals) ** 2).mean(axis=(1, 2)))
            sl = np.polyfit(np.log(ps[up]), np.log(rms[up]), 1)[0]
            r = rms / sig
            print('  (%d,%d) slope rms %+.2f  rms lo/hi %.3g/%.3g   rms/sigma lo/hi %.3g/%.3g' % (
                mr, mc, sl, rms[0], rms[-1], r[0], r[-1]))
