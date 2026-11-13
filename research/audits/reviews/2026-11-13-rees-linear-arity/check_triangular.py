"""Sanity checks (exact arithmetic) for this note.

(T) triangular solver with the explicit kappa in {2,3} contractions on (a+1)(a+2)/2 columns:
    random, low-rank, repeated/proportional, dead-pair-padded and zero-heavy banks,
    every prime p <= 101 with kappa | p-1, every a <= 6; every output re-verified.
(D) dead pairs: a dead pairs (2a columns) have no solution (brute force, small p, a <= 3),
    and every bank of 2a+1 columns at kappa = 2 has one (Chevalley-Warning; exhaustive at tiny p, a).
(C) Lemma C (collision = solution for P u -P): brute force on random tiny banks.
Usage: python check_triangular.py SEED
"""
import itertools
import random
import sys

from sdelib import (Field, brute_solvable, combo, dead_pair_bank, explicit_contraction,
                    is_prime, is_solution, kernel, random_bank, triangular_solve)


def banks(F, a, n, rng):
    p = F.p
    yield "random", random_bank(p, a, n, rng)
    # low rank: columns in a random subspace of dim r < a
    r = max(1, a - 2)
    B = random_bank(p, a, r, rng)
    cols = []
    for _ in range(n):
        c = [rng.randrange(p) for _ in range(r)]
        cols.append(combo(B, c, p))
    yield "lowrank", cols
    # proportional / repeated: few base columns, scaled by non-P elements
    base = random_bank(p, a, a + 1, rng)
    nonP = [y for y in range(1, p) if not F.inP0(y)]
    cols = [[t * rng.choice(nonP) % p for t in rng.choice(base)] for _ in range(n)]
    yield "proportional", cols
    # dead pairs first (they absorb the first round budget), then random filler
    dp = dead_pair_bank(F, a)
    cols = dp + random_bank(p, a, n - len(dp), rng) if n > len(dp) else dp[:n]
    yield "deadpairs+fill", cols
    # many zero columns mixed in (a zero column is itself a solution)
    cols = random_bank(p, a, n, rng)
    for i in rng.sample(range(n), min(n, 2)):
        cols[i] = [0] * a
    yield "zeros", cols
    # sparse columns (unit vectors times random scalars)
    cols = []
    for _ in range(n):
        e = [0] * a
        e[rng.randrange(a)] = rng.randrange(1, p)
        cols.append(e)
    yield "sparse", cols


def check_T(rng):
    tot = fails = 0
    per = {}
    for p in range(3, 102):
        if not is_prime(p):
            continue
        for k in (2, 3):
            if (p - 1) % k:
                continue
            F = Field(p, k)
            ab = explicit_contraction(F)
            for a in range(1, 7):
                n = (a + 1) * (a + 2) // 2
                for rep in range(4):
                    for name, cols in banks(F, a, n, rng):
                        x = triangular_solve(F, cols, *ab)
                        ok = is_solution(F, cols, x)
                        tot += 1
                        per[(k, name)] = per.get((k, name), 0) + 1
                        if not ok:
                            fails += 1
                            print("FAIL", p, k, a, name)
    print(f"(T) triangular runs: {tot}, failures: {fails}")
    for key in sorted(per):
        print(f"    kappa={key[0]} {key[1]:15s} {per[key]}")


def check_D():
    out = []
    for p in (3, 5, 7, 11, 13):
        F = Field(p, 2)
        for a in (1, 2, 3):
            if p ** (a) > 3000:
                continue
            cols = dead_pair_bank(F, a)
            out.append((p, a, brute_solvable(F, cols) is None))
    print("(D) dead-pair banks of 2a columns unsolvable (p, a, True=unsolvable):", out)
    # exhaustive: every bank of 2a+1 = 3 columns in F_p^1 solvable at kappa=2, p <= 13
    allok = True
    for p in (3, 5, 7, 11, 13):
        F = Field(p, 2)
        for cols in itertools.product(range(p), repeat=3):
            if brute_solvable(F, [[c] for c in cols]) is None and any(cols):
                # all-zero bank aside, kernel always nonempty for 3 cols in F_p^1
                allok = False
                print("  unsolvable 3-bank", p, cols)
    print("(D) every 3-column bank in F_p^1 (kappa=2, p<=13) solvable:", allok)
    # a = 2, 5 columns, p = 5, 7: random sample of 3000 banks each
    rng = random.Random(7)
    allok = True
    for p in (5, 7, 11):
        F = Field(p, 2)
        for _ in range(3000):
            cols = random_bank(p, 2, 5, rng)
            if brute_solvable(F, cols) is None:
                allok = False
    print("(D) 3000 random 5-column banks in F_p^2, p in {5,7,11}, all solvable:", allok)


def collision_bruteforce(F, cols):
    """Exists disjoint I != {}, J and P-weights with sum_I w v = sum_J w v (J may be empty)."""
    p, n = F.p, len(cols)
    Pm = set(F.P) | {(-y) % p for y in F.P}
    ker = kernel(cols, p)
    for coef in itertools.product(range(p), repeat=len(ker)):
        if not any(coef):
            continue
        x = [sum(c * y[i] for c, y in zip(coef, ker)) % p for i in range(n)]
        if all(xi == 0 or xi in Pm for xi in x):
            return True
    return False


def check_C(rng):
    agree = tot = 0
    for p in (7, 11, 13, 19, 29):
        for k in (2, 3, 4, 6):
            if (p - 1) % k:
                continue
            F = Field(p, k)
            for _ in range(60):
                a = rng.choice((1, 2))
                n = rng.choice((a + 1, a + 2, 2 * a + 1))
                cols = random_bank(p, a, n, rng)
                if len(kernel(cols, p)) > 3:
                    continue
                c1 = collision_bruteforce(F, cols)
                # solution problem for P' = P u -P, i.e. kappa' = kappa if -1 in P else kappa/2
                kp = k if (-1) % p in F.Pset else k // 2
                Fp_ = Field(p, kp)
                c2 = brute_solvable(Fp_, cols) is not None
                tot += 1
                agree += (c1 == c2)
    print(f"(C) collision(kappa) == solvable(kappa'): {agree}/{tot}")


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    check_T(rng)
    check_D()
    check_C(rng)


if __name__ == "__main__":
    main()
