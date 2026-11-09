"""Compare an mc_classes.py npz with the exact osc-k5 class values (k = 5): per support bin, the
MC error against the MC standard error, and |V_exact| against the finite-ensemble scale
sigma_config / sqrt(N_unl) (N_unl = number of unlabelled (C1) PGL_2-orbits)."""
import sys, numpy as np
f = sys.argv[1]
d = np.load(f)
k, p = int(d['k']), int(d['p'])
names = list(d['names'])
supp = d['supp']
N = d['cnt'].sum()
Vh = d['S1'].sum(0) / N
sig = np.sqrt(np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0))
se = sig / np.sqrt(N)
Nunl = float(d['Nunl'])
ex = np.load('../osc-bdry/class_values_k%d.npz' % k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
mn = [name(tuple(c)) for c in ex['ms']]
perm = [mn.index(x) for x in names]
a = list(ex['ps']).index(p)
Ve = ex["V"][a][np.ix_(perm, perm)]
z = np.abs(Vh - Ve) / np.maximum(se, 1e-12)
print('k=%d p=%d conf=%d N_unl=%.1f   max |MC-exact|/se = %.2f, median %.2f' % (k, p, N, Nunl, z.max(), np.median(z)))
print(' bin    rms|V_exact|   rms sigma_config   rms sigma/sqrt(N_unl)   ratio |V|/(sigma/sqrt N_unl)')
for mr in range(k + 1):
    for mc in range(mr, k + 1):
        if mr + mc == 0 or 1 in (mr, mc): continue
        I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mc)
        ve = np.abs(Ve[np.ix_(I, J)]); sg = sig[np.ix_(I, J)]
        rv = np.sqrt((ve ** 2).mean()); rs = np.sqrt((sg ** 2).mean())
        print(' (%d,%d)  %10.4f   %12.4f   %14.4f   %10.2f' % (mr, mc, rv, rs, rs / np.sqrt(Nunl), rv / (rs / np.sqrt(Nunl))))
