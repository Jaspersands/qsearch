"""Exact integer / rational checks of the counting steps of Appendix E.

1. Spanning bound (used by Lemma lem:app-codim-sample and the birthday learner):
   P[t uniform vectors fail to span F_p^r] = 1 - prod_{i<r}(1 - p^{i-t}) <= p^{r-t}.
2. Birthday batch: B = isqrt(2I) + 2 gives B(B-1) > 2I and
   P[no repeated coset among B uniform draws from J <= I cosets] < 1/2.
3. Small primes: for p < 64k^2, log2 B <= k(3 + log2 k) + 2, i.e.
   B <= 4 * (8k)^k, checked with the largest prime below 64k^2, k = 1..300.
4. Error budget of the quantum route: with T = m + ceil(log2(4m/eps)),
   m * 2^(m-T) <= eps/4 and 2 m N_s eta = eps/4 for eta = eps/(8 m N_s).
Run: /opt/anaconda3/bin/python bounds_check.py
"""
from fractions import Fraction as Fr
from math import isqrt, ceil, log2
import sys


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def main():
    bad = 0
    # 1
    cnt = 0
    for p in (2, 3, 5, 7, 11):
        for r in range(0, 7):
            for t in range(r, r + 12):
                span = Fr(1)
                for i in range(r):
                    span *= 1 - Fr(p) ** (i - t)
                fail = 1 - span
                cnt += 1
                if fail > Fr(p) ** (r - t):
                    bad += 1
                    print("spanning bound fails", p, r, t)
    print(f"1. spanning bound: {cnt} cases (p<=11, r<=6, r<=t<r+12), failures {bad}")
    # 2
    cnt = 0
    for I in list(range(1, 3001)) + [p ** k for p in (3, 5, 7) for k in range(1, 6)]:
        B = isqrt(2 * I) + 2
        if not B * (B - 1) > 2 * I:
            bad += 1
            print("B(B-1) > 2I fails", I)
        J = I            # worst case: no-repeat probability increases with J
        if B > J:
            continue
        pr = Fr(1)
        for i in range(1, B):
            pr *= Fr(J - i, J)
        cnt += 1
        if not pr < Fr(1, 2):
            bad += 1
            print("no-repeat >= 1/2", I, B, float(pr))
    # monotonicity in J used above: check directly for small I
    for I in range(1, 400):
        B = isqrt(2 * I) + 2
        for J in range(1, I + 1):
            if B > J:
                continue
            pr = Fr(1)
            for i in range(1, B):
                pr *= Fr(J - i, J)
            if not pr < Fr(1, 2):
                bad += 1
                print("no-repeat >= 1/2 at J<I", I, J)
    print(f"2. birthday batch: {cnt} values of I (and all J <= I < 400), failures so far {bad}")
    # 3
    worst = 0.0
    for k in range(1, 301):
        q = 64 * k * k - 1
        while not is_prime(q):
            q -= 1
        B = isqrt(2 * q ** k) + 2
        if not B <= 4 * (8 * k) ** k:
            bad += 1
            print("small-prime bound fails", k, q)
        worst = max(worst, log2(B) / (k * log2(k + 2)))
    print(f"3. small primes, k=1..300, largest prime < 64k^2: max log2(B)/(k log2(k+2)) = "
          f"{worst:.4f}; failures so far {bad}")
    # 4
    for m in range(1, 60):
        for eps in (Fr(1, 3), Fr(1, 10), Fr(1, 1000), Fr(1, 2 ** 40)):
            x, e = Fr(4 * m) / eps, 0          # T = m + ceil(log2(4m/eps)), exactly
            while Fr(2) ** e < x:
                e += 1
            T = m + e
            if not m * Fr(2) ** (m - T) <= eps / 4:
                bad += 1
                print("abort budget fails", m, eps)
            Ns = m * (T + m + 1)
            eta = eps / (8 * m * Ns)
            if 2 * m * Ns * eta != eps / 4:
                bad += 1
    print(f"4. error budget arithmetic: failures {bad} (total)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
