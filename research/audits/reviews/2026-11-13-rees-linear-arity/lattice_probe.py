"""Approach (i), lattice reduction at fixed kappa (heuristic, random banks only).

L = {x in Z^n : Lambda x = 0 mod p}.  BKZ-10 basis; candidates = basis vectors and all pairwise
sums/differences; success = some candidate is a kappa-solution mod p.  Control: the same number
of uniformly random nonzero kernel vectors mod p.  Also (B1): binary {0,1} solutions versus P0
solutions on random banks (exhaustive over {0,1}^n).
Interpreter: /opt/anaconda3/envs/qsearch-cas/bin/python (fpylll).
Usage: python lattice_probe.py SEED
"""
import itertools
import random
import sys

from fpylll import IntegerMatrix, LLL, BKZ

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sdelib import Field, kernel, random_bank  # noqa: E402


def lattice_candidates(cols, p, beta=10):
    n = len(cols)
    ker = kernel(cols, p)
    rows = [list(v) for v in ker] + [[p if i == j else 0 for i in range(n)] for j in range(n)]
    B = IntegerMatrix.from_matrix(rows)
    LLL.reduction(B)
    # drop zero rows
    basis = [[B[i, j] for j in range(n)] for i in range(B.nrows) if any(B[i, j] for j in range(n))]
    B2 = IntegerMatrix.from_matrix(basis)
    if beta:
        BKZ.reduction(B2, BKZ.Param(block_size=min(beta, n)))
    basis = [[B2[i, j] for j in range(n)] for i in range(B2.nrows)]
    cands = list(basis)
    for u, v in itertools.combinations(basis, 2):
        cands.append([x + y for x, y in zip(u, v)])
        cands.append([x - y for x, y in zip(u, v)])
    return cands, ker


def ok(F, x):
    return any(xi % F.p for xi in x) and all(F.inP0(xi) for xi in x)


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    print("kappa p a n  trials  lattice_succ  random_succ  #cands  (CW bound kappa*a+1)")
    for k, p in ((2, 31), (2, 101), (3, 31), (3, 97)):
        F = Field(p, k)
        for a in (2, 4, 6):
            for n in sorted({a + 2, 2 * a + 1, k * a + 1, 3 * a + 1}):
                T = 20
                ls = rs = 0
                nc = 0
                for _ in range(T):
                    cols = random_bank(p, a, n, rng)
                    cands, ker = lattice_candidates(cols, p)
                    nc = len(cands)
                    ls += any(ok(F, x) for x in cands)
                    hit = False
                    for _ in range(len(cands)):
                        c = [rng.randrange(p) for _ in ker]
                        x = [sum(ci * y[i] for ci, y in zip(c, ker)) % p for i in range(n)]
                        if ok(F, x):
                            hit = True
                            break
                    rs += hit
                print(f"{k:5d} {p:3d} {a} {n:2d}  {T:6d}  {ls:12d}  {rs:11d}  {nc:6d}  {k*a+1}")
    print()
    print("(B1) kappa=2, p=101, a=2: banks with a {0,1}-solution vs with a P0-solution (200 banks each)")
    F = Field(101, 2)
    for n in range(5, 15):
        nb = nP = 0
        for _ in range(200):
            cols = random_bank(101, 2, n, rng)
            hasb = False
            for bits in range(1, 1 << n):
                s0 = s1 = 0
                for i in range(n):
                    if bits >> i & 1:
                        s0 += cols[i][0]
                        s1 += cols[i][1]
                if s0 % 101 == 0 and s1 % 101 == 0:
                    hasb = True
                    break
            nb += hasb
            nP += 1  # Chevalley-Warning: n >= 2a+1 = 5 always solvable
        print(f"  n={n:2d}: binary {nb:3d}/200   P0 200/200 (CW)   expected #binary sols (2^n-1)/p^2 = {(2**n-1)/101**2:.3f}")


if __name__ == "__main__":
    main()
