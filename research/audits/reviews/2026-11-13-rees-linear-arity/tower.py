"""Lemma D (coset-doubling tower): a law-free kappa-solver of arity (a+1)^(m+1) built from
m binary refinements of coset unions, A_{j+1} = A_j u (A_j + e_j), A_1 = {0}, A_{m+1} = Z_kappa.

Level K = A_j (union of cosets C_nu, nu in A_j).  A K-solution: x != 0, sum x_i lam_i = 0,
every nonzero x_i in a coset of K.  A K-rep of v: disjoint support, K-weights, value v.
Refinement K' = K u (K+e) -> K: run the K'-solver on a+1 disjoint blocks; each block gives a
K-solution (done) or u with K-reps of u and of c*u, c = -g^{-e}; then F1: Gaussian elimination
on the a+1 vectors u_nu and eta = y1 + c*y2 with y in P0 (two-term), scaling reps by P0.

Usage:
  python tower.py coverage KMAX PMAX     # exact minimal number of levels m*(p,kappa), table
  python tower.py run SEED               # run the solver on random/structured banks
"""
import random
import sys

from sdelib import (Field, combo, is_prime, is_solution, kernel, random_bank, vadd, vscale)


def good_table(F):
    """good[nu] = (P0 + g^nu P0 contains F_p^*), plus a decomposition table."""
    p, k = F.p, F.k
    good, dec = [], []
    for nu in range(k):
        c = F.coset_elt(nu)
        table = {}
        for y1 in F.P0:
            for y2 in F.P0:
                t = (y1 + c * y2) % p
                if t and t not in table:
                    table[t] = (y1, y2)
        good.append(len(table) == p - 1)
        dec.append(table)
    return good, dec


def fast_good(F):
    """good[nu] via P-invariance: (P0 + cP0)\\0 = P*{1 + c z : z in P0} u cP, c = g^nu."""
    p, k = F.p, F.k
    good = []
    for nu in range(k):
        c = F.coset_elt(nu)
        cov = {nu}
        for z in F.P0:
            t = (1 + c * z) % p
            if t:
                cov.add(F.cos(t))
        good.append(len(cov) == k)
    return good


def min_levels(F, good):
    """BFS over coset unions A (bitmasks) from {0}: step A -> A u (A+e) allowed iff
    good[cos(-1) - e] (object type (1, c), c = -g^{-e}, needs P0 + c P0 = F^*)."""
    k = F.k
    full = (1 << k) - 1
    c1 = F.cos(F.p - 1)
    shift = lambda A, e: sum(1 << ((i + e) % k) for i in range(k) if A >> i & 1)
    start = 1
    dist = {start: 0}
    frontier = [start]
    while frontier:
        nxt = []
        for A in frontier:
            if A == full:
                return dist[A], None
            for e in range(1, k):
                if not good[(c1 - e) % k]:
                    continue
                B = A | shift(A, e)
                if B not in dist:
                    dist[B] = dist[A] + 1
                    nxt.append(B)
        frontier = nxt
    return None, None


def plan(F, good):
    """Return list of shifts e_1..e_m (greedy BFS path) reaching Z_kappa, or None."""
    k = F.k
    full = (1 << k) - 1
    c1 = F.cos(F.p - 1)
    shift = lambda A, e: sum(1 << ((i + e) % k) for i in range(k) if A >> i & 1)
    prev = {1: None}
    frontier = [1]
    while frontier:
        nxt = []
        for A in frontier:
            if A == full:
                path = []
                while prev[A] is not None:
                    A0, e = prev[A]
                    path.append(e)
                    A = A0
                return path[::-1]
            for e in range(1, k):
                if good[(c1 - e) % k]:
                    B = A | shift(A, e)
                    if B not in prev:
                        prev[B] = (A, e)
                        nxt.append(B)
        frontier = nxt
    return None


def in_union(F, y, A):
    return y % F.p == 0 or (A >> F.cos(y) & 1)


def solve_level(F, cols, idx, unions, shifts, level, dec):
    """Return a K-solution (dict index->weight) for K = unions[level] on columns idx.
    unions[level+1] = unions[level] u (unions[level] + shifts[level]); top level = Z_kappa."""
    p, k = F.p, F.k
    a = len(cols[0])
    if level == len(shifts):            # K = Z_kappa: linear algebra on a+1 columns
        S = [cols[i] for i in idx[:a + 1]]
        y = kernel(S, p)[0]
        return {idx[t]: y[t] for t in range(a + 1) if y[t]}
    K = unions[level]
    e = shifts[level]
    c = (-pow(F.coset_elt(e), -1, p)) % p          # c = -g^{-e}
    blk = len(idx) // (a + 1)
    objs = []
    for b in range(a + 1):
        sub = idx[b * blk:(b + 1) * blk]
        x = solve_level(F, cols, sub, unions, shifts, level + 1, dec)
        I = {i: w for i, w in x.items() if in_union(F, w, K)}
        J = {i: w for i, w in x.items() if i not in I}
        if not J:
            return I
        ge = F.coset_elt(e)
        Jp = {i: w * pow(ge, -1, p) % p for i, w in J.items()}   # J-weights / g^e  in K
        assert all(in_union(F, w, K) for w in Jp.values())
        if not I:
            return Jp
        u = combo([cols[i] for i in I], list(I.values()), p)
        # sum_I w lam + g^e sum_J w' lam = 0  ->  sum_J w' lam = -g^{-e} u = c u
        objs.append((u, I, Jp))
    U = [o[0] for o in objs]
    eta = kernel(U, p)[0]
    out = {}
    cn = F.cos(c)
    for (u, I, Jp), et in zip(objs, eta):
        if not et:
            continue
        y1, y2 = dec[cn][et]          # y1 + g^cn y2 = et
        y2 = y2 * F.coset_elt(cn) * pow(c, -1, p) % p   # rescale: y1 + c y2 = et, y2 in P0
        for i, w in I.items():
            if y1:
                out[i] = y1 * w % p
        for i, w in Jp.items():
            if y2:
                out[i] = y2 * w % p
    return out


def tower_solve(F, cols, shifts, dec):
    k, a = F.k, len(cols[0])
    unions = [1]
    for e in shifts:
        A = unions[-1]
        unions.append(A | sum(1 << ((i + e) % k) for i in range(k) if A >> i & 1))
    assert unions[-1] == (1 << k) - 1
    need = (a + 1) ** (len(shifts) + 1)
    assert len(cols) >= need
    x = solve_level(F, cols, list(range(need)), unions, shifts, 0, dec)
    full = [0] * len(cols)
    for i, w in x.items():
        full[i] = w
    return full


def coverage(kmax, pmax):
    print("kappa  p-range       primes  tower-ok  m*-histogram   (degree = m*+1; ceil(log2 k)+1 shown)")
    for k in range(2, kmax + 1):
        hist = {}
        bad = []
        cnt = 0
        top = min(pmax, 4 * k ** 4) if pmax > 0 else 4 * k ** 4
        for p in range(k + 1, top + 1):
            if not is_prime(p) or (p - 1) % k:
                continue
            cnt += 1
            F = Field(p, k)
            good = fast_good(F)
            if p < 3000:
                assert good == good_table(F)[0]
            m, _ = min_levels(F, good)
            hist[m] = hist.get(m, 0) + 1
            if m is None or m > (k - 1).bit_length():
                bad.append((p, m))
        lg = (k - 1).bit_length()
        print(f"{k:5d}  <= {top:<9d} {cnt:6d}  {hist}   ceil(log2)={lg}  "
              f"primes with m* > ceil(log2) or impossible: {len(bad)}; largest: {bad[-5:]}")


def run(seed):
    rng = random.Random(seed)
    cases = [(3, 7), (3, 13), (3, 331), (3, 337), (5, 11), (5, 31), (5, 2521), (7, 29), (7, 9661),
             (9, 19), (9, 37), (9, 26263), (4, 13), (4, 1009), (6, 1009), (8, 1009)]
    tot = bad = 0
    for k, p in cases:
        if not is_prime(p) or (p - 1) % k:
            print("skip", k, p)
            continue
        F = Field(p, k)
        good, dec = good_table(F)
        sh = plan(F, good)
        if sh is None:
            print(f"kappa={k} p={p}: no tower plan")
            continue
        for a in (1, 2, 3):
            need = (a + 1) ** (len(sh) + 1)
            if need > 400:
                continue
            for rep in range(6):
                if rep % 3 == 0:
                    cols = random_bank(p, a, need, rng)
                elif rep % 3 == 1:   # proportional-heavy bank
                    base = random_bank(p, a, a + 1, rng)
                    cols = [vscale(rng.choice(base), rng.randrange(1, p), p) for _ in range(need)]
                else:                # sparse bank
                    cols = []
                    for _ in range(need):
                        e = [0] * a
                        e[rng.randrange(a)] = rng.randrange(1, p)
                        cols.append(e)
                x = tower_solve(F, cols, sh, dec)
                ok = is_solution(F, cols, x)
                tot += 1
                bad += not ok
                if not ok:
                    print("FAIL", k, p, a, rep)
        print(f"kappa={k} p={p}: shifts={sh} degree={len(sh)+1}")
    print(f"tower runs {tot}, failures {bad}")


if __name__ == "__main__":
    if sys.argv[1] == "coverage":
        coverage(int(sys.argv[2]), int(sys.argv[3]))
    else:
        run(int(sys.argv[2]))
