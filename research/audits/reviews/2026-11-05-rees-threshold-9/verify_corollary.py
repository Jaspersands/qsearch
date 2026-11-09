"""Checks the three explicit sufficient conditions (A), (B), (C) of Corollary 3 (report Sec. 2.3)
for every k in [k_lo, k_hi], in floating point with a safety margin, and prints the first k from
which all three hold for every larger k in the range.

(A) Lambda in [L0, ln k + 1.5] (only if ln k + 1.5 > L0), R + 1 = 2*ceil(2 mu + 2) <= 4 mu + 6,
    K = ceil(4 R Lambda) <= Kbar_A := 16 c0 k + 20 (ln k + 1.5) + 1, c0 = L0 e^{-L0} (= max of Lambda e^{-Lambda}):
      (k/2 - Kbar_A) ln k  >=  ln(3.1 k Kbar_A) + 8 c0 k + 10 (ln k + 1.5) + c_main k e^{-L0} + ln 3   [+ margin],
      c_main = 1/(1 - e^{-L0}) (1.00248 at L0 = 6, 1.00410 at L0 = 5.5)
(B) Lambda in [ln k + 1.5, sqrt(8k)], R = 1, K = ceil(3.6 Lambda) <= Kbar_B := 3.6 sqrt(8k) + 1:
      ln 3.1 + 2 ln k + ln Kbar_B + (Kbar_B - k/2) ln k + sqrt(8k)  <=  ln 0.5
(C) Lambda >= sqrt(8k): TH2 Theorem 5 with m = 2:
      3/8 + k (8k)^{-3/2} + k * W2max * dTH2 < 1, W2max = 16 + 24/L + 11/L^2 + 1/L^3 at L = sqrt(8k),
      dTH2 = 2(k-1)(8 k^4/sqrt(p) + 4/p) at p = sqrt(8k) k^k (upper bound for TH2's delta_k, k<=4).
Also checks TH2's side condition (k-1) eps* <= 1, eps* = 8 k^4/sqrt(p).  All logs natural.  Usage: python verify_corollary.py L0 k_lo k_hi
"""
import sys, math

L0 = float(sys.argv[1]); klo = int(sys.argv[2]); khi = int(sys.argv[3])
c0 = L0 * math.exp(-L0)
cmain = 1 / (1 - math.exp(-L0)) + 1e-9   # (1-u)^k >= exp(-cmain*mu) for u <= e^{-L0}
first_bad = None
last_bad = None
for k in range(klo, khi + 1):
    lk = math.log(k)
    okA = True
    if lk + 1.5 > L0:
        KA = 16 * c0 * k + 20 * (lk + 1.5) + 1
        lhs = (k / 2 - KA) * lk
        rhs = math.log(3.1 * k * KA) + 8 * c0 * k + 10 * (lk + 1.5) + cmain * k * math.exp(-L0) + math.log(3)
        okA = (KA < k / 2) and lhs >= rhs + 1.0
    Lmax = math.sqrt(8 * k)
    KB = 3.6 * Lmax + 1
    okB = (math.log(3.1) + 2 * lk + math.log(KB) + (KB - k / 2) * lk + Lmax) <= math.log(0.5) - 1.0
    # (C): log sqrt(p) = 0.5*(ln sqrt(8k) + k ln k)
    lsp = 0.5 * (0.5 * math.log(8 * k) + k * lk)
    d = 2 * (k - 1) * (8 * math.exp(4 * lk - lsp) + 4 * math.exp(-2 * lsp))
    W2 = 16 + 24 / Lmax + 11 / Lmax ** 2 + 1 / Lmax ** 3
    epsstar = 8 * math.exp(4 * lk - lsp)            # TH2's eps* for m = 2
    okC = ((k - 1) * epsstar <= 1) and (3 / 8 + k * (8 * k) ** -1.5 + k * W2 * d < 0.9)
    if not (okA and okB and okC):
        last_bad = (k, okA, okB, okC)
        if first_bad is None:
            first_bad = last_bad
print(f"L0={L0} range [{klo},{khi}] first failure={first_bad} last failure={last_bad}")
print(f"=> all of (A),(B),(C) hold for every k in [{(last_bad[0]+1) if last_bad else klo}, {khi}]")
