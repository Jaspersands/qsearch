"""Lemma K check: the explicit two-level contractions for kappa = 2 and 3 exist at every prime
in range, satisfy all kappa^2 coset conditions, and (kappa = 3) the count of admissible b equals
Gauss's cyclotomic number (1,2)_3 = (p + 1 + L)/9, 4p = L^2 + 27 M^2, L = 1 mod 3.
Usage: python check_contractions.py PMAX
"""
import math
import sys

from sdelib import Field, contraction_ok, explicit_contraction, is_prime


def gauss_L(p):
    for M in range(0, int(math.isqrt(4 * p // 27)) + 2):
        r = 4 * p - 27 * M * M
        if r < 0:
            break
        L = math.isqrt(r)
        if L * L == r:
            for s in (L, -L):
                if s % 3 == 1:
                    return s
    return None


def main():
    pmax = int(sys.argv[1])
    bad = []
    n2 = n3 = 0
    minratio = None
    for p in range(3, pmax + 1):
        if not is_prime(p):
            continue
        F = Field(p, 2)
        ab = explicit_contraction(F)
        if ab is None or not contraction_ok(F, *ab):
            bad.append((p, 2))
        n2 += 1
        if p % 3 == 1:
            F = Field(p, 3)
            ab = explicit_contraction(F)
            if ab is None or not contraction_ok(F, *ab):
                bad.append((p, 3))
            cnt = sum(1 for b in range(1, p)
                      if F.cos(b) == 1 and (1 + b) % p and F.cos(1 + b) == 2)
            L = gauss_L(p)
            if L is None or 9 * cnt != p + 1 + L:
                bad.append((p, 3, "gauss", cnt, L))
            r = cnt / p
            minratio = r if minratio is None else min(minratio, r)
            n3 += 1
    print(f"primes checked: kappa=2: {n2} (3..{pmax}); kappa=3: {n3} (p = 1 mod 3)")
    print(f"failures: {bad}")
    print(f"kappa=3: min over p of #b / p = {minratio:.4f}")


if __name__ == "__main__":
    main()
