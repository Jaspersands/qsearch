"""Structured bank families (arbitrary banks, not general position)."""
import random


def rvec(rng, p, a):
    return [rng.randrange(p) for _ in range(a)]


def comb(rng, p, basis, a):
    co = [rng.randrange(1, p) for _ in basis]
    return [sum(c * v[t] for c, v in zip(co, basis)) % p for t in range(a)]


def scal(rng, p, v):
    c = rng.randrange(1, p)
    return [c * x % p for x in v]


def lines(rng, p, a, M, m):
    vs = [rvec(rng, p, a) for _ in range(m)]
    return [scal(rng, p, vs[i % m]) for i in range(M)]


def pairs_nr(rng, p, a, M, nr):
    """parallel pairs with ratio -nr (no 2-term solution), plus generic columns."""
    cols = []
    while len(cols) + 2 <= M:
        v = rvec(rng, p, a)
        c = rng.randrange(1, p)
        cols.append([c * x % p for x in v])
        cols.append([(-c * nr) * x % p for x in v])
    while len(cols) < M:
        cols.append(rvec(rng, p, a))
    return cols


def subspace(rng, p, a, M, y, frac):
    Y = [rvec(rng, p, a) for _ in range(y)]
    cols = [comb(rng, p, Y, a) if i < int(frac * M) else rvec(rng, p, a) for i in range(M)]
    rng.shuffle(cols)
    return cols


def chain(rng, p, a, M, dims, counts):
    """nested flats F_1 < F_2 < ... with counts[i] columns in F_i (generic there)."""
    basis = [rvec(rng, p, a) for _ in range(a)]
    cols = []
    for d, c in zip(dims, counts):
        cols += [comb(rng, p, basis[:d], a) for _ in range(c)]
    while len(cols) < M:
        cols.append(comb(rng, p, basis, a))
    return cols[:M]


def flats(rng, p, a, M, nflat, dim, per):
    """nflat random dim-flats with per columns each, rest generic."""
    cols = []
    for _ in range(nflat):
        F = [rvec(rng, p, a) for _ in range(dim)]
        cols += [comb(rng, p, F, a) for _ in range(per)]
    while len(cols) < M:
        cols.append(rvec(rng, p, a))
    return cols[:M]


def hyper_plus(rng, p, a, M, out):
    """a hyperplane holding M-out columns (generic in it), out columns outside."""
    H = [rvec(rng, p, a) for _ in range(a - 1)]
    cols = [comb(rng, p, H, a) for _ in range(M - out)] + [rvec(rng, p, a) for _ in range(out)]
    return cols


def sparse(rng, p, a, M):
    cols = []
    for _ in range(M):
        v = [0] * a
        for t in rng.sample(range(a), rng.choice([1, 2])):
            v[t] = rng.choice([1, p - 1, 2, 3])
        cols.append(v)
    return cols


def small_entries(rng, p, a, M, pal):
    return [[rng.choice(pal) % p for _ in range(a)] for _ in range(M)]


def flag01(rng, p, a, M):
    cols = []
    for _ in range(M):
        d = min(a, 1 + int(rng.expovariate(0.6)))
        cols.append([rng.randrange(p) if t < d else 0 for t in range(a)])
    return cols


def family_list(rng, p, a, M, nr):
    return {
        "lines_a+1": lambda: lines(rng, p, a, M, a + 1),
        "lines_a+2": lambda: lines(rng, p, a, M, a + 2),
        "pairs_nr": lambda: pairs_nr(rng, p, a, M, nr),
        "subsp_a-1": lambda: subspace(rng, p, a, M, a - 1, 0.8),
        "subsp_half": lambda: subspace(rng, p, a, M, max(1, a // 2), 0.6),
        "chain": lambda: chain(rng, p, a, M, list(range(1, a + 1)), [rng.randrange(1, 4) for _ in range(a)]),
        "flats2": lambda: flats(rng, p, a, M, M // 4, 2, 4),
        "flats3": lambda: flats(rng, p, a, M, M // 6, 3, 6),
        "hyper_plus_half": lambda: hyper_plus(rng, p, a, M, a // 2 + 2),
        "sparse": lambda: sparse(rng, p, a, M),
        "small012": lambda: small_entries(rng, p, a, M, [0, 1, 2, -1, -2]),
        "flag01": lambda: flag01(rng, p, a, M),
    }
