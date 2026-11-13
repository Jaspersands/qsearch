import sys, numpy as np, pipeline as P
p = int(sys.argv[1]); n = int(sys.argv[2])
P.log = lambda *a: None
for sd in range(100, 100 + n):
    rng = np.random.default_rng(sd)
    while True:
        eta = rng.integers(0, p, 5)
        if eta[0] % p: break
    eta = (eta * pow(int(eta[0]), -1, p)) % p
    P.run_once(p, eta, rng)
z = [tuple(int(v == 0) for v in k[0]) for k in P.K3LOG]
print('p=%d: %d level-3 systems; K3 shapes %s; zero pattern counts %s' % (p, len(P.K3LOG), set(len(k) for k in P.K3LOG),
      {pat: z.count(pat) for pat in set(z)}))
