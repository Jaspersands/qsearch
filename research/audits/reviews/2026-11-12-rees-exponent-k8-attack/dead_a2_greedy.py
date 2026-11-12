#!/opt/anaconda3/bin/python
"""Randomized greedy search for large dead banks in F_41^2 (P_8 u 0 weights).  Sampled, finite: it can
only exhibit dead banks (lower bounds on N(8,2,41)); failing to find one proves nothing."""
import numpy as np, random, sys, time
p, k = 41, 8
P = sorted({pow(x, k, p) for x in range(1, p)})
vecs = [(x, y) for x in range(p) for y in range(p) if (x, y) != (0, 0)]
def shifts(A, v):
    out = np.zeros_like(A)
    for q in P:
        out |= np.roll(A, ((q * v[0]) % p, (q * v[1]) % p), axis=(0, 1))
    return out
def verify_dead(bank):
    A = np.zeros((p, p), dtype=bool); A[0, 0] = True
    for v in bank:
        if any(A[(-q * v[0]) % p, (-q * v[1]) % p] for q in P):
            return False
        A |= shifts(A, v)
    return True
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
T = float(sys.argv[2]) if len(sys.argv) > 2 else 120
t0 = time.time(); best = []; hist = {}
while time.time() - t0 < T:
    A = np.zeros((p, p), dtype=bool); A[0, 0] = True; bank = []
    order = vecs[:]; rng.shuffle(order)
    # bias: sometimes repeat a chosen column (repetitions are allowed)
    for v in order:
        reps = 1 + (rng.random() < 0.3) * rng.randrange(1, 4)
        for _ in range(reps):
            if any(A[(-q * v[0]) % p, (-q * v[1]) % p] for q in P):
                break
            A |= shifts(A, v); bank.append(v)
    hist[len(bank)] = hist.get(len(bank), 0) + 1
    if len(bank) > len(best):
        best = bank
print('greedy runs by final size:', dict(sorted(hist.items())))
print('largest dead bank found:', len(best), best, 'independently re-verified dead:', verify_dead(best))
