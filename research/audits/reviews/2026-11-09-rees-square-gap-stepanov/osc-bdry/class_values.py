"""Per-multiset-class values of n*Fhat(r,c)/Fhat(0) from saved ../osc-k5/acc_k*_p*.npy.

Fhat(r,c) depends only on the multisets of r and c (F is S_k x S_k invariant), so one
representative (sorted vector) per multiset suffices.  Output: class_values_k<k>.npz with
  ps (primes), ms (list of multisets as sorted tuples, sum = 0 mod k), V[p_index, i, j] =
  n*Fhat(ms[i], ms[j]) / Fhat(0)  (complex), n = p+1-2k, N1 = Fhat(0)/k^2.
Usage: python class_values.py k [pmin]
"""
import sys, os, glob, itertools, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'osc-k5')
sys.path.insert(0, SRC)
from osc_k5 import build_F  # noqa: E402

k = int(sys.argv[1])
pmin = int(sys.argv[2]) if len(sys.argv) > 2 else 0
ps = sorted(int(os.path.basename(f).split('_p')[1][:-4]) for f in glob.glob(os.path.join(SRC, 'acc_k%d_p*.npy' % k)))
ps = [p for p in ps if p >= pmin]
ms = sorted({tuple(sorted(v)) for v in itertools.product(range(k), repeat=k) if sum(v) % k == 0})
V = np.zeros((len(ps), len(ms), len(ms)), dtype=complex)
N1 = np.zeros(len(ps))
keep = []
for a, p in enumerate(ps):
    acc = np.load(os.path.join(SRC, 'acc_k%d_p%d.npy' % (k, p)))
    Ft, _ = build_F(k, acc)
    Fh = np.fft.fftn(Ft)
    F0 = Fh.flat[0].real
    if F0 < 0.5:
        continue
    n = p + 1 - 2 * k
    for i, r in enumerate(ms):
        for j, c in enumerate(ms):
            V[a, i, j] = n * Fh[r + c] / F0
    N1[a] = F0 / k ** 2
    keep.append(a)
    print(p, 'done', flush=True)
V = V[keep]
ps = [ps[a] for a in keep]
N1 = N1[keep]
np.savez(os.path.join(HERE, 'class_values_k%d.npz' % k), ps=np.array(ps), ms=np.array(ms), V=V, N1=N1)
print('saved', len(ps), 'primes', len(ms), 'multisets')
