"""First-moment predictions (independent-cell heuristic, with the clump sizes of each family's
symmetry group) and Weil / square-root thresholds for the structured families of the report.
Heuristic numbers only (labelled [heuristic] in the report), except the one-variable Weil
thresholds W1, which are the explicit bounds of Section 5 of the report.
Usage: python predictions.py
"""
import math


def solve_mean(f, target, lo=2.0, hi=1e300):
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return hi


for k in (5, 7, 11, 13, 17, 23, 31):
    kk = float(k) ** k
    fr = math.factorial(k) / kk          # P(random map Z_k -> Z_k is a bijection)
    F1 = lambda p: p * (k - 2) / (2 * kk)                      # orbit family, fixed chart
    # orbit family with all charts: solutions for one (C1) parameter clump are correlated, so the
    # relevant mean is (# C1 clumps of 2k parameters t) * P(clump has a good chart):
    # P = 1 - (2/k) exp(-p fr^2 / k)  (fixed chart good w.p. (k-2)/k; ~p fr^2/k generic z-orbits)
    F2 = lambda p: p / (2 * float(k) ** (k - 1)) * (1 - (2.0 / k) * math.exp(-min(700, p * fr * fr / k)))
    F3 = lambda p: p * p * (k - 2) / (4 * float(k) ** (2 * k - 2))  # open progressions
    rows = []
    for name, f in (("F1", F1), ("F2all", F2), ("F3", F3)):
        rows.append("%s m=1:%.3g m=5:%.3g" % (name, solve_mean(f, 1), solve_mean(f, 5)))
    TA = (k - 1) * kk
    # square-root thresholds kappa^(2c/v) with c in kappa-units:
    c_F2 = (k - 2) + 2 * math.log(1 / fr, k)
    sq = {"F1": float(k) ** (2 * (k - 2)), "F2": float(k) ** c_F2,
          "F3": float(k) ** (2 * k - 2), "full": float(k) ** (k + 1)}
    # one-variable Weil thresholds (report Section 5, subgroup-indicator form):
    # F1: sqrt p > 3(k-1) k^(k-1)/(k-2);  F3 (for each fixed rho): sqrt p > 3(2k-2) k^(2k-2)/(k-2)
    W1_F1 = (3 * (k - 1) * float(k) ** (k - 1) / (k - 2)) ** 2
    W1_F3 = (3 * (2 * k - 2) * float(k) ** (2 * k - 2) / (k - 2)) ** 2
    print("k=%d  T_A~(k-1)k^k=%.3g  k^((k+1)/2)=%.3g" % (k, TA, float(k) ** ((k + 1) / 2)))
    print("   first-moment crossings (mean # distinct solutions = 1 / = 5): " + "; ".join(rows))
    print("   square-root thresholds k^(2c/v): " + ", ".join("%s %.3g" % kv for kv in sq.items()))
    print("   one-variable Weil: F1 %.3g, F3 %.3g" % (W1_F1, W1_F3))
    print("   exponents log_k: F1 %.2f  F2all %.2f  F3 %.2f  vs T_A %.2f" % (
        math.log(solve_mean(F1, 1), k), math.log(solve_mean(F2, 1), k),
        math.log(solve_mean(F3, 1), k), math.log(TA, k)))
