"""Referee variant of verify_corollary.py condition (A): replaces the hard-coded 1.0025 (valid only for
L0 >= 6) by 1/(1-e^{-L0}), and also checks the second-error exponent at L0 is < 0 margin-wise."""
import sys, math
L0 = float(sys.argv[1]); klo = int(sys.argv[2]); khi = int(sys.argv[3])
c0 = L0 * math.exp(-L0); a = 1 / (1 - math.exp(-L0))
sec = -(4 * (math.log(4) - 1) - 1) * L0 - (math.log(4) - 1)   # exponent per R of the second error
last_bad = None
for k in range(klo, khi + 1):
    lk = math.log(k)
    if lk + 1.5 > L0:
        KA = 16 * c0 * k + 20 * (lk + 1.5) + 1
        lhs = (k / 2 - KA) * lk
        rhs = math.log(3.1 * k * KA) + 8 * c0 * k + 10 * (lk + 1.5) + a * k * math.exp(-L0) + math.log(3)
        if not (KA < k / 2 and lhs >= rhs + 1.0):
            last_bad = k
print(f"L0={L0} main-term const={a:.5f} second-error exponent/R={sec:.4f} last (A) failure in [{klo},{khi}]: {last_bad}")
