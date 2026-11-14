"""Draft helper check (2026-11-14): Lemma plus-sm closed forms at the six steps of
Schedule 1H+. Recomputes Phi at T_exist-1, T_exist and at p_D = least prime = 1 (mod D)
>= T_exist, and Psi at T_samp-1, T_samp, in 60-digit mpmath. Falsifier only."""
from mpmath import mp, mpf, sqrt
mp.dps = 60
ROWS = {"TL3": (3, 3, 1, 430, 39096), "TL4": (4, 4, 1, 9395, 778545),
        "TL5": (5, 5, 1, 99745, 6922583), "TL6": (6, 6, 1, 837384, 40924516),
        "TW9": (9, 3, 1, 1124521, 85628629), "U7": (7, 7, 2, 1995734, 149308802)}
def rho(p, D, r, k):
    p = mpf(p); h = (p - 1) / D
    g = (1 + (D - 1) ** 2 / sqrt(p)) * p ** 2 / (p - 1) ** 2
    m0 = h * (k * h / p) ** (r - 1); m1 = k * h * (k * h / p) ** (r - 1)
    return 1 / m0 + g ** (r - 1), 1 / m1 + g ** (r - 1)
def Phi(p, D, r, k):
    r0, r1 = rho(p, D, r, k); return (1 - 1 / r0) + (D - 1) * (1 - 1 / r1)
def Psi(p, D, r, k):
    r0, r1 = rho(p, D, r, k); return 4 * (r0 - 1) + 4 * (D - 1) * (r1 - 1)
def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
for name, (D, r, k, Te, Ts) in ROWS.items():
    pD = Te
    while not (isprime(pD) and pD % D == 1): pD += 1
    print(name, "Phi(Te-1)=%.6f Phi(Te)=%.6f" % (Phi(Te - 1, D, r, k), Phi(Te, D, r, k)),
          "pD=%d 1-Phi(pD)=%.4e" % (pD, 1 - Phi(pD, D, r, k)),
          "Psi(Ts-1)=%.6f Psi(Ts)=%.6f" % (Psi(Ts - 1, D, r, k), Psi(Ts, D, r, k)),
          "D*r*Ts/(1-Phi(pD))=%.3e" % (D * r * Ts / (1 - Phi(pD, D, r, k))))
