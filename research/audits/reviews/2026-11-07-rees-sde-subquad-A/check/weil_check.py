"""Independent check of the Lemma W thresholds quoted in the report:
least p (real) with kappa^{-e}(p - e - (kappa^e-1)(e-1)sqrt p) >= p/(2 kappa^E) for all e<=E,
the claim p >= 8 kappa^{2E} E^2 => that inequality, and the arithmetic of section 2
((kappa^E-1)(E-1)sqrt p + E <= p/2 at p = 8 kappa^{2E} E^2)."""
import math
def ok(p, k, E):
    return all(k ** (-e) * (p - e - (k ** e - 1) * (e - 1) * math.sqrt(p)) >= p / (2 * k ** E) for e in range(1, E + 1))
for k in (2, 3):
    for E in (5, 7, 10, 13, 16, 22):
        lo, hi = 1.0, 1e40
        while hi / lo > 1 + 1e-9:
            mid = math.sqrt(lo * hi)
            if ok(mid, k, E): hi = mid
            else: lo = mid
        p8 = 8 * k ** (2 * E) * E * E
        lhs = (k ** E - 1) * (E - 1) * math.sqrt(p8) + E
        print("kappa=%d E=%2d least p %.4e  8k^2E E^2=%.4e  ok(8k^2E E^2)=%s  ratio(err/p at p8)=%.4f  p/(2sqrt2)+0.15p over p = %.4f" % (
            k, E, hi, p8, ok(p8, k, E), lhs / p8, 1 / (2 * math.sqrt(2)) + 0.15))
# Corollary A3 constants
for k, E in ((2, 7), (3, 7)):
    print("   rho<=7r/2, 1/G*<=2k^7/p -> 7 r k^7 / p <= 1/2 -> p >= 14 k^7 r =", 14 * k ** 7, "r")
