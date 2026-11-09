"""Heuristic probe: does lattice reduction find {0,+-1} kernel vectors (h = 2, i.e.
P = {0, +-1}, kappa = (p-1)/2) or {0,1} kernel vectors (h = 1, kappa = p-1) at
linear arity, on RANDOM columns?  Float/heuristic only; says nothing about worst case.

Lattice: L = {x in Z^M : Lambda x = 0 mod p}, basis from the kernel over F_p plus p*Z^M.
After BKZ-beta we scan basis vectors and pairwise sums/differences for a valid witness
(entries in P as integers mod p).  Every reported success is re-checked exactly mod p.

Usage (needs fpylll; use /opt/anaconda3/envs/qsearch-cas/bin/python):
  python lattice_probe.py p h a_list M_factor trials beta [seed]
  e.g. python lattice_probe.py 5 2 10,20,30 2 10 20
M = M_factor * a + 1.
"""
import random
import sys

from fpylll import IntegerMatrix, LLL, BKZ
from fpylll.algorithms.bkz2 import BKZReduction


def kernel_basis_modp(A, p):
    """A: a x M over F_p. Return (pivots, list of kernel basis vectors)."""
    a, M = len(A), len(A[0])
    R = [row[:] for row in A]
    piv, r = [], 0
    for c in range(M):
        pr = next((i for i in range(r, a) if R[i][c] % p), None)
        if pr is None:
            continue
        R[r], R[pr] = R[pr], R[r]
        inv = pow(R[r][c], -1, p)
        R[r] = [v * inv % p for v in R[r]]
        for i in range(a):
            if i != r and R[i][c] % p:
                f = R[i][c]
                R[i] = [(x - f * y) % p for x, y in zip(R[i], R[r])]
        piv.append(c)
        r += 1
        if r == a:
            break
    free = [c for c in range(M) if c not in piv]
    ker = []
    for fc in free:
        y = [0] * M
        y[fc] = 1
        for i, pc in enumerate(piv):
            y[pc] = (-R[i][fc]) % p
        ker.append(y)
    return piv, ker


def lattice_basis(A, p):
    a, M = len(A), len(A[0])
    piv, ker = kernel_basis_modp(A, p)
    rows = []
    for y in ker:
        rows.append([((v + p // 2) % p) - p // 2 for v in y])
    for c in piv:
        e = [0] * M
        e[c] = p
        rows.append(e)
    return rows


def valid(x, A, p, h):
    if not any(x):
        return False
    allowed = {0, 1} if h == 1 else {0, 1, p - 1}
    if not all((v % p) in allowed for v in x):
        return False
    return all(sum(r[j] * x[j] for j in range(len(x))) % p == 0 for r in A)


def probe(p, h, a, M, beta, rng):
    A = [[rng.randrange(p) for _ in range(M)] for _ in range(a)]
    B = IntegerMatrix.from_matrix(lattice_basis(A, p))
    LLL.reduction(B)
    if beta > 2:
        BKZReduction(B)(BKZ.EasyParam(beta, max_loops=4))
    vecs = [list(B[i]) for i in range(B.nrows)]
    cands = list(vecs)
    small = vecs[: min(len(vecs), 60)]
    for i in range(len(small)):
        for j in range(i + 1, len(small)):
            cands.append([x + y for x, y in zip(small[i], small[j])])
            cands.append([x - y for x, y in zip(small[i], small[j])])
    for x in cands:
        for s in (1, -1):
            xx = [s * v for v in x]
            if valid(xx, A, p, h):
                return True
    return False


def main():
    p, h = int(sys.argv[1]), int(sys.argv[2])
    a_list = [int(t) for t in sys.argv[3].split(",")]
    fac, trials, beta = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    seed = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    assert (p - 1) % h == 0 and h in (1, 2)
    rng = random.Random(seed)
    for a in a_list:
        M = fac * a + 1
        ok = sum(probe(p, h, a, M, beta, rng) for _ in range(trials))
        print(f"p={p} h={h} kappa={(p-1)//h} a={a} M={M} BKZ-{beta}: {ok}/{trials}", flush=True)


if __name__ == "__main__":
    main()
