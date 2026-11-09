"""Tower checker: independent re-check of the exact witnesses of
2026-11-05-rees-threshold-6/ and of the 'uncovered prime' claims.

Witness lines: "p FEASIBLE g=G beta b_(R in order) alpha a_0 .. a_(D-1)".
Classes are computed here by exponentiation with xi = G; G is first checked to
generate F_p^x / (F_p^x)^D. Shares no code with that folder's verify.py.
"""
import sys
import random
import itertools
import numpy as np
from sympy import isprime, primefactors

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from tower_check import Field, Finder, check_rc  # noqa: E402

SRC = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-05-rees-threshold-6/"


def classer(p, g, D):
    assert isprime(p) and (p - 1) % D == 0
    for q in primefactors(D):
        assert pow(g, (p - 1) // q, p) != 1, "g is not a coset generator"
    z = pow(g, (p - 1) // D, p)
    tab = {pow(z, m, p): m for m in range(D)}
    return lambda x: tab[pow(x % p, (p - 1) // D, p)]


def check_line(line, D, R, K):
    f = line.split()
    p = int(f[0])
    assert f[1] == "FEASIBLE"
    g = int(f[2].split("=")[1])
    bi = f.index("beta")
    ai = f.index("alpha")
    beta = [int(x) for x in f[bi + 1:ai]]
    alpha = [int(x) for x in f[ai + 1:ai + 1 + D]]
    assert len(beta) == len(R) and len(alpha) == D, line
    cl = classer(p, g, D)
    b = dict(zip(R, beta))
    v00 = (alpha[0] + b[0]) % p
    if v00 == 0 or cl(v00) != 0:
        return p, False
    for i in R:
        for j in range(D):
            v = (alpha[j] + b[i]) % p
            if v and cl(v) not in {(k - i - j) % D for k in K}:
                return p, False
    return p, True


def check_file(name, D, R, K, sample=None, seed=1):
    lines = [l for l in open(SRC + name) if " FEASIBLE" in l and "INFEASIBLE" not in l]
    if sample and len(lines) > sample:
        lines = random.Random(seed).sample(lines, sample)
    bad = [p for p, ok in (check_line(l, D, R, K) for l in lines) if not ok]
    print(f"{name}: D={D} R={R} K={K}: checked {len(lines)} witnesses, bad={bad}", flush=True)
    return bad


def witnesses():
    jobs = [
        ("rc_4_2.out", 4, [0, 2], [0], None),
        ("rc_6_3.out", 6, [0, 3], [0], None),
        ("rc_6_2.out", 6, [0, 2, 4], [0], None),
        ("rc_6_2b.out", 6, [0, 2, 4], [0], None),
        ("rc_8_4.out", 8, [0, 4], [0], None),
        ("rc_8_2_lo.out", 8, [0, 2, 4, 6], [0], None),
        ("rc_8_2_mid.out", 8, [0, 2, 4, 6], [0], None),
        ("rc_8_2_hi.out", 8, [0, 2, 4, 6], [0], 400),
        ("rc_9_3_low.out", 9, [0, 3, 6], [0], None),
        ("rc_9_3_hi.out", 9, [0, 3, 6], [0], 400),
        ("rc_16_8.out", 16, [0, 8], [0], None),
        ("u5_step1_lo.out", 5, list(range(5)), [0, 1], None),
        ("u5_step1_hi.out", 5, list(range(5)), [0, 1], 400),
        ("u5_step2.out", 5, [0, 1], [0], None),
        ("u7_step2A_lo.out", 7, [0, 1, 2, 3], [0], None),
        ("u7_step2A_hi.out", 7, [0, 1, 2, 3], [0], 400),
        ("u7_step1A_lo.out", 7, list(range(7)), [0, 1, 2, 3], None),
        ("u7_step1A_hi.out", 7, list(range(7)), [0, 1, 2, 3], 1000),
    ]
    import glob, os
    for f in sorted(glob.glob(SRC + "uw_k*_s1.out")):
        n = os.path.basename(f)
        k = int(n.split("_")[1][1:])
        K = [int(x) for x in n.split("_K")[1].split("_s1")[0].split("-")]
        jobs.append((n, k, list(range(k)), K, None))
        jobs.append((n.replace("_s1", "_s2"), k, K, [0], None))
    allbad = []
    for name, D, R, K, s in jobs:
        allbad += check_file(name, D, R, K, s)
    print("TOTAL bad:", allbad)


def step1_dfs(fd, D, K):
    """Complete decision of RC(D; Z_D -> K) (rows Z_D), beta_0 = 0, DFS over beta_1..beta_{D-1}
    with the column-wise prune: every column j must keep an admissible x."""
    p = fd.F.p
    xs = fd.xs
    masks0 = [fd.okmask(D, 0, j, K, xs) for j in range(D)]
    # rowmask[i][j] as a function of y: precompute boolean over y
    rowok = {i: [fd.okmask(D, i, j, K, xs) for j in range(D)] for i in range(1, D)}
    nodes = [0]

    def rec(i, cur):
        nodes[0] += 1
        if i == D:
            return True
        for b in range(p):
            new = []
            for j in range(D):
                m = cur[j] & np.roll(rowok[i][j], -b)  # rowok[x+b]
                if not m.any():
                    break
                new.append(m)
            else:
                if rec(i + 1, new):
                    return True
        return False

    return rec(1, masks0), nodes[0]


def uncovered():
    """For each claimed uncovered prime: for every K with 0 in K, |K| in {2,3}, the union
    chain Z_k -> K -> {0} fails (step 2 by complete FFT search, else step 1 by complete DFS)."""
    claims = {4: [5, 13], 5: [11], 6: [7, 13, 19, 31, 43, 67], 8: [17, 41, 73, 89, 137, 233],
              9: [19, 37, 73, 109, 127, 163, 181, 199, 307, 433], 7: [29, 43, 71, 113]}
    which = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else sorted(claims)
    for k in which:
        for p in claims[k]:
            F = Field(p, k)
            fd = Finder(F)
            res = []
            for size in (2, 3):
                for rest in itertools.combinations(range(1, k), size - 1):
                    K = [0] + list(rest)
                    s2 = fd.complete_search(k, K, [0])
                    if s2 is not None:
                        assert check_rc(F, k, K, [0], *s2)
                        if p ** (k - 1) <= 2e6 or True:
                            ok1, nodes = step1_dfs(fd, k, K)
                        res.append((tuple(K), "step2 feasible", "step1 " + ("FEASIBLE" if ok1 else "infeasible") + f" ({nodes} nodes)"))
                    else:
                        res.append((tuple(K), "step2 infeasible"))
            covered = [r for r in res if len(r) == 3 and "FEASIBLE" in r[2]]
            n2 = sum(1 for r in res if len(r) == 2)
            print(f"kappa={k} p={p}: {len(res)} K's; step2 infeasible for {n2}; "
                  f"step2-feasible K's: {[r for r in res if len(r) == 3]}; covered={bool(covered)}", flush=True)


if __name__ == "__main__":
    {"witnesses": witnesses, "uncovered": uncovered}[sys.argv[1]]()
