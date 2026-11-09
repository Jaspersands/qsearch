"""Exact-integer check of RANDOM_COLUMN_REES_PARAMETER_BOUND.md Section 6 (hidden-codimension
corollary) and of the classical small-prime branch.

Large-prime branch: terminal of the abelian-ideal reduction has class c* <= 2k-1 and every
Rees label rank a_d <= k. Take u = 2k, M = 4u = 8k, p >= 16u^2 = 64k^2, and evaluate every
quantity of Thm random-column at the WORST profile c = 2k-1 and a_d = k at every grade
(mu decreases and the bank failure increases in a; the node count increases in c), with the
true kappa_d = gcd(d, p-1), for the least prime >= 64k^2 and for p = 2^61-1:
  mu_d >= 2^(8u+1) u^(2u+1);  acceptance >= 1/(4 kappa^M);  bank sum <= 1/64;  abort <= 1/16.
Also reports log2(queries per tree) and log2(classical trials per tree) over k log2(k+2).
Small-prime branch (p < 64k^2): birthday batch B = floor(sqrt(2 p^k)) + 2 of
BOUNDED_CODIMENSION_HYBRID_BOUND.md Section 2; reports log2(B)/(k log2(k+2)).
Run: /opt/anaconda3/bin/python section6_bounds.py
"""
from fractions import Fraction
from math import gcd, log2, ceil, isqrt


def is_prime(n):
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


def next_prime(n):
    while not is_prime(n):
        n += 1
    return n


def prev_prime(n):
    while not is_prime(n):
        n -= 1
    return n


def large_branch(k, p):
    u, M, c, a = 2 * k, 8 * k, 2 * k - 1, k
    assert p >= 16 * u * u and c <= u and a <= u - 1
    T_tree = sum(M ** j for j in range(c - 1))
    P_tree = M ** (c - 1)
    B = ceil(log2(64 * P_tree))
    worst_beta, mu_ok, acc_ok, kmax = Fraction(0), True, True, 1
    for d in range(2, c + 1):
        kap = gcd(d, p - 1)
        kmax = max(kmax, kap)
        h = (p - 1) // kap
        N0 = (h + 1) ** M - 1
        mu_ok &= N0 >= h * p ** a * 2 ** (8 * u + 1) * u ** (2 * u + 1)
        acc_ok &= 4 * N0 * kap ** M >= 2 * p ** M
        worst_beta = max(worst_beta, Fraction(4 * h * p ** a, N0) + Fraction(2, p ** (M - a)))
    bank = T_tree * worst_beta
    abort = Fraction(3, 64) + bank
    scale = k * log2(k + 2)
    lq = log2(c) + log2(P_tree)
    lc = log2(max(T_tree, 1)) + log2(4 * B) + M * log2(kmax)
    return dict(k=k, p=p, mu=mu_ok, acc=acc_ok, bank=bank <= Fraction(1, 64),
                abort=abort <= Fraction(1, 16), qr=lq / scale, cr=lc / scale,
                lbank=log2(bank.numerator) - log2(bank.denominator) if bank else float('-inf'))


def main():
    print("== Large-prime branch: u = 2k, M = 8k, c = 2k-1, a_d = k at every grade (worst case)")
    rows = []
    for k in list(range(2, 41)) + [60, 100, 150, 200]:
        for p in (next_prime(64 * k * k), 2 ** 61 - 1):
            if p >= 64 * k * k:
                rows.append(large_branch(k, p))
    bad = [r for r in rows if not (r['mu'] and r['acc'] and r['bank'] and r['abort'])]
    print(f" cases {len(rows)}; failures of mu / acceptance / bank<=1/64 / abort<=1/16: {len(bad)}")
    for r in rows:
        if r['k'] in (2, 3, 4, 5, 10, 20, 40, 100, 200):
            print(f"  k={r['k']:3d} p={r['p']:<20d} log2(bank sum)={r['lbank']:10.1f} "
                  f"log2(queries/tree)/(k log2(k+2))={r['qr']:.3f} "
                  f"log2(classical/tree)/(k log2(k+2))={r['cr']:.3f}")
    print(f" max ratios: queries {max(r['qr'] for r in rows):.3f}, classical {max(r['cr'] for r in rows):.3f}")
    print("\n== Small-prime branch: p < 64k^2, birthday batch B = floor(sqrt(2p^k)) + 2")
    worst = 0
    for k in range(1, 201):
        p = prev_prime(64 * k * k - 1)
        if p < 3:
            continue
        B = isqrt(2 * p ** k) + 2
        ratio = log2(B) / (k * log2(k + 2))
        worst = max(worst, ratio)
        if k in (1, 2, 3, 5, 10, 50, 100, 200):
            print(f"  k={k:3d} p={p:7d} log2(B)/(k log2(k+2))={ratio:.3f}")
    print(f"  max over k=1..200: {worst:.3f}  (log2 p < 6 + 2 log2 k, so log2 B <= k(3 + log2 k) + 2)")
    # u = 2k-1 also suffices for k >= 2 (c* <= 2k-1 <= u, a_d <= k <= u-1)
    print("\n== Remark: u = 2k-1 also satisfies the hypotheses for k >= 2; threshold p >= 16(2k-1)^2")


if __name__ == "__main__":
    main()
