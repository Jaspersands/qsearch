"""D_E(q): worst greedy forward cost.  Checks D_3(q) = floor((q+2)^2/4) (q >= 1) and
D_E(q) <= q^2/(2(E-1)) + q(1/(E-1) + 5/2); prints the budget D_E(a) + a against the
triangular count (a+1)(a+2)/2, M_E(a) and Chevalley-Warning."""
import sys
sys.setrecursionlimit(10000)
from sss import worst_forward_cost

ok = True
for E in range(2, 13):
    memo = {}
    for q in range(1, 401):
        D = worst_forward_cost(q, E, memo)
        if E == 3 and D != (q + 2) ** 2 // 4:
            ok = False; print("D3 mismatch", q, D)
        if D > q * q / (2 * (E - 1)) + q * (1 / (E - 1) + 2.5) + 1e-9:
            ok = False; print("bound fails", E, q, D)
print("closed form and bound for q<=400, E<=12:", ok)
def ME(a, E):
    q, M = a, 0
    while q >= 1:
        M += q + 1; q -= min(E - 1, q)
    return M + 1
print("a  triangular  M3(iid)  D3+a(worst,GP)  D4+a  D5+a  CW(k=2) CW(k=3)")
for a in (2, 3, 4, 5, 6, 8, 10, 12, 20, 50, 100):
    print(a, (a + 1) * (a + 2) // 2, ME(a, 3), worst_forward_cost(a, 3, {}) + a,
          worst_forward_cost(a, 4, {}) + a, worst_forward_cost(a, 5, {}) + a, 2 * a + 1, 3 * a + 1)
