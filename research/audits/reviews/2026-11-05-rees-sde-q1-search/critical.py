"""Explicit constructions of the critical stall of the worst-case report §6:
q = 1, |B \\ U_L| = 1, no unused column, on the identity order.

chain4(r): B = b_1..b_r first.  Round l (l = 1..m) is a 4-circuit
      c_k, c_l, c_i, c_new   with   delta = (d_k, d_l, d_i, 1),
   cls(d_i) = 0, cls(d_k) = cls(d_l) = 1, c_i, c_new in span(b_{2l-1}, b_{2l}).
   The class-0 pair {c_i, c_new} is the largest class group (tie broken to class 0), so
   split_blocks cuts it into two singletons for every random cut and U_l = U_{l-1} +
   span(b_{2l-1}, b_{2l}) deterministically.  For even r the last gain-1 round is a
   proportional-mod-U pair inside span(U, b_{r-1}).  Then `npool` generic columns of
   span(b_1..b_{r-1}) follow; they are all true-pool events.  With
   npool = M - r - (rounds) the identity order ends in the critical stall.

chainfull(r) (kappa = 3 only): the same with FULL circuits mod U (cost q+1), whose
   three class groups are the blocks (no split): groups' sums are steered so that
   U_l = U_{l-1} + span(b_{2l-1}, b_{2l}).  This minimises the pool: pi = 2 for odd r.
"""
import random
from q1lib import rvec, comb, D3


def lin(p, *terms):
    a = len(terms[0][1])
    return [sum(c * v[t] for c, v in terms) % p for t in range(a)]


def pick(Fd, rng, cl):
    while True:
        y = rng.randrange(1, Fd.p)
        if Fd.cls(y) == cl:
            return y


def chain4(Fd, rng, a, M, outside_generic=True):
    p = Fd.p
    r = a
    b = [rvec(rng, p, a) for _ in range(r)]
    cols = list(b)
    m = (r - 1) // 2
    inv = lambda y: pow(y, p - 2, p)
    for l in range(m):
        P1, P2 = b[2 * l], b[2 * l + 1]
        ci = comb(rng, p, [P1, P2], a)
        cnew = comb(rng, p, [P1, P2], a)
        di = pick(Fd, rng, 0)
        dk = pick(Fd, rng, 1)
        dl = pick(Fd, rng, 1)
        ck = rvec(rng, p, a)
        # dk ck + dl cl + di ci + cnew = 0
        s = lin(p, (dk, ck), (di, ci), (1, cnew))
        cl_ = [(-v) * inv(dl) % p for v in s]
        cols += [ck, cl_, ci, cnew]
    if r % 2 == 0:
        # gain-1 round: c, c' with c' = mu c + u, u in U, both in span(U, b_{r-1})
        Ub = b[:r - 2]
        c = lin(p, (1, b[r - 2]), *[(rng.randrange(p), v) for v in Ub]) if Ub else list(b[r - 2])
        u = comb(rng, p, Ub, a) if Ub else [0] * a
        mu = rng.randrange(1, p)
        c2 = [(mu * x + y) % p for x, y in zip(c, u)]
        cols += [c, c2]
    span_UL = b[:r - 1]
    while len(cols) < M:
        cols.append(comb(rng, p, span_UL, a))
    return cols[:M]


def chainfull(Fd, rng, a, M):
    """kappa = 3: full circuits mod U, blocks = the three class groups."""
    p = Fd.p
    assert Fd.k == 3
    r = a
    b = [rvec(rng, p, a) for _ in range(r)]
    cols = list(b)
    inv = lambda y: pow(y, p - 2, p)
    q, l = r, 0
    Ub = []
    while q > 1:
        if q >= 3:
            # circuit of size q+1 mod U: q columns T independent mod U, plus c_new.
            # groups: G1 (class 1) sums to b_{2l+1}+u1, G2 (class 2) sums to b_{2l+2}+u2,
            # G0 (class 0, contains c_new) sums to -(those) + e, e = 0.
            k = q
            n1 = (k + 1) // 3
            n2 = (k + 1) // 3
            n0 = k + 1 - n1 - n2
            T = []
            # free generic columns (they keep T independent mod U)
            sizes = [n1, n2, n0]
            targets = [b[2 * l], b[2 * l + 1]]
            grp = []
            for g, n in enumerate(sizes):
                cl = [1, 2, 0][g]
                ds = [pick(Fd, rng, cl) for _ in range(n)]
                if g == 2:
                    ds[-1] = 1  # c_new has delta 1
                vs = [rvec(rng, p, a) for _ in range(n)]
                grp.append((ds, vs))
            # fix the last member of groups 0,1 so that group sums are the targets
            for g in range(2):
                ds, vs = grp[g]
                rest = lin(p, *[(d, v) for d, v in zip(ds[:-1], vs[:-1])]) if len(ds) > 1 else [0] * a
                vs[-1] = [(t - x) * inv(ds[-1]) % p for t, x in zip(targets[g], rest)]
            # group 0: sum = -(b1 + b2); fix c_new (delta 1)
            ds, vs = grp[2]
            rest = lin(p, *[(d, v) for d, v in zip(ds[:-1], vs[:-1])]) if len(ds) > 1 else [0] * a
            vs[-1] = [(-(t1 + t2) - x) % p for t1, t2, x in zip(targets[0], targets[1], rest)]
            order = grp[0][1] + grp[1][1] + grp[2][1][:-1] + [grp[2][1][-1]]
            cols += order
            Ub += targets
            q -= 2
            l += 1
        else:  # q == 2: gain-1 pair inside span(U, b_{r-1})
            c = lin(p, (1, b[r - 2]), *[(rng.randrange(p), v) for v in Ub])
            u = comb(rng, p, Ub, a)
            mu = rng.randrange(1, p)
            cols += [c, [(mu * x + y) % p for x, y in zip(c, u)]]
            q -= 1
    span_UL = b[:r - 1]
    while len(cols) < M:
        cols.append(comb(rng, p, span_UL, a))
    return cols[:M]
