"""Negative controls (the support check must be able to fail): drop the public cubic Q3 (q = 0) in the true
level-2 states while keeping everything else public and unchanged."""
import sys, numpy as np, pipeline as P
p = int(sys.argv[1]); P.log = lambda *a: None
orig_L2 = P.Level2.__init__
def noQ(self, trips, u, q, p_, rng): orig_L2(self, trips, u, np.zeros(4, dtype=np.int64), p_, rng)
for name in ('A_noQ3',):
    P.Level2.__init__ = noQ
    res = []
    for sd in range(200, 206):
        rng = np.random.default_rng(sd)
        while True:
            eta = rng.integers(0, p, 5)
            if eta[0] % p: break
        eta = (eta * pow(int(eta[0]), -1, p)) % p
        R = P.run_once(p, eta, rng)
        if R['ok']: res.append((R['viol'], round(R['mass_on_line'], 3), R['supp']))
    print(name, 'p=%d (violations, mass on predicted line, support) per run:' % p, res)
    P.Level2.__init__ = orig_L2
