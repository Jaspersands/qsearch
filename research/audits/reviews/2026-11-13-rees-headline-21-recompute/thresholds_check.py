"""Recompute Table tab:sm-thresholds from Lemma lem:sm's closed forms (mpmath, 60 digits)."""
from mpmath import mp, mpf, sqrt
mp.dps = 60
def forms(p, D, r, k):
    p = mpf(p); h = (p - 1) / D
    g = (1 + (D - 1) ** 2 / sqrt(p)) * p ** 2 / (p - 1) ** 2
    mu0 = h * (k * h / p) ** (r - 1); mu1 = k * h * (k * h / p) ** (r - 1)
    r0 = 1 / mu0 + g ** (r - 1); r1 = 1 / mu1 + g ** (r - 1)
    Phi = (1 - 1 / r0) + (D - 1) * (1 - 1 / r1)
    Psi = 4 * (r0 - 1) + 4 * (D - 1) * (r1 - 1)
    return Phi, Psi
def least_int(pred, lo=3, hi=10**12):
    assert pred(hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid): hi = mid
        else: lo = mid + 1
    return lo
rows = [("TL3", 3, 3, 1), ("TL4", 4, 4, 1), ("TL5", 5, 5, 1), ("TW9", 9, 3, 1), ("U7", 7, 7, 2)]
claimed = {"TL3": (430, 39096), "TL4": (9395, 778545), "TL5": (99745, 6922583), "TW9": (1124521, 85628629), "U7": (1995734, 149308802)}
for name, D, r, k in rows:
    te = least_int(lambda x: forms(x, D, r, k)[0] < 1)
    ts = least_int(lambda x: forms(x, D, r, k)[1] <= mpf(1) / 2)
    # monotonicity spot-check on a grid
    import random
    mono = all(forms(x, D, r, k)[0] >= forms(x + 1, D, r, k)[0] for x in [te - 5, te - 1, te, te + 10, 10 * te])
    print(name, (D, r, k), "T_exist", te, "T_samp", ts, "claimed", claimed[name], "match", (te, ts) == claimed[name], "mono", mono)
