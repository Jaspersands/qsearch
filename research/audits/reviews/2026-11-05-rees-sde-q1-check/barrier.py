"""Counting barrier for heavy stalls whose Y-fallback fails (ALG-Q1 with the code's fallback).
At a case-4 stall with q >= 3, b >= q-1, eps >= 1, r = q+b+eps, M >= f(r):
  cols(span(B cap U)) >= b + pi >= b + 2r + D_3(q) - q.
The Y-recursion count fails only if this lower bound is < f(b) = D_3(b) + 3b.
Also checks the identities of the proof of Theorem Q1 and the Lemma W thresholds."""
import math
from myq1 import D3, f

print("identities: f(r)-f(r-1) = floor((r+2)/2)+3 >= 4 ; f(r)-f(r-2) = r+7 (r>=3) ; D3(q)-D3(q-2) = q+1 (q>=3)")
for r in range(1, 400):
    assert f(r) - f(r - 1) >= 4
    if r >= 2: assert f(r) - f(r - 1) == (r + 2) // 2 + 3
    if r >= 3: assert f(r) - f(r - 2) == r + 7
    if r >= 3: assert D3(r) - D3(r - 2) == r + 1
assert f(2) - f(0) == 10
print("  ok for r < 400")
print("case-2 count: b + 2r + D3(q) - q >= f(b) whenever b <= q-2, all r,q < 200:")
for r in range(2, 200):
    for q in range(3, r):
        for b in range(1, min(q - 1, r - q + 1)):
            assert b + 2 * r + D3(q) - q >= f(b), (r, q, b)
print("  ok")
print("case-3 count: f(r) - (r+1) >= f(r - qp) for 2 <= qp < r:")
for r in range(3, 300):
    for qp in range(2, r):
        assert f(r) - (r + 1) >= f(r - qp)
print("  ok")
print("heavy stalls with Y-count failing are possible by counting only for:")
first = None
for r in range(3, 40):
    sh = []
    for q in range(3, r // 2 + 1):
        for b in range(q - 1, r - q):
            eps = r - q - b
            if eps < 1:
                continue
            slack = f(b) - 1 - (b + 2 * r + D3(q) - q)
            if slack >= 0:
                sh.append((q, b, eps, slack))
    if sh:
        first = first or r
        print("  r=%d" % r, sh[:6])
    if r > 14:
        break
print("smallest r:", first)
print("Lemma W bound G*_E >= kappa^-E (p - E - (kappa^E-1)(E-1) sqrt p); least p with bound >= p/(2 kappa^E):")
for k in (2, 3):
    for E in (3, 4, 5, 6):
        A = (k ** E - 1) * (E - 1)
        # p/2 - A sqrt p - E >= 0
        x = A + math.sqrt(A * A + 2 * E)
        pt = math.ceil(x * x)
        # verify on a range: min over e<=E of the bound >= p/(2k^E) for p >= pt
        for p in list(range(pt, pt + 2000)) + [10 * pt, 1000 * pt]:
            m = min(k ** -e * (p - e - (k ** e - 1) * (e - 1) * math.sqrt(p)) for e in range(1, E + 1))
            assert m >= p / (2 * k ** E) - 1e-9, (k, E, p)
        print("  kappa=%d E=%d: p >= %d  (2 kappa^E = %d)" % (k, E, pt, 2 * k ** E))
print("Theorem Q1(c), c<=2: need 2.5 r * 2 kappa^5 / p <= 1/2  ->  p >= 10 kappa^5 r =", [10 * 2 ** 5, 10 * 3 ** 5])
print("kappa/(p-1) <= 2 kappa^5/p at those p:", 2 / (62000 - 1) <= 64 / 62000, 3 / (3.75e6 - 1) <= 486 / 3.75e6)
print("general range check, E'=3+c, p >= 8 k^{2E'} E'^2 implies Lemma W bound >= p/(2k^E'):")
for k in (2, 3):
    for c in range(0, 6):
        E = 3 + c
        p = 8 * k ** (2 * E) * E * E
        for pp in (p, 2 * p, 10 * p):
            m = min(k ** -e * (pp - e - (k ** e - 1) * (e - 1) * math.sqrt(pp)) for e in range(1, E + 1))
            assert m >= pp / (2 * k ** E)
print("  ok")
