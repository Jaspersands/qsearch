"""Referee checks, written independently of the report's scripts.

(1) Lemma K existence count: N(p) = #{b in C_1 : 1 + b in C_2} for every p = 1 mod 3 up to PMAX,
    for BOTH choices of the coset generator; compare with Gauss (p + 1 + L)/9; min N/(p-1).
    kappa = 2: the least non-residue nu has nu - 1 a nonzero square.
(2) Lemma D coverage: for kappa = 2..KMAX and every prime p = 1 mod kappa below 4 kappa^4,
    the set of good shifts e (P0 - g^{-e} P0 contains F_p^*) and the BFS minimum m* of
    {0} -> A u (A + e) -> ... -> Z_kappa. Prints the exceptions (m* != ceil(log2 kappa) or none).
(3) Lemma D solver: an independent implementation of the tower on random/adversarial banks.

Usage: /opt/anaconda3/bin/python ref_counts_tower.py PMAX KMAX
"""
import math
import random
import sys
from collections import deque

import numpy as np


def sieve(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return [int(x) for x in np.nonzero(s)[0]]


def prim_root(p):
    m, fac, q = p - 1, [], 2
    while q * q <= m:
        if m % q == 0:
            fac.append(q)
            while m % q == 0:
                m //= q
        q += 1
    if m > 1:
        fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in fac):
            return g
    return 1


def dlog_table(p):
    g = prim_root(p)
    log = np.full(p, -1, dtype=np.int64)
    pw = np.zeros(p - 1, dtype=np.int64)
    x = 1
    for k in range(p - 1):
        log[x] = k
        pw[k] = x
        x = x * g % p
    return g, log, pw


def gauss_L(p):
    for M in range(1, int(math.isqrt(4 * p // 27)) + 2):
        r = 4 * p - 27 * M * M
        if r < 0:
            break
        L = math.isqrt(r)
        if L * L == r:
            return L if L % 3 == 1 else -L
    return None


def part1(pmax):
    primes = sieve(pmax)
    bad, minr, n3 = [], (9, None), 0
    for p in primes:
        if p % 3 != 1:
            continue
        g, log, pw = dlog_table(p)
        b = np.arange(1, p - 1)  # b != p-1 so 1+b != 0
        lb, l1 = log[b] % 3, log[b + 1] % 3
        for s in (1, 2):  # generator g^s: cos = s^{-1} * log mod 3 = s * log mod 3
            N = int(np.sum(((s * lb) % 3 == 1) & ((s * l1) % 3 == 2)))
            if N < 1 or 9 * N != p + 1 + gauss_L(p):
                bad.append((p, s, N))
            if N / (p - 1) < minr[0]:
                minr = (N / (p - 1), p)
        n3 += 1
    bad2, n2 = [], 0
    for p in primes:
        if p == 2:
            continue
        nu = next(y for y in range(2, p) if pow(y, (p - 1) // 2, p) == p - 1)
        if pow(nu - 1, (p - 1) // 2, p) != 1:
            bad2.append(p)
        n2 += 1
    print(f"(1) kappa=3: {n3} primes p=1 mod 3 <= {pmax}, both generators; failures {bad[:5]} "
          f"(count {len(bad)}); min N/(p-1) = {minr[0]:.4f} at p = {minr[1]}")
    print(f"(1) kappa=2: {n2} odd primes <= {pmax}; least non-residue nu with nu-1 not a square: {bad2}")


def good_shifts(p, kappa, log, pw):
    h = (p - 1) // kappa
    isP0 = np.zeros(p, dtype=bool)
    isP0[0] = True
    isP0[pw[::kappa]] = True
    P0 = np.nonzero(isP0)[0]
    good = []
    for e in range(1, kappa):
        c = (-int(pw[(-e) % (p - 1)])) % p  # -g^{-e}
        ok = True
        for nu in range(kappa):
            eta = int(pw[nu])
            # eta = y1 + c y2 with y1, y2 in P0
            if not np.any(isP0[(eta - c * P0) % p]):
                ok = False
                break
        if ok:
            good.append(e)
    return good


def bfs_mstar(kappa, good):
    full = (1 << kappa) - 1
    start = 1
    dist = {start: 0}
    dq = deque([start])
    while dq:
        A = dq.popleft()
        if A == full:
            return dist[A]
        for e in good:
            sh = ((A << e) | (A >> (kappa - e))) & full
            B = A | sh
            if B not in dist:
                dist[B] = dist[A] + 1
                dq.append(B)
    return None


def part2(kmax):
    for kappa in range(2, kmax + 1):
        bound = 4 * kappa ** 4
        target = math.ceil(math.log2(kappa))
        exc, n = [], 0
        for p in sieve(bound - 1):
            if p % kappa != 1:
                continue
            g, log, pw = dlog_table(p)
            ms = bfs_mstar(kappa, good_shifts(p, kappa, log, pw))
            n += 1
            if ms != target:
                exc.append((p, None if ms is None else ms + 1))
        # sanity above the threshold: two primes >= 4 kappa^4, every shift must be good
        above = [q for q in sieve(bound + 4000) if q >= bound and q % kappa == 1][:2]
        allgood = all(len(good_shifts(q, kappa, *dlog_table(q)[1:])) == kappa - 1 for q in above)
        print(f"(2) kappa={kappa}: primes<4k^4 = {n}; doubling degree {target + 1}; exceptions (p, degree|None) "
              f"{exc}; all shifts good at {above}: {allgood}", flush=True)


# ---------- (3) Lemma D tower solver ----------

def kernel_vector(cols, p):
    n = len(cols)
    a = len(cols[0])
    M = [[cols[j][i] % p for j in range(n)] for i in range(a)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, a) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(a):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == a:
            break
    free = [c for c in range(n) if c not in piv]
    fc = free[0]
    x = [0] * n
    x[fc] = 1
    for i, c in enumerate(piv):
        x[c] = (-M[i][fc]) % p
    return x


class Tower:
    def __init__(self, p, kappa, shifts, rng):
        self.p, self.k, self.rng = p, kappa, rng
        self.g, self.log, self.pw = dlog_table(p)
        self.shifts = shifts
        A = {0}
        self.A = [None, frozenset(A)]
        for e in shifts:
            A = A | {(x + e) % kappa for x in A}
            self.A.append(frozenset(A))
        assert self.A[-1] == frozenset(range(kappa))
        self.m = len(shifts)

    def cos(self, y):
        return int(self.log[y % self.p]) % self.k

    def inP0(self, y):
        return y % self.p == 0 or self.cos(y) == 0

    def two_term(self, eta, c):
        # random draws, as in the Las Vegas step: y1 = u^kappa, y2 = (eta - y1)/c in P0
        p = self.p
        cinv = pow(c, p - 2, p)
        for _ in range(100000):
            u = self.rng.randrange(0, p)
            y1 = pow(u, self.k, p)
            y2 = (eta - y1) * cinv % p
            if self.inP0(y2) and (y1 or y2):
                return y1, y2
        raise RuntimeError("two-term draws exhausted")

    def solve(self, j, cols):
        """K_j-solution (list of weights) on cols, len(cols) = (a+1)^(m+2-j)."""
        p, a = self.p, len(cols[0])
        if j == self.m + 1:
            return kernel_vector(cols, p)
        e = self.shifts[j - 1]
        ge_inv = pow(int(self.pw[e % (p - 1)]), p - 2, p)
        c = (-pow(int(self.pw[e % (p - 1)]), p - 2, p)) % p
        N = len(cols) // (a + 1)
        objs = []
        for blk in range(a + 1):
            sub = cols[blk * N:(blk + 1) * N]
            x = self.solve(j + 1, sub)
            I = [i for i, t in enumerate(x) if t and self.cos(t) in self.A[j]]
            J = [i for i, t in enumerate(x) if t and self.cos(t) not in self.A[j]]
            assert all(self.cos(x[i] * ge_inv) in self.A[j] for i in J)
            if not J or not I:
                w = [0] * len(cols)
                for i, t in enumerate(x):
                    if t:
                        w[blk * N + i] = t if not J else t * ge_inv % p
                return w
            u = [sum(x[i] * sub[i][r] for i in I) % p for r in range(a)]
            objs.append((blk, u, {i: x[i] for i in I}, {i: x[i] * ge_inv % p for i in J}))
        eta = kernel_vector([o[1] for o in objs], p)
        w = [0] * len(cols)
        for (blk, u, R1, R2), et in zip(objs, eta):
            if et:
                y1, y2 = self.two_term(et, c)
                for i, t in R1.items():
                    w[blk * N + i] = y1 * t % p
                for i, t in R2.items():
                    w[blk * N + i] = y2 * t % p
        return w


def part3(rng):
    cases = [(3, 7, None), (3, 13, None), (5, 31, None), (5, 41, None), (5, 61, None), (5, 2521, None),
             (7, 113, None), (7, 9661, None), (9, 199, None), (6, 67, None), (4, 37, None), (8, 1009, None)]
    runs = fails = 0
    for kappa, p, _ in cases:
        g, log, pw = dlog_table(p)
        good = good_shifts(p, kappa, log, pw)
        # BFS with parent pointers to recover shifts
        full = (1 << kappa) - 1
        par = {1: None}
        dq = deque([1])
        while dq:
            A = dq.popleft()
            for e in good:
                B = A | (((A << e) | (A >> (kappa - e))) & full)
                if B not in par:
                    par[B] = (A, e)
                    dq.append(B)
        if full not in par:
            print(f"(3) kappa={kappa} p={p}: no tower plan")
            continue
        sh, B = [], full
        while par[B]:
            B, e = par[B]
            sh.append(e)
        sh.reverse()
        T = Tower(p, kappa, sh, rng)
        for a in (1, 2):
            M = (a + 1) ** (T.m + 1)
            for fam in ("random", "rank1", "units", "zero_heavy"):
                if fam == "random":
                    cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                elif fam == "rank1":
                    w0 = [rng.randrange(1, p) for _ in range(a)]
                    cols = [[int(pw[rng.randrange(p - 1)]) * t % p for t in w0] for _ in range(M)]
                elif fam == "units":
                    cols = []
                    for _ in range(M):
                        v = [0] * a
                        v[rng.randrange(a)] = int(pw[rng.randrange(kappa)])
                        cols.append(v)
                else:
                    cols = [[rng.randrange(p) if rng.random() < 0.15 else 0 for _ in range(a)] for _ in range(M)]
                w = T.solve(1, cols)
                ok = any(w) and all(T.inP0(t) for t in w) and all(
                    sum(w[i] * cols[i][r] for i in range(M)) % p == 0 for r in range(a))
                runs += 1
                fails += (not ok)
        print(f"(3) kappa={kappa} p={p}: shifts {sh}, degree {len(sh) + 1}", flush=True)
    print(f"(3) Lemma D tower runs {runs}, failures {fails}")


if __name__ == "__main__":
    pmax, kmax = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(7)
    part1(pmax)
    part3(rng)
    part2(kmax)
