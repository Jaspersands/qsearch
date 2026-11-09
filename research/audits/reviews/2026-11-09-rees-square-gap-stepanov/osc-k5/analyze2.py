"""Second-pass diagnostics from saved acc_k5_p*.npy (produced by osc_k5.py; no re-enumeration).
Per prime and per support class (|supp r|, |supp c|): max and RMS of n|Fh|/Fh0, and the argmax rho
(as multisets of r and c values).  Usage: python analyze2.py k p1 p2 ...   (or 'all')"""
import sys, os, glob, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from osc_k5 import build_F  # noqa: E402

k = int(sys.argv[1])
if sys.argv[2:] == ['all']:
    ps = sorted(int(os.path.basename(f).split('_p')[1][:-4]) for f in glob.glob(os.path.join(HERE, 'acc_k%d_p*.npy' % k)))
else:
    ps = list(map(int, sys.argv[2:]))
sh = (k,) * k
idx = np.indices(sh)
rs1 = (idx.sum(0) % k == 0)
m1 = (idx != 0).sum(0)
for p in ps:
    acc = np.load(os.path.join(HERE, 'acc_k%d_p%d.npy' % (k, p)))
    Ft, _ = build_F(k, acc)
    Fh = np.fft.fftn(Ft)
    F0 = Fh.flat[0].real
    if F0 < 0.5:
        print(json.dumps(dict(p=p, empty=True)), flush=True)
        continue
    n = p + 1 - 2 * k
    A = (n * np.abs(Fh) / F0).reshape(k ** k, k ** k)
    out = dict(p=p, classes={})
    rr = rs1.ravel()
    mm = m1.ravel()
    for a in (0, 2, 3, 4, 5):
        for b in (0, 2, 3, 4, 5):
            if a + b == 0 or a > b:
                continue
            ri = np.flatnonzero(rr & (mm == a))
            ci = np.flatnonzero(rr & (mm == b))
            sub = A[np.ix_(ri, ci)]
            j = np.unravel_index(np.argmax(sub), sub.shape)
            rv = np.unravel_index(ri[j[0]], sh)
            cv = np.unravel_index(ci[j[1]], sh)
            out['classes']['%d,%d' % (a, b)] = dict(
                max=float(sub.max()), rms=float(np.sqrt((sub ** 2).mean())), med=float(np.median(sub)),
                arg_r=sorted(int(x) for x in rv), arg_c=sorted(int(x) for x in cv))
    print(json.dumps(out), flush=True)
