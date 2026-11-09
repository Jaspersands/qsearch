"""Cor. codim(ii) via Thm free-coordinate(iii): per-run query bound at the worst
terminal shape c_J = 2k-1, g_d = k(k+1)/2 (an upper bound for every grade), error 1/3,
using the arity bound M_d <= (1+2 log2 c) g + 3 log2(216 (c-1) S n_d) + 3 of the proof of
Prop. fc-uniform(b) (linear grades have M_d = g+1, smaller).  Also the crude bound
c S (4 alpha c)^(c-1) quoted in the codimension appendix.  AI-checked, pending human review.
"""
from math import log2, ceil
worst = 0
for k in list(range(2, 41)) + [60, 100, 200]:
    c = 2 * k - 1
    g = k * (k + 1) // 2
    S = g + 2
    ln = 0.0
    Mmax = 0
    for d in range(2, c + 1):
        M = (1 + 2 * log2(c)) * g + 3 * (log2(216 * (c - 1) * S) + ln) + 3
        Mmax = max(Mmax, M)
        ln += log2(M)
    lq = log2(c * S) + ln
    alpha = (1 + 2 * log2(c)) * g + 3 * log2(216 * c * S) + 3
    crude = log2(c * S) + (c - 1) * log2(4 * alpha * c)
    r1 = lq / (k * log2(k + 2))
    r2 = crude / (k * log2(k + 2))
    ra = Mmax / (k * k * log2(k + 2))
    worst = max(worst, r2)
    if k in (2, 3, 5, 10, 20, 40, 100, 200):
        print(f"k={k:3d}: log2 Q_run={lq:9.1f} (/k log2(k+2) = {r1:.2f}); crude bound {crude:9.1f} "
              f"(ratio {r2:.2f}); max M_d / (k^2 log2(k+2)) = {ra:.2f}")
print("max crude ratio over tested k: %.2f (bounded, consistent with 2^{O(k log(k+2))})" % worst)
