"""Arity/time tradeoff obtained by instantiating Theorem A of report
2026-11-07-rees-sde-subquad-A.md at general J: arity F_J(a) = D_J(a) + max(2, 2J-4) a,
expected time kappa^(3J-2) poly, primes p >= max(8 kappa^(2E) E^2, 2 E a kappa^E), E = 3J-2.
D_J(0) = 0, D_J(q) = max_{1<=k<=q} (k + 1 + D_J(q - min(J-1, k))). Exact integers.
Run: /opt/anaconda3/bin/python -I tradeoff.py"""
import math
def DJ(J, amax):
    D = [0] * (amax + 1)
    for q in range(1, amax + 1):
        best = 0
        # k >= J-1 all give gain J-1; the max over those is k = q
        for k in range(1, min(q, J - 1) + 1):
            best = max(best, k + 1 + D[q - k])
        if q >= J - 1:
            best = max(best, q + 1 + D[q - (J - 1)])
        D[q] = best
    return D
print("a  J*  F_J*(a)  F/a^1.5  3J*-2(exponent of kappa)  | F at J=ceil(log2 a)  ratio to (a+1)(a+2)/2")
for a in [64, 256, 1024, 4096, 16384]:
    best = None
    for J in range(2, int(2 * math.sqrt(a)) + 3):
        F = DJ(J, a)[a] + max(2, 2 * J - 4) * a
        if best is None or F < best[1]:
            best = (J, F)
    J0 = max(3, math.ceil(math.log2(a)))
    F0 = DJ(J0, a)[a] + max(2, 2 * J0 - 4) * a
    print(a, best[0], best[1], f"{best[1] / a ** 1.5:.3f}", 3 * best[0] - 2, "|", F0, f"{F0 / ((a + 1) * (a + 2) / 2):.3f}")
