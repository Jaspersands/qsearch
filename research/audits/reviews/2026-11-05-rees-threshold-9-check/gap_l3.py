"""Referee check: for r odd, Theorem 1 as stated lets U_r use l_m with eta_m >= 1.
Exact E C(n_0, 3) at k=3, p=31 versus l_3(1) = C(h,3) rho_3^2 (1-eta_3)^2."""
import itertools, math
from fractions import Fraction
k, p = 3, 31
h = (p - 1) // k
g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in (2, 3, 5)))
ind = {pow(g, e, p): e % k for e in range(p - 1)}
tot = Fraction(0)
for y1 in range(p):
    for y2 in range(p):
        y = [0, y1, y2]
        n0 = sum(1 for x in range(1, p) if all((x + y[i]) % p != 0 and ind[(x + y[i]) % p] == (-i) % k for i in range(k)))
        tot += math.comb(n0, 3)
ECn3 = tot / p ** 2
sp = math.sqrt(p)
E3 = (3 - 1 - 3 / k + k ** -3) * sp + 3 / k - 3 * k ** -3
eta3 = k ** 3 * E3 / (p - 3)
rho3 = (p - 3) / (p * k ** 3)
l3 = math.comb(h, 3) * rho3 ** (k - 1) * (1 - eta3) ** (k - 1)
print(f"k=3 p=31: exact E C(n_0,3) = {float(ECn3):.5f}; eta_3 = {eta3:.3f}; formula l_3(1) = {l3:.4f}  -> l_3 is {'NOT ' if l3 > ECn3 else ''}a lower bound")
