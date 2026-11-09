"""Moebius helpers shared by pairsym.py (same formulas as sym_confs.py)."""


def mob_from(z, w, p=None):
    p = mob_from.p if p is None else p
    def h(z1, z2, z3):     # sends z1 -> 0, z2 -> inf, z3 -> 1
        return ((z3 - z2) % p, (-z1 * (z3 - z2)) % p, (z3 - z1) % p, (-z2 * (z3 - z1)) % p)
    A = h(*z); B = h(*w)
    a_, b_, c_, d_ = B; Bi = (d_, (-b_) % p, (-c_) % p, a_)
    m = lambda X, Y: ((X[0] * Y[0] + X[1] * Y[2]) % p, (X[0] * Y[1] + X[1] * Y[3]) % p,
                      (X[2] * Y[0] + X[3] * Y[2]) % p, (X[2] * Y[1] + X[3] * Y[3]) % p)
    return m(Bi, A)


def act_factory(p):
    mob_from.p = p
    inv = [0] + [pow(i, p - 2, p) for i in range(1, p)]
    INF = p
    def act(gm, pts):
        a_, b_, c_, d_ = gm; out = []
        for x in pts:
            if x == INF:
                out.append(INF if c_ == 0 else a_ * inv[c_] % p)
            else:
                den = (c_ * x + d_) % p
                out.append(INF if den == 0 else (a_ * x + b_) * inv[den] % p)
        return out
    return act
