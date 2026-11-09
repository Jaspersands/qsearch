import numpy as np, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'osc-k5'))
from osc_k5 import primroot
def gammas(p, k):
    g = primroot(p); ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    xs = np.arange(1, p)
    add = np.exp(2j * np.pi * xs / p)
    return {a: (np.exp(2j * np.pi * a * (ind[xs] % k) / k) * add).sum() / np.sqrt(p) for a in range(1, k)}
def load(k):
    d = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'class_values_k%d.npz' % k))
    ms = [tuple(m) for m in d['ms']]
    name = lambda m: ''.join(str(x) for x in m if x) or '0'
    return d['ps'], ms, d['V'], {name(m): i for i, m in enumerate(ms)}
