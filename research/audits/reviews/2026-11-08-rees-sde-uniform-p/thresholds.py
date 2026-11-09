"""Least thresholds from Lemma W (same bound and integer search as
../2026-11-07-rees-sde-subquad-A/weil_thresholds.py), for E = 3J - 2.

LW(p) = min_{1<=e<=E} kappa^{-e} (p - e - (kappa^e - 1)(e - 1) sqrt p)  <=  G*_E(p).
  C0     : least p with LW(p) > 0            (every Good set with <= E distinct offsets nonempty)
  C_loc  : least p with LW(p) >= N_loc + 1 and (p-1)/kappa >= N_loc + 1, where
           N_loc = max number of cross-class pairs among E blocks (balanced classes):
           the lookahead pass of Theorem L never fails on a leaf with fan-in <= N_loc.
  C_old  : least p with LW(p) >= p/(2 kappa^E) (Theorem A's constant part); Theorem A also
           needs p >= 2 E r kappa^E.
Also the least prime = 1 mod kappa at or above each threshold, and the pigeonhole bound:
G*_E(p) = 0 whenever kappa^E > p + E(kappa - 1).
"""
import math


def LW(p, k, E):
    return min(k ** (-e) * (p - e - (k ** e - 1) * (e - 1) * math.sqrt(p)) for e in range(1, E + 1))


def least(pred):
    hi = 2
    while not pred(hi):
        hi *= 2
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid
    assert all(pred(int(hi * f)) for f in (1, 1.01, 1.5, 2, 10, 100, 1e4))
    return hi


def isprime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def nextp(n, k):
    while not (isprime(n) and (n - 1) % k == 0):
        n += 1
    return n


def maxcross(E, k):
    sizes = [E // k + (1 if i < E % k else 0) for i in range(k)]
    return E * (E - 1) // 2 - sum(s * (s - 1) // 2 for s in sizes)


for k in (2, 3):
    for J in (3, 4, 5):
        E = 3 * J - 2
        N = maxcross(E, k)
        c0 = least(lambda p: LW(p, k, E) > 0)
        cl = least(lambda p: LW(p, k, E) >= N + 1 and (p - 1) / k >= N + 1)
        co = least(lambda p: LW(p, k, E) >= p / (2 * k ** E))
        pig = k ** E - E * (k - 1)
        print("kappa=%d J=%d E=%2d N_loc=%2d | C0 = %d (prime %d) | C_loc = %d (prime %d) | "
              "C_old = %d and p >= %d r | pigeonhole: G*_E(p) = 0 for p < %d"
              % (k, J, E, N, c0, nextp(c0, k), cl, nextp(cl, k), co, 2 * E * k ** E, pig))
