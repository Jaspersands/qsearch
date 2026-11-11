r"""Check the counting identity and the error bound behind Theorem E.

For a bank T of n columns spanning F_p^d:
  N := #{y in F_p^n : sum_i y_i^kappa lambda_i = 0}
     = p^{-d} sum_{u in F_p^d} prod_i S(<u, lambda_i>),   S(c) = sum_y e_p(c y^kappa)   (identity)
  |N - p^{n-d}| <= p^{n-d} * sum_{T' subset T, rk T' < d} (kappa-1)^{|T \ T'|} p^{(d - rk T') - |T \ T'|/2}
                                                                                   (bound used in Theorem E)
N is computed independently from the kernel (projective points with one coset class).
Run: /opt/anaconda3/bin/python -I count_check.py
"""
import itertools
import random
import sys
import numpy as np

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdecore import coset_table, rank_mod, solutions_proj  # noqa: E402


def N_from_kernel(cols, p, kap, cos):
    sols = solutions_proj(cols, p, cos)
    supp = (sols != 0).sum(axis=1)
    return 1 + int(sum(((p - 1) // kap) * kap ** int(s) for s in supp))


def N_from_chars(cols, p, kap):
    y = np.arange(p)
    yk = np.array([pow(int(v), kap, p) for v in y])
    S = np.array([np.exp(2j * np.pi * (c * yk % p) / p).sum() for c in range(p)])
    d = len(cols[0])
    U = np.array(list(itertools.product(range(p), repeat=d)), dtype=np.int64)
    L = np.array(cols, dtype=np.int64)  # n x d
    ip = (U @ L.T) % p  # |U| x n
    tot = np.prod(S[ip], axis=1).sum() / p ** d
    return tot


def bound(cols, p, kap):
    n, d = len(cols), len(cols[0])
    tot = 0.0
    for r in range(n + 1):
        for Tp in itertools.combinations(range(n), r):
            rk = rank_mod([cols[i] for i in Tp], p) if Tp else 0
            if rk < d:
                m, c = n - r, d - rk
                tot += (kap - 1) ** m * p ** (c - m / 2)
    return tot  # relative to p^{n-d}


def main():
    rng = random.Random(20261111)
    print("kappa p d n kind  N_kernel  N_chars(real,imag)  p^(n-d)  |N-p^(n-d)|/p^(n-d)  bound  ok")
    bad = 0
    cases = []
    for kap, plist in [(3, [13, 31, 61]), (4, [13, 29, 53]), (6, [13, 31, 61])]:
        for p in plist:
            g, cos = coset_table(p, kap)
            nonP = g  # g is not a kappa-th power
            for d, n in [(1, 3), (1, 4), (2, 5), (2, 6)]:
                if d == 2 and n == 6 and p > 31:
                    continue
                for kind in ["random", "pairs+", "repeat"]:
                    if kind == "random":
                        cols = [[rng.randrange(p) for _ in range(d)] for _ in range(n)]
                        if any(all(v == 0 for v in c) for c in cols):
                            continue
                    elif kind == "pairs+":
                        # d dead pairs (mu, c mu) with -c not in P, then extra random columns
                        c = (-nonP) % p  # -c = nonP not in P
                        cols = []
                        for j in range(d):
                            e = [0] * d
                            e[j] = 1
                            cols += [e, [c * v % p for v in e]]
                        while len(cols) < n:
                            cols.append([rng.randrange(1, p) for _ in range(d)])
                    else:
                        base = [rng.randrange(1, p) for _ in range(d)]
                        cols = [[base[i] * pow(nonP, j, p) % p for i in range(d)] for j in range(n - d + 1)]
                        while len(cols) < n:
                            cols.append([rng.randrange(1, p) for _ in range(d)])
                    if rank_mod(cols, p) < d:
                        continue
                    Nk = N_from_kernel(cols, p, kap, cos)
                    Nc = N_from_chars(cols, p, kap)
                    main_t = p ** (n - d)
                    rel = abs(Nk - main_t) / main_t
                    b = bound(cols, p, kap)
                    ok = abs(Nc.real - Nk) < 1e-6 * max(1, Nk) and abs(Nc.imag) < 1e-6 * max(1, Nk) and rel <= b + 1e-12
                    bad += (not ok)
                    print(kap, p, d, n, kind, Nk, f"{Nc.real:.3f},{Nc.imag:.1e}", main_t, f"{rel:.4f}", f"{b:.4f}", ok)
    print("failures:", bad)


if __name__ == "__main__":
    main()
