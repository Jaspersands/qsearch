"""Theorems O1 and O1' (pattern-blind certificates): the largest p at which failure is forced.
O1  (term-by-term, L1):  fails whenever kappa^(kappa(kappa-1)) >= 2 p^(kappa-1)
                          i.e. p <= P1 = kappa^kappa * 2^(-1/(kappa-1)).
O1' (Parseval/L2 with the (kappa!)^2/kappa relabelling orbit O of the Rees pattern):
     fails whenever kappa^(kappa(kappa-1)) >= p^(kappa-1) (1 + sqrt(|O| / kappa^kappa)),
     i.e. p <= P2 = kappa^kappa / (1 + sqrt(|O|/kappa^kappa))^(1/(kappa-1)).
Both use only N_c >= p h^kappa for row-constant c and S_0 <= p^kappa (p-1)^kappa.
Usage: blind_bounds.py"""
from mpmath import mp, mpf, factorial, sqrt, log
mp.dps = 40
print("kappa | P1/kappa^kappa | P2 | P2/kappa^kappa | log_kappa P2 - kappa")
for K in list(range(3, 21)) + [30, 50, 100]:
    KK = mpf(K) ** K
    O = factorial(K) ** 2 / K
    P1 = KK * mpf(2) ** (-mpf(1) / (K - 1))
    P2 = KK / (1 + sqrt(O / KK)) ** (mpf(1) / (K - 1))
    print(f"{K} | {float(P1 / KK):.4f} | {float(P2):.4g} | {float(P2 / KK):.4f} | {float(log(P2) / log(K) - K):.4f}")
