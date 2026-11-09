"""Check Lemma (T_R closed-form bound): for D >= 4 and 2 <= r <= D,
   T_R(D,r) <= P(D,r) := max(4 D^(r+1), 4 r^2 D^5),
by evaluating the T_R condition lhs(D,r,P) < 1/(D-1) at P and comparing with the bisected
T_R.  Also prints the constants used in the written proof (0.2526/D + 0.1812/D)."""
from mpmath import mpf
from thresholds import lhs, TR
worst = 0
for D in range(4, 65):
    for r in range(2, D+1):
        P = max(4*mpf(D)**(r+1), 4*mpf(r)**2*mpf(D)**5)
        val = lhs(D, r, P) * D          # proof claims lhs(P) <= 0.4338/D
        worst = max(worst, val)
        assert lhs(D, r, P) < mpf(1)/(D-1), (D, r)
        if r <= 8 and D <= 32 and D % r == 0:
            t = TR(D, r)
            assert t <= P
            print(f"D={D:3d} r={r}  T_R={float(t):.4g}  P={float(P):.4g}  ratio={float(t/P):.3f}")
print("max over D<=64, 2<=r<=D of D*lhs(D,r,P(D,r)) =", float(worst), "(proof bound 0.4338)")
