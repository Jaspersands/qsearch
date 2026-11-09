"""Corollary A / Lemma A need U_L != 0: a stall with |B minus U_L| = q and U_L = 0 on an unsolvable bank.
Bank e1, e2, e1+e2 in F_7^2, kappa = 2 (7 = 3 mod 4, so -1 is not a square)."""
import random
from itertools import product
from myq1 import GF, forward, flag_basis, verify
p, k = 7, 2
cols = [[1, 0], [0, 1], [1, 1]]
F = GF(p, k)
st = forward(F, cols, "first", random.Random(1))
U, _ = flag_basis(F, st["rounds"])
print("status", st["status"], "dim U_L", len(U), "B", st["B"], "unused", st["T"], "pool", st["pool"])
P0 = sorted({pow(y, k, p) for y in range(p)})
sols = [x for x in product(P0, repeat=3) if verify(p, k, cols, list(x))]
print("q =", 2 - len(U), "|B minus U| =", 2, "eps = 0;  nonzero solutions by brute force:", len(sols))
