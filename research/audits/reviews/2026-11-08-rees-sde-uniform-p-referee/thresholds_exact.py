"""Referee recomputation of Corollary L2's thresholds with exact integer arithmetic.

LW_E(p) = min_{1<=e<=E} kappa^{-e} (p - e - (kappa^e - 1)(e - 1) sqrt(p)).
Condition LW_E(p) >= N + 1  <=>  for every e <= E:
    p - e - (N+1) kappa^e >= (kappa^e - 1)(e - 1) sqrt(p)
  <=>  A_e := p - e - (N+1) kappa^e >= 0  and  A_e^2 >= (kappa^e - 1)^2 (e - 1)^2 p.
Everything below is integer arithmetic; primality by sympy.isprime (deterministic below 3.3e24).

C0    : least integer p with LW_E(p) > 0            (N = -1 with strict inequality; handled separately)
C_loc : least integer p with LW_E(p) >= N_loc + 1 and (p - 1)/kappa >= N_loc + 1
C_old : least integer p with LW_E(p) >= p / (2 kappa^E)
and the least prime p == 1 (mod kappa) at or above each.  Also: the largest prime == 1 mod kappa
below each prime threshold is checked to FAIL the condition (so the prime is the least admissible).
"""
from math import isqrt
from sympy import isprime


def lw_ge(p, k, E, N):
    """LW_E(p) >= N + 1 exactly (N may be -1 for '>= 0')."""
    for e in range(1, E + 1):
        A = p - e - (N + 1) * k ** e
        if A < 0:
            return False
        if A * A < ((k ** e - 1) * (e - 1)) ** 2 * p:
            return False
    return True


def lw_gt0(p, k, E):
    for e in range(1, E + 1):
        A = p - e
        if A <= 0:
            return False
        if A * A <= ((k ** e - 1) * (e - 1)) ** 2 * p:
            return False
    return True


def old_cond(p, k, E):
    """LW_E(p) >= p/(2 kappa^E): for every e, 2 kappa^E (p - e - c_e sqrt p) >= kappa^e p, i.e.
    2 kappa^(E-e) (p - e) - p >= 2 kappa^(E-e) c_e sqrt p."""
    for e in range(1, E + 1):
        c = (k ** e - 1) * (e - 1)
        A = 2 * k ** (E - e) * (p - e) - p
        if A < 0:
            return False
        if A * A < (2 * k ** (E - e) * c) ** 2 * p:
            return False
    return True


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
    # monotonicity spot check on a range above
    assert all(pred(hi + d) for d in range(0, 2000, 37))
    assert not pred(hi - 1)
    return hi


def next_prime_1mod(n, k):
    while not (isprime(n) and (n - 1) % k == 0):
        n += 1
    return n


def prev_prime_1mod(n, k):
    n -= 1
    while not (isprime(n) and (n - 1) % k == 0):
        n -= 1
    return n


def maxcross(E, k):
    sizes = [E // k + (1 if i < E % k else 0) for i in range(k)]
    return E * (E - 1) // 2 - sum(s * (s - 1) // 2 for s in sizes)


def maxcross_bruteforce(E, k):
    best = 0
    import itertools
    for c in itertools.product(range(k), repeat=E):
        best = max(best, sum(1 for i in range(E) for j in range(i + 1, E) if c[i] != c[j]))
    return best


claimed = {(2, 3): 583991, (2, 4): 84822113, (3, 3): 172103821, (3, 4): 282423985969}
claimed_old = {(2, 3): 2322604, (2, 4): 339075436, (3, 3): 688117852, (3, 4): 1129679882536}
for k in (2, 3):
    for J in (3, 4):
        E = 3 * J - 2
        N = maxcross(E, k)
        if E <= 10:
            assert N == maxcross_bruteforce(E, k), (E, k)
        c0 = least(lambda p: lw_gt0(p, k, E))
        cl = least(lambda p: lw_ge(p, k, E, N) and (p - 1) >= k * (N + 1))
        co = least(lambda p: old_cond(p, k, E))
        pl = next_prime_1mod(cl, k)
        pprev = prev_prime_1mod(pl, k)
        ok_prev = lw_ge(pprev, k, E, N) and (pprev - 1) >= k * (N + 1)
        print("kappa=%d J=%d E=%d N_loc=%d | C0=%d (prime %d) | C_loc=%d prime %d [claimed %d, %s] "
              "prev prime %d satisfies: %s | C_old=%d [claimed %d, %s]"
              % (k, J, E, N, c0, next_prime_1mod(c0, k), cl, pl, claimed[(k, J)],
                 "MATCH" if pl == claimed[(k, J)] else "MISMATCH", pprev, ok_prev, co,
                 claimed_old[(k, J)], "MATCH" if co == claimed_old[(k, J)] else "MISMATCH"))
        # which e attains the minimum at the threshold?
        import math
        vals = [(k ** (-e) * (cl - e - (k ** e - 1) * (e - 1) * math.sqrt(cl)), e) for e in range(1, E + 1)]
        print("   LW_E(C_loc) float = %.4f attained at e=%d; N_loc+1 = %d" % (min(vals)[0], min(vals)[1], N + 1))
