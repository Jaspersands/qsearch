"""Structured / adversarial column families at the budget D_E(a)+a >= kappa*a+1 (so every
instance is solvable by Chevalley-Warning).  Compares plain SSS and recursive SSS."""
import random
import sys

from sss import Field, sss, sss_rec, budget


def rnd(rng, p, a):
    return [rng.randrange(p) for _ in range(a)]


def fam_lines(rng, p, a, M, m):
    vs = [rnd(rng, p, a) for _ in range(m)]
    cols = []
    for i in range(M):
        v = vs[i % m]
        c = rng.randrange(1, p)
        cols.append([c * t % p for t in v])
    return cols


def fam_subspace(rng, p, a, M, y, frac):
    Y = [rnd(rng, p, a) for _ in range(y)]
    cols = []
    for i in range(M):
        if i < int(frac * M):
            co = [rng.randrange(p) for _ in range(y)]
            cols.append([sum(c * Y[j][t] for j, c in enumerate(co)) % p for t in range(a)])
        else:
            cols.append(rnd(rng, p, a))
    rng.shuffle(cols)
    return cols


def fam_flag(rng, p, a, M):
    """nested subspaces: column i lies in span(e_1..e_{d_i}) with d_i small for many i."""
    cols = []
    for i in range(M):
        d = min(a, 1 + int(rng.expovariate(0.6)))
        cols.append([rng.randrange(p) if t < d else 0 for t in range(a)])
    return cols


def fam_sparse(rng, p, a, M):
    """columns with support <= 2 and coefficients in {1, -1, g}."""
    cols = []
    for i in range(M):
        v = [0] * a
        for t in rng.sample(range(a), rng.choice([1, 2])):
            v[t] = rng.choice([1, p - 1, 2, 3])
        cols.append(v)
    return cols


def main():
    rng = random.Random(7)
    E = 3
    for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
        Fd = Field(p, k)
        for a in ((3, 5, 7, 9) if k == 2 else (4, 6, 8)):
            M = budget(a, E)
            assert M >= k * a + 1
            fams = {
                "lines2": lambda: fam_lines(rng, p, a, M, 2),
                "lines_a": lambda: fam_lines(rng, p, a, M, a),
                "lines_a+1": lambda: fam_lines(rng, p, a, M, a + 1),
                "subsp_y1": lambda: fam_subspace(rng, p, a, M, 1, 0.5),
                "subsp_half": lambda: fam_subspace(rng, p, a, M, a // 2, 0.6),
                "subsp_a-1": lambda: fam_subspace(rng, p, a, M, a - 1, 0.8),
                "flag": lambda: fam_flag(rng, p, a, M),
                "sparse": lambda: fam_sparse(rng, p, a, M),
            }
            for name, gen in fams.items():
                plain, rec = {}, {}
                for trial in range(6):
                    cols = gen()
                    x, st = sss(Fd, cols, E, rng, passes=10, forwards=1)
                    plain[st.split("(")[0]] = plain.get(st.split("(")[0], 0) + 1
                    x2, st2 = sss_rec(Fd, cols, E, rng, passes=10)
                    rec[st2] = rec.get(st2, 0) + 1
                print(p, k, "a=%d M=%d" % (a, M), name, "plain", plain, "rec", rec, flush=True)


if __name__ == "__main__":
    main()
