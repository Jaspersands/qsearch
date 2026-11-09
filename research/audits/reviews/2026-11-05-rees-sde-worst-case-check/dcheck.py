"""Check D_E: closed form D_3(q) = floor((q+2)^2/4), the bound D_E(q) <= q^2/(2(E-1)) + q(1/(E-1)+5/2),
monotonicity, D_2(q) = (q+1)(q+2)/2 - 1, the excess D_E(r) - (M_E(r) - 1) (M_E of rem:sde-block-steered),
and the arity table of the report (Section 3.1)."""
import sys
sys.setrecursionlimit(10000)
from mysss import D
def M_E(E, a):
    m, r = divmod(a, E - 1)
    return 1 + m * (a + 1) - (E - 1) * m * (m - 1) // 2 + ((r + 1) if r > 0 else 0)
bad = 0
for q in range(1, 401):
    bad += D(3, q) != (q + 2) ** 2 // 4
    bad += D(2, q) != (q + 1) * (q + 2) // 2 - 1
    for E in range(3, 13):
        bad += D(E, q) > q * q / (2 * (E - 1)) + q * (1 / (E - 1) + 2.5) + 1e-9
        bad += D(E, q) < D(E, q - 1)
        bad += D(E, q) - (M_E(E, q) - 1) > 2 * q
    bad += D(3, q) - (M_E(3, q) - 1) != (1 if q % 2 == 0 else 0)
print("violations (q<=400, E<=12):", bad)
print("max excess D_E(r)-(M_E(r)-1) over r<=400:", {E: max(D(E, q) - (M_E(E, q) - 1) for q in range(1, 401)) for E in (3, 4, 5, 8)})
print("E=4 r=3: D=%d M-1=%d" % (D(4, 3), M_E(4, 3) - 1))
print("a | tri | M_3 | D_3+a | D_4+a | D_5+a")
for a in (4, 6, 10, 20, 50, 100):
    print(a, (a + 1) * (a + 2) // 2, M_E(3, a), D(3, a) + a, D(4, a) + a, D(5, a) + a)
