"""Negative control for chain_solver: a corrupted contraction (alpha_j shifted) must be caught."""
import random, math
from chain_solver import *
rng = random.Random(1); p, kap = 3821, 5; g = primitive_root(p); ctx = Ctx(p, g)
steps = []
for (D, R, K) in chain_steps([(5, [0, 1, 2]), (5, [0])]):
    al, be, _ = sample_pair(p, g, D, R, K, rng); steps.append((D, R, K, al, be))
roots = kth_root_table(p, kap); caught = 0; N = 40
for t in range(N):
    D, R, K, al, be = steps[t % 2]
    al2 = list(al); j = 1 + t % 4; al2[j] = (al2[j] + 1 + rng.randrange(p - 1)) % p
    bad = list(steps); bad[t % 2] = (D, R, K, al2, be)
    lam = [[rng.randrange(p) for _ in range(3)] for _ in range(math.comb(6, 3))]
    try: run(ctx, kap, 3, bad, lam, roots)
    except (AssertionError, KeyError): caught += 1
print("corrupted contractions caught: %d of %d" % (caught, N))
