"""Exact-integer checks of the displayed inequalities of Appendix B (Schedule 3).

Independent re-derivation for the 2026-11-03 unanchored check. Every comparison uses
Python integers or fractions.Fraction; no floats decide anything.

Run: /opt/anaconda3/bin/python -I ineq_check.py [UMAX]
"""
import sys
from fractions import Fraction as Fr
from math import comb, gcd


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


def clog2(x):
    """ceil(log2 x) for a positive rational x, exactly."""
    x = Fr(x)
    k = 0
    while Fr(2) ** k < x:
        k += 1
    while k > 0 and Fr(2) ** (k - 1) >= x:
        k -= 1
    return k


fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


UMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
count = 0
for u in range(2, UMAX + 1):
    M = 4 * u
    # Lemma s3-mu(a): (16u^2)^{3u} / (2u)^{4u-1} = 2^{8u+1} u^{2u+1}
    check((16 * u * u) ** (3 * u) == 2 ** (8 * u + 1) * u ** (2 * u + 1) * (2 * u) ** (4 * u - 1),
          f"identity u={u}")
    # Lemma s3-tree(c) closed forms
    t1 = Fr((4 * u) ** (u - 1) * 4, 2 ** (8 * u + 1) * u ** (2 * u + 1))
    t2 = Fr((4 * u) ** (u - 1) * 2, (16 * u * u) ** (3 * u + 1))
    check(t1 == Fr(1, 2 ** (6 * u + 1) * u ** (u + 2)), f"tree t1 u={u}")
    check(t2 == Fr(1, 2 ** (10 * u + 5) * u ** (5 * u + 3)), f"tree t2 u={u}")
    check(t1 + t2 < Fr(1, 64), f"tree bank sum u={u}")
    # Prop s3-uniform(a): beta_d <= 2^-17 (appendix prints 2^-20 + 2^-37 at u=2)
    beta_bd = Fr(4, 2 ** (8 * u + 1) * u ** (2 * u + 1)) + Fr(2, (16 * u * u) ** (3 * u + 1))
    check(beta_bd <= Fr(1, 2 ** 17), f"beta<=2^-17 u={u}")
    if u == 2:
        check(Fr(2, (16 * u * u) ** (3 * u + 1)) == Fr(1, 2 ** 41), "u=2 second term is 2^-41")
        check(Fr(4, 2 ** (8 * u + 1) * u ** (2 * u + 1)) == Fr(1, 2 ** 20), "u=2 first term 2^-20")
    for c in range(2, u + 1):
        T = sum(M ** j for j in range(c - 1))
        check(T == (M ** (c - 1) - 1) // (M - 1), f"T formula u={u} c={c}")
        check(T <= M ** (c - 1) <= (4 * u) ** (u - 1), f"T bound u={u} c={c}")
        B = clog2(64 * M ** (c - 1))
        check(B == 6 + clog2(Fr(M) ** (c - 1)), f"B split u={u} c={c}")
        check(B <= 6 + (u - 1) * clog2(4 * u), f"B<=6+.. u={u} c={c}")
        check(3 * T * Fr(1, 2 ** B) <= Fr(3, 64), f"3T2^-B u={u} c={c}")
        check(T * (beta_bd + 3 * Fr(1, 2 ** B)) <= Fr(1, 16), f"tree abort u={u} c={c}")
        # N_instr <= 4m'(M^{c-1} + (M+1)T) + m' <= 13 m' M^{c-1}  (per unit m')
        check(4 * (M ** (c - 1) + (M + 1) * T) + 1 <= 13 * M ** (c - 1), f"Ninstr u={u} c={c}")
        # node failure accounting: F = K M + M L R draws, cap B + ceil log2 F
        for kappa in range(1, c + 1):
            K = 4 * kappa ** M * B
            L = max(1, clog2(kappa))
            R = 2 * (B + clog2(M * L))
            F = K * M + M * L * R
            cap = B + clog2(F)
            check(F * Fr(1, 2 ** cap) <= Fr(1, 2 ** B), f"draw union u={u} c={c} k={kappa}")
            check(M * L * Fr(4, 9) ** (B + clog2(M * L)) <= Fr(1, 2 ** B), f"root union u={u} c={c} k={kappa}")
            check((Fr(2, 3) ** 2) < Fr(1, 2), "4/9<1/2")
            # (1 - 1/(4k^M))^K <= 2^-B: check via (1-x)^K <= e^{-xK} = e^{-B} <= 2^{-B}; exact for small
            if M * B <= 64 and kappa <= 2:
                x = Fr(1, 4 * kappa ** M)
                check((1 - x) ** K <= Fr(1, 2 ** B), f"trial fail u={u} k={kappa}")
        count += 1
    # parameter bounds at real primes: least prime >= 16u^2, and 2^61-1
    for p in sorted({next_prime(16 * u * u), 2 ** 61 - 1}):
        for d in range(2, u + 1):
            kappa = gcd(d, p - 1)
            h = (p - 1) // kappa
            for a in (0, u - 1):
                num = (h + 1) ** M - 1
                # mu = num / (h p^a) >= 2^{8u+1} u^{2u+1}
                check(num >= 2 ** (8 * u + 1) * u ** (2 * u + 1) * h * p ** a, f"mu p={p} u={u} d={d} a={a}")
                # acceptance num/(2 p^M) >= 1/(4 kappa^M)
                check(4 * kappa ** M * num >= 2 * p ** M, f"acc p={p} u={u} d={d}")
                beta = Fr(4 * h * p ** a, num) + 2 * Fr(p ** a, p ** M)
                check(beta <= Fr(1, 2 ** 17), f"beta real p={p} u={u} d={d} a={a}")

# binomial/restart bound: C(4m',3m') 16^{-3m'} <= C(4m',3m') 4^{-3m'} <= 2^{-2m'}
for mp in range(1, 401):
    check(comb(4 * mp, 3 * mp) * 2 ** (2 * mp) <= 4 ** (3 * mp), f"binom 1/4 m'={mp}")
    check(comb(4 * mp, 3 * mp) <= 2 ** (4 * mp), f"binom<=2^4m' m'={mp}")
# exact restart probability with abort prob exactly 1/16 (tail of Binomial(4m',15/16) < m')
for mp in range(1, 121):
    q = Fr(1, 16)
    tail = sum(comb(4 * mp, s) * (1 - q) ** s * q ** (4 * mp - s) for s in range(mp))
    check(tail <= Fr(1, 2 ** (2 * mp)), f"exact restart tail m'={mp}")
# eps split: 2^{-2m'} <= (eps/3)^2 <= eps/3 and rank bound with m'-k >= ceil log2(3/eps)
for kk in range(1, 2001):
    eps = Fr(1, kk)
    t = clog2(3 / eps)
    check(Fr(1, 2 ** (2 * t)) <= (eps / 3) ** 2 <= eps / 3, f"eps split 1/{kk}")
    for p in (67, 2 ** 61 - 1):
        check(Fr(1, (p - 1) * 2 ** t) <= eps / 3, f"rank third 1/{kk} p={p}")
# eps > 1 boundary: eps in (1,3)
for num in range(4, 30):
    eps = Fr(num, 10)
    if eps < 3:
        t = clog2(3 / eps)
        check(Fr(1, 2 ** (2 * t)) <= eps / 3, f"eps={eps}")

print(f"(u,c) cases: {count}; failures: {len(fails)}")
for f in fails[:40]:
    print("FAIL", f)
