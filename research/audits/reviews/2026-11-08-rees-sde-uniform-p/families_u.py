"""Bank families for the uniform-p pass.

ec_bank: the exact-circuit family EC(r, J).  V = F_p^r, r = (J-1)L.  A random invertible A splits
V = Pi_1 (+) ... (+) Pi_L into (J-1)-dimensional pieces.  Round l is an *exact* circuit
{u_1..u_{J-1}, w = sum c_i u_i} inside Pi_l (non-monochromatic relation), so its defect e_l = 0.
Bank order: a generic reserved basis B (r random vectors) first, then the L circuits, then
random padding up to M columns.  ALG-T's forward pass (scan order = bank order) reaches V after
the circuits, so the leaf is (flag of L exact rounds, Src = B).

uniform_bank: i.i.d. uniform columns of rank r (padded to M).
"""
import random


def rand_inv(rng, p, r):
    from sss import rank
    while True:
        A = [[rng.randrange(p) for _ in range(r)] for _ in range(r)]
        if rank(A, p)[0] == r:
            return A


def ec_bank(rng, Fd, J, L, M, nonmono=True):
    p = Fd.p
    r = (J - 1) * L
    A = rand_inv(rng, p, r)              # rows used as vectors u
    B = rand_inv(rng, p, r)
    cols = [list(v) for v in B]
    for l in range(L):
        us = A[(J - 1) * l:(J - 1) * (l + 1)]
        while True:
            c = [rng.randrange(1, p) for _ in us]
            # forward pass normalises delta_w = 1, delta_u = -c
            cl = {Fd.cls(-ci % p) for ci in c} | {0}
            if len(cl) > 1 or not nonmono:
                break
        w = [sum(ci * u[t] for ci, u in zip(c, us)) % p for t in range(r)]
        cols += [list(u) for u in us] + [w]
    while len(cols) < M:
        cols.append([rng.randrange(p) for _ in range(r)])
    return cols


def uniform_bank(rng, Fd, r, M):
    p = Fd.p
    from sss import rank
    while True:
        cols = [[rng.randrange(p) for _ in range(r)] for _ in range(M)]
        if rank(cols[:3 * r], p)[0] == r:
            return cols


def ec_copies_bank(rng, Fd, J, L, M):
    """EC circuits + generic B, padded with proportional copies c*lambda of B and circuit
    columns, with -c not in P (so no copy pair is a monochromatic exact relation, i.e. no
    direct solution of size 2).  Every padding column lies on a line already in the bank."""
    p = Fd.p
    cols = ec_bank(rng, Fd, J, L, 0)
    base = len(cols)
    bad_c = [c for c in range(1, p) if Fd.cls(-c % p) != 0]
    while len(cols) < M:
        v = cols[rng.randrange(base)]
        c = rng.choice(bad_c)
        cols.append([c * t % p for t in v])
    return cols
