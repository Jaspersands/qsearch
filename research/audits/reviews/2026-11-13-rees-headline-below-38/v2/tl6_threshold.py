"""v2: exact-rational check of the Lemma SM existence threshold for TL6 = RC(6; Z_6 -> {0})
(D = r = 6, k = 1) and the band constant 1 - Phi(p_D).  sqrt(p) is bounded below by
isqrt(p * 10^40) / 10^20, which makes gamma (hence Phi) an upper bound.  AI-written, pending review."""
from fractions import Fraction as Fr
from math import isqrt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from certs import primes_upto
def Phi_up(p, D=6, r=6, k=1):
    sq = Fr(isqrt(p * 10 ** 40), 10 ** 20)            # <= sqrt(p)
    gam = (1 + Fr((D - 1) ** 2) / sq) * Fr(p, p - 1) ** 2
    h = Fr(p - 1, D)
    E0 = h * (k * h / p) ** (r - 1); Ej = k * h * (k * h / p) ** (r - 1)
    r0 = 1 / E0 + gam ** (r - 1); rj = 1 / Ej + gam ** (r - 1)
    return (1 - 1 / r0) + (D - 1) * (1 - 1 / rj)
def Phi_lo(p, D=6, r=6, k=1):
    sq = Fr(isqrt(p * 10 ** 40) + 1, 10 ** 20)        # >= sqrt(p)
    gam = (1 + Fr((D - 1) ** 2) / sq) * Fr(p, p - 1) ** 2
    h = Fr(p - 1, D)
    E0 = h * (k * h / p) ** (r - 1); Ej = k * h * (k * h / p) ** (r - 1)
    r0 = 1 / E0 + gam ** (r - 1); rj = 1 / Ej + gam ** (r - 1)
    return (1 - 1 / r0) + (D - 1) * (1 - 1 / rj)
T = 837384
print('Phi_up(T) < 1:', Phi_up(T) < 1, float(Phi_up(T)), ' Phi_lo(T-1) >= 1:', Phi_lo(T - 1) >= 1, float(Phi_lo(T - 1)))
pD = next(q for q in primes_upto(T + 2000) if q >= T and q % 6 == 1)
print('least prime = 1 mod 6 at or above T:', pD, ' 1 - Phi_up(pD) =', float(1 - Phi_up(pD)))
q2520 = next(q for q in primes_upto(T + 30000) if q >= T and q % 2520 == 1)
print('least prime = 1 mod 2520 above T:', q2520, ' 1 - Phi_up =', float(1 - Phi_up(q2520)))
