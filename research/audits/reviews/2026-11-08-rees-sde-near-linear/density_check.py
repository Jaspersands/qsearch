"""Dead-weight density: exact solution counts for small banks.
(i) kappa in {2,3,4}, a=1: every bank of 3 columns has a nonzero (P u 0)-solution for p
    large (exhaustive over all banks up to scaling, p moderate) -> dead weight has <= 2
    columns per dimension in a=1.
(ii) kappa=3, a=2: M=4 dead-pair bank has no solution; M=5 = 2a+1 (< kappa*a+1 = 7)
    random and structured banks: count nonzero solutions in (P u 0)^5 exactly.
"""
import random, itertools
from reduction_check import is_prime, gen, cos_table

def P0set(p, cos):
    return [y for y in range(p) if y == 0 or cos[y] == 0]

def a1_all_triples(p, kappa):
    g = gen(p); cos = cos_table(p, kappa, g); P0 = P0set(p, cos)
    S = set(P0)
    # bank (1, c2, c3) up to scaling and permutation; c's nonzero (a zero column is a trivial solution)
    worst = None; fails = []
    for c2 in range(1, p):
        for c3 in range(c2, p):
            # exists x in P0^3 nonzero with x1 + c2 x2 + c3 x3 = 0 ?
            found = False
            for x2 in P0:
                for x3 in P0:
                    if x2 == 0 and x3 == 0: continue
                    x1 = (-(c2*x2 + c3*x3)) % p
                    if x1 in S: found = True; break
                if found: break
            if not found: fails.append((1, c2, c3))
    return fails

def a1_pairs(p, kappa):
    g = gen(p); cos = cos_table(p, kappa, g); P0 = P0set(p, cos); S = set(P0)
    dead = 0
    for c in range(1, p):
        found = any(((-c*x2) % p) in S for x2 in P0 if x2 != 0)
        if not found: dead += 1
    return dead  # number of c with pair (1,c) dead; expect (kappa-1)(p-1)/kappa

def a2_count(p, kappa, cols, cos):
    """cols: list of 5 (or 4) vectors in F_p^2.  Count nonzero x in P0^M with sum x_i col_i = 0.
    Solve for x1,x2 from the last M-2 entries when cols[0],cols[1] independent."""
    import numpy as np
    P0 = np.array(P0set(p, cos), dtype=np.int64)
    ok = np.zeros(p, dtype=bool); ok[P0] = True
    M = len(cols)
    # reorder so that the first two columns are independent
    for i in range(M):
        for j in range(i+1, M):
            if (cols[i][0]*cols[j][1] - cols[i][1]*cols[j][0]) % p:
                cols = [cols[i], cols[j]] + [cols[t] for t in range(M) if t not in (i, j)]
                break
        else: continue
        break
    (a11, a21), (a12, a22) = cols[0], cols[1]
    det = (a11*a22 - a12*a21) % p
    assert det, "first two columns dependent"
    dinv = pow(det, p-2, p)
    rest = cols[2:]
    grids = np.meshgrid(*([P0]*(M-2)), indexing='ij')
    r1 = np.zeros_like(grids[0]); r2 = np.zeros_like(grids[0])
    for gq, (c1, c2) in zip(grids, rest):
        r1 = (r1 + c1*gq) % p; r2 = (r2 + c2*gq) % p
    # solve a11 x1 + a12 x2 = -r1 ; a21 x1 + a22 x2 = -r2
    x1 = ((-r1)*a22 - a12*(-r2)) % p * dinv % p
    x2 = (a11*(-r2) - a21*(-r1)) % p * dinv % p
    good = ok[x1] & ok[x2]
    nz = np.zeros_like(good)
    for gq in grids: nz |= (gq != 0)
    nz |= (x1 != 0) | (x2 != 0)
    return int(np.count_nonzero(good & nz))

def main():
    rng = random.Random(7)
    print("(i) a=1, three nonzero columns, exhaustive over banks:")
    for kappa, p in [(2, 101), (2, 109), (3, 103), (3, 109), (4, 101), (4, 109), (6, 103)]:
        assert is_prime(p) and (p-1) % kappa == 0
        fails = a1_all_triples(p, kappa)
        print(f"  kappa={kappa} p={p}: banks (1,c2,c3) with NO nonzero P0-solution: {len(fails)} of {(p-1)*p//2} ; dead pairs (1,c): {a1_pairs(p,kappa)} (expected {(kappa-1)*(p-1)//kappa})")
    print("(ii) kappa=3, a=2: exact counts of nonzero P0-solutions")
    for p in [1009, 1033]:
        g = gen(p); cos = cos_table(p, 3, g)
        c = next(x for x in range(2, p) if cos[(-x) % p] != 0)   # -c not in P
        dead4 = [(1, 0), (c, 0), (0, 1), (0, c)]
        print(f"  p={p}: dead-pair bank M=4 count = {a2_count(p, 3, dead4, cos)}")
        counts = []
        for t in range(60):
            cols = []
            while True:
                cols = [(rng.randrange(1, p), rng.randrange(1, p)) for _ in range(5)]
                if (cols[0][0]*cols[1][1] - cols[0][1]*cols[1][0]) % p: break
            counts.append(a2_count(p, 3, cols, cos))
        print(f"  p={p}: 60 random banks M=5: min={min(counts)} median={sorted(counts)[30]} max={max(counts)}  (heuristic p^3/27 = {p**3//27})")
        # structured: two dead pairs plus one extra column; proportional triple; column in P-span
        structs = {
          "dead pairs + generic": [(1, 0), (c, 0), (0, 1), (0, c), (rng.randrange(1,p), rng.randrange(1,p))],
          "dead pairs + (1,1)": [(1, 0), (c, 0), (0, 1), (0, c), (1, 1)],
          "dead pairs + (1,c)": [(1, 0), (c, 0), (0, 1), (0, c), (1, c)],
          "dead pairs + (c,c)": [(1, 0), (c, 0), (0, 1), (0, c), (c, c)],
          "dead pairs + (c^2,c)": [(1, 0), (c, 0), (0, 1), (0, c), (c*c % p, c)],
          "proportional triple": [(1, 0), (0, 1), (1, 1), (c, c), (c*c % p, c*c % p)],
          "4 proportional": [(1, 0), (0, 1), (1, 1), (c, c), (c*c % p, c*c % p)][:2] + [(1,1),(c,c),(c*c%p,c*c%p)],
        }
        for name, cols in structs.items():
            print(f"  p={p}: {name}: count = {a2_count(p, 3, cols, cos)}")

if __name__ == "__main__":
    main()
